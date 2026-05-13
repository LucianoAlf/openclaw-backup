from pathlib import Path
p=Path('/root/.openclaw/workspace/render_student_photo_school_post_v2.py')
s=p.read_text()
s=s.replace("right:-118px;bottom:116px;width:430px;height:430px;z-index:6;opacity:.33", "right:-185px;bottom:92px;width:470px;height:470px;z-index:6;opacity:.22")
s=s.replace("max-width:500px;font-size:33px;line-height:1.12;font-weight:700;color:#fff;text-shadow:0 6px 18px rgba(0,0,0,.96)", "max-width:520px;font-size:34px;line-height:1.12;font-weight:700;color:#fff;text-shadow:0 6px 18px rgba(0,0,0,1),0 0 3px rgba(0,0,0,1)")
s=s.replace(".footer{position:absolute;bottom:46px;", ".footer{position:absolute;bottom:42px;")
s=s.replace(".stripes{display:flex;gap:8px;margin-top:14px}", ".stripes{display:flex;gap:8px;margin-top:12px}")
p.write_text(s)
