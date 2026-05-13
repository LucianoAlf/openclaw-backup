from pathlib import Path
p=Path('/root/.openclaw/workspace/render_student_photo_school_post.py')
s=p.read_text()
s=s.replace("font-size:31px;line-height:1.15", "font-size:29px;line-height:1.15")
s=s.replace("background:rgba(0,0,0,.34);border-left:5px solid var(--pink);padding:14px 18px 16px", "background:rgba(0,0,0,.22);border-left:4px solid var(--pink);padding:12px 17px 14px")
p.write_text(s)
