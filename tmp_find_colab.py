import os,json,requests
from pathlib import Path
for line in Path('/root/.openclaw/workspace/.env').read_text().splitlines():
 if not line or line.strip().startswith('#') or '=' not in line: continue
 k,v=line.split('=',1); os.environ.setdefault(k,v.strip().strip('"').strip("'"))
url=os.environ['LAREPORT_SUPABASE_URL'].rstrip('/'); key=os.environ.get('LAREPORT_SUPABASE_SERVICE_ROLE') or os.environ['LAREPORT_SUPABASE_ANON_KEY']
headers={'apikey':key,'Authorization':'Bearer '+key,'Content-Type':'application/json'}
sql="""
SELECT 'colaboradores' AS tabela, id::text, nome, status::text, cargo::text
FROM colaboradores
WHERE lower(nome) LIKE lower('%Rayane%') OR lower(nome) LIKE lower('%Leonardo Castro%')
ORDER BY nome;
"""
r=requests.post(url+'/rest/v1/rpc/executar_query_auditoria',headers=headers,json={'p_sql':sql},timeout=60)
print(r.status_code); print(json.dumps(r.json(),ensure_ascii=False,indent=2))
