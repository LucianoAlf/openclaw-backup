from pathlib import Path
import shutil, textwrap
root=Path('/root/.openclaw/workspace')
repo=root/'repos/la-hq-agents'
out=root/'outputs/la-kids-aulas-em-turma-v4-LAHQ'
(out/'png').mkdir(parents=True, exist_ok=True)
assets=out/'assets'; assets.mkdir(exist_ok=True)
for name in ['Volkswagen-Heavy.otf','Volkswagen-Bold.otf','Volkswagen-Regular.otf','Madelina.otf']:
    shutil.copy2(repo/f'shared/design-systems/la-music-kids-v2/assets/fonts/{name}', assets/name)
shutil.copy2(repo/'shared/design-systems/la-music-kids-v2/assets/logos/logo-la-music-kids-light-completa.svg', assets/'logo-kids.svg')
shutil.copy2('/root/.openclaw/media/tool-image-generation/image-1---7953cb0e-93bf-4e56-af33-110ed0de6246.png', assets/'turma-kids.png')
slides=[
('01','AULA EM TURMA','seu filho aprende junto','Na música, convivência também vira aprendizado.','hero'),
('02','TOCAR JUNTO','dá coragem','Quando uma criança vê a outra tentando, ela tenta também.','photo-left'),
('03','NÃO É SÓ','juntar crianças','Tem método, escuta e condução pra cada um evoluir no seu tempo.','solid-red'),
('04','O GRUPO','cria ritmo','A turma ajuda a criança a ouvir, esperar, entrar e participar.','photo-right'),
('05','MENOS TELA','mais presença','Música em grupo cria vínculo real: olho no olho, som e amizade.','solid-blue'),
('06','MÚSICA','não é só pra gente grande','Agende uma aula experimental na LA Music Kids.','cta')]
css="""
@font-face{font-family:Volkswagen;src:url('assets/Volkswagen-Regular.otf')}@font-face{font-family:Volkswagen;src:url('assets/Volkswagen-Bold.otf');font-weight:700}@font-face{font-family:Volkswagen;src:url('assets/Volkswagen-Heavy.otf');font-weight:900}@font-face{font-family:Madelina;src:url('assets/Madelina.otf')}
:root{--yellow:#FFF212;--green:#17B255;--blue:#00AFEF;--red:#ED3237;--black:#1A1A1A;--orange:#ff8d00;--cream:#FFFEF5}*{box-sizing:border-box}body{margin:0;background:#eee;font-family:Volkswagen,Arial,sans-serif}.deck{display:flex;flex-wrap:wrap;gap:30px;padding:30px}.slide{width:1080px;height:1350px;position:relative;overflow:hidden;background:linear-gradient(145deg,var(--yellow),var(--orange));color:white}.slide:before{content:'';position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.55) 2px,transparent 2px);background-size:30px 30px;opacity:.32;z-index:0}.logo{position:absolute;top:38px;left:52px;width:250px;z-index:30}.handle{position:absolute;top:58px;right:52px;background:var(--red);color:var(--yellow);font-size:32px;font-weight:900;padding:15px 30px;border-radius:45px 25px 42px 24px;z-index:30;box-shadow:0 10px 0 rgba(0,0,0,.16)}.num{position:absolute;right:60px;bottom:42px;z-index:30;color:white;font-size:30px;font-weight:900}.blob{position:absolute;z-index:1;border-radius:50% 50% 37% 63%/55% 37% 63% 45%;box-shadow:0 15px 0 rgba(0,0,0,.1)}.b1{right:-140px;top:155px;width:390px;height:360px;background:var(--blue);transform:rotate(14deg)}.b2{left:-150px;bottom:170px;width:400px;height:350px;background:var(--green);transform:rotate(-18deg)}.b3{right:75px;bottom:-100px;width:280px;height:260px;background:var(--red);transform:rotate(8deg)}.b4{left:250px;top:185px;width:160px;height:140px;background:white;opacity:.55}.strip{position:absolute;left:0;right:0;bottom:0;height:24px;z-index:40;display:grid;grid-template-columns:repeat(4,1fr)}.strip span:nth-child(1){background:var(--yellow)}.strip span:nth-child(2){background:var(--green)}.strip span:nth-child(3){background:var(--blue)}.strip span:nth-child(4){background:var(--red)}
.main{position:absolute;left:62px;right:62px;top:275px;z-index:15}.tag{display:inline-block;background:var(--red);color:white;font-weight:900;font-size:34px;padding:12px 22px;border-radius:15px;box-shadow:0 8px 0 rgba(0,0,0,.16);transform:rotate(-2deg);margin-bottom:20px}h1{margin:0;max-width:650px;font-size:126px;line-height:.78;letter-spacing:-5px;font-weight:900;text-transform:uppercase;text-shadow:0 8px 0 rgba(0,0,0,.16)}.script{font-family:Madelina,cursive;text-transform:none;font-weight:400;display:block;color:white;font-size:88px;line-height:.95;letter-spacing:0;text-shadow:0 6px 0 rgba(0,0,0,.13)}.sub{margin-top:24px;max-width:560px;color:white;font-size:39px;line-height:1.08;font-weight:900;text-shadow:0 4px 0 rgba(0,0,0,.14)}.turma{position:absolute;z-index:8;background:white;overflow:hidden;box-shadow:0 24px 0 rgba(0,0,0,.16)}.turma img{width:100%;height:100%;object-fit:cover}.hero .turma{right:-50px;bottom:105px;width:590px;height:610px;border-radius:95px 42px 100px 52px;transform:rotate(2deg)}.photo-left .turma{left:55px;bottom:125px;width:465px;height:500px;border-radius:82px 35px 90px 44px;transform:rotate(-3deg)}.photo-left .main{left:520px;top:315px}.photo-left h1{max-width:500px;font-size:104px}.photo-left .script{font-size:78px;color:var(--yellow)}.photo-left .sub{max-width:450px}.photo-right .turma{right:45px;bottom:135px;width:470px;height:500px;border-radius:82px 35px 90px 44px;transform:rotate(3deg)}.photo-right h1{max-width:555px;font-size:108px}.photo-right .script{font-size:78px;color:var(--yellow)}.solid-red{background:linear-gradient(145deg,var(--red),#ff8d00)}.solid-red .tag{background:var(--yellow);color:var(--black)}.solid-red .script{color:var(--yellow)}.solid-red .sub{max-width:720px}.solid-red h1{max-width:840px}.solid-blue{background:linear-gradient(145deg,var(--yellow),#ff9c00 48%,var(--red))}.solid-blue h1,.solid-blue .sub{color:var(--black);text-shadow:none}.solid-blue .script{color:var(--blue);text-shadow:0 5px 0 rgba(255,255,255,.5)}.solid-blue .tag{background:var(--blue);color:white}.cta{background:linear-gradient(145deg,var(--yellow),#ff9c00 46%,var(--red))}.cta .main{text-align:center;top:260px}.cta h1{margin:auto;max-width:850px;color:white}.cta .script{color:var(--blue);font-size:82px;text-shadow:0 5px 0 rgba(255,255,255,.45)}.cta .sub{margin:30px auto 0;max-width:750px;font-size:44px}.button{position:absolute;left:84px;right:84px;bottom:150px;background:var(--red);color:white;border:7px solid white;border-radius:999px;padding:26px 30px;text-align:center;font-size:44px;font-weight:900;z-index:25;box-shadow:0 14px 0 rgba(0,0,0,.16)}.cta .turma{right:70px;bottom:330px;width:350px;height:330px;border-radius:70px 34px 75px 38px;opacity:.95;transform:rotate(4deg)}
"""
def slide(i,tag,main,script,sub,kind):
    turma=""
    if kind in ['hero','photo-left','photo-right','cta']:
        turma="<div class='turma'><img src='assets/turma-kids.png'></div>"
    button="<div class='button'>CHAMA NO ZAP E AGENDE</div>" if kind=='cta' else ""
    return f"""<section class='slide {kind}'>
      <div class='blob b1'></div><div class='blob b2'></div><div class='blob b3'></div><div class='blob b4'></div>
      <img class='logo' src='assets/logo-kids.svg'><div class='handle'>@lamusickids</div>
      <div class='main'><div class='tag'>{tag}</div><h1>{main}<span class='script'>{script}</span></h1><div class='sub'>{sub}</div></div>
      {turma}{button}<div class='num'>{i}/06</div><div class='strip'><span></span><span></span><span></span><span></span></div>
    </section>"""
html='<!doctype html><html><head><meta charset="utf-8"><style>'+css+'</style></head><body><div class="deck">'+''.join(slide(str(idx).zfill(2), *s) for idx, s in enumerate(slides, 1))+'</div></body></html>'
(out/'carousel.html').write_text(html)
(out/'LAHQ_PIPELINE.md').write_text(textwrap.dedent('''
# LAHQ Pipeline — LA Music Kids V4 / Aulas em turma

## Erro corrigido
V3 foi reprovada pelo Alf por não mostrar crianças em turma e não parecer as referências. V4 corrige isso usando imagem central de turma musical em slides-chave.

## NotebookLM
Base real: Notebook `Treinamento e Estratégias para Aula em Turma` (`b4481df5-57c0-4f45-93cf-44cf523032cb`).
Tese usada: aula em turma cria conexão, escuta, motivação, pertencimento e evolução com método.

## LAHQ
- Nina: reposicionou a direção para campanha Kids com foto/turma como prova visual.
- Theo: copy curta, emocional e baseada no notebook, falando com pais.
- Luna: gerou asset de crianças em turma musical; QA visual PASS.
- Diego: montou em HTML/CSS com DS Kids novo, fontes/logos oficiais.
- Tina: QA deve reprovar se não parecer campanha LA Music Kids real ou se faltar turma.
'''))
print(out)
