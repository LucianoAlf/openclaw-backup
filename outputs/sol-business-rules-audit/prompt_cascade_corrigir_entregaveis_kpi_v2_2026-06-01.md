Cascade, conferimos os entregáveis `MIGRACAO_REGLA_KPI_V2.sql`, `VALIDACAO_KPI_CG_MAIO2026.sql`, `AUDITORIA_SOL_INCONSISTENCIAS.sql` e `RELATORIO_TECNICO_REGLAS_KPI.md`.

O pacote está no caminho certo, mas ainda NÃO está aprovado para aplicar. Corrija os pontos abaixo e devolva uma V3.

NÃO executar nada em produção.
NÃO rodar RPC.
NÃO aplicar migration.
NÃO rodar backfill.
Gerar somente arquivos corrigidos para nova auditoria.

## 1. Corrigir exemplo errado do Carlos Eduardo no relatório

O relatório diz:

> Carlos Eduardo tem Permuta (R$0, não pagante) + Canto (R$300, pagante). Conta 1 pagante.

Isso está errado.

Validação do Alf:
- Carlos Eduardo é permuta/parceria.
- Foi corrigido como Bolsista Integral nos dois cursos.
- Não deve contar como pagante.

Remover esse exemplo ou substituir por um caso legítimo, como Barbara Ribeiro:
- banda/projeto + Home Studio pagante;
- conta como 1 pessoa pagante, não 2.

## 2. Reescrever VALIDACAO_KPI_CG_MAIO2026.sql sem comandos psql

O arquivo usa:

```sql
\set unidade_id ...
\set ano ...
\set mes ...
:unidade_id
:ano
:mes
```

Isso não roda no SQL Editor do Supabase.

Trocar por CTE literal:

```sql
WITH params AS (
  SELECT
    '2ec861f6-023f-4d7b-9927-3960ad8c2a92'::uuid AS unidade_id,
    2026::int AS ano,
    5::int AS mes,
    DATE '2026-05-01' AS inicio_mes,
    DATE '2026-05-31' AS fim_mes
)
```

O SQL final precisa ser SELECT-only e colável direto no Supabase SQL Editor.

## 3. Remover `\echo` do arquivo da Sol

`AUDITORIA_SOL_INCONSISTENCIAS.sql` usa comandos `\echo`, que também são psql-only.

Remover todos.
Se quiser identificar blocos, usar coluna `query_label` nos SELECTs.

## 4. Separar DDL da Sol de queries read-only

O arquivo diz read-only, mas contém:

```sql
DROP VIEW IF EXISTS vw_auditoria_inconsistencias;
CREATE OR REPLACE VIEW ...
```

Isso altera schema.

Separar em dois arquivos:

1. `CREATE_VIEW_AUDITORIA_SOL_V3.sql`
   - contém `CREATE OR REPLACE VIEW`;
   - exige aprovação.

2. `QUERIES_AUDITORIA_SOL_READONLY_V3.sql`
   - apenas SELECTs;
   - sem DROP, sem CREATE, sem UPDATE, sem DELETE.

## 5. Corrigir A1 da auditoria da Sol

A1 diz “ativo/pagante com valor zerado”, mas hoje pega qualquer ativo zerado:

```sql
WHERE sa.valor_parcela IS NULL OR sa.valor_parcela = 0
```

Isso gera muito ruído, porque pega banda, bolsista, permuta etc.

Criar alertas separados:

### A1_PAGANTE_SEM_VALOR

```sql
WHERE sa.conta_como_pagante = true
  AND (sa.valor_parcela IS NULL OR sa.valor_parcela = 0)
```

### A1B_NAO_PAGANTE_ZERADO_INFO

Bolsistas, banda, permuta e não pagantes zerados devem ser informativos, não erro crítico.

## 6. Corrigir A4 segundo curso zerado

A4 atual mistura banda/projeto de novo.

Trocar para:

```sql
WHERE sa.is_segundo_curso = true
  AND COALESCE(sa.is_projeto_banda,false)=false
  AND (sa.valor_parcela IS NULL OR sa.valor_parcela = 0)
```

Banda/projeto deve ter alerta próprio separado, se necessário.

## 7. Melhorar regra de duplicidade por nome

A3 hoje marca qualquer nome repetido como duplicidade. Isso pega casos legítimos de:
- curso + segundo curso;
- curso + banda;
- curso + Power Kids.

Classificar duplicidade por severidade:

- ALTA: duas ou mais linhas não-banda e não-segundo-curso na mesma unidade.
- MÉDIA: duas linhas do mesmo curso para a mesma pessoa.
- BAIXA/INFO: curso principal + banda/projeto ou segundo curso legítimo.

Não tratar toda repetição de nome como sujeira.

## 8. Não tratar ticket médio como resolvido sem bater com o card atual

A view atual CG/Maio retorna aproximadamente:

- `ticket_medio = 385.59`

O relatório fala 386/manual, mas a migration altera a fórmula para média da soma por pessoa. Essa fórmula precisa ser validada antes de entrar no patch.

Opções:

A) manter a regra atual de ticket médio e corrigir apenas alunos/matrículas; ou
B) entregar SQL comparando fórmula antiga vs nova e explicar a diferença nominal.

Recomendação: agora não mexer no ticket médio, a menos que a fórmula bata com o card validado.

## 9. Evitar `DROP VIEW` em `vw_kpis_gestao_mensal`

A migration faz:

```sql
DROP VIEW IF EXISTS vw_kpis_gestao_mensal;
CREATE OR REPLACE VIEW ...
```

Preferir:

```sql
CREATE OR REPLACE VIEW vw_kpis_gestao_mensal AS ...
```

Sem DROP, salvo se houver justificativa e mapa de dependências.

## 10. Padronizar regra de `alunos_ativos` entre view e função

Na função:

```sql
COUNT(DISTINCT a.nome)
```

Na view:

```sql
COUNT(DISTINCT sb.nome) FILTER (WHERE sb.is_segundo_curso IS NULL OR sb.is_segundo_curso = false)
```

Padronizar.

Se a regra canônica for “pessoa distinta no snapshot”, usar a mesma nos dois.
Se for “base principal exclui segundo curso”, documentar explicitamente e criar alerta para pessoa que só aparece como segundo curso.

## 11. Definir explicitamente novas_matriculas

A regra atual de novas matrículas não filtra status.

Decidir e documentar:

- Se `novas_matriculas` é evento comercial, pode contar matrícula aberta no mês mesmo que status mude depois, mas precisa fonte/evento.
- Se é snapshot operacional, deve filtrar `status IN ('ativo','trancado')`.

Para CG/Maio o esperado continua 23.

## Entregáveis V3 esperados

1. `MIGRACAO_REGLA_KPI_V3.sql`
2. `VALIDACAO_KPI_CG_MAIO2026_V3.sql` colável no Supabase SQL Editor
3. `CREATE_VIEW_AUDITORIA_SOL_V3.sql`
4. `QUERIES_AUDITORIA_SOL_READONLY_V3.sql`
5. `RELATORIO_TECNICO_REGRAS_KPI_V3.md`

Resultado esperado CG/Maio:

- ativos = 496
- pagantes = 470
- matrículas = 561
- banda = 41
- segundo curso operacional = 27
- novas = 23
- evasões = 13
- churn = 2,77%

Não aplicar nada. Devolver para nova auditoria.
