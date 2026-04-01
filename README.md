# 🦞 OpenClaw Backup — Guia de Restore & Deploy

> Repositório de backup automático da configuração do OpenClaw (AlfBot).
> Backup diário às 3h via Windows Task Scheduler.

---

## 📋 Visão Geral

Este repositório contém toda a configuração do agente OpenClaw rodando localmente no Windows, conectado ao Telegram via bot `@lucianoalf_bot` e usando o modelo `anthropic/claude-sonnet-4-6` via conta Claude Max.

**O que está incluído no backup:**
- `openclaw.json` — configuração principal do gateway
- `agents/` — configuração e memória dos agentes
- `credentials/` — configuração de canais (Telegram, etc.)
- `completions/` — scripts de autocompletar do shell
- `devices/` — dispositivos pareados
- `identity/` — identidade do agente
- `memory/` — memória persistente do agente
- `tasks/` — banco de dados de tarefas agendadas
- `telegram/` — configuração do canal Telegram
- `backup.ps1` — script de backup automático

**O que NÃO está incluído (por segurança):**
- Sessões ativas (`agents/main/sessions/`)
- Tokens de autenticação (`*.token`, `*.session`)
- Arquivos de log (`*.log`)
- Backups locais (`*.bak`)

---

## ✅ Pré-requisitos

Antes de fazer qualquer restore ou deploy, tenha em mãos:

### Software necessário
- [ ] **Windows 10/11** (ou Ubuntu 20.04+ para VPS)
- [ ] **Node.js v18+** → https://nodejs.org
- [ ] **Git for Windows** → https://git-scm.com *(Windows)*
- [ ] **Git** → `apt install git` *(Linux)*

### Credenciais necessárias
- [ ] **Anthropic API Key** ou **Claude setup-token** (gerado via `claude setup-token`)
- [ ] **Telegram Bot Token** do `@lucianoalf_bot` (gerado via @BotFather)
- [ ] **Credenciais do GitHub** para clonar este repo

> ⚠️ Nunca commite os valores reais dessas credenciais neste repositório.

---

## 🔄 Restore no Mesmo Windows

Use quando o OpenClaw parou de funcionar mas o PC está acessível.

```powershell
# 1. Instalar OpenClaw novamente
irm https://claude.ai/install.ps1 | iex

# 2. Adicionar ao PATH (se necessário)
# Painel de Controle → Variáveis de Ambiente → PATH → Adicionar:
# C:\Users\Texeira\.local\bin

# 3. Restaurar configurações do backup
cd C:\Users\Texeira\.openclaw
git pull origin main

# 4. Reconfigurar credenciais
openclaw configure

# 5. Reiniciar o gateway
openclaw gateway install
openclaw gateway
```

---

## 💻 Deploy em Máquina Windows Nova

Use quando está configurando um PC novo do zero.

### Passo 1 — Instalar dependências
```powershell
# Instalar Git for Windows
# Baixar em: https://git-scm.com/download/win
# Marcar "Add Git to PATH" durante instalação

# Instalar Node.js
# Baixar em: https://nodejs.org (versão LTS)
```

### Passo 2 — Instalar OpenClaw
```powershell
irm https://claude.ai/install.ps1 | iex
```

### Passo 3 — Adicionar ao PATH
```
Painel de Controle → Sistema → Configurações avançadas do sistema
→ Variáveis de Ambiente → PATH (usuário) → Novo:
C:\Users\[SEU_USUARIO]\.local\bin
```
Fechar e abrir novo PowerShell.

### Passo 4 — Clonar este repositório
```powershell
cd C:\Users\[SEU_USUARIO]
git clone https://github.com/LucianoAlf/openclaw-backup.git .openclaw
cd .openclaw
```

### Passo 5 — Configurar OpenClaw
```powershell
openclaw configure
```
Seguir o wizard:
- Model: `anthropic/claude-sonnet-4-6`
- Auth: Anthropic token (colar o setup-token gerado via `claude setup-token`)
- Channel: Telegram → colar o Bot Token do `@lucianoalf_bot`
- Web search: DuckDuckGo (sem API key)

### Passo 6 — Iniciar o Gateway
```powershell
openclaw gateway install
openclaw gateway
```

### Passo 7 — Parear no Telegram
Abrir o `@lucianoalf_bot` no Telegram e enviar `/start`.
Copiar o pairing code e rodar:
```powershell
openclaw pairing approve telegram [CODIGO]
```

### Passo 8 — Agendar backup diário
```powershell
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File C:\Users\[SEU_USUARIO]\.openclaw\backup.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At "03:00"
Register-ScheduledTask -TaskName "OpenClaw Daily Backup" -Action $action -Trigger $trigger -RunLevel Highest
```

---

## 🐧 Deploy em VPS Linux (Ubuntu 20.04+)

### Passo 1 — Conectar na VPS
```bash
ssh root@[IP_DA_VPS]
```

### Passo 2 — Instalar dependências
```bash
apt update && apt upgrade -y
apt install git curl -y

# Instalar Node.js v22
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs
```

### Passo 3 — Instalar OpenClaw
```bash
curl -sSL https://openclaw.ai/install.sh | bash
```

### Passo 4 — Clonar este repositório
```bash
cd ~
git clone https://github.com/LucianoAlf/openclaw-backup.git .openclaw
cd .openclaw
```

### Passo 5 — Configurar OpenClaw
```bash
openclaw configure
```

### Passo 6 — Iniciar como serviço
```bash
# Criar serviço systemd
cat > /etc/systemd/system/openclaw.service << EOF
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw
ExecStart=/usr/local/bin/openclaw gateway run
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable openclaw
systemctl start openclaw
```

### Passo 7 — Parear no Telegram
```bash
openclaw pairing approve telegram [CODIGO]
```

### Passo 8 — Agendar backup diário via cron
```bash
crontab -e
# Adicionar linha:
0 3 * * * cd /root/.openclaw && git add -A && git commit -m "backup: $(date '+%Y-%m-%d %H:%M:%S')" && git push origin main
```

---

## 📱 Reconectar o Telegram

Se o bot parou de responder ou foi reconfigurado:

```powershell
# Windows
openclaw gateway stop
openclaw configure  # seção Channels → Telegram → novo token se necessário
openclaw gateway install
openclaw gateway
```

No Telegram, enviar `/start` para `@lucianoalf_bot` e aprovar o novo pairing code.

---

## 🔑 Credenciais — O que Reconfigurar

Após qualquer restore, você precisará reinserir manualmente:

| Credencial | Onde obter | Onde inserir |
|---|---|---|
| Anthropic API Key | console.anthropic.com → API Keys | `openclaw configure` |
| Claude setup-token | `claude setup-token` no terminal | `openclaw configure` |
| Telegram Bot Token | @BotFather no Telegram | `openclaw configure` |
| GitHub token (para backup) | github.com → Settings → Tokens | `git remote set-url` |

> ⚠️ Esses valores nunca devem ser commitados neste repositório.

---

## 💾 Backup Manual

Para rodar o backup fora do horário agendado:

```powershell
# Windows
cd C:\Users\Texeira\.openclaw
.\backup.ps1
```

```bash
# Linux
cd ~/.openclaw
git add -A && git commit -m "backup manual: $(date)" && git push origin main
```

---

## 🔧 Troubleshooting

### Gateway não inicia
```powershell
openclaw gateway stop
openclaw gateway install
openclaw gateway
```

### Bot não responde no Telegram
```powershell
# Verificar status
openclaw status

# Reiniciar gateway
openclaw gateway restart

# Verificar logs
openclaw gateway status --deep
```

### Erro de PATH (claude não encontrado)
```powershell
# Adicionar ao PATH manualmente
[Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";C:\Users\Texeira\.local\bin", "User")
# Fechar e abrir novo PowerShell
```

### Push de backup falhou (sem credenciais Git)
```powershell
git config --global user.email "seu@email.com"
git config --global user.name "LucianoAlf"
# Usar GitHub token como senha ao fazer push
```

### OpenClaw desatualizado
```powershell
irm https://claude.ai/install.ps1 | iex  # atualiza automaticamente
```

---

## 📊 Informações do Setup Atual

| Item | Valor |
|---|---|
| Modelo | `anthropic/claude-sonnet-4-6` |
| Conta | Claude Max |
| Bot Telegram | `@lucianoalf_bot` |
| Gateway porta | `18789` |
| Workspace | `~/.openclaw/workspace` |
| Backup | Diário às 03:00 (Windows Task Scheduler) |
| Repositório | github.com/LucianoAlf/openclaw-backup (privado) |

---

*Última atualização: Abril 2026*# openclaw-backup
repositório de backup do OpenClaw AlfBot
