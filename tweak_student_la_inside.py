from pathlib import Path
p=Path('/root/.openclaw/workspace/render_student_photo_school_post_v2.py')
s=p.read_text()
# Bring bottom-right solo LA slightly inward and make it a bit more visible, keeping it ghosted.
s=s.replace("right:-210px;bottom:105px;width:460px;height:460px;z-index:6;opacity:.16", "right:-145px;bottom:112px;width:460px;height:460px;z-index:6;opacity:.22")
p.write_text(s)
