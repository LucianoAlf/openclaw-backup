from pathlib import Path
p=Path('/root/.openclaw/workspace/render_drummer_carousel_real_photos.py')
s=p.read_text()
# Global readability
s=s.replace("font-size:34px;line-height:1.13", "font-size:39px;line-height:1.10")
s=s.replace("font-size:22px;font-weight:900;letter-spacing:3px", "font-size:25px;font-weight:900;letter-spacing:3px")
s=s.replace(".tag{display:inline-block;margin-top:24px", ".tag{display:inline-block;margin-top:20px")
s=s.replace("font-size:28px;text-transform:uppercase", "font-size:32px;text-transform:uppercase")
s=s.replace("padding:18px 30px", "padding:20px 36px")
# Improve photo brightness but not blow highlights
s=s.replace("filter:contrast(1.1) saturate(1.12)", "filter:contrast(1.08) saturate(1.13) brightness(1.10)")
# Reduce dark overlays a touch
s=s.replace("rgba(0,0,0,.88)),linear-gradient", "rgba(0,0,0,.80)),linear-gradient")
s=s.replace("rgba(0,0,0,.9))", "rgba(0,0,0,.84))")
s=s.replace("rgba(0,0,0,.88),rgba(0,0,0,.35)", "rgba(0,0,0,.80),rgba(0,0,0,.30)")
# Make card 4 text area cleaner via stronger left overlay but brighter subject retained
s=s.replace("<div class='photo p3'><img src='assets/photo3.jpg'></div><div class='shade left'></div>", "<div class='photo p3'><img src='assets/photo3.jpg'></div><div class='shade left' style='background:linear-gradient(90deg,rgba(0,0,0,.86),rgba(0,0,0,.48) 44%,rgba(0,0,0,.12)),linear-gradient(180deg,rgba(0,0,0,.45),rgba(0,0,0,.04) 35%,rgba(0,0,0,.78))'></div>")
# Card 6: move text up/left a bit and simplify title size to breathe
s=s.replace("<div class='content leftText lower'><div class='kicker'>04 · palco</div><h2 class='small'>LUZ ACESA.<br>BAQUETAS<br><span class='pinkword'>NO ALTO.</span></h2>", "<div class='content leftText lower' style='bottom:235px'><div class='kicker'>04 · palco</div><h2 class='small' style='font-size:70px'>LUZ ACESA.<br>BAQUETAS<br><span class='pinkword'>NO ALTO.</span></h2>")
# Card 7: push text slightly right/up away from sticks, larger support
s=s.replace("<div class='content right mid'><div class='kicker'>05 · chamado</div>", "<div class='content right mid' style='top:190px;right:50px;width:570px'><div class='kicker'>05 · chamado</div>")
# CTA footer/handle more breathing: slightly higher CTA content? keep
p.write_text(s)
