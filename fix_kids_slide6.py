from pathlib import Path
import re
p=Path('outputs/la-kids-aula-em-grupo-v1/carousel.html')
s=p.read_text()
# remove only the slide 6 illustration block
s=re.sub(r"<div class='photo-card p6'>.*?<div class='staff'></div></div>", "", s, count=1, flags=re.S)
p.write_text(s)
print('slide6 illustration removed')
