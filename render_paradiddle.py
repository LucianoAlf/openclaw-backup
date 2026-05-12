from pathlib import Path
import shutil

repo = Path('/root/.openclaw/workspace/repos/la-hq-agents')
out = Path('/root/.openclaw/workspace/outputs/la-school-paradiddle-drums-e2e')
html_dir = out/'html'; png_dir = out/'png'; asset_dir = out/'assets'
for d in [html_dir, png_dir, asset_dir]:
    d.mkdir(parents=True, exist_ok=True)

src_imgs = [
    Path('/root/.openclaw/media/tool-image-generation/lahq-paradiddle-drums-assets---042e3aac-c74e-406b-8fcb-57e9045a8da2.png'),
    Path('/root/.openclaw/media/tool-image-generation/lahq-paradiddle-drums-assets---5057c6ac-9fec-467b-90d7-b82217e52871.png'),
    Path('/root/.openclaw/media/tool-image-generation/lahq-paradiddle-drums-assets---8d5b4434-6aae-4171-81ec-953cbae6b6d8.png'),
    Path('/root/.openclaw/media/tool-image-generation/lahq-paradiddle-drums-assets---ceb21348-a6ca-4764-93fb-61db709e8e03.png'),
]
imgs = []
for p in src_imgs:
    dst = asset_dir / p.name
    shutil.copy2(p, dst)
    imgs.append(dst)

logo_dark = repo/'shared/brand-assets/logos/school/logo-la-music-dark-completa.svg'
logo_light = repo/'shared/brand-assets/logos/school/logo-la-music-light-completa.svg'
font_black = repo/'shared/brand-assets/fonts/school/Prompt-Black.ttf'
font_bold = repo/'shared/brand-assets/fonts/school/Prompt-Bold.ttf'
font_regular = repo/'shared/brand-assets/fonts/school/Prompt-Regular.ttf'
font_medium = repo/'shared/brand-assets/fonts/school/Prompt-Medium.ttf'
font_semibold = repo/'shared/brand-assets/fonts/school/Prompt-SemiBold.ttf'

def uri(p):
    return Path(p).resolve().as_uri()

slides = [
    dict(theme='dark', type='cover', img=0, badge='TÉCNICA DE BATERIA', title_html="<span class='pinkword'>PARA</span>DIDDLE", outline='sem mistério', body='O rudimento que destrava controle, velocidade e groove.', kicker='Passe pro lado →'),
    dict(theme='light', type='content', img=None, badge='O PADRÃO', title_html='D E D D', outline='E D E E', body='Direita, esquerda, direita, direita. Depois inverte. Simples no papel. Poderoso na bateria.', kicker='RLRR • LRLL'),
    dict(theme='dark', type='photo', img=1, badge='REGRA #1', title_html='NÃO É FORÇA.', outline='É controle.', body='Paradiddle bom nasce do rebote. Deixa a baqueta trabalhar — sua mão só guia.', kicker='Relaxou? Tocou melhor.'),
    dict(theme='pink', type='content', img=None, badge='ACENTO', title_html='MARQUE O PRIMEIRO', outline='toque', body='Acentue o “D” e o “E” que abrem cada grupo. É isso que transforma exercício em música.', kicker='D e d d / E d e e'),
    dict(theme='dark', type='photo', img=2, badge='TREINO CERTO', title_html='COMECE A 60 BPM', outline='sem pressa', body='Pad, metrônomo e som limpo. Se embolou, baixa o BPM. Técnica não aceita mentira.', kicker='5 minutos por dia > 1 hora torta'),
    dict(theme='light', type='photo', img=3, badge='APLICAÇÃO', title_html='LEVE PRO GROOVE', outline='de verdade', body='Mova os acentos entre caixa, tons e chimbal. O paradiddle vira fraseado, não só exercício.', kicker='Rudimento + musicalidade'),
    dict(theme='dark', type='content', img=None, badge='ERRO COMUM', title_html='PULSO TRAVADO', outline='mata o som', body='Se o punho endurece, o groove fica quadrado. Respira, solta o braço e escuta o rebote.', kicker='Som bonito vem de movimento livre.'),
    dict(theme='pink', type='cta', img=0, badge='LA MUSIC SCHOOL', title_html='QUER TOCAR', outline='com precisão?', body='Aula de bateria pra quem quer técnica, som e atitude. Pra Quem Sabe o Que Quer.', kicker='Chama a LA Music School'),
]

css = f'''
@font-face {{ font-family: Prompt; src: url('{uri(font_regular)}') format('truetype'); font-weight: 400; }}
@font-face {{ font-family: Prompt; src: url('{uri(font_medium)}') format('truetype'); font-weight: 500; }}
@font-face {{ font-family: Prompt; src: url('{uri(font_semibold)}') format('truetype'); font-weight: 600; }}
@font-face {{ font-family: Prompt; src: url('{uri(font_bold)}') format('truetype'); font-weight: 700; }}
@font-face {{ font-family: Prompt; src: url('{uri(font_black)}') format('truetype'); font-weight: 900; }}
* {{ box-sizing: border-box; }}
html, body {{ margin:0; width:1080px; height:1440px; overflow:hidden; font-family: Prompt, sans-serif; }}
.slide {{ position:relative; width:1080px; height:1440px; overflow:hidden; color:#fff; background:#0A0A0A; }}
.slide.light {{ background:#E8E8E8; color:#0A0A0A; }}
.slide.pink {{ background:linear-gradient(145deg,#E91451 0%,#B01545 100%); color:#fff; }}
.bg {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; filter: contrast(1.15) saturate(1.1); }}
.dark .bg {{ opacity:.58; }} .pink .bg {{ opacity:.16; mix-blend-mode:multiply; }} .light .bg {{ opacity:.18; filter:grayscale(1) contrast(1.15); }}
.overlay {{ position:absolute; inset:0; background:radial-gradient(circle at 70% 25%, rgba(233,20,81,.38), transparent 34%), linear-gradient(180deg, rgba(10,10,10,.15), rgba(10,10,10,.75)); }}
.light .overlay {{ background:radial-gradient(circle at 80% 20%, rgba(233,20,81,.20), transparent 32%); }}
.pink .overlay {{ background:radial-gradient(circle at 72% 18%, rgba(255,255,255,.18), transparent 30%); }}
.logo {{ position:absolute; top:56px; left:64px; width:236px; max-height:86px; z-index:5; }}
.logo.center {{ left:50%; transform:translateX(-50%); width:300px; }}
.halftone {{ position:absolute; right:-80px; top:130px; width:520px; height:520px; opacity:.55; background-image: radial-gradient(circle, #E91451 0 5px, transparent 6px); background-size:28px 28px; mask-image:radial-gradient(circle, #000 20%, transparent 72%); }}
.light .halftone {{ opacity:.35; }} .pink .halftone {{ opacity:.23; background-image: radial-gradient(circle, #0A0A0A 0 5px, transparent 6px); }}
.watermark {{ position:absolute; right:-44px; bottom:186px; font-size:330px; font-weight:900; line-height:.8; color:transparent; -webkit-text-stroke:4px rgba(255,255,255,.16); transform:rotate(-7deg); }}
.light .watermark {{ -webkit-text-stroke-color:rgba(10,10,10,.13); }}
.content {{ position:absolute; left:64px; right:64px; top:210px; z-index:4; }}
.content.low {{ top:610px; }}
.badge {{ display:inline-block; background:#E91451; color:#fff; font-weight:800; font-size:24px; letter-spacing:2.5px; padding:13px 22px; border-radius:14px; box-shadow:10px 10px 0 rgba(0,0,0,.45); margin-bottom:26px; }}
.pink .badge {{ background:#0A0A0A; }}
.title {{ font-size:108px; font-weight:900; line-height:.88; letter-spacing:-5px; text-transform:uppercase; margin:0; max-width:940px; }}
.title .pinkword {{ color:#E91451; }} .pink .title .pinkword {{ color:#fff; }}
.outline {{ display:block; color:transparent; -webkit-text-stroke:3px currentColor; font-size:92px; font-weight:900; line-height:.9; letter-spacing:-4px; text-transform:uppercase; margin-top:8px; opacity:.98; }}
.dark .outline {{ -webkit-text-stroke-color:#fff; }} .light .outline {{ -webkit-text-stroke-color:#0A0A0A; }} .pink .outline {{ -webkit-text-stroke-color:#fff; }}
.bodycopy {{ margin-top:34px; max-width:760px; font-size:36px; line-height:1.14; font-weight:500; }}
.light .bodycopy {{ color:#222; }}
.kicker {{ margin-top:30px; display:inline-block; border:2px solid currentColor; border-radius:999px; padding:14px 24px; font-size:24px; font-weight:700; }}
.card {{ background:#E91451; color:#fff; border-radius:20px; padding:36px 42px; display:inline-block; box-shadow:18px 18px 0 rgba(0,0,0,.52); max-width:890px; }}
.light .card {{ color:#fff; }} .pink .card {{ background:#0A0A0A; }}
.pattern-bars {{ position:absolute; bottom:64px; left:50%; transform:translateX(-50%); width:420px; height:58px; background:repeating-linear-gradient(105deg, transparent 0 16px, rgba(255,255,255,.9) 17px 25px); opacity:.95; }}
.footer {{ position:absolute; bottom:92px; left:50%; transform:translateX(-50%); background:#E91451; color:#fff; border-radius:999px; padding:18px 46px; font-size:30px; font-weight:800; z-index:8; box-shadow:0 14px 0 rgba(0,0,0,.38); letter-spacing:.5px; }}
.pink .footer {{ background:#0A0A0A; }}
.chev {{ position:absolute; bottom:112px; left:54px; color:#E91451; font-size:56px; font-weight:900; letter-spacing:-8px; transform:skewX(-12deg); }}
.pink .chev {{ color:#fff; }}
.num {{ position:absolute; right:64px; bottom:84px; font-size:30px; font-weight:900; opacity:.72; z-index:9; }}
.stroke-bg {{ position:absolute; left:48px; top:380px; font-size:260px; line-height:.8; font-weight:900; color:transparent; -webkit-text-stroke:3px rgba(233,20,81,.26); transform:rotate(-5deg); }}
'''

for i, s in enumerate(slides, 1):
    cls = 'slide ' + s['theme']
    logo = logo_light if s['theme'] in ['light','pink'] else logo_dark
    bg = f"<img class='bg' src='{uri(imgs[s['img']])}'>" if s.get('img') is not None else ''
    content_class = 'content low' if s['type'] in ['photo'] else 'content'
    card_open = "<div class='card'>" if s['type'] in ['cover','cta'] else ""
    card_close = "</div>" if card_open else ""
    center = 'center' if i in [1,8] else ''
    html = f"""<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>
<section class='{cls}'>
{bg}<div class='overlay'></div><div class='halftone'></div><div class='watermark'>LA</div><div class='stroke-bg'>{i:02d}</div>
<img class='logo {center}' src='{uri(logo)}'>
<div class='{content_class}'>
  {card_open}<div class='badge'>{s['badge']}</div>
  <h1 class='title'>{s['title_html']}<span class='outline'>{s['outline']}</span></h1>
  <div class='bodycopy'>{s['body']}</div>
  <div class='kicker'>{s['kicker']}</div>{card_close}
</div>
<div class='chev'>&gt;&gt;&gt;&gt;</div><div class='pattern-bars'></div><div class='footer'>@lamusicschool</div><div class='num'>{i:02d}/08</div>
</section></body></html>"""
    (html_dir/f'la-school-paradiddle-{i:02d}.html').write_text(html, encoding='utf-8')

pipeline = '''# LAHQ PIPELINE — Carrossel LA Music School — Paradiddle na bateria

## Briefing (Nina)
Marca: LA Music School. Tema: técnica de paradiddle na bateria. Formato: carrossel Instagram 1080x1440, 8 cards. Tom: técnico, acessível, rock, direto.

## Copy (Theo)
1. PARADIDDLE sem mistério — rudimento que destrava controle, velocidade e groove.
2. D E D D / E D E E — entender o padrão.
3. Não é força. É controle — rebote e relaxamento.
4. Marque o primeiro toque — acento musical.
5. Comece a 60 BPM — pad + metrônomo.
6. Leve pro groove — caixa, tons e chimbal.
7. Pulso travado mata o som — erro comum.
8. Quer tocar com precisão? CTA LA Music School.

## Imagem (Luna)
4 assets fotorrealistas gerados com GPT Image 2: bateria, baquetas, practice pad, drummer motion. Sem texto/logos.

## Montagem (Diego)
HTML/CSS 1080x1440 usando Prompt local, SVG oficial, halftone, outline type, badge pink, footer pill @lamusicschool, chevrons e paleta #E91451/#B01545/#0A0A0A/#E8E8E8.

## QA (Tina)
Checklist: legibilidade mobile, logo oficial, sem logo fake, uma cor de destaque pink, textos sem overflow, export PNG 1080x1440.
'''
(out/'LAHQ_PIPELINE.md').write_text(pipeline, encoding='utf-8')
print(out)
