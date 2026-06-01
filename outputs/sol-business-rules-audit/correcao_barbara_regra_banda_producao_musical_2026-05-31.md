# Correção de regra — Barbara Ribeiro Alves / Banda / Produção Musical

Data: 2026-05-31

## Correção do Alf

Alf corrigiu a interpretação sobre Barbara Ribeiro Alves id 49:

> “Mas a Bárbara não tá interrompida. Ela tá estudando, fazendo aula de produção musical.”

## Implicação

A regra proposta “excluir todo `cursos.is_projeto_banda=true` de `alunos_ativos` e `alunos_pagantes`” está ampla demais.

Barbara está ativa e estudando produção musical; portanto não pode ser excluída de `alunos_ativos`/`alunos_pagantes` só porque o `curso_id` atual aponta para um curso marcado como `is_projeto_banda=true` (`Minha Banda Para Sempre`).

Isso indica um dos problemas:

1. `curso_id` da Barbara está errado/desatualizado no LA Report; ou
2. `is_projeto_banda` está sendo usado de forma ampla demais para curso/projeto que ainda deve contar como estudo ativo; ou
3. Barbara tem uma matrícula/curso real que não está representado corretamente no Supabase.

## Consequência para números

- `473 pagantes` não deve ser aceito como target final.
- Barbara deve permanecer como aluna ativa/pagante enquanto estiver fazendo aula regular/produção musical.
- A diferença 475 → 473 foi atribuída a Arthur + Barbara; agora Barbara não pode sair.
- Com o saneamento do Arthur mantido, a base cai de 475 para pelo menos 474, não 473, salvo nova validação nominal.

## Nova orientação

Pausar qualquer migration de `recalcular_dados_mensais` que aplique:

```sql
COALESCE(c.is_projeto_banda, false) = false
```

como filtro cego de `alunos_ativos` e `alunos_pagantes`.

Antes disso, Windsurf deve fazer auditoria nominal dos alunos/matrículas com `is_projeto_banda=true`, separando:

- aluno só em projeto/banda que não deve contar como curso ativo;
- aluno em curso/aula regular, mesmo com `curso_id` ou flag errado;
- erro cadastral de `curso_id`;
- erro de classificação em `cursos.is_projeto_banda`.

## Prompt atualizado necessário

Pedir ao Windsurf reconciliação READ-ONLY, não migration.
