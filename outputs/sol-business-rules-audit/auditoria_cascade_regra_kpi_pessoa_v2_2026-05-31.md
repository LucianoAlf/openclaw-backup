# Auditoria Alfredo — Cascade KPI pessoa v2

Data: 2026-05-31
Arquivos auditados:
- `/root/.openclaw/media/inbound/AUDITORIA_REGLA_KPI_CG_MAIO2026---738a97f0-4544-40e7-a598-99a6e1484753.md`
- `/root/.openclaw/media/inbound/AUDITORIA_REGLA_KPI_CG_MAIO2026---5e06b7fd-86fd-4d84-af65-09276c7fc451.sql`

## Veredito

Melhorou em relação à versão anterior, mas ainda NÃO está pronto para virar regra/migration.

## Acertos

- Mantém escopo READ-ONLY.
- Reconhece que `alunos_ativos` e `alunos_pagantes` são métricas de pessoa.
- Preserva Barbara como ativa/pagante e evita filtro cego de banda.
- Reconhece Carlos Eduardo como não pagante operacional, apesar de `Segundo Curso/conta_como_pagante=true`.
- Mantém bloqueio de migration/RPC/backfill/Barra/Recreio.

## Problemas bloqueantes

### 1. Documento contradiz o SQL sobre Plínio

No SQL seção 1, Plínio é excluído. Mas no markdown da query principal a cláusula de exclusão não aparece, embora o resultado diga “sem Plínio”.

### 2. Carlos ainda aparece como “caso real de diferença”

O markdown e o comentário SQL ainda chamam Carlos Eduardo de “caso real de diferença por pessoa vs row-by-row”, mas a validação visual do Alf mostrou que ele é ativo bolsista/não pagante.

A redação correta: Carlos Eduardo é falso pagante causado por `tipo_matricula=Segundo Curso` + `conta_como_pagante=true` + valor zero.

### 3. Regra `valor_parcela > 0` não pode virar regra final isolada

Já foi verificado que existem alunos com `valor_parcela` NULL/0 no LA Report e mensalidade positiva no Emusys. Então `valor_parcela > 0` pode excluir pagantes reais.

A regra só pode ser provisória para detectar falso positivo; a regra final precisa reconciliar fonte financeira/Emusys ou corrigir os valores nulos/zero no LA Report.

### 4. Pseudocódigo filtra `valor_parcela > 0` dentro do snapshot_linhas

Isso é grave: se `snapshot_linhas` filtrar valor > 0, ele remove não pagantes e bolsistas antes de contar `alunos_ativos`, `matriculas_ativas`, `matriculas_banda` e `matriculas_2_curso`.

O filtro de pagamento deve entrar somente no cálculo de `alunos_pagantes`, nunca no snapshot base.

### 5. Ledger 1d não é ledger nominal por pessoa

A query “lista de todos os 474 pagantes reais” retorna linhas/matrículas, não pessoas agregadas. Se houver pessoa com mais de uma linha pagante, duplica.

Precisa de ledger por pessoa com `GROUP BY nome` e `string_agg` das linhas.

### 6. Explicação Arthur não fecha com CSV ativo

O relatório afirma que CSV Emusys 499 vs cálculo 498 é explicado por Arthur. Mas o CSV ativo export_39 já foi auditado com Arthur ausente. Logo Arthur não explica a diferença entre CSV ativo atual e cálculo atual.

Arthur explica diferenças de view/ADM antes do saneamento, não a divergência atual contra CSV ativo.

### 7. Plínio aparece contraditório como ativo e inativo

O documento diz que linha 1361 estava ativa indevidamente, mas a tabela 6.3 lista Plínio 1361 como status inativo. Precisa anexar resultado real do SELECT ou corrigir a narrativa.

### 8. Ainda usa “cache” como hipótese

“Cache” não deve ser aceito como explicação final para 565 vs 563. Precisa ledger nominal/diff.

## Conclusão

A direção está correta, mas ainda faltam ajustes antes de aprovar qualquer design de migration:

- corrigir contradições do relatório;
- não usar `valor_parcela > 0` como regra final isolada;
- separar snapshot base de regra de pagamento;
- gerar ledger nominal por pessoa real;
- explicar 499/475/565 nominalmente, sem cache e sem Arthur quando o CSV ativo não contém Arthur.
