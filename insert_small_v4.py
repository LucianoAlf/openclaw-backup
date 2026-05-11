from pathlib import Path
p=Path('outputs/la-kids-aulas-em-turma-v4-LAHQ/carousel.html')
s=p.read_text()
s=s.replace("<div class='num'>03/06</div>", "<div class='turma small'><img src='assets/turma-kids.png'></div><div class='num'>03/06</div>")
s=s.replace("<div class='num'>05/06</div>", "<div class='turma small'><img src='assets/turma-kids.png'></div><div class='num'>05/06</div>")
p.write_text(s)
print('inserted small photos')
