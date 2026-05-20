from pathlib import Path
from PIL import Image
import subprocess
p=Path('render_carousel.py')
s=p.read_text()
s=s.replace("font-size:36px; line-height:1.13; color:#EDEDED;", "font-size:40px; line-height:1.12; color:#FFFFFF; text-shadow:0 4px 18px rgba(0,0,0,.75);")
s=s.replace("color:#373435; }}", "color:#373435; text-shadow:none; }}")
s=s.replace("linear-gradient(180deg,rgba(0,0,0,.24),rgba(0,0,0,.68) 58%,rgba(0,0,0,.92))", "linear-gradient(180deg,rgba(0,0,0,.34),rgba(0,0,0,.76) 56%,rgba(0,0,0,.94))")
s=s.replace("font-size:110px;", "font-size:124px;")
s=s.replace("opacity:.9; z-index:18;", "opacity:1; z-index:18;")
s=s.replace("font-size:27px;", "font-size:30px;")
p.write_text(s)
subprocess.run(['python3','render_carousel.py'], check=True)
for i in range(1,9):
    html=f'slide-{i:02d}.html'; png=f'slide-{i:02d}.png'
    subprocess.run(['/usr/local/bin/chromium','--headless=new','--no-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files','--window-size=1080,1440',f'--screenshot={png}',f'file://{Path.cwd()/html}'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
imgs=[Image.open(f'slide-{i:02d}.png').convert('RGB') for i in range(1,9)]
grid=Image.new('RGB',(1080,720),(20,20,20))
for idx,im in enumerate(imgs):
    t=im.resize((270,360), Image.LANCZOS)
    grid.paste(t,((idx%4)*270,(idx//4)*360))
grid.save('preview-grid.png', quality=95)
subprocess.run(['tar','-czf','carrossel-aulas-em-grupo-school.tar.gz',* [f'slide-{i:02d}.png' for i in range(1,9)], 'preview-grid.png', *[f'slide-{i:02d}.html' for i in range(1,9)], 'render_carousel.py'], check=True)
