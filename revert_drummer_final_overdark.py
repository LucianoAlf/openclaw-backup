from pathlib import Path
p=Path('/root/.openclaw/workspace/render_drummer_carousel_real_photos.py')
s=p.read_text()
# Revert final over-dark local overlays; keep v2 readability.
s=s.replace("text-shadow:0 7px 20px rgba(0,0,0,1),0 0 5px rgba(0,0,0,1)", "text-shadow:0 6px 18px rgba(0,0,0,1),0 0 3px rgba(0,0,0,1)")
s=s.replace(".footer{position:absolute;bottom:58px;", ".footer{position:absolute;bottom:48px;")
s=s.replace("<div style='position:absolute;left:0;top:120px;width:680px;height:760px;z-index:5;background:linear-gradient(90deg,rgba(0,0,0,.48),rgba(0,0,0,.18),transparent);pointer-events:none'></div><div class='content leftText mid'><div class='kicker'>03 · foco</div>", "<div class='content leftText mid'><div class='kicker'>03 · foco</div>")
s=s.replace("<div class='photo p2'><img src='assets/photo2.jpg'></div><div class='shade'></div><div class='glow'></div><div style='position:absolute;inset:0;z-index:3;background:radial-gradient(ellipse at 37% 43%,rgba(255,230,230,.12),transparent 24%);mix-blend-mode:screen;pointer-events:none'></div>", "<div class='photo p2'><img src='assets/photo2.jpg'></div><div class='shade'></div><div class='glow'></div>")
s=s.replace("<div class='photo p4'><img src='assets/photo4.jpg'></div><div class='shade'></div><div class='glow'></div><div style='position:absolute;inset:0;z-index:3;background:radial-gradient(ellipse at 45% 36%,rgba(255,230,230,.13),transparent 24%);mix-blend-mode:screen;pointer-events:none'></div>", "<div class='photo p4'><img src='assets/photo4.jpg'></div><div class='shade'></div><div class='glow'></div>")
p.write_text(s)
