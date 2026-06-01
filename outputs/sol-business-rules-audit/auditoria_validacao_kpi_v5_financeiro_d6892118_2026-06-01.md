# Auditoria — VALIDACAO_KPI_CG_MAIO2026_V5_FINANCEIRO d6892118

Data: 2026-06-01
Arquivo: `/root/.openclaw/media/inbound/VALIDACAO_KPI_CG_MAIO2026_V5_FINANCEIRO---d6892118-d966-4499-9c93-7f0fb2a02893.sql`

## Veredito

**Aprovado para rodar como SELECT-only / sanity check financeiro inicial.**

**Não aprova migration financeira ainda.**

O arquivo está seguro para SQL Editor porque não tem DDL/DML executável.

## Checagem estática

- Sem `CREATE`, `DROP`, `ALTER` executável.
- Sem `INSERT`, `UPDATE`, `DELETE` executável.
- Sem `\set`, `\echo`, `:param`.
- 1 `WITH` + 1 `SELECT` principal.
- Não escreve em `dados_mensais`.

## Pontos corretos

- Defende `ticket_medio = MRR / alunos_pagantes`.
- Calcula MRR por soma de `valor_parcela` em linhas pagantes.
- Calcula inadimplência por valor, não por cabeça.
- Separa faturamento previsto e realizado.
- Trata `valor_parcela NULL/0` em pagante como alerta bloqueante.
- Mantém financeiro como validação nominal antes de persistir.

## Ressalvas técnicas

### 1. É um sanity check, não validação nominal completa

O arquivo retorna o resumo financeiro e o número de alertas, mas não entrega automaticamente a lista nominal, porque os detalhamentos estão comentados.

Além disso, se descomentar `SELECT * FROM alertas_parcela;` no final, não funciona isoladamente porque CTE só existe no SELECT imediatamente seguinte.

Correção recomendada: criar SELECTs separados, cada um com seu próprio `WITH`, ou deixar os detalhamentos ativos no mesmo arquivo.

### 2. MRR filtra `valor_parcela > 0`

Isso é aceitável como cálculo provisório se o próprio arquivo bloquear quando há pagantes NULL/0. Mas é importante: se houver alertas, o MRR/ticket exibido não deve ser considerado final.

### 3. Não filtra `status_pagamento = 'sem_parcela'`

O arquivo soma linhas pagantes positivas mesmo que `status_pagamento='sem_parcela'`. A versão mais robusta deve excluir:

```sql
AND COALESCE(status_pagamento, '') <> 'sem_parcela'
```

### 4. `unidade_cg` pode retornar mais de uma linha

Provável que não aconteça, mas tecnicamente seria melhor usar `ORDER BY` + `LIMIT 1` ou validar quantidade de unidades encontradas.

### 5. Ticket usa faixa 380–395

Serve como alerta rápido, mas aprovação final precisa comparação nominal contra o card R$386 e contra ADM/Emusys.

## Conclusão

Pode rodar agora como leitura para obter primeira foto financeira.

Se retornar:

- ticket dentro da faixa;
- zero alertas de parcela;
- MRR coerente com ADM/Emusys;

então o próximo passo é rodar uma validação nominal detalhada antes de qualquer migration.

Se retornar qualquer alerta de `valor_parcela NULL/0`, a migration financeira continua bloqueada.
