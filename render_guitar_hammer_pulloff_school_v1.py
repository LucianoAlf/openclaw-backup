from pathlib import Path
from PIL import Image
import shutil, subprocess, tarfile

repo=Path('/root/.openclaw/workspace/repos/la-hq-agents')
out=Path('/root/.openclaw/workspace/outputs/la-school-guitar-hammer-pulloff-v1')
html_dir=out/'html'; png_dir=out/'png'; asset_dir=out/'assets'
for d in [html_dir,png_dir,asset_dir]: d.mkdir(parents=True,exist_ok=True)
imgs_src=[
 Path('/root/.openclaw/media/tool-image-generation/la-school-guitarist-hero-hammer-pull---6ffafe4f-8921-49a7-bb07-bc158f25dcf9.png'),
 Path('/root/.openclaw/media/tool-image-generation/la-school-guitar-fretboard-hammer-pulloff-closeup---297f81e2-d927-41c2-b49a-6af3e89805d3.png'),
 Path('/root/.openclaw/media/tool-image-generation/la-school-guitar-stage-detail-hammer-pulloff---612a9f3f-7188-48a9-8214-0abf64163554.png'),
]
imgs=[]
for p in imgs_src:
 dst=asset_dir/p.name; shutil.copy2(p,dst); imgs.append(dst)
logos=repo/'shared/brand-assets/logos/school'; font_dir=repo/'shared/brand-assets/fonts/school'
logo_dark=logos/'logo-la-music-dark-completa.svg'; logo_light=logos/'logo-la-music-light-completa.svg'
wm_dark=logos/'logo-la-music-dark-solo.svg'; wm_dark_vaz=logos/'logo-la-music-dark-solo-vazada.svg'; wm_light_vaz=logos/'logo-la-music-light-solo-vazada.svg'
def uri(p): return Path(p).resolve().as_uri()

slides=[
 dict(theme='dark',layout='cover',img=0,logo='center',wm='none',footer='full',quiet='',badge='GUITARRA',title='HAMMER-ON',outline='& pull-off',body='Ligados limpos deixam sua frase mais rápida, fluida e musical.',kicker='Passe pro lado →'),
 dict(theme='dark',layout='split',img=1,logo='small',wm='none',footer='mini',quiet='',badge='DICA 01',title='NÃO BATE',outline='de qualquer jeito',body='Hammer-on não é força bruta. É precisão: dedo cai firme, perto do traste.',kicker='Som claro sem palhetar'),
 dict(theme='light',layout='editorial',logo='small',wm='topgiant',footer='none',quiet='quiet',badge='DICA 02',title='COMECE',outline='devagar',body='Toque duas notas e escute se a segunda tem volume. Se sumiu, ainda não tá pronto.',kicker='Controle antes de velocidade'),
 dict(theme='dark',layout='photo',img=1,logo='small',wm='none',footer='mini',quiet='',badge='DICA 03',title='PULL-OFF NÃO É',outline='tirar o dedo',body='Puxe levemente a corda para baixo. É quase uma mini-palhetada com a mão esquerda.',kicker='Faz a nota falar'),
 dict(theme='pink',layout='poster',img=2,logo='small',wm='leftcolor',footer='none',quiet='quiet',badge='DICA 04',title='DEIXE',outline='SOAR',body='Não abafe sem querer. O ligado precisa respirar entre uma nota e outra.',kicker='Fluidez vem do sustain'),
 dict(theme='dark',layout='side',img=2,logo='small',wm='none',footer='none',quiet='quiet',badge='DICA 05',title='TREINE EM',outline='frases',body='Não pratique só exercício mecânico. Coloque hammer e pull-off dentro de licks reais.',kicker='Técnica vira música'),
 dict(theme='pink',layout='steps',logo='small',wm='edge',footer='mini',quiet='',badge='DICA 06',title='O ERRO',outline='clássico',body='A mão esquerda corre e a direita não entende. Treine com pulso e metrônomo.',kicker='Limpo primeiro. Rápido depois.'),
 dict(theme='dark',layout='cta',img=0,logo='center',wm='none',footer='full',quiet='',badge='LA MUSIC SCHOOL',title='QUER SOLAR',outline='melhor?',body='Aula de guitarra pra transformar técnica em som de verdade. Pra Quem Sabe o Que Quer.',kicker='Agende sua aula experimental'),
]

css=f'''
@font-face{{font-family:Prompt;src:url('{uri(font_dir/'Prompt-Regular.ttf')}') format('truetype');font-weight:400}}
@font-face{{font-family:Prompt;src:url('{uri(font_dir/'Prompt-Medium.ttf')}') format('truetype');font-weight:500}}
@font-face{{font-family:Prompt;src:url('{uri(font_dir/'Prompt-SemiBold.ttf')}') format('truetype');font-weight:600}}
@font-face{{font-family:Prompt;src:url('{uri(font_dir/'Prompt-Bold.ttf')}') format('truetype');font-weight:700}}
@font-face{{font-family:Prompt;src:url('{uri(font_dir/'Prompt-Black.ttf')}') format('truetype');font-weight:900}}
*{{box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1440px;overflow:hidden;font-family:Prompt,sans-serif}}.slide{{position:relative;width:1080px;height:1440px;overflow:hidden;background:#0A0A0A;color:#fff;isolation:isolate}}.light{{background:#E8E8E8;color:#0A0A0A}}.pink{{background:linear-gradient(145deg,#E91451 0%,#B01545 100%);color:#fff}}
.logo{{position:absolute;top:50px;left:58px;width:285px;max-height:102px;z-index:40;filter:drop-shadow(0 8px 10px rgba(0,0,0,.35))}}.logo.center{{left:50%;transform:translateX(-50%);width:338px}}.logo.hidden{{display:none}}
.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-20;filter:contrast(1.18) saturate(1.08)}}.cover .bg{{opacity:.96}}.split .bg{{height:1350px;width:auto;right:-210px;left:auto;top:80px;opacity:.72;filter:contrast(1.22) saturate(1.18)}}.photo .bg{{opacity:.64}}.poster .bg{{opacity:.14;filter:grayscale(.35) contrast(1.25)}}.side .bg{{height:1200px;width:auto;right:-155px;bottom:0;opacity:.78}}.cta .bg{{opacity:.28;filter:grayscale(.25) contrast(1.22)}}
.overlay{{position:absolute;inset:0;z-index:-19;background:linear-gradient(90deg,rgba(10,10,10,.95) 0%,rgba(10,10,10,.72) 42%,rgba(10,10,10,.18) 100%),radial-gradient(circle at 78% 18%,rgba(233,20,81,.32),transparent 35%)}}.split .overlay{{background:linear-gradient(90deg,rgba(10,10,10,.98) 0%,rgba(10,10,10,.82) 45%,rgba(10,10,10,.18) 100%),linear-gradient(180deg,rgba(233,20,81,.24),rgba(10,10,10,.18))}}.pink .overlay{{background:radial-gradient(circle at 25% 20%,rgba(255,255,255,.17),transparent 36%)}}.light .overlay{{background:radial-gradient(circle at 20% 16%,rgba(233,20,81,.15),transparent 36%)}}
.wm{{position:absolute;object-fit:contain;z-index:-12;pointer-events:none}}.wm.none{{display:none}}.wm.topgiant{{width:1240px;left:-360px;top:-410px;opacity:.145;transform:rotate(-5deg)}}.wm.leftcolor{{width:980px;left:-500px;bottom:10px;opacity:.17;transform:rotate(8deg)}}.wm.edge{{width:850px;right:-430px;bottom:-260px;opacity:.11;transform:rotate(-16deg)}}
.halftone{{position:absolute;width:620px;height:620px;opacity:.38;z-index:-10;background-image:radial-gradient(circle,#E91451 0 5px,transparent 6px);background-size:28px 28px;mask-image:radial-gradient(circle,#000 18%,transparent 72%)}}.hA{{right:-130px;top:110px}}.hB{{left:-190px;bottom:120px;transform:rotate(15deg)}}.pink .halftone{{background-image:radial-gradient(circle,#0A0A0A 0 5px,transparent 6px);opacity:.18}}.light .halftone{{opacity:.26}}
.slab{{position:absolute;background:#E91451;border-radius:34px;box-shadow:20px 20px 0 rgba(0,0,0,.42);z-index:-8;transform:rotate(-3deg)}}.slab.cover{{left:60px;bottom:248px;width:745px;height:440px}}.slab.split{{left:50px;top:388px;width:615px;height:500px;transform:rotate(-4deg);opacity:.98}}.slab.diag{{left:42px;top:340px;width:650px;height:620px;transform:rotate(7deg);opacity:.92}}.slab.dark{{background:#0A0A0A;right:52px;top:330px;width:570px;height:520px;transform:rotate(-4deg)}}
.content{{position:absolute;left:64px;right:64px;top:205px;z-index:25}}.low{{top:640px}}.mid{{top:330px}}.bottom{{top:750px}}
.badge{{display:inline-block;background:#E91451;color:#fff;font-weight:900;font-size:25px;letter-spacing:2.4px;padding:13px 22px;border-radius:14px;box-shadow:10px 10px 0 rgba(0,0,0,.46);margin-bottom:26px}}.pink .badge{{background:#0A0A0A}}
.title{{font-size:112px;font-weight:900;line-height:.86;letter-spacing:-5.5px;text-transform:uppercase;margin:0;max-width:930px}}.cover .title{{font-size:122px}}.poster .title{{font-size:104px}}.outline{{display:block;color:transparent;font-size:94px;font-weight:900;line-height:.88;letter-spacing:-4px;text-transform:uppercase;margin-top:10px;-webkit-text-stroke:3px #fff}}.light .outline{{-webkit-text-stroke-color:#0A0A0A}}
.bodycopy{{margin-top:32px;max-width:800px;font-size:45px;line-height:1.08;font-weight:700}}.light .bodycopy{{color:#222}}.split .bodycopy,.photo .bodycopy{{max-width:620px}}
.kicker{{margin-top:30px;display:inline-block;border:2px solid currentColor;border-radius:999px;padding:18px 32px;font-size:32px;font-weight:900}}
.card{{background:#E91451;color:#fff;border-radius:28px;padding:44px 50px;display:inline-block;max-width:910px;box-shadow:18px 18px 0 rgba(0,0,0,.52)}}.pink .card{{background:#0A0A0A}}
.stepsbox{{display:grid;gap:24px;margin-top:42px;max-width:850px}}.step{{background:#0A0A0A;color:#fff;border-radius:22px;padding:28px 34px;font-size:40px;font-weight:900;box-shadow:12px 12px 0 rgba(233,20,81,.85)}}
.footer{{position:absolute;bottom:94px;left:50%;transform:translateX(-50%);background:#E91451;color:#fff;border-radius:999px;padding:18px 46px;font-size:30px;font-weight:900;z-index:40;box-shadow:0 14px 0 rgba(0,0,0,.38)}}.pink .footer{{background:#0A0A0A}}.footer.mini{{left:auto;right:58px;transform:none;bottom:78px;padding:13px 26px;font-size:22px;box-shadow:0 8px 0 rgba(0,0,0,.34)}}.footer.none{{display:none}}
.bars{{position:absolute;bottom:62px;left:50%;transform:translateX(-50%);width:420px;height:58px;background:repeating-linear-gradient(105deg,transparent 0 16px,rgba(255,255,255,.9) 17px 25px);opacity:.95;z-index:33}}.bars.mini{{display:none}}.bars.none{{display:none}}.light .bars{{background:repeating-linear-gradient(105deg,transparent 0 16px,rgba(10,10,10,.86) 17px 25px)}}
.chev{{position:absolute;bottom:113px;left:54px;color:#E91451;font-size:56px;font-weight:900;letter-spacing:-8px;transform:skewX(-12deg);z-index:35}}.pink .chev{{color:#fff}}.quiet .chev{{display:none}}.num{{position:absolute;right:64px;bottom:86px;font-size:30px;font-weight:900;opacity:.72;z-index:42}}.quiet .num{{opacity:.22;right:52px;bottom:52px}}
'''

for i,s in enumerate(slides,1):
    theme=s['theme']; layout=s['layout']; logo=logo_light if theme=='light' else logo_dark
    wmfile=wm_dark if s['wm']=='leftcolor' else (wm_light_vaz if theme=='light' else wm_dark_vaz)
    bg=f"<img class='bg' src='{uri(imgs[s['img']])}'>" if 'img' in s else ''
    hcls='hA' if i in [1,3,5,8] else 'hB'
    logo_cls='center' if s['logo']=='center' else ('hidden' if s['logo']=='none' else '')
    ccls='content'
    if layout in ['cover','photo']: ccls='content low'
    if layout in ['split','side']: ccls='content mid'
    card_open='<div class="card">' if layout in ['cover','cta'] else ''
    card_close='</div>' if card_open else ''
    slab=''
    if layout=='cover': slab='<div class="slab cover"></div>'
    if layout=='split': slab='<div class="slab split"></div>'
    if layout=='side': slab='<div class="slab diag"></div>'
    if layout=='cta': slab='<div class="slab dark"></div>'
    steps=''
    if layout=='steps': steps='<div class="stepsbox"><div class="step">1. Chega com intenção</div><div class="step">2. Abre o corpo</div><div class="step">3. Respira antes de mover</div></div>'
    footer=s['footer']
    html=f"""<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>
<section class='slide {theme} {layout} {s.get('quiet','')}'>
{bg}<div class='overlay'></div><img class='wm {s['wm']}' src='{uri(wmfile)}'><div class='halftone {hcls}'></div>{slab}
<img class='logo {logo_cls}' src='{uri(logo)}'>
<div class='{ccls}'>{card_open}<div class='badge'>{s['badge']}</div><h1 class='title'>{s['title']}<span class='outline'>{s['outline']}</span></h1><div class='bodycopy'>{s['body']}</div>{steps}<div class='kicker'>{s['kicker']}</div>{card_close}</div>
<div class='chev'>&gt;&gt;&gt;&gt;</div><div class='bars {footer}'></div><div class='footer {footer}'>@lamusicschool</div><div class='num'>{i:02d}/08</div>
</section></body></html>"""
    (html_dir/f'la-school-guitar-hammer-pulloff-{i:02d}.html').write_text(html)

for i in range(1,9):
    html=html_dir/f'la-school-guitar-hammer-pulloff-{i:02d}.html'; png=png_dir/f'la-school-guitar-hammer-pulloff-{i:02d}.png'
    subprocess.run(['/usr/local/bin/chromium','--headless=new','--no-sandbox','--disable-gpu','--hide-scrollbars','--window-size=1080,1440',f'--screenshot={png}',html.resolve().as_uri()],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
preview=Image.new('RGB',(1080,720),'#111')
for idx in range(8):
    im=Image.open(png_dir/f'la-school-guitar-hammer-pulloff-{idx+1:02d}.png').convert('RGB'); im.thumbnail((270,360),Image.LANCZOS)
    preview.paste(im,((idx%4)*270,(idx//4)*360))
preview.save(out/'preview-grid.jpg',quality=92)
(out/'QA.md').write_text('# QA — Stage Posture Singer V4\n\n- Revisão pós-QA: capa hero forte, menos rodapé repetido, menos símbolo LA carimbado, mais variação estrutural.\n')
package=out.parent/'la-school-guitar-hammer-pulloff-v1-carousel.tar.gz'
if package.exists(): package.unlink()
with tarfile.open(package,'w:gz') as tar: tar.add(out,arcname=out.name)
print(out); print(package)
