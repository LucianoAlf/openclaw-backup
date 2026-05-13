from pathlib import Path
p=Path('/root/.openclaw/workspace/render_static_stage_attitude_post.py')
s=p.read_text()
# Put logo back as a small corner signature; bottom already has @ footer component.
s=s.replace(".logo{position:absolute;bottom:118px;left:0;right:0;display:flex;justify-content:center;z-index:20}.logo img{height:64px;max-width:310px;filter:drop-shadow(0 6px 14px rgba(0,0,0,.9))}", ".logo{position:absolute;top:42px;left:54px;right:auto;display:flex;justify-content:flex-start;z-index:20}.logo img{height:58px;max-width:280px;filter:drop-shadow(0 6px 14px rgba(0,0,0,.85))}")
s=s.replace("bottom:250px;z-index:10", "bottom:168px;z-index:10")
s=s.replace(".footer{position:absolute;bottom:34px;", ".footer{position:absolute;bottom:48px;")
p.write_text(s)
