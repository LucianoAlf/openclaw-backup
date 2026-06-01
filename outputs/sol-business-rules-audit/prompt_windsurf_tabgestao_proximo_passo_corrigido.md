Windsurf, a auditoria READ-ONLY do TabGestao.tsx está boa no diagnóstico geral, mas não aplique patch ainda.

Correção importante do Alfredo:

A afirmação “vw_kpis_gestao_mensal já calcula corretamente para qualquer mês” é apenas parcialmente verdadeira.

Validação feita contra Supabase mostrou que em `vw_kpis_gestao_mensal`, para março/abril/maio 2026, métricas de estoque se repetem por unidade:

- Campo Grande: total_alunos_ativos 499 / pagantes 475 em mar, abr e mai
- Recreio: 333 / 323 em mar, abr e mai
- Barra: 228 / 227 em mar, abr e mai

Isso indica que a view calcula eventos mensais, mas usa snapshot atual da tabela `alunos` para estoque de alunos. Portanto ela não pode substituir `dados_mensais` como histórico completo sem antes resolver snapshots históricos.

Também ajuste a recomendação técnica:

- Postgres VIEW não recebe parâmetros como `vw_kpis_gestao_periodo(ano_inicio, mes_inicio...)`.
- Se precisar receber período, deve ser RPC/function, por exemplo `get_kpis_gestao_periodo(p_ano_inicio, p_mes_inicio, p_ano_fim, p_mes_fim, p_unidade_id)`.
- Ou então criar uma view mensal sem parâmetros e o frontend filtra por ano/mês.

Novo objetivo READ-ONLY:

Faça uma auditoria de arquitetura dos KPIs do TabGestao separando:

1. KPIs de EVENTO mensal — podem ser reconstruídos por data:
   - novas matrículas
   - evasões
   - não renovações
   - renovações
   - reajuste médio
   - leads/eventos comerciais

2. KPIs de ESTOQUE/snapshot — precisam de fotografia histórica:
   - alunos ativos
   - pagantes
   - bolsistas
   - banda
   - MRR
   - ticket médio
   - inadimplência
   - faturamento previsto/realizado
   - Kids/School se for distribuição histórica

Para cada KPI, entregue:

- nome do KPI
- tipo: evento ou estoque
- fonte atual no TabGestao
- fonte atual na view
- fonte histórica confiável existente ou inexistente
- risco de usar `vw_kpis_gestao_mensal` no histórico
- recomendação: manter em dados_mensais por enquanto / mover para view mensal / criar snapshot novo / criar RPC de período

Importante:

- Não eliminar `dados_mensais` agora.
- Não tratar `dados_mensais` como fonte viva.
- Não usar `renovacoes` para KPI live.
- Não mexer em dados.
- Não criar migration ainda.
- O objetivo é desenhar a arquitetura correta para não trocar uma gambiarra por outra.
