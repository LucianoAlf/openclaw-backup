from pathlib import Path
p=Path('outputs/la-kids-aulas-em-turma-v4-LAHQ/carousel.html')
s=p.read_text()
# make pagination unmistakable
s=s.replace('font-size:30px;font-weight:900', 'font-size:44px;font-weight:900')
# improve script readability and wording
s=s.replace('font-size:88px;line-height:.95;', 'font-size:76px;line-height:1.02;')
s=s.replace('juntar crianças', 'tem bagunça')
s=s.replace('mais presença', 'presença')
s=s.replace('pra gente grande', 'pros pequenos')
# add small group photo cards to solid slides 03 and 05
s=s.replace("<section class='slide solid-red'>", "<section class='slide solid-red has-small-photo'>", 1)
s=s.replace("<section class='slide solid-blue'>", "<section class='slide solid-blue has-small-photo'>", 1)
s=s.replace('.solid-red h1{max-width:840px}', ".solid-red h1{max-width:700px}.has-small-photo .turma.small{display:block;position:absolute;right:55px;bottom:135px;width:360px;height:370px;border-radius:70px 35px 75px 40px;transform:rotate(4deg);z-index:9}")
s=s.replace("{turma}{button}<div class='num'", "{turma}{'<div class=\'turma small\'><img src=\'assets/turma-kids.png\'></div>' if kind in ['solid-red','solid-blue'] else ''}{button}<div class='num'")
p.write_text(s)
print('fixed v4')
