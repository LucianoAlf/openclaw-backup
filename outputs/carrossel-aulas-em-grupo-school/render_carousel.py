from pathlib import Path
import textwrap

OUT = Path('/root/.openclaw/workspace/outputs/carrossel-aulas-em-grupo-school')
OUT.mkdir(parents=True, exist_ok=True)
REPO = Path('/root/.openclaw/workspace/repos/la-hq-agents')
LOGO_DARK = REPO/'shared/brand-assets/logos/school/logo-la-music-dark-completa.svg'
LOGO_LIGHT = REPO/'shared/brand-assets/logos/school/logo-la-music-light-completa.svg'
SOLO_DARK = REPO/'shared/brand-assets/logos/school/logo-la-music-dark-solo-vazada.svg'
SOLO_LIGHT = REPO/'shared/brand-assets/logos/school/logo-la-music-light-solo-vazada.svg'
FONT_BLACK = REPO/'shared/brand-assets/fonts/school/Prompt-Black.ttf'
FONT_BOLD = REPO/'shared/brand-assets/fonts/school/Prompt-Bold.ttf'
FONT_MED = REPO/'shared/brand-assets/fonts/school/Prompt-Medium.ttf'
FONT_REG = REPO/'shared/brand-assets/fonts/school/Prompt-Regular.ttf'
PHOTOS = [
'/root/.openclaw/media/tool-image-generation/image-1---80484979-f9b3-41e7-81d8-013ffc97d0dc.png',
'/root/.openclaw/media/tool-image-generation/image-2---c93acd8e-d67c-4542-8a0c-9bdca524afe8.png',
'/root/.openclaw/media/tool-image-generation/image-3---af8edd7e-6da8-4d0b-ae04-87558f3f8ca1.png',
'/root/.openclaw/media/tool-image-generation/image-4---db2102ab-9ea2-4e4b-8062-edba1902b817.png',
]

def uri(p): return Path(p).resolve().as_uri()

slides = [
    dict(theme='photo', photo=PHOTOS[0], logo='dark', n='01', kicker='AULA EM TURMA', title=['Não é', 'plano B.'], outline='É REVOLUÇÃO.', sub='Quando tem método, o coletivo não dilui. Multiplica.', accent='revolução', solo='dark', solo_pos='right huge'),
    dict(theme='dark', logo='dark', n='02', kicker='O ERRO', title=['Juntar alunos', 'não é formar turma.'], outline='NÃO É LOTE.', sub='Turma precisa de propósito, nível possível e condução real.', solo='dark', solo_pos='left crop'),
    dict(theme='light', logo='light', n='03', kicker='O PORQUÊ', title=['As pessoas', 'querem conexão.'], outline='NÃO SÓ TÉCNICA.', sub='Depois de tanta tela, música virou encontro: pertencimento, escuta e presença.', solo='light', solo_pos='right low'),
    dict(theme='photo', photo=PHOTOS[1], logo='dark', n='04', kicker='PETERSON ENSINA', title=['Professor não', 'divide tempo.'], outline='CONDUZ A BANDA.', sub='Não são 20 minutos pra cada. É todo mundo tocando junto.', solo='dark', solo_pos='none'),
    dict(theme='pink', logo='dark', n='05', kicker='NIVELAMENTO', title=['Diferença de nível', 'pode ser motor.'], outline='SE FOR PENSADA.', sub='O iniciante acelera. O avançado vira referência. Os dois crescem.', solo='dark', solo_pos='left big'),
    dict(theme='photo', photo=PHOTOS[2], logo='dark', n='06', kicker='NARRATIVA', title=['Pai não compra', 'cadeira dividida.'], outline='COMPRA EVOLUÇÃO.', sub='A turma certa precisa parecer — e ser — uma decisão pedagógica.', solo='dark', solo_pos='none'),
    dict(theme='dark', logo='dark', n='07', kicker='CASE LA MUSIC', title=['Números que', 'calam o mito.'], outline='FUNCIONA.', sub='95% em grupo • 19 meses de permanência • churn 4% • NPS 9', solo='dark', solo_pos='right huge', metrics=True),
    dict(theme='photo', photo=PHOTOS[3], logo='dark', n='08', kicker='PRÓXIMO PASSO', title=['Forme turmas', 'que dão vontade', 'de continuar.'], outline='TOCAR JUNTO.', sub='Método. Narrativa. Pertencimento. Aula em grupo com alma de palco.', cta='@lamusicschool', solo='dark', solo_pos='none'),
]

base_css = f"""
@font-face {{ font-family: Prompt; src: url('{uri(FONT_REG)}'); font-weight: 400; }}
@font-face {{ font-family: Prompt; src: url('{uri(FONT_MED)}'); font-weight: 500; }}
@font-face {{ font-family: Prompt; src: url('{uri(FONT_BOLD)}'); font-weight: 700; }}
@font-face {{ font-family: Prompt; src: url('{uri(FONT_BLACK)}'); font-weight: 900; }}
* {{ box-sizing: border-box; }}
html, body {{ margin:0; width:1080px; height:1440px; overflow:hidden; font-family:Prompt, sans-serif; }}
.slide {{ position:relative; width:1080px; height:1440px; overflow:hidden; background:#0A0A0A; color:#fff; }}
.slide.light {{ background:#E8E8E8; color:#0A0A0A; }}
.slide.pink {{ background:linear-gradient(140deg,#E91451 0%,#B01545 62%,#740A28 100%); color:#fff; }}
.logo {{ position:absolute; top:54px; left:50%; transform:translateX(-50%); height:86px; z-index:30; }}
.photo {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; filter:contrast(1.12) saturate(1.05) brightness(.72); }}
.photoOverlay {{ position:absolute; inset:0; background:radial-gradient(circle at 70% 18%,rgba(233,20,81,.42),transparent 38%), linear-gradient(180deg,rgba(0,0,0,.34),rgba(0,0,0,.76) 56%,rgba(0,0,0,.94)); z-index:2; }}
.dots {{ position:absolute; inset:-120px; opacity:.42; z-index:4; background-image:radial-gradient(circle, rgba(233,20,81,.9) 0 4px, transparent 4.5px); background-size:28px 28px; mask-image:radial-gradient(circle at 82% 25%, black 0 18%, transparent 52%); -webkit-mask-image:radial-gradient(circle at 82% 25%, black 0 18%, transparent 52%); }}
.light .dots {{ background-image:radial-gradient(circle, rgba(233,20,81,.65) 0 4px, transparent 4.5px); opacity:.36; }}
.pink .dots {{ background-image:radial-gradient(circle, rgba(10,10,10,.45) 0 4px, transparent 4.5px); opacity:.5; mask-image:radial-gradient(circle at 18% 24%, black 0 22%, transparent 58%); -webkit-mask-image:radial-gradient(circle at 18% 24%, black 0 22%, transparent 58%); }}
.plus {{ position:absolute; right:70px; top:210px; color:#E91451; font-weight:900; font-size:42px; letter-spacing:20px; line-height:1.55; opacity:.55; z-index:5; white-space:pre; }}
.light .plus {{ color:#0A0A0A; opacity:.14; }}
.watermark {{ position:absolute; z-index:3; opacity:.13; filter:drop-shadow(0 20px 50px rgba(0,0,0,.4)); }}
.watermark.right.huge {{ width:860px; right:-300px; top:250px; transform:rotate(-8deg); }}
.watermark.left.crop {{ width:760px; left:-360px; top:420px; transform:rotate(8deg); }}
.watermark.right.low {{ width:740px; right:-260px; bottom:130px; transform:rotate(-11deg); opacity:.18; }}
.watermark.left.big {{ width:800px; left:-240px; top:310px; transform:rotate(10deg); opacity:.14; }}
.content {{ position:absolute; left:72px; right:72px; bottom:178px; z-index:20; }}
.kicker {{ display:inline-block; font-weight:800; font-size:22px; letter-spacing:4px; padding:12px 20px; background:#E91451; color:#fff; border-radius:999px; box-shadow:12px 12px 0 rgba(0,0,0,.55); margin-bottom:28px; transform:rotate(-1deg); }}
.light .kicker {{ box-shadow:10px 10px 0 rgba(10,10,10,.18); }}
.title {{ font-weight:900; font-size:96px; line-height:.91; letter-spacing:-4px; text-transform:uppercase; margin:0; max-width:940px; }}
.title.small {{ font-size:82px; }}
.title .pinkword {{ color:#E91451; }}
.outline {{ margin-top:8px; font-weight:900; font-size:82px; line-height:.9; letter-spacing:-3px; color:transparent; -webkit-text-stroke:4px #fff; text-shadow:0 8px 26px rgba(0,0,0,.75); text-transform:uppercase; }}
.light .outline {{ -webkit-text-stroke:4px #0A0A0A; text-shadow:none; }}
.pink .outline {{ -webkit-text-stroke:4px #fff; text-shadow:0 8px 26px rgba(0,0,0,.75); }}
.sub {{ margin-top:32px; max-width:830px; font-weight:500; font-size:40px; line-height:1.12; color:#FFFFFF; text-shadow:0 4px 18px rgba(0,0,0,.75); }}
.light .sub {{ color:#373435; text-shadow:none; }}
.n {{ position:absolute; top:205px; left:72px; font-weight:900; font-size:124px; line-height:1; color:transparent; -webkit-text-stroke:2px #E91451; opacity:1; z-index:18; }}
.chev {{ position:absolute; left:70px; bottom:78px; font-size:54px; font-weight:900; color:#E91451; letter-spacing:-12px; z-index:25; }}
.footer {{ position:absolute; left:50%; bottom:62px; transform:translateX(-50%); z-index:30; background:#E91451; color:#fff; border-radius:999px; padding:13px 34px 15px; font-weight:800; font-size:30px; letter-spacing:.5px; box-shadow:0 14px 0 rgba(0,0,0,.42); }}
.stripes {{ position:absolute; left:50%; bottom:36px; transform:translateX(-50%); color:#fff; opacity:.85; z-index:29; font-size:34px; font-weight:900; letter-spacing:-6px; }}
.metricBox {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-top:34px; max-width:820px; }}
.metric {{ background:rgba(233,20,81,.95); border-radius:22px; padding:18px 22px; box-shadow:10px 10px 0 rgba(0,0,0,.5); }}
.metric b {{ font-size:58px; line-height:.9; display:block; }}
.metric span {{ font-size:22px; font-weight:700; text-transform:uppercase; letter-spacing:1px; }}
.ctaPill {{ display:inline-block; margin-top:30px; background:#fff; color:#E91451; border-radius:999px; padding:16px 28px; font-weight:900; font-size:28px; box-shadow:10px 10px 0 rgba(233,20,81,.9); }}
"""

def slide_html(s):
    cls = 'slide ' + (s['theme'] if s['theme'] in ['light','pink'] else '')
    logo = LOGO_LIGHT if s.get('logo')=='light' else LOGO_DARK
    solo = SOLO_LIGHT if s.get('solo')=='light' else SOLO_DARK
    photo = ''
    if s['theme']=='photo':
        photo = f"<img class='photo' src='{uri(s['photo'])}'><div class='photoOverlay'></div>"
    wm = '' if s.get('solo_pos')=='none' else f"<img class='watermark {s.get('solo_pos','right huge')}' src='{uri(solo)}'>"
    plus = "<div class='plus'>+ + +<br>+ + +<br>+ + +</div>"
    title_lines = '<br>'.join(s['title'])
    # pink selected words via simple replacement
    for word in ['grupo','turmas','Números','plano B.','conexão.','motor.','evolução.']:
        title_lines = title_lines.replace(word, f"<span class='pinkword'>{word}</span>")
    title_class = 'title small' if len(' '.join(s['title']))>44 else 'title'
    metrics = ''
    if s.get('metrics'):
        metrics = """<div class='metricBox'>
        <div class='metric'><b>95%</b><span>aulas em grupo</span></div>
        <div class='metric'><b>19m</b><span>permanência média</span></div>
        <div class='metric'><b>4%</b><span>churn médio</span></div>
        <div class='metric'><b>9</b><span>NPS</span></div>
        </div>"""
    cta = f"<div class='ctaPill'>{s.get('cta')}</div>" if s.get('cta') else ''
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>{base_css}</style></head><body>
    <div class='{cls}'>
      {photo}<div class='dots'></div>{wm}{plus}
      <img class='logo' src='{uri(logo)}'>
      <div class='n'>{s['n']}</div>
      <div class='content'>
        <div class='kicker'>{s['kicker']}</div>
        <h1 class='{title_class}'>{title_lines}</h1>
        <div class='outline'>{s['outline']}</div>
        <div class='sub'>{s['sub']}</div>
        {metrics}{cta}
      </div>
      <div class='chev'>»»»</div>
      <div class='footer'>@lamusicschool</div><div class='stripes'>///////</div>
    </div></body></html>"""

for i,s in enumerate(slides,1):
    (OUT/f'slide-{i:02d}.html').write_text(slide_html(s), encoding='utf-8')
print(OUT)
