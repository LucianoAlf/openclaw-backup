# Auditoria Alfredo — Cascade KPI pessoa v4

Data: 2026-05-31
Arquivos auditados:
- `/root/.openclaw/media/inbound/AUDITORIA_REGLA_KPI_CG_MAIO2026---e7ceb725-0a21-4997-a624-0f00c350ff79.md`
- `/root/.openclaw/media/inbound/AUDITORIA_REGLA_KPI_CG_MAIO2026---efeb6e45-9d2c-4d61-b0ed-47620aad0f3c.sql`
- screenshot `image_2026-05-31_19-56-19---0287437a-a1e7-4046-838a-7f2361908789.png`

## Veredito

A versão v4 corrigiu quase toda a estrutura conceitual, mas ainda NÃO está aprovada para migration.

## Correções bem-feitas

- Markdown seção 3 agora inclui exclusão explícita de Plínio.
- Carlos Eduardo passou a ser tratado como falso pagante / pendência, não como explicação validada.
- Arthur foi corretamente limitado a explicar view antiga vs view atual, não CSV atual.
- Removido “cache” como explicação final; agora pede diff nominal.
- Pseudocódigo removeu `valor_parcela > 0` do `snapshot_linhas`.
- Regra final agora fala em evidência financeira positiva/reconciliação Emusys.
- SQL 1c/1d virou ledger por pessoa com `GROUP BY nome` + `string_agg`.

## Bloqueador novo: número 474 da query 1b não fecha

Executei conferência read-only via Supabase REST, sem SQL write/RPC/update. Resultado atual do snapshot CG/Maio pós-saneamento:

- linhas ativas válidas sem Plínio: 563
- pessoas ativas válidas sem Plínio: 498
- matrículas banda: 41
- pessoas com `bool_or(conta_como_pagante=true)`: 475
- pessoas com `bool_or(conta_como_pagante=true AND valor_parcela > 0)`: 464
- linhas com `conta_como_pagante=true AND valor_parcela > 0`: 488

Logo, a afirmação do relatório de que a query 1b (`valor_parcela > 0`) retorna 474 pagantes é inconsistente com o banco atual. Parece que o número 474 da view foi reaproveitado como se fosse resultado da query 1b.

## Anomalias que explicam a diferença

Pessoas com `conta_como_pagante=true`, mas sem nenhuma linha pagante com `valor_parcela > 0` no LA Report:

- Ana Clara Lima Santos Pinto — LR valor NULL; Emusys 447
- Anna Clara de Souza Iorio Sales — LR valor 0; Emusys 447 (match CSV como Anna Clara de Souza Iorio Sales Silva)
- Carlos Eduardo Garcia do Nascimento — LR valor 0/NULL; Emusys 0
- Bruna Damasceno De Castro — LR valor 0; sem match exato no CSV ativo
- Sofia Elaile da Silva Campos — LR valor NULL; Emusys 447
- Miguel Gomes Biancamano — LR valor 0/NULL; Emusys 0
- Sofia Lauermann Silva — LR valor NULL; Emusys 447
- Matheus Reis da Silva Gaspar — LR valor 0; Emusys 0
- Marcos da Silva Saturnino — LR valor 0; CSV match Marcos/Marquinhos 0
- Sarah Christina Mendes Silva — LR valor 0; Emusys 447
- Valkiria Carvalho Baeta — LR valor NULL; Emusys 447

Isso confirma que `valor_parcela > 0` não fecha a regra e que a contagem real exige reconciliação nominal com CSV/financeiro.

## Próximo passo obrigatório

Cascade deve rodar/entregar ledger de reconciliação dos 11 casos acima, separando:

1. pagante real por CSV positivo;
2. falso pagante por CSV 0;
3. sem match / validação manual;
4. impacto líquido na contagem de pagantes.

Também precisa explicar por que reportou 474 para query 1b se a regra `conta_como_pagante=true AND valor_parcela > 0` dá 464 pessoas no banco atual.

## Bloqueio mantido

- sem migration;
- sem RPC;
- sem backfill;
- sem Barra/Recreio;
- sem alterar `recalcular_dados_mensais`.
