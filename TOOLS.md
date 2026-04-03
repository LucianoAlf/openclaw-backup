# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### TickTick
- **Token:** salvo em `.env` como `TICKTICK_TOKEN`
- **API base:** `https://api.ticktick.com/open/v1`
- **Listas:** 📝 Notas Alf | 🏠 Pessoal Alf | 💼 Trabalho Alf | 💸 Contas Pessoais (ID: 67158c51db647de6536f46dc) | 💡 Mentorias
- **Acesso:** leitura + escrita (marcar como concluído via POST /task/{id} com status:2)
- ⚠️ Sempre checar `.env` antes de dizer que não tem acesso.

---

Add whatever helps you do your job. This is your cheat sheet.
