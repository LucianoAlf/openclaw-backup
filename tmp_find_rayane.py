import os, json, requests
from pathlib import Path
for line in Path('/root/.openclaw/workspace/.env').read_text().splitlines():
    if not line or line.strip().startswith('#') or '=' not in line: continue
    k,v=line.split('=',1); os.environ.setdefault(k, v.strip().strip('"').strip("'"))
url=os.environ['LAREPORT_SUPABASE_URL'].rstrip('/'); key=os.environ.get('LAREPORT_SUPABASE_SERVICE_ROLE') or os.environ['LAREPORT_SUPABASE_ANON_KEY']
headers={'apikey':key,'Authorization':'Bearer '+key,'Content-Type':'application/json'}
def q(label, sql):
 print('\n##',label)
 r=requests.post(url+'/rest/v1/rpc/executar_query_auditoria',headers=headers,json={'p_sql':sql},timeout=60)
 print('status',r.status_code)
 try: print(json.dumps(r.json(),ensure_ascii=False,indent=2))
 except Exception: print(r.text)
q('tables with nome-like columns', """
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema='public'
  AND data_type IN ('character varying','text')
  AND column_name ILIKE '%nome%'
ORDER BY table_name, ordinal_position;
""")
q('rayane in likely people tables', """
SELECT 'professores' AS tabela, id::text, nome, ativo::text AS status FROM professores WHERE lower(nome) LIKE lower('%Rayane%')
UNION ALL
SELECT 'alunos' AS tabela, id::text, nome, status::text FROM alunos WHERE lower(nome) LIKE lower('%Rayane%')
ORDER BY tabela, nome;
""")
