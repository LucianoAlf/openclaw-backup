# WhatsApp Duplicidade — Hardening

**Data:** 2026-05-05

## Problema observado
Mensagens operacionais chegaram duplicadas no WhatsApp durante testes manuais.

## Contexto técnico observado
- gateway WhatsApp oscilando repetidamente com `status 499`
- testes manuais disparados em sequência
- crons usando `delivery.mode=announce` no WhatsApp

## Hipóteses mais prováveis
1. reexecução manual em janela curta
2. duplicidade por reconnect do gateway
3. fluxo com announce + resposta explícita concorrendo semanticamente

## Regra operacional nova
Durante testes de crons no WhatsApp:
- evitar múltiplos disparos manuais do mesmo cron em sequência curta
- validar cada saída antes de forçar novo run
- tratar duplicidade de teste como risco conhecido enquanto o gateway estiver oscilando

## Leitura honesta
Até aqui, o principal sinal aponta mais para duplicidade de execução/transporte em ambiente instável do que para problema de conteúdo do cron em si.

## Próxima camada ideal
Se a duplicidade reaparecer sem novo disparo manual, aí precisa investigar camada mais funda de idempotência/entrega do runtime/gateway.
