# Auditoria dos entregáveis Windsurf/Cascade — KPI v2 CG/Maio 2026

Data: 2026-06-01
Status: **NÃO APROVAR AINDA**

Arquivos auditados:
- `MIGRACAO_REGLA_KPI_V2---d2a9afc1-1d33-4301-9586-e821c268a216.sql`
- `VALIDACAO_KPI_CG_MAIO2026---710526eb-2c9d-4079-99eb-a343cc3cedba.sql`
- `AUDITORIA_SOL_INCONSISTENCIAS---2ae65a1c-1167-4582-bcba-e4a2dd8624ae.sql`
- `RELATORIO_TECNICO_REGLAS_KPI---b973b709-8eed-444d-993d-dd6ccc726d68.md`

## Veredito

O pacote está **bem encaminhado**, mas ainda não pode ser aplicado.

Ele acerta a separação principal:

- pessoas vs linhas;
- banda/projeto separado de segundo curso;
- `matriculas_2_curso` operacional = 27;
- `matriculas_banda` = 41;
- `recalcular_dados_mensais` preserva assinatura e não tenta persistir colunas geradas.

Mas existem erros conceituais e técnicos que precisam voltar para o Cascade antes de executar qualquer migration.

---

## Pontos OK

1. **Segundo curso operacional foi corrigido**
   - Regra correta: `is_segundo_curso=true AND COALESCE(cursos.is_projeto_banda,false)=false`.
   - Evita o erro dos 65 brutos.
   - Esperado CG/Maio: 27.

2. **Banda/projeto ficou separada**
   - Regra: `cursos.is_projeto_banda=true`.
   - Esperado CG/Maio: 41.

3. **Snapshot base está no caminho certo**
   - `status IN ('ativo','trancado')`
   - `data_matricula <= fim_mes`
   - `data_saida IS NULL OR data_saida > fim_mes`

4. **Função preserva assinatura**
   - `recalcular_dados_mensais(p_ano integer, p_mes integer, p_unidade_id uuid)`
   - `SECURITY DEFINER` mantido.

5. **Colunas geradas não são persistidas**
   - `faturamento_estimado` e `saldo_liquido` não aparecem no INSERT/UPDATE.

---

## Bloqueadores antes de aplicar

### 1. Relatório técnico usa exemplo errado do Carlos Eduardo

No relatório, o Cascade escreveu:

> “Carlos Eduardo tem Permuta (R$0, não pagante) + Canto (R$300, pagante). Conta 1 pagante.”

Isso está **errado**.

Validação do Alf:

- Carlos Eduardo é permuta/parceria.
- Foi corrigido como **Bolsista Integral nos dois cursos**.
- Não deve contar como pagante.

Correção necessária:

- Trocar o exemplo por Barbara Ribeiro, que é caso legítimo de pessoa com curso de banda + curso pagante.
- Ou remover exemplo nominal.

---

### 2. Validation SQL usa comandos de psql, não roda no SQL Editor do Supabase

Arquivo `VALIDACAO_KPI_CG_MAIO2026.sql` usa:

```sql
\set unidade_id ...
\set ano ...
\set mes ...
:unidade_id
:ano
:mes
```

Isso funciona em `psql`, mas **não funciona no SQL Editor do Supabase** nem via maioria dos runners.

Correção necessária:

- Reescrever `params` com valores literais dentro do CTE:

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

---

### 3. `AUDITORIA_SOL_INCONSISTENCIAS.sql` também usa `\echo`

O arquivo de auditoria da Sol usa comandos `\echo`, que também são específicos de `psql`.

Correção necessária:

- Remover `\echo`.
- Transformar cada query em SELECT puro com uma coluna `query_label`.

---

### 4. A view da Sol não é read-only se executada como está

O arquivo diz “read-only”, mas contém:

```sql
DROP VIEW IF EXISTS vw_auditoria_inconsistencias;
CREATE OR REPLACE VIEW vw_auditoria_inconsistencias AS ...
```

Isso não altera dados de alunos, mas **altera schema**.

Correção necessária:

- Separar em dois arquivos:
  1. `CREATE_VIEW_AUDITORIA_SOL.sql` — DDL, exige aprovação.
  2. `QUERIES_AUDITORIA_SOL_READONLY.sql` — SELECT-only, pode rodar para inspeção.

---

### 5. A1 da auditoria da Sol está amplo demais e vai gerar ruído

Comentário diz “ativo/pagante com valor zerado”, mas o WHERE atual é:

```sql
WHERE sa.valor_parcela IS NULL OR sa.valor_parcela = 0
```

Isso pega **todo mundo zerado**, incluindo:

- banda/projeto legítimo;
- bolsista integral;
- bolsista parcial;
- segundo curso legítimo zerado;
- outros casos que não são necessariamente erro.

No estado atual de CG/Maio, esse critério bruto retorna 62 linhas, mas apenas parte delas é problema real.

Correção necessária:

Separar alertas:

- `PAGANTE_SEM_VALOR`: `conta_como_pagante=true AND valor_parcela IS NULL/0`.
- `NAO_PAGANTE_ZERADO_INFO`: bolsistas/banda/permuta etc. apenas informativo.
- `PASSAPORTE_MENSALIDADE_FUTURA`: precisa de fonte financeira/fatura para não confundir Sofia Elaile/Sofia Lauermann.

---

### 6. A4 “Segundo curso zerado” mistura banda de novo

A4 atual:

```sql
WHERE sa.is_segundo_curso = true
  AND (sa.valor_parcela IS NULL OR sa.valor_parcela = 0)
```

Isso volta a misturar banda/projeto com segundo curso.

Correção necessária:

```sql
WHERE sa.is_segundo_curso = true
  AND COALESCE(sa.is_projeto_banda,false)=false
  AND (sa.valor_parcela IS NULL OR sa.valor_parcela = 0)
```

Banda/projeto deve ter alerta separado, se necessário.

---

### 7. Duplicidade por nome está ingênua demais

A3 marca qualquer nome repetido como duplicidade.

Isso vai pegar casos legítimos:

- aluno com curso principal + segundo curso;
- aluno com curso + banda;
- aluno com curso + Power Kids;
- aluno com variações operacionais corretas.

Correção necessária:

Classificar duplicidades por severidade:

- **ALTA:** duas linhas não-banda, não-segundo-curso, mesmo nome/unidade.
- **MÉDIA:** mesma pessoa com duas linhas do mesmo curso.
- **BAIXA/INFO:** curso principal + banda/projeto ou segundo curso legítimo.

---

### 8. Ticket médio não está validado

O relatório diz ticket médio esperado 386/manual.

A migration calcula ticket como média da soma das parcelas por pessoa usando `entra_ticket_medio=true`.

Em consulta read-only, essa regra não bate exatamente com o valor atual da view/card:

- view atual CG/Maio: `ticket_medio = 385.59`.
- regra SQL-like do patch tende a dar aproximadamente `384.76` para CG/Maio, dependendo do tratamento de NULL.

Correção necessária:

- Não tratar ticket médio como resolvido nesse pacote.
- Ou alinhar fórmula explicitamente com a fórmula atual validada do card.
- Se ticket médio não for foco agora, manter regra atual e mexer só nos KPIs de alunos/matrículas.

---

### 9. `DROP VIEW IF EXISTS vw_kpis_gestao_mensal` é arriscado

A migration faz:

```sql
DROP VIEW IF EXISTS vw_kpis_gestao_mensal;
CREATE OR REPLACE VIEW vw_kpis_gestao_mensal AS ...
```

Riscos:

- quebrar dependências;
- perder grants/comentários;
- falhar se houver objetos dependentes;
- gerar downtime desnecessário.

Correção necessária:

- Preferir `CREATE OR REPLACE VIEW` direto, preservando assinatura/colunas.
- Se precisar drop, mapear dependências antes e justificar.

---

### 10. `alunos_ativos` está inconsistente entre view e função

Na função, alunos ativos é:

```sql
COUNT(DISTINCT a.nome)
```

Na view, está:

```sql
COUNT(DISTINCT sb.nome) FILTER (WHERE sb.is_segundo_curso IS NULL OR sb.is_segundo_curso = false)
```

Hoje CG/Maio fecha igual, mas a regra não está idêntica.

Correção necessária:

- Padronizar uma única regra.
- Se a regra for “pessoa distinta no snapshot”, não precisa filtrar segundo curso.
- Se a regra for “base principal”, documentar explicitamente e tratar casos segundo-curso-only como inconsistência.

---

### 11. `novas_matriculas` não filtra status

A regra usa data e `data_saida`, mas não exige `status IN ('ativo','trancado')` nem define se cancelados no próprio mês entram.

Pode estar ok, mas precisa decisão explícita.

Correção necessária:

- Documentar se novas matrículas contam evento comercial mesmo que aluno já tenha saído.
- Se for snapshot operacional, filtrar status.
- Se for evento comercial, usar fonte/evento próprio e não misturar com snapshot.

---

## Prompt de correção para Cascade

Ver arquivo:

`outputs/sol-business-rules-audit/prompt_cascade_corrigir_entregaveis_kpi_v2_2026-06-01.md`
