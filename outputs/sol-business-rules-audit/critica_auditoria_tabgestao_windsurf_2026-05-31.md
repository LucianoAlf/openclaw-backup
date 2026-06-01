# Crítica da auditoria Windsurf — TabGestao.tsx

Data: 2026-05-31
Arquivo recebido: `Auditoria-READ-ONLY-TabGestaotsx---ea620a5b-19bb-49a6-94e1-6f24c8a1733d.md`

## Veredito

A auditoria está boa no diagnóstico geral: `TabGestao.tsx` mistura regras de negócio, views, `dados_mensais`, tabelas base e fallbacks perigosos.

Mas há duas correções importantes antes de mandar aplicar qualquer arquitetura nova:

1. A frase “`vw_kpis_gestao_mensal` já calcula corretamente para qualquer mês” é só parcialmente verdadeira.
2. “Criar `vw_kpis_gestao_periodo(ano_inicio, mes_inicio...)`” está conceitualmente errado se for literalmente uma view parametrizada; Postgres view não recebe parâmetro. Isso deveria ser uma RPC/function ou uma view mensal sem parâmetros + filtros.

## Ponto crítico — histórico não pode sair simplesmente de `dados_mensais`

Consulta live em `vw_kpis_gestao_mensal` mostrou que métricas de estoque se repetem entre março, abril e maio de 2026:

Campo Grande:
- Mar/2026: total_alunos_ativos 499, pagantes 475
- Abr/2026: total_alunos_ativos 499, pagantes 475
- Mai/2026: total_alunos_ativos 499, pagantes 475

Recreio:
- Mar/Abr/Mai: 333 ativos, 323 pagantes

Barra:
- Mar/Abr/Mai: 228 ativos, 227 pagantes

Isso indica que a view usa snapshot atual de `alunos` para estoque de alunos, não snapshot histórico real por mês.

Logo:

- A view pode estar boa para eventos mensais: matrículas, evasões, renovações, reajuste.
- A view NÃO deve ser assumida como fonte histórica completa para estoque: alunos ativos, pagantes, bolsistas, banda, MRR, ticket, inadimplência etc.

## Conclusões por recomendação Windsurf

### Correto

- Remover fallback que usa `renovacoes` para KPI.
- Remover cálculo manual crítico no frontend quando `dados_mensais` não existe.
- Mover Kids/School para view/camada canônica.
- Manter drill-downs diretos em tabelas base por enquanto, desde que usem filtros canônicos.
- Tratar `dados_mensais` como legado/cache/snapshot, não como fonte viva.

### Perigoso / precisa ajustar

- Não substituir todo `dados_mensais` por `vw_kpis_gestao_mensal` sem resolver histórico de estoque.
- Não eliminar `dados_mensais` agora: pode ser a única fotografia histórica de alguns KPIs, mesmo defasada.
- Não criar “view com parâmetros”; usar RPC/function ou view mensal sem parâmetros.
- Não consolidar período no frontend se a fonte mensal mistura eventos históricos com estoque atual.

## Próximo passo seguro

Pedir ao Windsurf uma auditoria de arquitetura mensal antes de patch:

1. Separar KPIs de evento vs KPIs de estoque.
2. Para cada KPI, definir fonte histórica e fonte live.
3. Confirmar se existe snapshot histórico confiável além de `dados_mensais`.
4. Só então propor uma camada canônica:
   - `vw_kpis_gestao_mensal_eventos` para eventos por mês; ou
   - `vw_kpis_gestao_mensal_v2` com colunas claramente classificadas; ou
   - RPC `get_kpis_gestao_periodo(...)` para consolidação de período.

## Regra nova para sanitização

Antes de aposentar `dados_mensais`, precisamos saber qual tabela guarda snapshot histórico real de:

- alunos ativos
- pagantes
- bolsistas
- banda
- MRR
- ticket médio
- inadimplência
- faturamento previsto/realizado

Se não existir, o caminho não é apagar `dados_mensais`: é criar um modelo de snapshot correto e migrar/reconciliar o histórico útil.
