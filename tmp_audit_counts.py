import os,json,urllib.parse,urllib.request,collections
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
alunos=get('alunos', {'select':'id,nome,status,idade_atual,is_segundo_curso,valor_parcela,tipo_matricula_id,curso_id,tipos_matricula(codigo,conta_como_pagante,entra_ticket_medio),cursos(nome,is_projeto_banda)','unidade_id':'eq.'+CG,'status':'in.(ativo,trancado)','limit':'2000'})
for status in ['ativo','trancado']:
 rows=[a for a in alunos if a['status']==status]
 print('\nSTATUS',status,'TOTAL',len(rows))
 by=collections.Counter((a.get('tipos_matricula') or {}).get('codigo') or 'NULL' for a in rows)
 print('tipos', by)
 print('curso_banda true', sum(1 for a in rows if (a.get('cursos') or {}).get('is_projeto_banda') is True))
 print('tipo BANDA', sum(1 for a in rows if (a.get('tipos_matricula') or {}).get('codigo')=='BANDA'))
 print('conta_pagante true', sum(1 for a in rows if (a.get('tipos_matricula') or {}).get('conta_como_pagante') is True))
 print('valor > 0', sum(1 for a in rows if (a.get('valor_parcela') or 0)>0))
 # Try formulas
 formulas={
  'not_BANDA_not_BOLSISTA_INT': lambda a: (a.get('tipos_matricula') or {}).get('codigo') not in ['BANDA','BOLSISTA_INT'],
  'not_curso_banda_not_BOLSISTA_INT': lambda a: not ((a.get('cursos') or {}).get('is_projeto_banda') is True) and (a.get('tipos_matricula') or {}).get('codigo')!='BOLSISTA_INT',
  'not_curso_banda_not_bolsint_not_segundo': lambda a: not ((a.get('cursos') or {}).get('is_projeto_banda') is True) and (a.get('tipos_matricula') or {}).get('codigo')!='BOLSISTA_INT' and a.get('is_segundo_curso') is not True,
  'conta_pagante_not_curso_banda': lambda a: (a.get('tipos_matricula') or {}).get('conta_como_pagante') is True and not ((a.get('cursos') or {}).get('is_projeto_banda') is True),
  'conta_pagante_not_tipo_BANDA': lambda a: (a.get('tipos_matricula') or {}).get('conta_como_pagante') is True and (a.get('tipos_matricula') or {}).get('codigo')!='BANDA',
  'valor_gt_0_not_curso_banda': lambda a: (a.get('valor_parcela') or 0)>0 and not ((a.get('cursos') or {}).get('is_projeto_banda') is True),
  'valor_gt_0_not_banda_not_segundo': lambda a: (a.get('valor_parcela') or 0)>0 and not ((a.get('cursos') or {}).get('is_projeto_banda') is True) and a.get('is_segundo_curso') is not True,
 }
 for name,fn in formulas.items(): print(name, sum(1 for a in rows if fn(a)))
print('\nRows active excluded by formula total=479 (BANDA or BOLSISTA_INT)')
for a in [a for a in alunos if a['status']=='ativo' and ((a.get('tipos_matricula') or {}).get('codigo') in ['BANDA','BOLSISTA_INT'])][:80]: print(a['nome'], (a.get('tipos_matricula') or {}).get('codigo'), (a.get('cursos') or {}).get('nome'), a.get('valor_parcela'))
