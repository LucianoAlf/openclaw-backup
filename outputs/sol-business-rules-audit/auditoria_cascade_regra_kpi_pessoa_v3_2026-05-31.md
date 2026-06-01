# Auditoria Alfredo — Cascade KPI pessoa v3

Data: 2026-05-31
Arquivos auditados:
- `/root/.openclaw/media/inbound/AUDITORIA_REGLA_KPI_CG_MAIO2026---6d4b9826-dab1-4c60-b1ef-fc267109b61a.md`
- `/root/.openclaw/media/inbound/AUDITORIA_REGLA_KPI_CG_MAIO2026---813890a7-6e2e-4e42-b7cd-c799fb542fc6.sql`

## Veredito

Parcialmente ajustado, mas ainda NÃO aprovado para migration ou regra final.

## Avanços reais

- SQL anexo corrigiu `string_agg` com `||`, casts e `COALESCE`.
- SQL anexo passou a excluir Plínio nas CTEs das seções 1, 4, 5, 6, 1b, 1c e 1d.
- SQL anexo corrigiu o título de Carlos para “pendência / possível falso pagante”.
- Markdown passou a reconhecer que Carlos é falso pagante e que `valor_parcela > 0` sozinho é insuficiente.

## Bloqueadores restantes

### 1. Markdown ainda não está consistente com SQL

Na seção 3 do markdown, a query exibida não tem `AND a.nome != 'Plínio da Silva Bezerra Neto'`, mas o resultado diz “sem Plínio”. O SQL anexo tem a cláusula; o relatório precisa bater com o SQL.

### 2. Arthur ainda é usado indevidamente para explicar CSV ativo 499

O markdown ainda afirma que CSV Emusys ativo 499 vs cálculo 498 é Arthur. Isso está errado para o CSV ativo export_39 já auditado, porque Arthur está ausente do ativo. Arthur só explica diferença pré-saneamento/view antiga, não CSV atual.

### 3. Ainda aparece “cache” como hipótese para matrículas

A seção 2 ainda diz que diferença de 2 matrículas “pode ser cache”. Isso não pode ser aceito como explicação final. Precisa diff nominal.

### 4. Pseudocódigo final continua errado

Na seção 7.2, `snapshot_linhas` ainda contém:

```sql
AND a.valor_parcela > 0
```

Isso é erro crítico. O snapshot base não pode filtrar valor, senão remove bolsistas/não pagantes antes de contar ativos, matrículas, banda e segundo curso. Pagamento é filtro/agregação só no cálculo de `alunos_pagantes`.

### 5. Princípio 7.1.4 ainda contradiz a própria análise

A seção 6.3 diz corretamente que `valor_parcela > 0` sozinho é insuficiente, mas a seção 7.1.4 propõe exatamente isso como regra final. Precisa trocar para “pagante real exige evidência financeira positiva ou valor reconciliado”, não apenas `valor_parcela > 0`.

### 6. Ledger 1c e 1d ainda são por linha, não ledger por pessoa

A seção 1c diz “lista de todos os 498 ativos (por pessoa)”, mas seleciona linhas. 1d diz “474 pagantes reais”, mas também seleciona linhas. Para ledger nominal de KPI pessoa, precisa `GROUP BY nome` e `string_agg` das matrículas.

### 7. Plínio ainda contraditório

A narrativa diz que 1361 estava ativo indevidamente, mas a seção 6.3 lista Plínio 1361 como `status inativo`. Precisa anexar SELECT real atual e separar “estado antes do saneamento” vs “estado atual”.

## Conclusão

A versão v3 está melhor para auditoria read-only, mas ainda precisa nova rodada. Não gerar migration.

Próximo pedido ao Cascade: corrigir markdown + pseudocódigo, criar ledger por pessoa real, remover cache e Arthur como explicação do CSV atual, e separar regra final de pagante da heurística `valor_parcela > 0`.
