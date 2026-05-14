from pathlib import Path
import base64, subprocess, json, urllib.request, urllib.parse, datetime
from PIL import Image

WORK=Path('/root/.openclaw/workspace')
OUT=WORK/'outputs/la-school-e2e-musica-identidade-palco'
OUT.mkdir(parents=True, exist_ok=True)
REPO=WORK/'repos/la-hq-agents'
IMG=Path('/root/.openclaw/media/inbound/file_891---f8212e1f-fcd5-4ec6-81e9-69787cb9e963.jpg')
if not IMG.exists():
    raise SystemExit('Imagem inbound não encontrada')

def readenv(path):
    vals={}
    for line in Path(path).read_text().splitlines():
        if not line or line.startswith('#') or '=' not in line: continue
        k,v=line.split('=',1); vals[k]=v
    return vals
ENV=readenv(WORK/'.env')
BASE=ENV['SUPABASE_LAHQ_URL'].rstrip('/')
KEY=ENV['SUPABASE_LAHQ_SERVICE_ROLE']
HEAD={'apikey':KEY,'Authorization':'Bearer '+KEY,'Content-Type':'application/json'}

logo=(REPO/'shared/brand-assets/logos/school/logo-la-music-dark-completa.svg').read_text()
solo=(REPO/'shared/brand-assets/logos/school/logo-la-music-dark-solo-vazada.svg').read_text()
fonts={
 'reg': REPO/'shared/brand-assets/fonts/school/Prompt-Regular.ttf',
 'bold': REPO/'shared/brand-assets/fonts/school/Prompt-Bold.ttf',
 'black': REPO/'shared/brand-assets/fonts/school/Prompt-Black.ttf'
}
def b64(p): return base64.b64encode(Path(p).read_bytes()).decode()
fontcss=''.join([
 f"@font-face{{font-family:Prompt;src:url(data:font/ttf;base64,{b64(fonts['reg'])}) format('truetype');font-weight:400}}",
 f"@font-face{{font-family:Prompt;src:url(data:font/ttf;base64,{b64(fonts['bold'])}) format('truetype');font-weight:700}}",
 f"@font-face{{font-family:Prompt;src:url(data:font/ttf;base64,{b64(fonts['black'])}) format('truetype');font-weight:900}}",
])
common=f'''
{fontcss}
*{{box-sizing:border-box}} body{{margin:0;background:#111}} .art{{width:1080px;height:1440px;position:relative;overflow:hidden;background:#050505;font-family:Prompt,Arial,sans-serif;color:white}}
.photo{{position:absolute;inset:0;background:url(data:image/jpeg;base64,{b64(IMG)}) 62% 42%/cover no-repeat;filter:contrast(1.18) saturate(1.1) brightness(1.06)}}
.photo:after{{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.90),rgba(0,0,0,.60) 38%,rgba(0,0,0,.08) 70%),linear-gradient(0deg,rgba(0,0,0,.91),rgba(0,0,0,.30) 35%,rgba(0,0,0,.06) 70%,rgba(0,0,0,.62));}}
.logo{{position:absolute;top:58px;left:58px;width:225px;filter:drop-shadow(0 8px 22px rgba(0,0,0,.9))}} .logo svg{{width:225px;height:auto}}
.la{{position:absolute;left:-180px;bottom:130px;width:640px;opacity:.075;transform:rotate(-8deg)}} .la svg{{width:100%}}
.dots{{position:absolute;left:-80px;bottom:360px;width:390px;height:310px;opacity:.24;background-image:radial-gradient(circle,#E91451 0 4px,transparent 5px);background-size:30px 30px;mask-image:linear-gradient(110deg,black,transparent 82%);transform:rotate(-9deg)}}
.glow{{position:absolute;right:-160px;top:20px;width:590px;height:720px;background:radial-gradient(circle,rgba(233,20,81,.36),rgba(233,20,81,.08) 44%,transparent 72%);mix-blend-mode:screen}}
.copy{{position:absolute;left:62px;bottom:122px;width:735px;z-index:3}}
.kicker{{font-weight:900;color:#F06292;text-transform:uppercase;letter-spacing:.18em;font-size:24px;margin-bottom:24px;text-shadow:0 7px 20px rgba(0,0,0,.9)}}
.title{{font-weight:900;text-transform:uppercase;line-height:.88;letter-spacing:-.066em;font-size:104px;text-shadow:0 10px 30px rgba(0,0,0,.95)}}
.title span{{display:block}} .outline{{color:transparent;-webkit-text-stroke:3px #fff;text-stroke:3px #fff}} .pink{{color:#E91451}}
.sub{{margin-top:28px;width:660px;font-weight:700;font-size:30px;line-height:1.13;text-shadow:0 7px 20px rgba(0,0,0,.95)}}
.handle{{display:inline-block;margin-top:34px;background:#E91451;color:white;border-radius:999px;padding:13px 25px 14px;font-size:23px;font-weight:900;letter-spacing:.07em;text-transform:uppercase;box-shadow:12px 12px 0 rgba(0,0,0,.45)}}
.num{{position:absolute;right:54px;bottom:48px;color:rgba(255,255,255,.75);font-weight:900;font-size:24px;letter-spacing:.12em}}
'''
slides=[
 ('MÚSICA NÃO É SÓ AULA', ['AQUI', 'MÚSICA', 'TRANSFORMA'], 'A LA revela o que a técnica sozinha não mostra.', '01'),
 ('PRA QUEM QUER MAIS', ['A GENTE', 'NÃO FABRICA', 'MÚSICO.'], 'A gente cria espaço pra identidade aparecer.', '02'),
 ('IDENTIDADE NO SOM', ['A GENTE', 'REVELA', 'VERDADE.'], 'Cada voz, cada riff, cada escolha: tudo conta quem você é.', '03'),
 ('PAIXÃO COM MÉTODO', ['PAIXÃO', 'VIRA PRÁTICA.', ''], 'E prática, quando tem direção, vira palco.', '04'),
 ('EXCELÊNCIA HUMANA', ['EMPATIA', 'SEM MOLEZA.', ''], 'Excelência sem frieza. Técnica com escuta real.', '05'),
 ('AGORA É COM VOCÊ', ['SUA VEZ', 'DE OCUPAR', 'ESPAÇO.'], 'Aula experimental na LA Music School. Link na bio.', '06'),
]
files=[]
for i,(kicker,lines,sub,num) in enumerate(slides,1):
    spans=''.join(f'<span class="{"pink" if ("VERDADE" in l or "ESPAÇO" in l or "TRANSFORMA" in l) else "outline" if j==0 else ""}">{l}</span>' for j,l in enumerate(lines) if l)
    handle='<div class="handle">@LAMUSICSCHOOL</div>' if i in (1,6) else ''
    photo = '<div class="photo"></div>' if i in (1,3,6) else '<div class="photo" style="filter:contrast(1.05) saturate(.8) brightness(.55);background-position:64% 42%"></div><div style="position:absolute;inset:0;background:linear-gradient(135deg,#050505 0%,#170711 52%,#E91451 220%);"></div>'
    html=f'''<!doctype html><html><head><meta charset="utf-8"><style>{common}</style></head><body><div class="art">{photo}<div class="glow"></div><div class="la">{solo}</div><div class="dots"></div><div class="logo">{logo}</div><div class="copy"><div class="kicker">{kicker}</div><div class="title">{spans}</div><div class="sub">{sub}</div>{handle}</div><div class="num">{num}/06</div></div></body></html>'''
    h=OUT/f'slide-{i:02}.html'; h.write_text(html)
    png=OUT/f'la-school-e2e-{i:02}.png'
    subprocess.run(['chromium','--headless','--no-sandbox','--disable-gpu','--window-size=1080,1440',f'--screenshot={png}',f'file://{h}'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    files.append(png)
imgs=[Image.open(f).resize((270,360)) for f in files]
grid=Image.new('RGB',(270*3,360*2),(20,20,20))
for idx,im in enumerate(imgs): grid.paste(im,((idx%3)*270,(idx//3)*360))
grid_path=OUT/'preview-grid.jpg'; grid.save(grid_path,quality=92)

slug='la-school-e2e-musica-identidade-palco-'+datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
public_urls=[]
for png in files:
    object_path=f'{slug}/{png.name}'
    url=f'{BASE}/storage/v1/object/outputs/{urllib.parse.quote(object_path)}'
    req=urllib.request.Request(url,data=png.read_bytes(),headers={'apikey':KEY,'Authorization':'Bearer '+KEY,'Content-Type':'image/png','x-upsert':'true'},method='POST')
    with urllib.request.urlopen(req,timeout=60) as r: r.read()
    public_urls.append(f'{BASE}/storage/v1/object/public/outputs/{object_path}')
object_path=f'{slug}/preview-grid.jpg'
req=urllib.request.Request(f'{BASE}/storage/v1/object/outputs/{urllib.parse.quote(object_path)}',data=grid_path.read_bytes(),headers={'apikey':KEY,'Authorization':'Bearer '+KEY,'Content-Type':'image/jpeg','x-upsert':'true'},method='POST')
with urllib.request.urlopen(req,timeout=60) as r: r.read()
preview_url=f'{BASE}/storage/v1/object/public/outputs/{object_path}'

OFFICE='a1b2c3d4-0001-4000-8000-000000000001'; SQUAD='b2c3d4e5-0001-4000-8000-000000000001'
AG={'mike':'c3d4e5f6-0001-4000-8000-000000000001','tina':'c3d4e5f6-0007-4000-8000-000000000007'}
caption='''Música não é só aula. É identidade ganhando forma.\n\nNa LA Music School, técnica não é um fim — é o caminho pra você cantar, tocar e se reconhecer no próprio som.\n\nPaixão vira prática. Prática vira palco.\n\nAula experimental grátis — link na bio.'''
hashtags=['LAMusicSchool','MúsicaNãoÉSóAula','AulaDeMúsica','EscolaDeMúsica','Canto','Guitarra','Violão','Bateria','RioDeJaneiro','CampoGrande']

def post(table, payload, prefer='return=representation'):
    req=urllib.request.Request(f'{BASE}/rest/v1/{table}',data=json.dumps(payload).encode(),headers={**HEAD,'Prefer':prefer},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=60) as r:
            txt=r.read().decode()
            return json.loads(txt)[0] if txt else None
    except Exception as e:
        print('POST ERROR', table, e)
        if hasattr(e, 'read'):
            print(e.read().decode())
        raise
now=datetime.datetime.utcnow().isoformat()+'Z'
main=post('tasks',{'agent_id':AG['mike'],'squad_id':SQUAD,'type':'carousel','brand':'la-music-school','input':{'briefing':'E2E test Alfredo: música não é só aula — identidade, palco e transformação','tema':'música não é só aula','total_slides':6},'output':{'created_by':'alfredo_direct_e2e'},'status':'completed','approval_status':'approved','priority':'high','model_used':'openclaw-gpt-5.5','completed_at':now})
output=post('outputs',{'task_id':main['id'],'office_id':OFFICE,'type':'carousel','format':'instagram_carousel','brand':'la-music-school','title':'E2E School — Música não é só aula','theme':'música não é só aula — identidade/palco/transformação','file_urls':public_urls,'preview_url':preview_url,'total_slides':6,'published':False,'platform':'instagram','approval_status':'approved','approval_feedback':'QA Alfredo: aprovado para dry-run técnico; publicação live depende de aprovação explícita do Alf.','rendered_by':'alfredo_direct','status':'ready'})
tina=post('tasks',{'agent_id':AG['tina'],'squad_id':SQUAD,'parent_task_id':main['id'],'type':'publishing','brand':'la-music-school','input':{'output_id':output['id'],'legenda':caption,'hashtags':hashtags},'status':'pending','approval_status':'approved','priority':'high'})
post('calendar_entries',{'office_id':OFFICE,'brand':'la-music-school','title':'E2E School — Música não é só aula','content_type':'carousel','scheduled_date':now,'status':'ready_for_publication','output_id':output['id'],'notes':'Criado pelo Alfredo para teste E2E; live requer aprovação explícita.','created_by':'alfredo'}, prefer='return=minimal')
post('semantic_memory',{'office_id':OFFICE,'agent_id':AG['mike'],'content':'E2E test criado pelo Alfredo: carrossel School Música não é só aula registrado em outputs e Tina task pendente para dry-run. Live exige aprovação explícita do Alf.','category':'decision','metadata':{'task_id':main['id'],'output_id':output['id'],'tina_task_id':tina['id']},'source':'alfredo','relevance_score':0.8}, prefer='return=minimal')
summary={'local_dir':str(OUT),'preview_grid':str(grid_path),'output_id':output['id'],'task_id':main['id'],'tina_task_id':tina['id'],'public_urls':public_urls,'preview_url':preview_url}
(OUT/'e2e-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2))
