from pathlib import Path
p=Path('/usr/lib/node_modules/openclaw/dist/extensions/whatsapp/runtime-api.js')
text=p.read_text()
marker = "const finalText = String(finalTextRaw || '')"
if marker not in text:
    raise SystemExit('target line not found')
lines = text.splitlines()
out = []
replaced = False
for line in lines:
    if (not replaced) and marker in line:
        indent = line.split('const finalText',1)[0]
        out.append(f"{indent}const finalText = String(finalTextRaw || '')")
        out.append(f"{indent}\t.replace(/^\\s*(Enviar no WhatsApp para\\s+\\*\\*?\\d+\\*\\*?:?|Enviar no WhatsApp para\\s+\\d+:?|Destino:\\s*WhatsApp\\s+\\*\\*?\\d+\\*\\*?:?)\\s*\\n?/gim, '')")
        out.append(f"{indent}\t.replace(/^\\s*(Need escape script\\.?|Already patched on VPS.*|patched runtime-api\\.js|RESTART_OK|RESTART_FAIL|Command exited with code \\d+.*)\\s*$/gim, '')")
        out.append(f"{indent}\t.trim();")
        replaced = True
    else:
        out.append(line)
if not replaced:
    raise SystemExit('replacement failed')
p.write_text('\n'.join(out) + '\n')
print('patched sanitizer')
