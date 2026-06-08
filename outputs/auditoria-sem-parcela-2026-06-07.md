# Auditoria cruzada SELECT-only — ativos com `status_pagamento = sem_parcela`

Data: 2026-06-07
Executor: Alfredo
Escopo: banco LA Performance Report/Supabase, sem UPDATE.

## Resultado executivo

Foram encontrados **28 alunos ativos** com `status_pagamento = 'sem_parcela'` no banco.

Distribuição:

| Unidade | Contrato vigente | Contrato vencido | Contrato nulo |
|---|---:|---:|---:|
| Barra | 1 | 0 | 0 |
| Campo Grande | 1 | 0 | 10 |
| Recreio | 9 | 4 | 3 |

Ponto principal: **não é seguro tratar `sem_parcela` como passaporte/evasão automaticamente**. Muitos casos têm contrato vigente, presença recente, banda/bolsa ou evidência externa de aluno ativo.

## Achados críticos

1. **UPDATE automático deve continuar bloqueado.**
   - `movimentacoes_admin` sozinha gerou falso positivo em Olavo.
   - Giane tem movimentação por nome vinculada a outro `aluno_id` (`mov_aluno_id = 1026`), não ao ID 1723.

2. **`sem_parcela` está misturando categorias diferentes:**
   - banda/projeto com valor zero;
   - bolsistas integrais/parciais;
   - alunos regulares ativos com presença recente;
   - contratos vigentes;
   - contratos vencidos mas com renovação/presença;
   - possíveis cadastros órfãos.

3. **Tabela `historico_pagamentos` não ajudou nesses 28.**
   - Todos os casos regulares auditados vieram sem histórico de pagamento nessa tabela.
   - Ou seja: a evidência financeira precisa vir de Emusys/API/tabela externa/sync, não desse histórico.

4. **Presença/aulas contradizem várias suspeitas de evasão.**
   - Davi: 23 registros, 12 presenças, última aula 2026-06-03.
   - Giane: 2 registros, 2 presenças, última aula 2026-06-03.
   - Bento: 21 registros, 14 presenças, última aula 2026-06-06.
   - Beatriz: 21 registros, 18 presenças, última aula 2026-06-06.
   - João Miguel: 25 registros, 15 presenças, última aula 2026-05-28.

## Casos que NÃO devem ser corrigidos por status agora

- **Olavo Pereira Wood (337 / CG):** Emusys print mostrou ativo/em andamento, contrato vigente e 12 pagas. Banco tem `nao_renovacao`, mas isso é divergência/falso positivo.
- **Davi do Nascimento Alexandre da Gama Mello (483 / Recreio):** Report/Emusys mostram ativo; banco tem presença recente. Problema é contrato/status_pagamento desatualizado no Report, não evasão.
- **Giane Apoliana (1723 / Recreio):** contrato vigente até 2027-01-06 e presença em 2026-06-03. Movimentação de evasão veio por nome e aponta para `aluno_id = 1026`, não ID 1723. Precisa validar no Emusys.

## Lista nominal resumida — regulares com `sem_parcela` e `conta_como_pagante = true`

### Campo Grande

| ID | Aluno | Contrato | Valor | Mov/presença | Classificação atual |
|---:|---|---|---:|---|---|
| 191 | João Miguel da Cunha Alves Ferreira | Nulo | 399 | renovação; presença 2026-05-28 | validar Emusys; provável ativo/benefício/sync |
| 220 | Laura Andrade da Silveira | Nulo | 347 | sem mov; só ausências até 2026-03-30 | investigar prioridade |
| 269 | Manuela Lourenço Ribeiro | Nulo | 347 | presença 2026-06-01 | não mexer; ativa provável |
| 337 | Olavo Pereira Wood | Nulo no Report | 337 | `nao_renovacao`; sem presença no banco, mas Emusys ativo | falso positivo; não mexer |
| 358 | Priscila Amaro da Silva | Nulo | 347 | renovação; presença 2026-05-26 | validar Emusys |

### Recreio

| ID | Aluno | Contrato | Valor | Mov/presença | Classificação atual |
|---:|---|---|---:|---|---|
| 445 | Beatriz Souto Machado | Nulo | 445,50 | presença 2026-06-06 | ativa provável; sync financeiro |
| 450 | Bento Vieira Sindeaux | Nulo | 460 | presença 2026-06-06 | ativa provável; não é trial órfão pelo banco |
| 422 | Agatha Sampaio Mendes dos Santos | Vencido 2026-05-25 | 423,50 | renovação; presença 2026-06-01 | contrato/status desatualizado |
| 483 | Davi do nascimento Alexandre da Gama Mello | Vencido 2025-04-26 | 459 | renovação; presença 2026-06-03; Emusys ativo | sync contrato/status, não evasão |
| 549 | Isabela Ferreira Moura | Vencido 2024-02-24 | 365,15 | renovação; presença 2026-06-06 | sync contrato/status |
| 684 | Sofia Lima de Castro | Vencido 2025-04-29 | 385 | renovação; presença 2026-06-02 | sync contrato/status |
| 1723 | Giane Apoliana Albino de Oliveira | Vigente 2027-01-06 | 357 | presença 2026-06-03; evasão por nome em outro ID | validar Emusys; não mexer |
| 1676 | Luciana Lima de Moura | Vigente 2027-02-20 | 385 | presença 2026-06-06 | ativa provável; recente |

## Bandas/bolsistas com `sem_parcela`

Esses casos não são bug automático: tipo de matrícula já não conta como pagante/ticket.

- Banda: 6 casos (Barra/Recreio), todos `conta_como_pagante=false`.
- Bolsista integral/parcial: 9 casos, `conta_como_pagante=false`.

## SQLs/artefatos

Arquivos gerados:
- `outputs/auditoria-sem-parcela-2026-06-07.raw.jsonlog`
- `outputs/auditoria-sem-parcela-deep2-2026-06-07.raw.jsonlog`
- script: `tmp_audit_sem_parcela.cjs`
- script: `tmp_audit_sem_parcela_deep2.cjs`

## Recomendação

1. **Não executar UPDATE de `status`, `status_pagamento` ou `tipo_matricula_id` agora.**
2. Corrigir o fluxo de auditoria: cruzar `alunos.status_pagamento`, contrato, presença e Emusys antes de propor correção.
3. Investigar sync Emusys → LA Report para:
   - status_pagamento;
   - contrato vigente/renovações;
   - vínculo correto de movimentações por `aluno_id`/`emusys_matricula_id`, não por nome.
4. Próxima validação manual por unidade deve focar só nos regulares com `conta_como_pagante=true`, não em banda/bolsista.
