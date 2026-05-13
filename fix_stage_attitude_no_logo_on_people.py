from pathlib import Path
p=Path('/root/.openclaw/workspace/render_stage_attitude_carousel.py')
s=p.read_text()
# Hard rule: no giant LA watermark on photo cards with people. Replace with DS texture only.
repls = {
"<div class='wm a' style='opacity:.16;right:-330px;top:260px'><img src='assets/la-dark-solo-vazada.svg'></div>":"<div class='pluses' style='opacity:.75;right:70px;top:260px;bottom:auto'><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span></div>",
"<div class='wm c' style='opacity:.14;right:-300px;bottom:250px'><img src='assets/la-dark-solo-vazada.svg'></div>":"<div class='pluses' style='opacity:.45;right:68px;top:245px;bottom:auto'><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span><span>+</span></div>",
}
for a,b in repls.items():
    s=s.replace(a,b)
# Ensure slide 06 has no wm in photo. If any accidental remains near call, remove.
s=s.replace("<div class='wm c'><img src='assets/la-dark-solo-vazada.svg'></div>", "")
p.write_text(s)
