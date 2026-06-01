Windsurf, a auditoria por KPI está conceitualmente correta ao separar EVENTO vs ESTOQUE, mas ainda não crie migration.

Correção importante do Alfredo: o schema real de `dados_mensais` já possui algumas colunas que você listou como ausentes:

- `alunos_ativos`
- `matriculas_ativas`
- `matriculas_banda`
- `matriculas_2_curso`
- `ticket_medio_passaporte`
- `faturamento_passaporte`

E a função `recalcular_dados_mensais(p_ano, p_mes, p_unidade_id)` já popula pelo menos:

- `alunos_ativos`
- `alunos_pagantes`
- `matriculas_ativas`
- `matriculas_banda`
- `matriculas_2_curso`
- `novas_matriculas`
- `evasoes`
- `churn_rate`
- `ticket_medio`
- `tempo_permanencia`

Então o próximo passo NÃO é simplesmente “adicionar colunas”.

Novo objetivo READ-ONLY:

Auditar `dados_mensais` + função `recalcular_dados_mensais` + uso em `TabGestao.tsx`.

Entregar:

1. Schema real de `dados_mensais`
   - coluna
   - tipo
   - se é usada no TabGestao
   - se é populada por `recalcular_dados_mensais`
   - status: OK / existe mas não usada / existe mas regra divergente / falta

2. Função `recalcular_dados_mensais`
   - mapear cada SELECT/cálculo
   - comparar com regras canônicas validadas:
     - alunos ativos incluem trancados e excluem segundo curso
     - pagantes excluem bolsista integral, bolsista parcial e não pagante
     - matrícula ativa é registro, inclui segundo curso/banda/coral
     - segundo curso só pago de aluno pagante; não inclui banda/projeto/bolsista
     - evasão total = evasão interrompida + não renovação
     - aviso prévio separado
     - taxa renovação = renovação / (renovação + não renovação)
     - reajuste médio = só aumentos positivos

3. Completude de `dados_mensais`
   - listar meses/unidades ausentes ou incompletos em 2026
   - mostrar colunas nulas/zeradas que deveriam ter valor

4. Proposta de arquitetura futura
   - quais colunas realmente precisam ser adicionadas
   - quais colunas já existem e só precisam ser usadas/corrigidas
   - quais cálculos da função precisam mudar
   - como fazer backfill sem sobrescrever histórico útil errado

Importante:
- Não criar migration ainda.
- Não alterar dados.
- Não dropar/renomear nada.
- Não assumir que `dados_mensais.alunos_pagantes` é ativos; existe coluna `alunos_ativos`, então audite o uso real.
- O objetivo é evitar adicionar coluna duplicada ou corrigir a coisa errada.
