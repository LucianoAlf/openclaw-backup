from pathlib import Path
from PIL import Image, ImageDraw
import shutil, subprocess, tarfile

repo = Path('/root/.openclaw/workspace/repos/la-hq-agents')
out = Path('/root/.openclaw/workspace/outputs/la-school-paradiddle-skill-test')
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

logos = repo/'shared/brand-assets/logos/school'
logo_dark_full = logos/'logo-la-music-dark-completa.svg'
logo_light_full = logos/'logo-la-music-light-completa.svg'
wm_dark = logos/'logo-la-music-dark-solo-vazada.svg'
wm_light = logos/'logo-la-music-light-solo-vazada.svg'
font_dir = repo/'shared/brand-assets/fonts/school'
font_black = font_dir/'Prompt-Black.ttf'
font_bold = font_dir/'Prompt-Bold.ttf'
font_regular = font_dir/'Prompt-Regular.ttf'
font_medium = font_dir/'Prompt-Medium.ttf'
font_semibold = font_dir/'Prompt-SemiBold.ttf'

def uri(p): return Path(p).resolve().as_uri()

slides = [
    dict(theme='dark', type='cover', img=0, badge='TÉCNICA DE BATERIA', title="PARA|DIDDLE", outline='sem mistério', body='O rudimento que destrava controle, velocidade e groove.', kicker='Passe pro lado →'),
    dict(theme='light', type='content', img=None, badge='O PADRÃO', title='D E D D', outline='E D E E', body='Direita, esquerda, direita, direita. Depois inverte. Simples no papel. Poderoso na bateria.', kicker='RLRR • LRLL'),
    dict(theme='dark', type='photo', img=1, badge='REGRA #1', title='NÃO É FORÇA.', outline='É controle.', body='Paradiddle bom nasce do rebote. Deixa a baqueta trabalhar — sua mão só guia.', kicker='Relaxou? Tocou melhor.'),
    dict(theme='pink', type='content', img=None, badge='ACENTO', title='MARQUE O PRIMEIRO', outline='toque', body='Acentue a primeira nota de cada grupo. É isso que transforma exercício em música.', kicker='D e d d / E d e e'),
    dict(theme='dark', type='photo', img=2, badge='TREINO CERTO', title='COMECE A 60 BPM', outline='sem pressa', body='Pad, metrônomo e som limpo. Se embolou, baixa o BPM. Técnica não aceita mentira.', kicker='5 minutos por dia > 1 hora torta'),
    dict(theme='light', type='photo', img=3, badge='APLICAÇÃO', title='LEVE PRO GROOVE', outline='de verdade', body='Mova os acentos entre caixa, tons e chimbal. O paradiddle vira fraseado, não só exercício.', kicker='Rudimento + musicalidade'),
    dict(theme='dark', type='content', img=None, badge='ERRO COMUM', title='PULSO TRAVADO', outline='mata o som', body='Se o punho endurece, o groove fica quadrado. Respira, solta o braço e escuta o rebote.', kicker='Som bonito vem de movimento livre.'),
    dict(theme='pink', type='cta', img=0, badge='LA MUSIC SCHOOL', title='QUER TOCAR', outline='com precisão?', body='Aula de bateria pra quem quer técnica, som e atitude. Pra Quem Sabe o Que Quer.', kicker='Chama a LA Music School'),
]

css = f'''
@font-face {{ font-family: Prompt; src: url('{uri(font_regular)}') format('truetype'); font-weight: 400; }}
@font-face {{ font-family: Prompt; src: url('{uri(font_medium)}') format('truetype'); font-weight: 500; }}
@font-face {{ font-family: Prompt; src: url('{uri(font_semibold)}') format('truetype'); font-weight: 600; }}
@font-face {{ font-family: Prompt; src: url('{uri(font_bold)}') format('truetype'); font-weight: 700; }}
@font-face {{ font-family: Prompt; src: url('{uri(font_black)}') format('truetype'); font-weight: 900; }}
* {{ box-sizing:border-box; }} html, body {{ margin:0; width:1080px; height:1440px; overflow:hidden; font-family:Prompt, sans-serif; }}
.slide {{ position:relative; width:1080px; height:1440px; overflow:hidden; color:#fff; background:#0A0A0A; isolation:isolate; }}
.slide.light {{ background:#E8E8E8; color:#0A0A0A; }} .slide.pink {{ background:linear-gradient(145deg,#E91451 0%,#B01545 100%); color:#fff; }}
.bg {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; filter:contrast(1.18) saturate(1.12); z-index:-8; }}
.dark .bg {{ opacity:.62; }} .pink .bg {{ opacity:.20; mix-blend-mode:multiply; }} .light .bg {{ opacity:.20; filter:grayscale(1) contrast(1.2); }}
.overlay {{ position:absolute; inset:0; z-index:-7; background:radial-gradient(circle at 70% 24%, rgba(233,20,81,.42), transparent 32%), linear-gradient(180deg, rgba(10,10,10,.05), rgba(10,10,10,.80)); }}
.light .overlay {{ background:radial-gradient(circle at 80% 18%, rgba(233,20,81,.22), transparent 34%); }} .pink .overlay {{ background:radial-gradient(circle at 75% 18%, rgba(255,255,255,.18), transparent 30%); }}
.logo {{ position:absolute; top:54px; left:62px; width:250px; max-height:90px; z-index:20; }} .logo.center {{ left:50%; transform:translateX(-50%); width:310px; }}
/* Watermark LA oficial: SEM TEXTO. Somente SVG solo oficial em múltiplos tamanhos. */
.wm {{ position:absolute; pointer-events:none; z-index:-4; opacity:.11; object-fit:contain; }}
.wm.a {{ width:660px; right:-220px; top:125px; transform:rotate(-9deg); opacity:.13; }}
.wm.b {{ width:360px; left:-90px; bottom:245px; transform:rotate(12deg); opacity:.10; }}
.wm.c {{ width:170px; right:74px; bottom:138px; transform:rotate(-17deg); opacity:.16; }}
.light .wm {{ opacity:.13; }} .light .wm.c {{ opacity:.20; }} .pink .wm {{ opacity:.16; }} .pink .wm.a {{ opacity:.19; }}
.halftone {{ position:absolute; right:-70px; top:145px; width:540px; height:540px; opacity:.58; z-index:-3; background-image:radial-gradient(circle,#E91451 0 5px,transparent 6px); background-size:28px 28px; mask-image:radial-gradient(circle,#000 20%,transparent 73%); }}
.light .halftone {{ opacity:.34; }} .pink .halftone {{ opacity:.25; background-image:radial-gradient(circle,#0A0A0A 0 5px,transparent 6px); }}
.stroke-num {{ position:absolute; left:42px; top:390px; font-size:260px; line-height:.8; font-weight:900; color:transparent; -webkit-text-stroke:3px rgba(233,20,81,.25); transform:rotate(-5deg); z-index:-2; }}
.content {{ position:absolute; left:64px; right:64px; top:218px; z-index:10; }} .content.low {{ top:612px; }}
.badge {{ display:inline-block; background:#E91451; color:#fff; font-weight:900; font-size:24px; letter-spacing:2.5px; padding:13px 22px; border-radius:14px; box-shadow:10px 10px 0 rgba(0,0,0,.46); margin-bottom:26px; }} .pink .badge {{ background:#0A0A0A; }}
.title {{ font-size:106px; font-weight:900; line-height:.88; letter-spacing:-5px; text-transform:uppercase; margin:0; max-width:950px; }} .title .pinkword {{ color:#E91451; }} .pink .title .pinkword {{ color:#fff; }}
.outline {{ display:block; color:transparent; font-size:91px; font-weight:900; line-height:.9; letter-spacing:-4px; text-transform:uppercase; margin-top:10px; -webkit-text-stroke:3px #fff; }} .light .outline {{ -webkit-text-stroke-color:#0A0A0A; }}
.bodycopy {{ margin-top:34px; max-width:770px; font-size:35px; line-height:1.14; font-weight:500; }} .light .bodycopy {{ color:#222; }}
.kicker {{ margin-top:30px; display:inline-block; border:2px solid currentColor; border-radius:999px; padding:14px 24px; font-size:24px; font-weight:800; }}
.card {{ background:#E91451; color:#fff; border-radius:22px; padding:38px 44px; display:inline-block; box-shadow:18px 18px 0 rgba(0,0,0,.52); max-width:910px; }} .pink .card {{ background:#0A0A0A; }}
.pattern-bars {{ position:absolute; bottom:62px; left:50%; transform:translateX(-50%); width:420px; height:58px; background:repeating-linear-gradient(105deg, transparent 0 16px, rgba(255,255,255,.9) 17px 25px); opacity:.95; z-index:11; }} .light .pattern-bars {{ background:repeating-linear-gradient(105deg, transparent 0 16px, rgba(10,10,10,.86) 17px 25px); }}
.footer {{ position:absolute; bottom:94px; left:50%; transform:translateX(-50%); background:#E91451; color:#fff; border-radius:999px; padding:18px 46px; font-size:30px; font-weight:900; z-index:18; box-shadow:0 14px 0 rgba(0,0,0,.38); letter-spacing:.5px; }} .pink .footer {{ background:#0A0A0A; }}
.chev {{ position:absolute; bottom:113px; left:54px; color:#E91451; font-size:56px; font-weight:900; letter-spacing:-8px; transform:skewX(-12deg); z-index:13; }} .pink .chev {{ color:#fff; }}
.num {{ position:absolute; right:64px; bottom:86px; font-size:30px; font-weight:900; opacity:.72; z-index:19; }}
'''

for i, s in enumerate(slides, 1):
    logo = logo_light_full if s['theme'] == 'light' else logo_dark_full
    wm = wm_light if s['theme'] == 'light' else wm_dark
    bg = f"<img class='bg' src='{uri(imgs[s['img']])}'>" if s.get('img') is not None else ''
    content_class = 'content low' if s['type'] == 'photo' else 'content'
    title = s['title'].replace('|', "<span class='pinkword'>") + ("</span>" if '|' in s['title'] else '')
    card_open = "<div class='card'>" if s['type'] in ['cover','cta'] else ''
    card_close = "</div>" if card_open else ''
    center = 'center' if i in [1,8] else ''
    html = f"""<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>
<section class='slide {s['theme']}'>
{bg}<div class='overlay'></div>
<img class='wm a' src='{uri(wm)}'><img class='wm b' src='{uri(wm)}'><img class='wm c' src='{uri(wm)}'>
<div class='halftone'></div><div class='stroke-num'>{i:02d}</div>
<img class='logo {center}' src='{uri(logo)}'>
<div class='{content_class}'>
{card_open}<div class='badge'>{s['badge']}</div>
<h1 class='title'>{title}<span class='outline'>{s['outline']}</span></h1>
<div class='bodycopy'>{s['body']}</div><div class='kicker'>{s['kicker']}</div>{card_close}
</div>
<div class='chev'>&gt;&gt;&gt;&gt;</div><div class='pattern-bars'></div><div class='footer'>@lamusicschool</div><div class='num'>{i:02d}/08</div>
</section></body></html>"""
    (html_dir/f'la-school-paradiddle-skill-{i:02d}.html').write_text(html, encoding='utf-8')

# Render PNGs
for i in range(1,9):
    html = html_dir/f'la-school-paradiddle-skill-{i:02d}.html'
    png = png_dir/f'la-school-paradiddle-skill-{i:02d}.png'
    subprocess.run([
        '/usr/local/bin/chromium', '--headless=new', '--no-sandbox', '--disable-gpu',
        '--hide-scrollbars', '--window-size=1080,1440', f'--screenshot={png}', html.resolve().as_uri()
    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Preview grid 4x2
thumbs = []
for i in range(1,9):
    im = Image.open(png_dir/f'la-school-paradiddle-skill-{i:02d}.png').convert('RGB')
    im.thumbnail((270,360), Image.LANCZOS)
    thumbs.append(im.copy())
preview = Image.new('RGB', (1080, 720), '#111111')
for idx, im in enumerate(thumbs):
    x = (idx % 4) * 270
    y = (idx // 4) * 360
    preview.paste(im, (x,y))
preview_path = out/'preview-grid.jpg'
preview.save(preview_path, quality=92)

# QA doc
qa = '''# QA — LAHQ Skill Test — Paradiddle School

- Skill usada: `lahq-content-pipeline`.
- Runbook consultado: `docs/runbooks/LAHQ_SCHOOL_CARROSSEL.md`.
- Brand guide consultado: `shared/brand-guides/brand-la-music-school.md`.
- DS canônico consultado: `shared/design-systems/LA_MUSIC_SCHOOL_DS_CANONICAL.md`.
- Formato: 1080x1440, 8 cards.
- Watermark LA: SVG oficial solo-vazada em 3 tamanhos por card (`wm a/b/c`). Nenhum `LA` digitado como marca d'água.
- Logo: SVG oficial completo em todos os cards.
- Elementos-assinatura: halftone, outline type, pink blob/container, chevrons, footer pill @lamusicschool, barras diagonais, numeração.
- Paleta: #E91451, #B01545, #0A0A0A, #E8E8E8.
- Fonte: Prompt local.
'''
(out/'QA.md').write_text(qa, encoding='utf-8')

# Package
package = out.parent/'la-school-paradiddle-skill-test-carousel.tar.gz'
if package.exists(): package.unlink()
with tarfile.open(package, 'w:gz') as tar:
    tar.add(out, arcname=out.name)
print(out)
print(package)
