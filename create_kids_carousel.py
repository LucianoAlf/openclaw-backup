from pathlib import Path
import re, textwrap
out=Path('/root/.openclaw/workspace/outputs/la-kids-aula-em-grupo-v1')
(out/'png').mkdir(parents=True, exist_ok=True)
repo=Path('/root/.openclaw/workspace/repos/la-hq-agents')
ds=(repo/'shared/design-systems/la-music-kids-design-system.html').read_text(errors='ignore')
font_css='\n'.join(re.findall(r"@font-face\s*\{.*?\}\s*", ds, flags=re.S))
logo=(repo/'shared/design-systems/la-music-kids-v2/assets/logos/logo-la-music-kids-light-completa.svg').read_text(errors='ignore')
logo_data='data:image/svg+xml;utf8,'+logo.replace('#','%23').replace('\n',' ').replace('"',"'")
slides=[
('01','GUIA KIDS','AULA EM GRUPO','música que aproxima','Seu filho aprende, se expressa e cria vínculos enquanto toca com outras crianças.','dark'),
('02','APRENDIZADO','OUVIR O OUTRO','também é música','Na turma, a criança percebe ritmo, pausa, entrada e escuta. Isso desenvolve atenção musical de verdade.','white'),
('03','CORAGEM','O GRUPO DÁ','segurança','Quando uma criança vê a outra tentando, ela entende: “eu também posso”. A confiança cresce junto.','yellow'),
('04','MÉTODO','CADA CRIANÇA','tem seu tempo','Aula em grupo não é largar todo mundo igual. É conduzir diferenças com propósito, cuidado e acompanhamento.','blue'),
('05','CONEXÃO','MENOS TELA,','mais presença','Música em turma cria amizade, cooperação e pertencimento — coisas que nenhuma tela substitui.','white2'),
('06','VEM PRA KIDS','MÚSICA NÃO É','só pra gente grande','Agende uma aula experimental e veja seu filho descobrir a música brincando, tocando e convivendo.','cta'),
]

def blobs():
    return """
    <div class='blob b1'></div><div class='blob b2'></div><div class='blob b3'></div><div class='blob b4'></div>
    <div class='dots'></div><div class='mark4'>4</div>
    """

def mini_illustration(i):
    icons=['🎸','🥁','🎹','🎵','🎤','✨']
    return f"""<div class='photo-card p{i}'><div class='kid k1'></div><div class='kid k2'></div><div class='instrument'>{icons[i-1]}</div><div class='staff'></div></div>"""

html=f"""<!doctype html><html><head><meta charset='utf-8'><style>
{font_css}
:root{{--yellow:#FFF212;--green:#17B255;--blue:#00AFEF;--red:#ED3237;--black:#1A1A1A;--cream:#FFFEF5;}}
*{{box-sizing:border-box}} body{{margin:0;background:#ddd;font-family:'Volkswagen',system-ui,sans-serif;}}
.deck{{display:flex;gap:30px;flex-wrap:wrap;padding:30px}}
.slide{{width:1080px;height:1350px;position:relative;overflow:hidden;background:white;color:var(--black);padding:82px 78px;border-radius:0;}}
.dark{{background:linear-gradient(180deg,rgba(26,26,26,.92),rgba(26,26,26,.98)), radial-gradient(circle at 55% 20%, #00AFEF55, transparent 40%), var(--black);color:white}}
.yellow{{background:var(--yellow)}} .blue{{background:var(--blue);color:white}} .cta{{background:linear-gradient(135deg,var(--blue),#0797d5);color:white}} .white2{{background:var(--cream)}}
.handle{{position:absolute;top:44px;left:70px;background:var(--red);color:var(--yellow);padding:14px 28px;border-radius:40px 28px 44px 26px;font-weight:800;font-size:25px;letter-spacing:1px;text-transform:uppercase;z-index:5;box-shadow:0 10px 0 rgba(0,0,0,.12)}}
.num{{position:absolute;top:56px;right:70px;font-size:28px;font-weight:800;z-index:5;opacity:.85}}
.label{{display:inline-block;margin-top:130px;background:var(--red);color:var(--yellow);font-weight:800;font-size:31px;letter-spacing:2px;padding:12px 24px;border-radius:14px;transform:rotate(-2deg);box-shadow:0 10px 0 rgba(0,0,0,.12);position:relative;z-index:4}}
h1{{font-weight:800;font-size:118px;line-height:.9;margin:34px 0 0;letter-spacing:-4px;text-transform:uppercase;position:relative;z-index:4;max-width:880px}}
h1 .script{{display:block;font-family:'Madelina',cursive;text-transform:none;font-weight:400;font-size:118px;letter-spacing:0;color:var(--yellow);line-height:.85;margin-top:12px;text-shadow:0 5px 0 rgba(0,0,0,.12)}}
.white h1 .script,.white2 h1 .script{{color:var(--red)}} .yellow h1 .script{{color:var(--blue)}} .blue h1 .script,.cta h1 .script{{color:var(--yellow)}}
.desc{{font-size:39px;line-height:1.18;font-weight:600;max-width:760px;margin-top:32px;position:relative;z-index:4}}
.logo{{position:absolute;left:70px;bottom:54px;width:255px;z-index:5}} .swipe{{position:absolute;right:70px;bottom:72px;border:3px solid currentColor;border-radius:999px;padding:14px 26px;font-weight:800;font-size:24px;z-index:5}}
.bar{{position:absolute;left:0;right:0;bottom:0;height:18px;display:grid;grid-template-columns:repeat(4,1fr);z-index:9}}.bar span:nth-child(1){{background:var(--yellow)}}.bar span:nth-child(2){{background:var(--green)}}.bar span:nth-child(3){{background:var(--blue)}}.bar span:nth-child(4){{background:var(--red)}}
.blob{{position:absolute;border-radius:42% 58% 61% 39%/54% 35% 65% 46%;z-index:1;opacity:.96}}.b1{{width:360px;height:340px;background:var(--yellow);right:-140px;top:105px;transform:rotate(18deg)}}.b2{{width:330px;height:300px;background:var(--green);left:-145px;bottom:150px;transform:rotate(-18deg)}}.b3{{width:230px;height:240px;background:var(--red);right:65px;bottom:-82px;transform:rotate(24deg)}}.b4{{width:210px;height:190px;background:var(--blue);left:40px;top:-75px;transform:rotate(-9deg)}}
.dots{{position:absolute;inset:0;opacity:.14;background-image:radial-gradient(currentColor 2px, transparent 2px);background-size:30px 30px;z-index:0}}.mark4{{position:absolute;right:-70px;bottom:80px;font-size:760px;line-height:.8;font-weight:800;color:rgba(0,0,0,.055);z-index:0}}.dark .mark4,.blue .mark4,.cta .mark4{{color:rgba(255,255,255,.10)}}
.photo-card{{position:absolute;right:68px;bottom:210px;width:330px;height:380px;border-radius:46px;background:#fff;z-index:3;box-shadow:0 24px 0 rgba(0,0,0,.13);overflow:hidden;transform:rotate(3deg)}}.p2,.p5{{right:70px;top:250px;bottom:auto;transform:rotate(-3deg)}}.p3{{right:84px;bottom:165px;background:var(--blue)}}.p4{{right:70px;bottom:170px;background:#fff;color:var(--black)}}.p6{{right:70px;top:300px;background:var(--yellow)}}
.kid{{position:absolute;width:92px;height:92px;border-radius:50%;background:#f4b27b;top:88px}}.k1{{left:70px}}.k2{{right:65px;background:#8a5a3b}}.kid:after{{content:'';position:absolute;left:-18px;top:68px;width:130px;height:150px;border-radius:44px 44px 0 0;background:var(--red)}}.k2:after{{background:var(--green)}}.instrument{{position:absolute;left:50%;top:210px;transform:translateX(-50%);font-size:94px}}.staff{{position:absolute;left:35px;right:35px;bottom:46px;height:44px;background:repeating-linear-gradient(to bottom,transparent 0 8px,rgba(0,0,0,.25) 8px 11px)}}
.list{{position:relative;z-index:4;margin-top:45px;display:grid;gap:16px;max-width:640px}}.item{{background:rgba(255,255,255,.88);border-radius:28px;padding:20px 24px;font-size:30px;font-weight:800;color:var(--black);box-shadow:0 8px 0 rgba(0,0,0,.1)}}.item:before{{content:'✓';color:var(--green);margin-right:12px}}
.cta .button{{position:relative;z-index:5;display:inline-block;background:var(--yellow);color:var(--black);border-radius:999px;padding:24px 42px;font-size:34px;font-weight:800;margin-top:44px;box-shadow:0 12px 0 rgba(0,0,0,.18)}}
</style></head><body><div class='deck'>
"""
for idx,(num,label,title,script,desc,theme) in enumerate(slides,1):
    list_html=''
    if idx==4:
        list_html="<div class='list'><div class='item'>o professor observa</div><div class='item'>a turma inspira</div><div class='item'>cada avanço importa</div></div>"
    elif idx==5:
        list_html="<div class='list'><div class='item'>cooperação</div><div class='item'>autonomia</div><div class='item'>pertencimento</div></div>"
    button="<div class='button'>AGENDAR AULA EXPERIMENTAL</div>" if idx==6 else ''
    html += f"""<section class='slide {theme}' id='slide-{idx:02d}'>
      {blobs()}<div class='handle'>@lamusickids</div><div class='num'>{num}/06</div>
      <div class='label'>{label}</div><h1>{title}<span class='script'>{script}</span></h1>
      <p class='desc'>{desc}</p>{list_html}{button}{mini_illustration(idx)}
      <img class='logo' src=\"{logo_data}\"><div class='swipe'>{'chama no WhatsApp' if idx==6 else 'deslize →'}</div><div class='bar'><span></span><span></span><span></span><span></span></div>
    </section>"""
html += "</div></body></html>"
(out/'carousel.html').write_text(html)
(out/'LAHQ_PIPELINE.md').write_text(textwrap.dedent('''
# LAHQ Pipeline — LA Music Kids / Aula em Grupo

## Nina — Direção e estrutura
Tema extraído do NotebookLM `A Revolução Silenciosa das Aulas em Grupo`: aula em grupo como conexão, pertencimento, desenvolvimento musical e socioemocional.

## Theo — Copy
Comunicação para pais, leve e profissional, sem infantilizar. Promessa central: aula em grupo não divide atenção; multiplica escuta, coragem e vínculo.

## Luna — Visual
DS LA Music Kids v2: Volkswagen + Madelina; paleta catavento; blobs orgânicos; dotted pattern; handle vermelho `@lamusickids`; logo oficial SVG; barra 4 cores.

## Diego — Render
HTML/CSS 1080x1350, 6 slides PNG + preview grid.
'''))
print(out)
