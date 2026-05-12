from pathlib import Path
from PIL import Image
import shutil, subprocess, tarfile

repo = Path('/root/.openclaw/workspace/repos/la-hq-agents')
out = Path('/root/.openclaw/workspace/outputs/la-school-stage-posture-singer-test-v2')
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
  dict(theme='dark', kind='hero1', img=0, wm='top-left-huge', wmfile='vaz-dark', logo='center', badge='POSTURA DE PALCO', title='PALCO NÃO É', outline='esconderijo', body='Antes da primeira nota, seu corpo já começou a cantar.', kicker='Passe pro lado →'),
  dict(theme='pink', kind='hero2', img=0, wm='left-color-bleed', wmfile='color-dark', logo='left', badge='PRESENÇA', title='ENTRA COMO', outline='protagonista', body='O público precisa entender onde olhar. Você mostra isso com postura.', kicker='Corpo também comunica'),
  dict(theme='light', kind='type', wm='top-giant-light', wmfile='vaz-light', logo='left', badge='BASE', title='PÉ NO CHÃO', outline='voz no corpo', body='Distribua o peso. Um pé levemente à frente. Joelho solto. Nada de travar.', kicker='Segurança começa na base'),
  dict(theme='dark', kind='photo', img=2, wm='bottom-left-vaz', wmfile='vaz-dark', logo='left', badge='MICROFONE', title='NÃO USE COMO', outline='escudo', body='Aproxime o microfone com intenção. Não esconda o rosto atrás dele.', kicker='Mostra a expressão'),
  dict(theme='light', kind='type', wm='center-cut-light', wmfile='vaz-light', logo='left', badge='RESPIRAÇÃO', title='PEITO ABERTO', outline='sem rigidez', body='Abrir o corpo não é estufar. É liberar espaço pra voz sair inteira.', kicker='Solto, não largado'),
  dict(theme='dark', kind='type', wm='left-edge-dark', wmfile='vaz-dark', logo='left', badge='OLHAR', title='ESCOLHA ALGUÉM', outline='na plateia', body='Olhar perdido entrega insegurança. Escolha pontos no público e sustente.', kicker='Contato cria presença'),
  dict(theme='pink', kind='type', wm='none', wmfile='vaz-dark', logo='left', badge='MOVIMENTO', title='NÃO ANDE', outline='à toa', body='Todo passo precisa ter intenção: chegar, abrir, marcar, respirar.', kicker='Movimento sem motivo distrai'),
  dict(theme='dark', kind='cta', wm='top-right-crop', wmfile='color-dark', logo='center', badge='LA MUSIC SCHOOL', title='QUER CANTAR', outline='com presença?', body='Aula de canto pra desenvolver voz, corpo e palco. Pra Quem Sabe o Que Quer.', kicker='Chama a LA Music School'),
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
.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:contrast(1.16) saturate(1.08);z-index:-10}} .photo .bg{{opacity:.60}}
.hero-person{{position:absolute;z-index:-7;object-fit:cover;filter:contrast(1.12) saturate(1.06)}} .hero1 .hero-person{{height:1260px;right:-118px;bottom:0;opacity:.92}} .hero2 .hero-person{{height:1280px;left:-610px;bottom:0;opacity:.38;filter:contrast(1.15) saturate(1.2)}}
.overlay{{position:absolute;inset:0;z-index:-9;background:radial-gradient(circle at 74% 20%,rgba(233,20,81,.36),transparent 32%),linear-gradient(180deg,rgba(10,10,10,.06),rgba(10,10,10,.84))}} .light .overlay{{background:radial-gradient(circle at 25% 18%,rgba(233,20,81,.16),transparent 36%)}} .pink .overlay{{background:radial-gradient(circle at 25% 28%,rgba(255,255,255,.15),transparent 33%)}}
.wm{{position:absolute;object-fit:contain;pointer-events:none;z-index:-6}} .wm.none{{display:none}}
.wm.top-left-huge{{width:980px;left:-350px;top:-215px;opacity:.14;transform:rotate(9deg)}}
.wm.left-color-bleed{{width:920px;left:-410px;bottom:95px;opacity:.17;transform:rotate(5deg)}}
.wm.top-giant-light{{width:1060px;left:-245px;top:-285px;opacity:.145;transform:rotate(-4deg)}}
.wm.bottom-left-vaz{{width:780px;left:-330px;bottom:-155px;opacity:.12;transform:rotate(-12deg)}}
.wm.center-cut-light{{width:980px;left:120px;top:250px;opacity:.12;transform:rotate(4deg)}}
.wm.left-edge-dark{{width:900px;left:-500px;top:220px;opacity:.11;transform:rotate(10deg)}}
.wm.top-right-crop{{width:880px;right:-390px;top:-230px;opacity:.15;transform:rotate(-10deg)}}
.halftone{{position:absolute;width:560px;height:560px;opacity:.42;z-index:-4;background-image:radial-gradient(circle,#E91451 0 5px,transparent 6px);background-size:28px 28px;mask-image:radial-gradient(circle,#000 20%,transparent 73%)}} .halftone.a{{right:-80px;top:110px}} .halftone.b{{left:-120px;bottom:130px;transform:rotate(15deg)}} .pink .halftone{{background-image:radial-gradient(circle,#0A0A0A 0 5px,transparent 6px);opacity:.19}} .light .halftone{{opacity:.28}}
.content{{position:absolute;left:64px;right:64px;top:210px;z-index:15}} .content.low{{top:585px}} .content.mid{{top:360px}}
.card{{background:#E91451;color:#fff;border-radius:24px;padding:42px 48px;max-width:900px;display:inline-block;box-shadow:18px 18px 0 rgba(0,0,0,.50)}} .pink .card{{background:#0A0A0A}} .light .card{{box-shadow:18px 18px 0 rgba(0,0,0,.22)}}
.badge{{display:inline-block;background:#E91451;color:#fff;font-weight:900;font-size:25px;letter-spacing:2.4px;padding:13px 22px;border-radius:14px;box-shadow:10px 10px 0 rgba(0,0,0,.46);margin-bottom:26px}} .pink .badge{{background:#0A0A0A}}
.title{{font-size:106px;font-weight:900;line-height:.88;letter-spacing:-5px;text-transform:uppercase;margin:0;max-width:900px}} .outline{{display:block;color:transparent;font-size:91px;font-weight:900;line-height:.9;letter-spacing:-4px;text-transform:uppercase;margin-top:10px;-webkit-text-stroke:3px #fff}} .light .outline{{-webkit-text-stroke-color:#0A0A0A}}
.bodycopy{{margin-top:32px;max-width:820px;font-size:39px;line-height:1.13;font-weight:600}} .light .bodycopy{{color:#222}}
.kicker{{margin-top:30px;display:inline-block;border:2px solid currentColor;border-radius:999px;padding:16px 28px;font-size:27px;font-weight:800}}
.chev{{position:absolute;bottom:113px;left:54px;color:#E91451;font-size:56px;font-weight:900;letter-spacing:-8px;transform:skewX(-12deg);z-index:16}} .pink .chev{{color:#fff}}
.footer{{position:absolute;bottom:94px;left:50%;transform:translateX(-50%);background:#E91451;color:#fff;border-radius:999px;padding:18px 46px;font-size:30px;font-weight:900;z-index:22;box-shadow:0 14px 0 rgba(0,0,0,.38);letter-spacing:.5px}} .pink .footer{{background:#0A0A0A}}
.bars{{position:absolute;bottom:62px;left:50%;transform:translateX(-50%);width:420px;height:58px;background:repeating-linear-gradient(105deg,transparent 0 16px,rgba(255,255,255,.9) 17px 25px);opacity:.95;z-index:18}} .light .bars{{background:repeating-linear-gradient(105deg,transparent 0 16px,rgba(10,10,10,.86) 17px 25px)}}
.num{{position:absolute;right:64px;bottom:86px;font-size:30px;font-weight:900;opacity:.72;z-index:24}}
'''

for i,s in enumerate(slides,1):
    theme=s['theme']; kind=s['kind']
    logo = logo_light_full if theme=='light' else logo_dark_full
    wm_map={'vaz-light': wm_light_vaz, 'vaz-dark': wm_dark_vaz, 'color-dark': wm_dark}
    wm = wm_map[s['wmfile']]
    bg=''
    if kind in ['hero1','hero2']:
        bg=f"<img class='hero-person' src='{uri(imgs[s['img']])}'>"
    elif kind=='photo':
        bg=f"<img class='bg' src='{uri(imgs[s['img']])}'>"
    content_cls='content low' if kind in ['hero1','photo'] else ('content mid' if kind=='hero2' else 'content')
    card_open = "<div class='card'>" if kind in ['hero1','cta'] else ''
    card_close = "</div>" if card_open else ''
    logo_center = 'center' if s['logo']=='center' else ''
    hclass = 'a' if i % 2 else 'b'
    html=f"""<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>
<section class='slide {theme} {kind}'>
{bg}<div class='overlay'></div><img class='wm {s['wm']}' src='{uri(wm)}'><div class='halftone {hclass}'></div>
<img class='logo {logo_center}' src='{uri(logo)}'>
<div class='{content_cls}'>{card_open}<div class='badge'>{s['badge']}</div><h1 class='title'>{s['title']}<span class='outline'>{s['outline']}</span></h1><div class='bodycopy'>{s['body']}</div><div class='kicker'>{s['kicker']}</div>{card_close}</div>
<div class='chev'>&gt;&gt;&gt;&gt;</div><div class='bars'></div><div class='footer'>@lamusicschool</div><div class='num'>{i:02d}/08</div>
</section></body></html>"""
    (html_dir/f'la-school-stage-posture-v2-{i:02d}.html').write_text(html)

for i in range(1,9):
    html=html_dir/f'la-school-stage-posture-v2-{i:02d}.html'; png=png_dir/f'la-school-stage-posture-v2-{i:02d}.png'
    subprocess.run(['/usr/local/bin/chromium','--headless=new','--no-sandbox','--disable-gpu','--hide-scrollbars','--window-size=1080,1440',f'--screenshot={png}',html.resolve().as_uri()],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

preview=Image.new('RGB',(1080,720),'#111')
for idx in range(8):
    im=Image.open(png_dir/f'la-school-stage-posture-v2-{idx+1:02d}.png').convert('RGB'); im.thumbnail((270,360),Image.LANCZOS)
    preview.paste(im,((idx%4)*270,(idx//4)*360))
preview.save(out/'preview-grid.jpg',quality=92)

(out/'QA.md').write_text('''# QA — Stage Posture Singer Test V2

- Skill carregada e atualizada: QA deve reprovar padrão mecânico de LA no mesmo canto/tamanho.
- Correção principal: símbolo LA reposicionado card a card: topo/esquerda, esquerda vazando, topo gigante, rodapé esquerdo, centro cortado, borda esquerda, ausente, topo direito.
- Sem LA digitado como watermark.
- Tema: postura de palco para cantor.
- Formato: 8 cards 1080x1440.
''')
package=out.parent/'la-school-stage-posture-singer-test-v2-carousel.tar.gz'
if package.exists(): package.unlink()
with tarfile.open(package,'w:gz') as tar: tar.add(out,arcname=out.name)
print(out); print(package)
