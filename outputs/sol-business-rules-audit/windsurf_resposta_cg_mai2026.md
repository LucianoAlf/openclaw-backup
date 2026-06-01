Auditoria LA Report — Analytics > Gestão | Campo Grande | Maio/2026
Respostas Diretas às 12 Perguntas
1. SQL atual da view vw_kpis_gestao_mensal
Arquivos no repositório (OBSOLETOS): supabase/migrations/fase3_views_kpis.sql e fase3_01_view_gestao.sql
SQL ATUAL no banco: Obtido via pg_get_viewdef. A view foi completamente reescrita e não corresponde aos arquivos do repo. Ela agora usa:
CTE alunos_mes com tipos_matricula (campos conta_como_pagante, entra_ticket_medio)
CTE ticket_por_unidade com deduplicação por lower(trim(nome)) || data_nascimento || unidade_id
CTE permanencia_calc unindo alunos_historico + alunos (status inativo/evadido)
CTE evasoes_mes lendo de movimentacoes_admin (não de evasoes_v2)
CTE renovacoes_mes lendo da tabela renovacoes
CTE leads_mes lendo da tabela leads
2. SQL atual da view vw_kpis_retencao_mensal
Arquivo no repositório (OBSOLETO): supabase/migrations/fase3_views_kpis.sql
SQL ATUAL no banco: Reescrita. Todas as CTEs (evasoes_dedup, evasoes_mes, renovacoes_mes) leem de movimentacoes_admin, não de evasoes_v2 nem da tabela renovacoes. Isso é crítico para os bugs encontrados.
3. Como total_alunos_ativos = 499 é calculado
sql
-- CTE alunos_mes na view
count(*) FILTER (WHERE is_segundo_curso IS NULL OR is_segundo_curso = false)
FROM alunos WHERE status IN ('ativo', 'trancado')
Total registros ativos+trancados em CG = 565
Segundo curso ativos+trancados = 66
565 - 66 = 499
Nota: A view chama esse campo total_alunos_ativos, mas a query inclui trancados. O nome "ativos" é enganoso — deveria ser "alunos base" ou "alunos sem segundo curso".
4. Como total_alunos_pagantes = 475 é calculado
sql
count(*) FILTER (
  WHERE tm.conta_como_pagante = true 
  AND (is_segundo_curso IS NULL OR is_segundo_curso = false)
)
Dos 565 registros em CG:
REGULAR: 475 (conta_como_pagante = true)
BANDA: 23 (false)
BOLSISTA_INT: 15 (false)
BOLSISTA_PARC: 11 (false)
SEGUNDO_CURSO: 41 (true, mas filtrado fora por is_segundo_curso)
Resultado = 475 (apenas REGULAR sem segundo curso)
5. Bolsista parcial como não pagante?
Sim. A view trata bolsista parcial como não pagante.

tipos_matricula.conta_como_pagante = false para BOLSISTA_PARC
Local: CTE alunos_mes na vw_kpis_gestao_mensal
O relatório administrativo confirma: 24 não pagantes = 14 bolsistas integrais + 10 parciais. Os números batem com a view.
6. Por que Kids 214 + School 351 = 565, enquanto "Alunos ativos" = 499?
BUG DE RÓTULO / CONTEXTO INCONSISTENTE.

Card "Total Alunos Ativos": 499 (fonte: view, que exclui segundo curso, mas inclui trancados)
Kids + School: 214 + 351 = 565 (fonte: query direta em alunos com status IN ('ativo','trancado'), inclui todos os registros, inclusive 2º curso)
O frontend calcula o percentual como:
ts
`${(dados.total_la_kids / dados.total_alunos_ativos) * 100}% do total`
Ex: 214 / 499 = 42.8% → arredonda para 43%
Mas 214 vem de 565 registros (incluindo 2º curso), enquanto 499 é o total sem 2º curso.
Impacto: O percentual exibido é matematicamente inconsistente — o numerador inclui 2º curso, o denominador exclui.
7. Por que relatório mostra matrículas de 2º curso = 28, mas banco tem 66?
DIVERGÊNCIA DE DADO / REGRA DIFERENTE.

Fonte	Valor	Nota
Banco (is_segundo_curso = true, ativos+trancados)	66	CG total
Relatório administrativo equipe (30/05)	28	Possivelmente "novos 2º cursos no mês"
dados_mensais	68	Snapshot defasado (provavelmente de outro mês)
Distribuição dos 66 no banco: Minha Banda Para Sempre (24), Power Kids (14), Canto (10), Guitarra (5), Violão (4), etc.
Hipótese mais provável: O relatório da equipe conta apenas alunos que fizeram 2º curso no mês (novas matrículas de 2º curso), não o saldo acumulado. Ou a equipe exclui "Power Kids" da contagem de 2º curso (se fizer isso: 66 - 14 = 52, ainda diverge de 28).
8. Por que relatório mostra trancados = 2, mas query retorna 5?
Fonte	Valor
Query direta status = 'trancado' em CG	5
Relatório administrativo	2
Dos 5 trancados no banco, 1 é segundo curso.
Possível causa: O relatório da equipe pode estar usando uma data de corte diferente (ex: trancados apenas do mês) ou excluir trancados de longa data. Divergência de 3 registros precisa validação com a equipe/Hugo.
9. Por que vw_kpis_retencao_mensal.total_evasoes = 21?
BUG CONFIRMADO NA VIEW.

A CTE evasoes_dedup filtra:
sql
WHERE m.tipo = ANY (ARRAY['evasao', 'nao_renovacao', 'aviso_previo'])
movimentacoes_admin em CG (maio/2026): 8 evasão + 5 nao_renovacao + 8 aviso_previo = 21
Regra de negócio: Evasões = Cancelamentos (8) + Não Renovações (5) = 13
Aviso prévio NÃO é evasão — o aluno ainda está ativo.
A view está somando aviso prévio indevidamente. Resultado: 21 em vez de 13.
10. Regra do frontend para taxa de renovação
Sim, confirma a fórmula do relatório:

ts
// TabGestao.tsx ~linha 820
renovacoes_realizadas / (renovacoes_realizadas + nao_renovacoes) * 100
Relatório: 38 / (38 + 5) = 88,4% ✅
Mas: As views não usam essa fórmula.
vw_kpis_gestao_mensal usa renovacoes / total_contratos da tabela renovacoes → 61/61 = 100%
vw_kpis_retencao_mensal usa renovacoes_realizadas / renovacoes_previstas de movimentacoes_admin → 38/38 = 100%
11. Mês corrente deve usar view, não dados_mensais?
Sim. O frontend já faz isso corretamente:

ts
// TabGestao.tsx ~linha 248
if (isPeriodoAtual) {
  // usar vw_kpis_gestao_mensal e vw_kpis_retencao_mensal
} else {
  // usar dados_mensais (histórico)
}
dados_mensais é snapshot histórico/fechamento. Para maio/2026 (mês atual), a view em tempo real é a fonte correta.
12. Divergências Reais — Formato Auditável
Item 1 — vw_kpis_retencao_mensal soma aviso prévio em total_evasoes

Fonte encontrada: SQL atual do banco (via pg_get_viewdef), CTE evasoes_dedup
Regra atual implementada: WHERE tipo IN ('evasao', 'nao_renovacao', 'aviso_previo')
Divergência: total_evasoes retorna 21 (CG maio/2026) em vez de 13
Causa provável: Aviso prévio foi incluído na CTE de evasões durante reescrita da view (provavelmente porque evasoes_v2 está vazio para 2026 e a view foi adaptada para movimentacoes_admin)
Correção recomendada: Remover 'aviso_previo' da CTE evasoes_dedup. Criar CTE separada para avisos prévios se necessário.
Precisa validação do Alf? não — regra já foi validada em memórias anteriores: evasões = cancelamentos + não renovações (exclui aviso prévio e transferência)
Item 2 — vw_kpis_gestao_mensal chama "ativos" mas inclui trancados

Fonte encontrada: CTE alunos_mes na view, WHERE status = ANY (ARRAY['ativo', 'trancado'])
Regra atual implementada: total_alunos_ativos = count de registros sem segundo curso, incluindo trancados
Divergência: Exibe 499 como "ativos", mas inclui 5 trancados. O relatório separa "ativos: 499" e "trancados: 2" — o banco tem 5 trancados.
Causa provável: A view foi projetada para mostrar "base de alunos" (snapshot), não "ativos" estrito. Mas o rótulo diz "Ativos".
Correção recomendada: Renomear campo para total_alunos_base ou total_alunos_sem_segundo_curso; criar campo separado total_trancados se desejado.
Precisa validação do Alf? sim — Qual o conceito correto para o KPI "Total Alunos Ativos"? Deve incluir trancados?
Item 3 — Percentual Kids/School usa denominador inconsistente

Fonte encontrada: TabGestao.tsx linhas 1349-1360
Regra atual implementada: total_la_kids / total_alunos_ativos * 100 → 214 / 499 = 43%
Divergência: Numerador (214) vem de TODOS os registros (565), mas denominador (499) exclui 2º curso. Se houver kids no 2º curso, o percentual está inflado.
Causa provável: Query de idade busca todos com status IN ('ativo','trancado'), enquanto card de total usa a view.
Correção recomendada: Alinhar a query de faixa etária com o mesmo filtro da view (excluir 2º curso) OU mudar o denominador para o total real de registros (565).
Precisa validação do Alf? sim — O percentual de Kids deve ser sobre "total de alunos (pessoas)" ou "total de matrículas (registros)"?
Item 4 — Segundo curso: banco 66 vs relatório 28

Fonte encontrada: Query direta alunos.is_segundo_curso = true em CG
Regra atual implementada: Banco conta 66 registros ativos+trancados; relatório da equipe conta 28
Divergência: 38 registros de diferença
Causa provável: Relatório da equipe pode estar contando apenas novos 2º cursos do mês, ou usando critério diferente (ex: excluir Power Kids, ou contar por pessoa e não por curso).
Correção recomendada: Validar com Hugo/equipe qual é a definição operacional de "matrículas de 2º curso" no relatório. Pode ser necessário criar uma view ou campo separado para "novos 2º cursos no mês".
Precisa validação do Alf? sim — A regra do relatório da equipe (28) ou do banco (66) está correta?
Item 5 — Trancados: banco 5 vs relatório 2

Fonte encontrada: Query direta status = 'trancado' em CG
Regra atual implementada: Banco = 5; Relatório = 2
Divergência: 3 registros
Causa provável: Relatório pode usar data de corte (trancados do mês apenas) ou filtro diferente.
Correção recomendada: Validar com equipe os critérios do relatório. Se o banco está correto, atualizar relatório.
Precisa validação do Alf? sim
Item 6 — Taxa de renovação: views divergem do relatório (88,4%)

Fonte encontrada: vw_kpis_gestao_mensal (usa renovacoes → 100%) e vw_kpis_retencao_mensal (usa movimentacoes_admin → 100%)
Regra atual implementada: Frontend calcula corretamente: 38 / (38 + 5) = 88,4%
Divergência: Ambas as views retornam 100% para CG maio/2026
Causa probável:
vw_kpis_gestao_mensal lê tabela renovacoes que tem 61 registros, todos status='renovado', 0 nao_renovado para maio/2026.
vw_kpis_retencao_mensal lê movimentacoes_admin que tem 38 renovações, todas com status implícito de realizadas.
Correção recomendada: Inserir os 5 não-renovações na tabela renovacoes com status='nao_renovado' (ou corrigir a view para usar movimentacoes_admin como fonte única de verdade para retenção, alinhada com o frontend).
Precisa validação do Alf? não — A fórmula 38/(38+5)=88,4% está correta e bate com o relatório da equipe.
Item 7 — evasoes_v2 vazia para 2026 força views a usarem movimentacoes_admin

Fonte encontrada: Query direta em evasoes_v2 — 0 registros para maio/2026 em CG (330 históricos, todos pré-2026)
Regra atual implementada: Views reescritas para ler de movimentacoes_admin
Divergência: A tabela evasoes_v2 foi criada como fonte de verdade para evasões, mas não está sendo populada em 2026.
Causa probável: Trigger trg_sync_movimentacoes_admin existe e deveria sincronizar, mas pode não estar funcionando para 2026, ou as movimentações foram inseridas diretamente sem passar pelo trigger.
Correção recomendada: Investigar por que evasoes_v2 não tem dados de 2026. Se o trigger estiver funcionando, verificar se tipo_saida_id está sendo mapeado corretamente. Se não, corrigir o fluxo de inserção.
Precisa validação do Alf? sim — Qual a fonte de verdade desejada para evasões? movimentacoes_admin ou evasoes_v2?
Item 8 — dados_mensais defasado (alunos_ativos=511, pagantes=481, matriculas=29)

Fonte encontrada: Tabela dados_mensais para CG maio/2026
Regra atual implementada: Snapshot mensal fechado
Divergência: dados_mensais.alunos_pagantes = 481 vs view/tempo real = 475; novas_matriculas = 29 vs view = 23
Causa probável: Snapshot não foi recalculado/atualizado recentemente. O botão "Recalcular" existe no frontend, mas pode não ter sido clicado.
Correção recomendada: Clicar "Recalcular" no frontend para atualizar o snapshot de maio/2026. Ou automatizar via cron.
Precisa validação do Alf? não
Resumo Executivo para Equipe/Hugo
Prioridade	Item	Impacto	Ação
🔴 Alta	View retenção soma aviso prévio em evasões (21 vs 13)	Churn rate inflado	Corrigir SQL da view
🔴 Alta	Views renovação retornam 100% (vs 88,4% real)	Taxa de retenção falsa	Alinhar fonte de dados
🟡 Média	Kids/School percentual com denominador inconsistente	KPI de faixa etária distorcido	Alinhar query com view
🟡 Média	Segundo curso 66 vs relatório 28	Dado operacional divergente	Validar regra com equipe
🟡 Média	Trancados 5 vs relatório 2	Base de alunos inconsistente	Validar regra com equipe
🟢 Baixa	dados_mensais defasado	Snapshot histórico desatualizado	Recalcular snapshot
🟢 Baixa	evasoes_v2 vazia para 2026	Fonte de verdade não populada	Investigar trigger/população
Recomendação: Antes de tocar no código, validar com Hugo/equipe:

O conceito de "aluno ativo" inclui trancados?
O relatório de 2º curso (28) é saldo acumulado ou novos do mês?
A fonte de verdade para evasões deve ser evasoes_v2 (ressuscitar) ou movimentacoes_admin (consolidar)?