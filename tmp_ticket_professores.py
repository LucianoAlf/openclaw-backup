import os, json, requests
from pathlib import Path
for line in Path('/root/.openclaw/workspace/.env').read_text().splitlines():
    if not line or line.strip().startswith('#') or '=' not in line: continue
    k,v=line.split('=',1); os.environ.setdefault(k, v.strip().strip('"').strip("'"))
url=os.environ['LAREPORT_SUPABASE_URL'].rstrip('/'); key=os.environ.get('LAREPORT_SUPABASE_SERVICE_ROLE') or os.environ['LAREPORT_SUPABASE_ANON_KEY']
headers={'apikey':key,'Authorization':'Bearer '+key,'Content-Type':'application/json'}
sql = """
WITH prof AS (
  SELECT id AS professor_id, lower(trim(nome)) AS nome_key, nome AS professor_nome
  FROM professores
  WHERE ativo = true
), base AS (
  SELECT
    a.id, a.nome, u.nome AS unidade, c.nome AS curso, a.status, a.valor_parcela,
    a.is_segundo_curso, COALESCE(c.is_projeto_banda,false) AS is_projeto_banda,
    tm.nome AS tipo_matricula, tm.codigo, tm.entra_ticket_medio, tm.conta_como_pagante,
    prof.professor_id,
    prof.professor_nome,
    (a.status='ativo' AND COALESCE(tm.entra_ticket_medio,false)=true) AS entra_ticket_atual
  FROM alunos a
  JOIN prof ON lower(trim(a.nome)) = prof.nome_key
  LEFT JOIN unidades u ON u.id=a.unidade_id
  LEFT JOIN cursos c ON c.id=a.curso_id
  LEFT JOIN tipos_matricula tm ON tm.id=a.tipo_matricula_id
)
SELECT *
FROM base
WHERE entra_ticket_atual = true
ORDER BY valor_parcela ASC, unidade, nome;
"""
r=requests.post(url+'/rest/v1/rpc/executar_query_auditoria',headers=headers,json={'p_sql':sql},timeout=60)
print('status', r.status_code)
print(json.dumps(r.json(),ensure_ascii=False,indent=2))
