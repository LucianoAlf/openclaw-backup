import os,json,urllib.parse,urllib.request
from pathlib import Path
for p in ['/root/.openclaw/workspace/.env','/root/.openclaw/workspace/repos/LAperformanceReport/.env']:
 if Path(p).exists():
  for line in Path(p).read_text().splitlines():
   if '=' in line and not line.strip().startswith('#'):
    k,v=line.split('=',1); os.environ.setdefault(k.strip(),v.strip().strip('"').strip("'"))
url=os.environ.get('LAREPORT_SUPABASE_URL') or os.environ.get('SUPABASE_URL'); key=os.environ.get('LAREPORT_SUPABASE_ANON_KEY') or os.environ.get('SUPABASE_ANON_KEY')
CG='2ec861f6-023f-4d7b-9927-3960ad8c2a92'; headers={'apikey':key,'Authorization':'Bearer '+key,'Accept':'application/json'}
def get(table, params):
 qs=urllib.parse.urlencode(params,doseq=True,safe='*,(),.:')
 req=urllib.request.Request(f'{url}/rest/v1/{table}?{qs}',headers=headers)
 with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read().decode())
for table, params in [('vw_kpis_gestao_mensal',[('select','*'),('unidade_id','eq.'+CG),('ano','eq.2026'),('mes','eq.6')]),('alunos',[('select','id,nome,status,idade_atual,is_segundo_curso,valor_parcela,tipos_matricula(codigo,conta_como_pagante),cursos(nome,is_projeto_banda)'),('unidade_id','eq.'+CG),('status','in.(ativo,trancado)'),('limit','2000')])]:
 print('\n',table)
 data=get(table,params)
 if table=='alunos':
  print('rows',len(data),'ativo',sum(1 for a in data if a['status']=='ativo'),'tranc',sum(1 for a in data if a['status']=='trancado'))
  print('kids',sum(1 for a in data if a.get('idade_atual') is not None and float(a['idade_atual'])<=11),'school',sum(1 for a in data if a.get('idade_atual') is not None and float(a['idade_atual'])>=12),'sem idade',sum(1 for a in data if a.get('idade_atual') is None))
 else: print(json.dumps(data,ensure_ascii=False,indent=2))
