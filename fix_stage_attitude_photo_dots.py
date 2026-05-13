from pathlib import Path
p=Path('/root/.openclaw/workspace/render_stage_attitude_carousel.py')
s=p.read_text()
# Add stronger, intentional halftone dots on the three main photo cards.
s=s.replace(".halftone.lightdots{background-image:radial-gradient(circle,var(--pink) 1.9px,transparent 3px);opacity:.25;mask-image:linear-gradient(to bottom,black 0%,transparent 70%);-webkit-mask-image:linear-gradient(to bottom,black 0%,transparent 70%)}",
".halftone.lightdots{background-image:radial-gradient(circle,var(--pink) 1.9px,transparent 3px);opacity:.25;mask-image:linear-gradient(to bottom,black 0%,transparent 70%);-webkit-mask-image:linear-gradient(to bottom,black 0%,transparent 70%)}.photoDots{position:absolute;inset:0;z-index:5;pointer-events:none;background-image:radial-gradient(circle,var(--pink) 2.4px,transparent 3.5px);background-size:20px 20px;opacity:.62;mix-blend-mode:screen}.photoDots.left{mask-image:linear-gradient(to right,black 0%,black 18%,transparent 48%);-webkit-mask-image:linear-gradient(to right,black 0%,black 18%,transparent 48%)}.photoDots.topLeft{mask-image:radial-gradient(ellipse at top left,black 0%,black 24%,transparent 57%);-webkit-mask-image:radial-gradient(ellipse at top left,black 0%,black 24%,transparent 57%)}.photoDots.rightEdge{mask-image:linear-gradient(to left,black 0%,black 15%,transparent 45%);-webkit-mask-image:linear-gradient(to left,black 0%,black 15%,transparent 45%)}")
# Card 1: capa with singer photo, dots on upper-left/left side
s=s.replace("<div class='halftone left'></div><div class='halftone'></div><div class='pluses'", "<div class='halftone left'></div><div class='photoDots topLeft'></div><div class='pluses'")
# Card 2: posture/rehearsal photo, dots on right edge/background
s=s.replace("<div class='halftone'></div><div class='pluses' style='opacity:.75;right:70px;top:260px;bottom:auto'>", "<div class='halftone'></div><div class='photoDots rightEdge'></div><div class='pluses' style='opacity:.75;right:70px;top:260px;bottom:auto'>")
# Card 4: mic close photo, dots on left edge, away from face/mic
s=s.replace("<div class='halftone left'></div><div class='pluses' style='opacity:.45;right:68px;top:245px;bottom:auto'>", "<div class='halftone left'></div><div class='photoDots left'></div><div class='pluses' style='opacity:.45;right:68px;top:245px;bottom:auto'>")
# Card 6 also has photo, but user asked three photos; add subtle dots because it is a photo card too, without overdoing it.
s=s.replace("<div class='overlay pinkwash'></div><div class='halftone'></div><div class='logo'><img src='assets/logo-dark.svg'></div><div class='call'>", "<div class='overlay pinkwash'></div><div class='halftone'></div><div class='photoDots left' style='opacity:.36'></div><div class='logo'><img src='assets/logo-dark.svg'></div><div class='call'>")
p.write_text(s)
