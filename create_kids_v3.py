from pathlib import Path
import shutil, textwrap, base64
root=Path('/root/.openclaw/workspace')
repo=root/'repos/la-hq-agents'
out=root/'outputs/la-kids-aulas-em-turma-v3-LAHQ'
(out/'png').mkdir(parents=True, exist_ok=True)
assets=out/'assets'; assets.mkdir(exist_ok=True)
# assets
for name in ['Volkswagen-Heavy.otf','Volkswagen-Bold.otf','Volkswagen-Regular.otf','Madelina.otf']:
    shutil.copy2(repo/f'shared/design-systems/la-music-kids-v2/assets/fonts/{name}', assets/name)
logo_src=repo/'shared/design-systems/la-music-kids-v2/assets/logos/logo-la-music-kids-light-completa.svg'
shutil.copy2(logo_src, assets/'logo-kids.svg')
refs=repo/'shared/design-systems/la-music-kids-v2/references/official-correct'
for i in [1,5]: shutil.copy2(refs/f'ref-0{i}.jpg', assets/f'ref-0{i}.jpg')
slides=[
  dict(n='01', theme='photo', tag='AULAS EM TURMA', main='JUNTO', script='também se aprende', sub='A música vira encontro: escuta, ritmo e coragem pra participar.', photo='ref-01.jpg', pos='center center'),
  dict(n='02', theme='yellow', tag='O QUE MUDA?', main='O GRUPO', script='puxa a criança', sub='Um aluno inspira o outro. A turma cria motivação real pra continuar tentando.', icon='🎵'),
  dict(n='03', theme='red', tag='NÃO É BAGUNÇA', main='TEM MÉTODO', script='por trás', sub='Aula em turma funciona quando tem propósito, acompanhamento e condução pedagógica.', icon='🥁'),
  dict(n='04', theme='blue', tag='CADA UM NO SEU TEMPO', main='DIFERENÇAS', script='também ensinam', sub='Quem está mais avançado vira referência. Quem começa agora ganha caminho.', icon='⭐'),
  dict(n='05', theme='photo2', tag='MENOS TELA', main='MAIS', script='presença', sub='A aula em grupo cria vínculo, amizade e uma experiência de convivência real.', photo='ref-05.jpg', pos='center center'),
  dict(n='06', theme='cta', tag='LA MUSIC KIDS', main='MÚSICA', script='não é só pra gente grande', sub='Agende uma aula experimental e descubra a turma ideal pro seu filho.', icon='✨'),
]
css="""
@font-face{font-family:Volkswagen;src:url('assets/Volkswagen-Regular.otf')}@font-face{font-family:Volkswagen;src:url('assets/Volkswagen-Bold.otf');font-weight:700}@font-face{font-family:Volkswagen;src:url('assets/Volkswagen-Heavy.otf');font-weight:900}@font-face{font-family:Madelina;src:url('assets/Madelina.otf')}
:root{--yellow:#FFF212;--green:#17B255;--blue:#00AFEF;--red:#ED3237;--black:#1A1A1A;--orange:#ff8a00;--cream:#FFFEF5}
*{box-sizing:border-box}body{margin:0;background:#eee;font-family:Volkswagen,Arial,sans-serif}.deck{display:flex;flex-wrap:wrap;gap:30px;padding:30px}.slide{width:1080px;height:1350px;position:relative;overflow:hidden;background:linear-gradient(135deg,var(--yellow),var(--orange));color:white}.slide:after{content:'';position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.55) 2px,transparent 2px);background-size:28px 28px;opacity:.28;z-index:0}.logo{position:absolute;top:38px;left:52px;width:245px;z-index:20}.handle{position:absolute;top:58px;right:55px;z-index:20;background:var(--red);color:var(--yellow);font-weight:900;font-size:25px;padding:13px 24px;border-radius:42px 24px 38px 22px;box-shadow:0 9px 0 rgba(0,0,0,.16)}.num{position:absolute;right:62px;bottom:42px;z-index:20;font-size:29px;font-weight:900;color:white}.blob{position:absolute;z-index:1;border-radius:52% 48% 42% 58%/56% 38% 62% 44%;box-shadow:0 16px 0 rgba(0,0,0,.1)}.b1{right:-185px;top:155px;width:470px;height:420px;background:var(--blue);transform:rotate(12deg)}.b2{left:-140px;bottom:190px;width:390px;height:345px;background:var(--green);transform:rotate(-17deg)}.b3{right:80px;bottom:-105px;width:275px;height:260px;background:var(--red);transform:rotate(8deg)}.b4{left:285px;top:170px;width:145px;height:132px;background:white;opacity:.55;transform:rotate(20deg)}
.main{position:absolute;left:62px;right:62px;top:300px;z-index:10}.tag{display:inline-block;background:var(--red);color:white;font-size:32px;font-weight:900;padding:13px 22px;border-radius:14px;box-shadow:0 8px 0 rgba(0,0,0,.15);transform:rotate(-2deg);margin-bottom:22px}h1{margin:0;font-weight:900;font-size:126px;line-height:.8;letter-spacing:-5px;text-transform:uppercase;text-shadow:0 8px 0 rgba(0,0,0,.16);max-width:760px}.script{display:block;font-family:Madelina,cursive;text-transform:none;font-weight:400;font-size:105px;line-height:.78;letter-spacing:0;color:var(--yellow);text-shadow:0 5px 0 rgba(0,0,0,.13)}.sub{margin-top:26px;max-width:560px;font-size:38px;line-height:1.08;font-weight:900;text-shadow:0 4px 0 rgba(0,0,0,.12)}.photoBox{position:absolute;right:-78px;bottom:112px;width:560px;height:650px;border-radius:95px 36px 95px 48px;overflow:hidden;z-index:6;box-shadow:0 24px 0 rgba(0,0,0,.16);transform:rotate(2deg);background:white}.photoBox img{width:100%;height:100%;object-fit:cover}.bigIcon{position:absolute;right:100px;bottom:175px;z-index:7;font-size:245px;filter:drop-shadow(0 17px 0 rgba(0,0,0,.16));transform:rotate(-8deg)}.ctaButton{position:absolute;left:80px;right:80px;bottom:150px;z-index:18;background:var(--blue);border:7px solid white;color:white;text-align:center;border-radius:999px;padding:26px 32px;font-size:43px;font-weight:900;box-shadow:0 14px 0 rgba(0,0,0,.16)}.strip{position:absolute;left:0;right:0;bottom:0;height:24px;z-index:25;display:grid;grid-template-columns:repeat(4,1fr)}.strip span:nth-child(1){background:var(--yellow)}.strip span:nth-child(2){background:var(--green)}.strip span:nth-child(3){background:var(--blue)}.strip span:nth-child(4){background:var(--red)}
.yellow{background:linear-gradient(135deg,var(--yellow),#ff9d00)}.yellow h1,.yellow .sub{color:var(--black);text-shadow:none}.yellow .script{color:var(--red);text-shadow:0 5px 0 rgba(255,255,255,.5)}.yellow .tag{background:var(--blue);color:white}.yellow .num{color:var(--black)}.red{background:linear-gradient(135deg,var(--red),#ff8a00)}.red .tag{background:var(--yellow);color:var(--black)}.blue{background:linear-gradient(135deg,var(--blue),#007fc9)}.blue .tag{background:var(--yellow);color:var(--black)}.blue .script{color:var(--yellow)}.photo,.photo2{background:linear-gradient(135deg,#FF7A00,var(--red))}.photo .main,.photo2 .main{top:255px}.photo h1,.photo2 h1{font-size:132px;max-width:590px}.photo .sub,.photo2 .sub{max-width:500px}.photo2 .script{color:var(--yellow)}.cta{background:linear-gradient(135deg,var(--yellow) 0%,#ff9d00 45%,var(--red) 100%)}.cta .main{text-align:center;top:265px}.cta h1{max-width:900px;margin:auto;color:white}.cta .script{color:var(--blue);font-size:98px}.cta .sub{margin:30px auto 0;max-width:780px;font-size:43px}.cta .tag{background:var(--red);color:var(--yellow)}
"""
def sec(s):
    media=''
    if 'photo' in s:
        media=f"<div class='photoBox'><img src='assets/{s['photo']}' style='object-position:{s.get('pos','center')}'></div>"
    elif s.get('icon'):
        media=f"<div class='bigIcon'>{s['icon']}</div>"
    cta="<div class='ctaButton'>CHAMA NO ZAP E AGENDE A AULA</div>" if s['theme']=='cta' else ''
    return f"""<section class='slide {s['theme']}'>
      <div class='blob b1'></div><div class='blob b2'></div><div class='blob b3'></div><div class='blob b4'></div>
      <img class='logo' src='assets/logo-kids.svg'><div class='handle'>@lamusickids</div>
      <div class='main'><div class='tag'>{s['tag']}</div><h1>{s['main']}<span class='script'>{s['script']}</span></h1><div class='sub'>{s['sub']}</div></div>
      {media}{cta}<div class='num'>{s['n']}/06</div><div class='strip'><span></span><span></span><span></span><span></span></div>
    </section>"""
html='<!doctype html><html><head><meta charset="utf-8"><style>'+css+'</style></head><body><div class="deck">'+''.join(sec(s) for s in slides)+'</div></body></html>'
(out/'carousel.html').write_text(html)
(out/'LAHQ_PIPELINE.md').write_text(textwrap.dedent('''
# LAHQ Pipeline — LA Music Kids V3 / Aulas em turma

## Mike — Demanda
Refazer carrossel Kids seguindo o pipeline LAHQ exatamente como no fluxo LA Music School, porém usando o DS novo da LA Music Kids.

## Nina — Direção criativa e estrutura
Fonte obrigatória: NotebookLM real `Treinamento e Estratégias para Aula em Turma` (`b4481df5-57c0-4f45-93cf-44cf523032cb`).
Tema: aulas em turma como conexão, escuta, motivação, pertencimento e método.
Estrutura: 6 slides — capa forte, 4 conteúdos curtos, CTA.

## Theo — Copy
Base do notebook: aula em grupo não dilui aprendizado; quando há método, o coletivo multiplica engajamento, escuta, confiança, vínculo e permanência.
Tom: LA Music Kids — fala com pais, leve e confiante, sem infantilizar.

## Luna — Visual/assets
DS Kids v2: Volkswagen + Madelina oficiais; logos SVG oficiais; refs oficiais corretas como alvo principal.
Visual: fundo quente amarelo/laranja/vermelho, blobs, pontilhado, texto grande, CTA inferior, logo topo.

## Diego — Montagem/exportação
HTML/CSS 1080x1350, slides independentes renderizados em PNG via Chromium.

## Tina/Nina — QA
Checklist visual: DS correto, cores corretas, fonte correta, logo presente, legibilidade mobile, CTA claro, sem placeholders/sobreposição crítica.
'''))
print(out)
