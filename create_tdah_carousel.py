from pathlib import Path
from PIL import Image, ImageOps
import subprocess, shutil

root=Path('/root/.openclaw/workspace')
repo=root/'repos/la-hq-agents'
out=root/'outputs/la-school-tdah-concentracao-disciplina-v1'
out.mkdir(parents=True, exist_ok=True)
media=Path('/root/.openclaw/media/tool-image-generation')
photos=[
 media/'la-school-tdah-photo-01-classroom-guitar---be999bbb-e290-43d7-a8e7-fcce720d3728.png',
 media/'la-school-tdah-photo-02-vocal-class---cc0bdc77-1cec-419c-b14f-b05cc8cb6e39.png',
 media/'la-school-tdah-photo-04-rhythm-discipline---72db3001-abbf-447f-8b1f-6c6826a388f0.png',
 media/'la-school-tdah-photo-03-stage-performance---9fa968de-7490-42a2-aa50-82eacb8d03ca.png',
]
for i,p in enumerate(photos,1):
    shutil.copy(p, out/f'photo-{i:02d}.png')
logo_dark=repo/'shared/brand-assets/logos/school/logo-la-music-dark-completa.svg'
logo_light=repo/'shared/brand-assets/logos/school/logo-la-music-light-completa.svg'
solo_vaz=repo/'shared/brand-assets/logos/school/logo-la-music-dark-solo-vazada.svg'
font_black=repo/'shared/brand-assets/fonts/school/Prompt-Black.ttf'
font_bold=repo/'shared/brand-assets/fonts/school/Prompt-Bold.ttf'
font_regular=repo/'shared/brand-assets/fonts/school/Prompt-Regular.ttf'

slides=[
 dict(theme='photo cover', photo='photo-01.png', logo='dark', num='01/07', kicker='TDAH + MÚSICA', title='FOCO\nTAMBÉM\nSE ENSAIA', outline='CONCENTRAÇÃO', body='A música dá começo, meio e fim para a atenção.', accent='»»»'),
 dict(theme='light', photo='photo-02.png', logo='light', num='02/07', kicker='SALA DE AULA', title='UM ALVO\nPOR VEZ', outline='MENOS RUÍDO', body='Quando o professor organiza o próximo passo, a mente para de brigar com dez tarefas ao mesmo tempo.'),
 dict(theme='dark', photo=None, logo='dark', num='03/07', kicker='RITMO', title='A BATIDA\nORGANIZA\nO CORPO', outline='PULSO', body='Contar, esperar, entrar no tempo certo: isso treina presença e autocontrole sem discurso chato.'),
 dict(theme='photo split', photo='photo-03.png', logo='dark', num='04/07', kicker='DISCIPLINA', title='ROTINA\nNÃO É\nCASTIGO', outline='PRÁTICA', body='Cinco minutos bem feitos, repetidos com direção, valem mais do que uma hora perdida no automático.'),
 dict(theme='photo stage', photo='photo-04.png', logo='dark', num='05/07', kicker='PALCO', title='ATENÇÃO\nVIRA\nPRESENÇA', outline='CORAGEM', body='No palco, o aluno aprende a sustentar foco mesmo com emoção, luz, erro e plateia.'),
 dict(theme='pink', photo=None, logo='dark', num='06/07', kicker='IMPORTANTE', title='MÚSICA\nNÃO SUBSTITUI\nCUIDADO', outline='MAS AJUDA', body='Para pessoas com TDAH, aula de música pode ser uma prática poderosa de foco, escuta e disciplina — junto do acompanhamento certo.'),
 dict(theme='cta', photo=None, logo='dark', num='07/07', kicker='LA MUSIC SCHOOL', title='CONCENTRAÇÃO\nCOM\nDIREÇÃO', outline='AULA EXPERIMENTAL', body='A gente ensina música com método, escuta e desafio real. Vem testar uma aula.', cta='LINK NA BIO'),
]

base_css=f'''
@font-face{{font-family:Prompt;src:url("file://{font_regular}");font-weight:400}}
@font-face{{font-family:Prompt;src:url("file://{font_bold}");font-weight:700}}
@font-face{{font-family:Prompt;src:url("file://{font_black}");font-weight:900}}
*{{box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1440px;overflow:hidden;background:#0A0A0A;font-family:Prompt,Arial,sans-serif}}
.slide{{position:relative;width:1080px;height:1440px;overflow:hidden;color:#fff;background:#0A0A0A}}
.logo{{position:absolute;top:58px;left:50%;transform:translateX(-50%);width:250px;z-index:20}}
.num{{position:absolute;top:72px;right:64px;font-size:28px;font-weight:900;letter-spacing:.08em;z-index:20;color:#E91451}}
.kicker{{position:absolute;top:190px;left:66px;font-size:34px;font-weight:900;letter-spacing:.06em;color:#E91451;z-index:20}}
.title{{position:absolute;left:62px;right:50px;top:260px;font-size:126px;line-height:.9;font-weight:900;letter-spacing:-.055em;z-index:20;text-transform:uppercase;text-shadow:0 8px 0 rgba(0,0,0,.55)}}
.outline{{position:absolute;left:56px;right:40px;bottom:410px;font-size:82px;line-height:.9;font-weight:900;letter-spacing:-.045em;color:transparent;-webkit-text-stroke:2.5px rgba(255,255,255,.82);z-index:19;text-transform:uppercase}}
.body{{position:absolute;left:68px;right:78px;bottom:205px;font-size:42px;line-height:1.12;font-weight:700;z-index:22;color:#fff;max-width:875px}}
.footer{{position:absolute;left:50%;bottom:58px;transform:translateX(-50%);background:#E91451;color:#fff;border-radius:999px;padding:16px 42px 18px;font-size:30px;font-weight:900;letter-spacing:.02em;z-index:30;box-shadow:0 13px 0 rgba(0,0,0,.5)}}
.stripes{{position:absolute;left:340px;right:340px;bottom:30px;height:12px;background:repeating-linear-gradient(135deg,#E91451 0 18px,transparent 18px 31px);z-index:29}}
.halftone{{position:absolute;inset:-120px;background:radial-gradient(circle at 20% 20%,rgba(233,20,81,.34) 0 2px,transparent 2.5px),radial-gradient(circle at 82% 75%,rgba(255,255,255,.18) 0 1.5px,transparent 2.2px);background-size:22px 22px,18px 18px;mask-image:radial-gradient(circle at 15% 22%,#000 0,transparent 43%),radial-gradient(circle at 85% 75%,#000 0,transparent 38%);opacity:.95;z-index:4}}
.plus{{position:absolute;right:80px;top:230px;color:rgba(255,255,255,.19);font-size:44px;font-weight:900;line-height:1.15;white-space:pre;z-index:5}}
.photo{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1;filter:contrast(1.12) saturate(1.02)}}
.overlay{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.45),rgba(10,10,10,.22) 32%,rgba(10,10,10,.85) 78%,rgba(10,10,10,.96));z-index:2}}
.pinkGlow{{position:absolute;inset:auto -180px -240px -180px;height:620px;background:radial-gradient(ellipse at center,rgba(233,20,81,.65),transparent 62%);z-index:3}}
.laMark{{position:absolute;right:-220px;bottom:140px;width:640px;opacity:.10;z-index:3}}
.cta{{position:absolute;left:66px;bottom:320px;background:#E91451;border-radius:34px;padding:20px 38px 24px;font-size:60px;font-weight:900;z-index:25;box-shadow:14px 14px 0 rgba(0,0,0,.58)}}
.light{{background:#E8E8E8;color:#373435}}.light .title,.light .body{{color:#373435;text-shadow:none}}.light .outline{{-webkit-text-stroke:2.8px rgba(55,52,53,.40)}}.light .footer{{box-shadow:0 13px 0 rgba(55,52,53,.35)}}
.darkTypo{{background:radial-gradient(circle at 88% 12%,rgba(233,20,81,.45),transparent 30%),#0A0A0A}}
.pinkTheme{{background:linear-gradient(155deg,#E91451,#740A28 62%,#0A0A0A)}}.pinkTheme .outline{{-webkit-text-stroke:2.8px rgba(255,255,255,.55)}}
.ctaTheme{{background:radial-gradient(circle at 80% 20%,rgba(233,20,81,.5),transparent 28%),#0A0A0A}}
'''

def html_for(i,s):
    theme_class=''
    if s['theme']=='light': theme_class=' light'
    elif s['theme']=='pink': theme_class=' pinkTheme'
    elif s['theme']=='cta': theme_class=' ctaTheme'
    elif s['theme']=='dark': theme_class=' darkTypo'
    logo=logo_light if s.get('logo')=='light' else logo_dark
    title=s['title'].replace('\n','<br>')
    photo_html=''
    if s.get('photo'):
        photo_html=f'<img class="photo" src="{s["photo"]}"><div class="overlay"></div><div class="pinkGlow"></div>'
    mark=f'<img class="laMark" src="file://{solo_vaz}">' if not s.get('photo') or s['theme'] in ['cta','dark'] else ''
    plus='+  +  +\n  +  +  +\n+  +  +'
    cta=f'<div class="cta">{s.get("cta","")}</div>' if s.get('cta') else ''
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{base_css}</style></head><body>
<div class="slide{theme_class}">
{photo_html}<div class="halftone"></div>{mark}<div class="plus">{plus}</div>
<img class="logo" src="file://{logo}"><div class="num">{s['num']}</div>
<div class="kicker">{s['kicker']}</div>
<div class="title">{title}</div>
<div class="outline">{s['outline']}</div>
<div class="body">{s['body']}</div>{cta}
<div class="footer">@lamusicschool</div><div class="stripes"></div>
</div></body></html>'''

for idx,s in enumerate(slides,1):
    (out/f'slide-{idx:02d}.html').write_text(html_for(idx,s),encoding='utf-8')

chromium=shutil.which('chromium') or '/usr/local/bin/chromium'
for idx in range(1,8):
    html=(out/f'slide-{idx:02d}.html').as_uri()
    png=out/f'la-school-tdah-{idx:02d}.png'
    cmd=[chromium,'--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--hide-scrollbars','--window-size=1080,1440',f'--screenshot={png}',html]
    subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

imgs=[Image.open(out/f'la-school-tdah-{i:02d}.png').convert('RGB') for i in range(1,8)]
thumbs=[ImageOps.contain(im,(270,360)) for im in imgs]
canvas=Image.new('RGB',(1080,720),(18,18,18))
for i,t in enumerate(thumbs):
    x=(i%4)*270; y=(i//4)*360
    canvas.paste(t,(x,y))
canvas.save(out/'preview-grid.jpg',quality=92)
copy='''# Carrossel — TDAH, concentração e disciplina

Formato: 7 lâminas 1080x1440 — LA Music School

1. FOCO TAMBÉM SE ENSAIA — A música dá começo, meio e fim para a atenção.
2. UM ALVO POR VEZ — Quando o professor organiza o próximo passo, a mente para de brigar com dez tarefas ao mesmo tempo.
3. A BATIDA ORGANIZA O CORPO — Contar, esperar, entrar no tempo certo: isso treina presença e autocontrole sem discurso chato.
4. ROTINA NÃO É CASTIGO — Cinco minutos bem feitos, repetidos com direção, valem mais do que uma hora perdida no automático.
5. ATENÇÃO VIRA PRESENÇA — No palco, o aluno aprende a sustentar foco mesmo com emoção, luz, erro e plateia.
6. MÚSICA NÃO SUBSTITUI CUIDADO — Para pessoas com TDAH, aula de música pode ser uma prática poderosa de foco, escuta e disciplina — junto do acompanhamento certo.
7. CONCENTRAÇÃO COM DIREÇÃO — A gente ensina música com método, escuta e desafio real. Vem testar uma aula.

Observação ética: sem promessa terapêutica; linguagem de apoio/desenvolvimento.
'''
(out/'CARROSSEL_COMPLETO.md').write_text(copy,encoding='utf-8')
print(out)
