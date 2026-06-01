# Auditoria Alfredo — Windsurf v4 saneamento ciclo de vida CG/Maio

Data: 2026-05-31
Arquivos auditados:
- `SIMULACAO_SANEAMENTO_CG---73e81c3d-cc27-480a-ae26-d58dd10df54c.sql`
- `UPDATES-COM-GUARDS_Campo_Grande_Maio_2026-V3---79ae6e3a-3552-4ba4-9b42-228a4dee300b.sql`
- `RelatórioFinal-v4_SaneamentoCiclodeVida_Simulação---92f8c331-9f4e-47df-876c-c2703b352169.md`

## Veredito

**Aprovável com escopo limitado.**

A v4 está tecnicamente aceitável para:
1. rodar a simulação read-only;
2. executar somente o bloco de saneamento de ciclo de vida Campo Grande/Maio 2026, após aprovação explícita do Alf.

**Não aprovar ainda:**
- patch/alteração de `recalcular_dados_mensais`, porque o SQL/migration dessa alteração não veio neste pacote;
- execução da RPC `recalcular_dados_mensais(...)` antes de auditar/aplicar a correção da função;
- backfill Jan–Abr;
- Barra/Recreio.

## Evidências conferidas

### 1) Simulação v4
- Sem DDL: não há `DROP`, `CREATE`, `ALTER`, `INSERT`, `UPDATE`, `DELETE` ou `TRUNCATE` no arquivo de simulação.
- Parêntese do `no_snapshot_virt` foi corrigido.
- Removeu filtro perigoso `curso_id IS NOT NULL`.
- Mantém Giovanna id 1619 no snapshot apesar de `curso_id=NULL`.
- Arthur id 47 mantém `data_saida='2026-01-09'` na lógica virtual.

### 2) Update v4
- O SQL de update está comentado; rodar como está não altera nada. Para executar, precisa descomentar o bloco `DO $$ ... END $$;`.
- Usa `WITH updated AS (UPDATE ... RETURNING id)` + `SELECT COUNT(*) INTO v_count FROM updated`, corrigindo o erro do `ROW_COUNT` da v3.
- Updates limitados à unidade Campo Grande `2ec861f6-023f-4d7b-9927-3960ad8c2a92`.
- Não insere `movimentacoes_admin`.
- Não chama RPC.
- Não faz backfill.
- Não mexe em Barra/Recreio.

### 3) Guards conferidos no banco atual
Checagem read-only via REST confirmou que todos os guards atuais batem:

| Grupo | Esperado | Encontrado |
|---|---:|---:|
| A | 16 | 16 |
| B | 1 | 1 |
| C | 5 | 5 |
| D | 2 | 2 |
| E | 2 | 2 |

### 4) Simulação independente Alfredo
Resultado reproduzido sobre o estado atual do banco:

| Cenário | alunos_ativos | alunos_pagantes | matriculas_ativas | matriculas_banda |
|---|---:|---:|---:|---:|
| Atual | 515 | 485 | 582 | 45 |
| Após correções A–E | 500 | 474 | 567 | 43 |
| Após correções + excluir projeto/banda de ativos/pagantes | 495 | 473 | 567 | 43 |

Bate com o relatório v4.

## Ressalva de texto no relatório

A seção 7 do relatório diz “7 alunos com `is_projeto_banda=true`”. Isso está impreciso: existem 43 matrículas de banda/projeto no snapshot pós-correção. Os 7 listados são casos especiais/afetados/relevantes para a reconciliação, não a totalidade de `matriculas_banda`.

Isso **não bloqueia o update de saneamento**, porque o SQL e os números agregados estão corretos. Mas antes de transformar em documentação canônica, ajustar a redação para evitar confusão.

## Aprovação recomendada para Alf

Aprovação segura e limitada:

> Aprovo executar somente o saneamento de ciclo de vida Campo Grande/Maio 2026 da v4: primeiro rodar a simulação read-only; depois descomentar e executar o bloco `DO $$` do update v4. Não executar `recalcular_dados_mensais`, não aplicar patch de função, não fazer backfill, não rodar Barra/Recreio.

Após o update:
1. validar os 26 registros alterados;
2. rodar novamente a simulação read-only;
3. só então pedir/avaliar a migration de `recalcular_dados_mensais` com a regra `COALESCE(c.is_projeto_banda,false)=false` em ativos/pagantes.
