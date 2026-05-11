from pathlib import Path
p=Path('outputs/la-kids-aula-em-grupo-v1/carousel.html')
s=p.read_text()
s=s.replace('.desc{font-size:39px;', '.desc{font-size:43px;')
s=s.replace(".p2,.p5{right:70px;top:250px;bottom:auto;transform:rotate(-3deg)}", ".p2{right:70px;top:250px;bottom:auto;transform:rotate(-3deg)}.p5{right:54px;top:auto;bottom:175px;transform:rotate(-3deg) scale(.92)}")
s=s.replace('.b3{width:230px;height:240px;background:var(--red);right:65px;bottom:-82px;', '.b3{width:230px;height:240px;background:var(--red);right:-92px;bottom:-96px;')
p.write_text(s)
print('adjusted')
