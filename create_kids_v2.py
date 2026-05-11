from pathlib import Path
import re, shutil, textwrap
root=Path('/root/.openclaw/workspace')
out=root/'outputs/la-kids-aula-em-turma-v2'
(out/'png').mkdir(parents=True, exist_ok=True)
(out/'assets').mkdir(exist_ok=True)
repo=root/'repos/la-hq-agents'
ds=(repo/'shared/design-systems/la-music-kids-design-system.html').read_text(errors='ignore')
font_css='\n'.join(re.findall(r"@font-face\s*\{.*?\}\s*", ds, flags=re.S))
logo_src=repo/'shared/design-systems/la-music-kids-v2/assets/logos/logo-la-music-kids-light-completa.svg'
logo=(out/'assets/logo-la-music-kids-light-completa.svg'); shutil.copy2(logo_src, logo)
imgs=[]
for i,p in enumerate([Path('/root/.openclaw/media/tool-image-generation/image-1---4a743e4b-da79-4ed3-994c-20f9e9b6d248.png'),Path('/root/.openclaw/media/tool-image-generation/image-2---dde8d386-001c-409f-b544-129e561e9504.png')],1):
    dest=out/f'assets/kids-photo-{i}.png'; shutil.copy2(p,dest); imgs.append(dest.name)
slides=[
('01','AULA EM TURMA','não divide atenção','Ela multiplica conexão, escuta e vontade de tocar junto.','photo','image1'),
('02','APRENDER JUNTO','dá mais coragem','Uma criança inspira a outra. O grupo vira combustível pra tentar de novo.','blue','icon'),
('03','MÉTODO É O QUE','faz funcionar','Não é juntar crianças. É conduzir com propósito, nível, vínculo e acompanhamento.','red','image2'),
('04','DIFERENÇAS','também ensinam','Quem sabe mais vira referência. Quem está começando ganha um caminho pra seguir.','yellow','icon'),
('05','MENOS TELA','mais presença','A música cria pertencimento, amizade e uma experiência real de convivência.','green','image1'),
('06','MÚSICA NÃO É','só pra gente grande','Agende uma aula experimental na LA Music Kids.','cta','none'),
]
css=f"""
{font_css}
:root{{--amarelo:#FFF212;--verde:#17B255;--azul:#00AFEF;--vermelho:#ED3237;--preto:#1A1A1A;--creme:#FFFEF5;--laranja:#ff8900;}}
*{{box-sizing:border-box}} body{{margin:0;background:#eee;font-family:'Volkswagen',system-ui,sans-serif}} .deck{{display:flex;flex-wrap:wrap;gap:30px;padding:30px}}
.slide{{width:1080px;height:1350px;position:relative;overflow:hidden;padding:54px 64px;background:linear-gradient(145deg,var(--amarelo),var(--laranja));color:white}}
.slide:before{{content:'';position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.42) 2px, transparent 2px);background-size:28px 28px;opacity:.35;z-index:0}}
.logo{{position:absolute;top:42px;left:52px;width:220px;z-index:8}} .handle{{position:absolute;top:54px;right:52px;z-index:8;background:var(--vermelho);color:var(--amarelo);font-weight:800;font-size:25px;padding:12px 22px;border-radius:42px 22px 38px 24px;box-shadow:0 9px 0 rgba(0,0,0,.15)}}
.num{{position:absolute;right:70px;bottom:45px;color:white;font-size:30px;font-weight:800;z-index:9;text-shadow:0 3px 0 rgba(0,0,0,.15)}}
.blob{{position:absolute;border-radius:48% 52% 63% 37%/52% 42% 58% 48%;z-index:1;box-shadow:0 14px 0 rgba(0,0,0,.08)}}
.b1{{background:var(--azul);width:430px;height:390px;right:-150px;top:170px;transform:rotate(18deg)}} .b2{{background:var(--verde);width:330px;height:310px;left:-130px;bottom:180px;transform:rotate(-16deg)}} .b3{{background:var(--vermelho);width:260px;height:260px;right:70px;bottom:-95px}} .b4{{background:white;width:170px;height:160px;left:150px;top:210px;opacity:.95}}
.main{{position:absolute;left:64px;right:64px;top:310px;z-index:5}} .kicker{{display:inline-block;background:var(--vermelho);color:white;font-weight:800;font-size:34px;letter-spacing:1px;padding:10px 22px;border-radius:14px;transform:rotate(-2deg);box-shadow:0 8px 0 rgba(0,0,0,.13);margin-bottom:22px}}
h1{{font-size:112px;line-height:.86;margin:0;text-transform:uppercase;font-weight:800;letter-spacing:-5px;text-shadow:0 8px 0 rgba(0,0,0,.13);max-width:760px}} h1 .script{{display:block;font-family:'Madelina',cursive;text-transform:none;font-weight:400;font-size:108px;line-height:.82;letter-spacing:0;color:var(--azul);text-shadow:0 5px 0 rgba(255,255,255,.35)}}
.desc{{font-size:38px;line-height:1.1;font-weight:700;max-width:620px;color:#fff;margin-top:24px;text-shadow:0 3px 0 rgba(0,0,0,.14)}}
.photo{{position:absolute;right:-30px;bottom:120px;width:520px;height:620px;z-index:4;border-radius:70px 40px 80px 45px;overflow:hidden;box-shadow:0 25px 0 rgba(0,0,0,.16);transform:rotate(2deg);background:white}} .photo img{{width:100%;height:100%;object-fit:cover;object-position:center}}
.iconbig{{position:absolute;right:85px;bottom:185px;z-index:4;width:360px;height:360px;border-radius:54px;background:white;color:var(--azul);display:flex;align-items:center;justify-content:center;font-size:170px;box-shadow:0 25px 0 rgba(0,0,0,.14);transform:rotate(-5deg)}}
.ctaBox{{position:absolute;left:64px;right:64px;bottom:150px;z-index:6;background:var(--azul);border:6px solid white;border-radius:999px;padding:28px 34px;text-align:center;color:white;font-size:38px;font-weight:800;box-shadow:0 14px 0 rgba(0,0,0,.14)}}
.footer{{position:absolute;left:0;right:0;bottom:0;height:24px;display:grid;grid-template-columns:repeat(4,1fr);z-index:10}} .footer span:nth-child(1){{background:var(--amarelo)}}.footer span:nth-child(2){{background:var(--verde)}}.footer span:nth-child(3){{background:var(--azul)}}.footer span:nth-child(4){{background:var(--vermelho)}}
.slide.blue{{background:linear-gradient(145deg,#00AFEF,#008bd0)}} .slide.blue h1 .script{{color:var(--amarelo)}} .slide.blue .kicker{{background:var(--amarelo);color:var(--preto)}}
.slide.red{{background:linear-gradient(145deg,#ED3237,#ff8800)}} .slide.red h1 .script{{color:var(--amarelo)}}
.slide.yellow{{background:linear-gradient(145deg,#FFF212,#ff9c00)}} .slide.yellow h1,.slide.yellow .desc{{color:var(--preto);text-shadow:none}} .slide.yellow h1 .script{{color:var(--vermelho)}}
.slide.green{{background:linear-gradient(145deg,#17B255,#00AFEF)}} .slide.green h1 .script{{color:var(--amarelo)}}
.slide.cta{{background:linear-gradient(145deg,#FFF212 0%,#ff8900 52%,#ED3237 100%)}} .slide.cta .main{{top:285px;text-align:center}} .slide.cta h1{{margin:auto;max-width:900px}} .slide.cta h1 .script{{color:var(--azul)}} .slide.cta .desc{{margin:32px auto 0;max-width:760px;font-size:44px}} .slide.cta .logo{{width:260px}}
"""
def card(num,title,script,desc,theme,kind):
    media=''
    if kind=='image1': media=f"<div class='photo'><img src='assets/{imgs[0]}'></div>"
    if kind=='image2': media=f"<div class='photo'><img src='assets/{imgs[1]}'></div>"
    if kind=='icon': media="<div class='iconbig'>🎵</div>"
    cta="<div class='ctaBox'>CHAMA NO ZAP E AGENDE UMA AULA</div>" if theme=='cta' else ''
    return f"""<section class='slide {theme}' id='slide-{num}'>
    <div class='blob b1'></div><div class='blob b2'></div><div class='blob b3'></div><div class='blob b4'></div>
    <img class='logo' src='assets/{logo.name}'><div class='handle'>@lamusickids</div>
    <div class='main'><div class='kicker'>{num}/06</div><h1>{title}<span class='script'>{script}</span></h1><div class='desc'>{desc}</div></div>
    {media}{cta}<div class='num'>{num}/06</div><div class='footer'><span></span><span></span><span></span><span></span></div>
    </section>"""
html="<!doctype html><html><head><meta charset='utf-8'><style>"+css+"</style></head><body><div class='deck'>"+''.join(card(*s) for s in slides)+"</div></body></html>"
(out/'carousel.html').write_text(html)
(out/'LAHQ_PIPELINE.md').write_text(textwrap.dedent('''
# LAHQ Pipeline — LA Music Kids V2 / Aulas em turma

## Fonte NotebookLM consultada
Notebook: `Treinamento e Estratégias para Aula em Turma` (`b4481df5-57c0-4f45-93cf-44cf523032cb`).
Fontes usadas: `A Revolução Silenciosa das Aulas em Grupo.pdf` e `Conversa sobre treinamento para diretores Escola de Música.pdf`.

## Direção
Carrossel para pais/responsáveis. Tese: aula em turma não divide atenção; cria conexão, escuta, coragem, pertencimento e desenvolvimento socioemocional com método.

## DS usado
LA Music Kids v2: Volkswagen + Madelina, paleta catavento, logo oficial, @lamusickids, fundo quente, blobs, pontilhado e CTA inferior.
'''))
print(out)
