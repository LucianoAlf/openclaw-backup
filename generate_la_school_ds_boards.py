from pathlib import Path
import re, html, subprocess, textwrap, json, os
SRC = Path('/root/.openclaw/media/inbound/la-music-design-system---8b287cb8-bb46-484d-9b31-127d7e6c2011.html')
OUT = Path('/root/.openclaw/workspace/outputs/la-school-ds-token-audit-2026-05-12')
OUT.mkdir(parents=True, exist_ok=True)
text = SRC.read_text(errors='ignore')
imgs=[]
for m in re.finditer(r'<img\b[^>]*>', text, flags=re.I):
    tag=m.group(0)
    src=re.search(r'src=["\']([^"\']+)', tag)
    alt=re.search(r'alt=["\']([^"\']+)', tag)
    imgs.append((alt.group(1) if alt else '', src.group(1) if src else ''))
def pick(substr, idx=0):
    hits=[src for alt,src in imgs if substr.lower() in alt.lower()]
    return hits[idx] if len(hits)>idx else ''
logo_dark = pick('dark-completa',0)
logo_light = pick('light-completa',0)
watermark = pick('outline-white',0) or pick('Marca d',0)
photo = pick('Guitarrista',0)

CSS = f"""
@font-face {{ font-family: 'Prompt'; src: url('data:font/truetype;base64,{re.search(r"font-family: 'Prompt';[\\s\\S]*?base64,([^']+)'", text).group(1) if re.search(r"font-family: 'Prompt';[\\s\\S]*?base64,([^']+)'", text) else ''}') format('truetype'); }}
:root{{--pink:#E91451;--shade:#B01545;--deep:#740A28;--light:#F06292;--dark:#373435;--black:#0A0A0A;--soft:#141414;--gray:#E8E8E8;--mid:#9E9E9E;--white:#fff;}}
*{{box-sizing:border-box}} body{{margin:0;background:#111;font-family:Prompt,Arial,sans-serif}} .board{{width:1080px;height:1350px;position:relative;overflow:hidden;padding:58px 64px;background:var(--black);color:white}} .board.light{{background:var(--gray);color:var(--black)}}
.logo{{position:absolute;top:34px;left:0;right:0;text-align:center;z-index:10}} .logo img{{height:70px;object-fit:contain}} .eyebrow{{margin-top:70px;color:var(--pink);font-weight:800;text-transform:uppercase;letter-spacing:3px;font-size:24px}} h1{{font-size:86px;line-height:.88;margin:12px 0 18px;font-weight:900;letter-spacing:-4px;text-transform:uppercase}} h2{{font-size:56px;line-height:.92;margin:0;font-weight:900;letter-spacing:-2px}} p{{font-size:28px;line-height:1.35;color:#ddd;margin:0}} .light p{{color:#333}} .pink{{color:var(--pink)}} .outline{{color:transparent;-webkit-text-stroke:2px currentColor;text-stroke:2px currentColor}} .outline.white{{-webkit-text-stroke-color:#fff}} .outline.pink{{-webkit-text-stroke-color:var(--pink)}}
.grid{{display:grid;gap:22px}} .swatches{{grid-template-columns:repeat(2,1fr);margin-top:34px}} .swatch{{height:156px;border-radius:26px;padding:24px;display:flex;flex-direction:column;justify-content:flex-end;box-shadow:8px 10px 0 rgba(0,0,0,.35);border:1px solid rgba(255,255,255,.12)}} .swatch b{{font-size:31px}} .swatch span{{font-size:20px;opacity:.85;margin-top:5px}}
.note{{position:absolute;left:64px;right:64px;bottom:50px;padding:22px 26px;border-radius:999px;background:var(--pink);color:white;font-weight:800;font-size:25px;text-align:center;box-shadow:6px 8px 0 rgba(0,0,0,.7)}}
.tile{{position:relative;min-height:235px;border-radius:28px;background:#171717;padding:24px;overflow:hidden;border:1px solid rgba(255,255,255,.1)}} .tile h3{{font-size:30px;margin:0 0 10px;font-weight:900;color:#fff}} .tile p{{font-size:19px;line-height:1.24;color:#ccc}}
.halftone:after{{content:'';position:absolute;inset:0;background-image:radial-gradient(circle,var(--pink) 2px,transparent 3px);background-size:18px 18px;opacity:.55;mask-image:radial-gradient(ellipse at top right,black 0%,transparent 60%);-webkit-mask-image:radial-gradient(ellipse at top right,black 0%,transparent 60%)}}
.water:after{{content:'LA';position:absolute;right:-20px;bottom:-60px;font-size:210px;font-weight:900;color:transparent;-webkit-text-stroke:3px var(--pink);opacity:.35;letter-spacing:-18px}}
.container-demo .box{{display:inline-block;background:var(--pink);border-radius:22px;padding:19px 28px;transform:rotate(-3deg);box-shadow:10px 10px 0 #000;font-weight:900;font-size:44px;line-height:.9;margin-top:22px}}
.chev{{position:absolute;bottom:22px;left:24px;font-size:52px;font-weight:900;color:var(--pink);letter-spacing:-5px}} .plus{{position:absolute;right:24px;bottom:22px;display:grid;grid-template-columns:repeat(3,1fr);gap:4px 12px;color:var(--deep);font-size:34px;font-weight:900}}
.pill{{display:inline-flex;align-items:center;gap:12px;background:var(--pink);padding:14px 30px;border-radius:999px;font-weight:900;text-transform:uppercase;box-shadow:6px 7px 0 #000;margin-top:34px}} .stripes{{display:flex;gap:7px;justify-content:center;margin-top:14px}} .stripes i{{display:block;width:34px;height:6px;background:white;transform:skewX(-25deg)}}
.theme{{height:310px;border-radius:28px;padding:30px;position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:flex-end;box-shadow:8px 10px 0 rgba(0,0,0,.35)}} .theme h3{{font-size:42px;line-height:.9;margin:0;font-weight:900}} .theme p{{font-size:20px;margin-top:12px}} .theme.dark{{background:#000}} .theme.pgrad{{background:linear-gradient(135deg,var(--pink),var(--deep))}} .theme.psolid{{background:var(--pink)}} .theme.lmode{{background:var(--gray);color:#111}} .theme.lmode p{{color:#333}}
.post{{position:absolute;inset:0;background:#000}} .post img.bg{{width:100%;height:100%;object-fit:cover;filter:contrast(1.05) saturate(1.1)}} .post:before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 55% 35%,rgba(233,20,81,.08),rgba(0,0,0,.86) 72%)}} .post .dots{{position:absolute;inset:0;background-image:radial-gradient(circle,var(--pink) 2px,transparent 3px);background-size:17px 17px;opacity:.48;mask-image:linear-gradient(to right,black,transparent 40%);-webkit-mask-image:linear-gradient(to right,black,transparent 40%)}} .post .wm{{position:absolute;top:95px;left:-70px;font-size:290px;font-weight:900;color:transparent;-webkit-text-stroke:4px var(--pink);opacity:.35;letter-spacing:-26px}} .post .title{{position:absolute;left:70px;right:70px;bottom:330px;font-size:86px;line-height:.86;font-weight:900;text-transform:uppercase;letter-spacing:-4px}} .post .title .o{{color:transparent;-webkit-text-stroke:2px white}} .post .title .pinkword{{color:var(--pink)}} .post .footer{{position:absolute;bottom:70px;left:0;right:0;text-align:center}}
.rules{{margin-top:28px;grid-template-columns:1fr 1fr}} .rulebox{{border-radius:28px;padding:28px;background:#171717;border:1px solid rgba(255,255,255,.1)}} .rulebox h3{{font-size:38px;margin:0 0 18px;color:var(--pink)}} ul{{font-size:24px;line-height:1.25;margin:0;padding-left:28px}} li{{margin-bottom:15px}}
"""

def page(title, body, light=False):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><section class='board {'light' if light else ''}'><div class='logo'><img src='{logo_light if light else logo_dark}'></div>{body}</section></body></html>"

pages = []
pages.append(('01-tokens-paleta.html', page('tokens', """
<div class='eyebrow'>Diagnóstico DS · Tokens oficiais</div><h1>School usa <span class='pink'>uma cor</span><br><span class='outline white'>com profundidade</span></h1><p>O pink não é só fundo: ele vira CTA, textura, sombra, marca d’água, container e palavra-chave. Light mode é cinza #E8E8E8 — não bege.</p>
<div class='grid swatches'>
<div class='swatch' style='background:#E91451'><b>#E91451</b><span>Pink Primary · marca/CTA/pills</span></div><div class='swatch' style='background:#373435'><b>#373435</b><span>Dark LA · logo/texto em fundo claro</span></div><div class='swatch' style='background:#B01545'><b>#B01545</b><span>Pink Shade · halftone/gradiente</span></div><div class='swatch' style='background:#740A28'><b>#740A28</b><span>Pink Deep · sombra/marca d’água</span></div><div class='swatch' style='background:#0A0A0A'><b>#0A0A0A</b><span>Black · base dark</span></div><div class='swatch' style='background:#E8E8E8;color:#111'><b>#E8E8E8</b><span>Gray Light · fundo claro canônico</span></div>
</div><div class='note'>Regra pra skill: nunca puxar cream, roxo, azul ou multicolor. School = pink + dark + cinzas.</div>""")))

pages.append(('02-vocabulario-visual.html', page('vocab', """
<div class='eyebrow'>Vocabulário visual · 9 elementos</div><h1>Não é só <span class='pink'>card pink</span>.<br><span class='outline white'>é sistema.</span></h1>
<div class='grid' style='grid-template-columns:repeat(3,1fr);margin-top:26px'>
<div class='tile halftone'><h3>Halftone</h3><p>Pontos em degradê orgânico; textura de borda, não grid morto.</p></div>
<div class='tile water'><h3>Marca d’água LA</h3><p>Solo/outline gigante, sangrando, tom sobre tom.</p></div>
<div class='tile'><h3><span class='pink'>Sólido</span> + <span class='outline white'>Outline</span></h3><p>Assinatura tipográfica; sempre cria contra-peso.</p></div>
<div class='tile container-demo'><h3>Container Pink</h3><p>Bom, mas local. Não pode aparecer em todos os cards.</p><div class='box'>DICA 01</div></div>
<div class='tile'><h3>Chevrons</h3><p>Movimento e direção no canto inferior.</p><div class='chev'>» » »</div></div>
<div class='tile'><h3>Padrão +</h3><p>Textura sutil quando o halftone não precisa dominar.</p><div class='plus'><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span></div></div>
<div class='tile'><h3>Pill contato</h3><p>CTA inline: telefone/WhatsApp/@.</p><div class='pill'>@lamusicschool</div></div>
<div class='tile'><h3>Footer + listras</h3><p>Fechamento recorrente no rodapé.</p><div class='pill'>@lamusicschool</div><div class='stripes'><i></i><i></i><i></i><i></i></div></div>
<div class='tile'><h3>Logo topo</h3><p>Principal no topo centralizado em todos os cards.</p></div>
</div>""")))

pages.append(('03-temas.html', page('themes', """
<div class='eyebrow'>4 temas · alternar impacto</div><h1>Carrossel bom<br><span class='outline white'>respira em ciclos</span></h1><p>Não é tudo dark, nem tudo pink. A skill precisa escolher tema por função: capa, ensino, respiro, CTA.</p>
<div class='grid' style='grid-template-columns:1fr 1fr;margin-top:40px'>
<div class='theme dark halftone'><h3>DARK MODE</h3><p>Foto, palco, instrumento, atmosfera.</p></div>
<div class='theme pgrad halftone'><h3>PINK GRADIENT</h3><p>Impacto heroico, matrícula, convite.</p></div>
<div class='theme lmode'><h3>LIGHT MODE</h3><p>Conteúdo educativo mais respirado.</p></div>
<div class='theme psolid'><h3>PINK SOLID</h3><p>CTA final, chamada direta, fechamento.</p></div>
</div><div class='note'>Sequência recomendada: Dark/Pink capa → Light respiro → Dark/Pink energia → Pink Solid CTA.</div>""")))

pages.append(('04-anatomia-post.html', page('post', f"""
<div class='post'><img class='bg' src='{photo}'><div class='dots'></div><div class='wm'>LA</div><div class='logo'><img src='{logo_dark}'></div><div class='title'>tocar<br><span class='pinkword'>violão</span><br><span class='o'>com verdade</span></div><div class='footer'><div class='pill'>@lamusicschool</div><div class='stripes'><i></i><i></i><i></i><i></i></div></div><div class='chev'>» » »</div><div class='plus'><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span></div></div>
""")))

pages.append(('05-regras-skill.html', page('rules', """
<div class='eyebrow'>Regras novas pra lahq-school-content</div><h1>O padrão fixo é <span class='pink'>logo no topo</span>.<br>O resto é <span class='outline white'>composição.</span></h1>
<div class='grid rules'><div class='rulebox'><h3>Obrigatório</h3><ul><li>Logo principal centralizado no topo em todos os cards.</li><li>Usar SVG/logo oficial; nunca reconstruir com texto.</li><li>Prompt como família única.</li><li>Footer pill + listras no rodapé como padrão forte.</li><li>Comparar com refs ouro antes de entregar.</li></ul></div><div class='rulebox'><h3>Variável</h3><ul><li>Container pink pode aparecer, mas não em todos.</li><li>Alternar temas: dark, pink gradient, light, pink solid.</li><li>Usar halftone, LA watermark, chevrons, +, pills e outline type.</li><li>Foto hero quando vender desejo; light mode quando ensinar.</li><li>Card precisa parecer campanha, não template.</li></ul></div></div><div class='note'>Correção importante do Alf: logo principal no topo vira padrão; pink card vira recurso, não muleta.</div>""")))

pages.append(('06-componentes-aprovacao.html', page('components', """
<div class='eyebrow'>Componentes para aprovar antes da skill</div><h1>Biblioteca mínima<br><span class='pink'>School v1</span></h1><p>Minha proposta: a skill School não guarda layouts prontos; guarda este vocabulário e obriga escolha consciente por card.</p>
<div class='grid' style='grid-template-columns:1fr 1fr;margin-top:40px'>
<div class='tile'><h3>Header fixo</h3><p>Logo completo topo/centro. Varia só versão dark/light/vazada por contraste.</p></div>
<div class='tile'><h3>Hero visual</h3><p>Foto full-bleed + vignette + halftone + título grande.</p></div>
<div class='tile'><h3>Card educativo</h3><p>Light #E8E8E8, mais respiro, texto curto, outline pink/preto.</p></div>
<div class='tile'><h3>Card impacto</h3><p>Pink gradient ou dark com LA watermark gigante.</p></div>
<div class='tile'><h3>Card destaque</h3><p>Container pink inclinado com sombra preta — uso controlado.</p></div>
<div class='tile'><h3>CTA final</h3><p>Pink solid + footer pill + CTA direto e musical.</p></div>
</div><div class='note'>Se você aprovar essa biblioteca, eu transformo isso no coração da skill School.</div>""")))

html_paths=[]
for name, content in pages:
    p=OUT/name; p.write_text(content); html_paths.append(p)

chromium='/usr/local/bin/chromium'
for p in html_paths:
    png=OUT/(p.stem+'.png')
    cmd=[chromium,'--headless','--no-sandbox','--disable-gpu','--window-size=1080,1350',f'--screenshot={png}',p.as_uri()]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# index/contact sheet html
contact = "<!doctype html><html><head><meta charset='utf-8'><style>body{margin:0;background:#222;display:grid;grid-template-columns:repeat(3,360px);gap:12px;padding:12px}img{width:360px;height:450px;object-fit:cover}</style></head><body>" + ''.join(f"<img src='{(OUT/(p.stem+'.png')).name}'>" for p in html_paths) + "</body></html>"
idx=OUT/'contact-sheet.html'; idx.write_text(contact)
subprocess.run([chromium,'--headless','--no-sandbox','--disable-gpu','--window-size=1116,924',f'--screenshot={OUT/"contact-sheet.png"}',idx.as_uri()], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(OUT)
for p in sorted(OUT.glob('*.png')): print(p)
