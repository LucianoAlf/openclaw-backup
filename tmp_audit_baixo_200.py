import os,json,requests,csv
from pathlib import Path
from datetime import datetime
for line in Path('/root/.openclaw/workspace/.env').read_text().splitlines():
    if not line or line.startswith('#') or '=' not in line: continue
    k,v=line.split('=',1); os.environ[k]=v.strip().strip('"').strip("'")
url=os.environ['LAREPORT_SUPABASE_URL'].rstrip('/')
key=os.environ.get('LAREPORT_SUPABASE_SERVICE_ROLE') or os.environ['LAREPORT_SUPABASE_ANON_KEY']
h={'apikey':key,'Authorization':'Bearer '+key,'Content-Type':'application/json'}
def q(sql):
    r=requests.post(url+'/rest/v1/rpc/executar_query_auditoria',headers=h,json={'p_sql':sql},timeout=90)
    if r.status_code>=400:
        raise SystemExit(f'{r.status_code} {r.text}')
    return r.json()

sql = r"""
WITH prof AS (
  SELECT lower(trim(nome)) AS nome_key, id AS professor_id, nome AS professor_nome
  FROM professores
  WHERE ativo = true
), colab AS (
  SELECT lower(trim(nome)) AS nome_key, id AS colaborador_id, nome AS colaborador_nome, tipo AS colaborador_tipo, ativo AS colaborador_ativo
  FROM colaboradores
), low AS (
  SELECT
    a.id,
    a.nome,
    lower(trim(a.nome)) AS nome_key,
    u.nome AS unidade,
    c.nome AS curso,
    a.status,
    a.valor_parcela,
    a.valor_passaporte,
    a.status_pagamento,
    a.tipo_aluno,
    a.tipo_matricula_id,
    tm.nome AS tipo_matricula,
    tm.codigo AS tipo_codigo,
    tm.conta_como_pagante,
    tm.entra_ticket_medio,
    a.is_segundo_curso,
    COALESCE(c.is_projeto_banda,false) AS is_projeto_banda,
    p.nome AS professor_atual,
    a.data_matricula,
    a.data_saida
  FROM alunos a
  LEFT JOIN unidades u ON u.id=a.unidade_id
  LEFT JOIN cursos c ON c.id=a.curso_id
  LEFT JOIN tipos_matricula tm ON tm.id=a.tipo_matricula_id
  LEFT JOIN professores p ON p.id=a.professor_atual_id
  WHERE a.status IN ('ativo','trancado')
    AND COALESCE(a.valor_parcela,0) > 0
    AND COALESCE(a.valor_parcela,0) < 200
), joined AS (
  SELECT
    low.*,
    prof.professor_id,
    prof.professor_nome,
    colab.colaborador_id,
    colab.colaborador_nome,
    colab.colaborador_tipo,
    colab.colaborador_ativo,
    (low.status IN ('ativo','trancado') AND COALESCE(low.conta_como_pagante,false)=true) AS conta_pagante_atual,
    (low.status IN ('ativo','trancado') AND COALESCE(low.entra_ticket_medio,false)=true) AS entra_ticket_atual,
    CASE
      WHEN COALESCE(low.tipo_codigo,'') IN ('BOLSISTA_INT','BOLSISTA_PARC','BANDA') THEN 'OK_EXCLUIDO_PELO_TIPO'
      WHEN COALESCE(low.is_projeto_banda,false) THEN 'OK_BANDA_PROJETO'
      WHEN prof.professor_id IS NOT NULL THEN 'RISCO_PROFESSOR_COMO_PAGANTE'
      WHEN colab.colaborador_id IS NOT NULL THEN 'RISCO_COLABORADOR_COMO_PAGANTE'
      WHEN COALESCE(low.tipo_codigo,'')='REGULAR' AND COALESCE(low.conta_como_pagante,false)=true THEN 'RISCO_REGULAR_ABAIXO_200'
      WHEN COALESCE(low.tipo_codigo,'')='SEGUNDO_CURSO' THEN 'SEGUNDO_CURSO_ABAIXO_200_VERIFICAR'
      ELSE 'VERIFICAR'
    END AS classificacao_auditoria
  FROM low
  LEFT JOIN prof ON prof.nome_key=low.nome_key
  LEFT JOIN colab ON colab.nome_key=low.nome_key
)
SELECT *
FROM joined
ORDER BY
  CASE classificacao_auditoria
    WHEN 'RISCO_PROFESSOR_COMO_PAGANTE' THEN 1
    WHEN 'RISCO_COLABORADOR_COMO_PAGANTE' THEN 2
    WHEN 'RISCO_REGULAR_ABAIXO_200' THEN 3
    WHEN 'SEGUNDO_CURSO_ABAIXO_200_VERIFICAR' THEN 4
    ELSE 5
  END,
  unidade, valor_parcela, nome, curso;
"""
rows=q(sql)
outdir=Path('/root/.openclaw/workspace/outputs/sol-business-rules-audit')
outdir.mkdir(parents=True,exist_ok=True)
stamp=datetime.utcnow().strftime('%Y%m%d-%H%M%S')
json_path=outdir/f'auditoria_alunos_abaixo_200_{stamp}.json'
csv_path=outdir/f'auditoria_alunos_abaixo_200_{stamp}.csv'
md_path=outdir/f'auditoria_alunos_abaixo_200_{stamp}.md'
json_path.write_text(json.dumps(rows,ensure_ascii=False,indent=2))
if rows:
    with csv_path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

from collections import Counter,defaultdict
cnt=Counter(r['classificacao_auditoria'] for r in rows)
by_unit=defaultdict(int)
for r in rows: by_unit[r['unidade']]+=1
risk=[r for r in rows if str(r['classificacao_auditoria']).startswith('RISCO') or r['classificacao_auditoria']=='SEGUNDO_CURSO_ABAIXO_200_VERIFICAR']
lines=[]
lines.append('# Auditoria — alunos com parcela positiva abaixo de R$200\n')
lines.append(f'Gerado em UTC: {datetime.utcnow().isoformat(timespec="seconds")}\n')
lines.append('Escopo: SELECT-only. Alunos com status ativo/trancado, valor_parcela > 0 e < 200.\n')
lines.append('## Resumo\n')
lines.append(f'- Total de linhas/matrículas abaixo de R$200: **{len(rows)}**')
for k,v in cnt.most_common(): lines.append(f'- {k}: **{v}**')
lines.append('\nPor unidade:')
for k in sorted(by_unit): lines.append(f'- {k}: **{by_unit[k]}**')
lines.append('\n## Casos de risco/prioridade\n')
if not risk: lines.append('Nenhum caso de risco pelo critério automático.')
for r in risk:
    lines.append(f"- **{r['nome']}** — {r['unidade']} — {r['curso']} — R${r['valor_parcela']} — tipo `{r['tipo_matricula']}`/`{r['tipo_codigo']}` — conta_pagante={r['conta_pagante_atual']} — entra_ticket={r['entra_ticket_atual']} — classificação: **{r['classificacao_auditoria']}**")
    extra=[]
    if r.get('professor_nome'): extra.append(f"professor cadastrado: {r['professor_nome']}")
    if r.get('colaborador_nome'): extra.append(f"colaborador: {r['colaborador_nome']} ({r.get('colaborador_tipo')}, ativo={r.get('colaborador_ativo')})")
    if extra: lines.append('  - ' + '; '.join(extra))
lines.append('\n## Lista completa\n')
lines.append('| Nome | Unidade | Curso | Valor | Tipo | Pagante? | Ticket? | Classificação |')
lines.append('|---|---|---:|---:|---|---:|---:|---|')
for r in rows:
    lines.append(f"| {r['nome']} | {r['unidade']} | {r['curso']} | R${r['valor_parcela']} | {r['tipo_matricula']} | {r['conta_pagante_atual']} | {r['entra_ticket_atual']} | {r['classificacao_auditoria']} |")
md_path.write_text('\n'.join(lines))
print(json.dumps({'count':len(rows),'summary':cnt,'by_unit':dict(by_unit),'risk_count':len(risk),'json':str(json_path),'csv':str(csv_path),'md':str(md_path),'rows':rows},ensure_ascii=False,indent=2))
