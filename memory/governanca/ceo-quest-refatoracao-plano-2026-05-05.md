# CEO Quest — Plano de Refatoração Matinal

**Data:** 2026-05-05
**Status:** aprovado para execução em camadas

## Objetivo
Refatorar o CEO Quest matinal para sair do modelo de 3 reinos fixos e migrar para um modelo mais aderente ao uso real do Alf, centrado no TickTick, backlog vivo, ação CEO do dia e performance no jogo.

## Novo modelo matinal alvo
1. Streak
2. Hoje no tabuleiro
3. Pendência viva
4. Ação CEO do dia
5. Próxima ação
6. Leitura curta de performance

## Princípios
- TickTick como fonte operacional real
- memória/governança como camada interpretativa
- briefing curto, útil e ancorado no dia real
- sem reino inventado
- sem narrativa bonita vazia
- WhatsApp como canal principal do briefing matinal
- scorecard/painel podem continuar usando reinos como leitura estratégica posterior

## Execução por camadas

### Camada 1 — Documentação central
Atualizar:
- `ceo-quest-prd.md`
- `ceo-quest-skill.md`
- `ceo-quest-ticktick-map.md`

Mudanças principais:
- tirar reinos fixos do centro do briefing matinal
- manter reinos como camada estratégica / scorecard / painel
- formalizar novo template matinal
- formalizar WhatsApp como canal principal do briefing diário do jogo

### Camada 2 — Arquitetura operacional
Ajustar lógica de runtime para:
- briefing matinal ir para WhatsApp
- deixar de usar o tópico 218 como cockpit principal da manhã
- manter Telegram apenas onde fizer sentido estratégico/futuro
- preservar risk-check e close-day enquanto a migração do cockpit é avaliada

### Camada 3 — Prompt e lógica do briefing
Reescrever o briefing matinal para:
- olhar o que é hoje
- olhar o que ficou pendente/atrasado
- olhar o que foi planejado na semana
- definir ação CEO do dia
- apontar próxima ação
- fazer leitura curta da performance

### Camada 4 — Registro e versionamento
- registrar auditoria/refatoração em memória
- atualizar sessão do dia
- commit
- push

### Camada 5 — Teste real
- disparo manual do briefing refatorado
- entrega no WhatsApp
- validação do texto
- ajuste fino se necessário

## Regra de execução
Não pular camada.
Executar nesta ordem:
1. docs
2. arquitetura/prompt
3. memória
4. git
5. teste

## Critério de sucesso
O briefing da manhã precisa:
- chegar no WhatsApp
- consultar TickTick de verdade
- falar do que está vivo hoje
- apontar pendência viva
- sugerir ação CEO do dia
- não usar mais reinos fixos como esqueleto obrigatório
