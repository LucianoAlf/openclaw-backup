# Validação pós-justificativas do Alf — 5 alunos NULL/0

Data: 2026-06-01 UTC
Escopo: Campo Grande / Maio 2026
Status: READ-ONLY — nenhuma migration/RPC/backfill.

## Justificativas do Alf

- **Ana Clara Lima Santos Pinto**: está fazendo aula. No LA Report está zerada. Gabriela removeu 7 faturas dela; Alf vai perguntar à Gabi o que houve.
- **Sofia Elaile da Silva Campos**: matriculada em abril, mas não começou em maio; vai começar em junho. Provável problema financeiro/adiamento de início. Por isso está zerada no LA Report.
- **Sofia Lauermann Silva**: matriculou em maio/abril, pagou passaporte e começará em junho; primeira parcela em junho. Por isso está zerada no LA Report.
- **Sarah Christina Mendes Silva**: fazia aula normalmente; estava zerada no LA Report; Alf ajustou.
- **Valkiria Carvalho Baeta**: Alf corrigiu curso de Bateria para Canto; faz aula de Canto com Matheus, paga R$387, matriculou em abril e começou em maio.

## Estado atual no LA Report/Supabase após ajustes

| Aluno | ID | Status | Curso | Data matrícula | Início contrato | Valor parcela | Valor passaporte | Classificação operacional Maio |
|---|---:|---|---|---|---|---:|---:|---|
| Ana Clara Lima Santos Pinto | 21 | ativo | Canto | 2025-05-28 | NULL | NULL | NULL | Ativa; pagante real pendente de validar faturas removidas pela Gabi |
| Sofia Elaile da Silva Campos | 1643 | ativo | Violino | 2026-04-30 | 2026-04-30 | NULL | 325 | Matriculada/contrato criado; não iniciou/pagou mensalidade em maio segundo Alf; começa em junho |
| Sofia Lauermann Silva | 1633 | ativo | Canto | 2026-04-27 | 2026-04-28 | NULL | 500 | Matriculada com passaporte; primeira parcela em junho segundo Alf |
| Sarah Christina Mendes Silva | 1600 | ativo | Canto | 2026-04-02 | 2026-04-04 | 456.16 | NULL | Ativa e pagante em maio; corrigida no LR |
| Valkiria Carvalho Baeta | 1624 | ativo | Canto | 2026-04-22 | 2026-04-29 | 387 | 400 | Ativa e pagante em maio; curso/valor corrigidos no LR |

## Recontagem read-only atual

Após correções manuais em andamento:

- pessoas ativas sem Plínio: **497**
- matrículas ativas sem Plínio: **562**
- linhas banda: **41**
- pessoas pagantes por flag `conta_como_pagante=true`: **472**
- pessoas pagantes por `conta_como_pagante=true AND valor_parcela > 0`: **466**
- `vw_kpis_gestao_mensal`: **497 ativos / 471 pagantes / 41 banda / 65 segundo curso**

## Casos ainda sem valor positivo no LR

Atualmente restam 6 pessoas com `conta_como_pagante=true`, mas sem nenhuma linha com `valor_parcela > 0`:

1. Ana Clara Lima Santos Pinto — ativa; pendente Gabi/faturas removidas.
2. Anna Clara de Souza Iorio Sales — valor 0; precisa auditoria nominal.
3. Carlos Eduardo Garcia do Nascimento — bolsista/falso pagante confirmado.
4. Sofia Elaile da Silva Campos — início/pagamento em junho segundo Alf.
5. Sofia Lauermann Silva — início/pagamento em junho segundo Alf.
6. Marcos da Silva Saturnino — valor 0; precisa auditoria nominal/falso provável.

## Leitura crítica

O problema não é só “corrigir valor zerado”. Há pelo menos três naturezas diferentes misturadas:

1. **Erro/sincronização/fatura removida:** Ana Clara, Sarah antes do ajuste.
2. **Aluno novo/adiado para começar em junho:** Sofia Elaile, Sofia Lauermann.
3. **Falso pagante/bolsista/zero real:** Carlos, possivelmente Marcos.
4. **Correção cadastral de curso/valor:** Valkiria.
5. **Duplicidade/normalização de nome:** Bruna.

## Ponto de regra

Estamos remendando porque o banco não tem uma camada clara para competência financeira.

A regra precisa separar:

- **base ativa contratual/operacional**: aluno com matrícula/contrato ativo, ainda que pagamento comece depois;
- **pagante contratual**: aluno em tipo Regular/contrato pagante, mesmo antes da primeira parcela recorrente;
- **pagante financeiro da competência**: aluno com fatura/mensalidade positiva prevista ou paga naquele mês;
- **falso pagante cadastral**: flag pagante, mas bolsista/valor zero/fatura zero.

Sem essa separação, `valor_parcela`, `conta_como_pagante` e CSV Emusys vão continuar se contradizendo.

## Recomendação

Antes de migration:

1. fechar auditoria nominal dos 6 pendentes atuais;
2. exigir da equipe explicação da Ana Clara e faturas removidas;
3. confirmar Sofia Elaile/Sofia Lauermann como início em junho, sem contar como pagante financeiro de maio;
4. corrigir/validar Anna Clara e Marcos;
5. só depois recalcular KPI final CG/Maio;
6. criar regra estrutural: importar faturas/competências do Emusys para uma tabela de apoio, em vez de inferir financeiro por `valor_parcela`.
