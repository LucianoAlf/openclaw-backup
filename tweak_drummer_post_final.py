from pathlib import Path
p=Path('/root/.openclaw/workspace/render_drummer_real_photo_school_post.py')
s=p.read_text()
s=s.replace("left:-185px;bottom:170px;width:560px;height:560px;z-index:6;opacity:.18", "left:-230px;bottom:155px;width:560px;height:560px;z-index:6;opacity:.13")
s=s.replace("bottom:42px", "bottom:50px")
s=s.replace("rgba(0,0,0,.82) 100%", "rgba(0,0,0,.78) 100%")
p.write_text(s)
