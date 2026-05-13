from pathlib import Path
import re, html
from collections import Counter
p=Path('/root/.openclaw/media/inbound/la-music-design-system---8b287cb8-bb46-484d-9b31-127d7e6c2011.html')
text=p.read_text(errors='ignore')
body=re.sub(r'<style[\s\S]*?</style>','',text,flags=re.I)
body=re.sub(r'<script[\s\S]*?</script>','',body,flags=re.I)
print('--- headings ---')
for m in re.finditer(r'<(h[1-6])[^>]*>([\s\S]*?)</\1>', body, flags=re.I):
    s=re.sub('<[^>]+>',' ',m.group(2)); s=html.unescape(re.sub(r'\s+',' ',s)).strip()
    print(m.group(1), s)
print('\n--- visible text excerpt ---')
vis=re.sub(r'<[^>]+>','\n',body)
vis=html.unescape(vis)
lines=[re.sub(r'\s+',' ',l).strip() for l in vis.splitlines()]
lines=[l for l in lines if l]
print('\n'.join(lines[:350]))
print('\n--- classes freq ---')
classes=[]
for m in re.finditer(r'class=["\']([^"\']+)["\']', text):
    classes += m.group(1).split()
for c,n in Counter(classes).most_common(160): print(n,c)
