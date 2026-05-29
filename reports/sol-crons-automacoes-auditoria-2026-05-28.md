# Auditoria — Crons e automações da Sol

Data: 2026-05-28
Host: `lahq` / `89.116.73.186`

## Escopo

Auditoria sem alteração dos crons/automações, exceto tentativa manual de iniciar worker para confirmar estado.

## Crontab root

Encontrado:

```cron
*/5 * * * * /usr/bin/flock -n /tmp/la-dispatcher.lock /bin/bash -c 'cd /opt/LA-Organizer && /usr/bin/node src/rituals/dispatcher.js' >> /opt/LA-Organizer/logs/rituals.log 2>&1 # tom-rituals
0 6 * * * /opt/LA-Organizer/backup.sh >/dev/null 2>>/opt/LA-Organizer/logs/backup.log
0 6 * * * /opt/backups/la-organizer/backup-secrets.sh
```

Leitura:
- Esses jobs são do LA-Organizer/Tom/backup geral, não da Sol diretamente.
- O dispatcher roda a cada 5 minutos e merece auditoria separada, porque pode acionar rituais/automações fora da Sol.

## Crontab usuário `sol`

Encontrado:

```cron
0 21 * * * /home/sol/.openclaw/workspace/scripts/run-backup-with-status.sh >/dev/null 2>&1
@reboot /home/sol/.openclaw/workspace/scripts/start-lareport-sol-worker.sh
```

Leitura:
- Backup diário da Sol às 21:00 UTC.
- Worker BI da Sol inicia apenas no boot (`@reboot`).
- Não há cron de monitoramento/restart do worker se ele cair.

## OpenClaw cron

Comando `openclaw cron list` no ambiente da Sol retornou:

```text
No cron jobs.
```

Leitura:
- As rotinas descritas no `HEARTBEAT.md` não estão cadastradas como cron OpenClaw.
- `HEARTBEAT.md` é documentação/intenção, não execução ativa no momento.

## Timers systemd

Apenas timers padrão do sistema: apt, logrotate, sysstat, fstrim etc.
Sem timer próprio da Sol.

## Backup Sol

Status em `memory/backup-status.json`:

- último backup: `2026-05-27T21:00:01Z` → `2026-05-27T21:00:07Z`
- exit code: `0`
- push GitHub: `ok`
- arquivo: `/home/sol/backups/sol-adm/2026-05-27/sol-adm-20260527T210001Z.tar.gz`

Observação: o script inclui `.env` real do LA-Organizer no tarball. Alf já tratou como backup privado/risco controlado, mas saneamento futuro recomendado.

## Worker BI / LAReport

Script:

- `/home/sol/.openclaw/workspace/scripts/start-lareport-sol-worker.sh`
- `/home/sol/.openclaw/workspace/scripts/lareport-sol-worker.js`

Estado auditado:
- Após restart do gateway, worker não estava rodando.
- Tentativa manual de iniciar worker mostrou processo subir, registrar `Sol LAReport worker starting`, depois cair após `realtime TIMED_OUT`.
- Logs recentes:
  - `2026-05-28T15:52:51Z` worker starting → `15:53:01Z realtime TIMED_OUT`
  - `2026-05-28T15:59:21Z` worker starting → `15:59:31Z realtime TIMED_OUT`
  - `2026-05-28T16:51:30Z` worker starting → `16:51:40Z realtime TIMED_OUT`

Causa provável:
- O worker usa `setInterval(pollPending, FALLBACK_POLL_MS).unref()` e `setTimeout(pollPending, 3000).unref()`.
- Se o realtime não mantém o processo vivo quando dá timeout, o Node encerra.
- Como só existe `@reboot`, ele não volta sozinho.

Risco:
- Fila BI `bi_messages_lamusic` pode parar de ser processada se realtime falhar no startup.
- O fallback poll existe no código, mas por estar `unref()` pode não segurar o processo vivo.

## Processos automáticos ativos relevantes

- OpenClaw Sol gateway ativo na porta `19790`.
- Mike OpenClaw e Chrome headless ativos na mesma VPS, mas fora do escopo Sol.
- LA-Organizer/Tom ativo em `/opt/LA-Organizer`.
- Worker BI Sol estava caindo no startup por timeout de realtime.

## Conclusão

Antes de testar perguntas de BI/worker, precisa corrigir ou estabilizar o worker BI.

Crons da Sol estão simples:
1. backup diário;
2. worker no reboot.

Não há cron OpenClaw ativo para as rotinas de HEARTBEAT.

## Recomendações

1. Corrigir `lareport-sol-worker.js` para o fallback polling manter o processo vivo mesmo se realtime der `TIMED_OUT`.
2. Adicionar restart supervisionado para o worker: systemd service, cron watchdog, ou OpenClaw cron/tarefa controlada.
3. Auditar o dispatcher root do LA-Organizer separadamente antes de mexer em automações de operação.
4. Decidir quais rotinas do `HEARTBEAT.md` devem virar crons reais e em qual fase: dry-run, interno, externo aprovado.
5. Testar Sol com perguntas conversacionais depois; testar BI só após worker estável.
