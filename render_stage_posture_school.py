from pathlib import Path
from PIL import Image
import shutil, subprocess, tarfile

repo = Path('/root/.openclaw/workspace/repos/la-hq-agents')
out = Path('/root/.openclaw/workspace/outputs/la-school-stage-posture-singer-test')
html_dir = out/'html'; png_dir = out/'png'; asset_dir = out/'assets'
for d in [html_dir, png_dir, asset_dir]: d.mkdir(parents=True, exist_ok=True)

src_imgs = [
    Path('/root/.openclaw/media/tool-image-generation/la-school-stage-posture-singer-hero---0071f6dc-70a2-4c56-9dec-de88b040e83b.png'),
    Path('/root/.openclaw/media/tool-image-generation/la-school-stage-posture-singer-hero---1182aabd-eb5a-4dea-8319-b33283e1398b.png'),
    Path('/root/.openclaw/media/tool-image-generation/la-school-stage-posture-mic-closeup---351cef2c-c085-42e0-820a-66e0c5885a28.png'),
]
imgs=[]
for p in src_imgs:
    dst=asset_dir/p.name; shutil.copy2(p,dst); imgs.append(dst)

logos=repo/'shared/brand-assets/logos/school'
font_dir=repo/'shared/brand-assets/fonts/school'
logo_dark_full=logos/'logo-la-music-dark-completa.svg'
logo_light_full=logos/'logo-la-music-light-completa.svg'
wm_dark=logos/'logo-la-music-dark-solo.svg'
wm_dark_vaz=logos/'logo-la-music-dark-solo-vazada.svg'
wm_light_vaz=logos/'logo-la-music-light-solo-vazada.svg'

def uri(p): return Path(p).resolve().as_uri()

slides = [
  dict(theme='dark', kind='hero1', badge='POSTURA DE PALCO', title='PALCO NÃO É', outline='esconderijo', body='Antes da primeira nota, seu corpo já começou a cantar.', kicker='Passe pro lado →'),
  dict(theme='pink', kind='hero2', badge='PRESENÇA', title='ENTRA COMO', outline='protagonista', body='O público precisa entender onde olhar. Você mostra isso com postura.', kicker='Corpo também comunica'),
  dict(theme='light', kind='type', badge='BASE', title='PÉ NO CHÃO', outline='voz no corpo', body='Distribua o peso. Um pé levemente à frente. Joelho solto. Nada de travar.', kicker='Segurança começa na base'),
  dict(theme='dark', kind='photo', img=2, badge='MICROFONE', title='NÃO USE COMO', outline='escudo', body='Aproxime o microfone com intenção. Não esconda o rosto atrás dele.', kicker='Mostra a expressão'),
  dict(theme='light', kind='type', badge='RESPIRAÇÃO', title='PEITO ABERTO', outline='sem rigidez', body='Abrir o corpo não é estufar. É liberar espaço pra voz sair inteira.', kicker='Solto, não largado'),
  dict(theme='dark', kind='type', badge='OLHAR', title='ESCOLHA ALGUÉM', outline='na plateia', body='Olhar perdido entrega insegurança. Escolha pontos no público e sustente.', kicker='Contato cria presença'),
  dict(theme='pink', kind='type', badge='MOVIMENTO', title='NÃO ANDE', outline='à toa', body='Todo passo precisa ter intenção: chegar, abrir, marcar, respirar.', kicker='Movimento sem motivo distrai'),
  dict(theme='dark', kind='cta', badge='LA MUSIC SCHOOL', title='QUER CANTAR', outline='com presença?', body='Aula de canto pra desenvolver voz, corpo e palco. Pra Quem Sabe o Que Quer.', kicker='Chama a LA Music School'),
]

css=f'''
@font-face {{ font-family:Prompt; src:url('{uri(font_dir/'Prompt-Regular.ttf')}') format('truetype'); font-weight:400; }}
@font-face {{ font-family:Prompt; src:url('{uri(font_dir/'Prompt-Medium.ttf')}') format('truetype'); font-weight:500; }}
@font-face {{ font-family:Prompt; src:url('{uri(font_dir/'Prompt-SemiBold.ttf')}') format('truetype'); font-weight:600; }}
@font-face {{ font-family:Prompt; src:url('{uri(font_dir/'Prompt-Bold.ttf')}') format('truetype'); font-weight:700; }}
@font-face {{ font-family:Prompt; src:url('{uri(font_dir/'Prompt-Black.ttf')}') format('truetype'); font-weight:900; }}
*{{box-sizing:border-box}} html,body{{margin:0;width:1080px;height:1440px;overflow:hidden;font-family:Prompt,sans-serif}}
.slide{{position:relative;width:1080px;height:1440px;overflow:hidden;background:#0A0A0A;color:#fff;isolation:isolate}} .light{{background:#E8E8E8;color:#0A0A0A}} .pink{{background:linear-gradient(145deg,#E91451 0%,#B01545 100%);color:#fff}}
.logo{{position:absolute;top:54px;left:62px;width:248px;max-height:90px;z-index:30}} .logo.center{{left:50%;transform:translateX(-50%);width:310px}}
.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:contrast(1.16) saturate(1.08);z-index:-9}} .photo .bg{{opacity:.56}} .dark.photo .bg{{opacity:.58}}
.hero-person{{position:absolute;z-index:-5;object-fit:cover;filter:contrast(1.12) saturate(1.06)}} .hero1 .hero-person{{height:1260px;right:-140px;bottom:0;opacity:.92}} .hero2 .hero-person{{height:1260px;left:-610px;bottom:0;opacity:.35;filter:contrast(1.15) saturate(1.2)}}
.overlay{{position:absolute;inset:0;z-index:-8;background:radial-gradient(circle at 74% 20%,rgba(233,20,81,.36),transparent 32%),linear-gradient(180deg,rgba(10,10,10,.08),rgba(10,10,10,.82))}} .light .overlay{{background:radial-gradient(circle at 80% 18%,rgba(233,20,81,.18),transparent 34%)}} .pink .overlay{{background:radial-gradient(circle at 75% 18%,rgba(255,255,255,.15),transparent 32%)}}
.wm{{position:absolute;object-fit:contain;pointer-events:none;z-index:-6}} .wm.big-right{{width:910px;right:-360px;top:135px;opacity:.115;transform:rotate(-8deg)}} .wm.big-left{{width:870px;left:-360px;top:250px;opacity:.13;transform:rotate(8deg)}} .wm.color{{width:760px;right:-280px;bottom:130px;opacity:.16;transform:rotate(-10deg)}} .pink .wm{{opacity:.16}} .light .wm{{opacity:.14}}
.halftone{{position:absolute;right:-80px;top:110px;width:560px;height:560px;opacity:.46;z-index:-4;background-image:radial-gradient(circle,#E91451 0 5px,transparent 6px);background-size:28px 28px;mask-image:radial-gradient(circle,#000 20%,transparent 73%)}} .pink .halftone{{background-image:radial-gradient(circle,#0A0A0A 0 5px,transparent 6px);opacity:.22}} .light .halftone{{opacity:.30}}
.content{{position:absolute;left:64px;right:64px;top:210px;z-index:15}} .content.low{{top:585px}} .content.mid{{top:360px}}
.card{{background:#E91451;color:#fff;border-radius:24px;padding:40px 46px;max-width:900px;display:inline-block;box-shadow:18px 18px 0 rgba(0,0,0,.50)}} .pink .card{{background:#0A0A0A}} .light .card{{box-shadow:18px 18px 0 rgba(0,0,0,.22)}}
.badge{{display:inline-block;background:#E91451;color:#fff;font-weight:900;font-size:24px;letter-spacing:2.5px;padding:13px 22px;border-radius:14px;box-shadow:10px 10px 0 rgba(0,0,0,.46);margin-bottom:26px}} .pink .badge{{background:#0A0A0A}}
.title{{font-size:105px;font-weight:900;line-height:.88;letter-spacing:-5px;text-transform:uppercase;margin:0;max-width:900px}} .pinkword{{color:#E91451}} .pink .pinkword{{color:#fff}}
.outline{{display:block;color:transparent;font-size:90px;font-weight:900;line-height:.9;letter-spacing:-4px;text-transform:uppercase;margin-top:10px;-webkit-text-stroke:3px #fff}} .light .outline{{-webkit-text-stroke-color:#0A0A0A}}
.bodycopy{{margin-top:32px;max-width:800px;font-size:38px;line-height:1.13;font-weight:600}} .light .bodycopy{{color:#222}}
.kicker{{margin-top:30px;display:inline-block;border:2px solid currentColor;border-radius:999px;padding:16px 28px;font-size:27px;font-weight:800}}
.chev{{position:absolute;bottom:113px;left:54px;color:#E91451;font-size:56px;font-weight:900;letter-spacing:-8px;transform:skewX(-12deg);z-index:16}} .pink .chev{{color:#fff}}
.footer{{position:absolute;bottom:94px;left:50%;transform:translateX(-50%);background:#E91451;color:#fff;border-radius:999px;padding:18px 46px;font-size:30px;font-weight:900;z-index:22;box-shadow:0 14px 0 rgba(0,0,0,.38);letter-spacing:.5px}} .pink .footer{{background:#0A0A0A}}
.bars{{position:absolute;bottom:62px;left:50%;transform:translateX(-50%);width:420px;height:58px;background:repeating-linear-gradient(105deg,transparent 0 16px,rgba(255,255,255,.9) 17px 25px);opacity:.95;z-index:18}} .light .bars{{background:repeating-linear-gradient(105deg,transparent 0 16px,rgba(10,10,10,.86) 17px 25px)}}
.num{{position:absolute;right:64px;bottom:86px;font-size:30px;font-weight:900;opacity:.72;z-index:24}}
'''

for i,s in enumerate(slides,1):
    theme=s['theme']; kind=s['kind']
    logo = logo_light_full if theme=='light' else logo_dark_full
    wm = wm_light_vaz if theme=='light' else (wm_dark if i in [2,8] else wm_dark_vaz)
    bg=''
    if kind in ['hero1','hero2']:
        bg=f"<img class='hero-person' src='{uri(imgs[0])}'>"
    elif kind=='photo':
        bg=f"<img class='bg' src='{uri(imgs[s['img']])}'>"
    wm_cls = 'color' if i in [2,8] else ('big-left' if i in [4,6] else 'big-right')
    content_cls='content low' if kind in ['hero1','photo'] else ('content mid' if kind=='hero2' else 'content')
    card_open = "<div class='card'>" if kind in ['hero1','cta'] else ''
    card_close = "</div>" if card_open else ''
    logo_center = 'center' if i in [1,8] else ''
    html=f"""<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>
<section class='slide {theme} {kind}'>
{bg}<div class='overlay'></div><img class='wm {wm_cls}' src='{uri(wm)}'><div class='halftone'></div>
<img class='logo {logo_center}' src='{uri(logo)}'>
<div class='{content_cls}'>{card_open}<div class='badge'>{s['badge']}</div><h1 class='title'>{s['title']}<span class='outline'>{s['outline']}</span></h1><div class='bodycopy'>{s['body']}</div><div class='kicker'>{s['kicker']}</div>{card_close}</div>
<div class='chev'>&gt;&gt;&gt;&gt;</div><div class='bars'></div><div class='footer'>@lamusicschool</div><div class='num'>{i:02d}/08</div>
</section></body></html>"""
    (html_dir/f'la-school-stage-posture-{i:02d}.html').write_text(html)

for i in range(1,9):
    html=html_dir/f'la-school-stage-posture-{i:02d}.html'; png=png_dir/f'la-school-stage-posture-{i:02d}.png'
    subprocess.run(['/usr/local/bin/chromium','--headless=new','--no-sandbox','--disable-gpu','--hide-scrollbars','--window-size=1080,1440',f'--screenshot={png}',html.resolve().as_uri()],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

preview=Image.new('RGB',(1080,720),'#111')
for idx in range(8):
    im=Image.open(png_dir/f'la-school-stage-posture-{idx+1:02d}.png').convert('RGB'); im.thumbnail((270,360),Image.LANCZOS)
    preview.paste(im,((idx%4)*270,(idx//4)*360))
preview.save(out/'preview-grid.jpg',quality=92)

(out/'QA.md').write_text('''# QA — Stage Posture Singer Test

- Skill usada: lahq-content-pipeline, versão enxuta aprovada.
- Tema: postura de palco para cantor.
- Formato: 8 cards 1080x1440.
- Fotos: hero de cantor atravessando card 1/2 (continuidade sutil) + close de microfone no card 4. Demais cards tipográficos/DS.
- Logo: SVG oficial; símbolo LA oficial como composição variável, incluindo versão colorida/transparente em cards pink/dark.
- Elementos: halftone, outline type, chevrons, footer pill, Prompt, paleta School.
- Sem LA digitado como watermark.
''')
package=out.parent/'la-school-stage-posture-singer-test-carousel.tar.gz'
if package.exists(): package.unlink()
with tarfile.open(package,'w:gz') as tar: tar.add(out,arcname=out.name)
print(out); print(package)
