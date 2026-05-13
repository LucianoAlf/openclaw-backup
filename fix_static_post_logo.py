from pathlib import Path
p=Path('/root/.openclaw/workspace/render_static_stage_attitude_post.py')
s=p.read_text()
s=s.replace(".logo{position:absolute;top:52px;left:0;right:0;display:flex;justify-content:center;z-index:20}.logo img{height:82px;max-width:360px}", ".logo{position:absolute;top:42px;left:54px;right:auto;display:flex;justify-content:flex-start;z-index:20}.logo img{height:58px;max-width:280px;filter:drop-shadow(0 6px 14px rgba(0,0,0,.85))}")
s=s.replace("background:linear-gradient(180deg,rgba(0,0,0,.42) 0%,rgba(0,0,0,.02) 33%", "background:linear-gradient(180deg,rgba(0,0,0,.58) 0%,rgba(0,0,0,.05) 30%")
p.write_text(s)
