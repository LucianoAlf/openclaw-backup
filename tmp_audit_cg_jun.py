import os, json, urllib.parse, urllib.request
from pathlib import Path
for p in ['/root/.openclaw/workspace/.env','/root/.openclaw/workspace/repos/LAperformanceReport/.env']:
    if Path(p).exists():
        for line in Path(p).read_text().splitlines():
            line=line.strip()
            if not line or line.startswith('#') or '=' not in line: continue
            k,v=line.split('=',1); v=v.strip().strip('"').strip("'")
            os.environ.setdefault(k.strip(), v)
url=os.environ.get('LAREPORT_SUPABASE_URL') or os.environ.get('SUPABASE_URL')
key=os.environ.get('LAREPORT_SUPABASE_SERVICE_ROLE') or os.environ.get('SUPABASE_SERVICE_ROLE') or os.environ.get('LAREPORT_SUPABASE_ANON_KEY')
CG='2ec861f6-023f-4d7b-9927-3960ad8c2a92'
headers={'apikey':key,'Authorization':'Bearer '+key,'Accept':'application/json'}
def get(table, params):
    qs=urllib.parse.urlencode(params, doseq=True, safe='*,(),.:')
    req=urllib.request.Request(f'{url}/rest/v1/{table}?{qs}', headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())
def dump(title, obj):
    print('\n--- '+title+' ---')
    print(json.dumps(obj, ensure_ascii=False, indent=2, default=str))
view=get('vw_kpis_gestao_mensal', {'select':'*','unidade_id':'eq.'+CG,'ano':'eq.2026','mes':'eq.6'})
dump('vw_kpis_gestao_mensal CG Jun/2026', view)
dm=get('dados_mensais', {'select':'*','unidade_id':'eq.'+CG,'ano':'eq.2026','mes':'eq.6'})
dump('dados_mensais CG Jun/2026', dm)
# alunos active/trancado with relationships
alunos=get('alunos', {'select':'id,nome,status,idade_atual,is_segundo_curso,valor_parcela,data_matricula,data_saida,tipos_matricula(codigo,conta_como_pagante,entra_ticket_medio),cursos(nome,is_projeto_banda)','unidade_id':'eq.'+CG,'status':'in.(ativo,trancado)','order':'nome.asc','limit':'2000'})
def summarize(rows,label):
    kids=[a for a in rows if a.get('idade_atual') is not None and float(a.get('idade_atual'))<=11]
    school=[a for a in rows if a.get('idade_atual') is not None and float(a.get('idade_atual'))>=12]
    sem=[a for a in rows if a.get('idade_atual') is None]
    segundo=[a for a in rows if a.get('is_segundo_curso') is True]
    banda=[a for a in rows if (a.get('tipos_matricula') or {}).get('codigo')=='BANDA' or (a.get('cursos') or {}).get('is_projeto_banda') is True]
    bolsI=[a for a in rows if (a.get('tipos_matricula') or {}).get('codigo')=='BOLSISTA_INT']
    bolsP=[a for a in rows if (a.get('tipos_matricula') or {}).get('codigo')=='BOLSISTA_PARC']
    pag=[a for a in rows if (a.get('tipos_matricula') or {}).get('conta_como_pagante') is True]
    pagSem2=[a for a in rows if (a.get('tipos_matricula') or {}).get('conta_como_pagante') is True and a.get('is_segundo_curso') is not True]
    print('\n--- '+label+' ---')
    print(json.dumps({'total':len(rows),'kids':len(kids),'school':len(school),'kids_plus_school':len(kids)+len(school),'sem_idade':len(sem),'segundo_curso':len(segundo),'banda':len(banda),'bolsistas_int':len(bolsI),'bolsistas_parc':len(bolsP),'pagantes':len(pag),'pagantes_sem_segundo':len(pagSem2)}, ensure_ascii=False))
    if sem:
        print('Sem idade:')
        for a in sem: print({k:a.get(k) for k in ['id','nome','status','idade_atual','is_segundo_curso','valor_parcela']}, 'tipo=', (a.get('tipos_matricula') or {}).get('codigo'), 'curso=', (a.get('cursos') or {}).get('nome'))
summarize([a for a in alunos if a.get('status')=='ativo'],'alunos status=ativo')
summarize(alunos,'alunos status in ativo,trancado')
mov=get('movimentacoes_admin', {'select':'id,data,tipo,aluno_id,alunos(nome),motivos_saida(nome),origem,criado_em','unidade_id':'eq.'+CG,'data':'gte.2026-06-01','data':'gte.2026-06-01','tipo':'in.(evasao,nao_renovacao)','order':'data.asc','limit':'1000'})
# Can't send duplicate data params. filter client-side date < 2026-07-01 if necessary
mov=[m for m in mov if m.get('data','')<'2026-07-01']
print('\n--- movimentacoes_admin jun/CG evasao/nao_renovacao ---')
print('count', len(mov))
for m in mov: print(m.get('data'), m.get('tipo'), (m.get('alunos') or {}).get('nome'), (m.get('motivos_saida') or {}).get('nome'), m.get('origem'), m.get('criado_em'))
print('\n--- alunos nomes 5 saídas reais ---')
for nome in ['Daniel Oliveira dos Santos','Eduardo Knupp Gomes','Heloisa Nogueira Delgado','Hugo Sena da Cruz','Nicolas Faria dos Santos']:
    data=get('alunos', {'select':'id,nome,status,idade_atual,is_segundo_curso,data_saida,tipos_matricula(codigo,conta_como_pagante),cursos(nome)','unidade_id':'eq.'+CG,'nome':'ilike.%'+nome+'%','limit':'20'})
    dump(nome, data)
