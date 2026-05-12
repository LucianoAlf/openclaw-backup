from pathlib import Path
from PIL import Image
import shutil, subprocess, tarfile

repo = Path('/root/.openclaw/workspace/repos/la-hq-agents')
out = Path('/root/.openclaw/workspace/outputs/la-school-stage-posture-singer-test-v3')
html_dir = out/'html'; png_dir = out/'png'; asset_dir = out/'assets'
for d in [html_dir, png_dir, asset_dir]: d.mkdir(parents=True, exist_ok=True)

src_imgs = [
    Path('/root/.openclaw/media/tool-image-generation/la-school-singer-stage-hero-10---3aeec81b-5091-49f5-a500-bd6fb1f1fded.png'),
    Path('/root/.openclaw/media/tool-image-generation/la-school-singer-mic-closeup-10---38c75dc6-5fc4-447f-8510-6c61e941d284.png'),
    Path('/root/.openclaw/media/tool-image-generation/la-school-singer-side-stage-10---0f879db7-6920-4ff0-ba84-861b55c10ffb.png'),
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
  dict(theme='dark', layout='cover', img=0, logo='center', wm='none', badge='POSTURA DE PALCO', title='CANTE COMO', outline='protagonista', body='O público vê sua presença antes de ouvir sua primeira nota.', kicker='Passe pro lado →'),
  dict(theme='pink', layout='continuation', img=0, logo='left', wm='left_color', badge='PRESENÇA', title='O CORPO', outline='também canta', body='O jeito que você entra no palco já diz se você acredita no que vai cantar.', kicker='Entra decidido. Fica inteiro.'),
  dict(theme='light', layout='bigtype', logo='left', wm='top_light', badge='BASE', title='PÉ NO CHÃO', outline='voz no corpo', body='Peso distribuído. Um pé levemente à frente. Joelho solto. Nada de travar.', kicker='Segurança começa na base'),
  dict(theme='dark', layout='photo_card', img=1, logo='left', wm='bottom_left', badge='MICROFONE', title='NÃO USE COMO', outline='escudo', body='O microfone aproxima sua voz. Não esconda sua expressão atrás dele.', kicker='Mostra o rosto. Sustenta o olhar.'),
  dict(theme='pink', layout='statement', logo='left', wm='none', badge='ATITUDE', title='POSTURA NÃO É', outline='pose', body='É presença. É intenção. É fazer cada gesto trabalhar pela música.', kicker='Menos teatro. Mais verdade.'),
  dict(theme='dark', layout='side_photo', img=2, logo='left', wm='top_left', badge='OLHAR', title='ESCOLHA', outline='alguém', body='Olhar perdido entrega insegurança. Escolha pontos na plateia e sustente.', kicker='Contato cria presença'),
  dict(theme='light', layout='diagram', logo='left', wm='center_light', badge='MOVIMENTO', title='NÃO ANDE', outline='à toa', body='Chegue. Abra. Marque. Respire. Todo passo precisa ter intenção.', kicker='Movimento sem motivo distrai'),
  dict(theme='dark', layout='cta', img=0, logo='center', wm='right_color', badge='LA MUSIC SCHOOL', title='QUER CANTAR', outline='com presença?', body='Aula de canto pra desenvolver voz, corpo e palco. Pra Quem Sabe o Que Quer.', kicker='Chama a LA Music School'),
]

css=f'''
@font-face {{ font-family:Prompt; src:url('{uri(font_dir/'Prompt-Regular.ttf')}') format('truetype'); font-weight:400; }}
@font-face {{ font-family:Prompt; src:url('{uri(font_dir/'Prompt-Medium.ttf')}') format('truetype'); font-weight:500; }}
@font-face {{ font-family:Prompt; src:url('{uri(font_dir/'Prompt-SemiBold.ttf')}') format('truetype'); font-weight:600; }}
@font-face {{ font-family:Prompt; src:url('{uri(font_dir/'Prompt-Bold.ttf')}') format('truetype'); font-weight:700; }}
@font-face {{ font-family:Prompt; src:url('{uri(font_dir/'Prompt-Black.ttf')}') format('truetype'); font-weight:900; }}
*{{box-sizing:border-box}} html,body{{margin:0;width:1080px;height:1440px;overflow:hidden;font-family:Prompt,sans-serif}}
.slide{{position:relative;width:1080px;height:1440px;overflow:hidden;background:#0A0A0A;color:#fff;isolation:isolate}} .light{{background:#E8E8E8;color:#0A0A0A}} .pink{{background:linear-gradient(145deg,#E91451 0%,#B01545 100%);color:#fff}}
.logo{{position:absolute;top:54px;left:62px;width:248px;max-height:90px;z-index:40}} .logo.center{{left:50%;transform:translateX(-50%);width:318px}}
.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-12;filter:contrast(1.18) saturate(1.08)}}
.cover .bg{{opacity:.94}} .continuation .bg{{height:1260px;width:auto;left:-470px;top:145px;opacity:.24;filter:contrast(1.22) saturate(1.22)}} .photo_card .bg{{opacity:.58}} .side_photo .bg{{height:1180px;width:auto;right:-170px;bottom:0;opacity:.76}} .cta .bg{{opacity:.16;filter:grayscale(.35) contrast(1.2)}}
.overlay{{position:absolute;inset:0;z-index:-11;background:linear-gradient(90deg,rgba(10,10,10,.92) 0%,rgba(10,10,10,.74) 34%,rgba(10,10,10,.10) 100%),radial-gradient(circle at 76% 20%,rgba(233,20,81,.36),transparent 34%)}}
.cover .overlay{{background:linear-gradient(90deg,rgba(10,10,10,.94) 0%,rgba(10,10,10,.72) 43%,rgba(10,10,10,.20) 100%),linear-gradient(180deg,rgba(10,10,10,.05),rgba(10,10,10,.70))}}
.light .overlay{{background:radial-gradient(circle at 20% 18%,rgba(233,20,81,.16),transparent 34%)}} .pink .overlay{{background:radial-gradient(circle at 20% 12%,rgba(255,255,255,.16),transparent 36%)}}
.wm{{position:absolute;object-fit:contain;z-index:-8;pointer-events:none}} .wm.none{{display:none}}
.wm.left_color{{width:960px;left:-430px;bottom:40px;opacity:.15;transform:rotate(7deg)}} .wm.top_light{{width:1120px;left:-300px;top:-325px;opacity:.15;transform:rotate(-5deg)}} .wm.bottom_left{{width:830px;left:-380px;bottom:-180px;opacity:.12;transform:rotate(-13deg)}} .wm.top_left{{width:880px;left:-470px;top:-120px;opacity:.13;transform:rotate(10deg)}} .wm.center_light{{width:980px;right:-200px;top:310px;opacity:.11;transform:rotate(4deg)}} .wm.right_color{{width:880px;right:-390px;top:-230px;opacity:.15;transform:rotate(-10deg)}}
.halftone{{position:absolute;width:600px;height:600px;opacity:.42;z-index:-7;background-image:radial-gradient(circle,#E91451 0 5px,transparent 6px);background-size:28px 28px;mask-image:radial-gradient(circle,#000 19%,transparent 73%)}} .h1{{right:-120px;top:120px}} .h2{{left:-180px;bottom:120px;transform:rotate(15deg)}} .pink .halftone{{background-image:radial-gradient(circle,#0A0A0A 0 5px,transparent 6px);opacity:.18}} .light .halftone{{opacity:.28}}
.blob{{position:absolute;z-index:-6;background:#E91451;border-radius:42px;box-shadow:22px 22px 0 rgba(0,0,0,.45);transform:rotate(-3deg)}} .blob.cover{{left:62px;bottom:260px;width:720px;height:430px}} .blob.small{{right:70px;top:240px;width:290px;height:210px;transform:rotate(8deg);opacity:.95}}
.content{{position:absolute;left:64px;right:64px;top:208px;z-index:20}} .content.low{{top:650px}} .content.mid{{top:345px}} .content.bottom{{top:760px}}
.badge{{display:inline-block;background:#E91451;color:#fff;font-weight:900;font-size:25px;letter-spacing:2.4px;padding:13px 22px;border-radius:14px;box-shadow:10px 10px 0 rgba(0,0,0,.46);margin-bottom:26px}} .pink .badge{{background:#0A0A0A}}
.title{{font-size:112px;font-weight:900;line-height:.86;letter-spacing:-5.5px;text-transform:uppercase;margin:0;max-width:930px}} .cover .title{{font-size:118px}} .statement .title{{font-size:104px}}
.outline{{display:block;color:transparent;font-size:94px;font-weight:900;line-height:.88;letter-spacing:-4px;text-transform:uppercase;margin-top:10px;-webkit-text-stroke:3px #fff}} .light .outline{{-webkit-text-stroke-color:#0A0A0A}}
.bodycopy{{margin-top:32px;max-width:790px;font-size:40px;line-height:1.11;font-weight:650}} .light .bodycopy{{color:#222}}
.kicker{{margin-top:30px;display:inline-block;border:2px solid currentColor;border-radius:999px;padding:16px 28px;font-size:28px;font-weight:850}}
.card{{background:#E91451;color:#fff;border-radius:26px;padding:42px 48px;display:inline-block;max-width:900px;box-shadow:18px 18px 0 rgba(0,0,0,.52)}} .pink .card{{background:#0A0A0A}} .light .card{{box-shadow:18px 18px 0 rgba(0,0,0,.22)}}
.diagram-list{{display:grid;gap:24px;margin-top:42px;max-width:820px}} .diagram-item{{background:#0A0A0A;color:#fff;border-radius:22px;padding:24px 30px;font-size:34px;font-weight:800;box-shadow:12px 12px 0 rgba(233,20,81,.85)}}
.chev{{position:absolute;bottom:113px;left:54px;color:#E91451;font-size:56px;font-weight:900;letter-spacing:-8px;transform:skewX(-12deg);z-index:22}} .pink .chev{{color:#fff}}
.footer{{position:absolute;bottom:94px;left:50%;transform:translateX(-50%);background:#E91451;color:#fff;border-radius:999px;padding:18px 46px;font-size:30px;font-weight:900;z-index:30;box-shadow:0 14px 0 rgba(0,0,0,.38);letter-spacing:.5px}} .pink .footer{{background:#0A0A0A}}
.bars{{position:absolute;bottom:62px;left:50%;transform:translateX(-50%);width:420px;height:58px;background:repeating-linear-gradient(105deg,transparent 0 16px,rgba(255,255,255,.9) 17px 25px);opacity:.95;z-index:24}} .light .bars{{background:repeating-linear-gradient(105deg,transparent 0 16px,rgba(10,10,10,.86) 17px 25px)}}
.num{{position:absolute;right:64px;bottom:86px;font-size:30px;font-weight:900;opacity:.72;z-index:32}}
'''

for i,s in enumerate(slides,1):
    theme=s['theme']; layout=s['layout']
    logo = logo_light_full if theme=='light' else logo_dark_full
    wm_file = wm_dark if s.get('wm') in ['left_color','right_color'] else (wm_light_vaz if theme=='light' else wm_dark_vaz)
    bg=''
    if 'img' in s:
        bg=f"<img class='bg' src='{uri(imgs[s['img']])}'>"
    wm_cls=s.get('wm','none')
    hcls='h1' if i in [1,3,5,8] else 'h2'
    logo_center='center' if s['logo']=='center' else ''
    content_cls='content'
    if layout in ['cover','photo_card']: content_cls='content low'
    if layout in ['continuation','side_photo']: content_cls='content mid'
    card_open = "<div class='card'>" if layout in ['cover','cta'] else ''
    card_close = "</div>" if card_open else ''
    diagram = ""
    if layout=='diagram':
        diagram = "<div class='diagram-list'><div class='diagram-item'>1. Chega com intenção</div><div class='diagram-item'>2. Abre o corpo</div><div class='diagram-item'>3. Respira antes de mover</div></div>"
    html=f"""<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>
<section class='slide {theme} {layout}'>
{bg}<div class='overlay'></div><img class='wm {wm_cls}' src='{uri(wm_file)}'><div class='halftone {hcls}'></div>
<img class='logo {logo_center}' src='{uri(logo)}'>
<div class='{content_cls}'>{card_open}<div class='badge'>{s['badge']}</div><h1 class='title'>{s['title']}<span class='outline'>{s['outline']}</span></h1><div class='bodycopy'>{s['body']}</div>{diagram}<div class='kicker'>{s['kicker']}</div>{card_close}</div>
<div class='chev'>&gt;&gt;&gt;&gt;</div><div class='bars'></div><div class='footer'>@lamusicschool</div><div class='num'>{i:02d}/08</div>
</section></body></html>"""
    (html_dir/f'la-school-stage-posture-v3-{i:02d}.html').write_text(html)

for i in range(1,9):
    html=html_dir/f'la-school-stage-posture-v3-{i:02d}.html'; png=png_dir/f'la-school-stage-posture-v3-{i:02d}.png'
    subprocess.run(['/usr/local/bin/chromium','--headless=new','--no-sandbox','--disable-gpu','--hide-scrollbars','--window-size=1080,1440',f'--screenshot={png}',html.resolve().as_uri()],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

preview=Image.new('RGB',(1080,720),'#111')
for idx in range(8):
    im=Image.open(png_dir/f'la-school-stage-posture-v3-{idx+1:02d}.png').convert('RGB'); im.thumbnail((270,360),Image.LANCZOS)
    preview.paste(im,((idx%4)*270,(idx//4)*360))
preview.save(out/'preview-grid.jpg',quality=92)

(out/'QA.md').write_text('''# QA — Stage Posture Singer V3

- Skill carregada.
- Capa começa com foto forte/hero, não template.
- Fotos usadas conforme direção: capa hero, continuidade visual no card 2, close de microfone, lateral palco, CTA com fundo fotográfico sutil.
- Símbolo LA varia por card e não fica preso ao mesmo lado/tamanho.
- Elementos School: Prompt, pink #E91451, dark, light #E8E8E8, halftone, footer pill, chevrons, logo oficial.
- Sem LA digitado como watermark.
- QA: avaliar preview grid antes de enviar.
''')
package=out.parent/'la-school-stage-posture-singer-test-v3-carousel.tar.gz'
if package.exists(): package.unlink()
with tarfile.open(package,'w:gz') as tar: tar.add(out,arcname=out.name)
print(out); print(package)
