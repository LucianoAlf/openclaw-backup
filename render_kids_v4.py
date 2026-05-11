from pathlib import Path
import re, subprocess
out=Path('/root/.openclaw/workspace/outputs/la-kids-aulas-em-turma-v4-LAHQ')
html=(out/'carousel.html').read_text()
style=re.search(r'<style>(.*?)</style>', html, re.S).group(1)
sections=re.findall(r"<section class='slide.*?</section>", html, re.S)
(out/'png').mkdir(exist_ok=True)
for i,sec in enumerate(sections,1):
    solo=f"<!doctype html><html><head><meta charset='utf-8'><style>{style}\nbody{{background:white}}.deck{{display:block;padding:0}}.slide{{margin:0}}</style></head><body><div class='deck'>{sec}</div></body></html>"
    p=out/f'slide-{i:02d}.html'; p.write_text(solo)
    png=out/'png'/f'la-kids-aulas-em-turma-v4-{i:02d}.png'
    subprocess.run(['chromium','--headless','--no-sandbox','--disable-gpu','--hide-scrollbars','--window-size=1080,1350',f'--screenshot={png}',p.as_uri()],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
from PIL import Image, ImageDraw
imgs=[]
for p in sorted((out/'png').glob('*.png')):
    im=Image.open(p).convert('RGB'); im.thumbnail((216,270))
    can=Image.new('RGB',(230,300),'white'); can.paste(im,((230-im.width)//2,8)); ImageDraw.Draw(can).text((8,282),p.name[-6:-4],fill=(0,0,0)); imgs.append(can)
sheet=Image.new('RGB',(690,600),(238,238,238))
for idx,im in enumerate(imgs): sheet.paste(im,((idx%3)*230,(idx//3)*300))
sheet.save(out/'preview-grid.jpg',quality=92)
print('rendered',len(imgs),out/'preview-grid.jpg')
