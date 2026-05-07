# Auditoria SailQuest / CEO Quest + TickTick + Crons — 2026-05-07

## Diagnóstico

O problema da manhã não foi falta de disparo do cron.
Os crons rodaram, consultaram/geraram conteúdo e falharam na etapa de entrega WhatsApp.

Crons afetados:
- `510638fa-953c-4465-9e53-f5eff69c7d53` — 7h Briefing operacional pessoal
- `b7a53e03-0991-4b69-9217-8b0b430d3840` — 7h30 Pendências do dia anterior
- `21e4dbf9-2c98-4803-9ada-a0567a8d3ba3` — CEO Quest Briefing matinal

Erro visto nos runs:
- `TypeError: loaded.sendMessageWhatsApp is not a function`
- também apareceu antes `ParseError: Unexpected token` em runtime WhatsApp

## Causa técnica provável

Há mismatch de versão no runtime:
- OpenClaw core: `2026.5.4`
- Plugin WhatsApp ativo: `@openclaw/whatsapp 2026.5.6`
- O plugin declara peer dependency `openclaw >=2026.5.6`

Isso explica a falha de entrega: o gateway carrega uma interface antiga/esperada pelo core, mas o plugin instalado já está em contrato mais novo.

## TickTick

Acesso real validado via token em `.env`.
Projetos consultáveis:
- Contas Pessoais: 33 tasks
- Pessoal Alf: 2 tasks
- Trabalho Operacional: 4 tasks
- Mentorias: 2 tasks
- CEO Quest: 14 tasks
- Emusys Academy: 0 tasks

Conclusão: o TickTick não é a raiz da falha de hoje. Ele está acessível. O problema principal foi entrega/runtime WhatsApp.

## Correções aplicadas agora

### Prompts corrigidos para não induzir envio manual
Removido/neutralizado o padrão errado de instruir o agente a “Enviar explicitamente no WhatsApp”.

Agora os crons dizem:
- resposta final deve conter só o texto do Alf
- não usar ferramenta de mensagem
- não tentar enviar WhatsApp por conta própria
- OpenClaw fará a entrega via `delivery` configurado

Crons atualizados:
- 7h Briefing operacional pessoal → V3, timeout 180s, modelo `gpt-5.4-mini`
- 7h30 Pendências do dia anterior → V3, timeout 180s, modelo `gpt-5.4-mini`
- CEO Quest Briefing matinal → V3, timeout 180s, modelo `gpt-5.4-mini`
- 19h30 Fechamento operacional pessoal → V2, timeout 180s, modelo `gpt-5.4-mini`

## Ainda pendente

A correção estrutural exige alinhar versão do core/plugin WhatsApp:

Opção recomendada:
- atualizar OpenClaw core para `2026.5.6`, mantendo o plugin WhatsApp atual.

Opção alternativa:
- fazer downgrade do plugin WhatsApp para versão compatível com core `2026.5.4`.

Depois disso, rodar um teste controlado de entrega WhatsApp ponta a ponta.

## Decisão

Não executar update/downgrade sem confirmação explícita do Alf, porque mexe em componente do OpenClaw/gateway.
