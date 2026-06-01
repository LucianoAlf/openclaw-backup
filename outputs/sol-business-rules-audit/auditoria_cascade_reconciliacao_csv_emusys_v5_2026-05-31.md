# Auditoria Alfredo — Cascade reconciliação CSV Emusys v5

Data: 2026-05-31
Arquivo auditado: `/root/.openclaw/media/inbound/AUDITORIA_REGLA_KPI_CG_MAIO2026---6ca33b7b-d53d-49c2-ba86-e72dbab2c45f.md`
Prints: `image_2026-05-31_20-00-49---26939aa1...png` e `---4b21db32...png`

## Veredito

A revisão com CSV avançou, mas a matemática continua errada. Não aprovar migration.

## Conferência read-only independente

Consulta via Supabase REST + CSV `relatorio_exportado_39`, sem SQL/RPC/update.

Snapshot CG/Maio pós-saneamento, sem Plínio:

- pessoas ativas: 498
- linhas/matrículas ativas: 563
- linhas banda: 41
- pessoas com `bool_or(conta_como_pagante=true)`: 475
- pessoas com `bool_or(conta_como_pagante=true AND valor_parcela > 0)`: 464

Logo, a base `valor_parcela > 0` NÃO é 474. É 464.

## Lista completa — flag pagante sem valor positivo

Foram encontrados 11 casos com `conta_como_pagante=true`, mas sem nenhuma linha com `valor_parcela > 0` no LA Report:

### CSV positivo — pagante real no Emusys

- Ana Clara Lima Santos Pinto — Emusys 447
- Anna Clara de Souza Iorio Sales — match CSV “Anna Clara de Souza Iorio Sales Silva” — Emusys 447
- Sofia Elaile da Silva Campos — Emusys 447
- Sofia Lauermann Silva — Emusys 447
- Sarah Christina Mendes Silva — Emusys 447
- Valkiria Carvalho Baeta — Emusys 447

Total: 6 positivos.

### CSV zero — falso pagante

- Carlos Eduardo Garcia do Nascimento — Emusys 0
- Miguel Gomes Biancamano — Emusys 0
- Matheus Reis da Silva Gaspar — Emusys 0
- Marcos da Silva Saturnino — match CSV “Marcos (Marquinhos) da Silva Saturnino” — Emusys 0

Total: 4 falsos.

### Sem match exato

- Bruna Damasceno De Castro — sem match no CSV ativo export_39.

## Correção do cálculo

O relatório Cascade diz:

- base `valor_parcela > 0`: 474
- +5 positivos CSV
- = 479

Isso está errado por dois motivos:

1. Base real `conta_como_pagante=true AND valor_parcela > 0` por pessoa é 464, não 474.
2. Positivos CSV são 6, não 5, porque Anna Clara de Souza Iorio Sales aparece no CSV como Anna Clara de Souza Iorio Sales Silva.

Cálculo corrigido mínimo:

- 464 base real
- +6 positivos CSV
- = 470 pagantes reais confirmados

Se Bruna for validada como pagante real, sobe para 471. Se não, fica 470.

Outra forma equivalente:

- 475 pessoas por flag `conta_como_pagante=true`
- remover 4 falsos confirmados CSV 0
- remover/validar Bruna sem match
- resultado confirmado = 470 ou 471, não 479.

## Implicação

O ADM 475 pode estar simplesmente contando a flag `conta_como_pagante=true`, incluindo falsos pagantes. Mas a regra de pagante real reconciliada aponta para 470/471, salvo novos dados financeiros.

## Próximo prompt necessário

Pedir ao Cascade para corrigir a base da query 1b, incluir Anna e Marcos, tratar Bruna como pendência, e recalcular sem usar 474 como base da regra `valor_parcela > 0`.
