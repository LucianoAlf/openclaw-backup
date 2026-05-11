from pathlib import Path
p=Path('outputs/la-kids-aula-em-turma-v2/carousel.html')
s=p.read_text()
s=s.replace('.b4{background:white;width:170px;height:160px;left:150px;top:210px;opacity:.95}', '.b4{background:var(--verde);width:120px;height:115px;left:160px;top:205px;opacity:.55}')
s=s.replace('font-size:38px;font-weight:800', 'font-size:44px;font-weight:800')
p.write_text(s)
print('fixed')
