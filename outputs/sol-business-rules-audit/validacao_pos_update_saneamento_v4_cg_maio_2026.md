# Validação pós-update — Saneamento v4 Campo Grande / Maio 2026

Data: 2026-05-31
Status: update v4 executado e validado.

## Fonte da validação
- Print enviado pelo Alf/Windsurf confirmando execução.
- Conferência read-only Alfredo direto no Supabase via REST após execução.

## Resultado do update

26 registros alterados conforme aprovado:

| Grupo | Esperado | Resultado |
|---|---:|---:|
| A | 16 | 16 `data_saida` preenchidas |
| B | 1 | Arthur id 47 com `status='inativo'` e `data_saida='2026-01-09'` mantida |
| C | 5 | 5 `data_saida` limpas |
| D | 2 | Maria id 1450 e Ana Julia id 1378 com `data_saida='2026-05-31'` |
| E | 2 | Luciano id 945 e Alexandre id 1598 com `data_saida='2026-05-31'` |

## Validação nominal conferida no banco

- Arthur Souza Del Bosco id 47: `status='inativo'`, `data_saida='2026-01-09'`.
- Giovanna Campos Peixoto Ueoka id 1619: não alterada, `status='ativo'`, `data_saida=NULL`, `curso_id=NULL` preservado para correção cadastral posterior.
- Alexandre Dos Santos id 1598: `status='inativo'`, `data_saida='2026-05-31'`.
- Maria Eduarda de Lima Bomfim Pedro id 1450: `status='inativo'`, `data_saida='2026-05-31'`.
- Ana Julia de Oliveira Gomes id 1378: `status='inativo'`, `data_saida='2026-05-31'`.
- Grupo C reativados confirmados com `data_saida=NULL`: 31, 263, 323, 405, 949.
- Conferência automatizada retornou `validation_problems []`.

## Métricas após update

Cálculo por snapshot de data após saneamento:

| Cenário pós-update | alunos_ativos | alunos_pagantes | matriculas_ativas | matriculas_banda |
|---|---:|---:|---:|---:|
| Sem aplicar regra de exclusão banda em ativos/pagantes | 500 | 474 | 567 | 43 |
| Aplicando regra `cursos.is_projeto_banda=false` em ativos/pagantes | 495 | 473 | 567 | 43 |

## Escopo ainda bloqueado

Ainda **não aprovado**:
- atualizar/aplicar migration de `recalcular_dados_mensais`;
- executar `recalcular_dados_mensais(2026, 5, Campo Grande)`;
- backfill Jan–Abr;
- Barra/Recreio.

## Próximo passo

Auditar SQL/migration da função `recalcular_dados_mensais` para aplicar a regra:

```sql
COALESCE(c.is_projeto_banda, false) = false
```

somente em `alunos_ativos` e `alunos_pagantes`, preservando `matriculas_banda` como métrica separada.
