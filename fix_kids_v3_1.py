from pathlib import Path
p=Path('outputs/la-kids-aulas-em-turma-v3-LAHQ/carousel.html')
s=p.read_text()
# remove photo boxes from slides by replacing generated photo media with clean music badges/icons
s=s.replace("<div class='photoBox'><img src='assets/ref-01.jpg' style='object-position:center center'></div>", "<div class='musicBadge big'>🎤</div>")
s=s.replace("<div class='photoBox'><img src='assets/ref-05.jpg' style='object-position:center center'></div>", "<div class='musicBadge big guitar'>🎸</div>")
# keep all backgrounds warm; blue slide becomes warm with blue accents
s=s.replace(".blue{background:linear-gradient(135deg,var(--blue),#007fc9)}", ".blue{background:linear-gradient(135deg,var(--yellow),#ff9d00 48%,var(--red))}")
s=s.replace(".blue .tag{background:var(--yellow);color:var(--black)}.blue .script{color:var(--yellow)}", ".blue .tag{background:var(--blue);color:white}.blue .script{color:var(--blue);text-shadow:0 5px 0 rgba(255,255,255,.35)}.blue h1,.blue .sub{color:var(--black);text-shadow:none}")
# improve script legibility and sub copy
s=s.replace("font-size:105px;line-height:.78;", "font-size:92px;line-height:.88;")
s=s.replace(".photo h1,.photo2 h1{font-size:132px;max-width:590px}", ".photo h1,.photo2 h1{font-size:118px;max-width:720px}")
s=s.replace(".photo .sub,.photo2 .sub{max-width:500px}", ".photo .sub,.photo2 .sub{max-width:620px}")
# add clean badge css after bigIcon
s=s.replace(".bigIcon{position:absolute;right:100px;bottom:175px;z-index:7;font-size:245px;filter:drop-shadow(0 17px 0 rgba(0,0,0,.16));transform:rotate(-8deg)}", ".bigIcon{position:absolute;right:100px;bottom:175px;z-index:7;font-size:245px;filter:drop-shadow(0 17px 0 rgba(0,0,0,.16));transform:rotate(-8deg)}.musicBadge{position:absolute;right:95px;bottom:165px;z-index:7;width:360px;height:360px;border-radius:80px 45px 88px 48px;background:white;display:flex;align-items:center;justify-content:center;font-size:180px;box-shadow:0 24px 0 rgba(0,0,0,.16);transform:rotate(5deg)}.musicBadge.guitar{background:var(--blue)}")
p.write_text(s)
print('v3.1 fixed clean refs')
