import os, json, requests
from pathlib import Path
for line in Path('/root/.openclaw/workspace/.env').read_text().splitlines():
    if not line or line.strip().startswith('#') or '=' not in line: continue
    k,v=line.split('=',1)
    os.environ.setdefault(k, v.strip().strip('"').strip("'"))
url=os.environ['LAREPORT_SUPABASE_URL'].rstrip('/')
key=os.environ.get('LAREPORT_SUPABASE_SERVICE_ROLE') or os.environ['LAREPORT_SUPABASE_ANON_KEY']
headers={'apikey':key,'Authorization':'Bearer '+key,'Content-Type':'application/json'}
def q(label, sql):
    print('\n## '+label)
    r=requests.post(url+'/rest/v1/rpc/executar_query_auditoria',headers=headers,json={'p_sql':sql},timeout=60)
    print('status', r.status_code)
    try: print(json.dumps(r.json(),ensure_ascii=False,indent=2))
    except Exception: print(r.text)

q('alunos Leonardo/Rayane', """
SELECT
  a.id,
  a.nome,
  u.nome AS unidade,
  c.nome AS curso,
  a.status,
  a.valor_parcela,
  a.is_segundo_curso,
  COALESCE(c.is_projeto_banda,false) AS is_projeto_banda,
  COALESCE(c.is_coral,false) AS is_coral,
  tm.id AS tipo_id,
  tm.nome AS tipo_matricula,
  tm.codigo AS tipo_codigo,
  tm.conta_como_pagante,
  tm.entra_ticket_medio,
  p.nome AS professor_atual,
  (a.status = 'ativo' AND COALESCE(tm.entra_ticket_medio,false) = true) AS entra_ticket_dashboard_atual,
  (a.status = 'ativo' AND COALESCE(tm.entra_ticket_medio,false) = true AND COALESCE(a.valor_parcela,0) > 0) AS entra_ticket_dashboard_pos_zero
FROM alunos a
LEFT JOIN unidades u ON u.id = a.unidade_id
LEFT JOIN cursos c ON c.id = a.curso_id
LEFT JOIN tipos_matricula tm ON tm.id = a.tipo_matricula_id
LEFT JOIN professores p ON p.id = a.professor_atual_id
WHERE lower(a.nome) LIKE lower('%Leonardo Castro%')
   OR lower(a.nome) LIKE lower('%Rayane Bianca%')
ORDER BY u.nome, a.nome, a.id;
""")
q('professores com nomes', """
SELECT id, nome, unidade_id, ativo
FROM professores
WHERE lower(nome) LIKE lower('%Leonardo Castro%')
   OR lower(nome) LIKE lower('%Rayane Bianca%')
ORDER BY nome;
""")
q('tipos matricula', """
SELECT id, nome, codigo, conta_como_pagante, entra_ticket_medio, entra_ltv, entra_churn
FROM tipos_matricula
ORDER BY id;
""")
q('menores positivos que entram ticket atual', """
SELECT
  a.nome, u.nome AS unidade, c.nome AS curso, a.valor_parcela,
  tm.nome AS tipo_matricula, tm.codigo, tm.entra_ticket_medio,
  a.status, a.is_segundo_curso,
  COALESCE(c.is_projeto_banda,false) AS is_projeto_banda,
  COALESCE(c.is_coral,false) AS is_coral
FROM alunos a
LEFT JOIN unidades u ON u.id = a.unidade_id
LEFT JOIN cursos c ON c.id = a.curso_id
LEFT JOIN tipos_matricula tm ON tm.id = a.tipo_matricula_id
WHERE a.status='ativo'
  AND COALESCE(tm.entra_ticket_medio,false)=true
  AND COALESCE(a.valor_parcela,0) > 0
ORDER BY a.valor_parcela ASC, a.nome
LIMIT 20;
""")
q('impacto ticket atual vs excluindo bolsistas', """
WITH base AS (
  SELECT a.*, u.nome AS unidade, c.nome AS curso, COALESCE(c.is_projeto_banda,false) AS is_projeto_banda, COALESCE(c.is_coral,false) AS is_coral,
         tm.nome AS tipo_matricula, tm.codigo, tm.entra_ticket_medio
  FROM alunos a
  LEFT JOIN unidades u ON u.id=a.unidade_id
  LEFT JOIN cursos c ON c.id=a.curso_id
  LEFT JOIN tipos_matricula tm ON tm.id=a.tipo_matricula_id
  WHERE a.status='ativo'
), agg AS (
  SELECT
    unidade,
    COUNT(*) FILTER (WHERE COALESCE(entra_ticket_medio,false)=true) AS qtd_dashboard_atual,
    ROUND(AVG(valor_parcela) FILTER (WHERE COALESCE(entra_ticket_medio,false)=true),2) AS ticket_dashboard_atual,
    COUNT(*) FILTER (
      WHERE COALESCE(entra_ticket_medio,false)=true
        AND COALESCE(valor_parcela,0) > 0
        AND COALESCE(is_segundo_curso,false)=false
        AND is_projeto_banda=false
        AND is_coral=false
        AND COALESCE(codigo,'') NOT ILIKE '%BOLS%'
        AND COALESCE(tipo_matricula,'') NOT ILIKE '%Bolsista%'
    ) AS qtd_canonico_sem_bolsista,
    ROUND(AVG(valor_parcela) FILTER (
      WHERE COALESCE(entra_ticket_medio,false)=true
        AND COALESCE(valor_parcela,0) > 0
        AND COALESCE(is_segundo_curso,false)=false
        AND is_projeto_banda=false
        AND is_coral=false
        AND COALESCE(codigo,'') NOT ILIKE '%BOLS%'
        AND COALESCE(tipo_matricula,'') NOT ILIKE '%Bolsista%'
    ),2) AS ticket_canonico_sem_bolsista
  FROM base
  GROUP BY unidade
)
SELECT * FROM agg ORDER BY unidade;
""")
