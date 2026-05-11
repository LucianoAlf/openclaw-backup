from pathlib import Path
p=Path('outputs/la-kids-aulas-em-turma-v3-LAHQ/carousel.html')
s=p.read_text()
# bigger handle, clearer script
s=s.replace('font-size:25px;padding:13px 24px', 'font-size:32px;padding:16px 30px')
s=s.replace('font-size:92px;line-height:.88;', 'font-size:82px;line-height:.95;')
s=s.replace('também se aprende', 'aproxima')
s=s.replace('também ensinam', 'ensinam')
s=s.replace('não é só pra gente grande', 'pra pequenos')
s=s.replace(".cta .script{color:var(--blue);font-size:98px}", ".cta .script{color:var(--blue);font-size:86px}")
p.write_text(s)
print('v3.2 legibility')
