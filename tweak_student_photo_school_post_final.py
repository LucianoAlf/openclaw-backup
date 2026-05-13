from pathlib import Path
p=Path('/root/.openclaw/workspace/render_student_photo_school_post.py')
s=p.read_text()
s=s.replace("opacity:.46;mix-blend-mode:screen", "opacity:.34;mix-blend-mode:screen")
s=s.replace(".pinkGlow{position:absolute;inset:0;z-index:3;background:radial-gradient(ellipse at 80% 30%,rgba(233,20,81,.54),transparent 36%),radial-gradient(ellipse at 18% 72%,rgba(233,20,81,.22),transparent 30%);mix-blend-mode:screen;opacity:.65}", ".pinkGlow{position:absolute;inset:0;z-index:3;background:radial-gradient(ellipse at 80% 30%,rgba(233,20,81,.48),transparent 36%),radial-gradient(ellipse at 18% 72%,rgba(233,20,81,.20),transparent 30%);mix-blend-mode:screen;opacity:.62}.subjectLight{position:absolute;inset:0;z-index:3;background:radial-gradient(ellipse at 35% 40%,rgba(255,220,230,.16),transparent 25%);mix-blend-mode:screen;pointer-events:none}")
s=s.replace("<div class=\"pinkGlow\"></div><div class=\"halftone\"></div>", "<div class=\"pinkGlow\"></div><div class=\"subjectLight\"></div><div class=\"halftone\"></div>")
s=s.replace(".sub{margin-top:24px;margin-left:auto;max-width:440px;font-size:31px;line-height:1.15;font-weight:700;color:#fff;text-shadow:0 5px 16px rgba(0,0,0,.9)}", ".sub{margin-top:24px;margin-left:auto;max-width:440px;font-size:31px;line-height:1.15;font-weight:700;color:#fff;text-shadow:0 5px 16px rgba(0,0,0,.95);background:rgba(0,0,0,.34);border-left:5px solid var(--pink);padding:14px 18px 16px;border-radius:14px;backdrop-filter:blur(1px)}")
p.write_text(s)
