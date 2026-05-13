from pathlib import Path
import shutil, subprocess, textwrap
OUT = Path('/root/.openclaw/workspace/outputs/la-school-stage-attitude-singers')
AS = OUT/'assets'
PNG = OUT/'png'
for d in [AS, PNG]: d.mkdir(parents=True, exist_ok=True)
REPO = Path('/root/.openclaw/workspace/repos/la-hq-agents')
# Official assets
assets = {
 'logo-dark.svg': REPO/'shared/brand-assets/logos/school/logo-la-music-dark-completa.svg',
 'logo-light.svg': REPO/'shared/brand-assets/logos/school/logo-la-music-light-completa.svg',
 'la-dark-solo-vazada.svg': REPO/'shared/brand-assets/logos/school/logo-la-music-dark-solo-vazada.svg',
 'la-light-solo-vazada.svg': REPO/'shared/brand-assets/logos/school/logo-la-music-light-solo-vazada.svg',
 'font-black.ttf': REPO/'shared/brand-assets/fonts/school/Prompt-Black.ttf',
 'font-bold.ttf': REPO/'shared/brand-assets/fonts/school/Prompt-Bold.ttf',
 'font-regular.ttf': REPO/'shared/brand-assets/fonts/school/Prompt-Regular.ttf',
 'photo-hero.png': Path('/root/.openclaw/media/tool-image-generation/la-school-vocalist-confident-posture---7f2034de-17b3-47c2-bf6d-16ce2d997093.png'),
 'photo-mic.png': Path('/root/.openclaw/media/tool-image-generation/la-school-mic-close-stage---b115b4d9-46ca-4c19-8496-90502f06c9f3.png'),
 'photo-rehearsal.png': Path('/root/.openclaw/media/tool-image-generation/la-school-singer-rehearsal-stage-movement---89540544-8d22-471c-bb7d-f20669668f30.png'),
 'photo-singer-ds.jpg': OUT/'assets/06-cantora.jpg',
}
# Ensure DS extracted photo exists; if not copy from prior extraction location already there.
for name, src in assets.items():
    if src.exists():
        shutil.copy2(src, AS/name)
    else:
        print('missing', name, src)

CSS = r'''
@font-face{font-family:Prompt;src:url('assets/font-black.ttf') format('truetype');font-weight:900}
@font-face{font-family:Prompt;src:url('assets/font-bold.ttf') format('truetype');font-weight:700}
@font-face{font-family:Prompt;src:url('assets/font-regular.ttf') format('truetype');font-weight:400}
:root{--pink:#E91451;--shade:#B01545;--deep:#740A28;--light:#F06292;--dark:#373435;--black:#0A0A0A;--soft:#141414;--gray:#E8E8E8;--white:#fff}
*{box-sizing:border-box} body{margin:0;background:#111;font-family:Prompt,Arial,sans-serif}.slide{width:1080px;height:1440px;position:relative;overflow:hidden;background:#0A0A0A;color:#fff}.slide.light{background:#E8E8E8;color:#0A0A0A}.slide.pink{background:linear-gradient(135deg,#E91451 0%,#740A28 100%)}
.logo{position:absolute;top:56px;left:0;right:0;display:flex;justify-content:center;z-index:20}.logo img{height:82px;max-width:360px;object-fit:contain}.logo.lightlogo img{height:82px}.photo{position:absolute;inset:0;z-index:1}.photo img{width:100%;height:100%;object-fit:cover;filter:contrast(1.08) saturate(1.12)}.photo.mic img{object-position:52% center}.photo.hero img{object-position:center top}.photo.rehearsal img{object-position:center center}.overlay{position:absolute;inset:0;z-index:2;background:radial-gradient(ellipse at 55% 35%,rgba(233,20,81,.05) 0%,rgba(10,10,10,.42) 42%,rgba(10,10,10,.95) 100%)}.overlay.pinkwash{background:radial-gradient(ellipse at 62% 33%,rgba(233,20,81,.08) 0%,rgba(116,10,40,.58) 62%,rgba(10,10,10,.96) 100%)}.overlay.deep{background:linear-gradient(180deg,rgba(0,0,0,.55),rgba(0,0,0,.2) 36%,rgba(0,0,0,.94) 88%)}
.halftone{position:absolute;inset:0;z-index:3;pointer-events:none;background-image:radial-gradient(circle,var(--pink) 2.15px,transparent 3.2px);background-size:18px 18px;opacity:.56;mask-image:radial-gradient(ellipse at top right,black 0%,transparent 58%);-webkit-mask-image:radial-gradient(ellipse at top right,black 0%,transparent 58%)}.halftone.left{mask-image:linear-gradient(to right,black 0%,transparent 45%);-webkit-mask-image:linear-gradient(to right,black 0%,transparent 45%)}.halftone.all{background-image:radial-gradient(circle,var(--deep) 2.1px,transparent 3.2px);opacity:.7;mask-image:radial-gradient(ellipse at center,transparent 22%,black 95%);-webkit-mask-image:radial-gradient(ellipse at center,transparent 22%,black 95%)}.halftone.lightdots{background-image:radial-gradient(circle,var(--pink) 1.9px,transparent 3px);opacity:.25;mask-image:linear-gradient(to bottom,black 0%,transparent 70%);-webkit-mask-image:linear-gradient(to bottom,black 0%,transparent 70%)}.photoDots{position:absolute;inset:0;z-index:5;pointer-events:none;background-image:radial-gradient(circle,var(--pink) 2.4px,transparent 3.5px);background-size:20px 20px;opacity:.62;mix-blend-mode:screen}.photoDots.left{mask-image:linear-gradient(to right,black 0%,black 18%,transparent 48%);-webkit-mask-image:linear-gradient(to right,black 0%,black 18%,transparent 48%)}.photoDots.topLeft{mask-image:radial-gradient(ellipse at top left,black 0%,black 24%,transparent 57%);-webkit-mask-image:radial-gradient(ellipse at top left,black 0%,black 24%,transparent 57%)}.photoDots.rightEdge{mask-image:linear-gradient(to left,black 0%,black 15%,transparent 45%);-webkit-mask-image:linear-gradient(to left,black 0%,black 15%,transparent 45%)}
.wm{position:absolute;z-index:4;opacity:.34;pointer-events:none}.wm img{width:100%;height:100%;object-fit:contain}.wm.a{width:740px;height:740px;right:-250px;top:120px;transform:rotate(-8deg)}.wm.b{width:800px;height:800px;left:-250px;bottom:30px;transform:rotate(8deg);opacity:.20}.wm.c{width:690px;height:690px;right:-180px;bottom:160px;opacity:.23}.wm.d{width:840px;height:840px;left:-270px;top:250px;opacity:.18}.wm.lightwm{opacity:.12;filter:brightness(.2)}
.num{position:absolute;z-index:6;font-weight:900;font-size:230px;line-height:.8;color:transparent;-webkit-text-stroke:4px var(--pink);opacity:.72;letter-spacing:-16px}.num.n1{right:38px;top:170px}.num.n2{left:54px;top:160px}.num.n3{right:56px;bottom:215px}.num.n4{left:50px;bottom:240px}
.content{position:absolute;z-index:10;left:66px;right:66px}.mid{top:245px}.lower{bottom:228px}.center{top:250px;bottom:190px;display:flex;flex-direction:column;justify-content:center}.kicker{display:inline-flex;align-items:center;gap:14px;font-size:25px;font-weight:900;letter-spacing:3px;text-transform:uppercase;color:var(--pink);margin-bottom:22px}.kicker:before{content:'';display:block;width:54px;height:6px;background:var(--pink);transform:skewX(-25deg)}.light .kicker{color:#B01545}.light .kicker:before{background:#B01545}
h1,h2{margin:0;font-weight:900;text-transform:uppercase;letter-spacing:-5px}h1{font-size:128px;line-height:.84}h2{font-size:102px;line-height:.86}.smalltitle{font-size:82px}.huge{font-size:160px;line-height:.78;letter-spacing:-8px}.pinkword{color:var(--pink)}.outline{color:transparent;-webkit-text-stroke:3.4px #fff}.light .outline{color:transparent;-webkit-text-stroke:3.4px #0A0A0A}.outline.pinkstroke{-webkit-text-stroke-color:var(--pink)}.natural{text-transform:none;letter-spacing:-4px}.bodycopy{max-width:760px;margin-top:28px;font-size:39px;line-height:1.14;font-weight:700;color:#fff}.light .bodycopy{color:#1a1a1a}.bodycopy .thin{font-weight:400}.micro{font-size:30px;line-height:1.22;font-weight:700;max-width:640px;color:#ddd}.light .micro{color:#333}
.pinkbox{display:inline-block;background:var(--pink);border-radius:22px;padding:25px 33px 30px;box-shadow:12px 13px 0 rgba(0,0,0,.84);transform:rotate(-2.5deg);margin-top:24px}.pinkbox h2{font-size:86px;line-height:.86}.pinkbox .outline{-webkit-text-stroke-color:#fff}.slab{display:inline-block;background:#fff;color:#111;border-radius:999px;padding:11px 24px;font-size:25px;font-weight:900;text-transform:uppercase;letter-spacing:1px;margin-top:24px}.light .slab{background:#111;color:#fff}.call{position:absolute;z-index:10;right:68px;top:245px;width:390px;background:rgba(10,10,10,.86);padding:30px;border-radius:26px;box-shadow:12px 12px 0 rgba(233,20,81,.42);border:3px solid rgba(233,20,81,.9);transform:rotate(1.2deg)}.call b{font-size:48px;line-height:.9;text-transform:uppercase}.call p{font-size:24px;line-height:1.14;margin:14px 0 0;font-weight:700}
.footer{position:absolute;bottom:48px;left:0;right:0;display:flex;flex-direction:column;align-items:center;z-index:25}.pill{display:inline-flex;align-items:center;gap:13px;background:var(--pink);color:#fff;padding:14px 31px;border-radius:999px;font-weight:900;font-size:19px;text-transform:uppercase;letter-spacing:1.4px;box-shadow:6px 7px 0 rgba(0,0,0,.75)}.pill.dark{background:#111;color:#fff}.ig{width:23px;height:23px;border:2px solid #fff;border-radius:6px;position:relative}.ig:after{content:'';position:absolute;top:50%;left:50%;width:8px;height:8px;border:2px solid #fff;border-radius:50%;transform:translate(-50%,-50%)}.stripes{display:flex;gap:8px;margin-top:14px}.stripes i{display:block;width:36px;height:7px;background:#fff;transform:skewX(-25deg)}.light .stripes i{background:#111}.chev{position:absolute;z-index:12;bottom:132px;left:62px;color:var(--pink);font-size:58px;font-weight:900;letter-spacing:-7px}.chev.right{left:auto;right:70px}.pluses{position:absolute;z-index:8;right:62px;bottom:138px;display:grid;grid-template-columns:repeat(3,1fr);gap:9px 16px;color:var(--deep);font-size:39px;font-weight:900}.light .pluses{color:rgba(233,20,81,.45)}.splitword span{display:block}.breakgrid{display:grid;grid-template-columns:.86fr 1fr;gap:36px;align-items:center;margin-top:34px}.tip{background:#111;color:#fff;padding:28px;border-radius:24px;border:2px solid rgba(233,20,81,.28);box-shadow:10px 10px 0 rgba(233,20,81,.2)}.tip b{font-size:35px;text-transform:uppercase}.tip p{font-size:28px;line-height:1.14;margin:12px 0 0}.quote{font-size:52px;line-height:.96;font-weight:900;text-transform:uppercase;letter-spacing:-2px;color:#111}.quote .pinkword{color:var(--pink)}
'''
slides = [
("01", """
<div class='photo hero'><img src='assets/photo-hero.png'></div><div class='overlay pinkwash'></div><div class='halftone left'></div><div class='photoDots topLeft'></div><div class='pluses'><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span></div><div class='logo'><img src='assets/logo-dark.svg'></div><div class='content lower'><div class='kicker'>cantores</div><h1>ATITUDE<br><span class='outline'>DE PALCO</span></h1><div class='bodycopy'>A voz começa antes da primeira nota.</div></div><div class='chev'>» » »</div>"""),
("02", """
<div class='photo rehearsal'><img src='assets/photo-rehearsal.png'></div><div class='overlay deep'></div><div class='halftone'></div><div class='photoDots rightEdge'></div><div class='pluses' style='opacity:.75;right:70px;top:260px;bottom:auto'><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span></div><div class='logo'><img src='assets/logo-dark.svg'></div><div class='content mid'><div class='kicker'>01 · postura</div><h2>o corpo<br><span class='pinkword'>canta</span><br><span class='outline'>primeiro</span></h2><div class='bodycopy'>Peito aberto. Pés firmes. Respiração presente. O palco lê seu corpo antes da voz sair.</div></div><div class='pluses'><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span></div>"""),
("03", """light|
<div class='halftone lightdots'></div><div class='wm b lightwm'><img src='assets/la-light-solo-vazada.svg'></div><div class='logo lightlogo'><img src='assets/logo-light.svg'></div><div class='content center'><div class='kicker'>02 · olhar</div><h2 class='huge splitword'><span>NÃO</span><span>CANTE</span><span class='outline pinkstroke'>PRO</span><span>CHÃO</span></h2><div class='breakgrid'><div class='quote'>Olhar também é <span class='pinkword'>presença.</span></div><div class='tip'><b>Treino real</b><p>Escolha esquerda, centro e direita. Cante para pessoas, não para o medo.</p></div></div></div><div class='chev right'>» » »</div>"""),
("04", """
<div class='photo mic'><img src='assets/photo-mic.png'></div><div class='overlay'></div><div class='halftone left'></div><div class='photoDots left'></div><div class='pluses' style='opacity:.45;right:68px;top:245px;bottom:auto'><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span></div><div class='logo'><img src='assets/logo-dark.svg'></div><div class='content lower'><div class='kicker'>03 · microfone</div><h2>domine<br><span class='outline'>a distância</span></h2><div class='pinkbox'><h2>não<br><span class='outline'>engula</span><br>a voz</h2></div></div>"""),
("05", """light|
<div class='halftone lightdots'></div><div class='wm a lightwm'><img src='assets/la-light-solo-vazada.svg'></div><div class='logo lightlogo'><img src='assets/logo-light.svg'></div><div class='num n1'>04</div><div class='content center'><div class='kicker'>04 · silêncio</div><h2 class='huge'>respira.<br><span class='outline pinkstroke'>segura.</span><br>entra.</h2><div class='bodycopy'>Pausa não é vazio. É controle. Quem domina o silêncio domina a entrada.</div></div><div class='pluses'><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span></div>"""),
("06", """
<div class='photo'><img src='assets/photo-singer-ds.jpg'></div><div class='overlay pinkwash'></div><div class='halftone'></div><div class='photoDots left' style='opacity:.36'></div><div class='logo'><img src='assets/logo-dark.svg'></div><div class='call'><b>cada passo precisa ter motivo</b><p>Sem intenção, movimento vira distração. Com intenção, vira presença.</p></div><div class='content lower'><div class='kicker'>05 · movimento</div><h2 class='huge'>ocupe<br><span class='outline'>o palco</span></h2></div><div class='chev'>» » »</div>"""),
("07", """
<div class='wm b'><img src='assets/la-dark-solo-vazada.svg'></div><div class='halftone all'></div><div class='logo'><img src='assets/logo-dark.svg'></div><div class='num n2'>06</div><div class='content center'><div class='kicker'>06 · coragem</div><h2 class='huge'>ERROU?<br><span class='pinkword'>SEGUE</span><br><span class='outline'>NO SHOW</span></h2><div class='bodycopy'>Atitude não é parecer perfeito. É continuar presente quando algo sai do roteiro.</div></div><div class='chev right'>» » »</div>"""),
("08", """pink|
<div class='halftone all'></div><div class='wm a'><img src='assets/la-dark-solo-vazada.svg'></div><div class='logo'><img src='assets/logo-dark.svg'></div><div class='content center'><div class='kicker' style='color:#fff'>aula experimental</div><h2 class='huge'>sua voz<br><span class='outline'>merece</span><br>palco.</h2><div class='bodycopy'>Vem cantar com presença, técnica e coragem. Sobe no palco com a LA.</div><div class='slab'>chama no direct</div></div><div class='chev'>» » »</div>"""),
]
htmls=[]
for code, body in slides:
    cls='slide'
    if body.startswith('light|'):
        cls+=' light'; body=body[6:]
    elif body.startswith('pink|'):
        cls+=' pink'; body=body[5:]
    body += "<div class='footer'><div class='pill'><span class='ig'></span>@lamusicschool</div><div class='stripes'><i></i><i></i><i></i><i></i></div></div>"
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><section class='{cls}'>{body}</section></body></html>"
    p=OUT/f'slide-{code}.html'; p.write_text(html); htmls.append((code,p))

chromium='/usr/local/bin/chromium'
for code,p in htmls:
    png=PNG/f'la-school-stage-attitude-{code}.png'
    subprocess.run([chromium,'--headless','--no-sandbox','--disable-gpu','--window-size=1080,1440',f'--screenshot={png}',p.as_uri()], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# preview grid 4x2
from PIL import Image, ImageOps, ImageDraw
imgs=[]
for code,p in htmls:
    im=Image.open(PNG/f'la-school-stage-attitude-{code}.png').convert('RGB')
    im=ImageOps.fit(im,(270,360))
    imgs.append(im)
canvas=Image.new('RGB',(4*270,2*360),(17,17,17))
for i,im in enumerate(imgs): canvas.paste(im,((i%4)*270,(i//4)*360))
canvas.save(OUT/'preview-grid.jpg',quality=92)
# pipeline doc
(OUT/'LAHQ_PIPELINE.md').write_text('''# LAHQ Pipeline — Atitude de Palco para Cantores\n\nMarca: LA Music School\nFormato: 8 lâminas 1080x1440\nSkill usada: lahq-school-content\n\n## Nina / Direção\nTema: atitude de palco para cantores. Narrativa: presença começa antes da voz; postura, olhar, microfone, silêncio, movimento, coragem e CTA.\n\n## Theo / Copy\nTítulos curtos, aspiracionais e técnicos: corpo canta primeiro, não cante pro chão, domine a distância, respira/segura/entra, ocupe o palco, errou segue no show, sua voz merece palco.\n\n## Luna / Imagens\nFotos geradas/selecionadas sem texto/logos/watermark: cantor no palco, close de microfone, ensaio de movimento e referência DS cantora.\n\n## Diego / Montagem\nDS v2 School: Prompt, logo oficial topo centralizado em todos os cards, pink #E91451, dark, gray light, halftone, LA oficial como composição, sólido+outline, chevrons, padrão +, footer pill + listras.\n\n## Tina + Nina QA\nChecar preview grid: variação real entre cards, card pink não virou muleta, tipografia com direção de arte, logo topo em todos, texto legível, cara de campanha.\n''')
subprocess.run(['tar','-czf',str(OUT.with_suffix('.tar.gz')),'-C',str(OUT.parent),OUT.name], check=True)
print(OUT)
print(OUT/'preview-grid.jpg')
print(OUT.with_suffix('.tar.gz'))
