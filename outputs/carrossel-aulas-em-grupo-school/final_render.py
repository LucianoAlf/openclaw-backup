from pathlib import Path
from PIL import Image
import subprocess
p=Path('render_carousel.py')
s=p.read_text()
s=s.replace('-webkit-text-stroke:2.6px #fff;', '-webkit-text-stroke:4px #fff; text-shadow:0 8px 26px rgba(0,0,0,.75);')
s=s.replace('-webkit-text-stroke:2.6px #0A0A0A;', '-webkit-text-stroke:4px #0A0A0A; text-shadow:none;')
p.write_text(s)
subprocess.run(['python3','render_carousel.py'], check=True)
for i in range(1,9):
    subprocess.run(['/usr/local/bin/chromium','--headless=new','--no-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files','--window-size=1080,1440',f'--screenshot=slide-{i:02d}.png',f'file://{Path.cwd()/f"slide-{i:02d}.html"}'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
imgs=[Image.open(f'slide-{i:02d}.png').convert('RGB') for i in range(1,9)]
grid=Image.new('RGB',(1080,720),(20,20,20))
for idx,im in enumerate(imgs):
    grid.paste(im.resize((270,360), Image.LANCZOS),((idx%4)*270,(idx//4)*360))
grid.save('preview-grid.png', quality=95)
subprocess.run(['tar','-czf','carrossel-aulas-em-grupo-school.tar.gz',*[f'slide-{i:02d}.png' for i in range(1,9)],'preview-grid.png',*[f'slide-{i:02d}.html' for i in range(1,9)],'render_carousel.py'], check=True)
