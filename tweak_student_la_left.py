from pathlib import Path
p=Path('/root/.openclaw/workspace/render_student_photo_school_post_v2.py')
s=p.read_text()
old=".laSolo{position:absolute;right:-145px;bottom:112px;width:460px;height:460px;z-index:6;opacity:.22;filter:drop-shadow(0 10px 24px rgba(0,0,0,.25));pointer-events:none}.laSolo img{width:100%;height:100%;object-fit:contain}"
new=".laSolo{position:absolute;left:-135px;bottom:118px;width:500px;height:500px;z-index:6;opacity:.22;filter:drop-shadow(0 10px 24px rgba(0,0,0,.25));pointer-events:none;transform:rotate(-10deg)}.laSolo img{width:100%;height:100%;object-fit:contain}"
s=s.replace(old,new)
p.write_text(s)
