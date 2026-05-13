from pathlib import Path
import re
text=Path('/root/.openclaw/media/inbound/la-music-design-system---8b287cb8-bb46-484d-9b31-127d7e6c2011.html').read_text(errors='ignore')
for m in re.finditer(r'<img\b[^>]*>', text, flags=re.I):
    tag=m.group(0)
    src=re.search(r'src=["\']([^"\']+)', tag)
    alt=re.search(r'alt=["\']([^"\']+)', tag)
    print('IMG', (alt.group(1) if alt else ''), (src.group(1)[:160] if src else ''))
print('svg count', len(re.findall(r'<svg\b', text, flags=re.I)))
style=re.search(r'<style>([\s\S]*?)</style>', text, flags=re.I).group(1)
for key in ['.post-demo','.post-logo','.post-footer-v2','.footer-pill','.post-halftone','.post-watermark','.post-title-pink','.post-chevrons','.post-pluses','.theme-card','.elem-card','.logo-card','.wave-bar']:
    print('\n---',key,'---')
    found=False
    for m in re.finditer(re.escape(key)+r'[^\{]*\{[^\}]*\}', style):
        found=True
        print(m.group(0)[:2000])
    if not found: print('not found')
