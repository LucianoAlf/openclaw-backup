from pathlib import Path
from PIL import Image, ImageOps
import subprocess, shutil

root=Path('/root/.openclaw/workspace')
repo=root/'repos/la-hq-agents'
out=root/'outputs/la-school-tdah-concentracao-disciplina-v3'
out.mkdir(parents=True, exist_ok=True)
prev=root/'outputs/la-school-tdah-concentracao-disciplina-v1'
for i in range(1,5): shutil.copy(prev/f'photo-{i:02d}.png', out/f'photo-{i:02d}.png')
logo_dark=repo/'shared/brand-assets/logos/school/logo-la-music-dark-completa.svg'
logo_light=repo/'shared/brand-assets/logos/school/logo-la-music-light-completa.svg'
solo_vaz=repo/'shared/brand-assets/logos/school/logo-la-music-dark-solo-vazada.svg'
font_black=repo/'shared/brand-assets/fonts/school/Prompt-Black.ttf'
font_bold=repo/'shared/brand-assets/fonts/school/Prompt-Bold.ttf'
font_regular=repo/'shared/brand-assets/fonts/school/Prompt-Regular.ttf'

slides=[
 dict(cls='s1 photoCard', photo='photo-01.png', logo='dark', num='01/07', kicker='TDAH + MÚSICA', title='FOCO\nTAMBÉM\nSE ENSAIA', outline='CONCENTRAÇÃO', body='Escutar. Esperar. Entrar no tempo certo.'),
 dict(cls='s2 lightCard', photo='photo-02.png', logo='light', num='02/07', kicker='SALA DE AULA', title='UM ALVO\nPOR VEZ', outline='MENOS RUÍDO', body='Instrumento, tempo, trecho. Uma tarefa clara por rodada.'),
 dict(cls='s3 darkTypo', photo=None, logo='dark', num='03/07', kicker='RITMO', title='A BATIDA\nORGANIZA\nO CORPO', outline='PULSO', body='Contar e esperar também é treino de autocontrole.'),
 dict(cls='s4 photoCard', photo='photo-03.png', logo='dark', num='04/07', kicker='DISCIPLINA', title='ROTINA\nNÃO É\nCASTIGO', outline='PRÁTICA', body='Pequenas repetições. Correção certa. Progresso visível.'),
 dict(cls='s5 photoCard', photo='photo-04.png', logo='dark', num='05/07', kicker='PALCO', title='ATENÇÃO\nVIRA\nPRESENÇA', outline='CORAGEM', body='No palco, foco vira atitude — mesmo com emoção e plateia.'),
 dict(cls='s6 pinkTheme', photo=None, logo='dark', num='06/07', kicker='IMPORTANTE', title='NÃO É\nTRATAMENTO.\nÉ PRÁTICA.', outline='COM DIREÇÃO', body='Para pessoas com TDAH, música pode apoiar foco, escuta e disciplina — quando necessário, junto do acompanhamento profissional adequado.'),
 dict(cls='s7 ctaTheme', photo=None, logo='dark', num='07/07', kicker='LA MUSIC SCHOOL', title='CONCENTRAÇÃO\nCOM\nDIREÇÃO', outline='AULA EXPERIMENTAL', body='Aula com método, escuta e desafio real.', cta='LINK NA BIO'),
]

base_css=f'''
@font-face{{font-family:Prompt;src:url("file://{font_regular}");font-weight:400}}
@font-face{{font-family:Prompt;src:url("file://{font_bold}");font-weight:700}}
@font-face{{font-family:Prompt;src:url("file://{font_black}");font-weight:900}}
*{{box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1440px;overflow:hidden;background:#0A0A0A;font-family:Prompt,Arial,sans-serif}}
.slide{{position:relative;width:1080px;height:1440px;overflow:hidden;color:#fff;background:#0A0A0A}}
.logo{{position:absolute;top:58px;left:50%;transform:translateX(-50%);width:250px;z-index:30}}
.num{{position:absolute;top:72px;right:64px;font-size:28px;font-weight:900;letter-spacing:.08em;z-index:30;color:#E91451}}
.kicker{{position:absolute;top:185px;left:66px;font-size:34px;font-weight:900;letter-spacing:.06em;color:#E91451;z-index:25}}
.title{{position:absolute;left:62px;right:50px;top:285px;font-size:118px;line-height:.9;font-weight:900;letter-spacing:-.055em;z-index:25;text-transform:uppercase;text-shadow:0 8px 0 rgba(0,0,0,.58)}}
.outline{{position:absolute;left:60px;right:40px;bottom:382px;font-size:74px;line-height:.9;font-weight:900;letter-spacing:-.045em;color:rgba(255,255,255,.10);-webkit-text-stroke:2.2px rgba(255,255,255,.62);z-index:19;text-transform:uppercase}}
.body{{position:absolute;left:68px;right:74px;bottom:205px;font-size:52px;line-height:1.05;font-weight:800;z-index:26;color:#fff;max-width:900px;text-shadow:0 4px 0 rgba(0,0,0,.55)}}
.footer{{position:absolute;left:50%;bottom:58px;transform:translateX(-50%);background:#E91451;color:#fff;border-radius:999px;padding:16px 42px 18px;font-size:30px;font-weight:900;letter-spacing:.02em;z-index:35;box-shadow:0 13px 0 rgba(0,0,0,.5)}}
.stripes{{position:absolute;left:340px;right:340px;bottom:30px;height:12px;background:repeating-linear-gradient(135deg,#E91451 0 18px,transparent 18px 31px);z-index:34}}
.halftone{{position:absolute;inset:-100px;background:radial-gradient(circle at 15% 18%,rgba(233,20,81,.36) 0 2px,transparent 2.6px),radial-gradient(circle at 88% 76%,rgba(255,255,255,.15) 0 1.5px,transparent 2.2px);background-size:22px 22px,18px 18px;mask-image:radial-gradient(circle at 18% 20%,#000 0,transparent 42%),radial-gradient(circle at 86% 76%,#000 0,transparent 38%);z-index:4}}
.plus{{position:absolute;right:74px;top:238px;color:rgba(255,255,255,.18);font-size:42px;font-weight:900;line-height:1.15;white-space:pre;z-index:5}}
.photo{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1;filter:contrast(1.12) saturate(1.05)}}
.overlay{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.28),rgba(10,10,10,.14) 28%,rgba(10,10,10,.74) 62%,rgba(10,10,10,.97) 100%);z-index:2}}
.pinkGlow{{position:absolute;left:-160px;right:-160px;bottom:-240px;height:650px;background:radial-gradient(ellipse at center,rgba(233,20,81,.67),transparent 62%);z-index:3}}
.laMark{{position:absolute;right:-240px;bottom:105px;width:700px;opacity:.105;z-index:3}}
.cta{{position:absolute;left:66px;bottom:320px;background:#E91451;border-radius:34px;padding:20px 38px 24px;font-size:60px;font-weight:900;z-index:25;box-shadow:14px 14px 0 rgba(0,0,0,.58)}}
.lightCard{{background:#E8E8E8;color:#373435}}.lightCard .photo{{inset:500px 42px auto auto;width:470px;height:600px;border-radius:42px;box-shadow:22px 22px 0 #E91451;object-position:center;z-index:8}}.lightCard .overlay,.lightCard .pinkGlow{{display:none}}.lightCard .title,.lightCard .body{{color:#373435;text-shadow:none}}.lightCard .title{{right:380px;top:300px;font-size:114px}}.lightCard .outline{{bottom:265px;-webkit-text-stroke:2.7px rgba(55,52,53,.38)}}.lightCard .body{{right:560px;bottom:360px;font-size:42px}}.lightCard .footer{{box-shadow:0 13px 0 rgba(55,52,53,.35)}}
.darkTypo{{background:radial-gradient(circle at 85% 10%,rgba(233,20,81,.48),transparent 30%),#0A0A0A}}.darkTypo .title{{font-size:108px;top:305px}}.darkTypo .body{{font-size:54px;bottom:225px}}
.pinkTheme{{background:linear-gradient(155deg,#E91451,#740A28 58%,#0A0A0A)}}.pinkTheme .title{{font-size:104px;top:275px}}.pinkTheme .outline{{bottom:310px;-webkit-text-stroke:2.6px rgba(255,255,255,.58)}}.pinkTheme .body{{font-size:46px;bottom:190px;right:70px}}
.ctaTheme{{background:radial-gradient(circle at 80% 20%,rgba(233,20,81,.55),transparent 28%),#0A0A0A}}.ctaTheme .title{{font-size:112px}}.ctaTheme .body{{bottom:225px}}
.photoCard .outline{{display:none}}
.s1 .title{{top:585px;font-size:120px;left:50px;right:52px;background:linear-gradient(135deg,rgba(233,20,81,.96),rgba(116,10,40,.92));padding:24px 28px 32px;border-radius:38px;box-shadow:18px 18px 0 rgba(0,0,0,.62);transform:rotate(-1deg)}}.s1 .kicker{{top:500px}}.s1 .body{{bottom:205px;font-size:50px}}
.s4 .title{{top:650px;font-size:108px}}.s4 .kicker{{top:560px}}.s4 .body{{bottom:205px;font-size:49px}}
.s5 .title{{top:650px;font-size:108px}}.s5 .kicker{{top:560px}}.s5 .body{{bottom:205px;font-size:49px}}
'''

def html_for(s):
    logo=logo_light if s.get('logo')=='light' else logo_dark
    title=s['title'].replace('\n','<br>')
    photo_html=''
    if s.get('photo'):
        photo_html=f'<img class="photo" src="{s["photo"]}"><div class="overlay"></div><div class="pinkGlow"></div>'
    mark=f'<img class="laMark" src="file://{solo_vaz}">' if not s.get('photo') or 'darkTypo' in s['cls'] or 'ctaTheme' in s['cls'] else ''
    plus='+  +  +\n  +  +  +\n+  +  +'
    cta=f'<div class="cta">{s.get("cta","")}</div>' if s.get('cta') else ''
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{base_css}</style></head><body>
<div class="slide {s['cls']}">
{photo_html}<div class="halftone"></div>{mark}<div class="plus">{plus}</div>
<img class="logo" src="file://{logo}"><div class="num">{s['num']}</div>
<div class="kicker">{s['kicker']}</div><div class="title">{title}</div>
<div class="outline">{s['outline']}</div><div class="body">{s['body']}</div>{cta}
<div class="footer">@lamusicschool</div><div class="stripes"></div>
</div></body></html>'''

for idx,s in enumerate(slides,1): (out/f'slide-{idx:02d}.html').write_text(html_for(s),encoding='utf-8')
chromium=shutil.which('chromium') or '/usr/local/bin/chromium'
for idx in range(1,8):
    subprocess.run([chromium,'--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--hide-scrollbars','--window-size=1080,1440',f'--screenshot={out/f"la-school-tdah-v3-{idx:02d}.png"}',(out/f'slide-{idx:02d}.html').as_uri()],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
imgs=[Image.open(out/f'la-school-tdah-v3-{i:02d}.png').convert('RGB') for i in range(1,8)]
thumbs=[ImageOps.contain(im,(270,360)) for im in imgs]
canvas=Image.new('RGB',(1080,720),(18,18,18))
for i,t in enumerate(thumbs): canvas.paste(t,((i%4)*270,(i//4)*360))
canvas.save(out/'preview-grid.jpg',quality=92)
copy='''# Carrossel — TDAH, concentração e disciplina\n\nFormato: 7 lâminas 1080x1440 — LA Music School\n\n1. FOCO TAMBÉM SE ENSAIA — Escutar. Esperar. Entrar no tempo certo.\n2. UM ALVO POR VEZ — Instrumento, tempo, trecho. Uma tarefa clara por rodada.\n3. A BATIDA ORGANIZA O CORPO — Contar e esperar também é treino de autocontrole.\n4. ROTINA NÃO É CASTIGO — Pequenas repetições. Correção certa. Progresso visível.\n5. ATENÇÃO VIRA PRESENÇA — No palco, foco vira atitude — mesmo com emoção e plateia.\n6. NÃO É TRATAMENTO. É PRÁTICA. — Para pessoas com TDAH, música pode apoiar foco, escuta e disciplina — quando necessário, junto do acompanhamento profissional adequado.\n7. CONCENTRAÇÃO COM DIREÇÃO — Aula com método, escuta e desafio real. CTA: LINK NA BIO.\n\nObservação ética: sem promessa terapêutica; linguagem de apoio/desenvolvimento.\n'''
(out/'CARROSSEL_COMPLETO.md').write_text(copy,encoding='utf-8')
print(out)
