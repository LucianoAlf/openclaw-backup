from pathlib import Path
p=Path('/root/.openclaw/workspace/render_student_photo_school_post_v2.py')
s=p.read_text()
s=s.replace("top:46px;right:56px", "top:56px;right:62px")
s=s.replace("height:68px;max-width:320px", "height:64px;max-width:300px")
s=s.replace("right:-215px;bottom:96px;width:500px;height:500px;z-index:6;opacity:.18", "right:-210px;bottom:105px;width:460px;height:460px;z-index:6;opacity:.16")
s=s.replace(".sub{margin-top:28px;", ".sub{margin-top:22px;")
p.write_text(s)
