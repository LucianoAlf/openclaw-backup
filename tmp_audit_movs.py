import os,json,urllib.parse,urllib.request
from pathlib import Path
for p in ['/root/.openclaw/workspace/.env','/root/.openclaw/workspace/repos/LAperformanceReport/.env']:
 if Path(p).exists():
  for line in Path(p).read_text().splitlines():
   if '=' in line and not line.strip().startswith('#'):
    k,v=line.split('=',1); os.environ.setdefault(k.strip(),v.strip().strip('"').strip("'"))
url=os.environ.get('LAREPORT_SUPABASE_URL') or os.environ.get('SUPABASE_URL'); key=os.environ.get('LAREPORT_SUPABASE_SERVICE_ROLE') or os.environ.get('SUPABASE_SERVICE_ROLE') or os.environ.get('LAREPORT_SUPABASE_ANON_KEY')
CG='2ec861f6-023f-4d7b-9927-3960ad8c2a92'; headers={'apikey':key,'Authorization':'Bearer '+key,'Accept':'application/json'}
def get(table, params):
 qs=urllib.parse.urlencode(params, doseq=True, safe='*,(),.:')
 req=urllib.request.Request(f'{url}/rest/v1/{table}?{qs}', headers=headers)
 with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read().decode())
print('--- movimentacoes_admin jun/CG evasao/nao_renovacao ---')
mov=get('movimentacoes_admin', [('select','id,data,tipo,aluno_id,alunos(nome),motivos_saida(nome),origem,criado_em'),('unidade_id','eq.'+CG),('data','gte.2026-06-01'),('data','lt.2026-07-01'),('tipo','in.(evasao,nao_renovacao)'),('order','data.asc'),('limit','1000')])
print('count',len(mov))
for m in mov: print(m.get('data'), m.get('tipo'), (m.get('alunos') or {}).get('nome'), (m.get('motivos_saida') or {}).get('nome'), m.get('origem'), m.get('criado_em'))
print('\n--- leads/matrículas junho CG ---')
leads=get('leads',[('select','id,nome,status,data_contato,quantidade,valor_parcela,origem'),('unidade_id','eq.'+CG),('data_contato','gte.2026-06-01'),('data_contato','lt.2026-07-01'),('order','data_contato.asc'),('limit','200')])
print('leads count',len(leads))
for l in leads: print(l.get('data_contato'), l.get('status'), l.get('nome'), l.get('quantidade'), l.get('valor_parcela'), l.get('origem'))
print('\n--- 5 saídas reais alunos ---')
for nome in ['Daniel Oliveira dos Santos','Eduardo Knupp Gomes','Heloisa Nogueira Delgado','Hugo Sena da Cruz','Nicolas Faria dos Santos']:
 data=get('alunos',[('select','id,nome,status,idade_atual,is_segundo_curso,data_saida,valor_parcela,tipos_matricula(codigo,conta_como_pagante),cursos(nome,is_projeto_banda)'),('unidade_id','eq.'+CG),('nome','ilike.%'+nome+'%'),('limit','20')])
 print('\n'+nome); print(json.dumps(data,ensure_ascii=False,indent=2))
