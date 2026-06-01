Auditoria LA Report — Analytics > Gestão
Unidade: Campo Grande | Período: Maio/2026
1. Números Atuais no Banco
Item	vw_kpis_gestao_mensal	vw_kpis_retencao_mensal	Query Direta	dados_mensais	Regra Validada (Alf)
total_alunos_ativos	499	—	565 registros¹	511	499 (exclui 2º curso)
total_alunos_pagantes	475	—	475	481	475
bolsistas integrais	14	—	14	—	14
bolsistas parciais	10	—	10	—	10
matrículas ativas (registros)	—	—	560 ativos + 5 trancados	—	565
matrículas banda	41	—	41 (todos 2º curso)	—	41?²
matrículas 2º curso pagante	66 (total)	—	27 (excl. banda/bolsista)	—	27-28
trancados	—	—	5 (1 segundo curso)	—	?³
novas matrículas	23	—	23	29	23
evasões/cancelamentos	13	21	8 (cancel) + 5 (não renov)	13	13
não renovações	—	5	5	—	5
avisos prévios	—	8	8	—	8 (não é evasão)
renovações realizadas	61	38	38 (mov_admin) / 61 (tabela)	0	38
taxa renovação	100%	100%	—	0%	88,4% (38/43)
churn rate	2.74%	4.42%	—	2.83%	2.74%
ticket médio	385.35	—	—	348.13	385.35
MRR	176.695,73	—	176.695,73	167.450,53	176.695,73
inadimplência %	1.26%	—	1.16% (6 alunos / R$ 2.058)	0.00%	1.16%
Notas: ¹ 565 registros = 560 ativos + 5 trancados. A view exclui 66 registros de 2º curso. ² A regra Alf diz "banda/projeto não deve inflar segundo curso pagante" — mas o card Banda no frontend mostra 41 como banda. Precisa validar se banda deve aparecer no KPI de banda mesmo sendo 2º curso. ³ O relatório operacional da equipe mostra 2 trancados. Divergência de 3 registros.

2. Divergências Detalhadas
Item A — vw_kpis_retencao_mensal soma aviso prévio em total_evasoes
View retencao: total_evasoes = 21 (8 cancelamentos + 5 não renovações + 8 avisos prévios)
View gestão: total_evasoes = 13 (8 + 5, corretamente exclui aviso prévio)
Regra Alf: "Evasões operacionais = cancelamentos + não renovação. Aviso prévio não é evasão."
Status: BUG SQL CONFIRMADO
Causa: A CTE evasoes_dedup na view retenção usa WHERE tipo IN ('evasao', 'nao_renovacao', 'aviso_previo'), enquanto a view gestão usa apenas ('evasao', 'nao_renovacao').
Correção: Remover 'aviso_previo' da CTE evasoes_dedup em vw_kpis_retencao_mensal.
Item B — Taxa de renovação = 100% em ambas as views (vs 88,4% real)
View gestão: Lê da tabela renovacoes → 61 registros, todos status='renovado', 0 nao_renovado → 100%
View retenção: Lê de movimentacoes_admin WHERE tipo='renovacao' → 38 registros, nenhuma não-renovação mapeada → 100%
Relatório operacional: 38 renovações / (38 + 5 não renovações) = 88,4%
Status: BUG SQL/DADO CONFIRMADO
Causa: A tabela renovacoes não tem os registros de não-renovação de maio/2026. O trigger de sincronização trg_sync_movimentacoes_admin deveria inserir status='nao_renovado' quando tipo='nao_renovacao', mas não está funcionando para esses registros (ou os registros foram inseridos diretamente sem passar pelo trigger).
Correção: Verificar por que as 5 não-renovações de maio/2026 não aparecem na tabela renovacoes. Inserir manualmente ou corrigir o trigger. Alternativamente, mudar a view gestão para calcular taxa de renovação a partir de movimentacoes_admin (38 renovações vs 5 não renovações).
Item C — Segundo curso: 66 na view vs 27-28 na regra Alf
View gestão: total_segundo_curso = 66 (todos os registros com is_segundo_curso = true)
Query direta corrigida: 27 pagantes (excluindo 38 banda/projeto e 2 bolsistas)
Relatório equipe: 28 matrículas de 2º curso
Status: DIVERGÊNCIA DE REGRA / RÓTULO
Causa: A view não separa "2º curso pagante" de "2º curso banda/bolsista". O relatório da equipe conta apenas os 27-28 que são cursos regulares pagantes.
Correção: Criar campo separado na view: segundo_curso_pagante (excluindo banda e bolsista) OU mudar o rótulo do card para "Total 2º Curso (inclui banda)".
Item D — Trancados: banco 5 vs relatório 2
Query direta: 5 trancados (Adriana Vitor Pim, Beatriz Cardoso Schmitz, Ester Santos do Amaral, Jonatas Viana Carvalho, Rayane Bianca dos Santos Stoianof Leite)
Dos 5: 1 é 2º curso (Rayane, Violão, SEGUNDO_CURSO). 4 são 1º curso.
Relatório equipe: 2 trancados
Status: DIVERGÊNCIA DE DADO / REGRA PENDENTE
Causa: Desconhecida. Possivelmente o relatório da equipe usa data de corte (apenas trancados do mês) ou exclui trancados de longa data.
Correção: Validar com Hugo/equipe os critérios do relatório operacional.
Item E — Banda: view conta 41, mas todos são 2º curso
View gestão: total_banda = 41 (filtro: c.nome ILIKE '%banda%' OR '%power kids%', sem filtro de is_segundo_curso)
Query direta: 41 alunos em Banda/Power Kids, todos com is_segundo_curso = true
Frontend modal: Busca cursos.is_projeto_banda = true sem filtrar is_segundo_curso
Status: REGRA PENDENTE DE VALIDAÇÃO
Causa: Todos os alunos de banda estão matriculados como 2º curso (fazem aula regular + banda).
Correção: Validar com Alf se o KPI "Banda" no Analytics deve mostrar:
(a) Todos os alunos em projetos de banda (41), ou
(b) Apenas os alunos cujo 1º curso é banda (0, já que todos são 2º curso)
Item F — dados_mensais defasado
alunos_pagantes: 481 (view: 475) → diferença de 6
novas_matriculas: 29 (view: 23) → diferença de 6
ticket_medio: 348.13 (view: 385.35) → diferença de 37.22
faturamento_estimado: 167.450,53 (view: 176.695,73)
Status: SNAPSHOT DESATUALIZADO
Correção: Clicar "Recalcular" no frontend para atualizar o snapshot de maio/2026.
3. Segundo Curso — Listagem Nominal
Tipo	Quantidade	Deve contar?	Observação
Pagante regular	27	✅ SIM	Segundo curso pagando (Violão, Canto, Guitarra, etc.)
Banda/projeto	38	❌ NÃO	Power Kids (14) + Minha Banda (24) — não devem "inflar 2º curso pagante"
Bolsista	2	❌ NÃO	Miguel Gomes Biancamano (BOLSISTA_INT, Harmonia) + Anne Krissya (BOLSISTA_PARC, Banda)
Total registros	66	—	View retorna 66, mas regra correta é 27
Listagem dos 27 segundo curso pagantes (corretos):
Aluno	Curso	Valor Parcela	Status
Carlos Eduardo Garcia do Nascimento	Canto	R$ 0,00	ativo
Daniela Beiriz Moura	Canto	R$ 288,00	ativo
Davi Guilherme De Souza Chaves Ribeiro	Canto	R$ 355,00	ativo
Israel Gonçalves Monteiro	Canto	R$ 250,00	ativo
João Paulo Costa do Carmo	Canto	R$ 288,00	ativo
Luiza Pimentel Oliveira Barbosa	Canto	R$ 347,00	ativo
Plínio da Silva Bezerra Neto	Canto	R$ 345,00	ativo
Thiago Sandes	Canto	R$ 295,00	ativo
Valdemir De Vargas Junior	Canto	R$ 315,00	ativo
Yuri Gabriel dos Santos Rodrigues	Canto	R$ 300,00	ativo
Gabriela Nascimento Brum	Contrabaixo	R$ 337,00	ativo
Marcello Fernandes Junior	Contrabaixo	R$ 427,00	ativo
Gabriel Teixeira Nogueira	Guitarra	R$ 387,00	ativo
Israel Gonçalves Monteiro	Guitarra	R$ 347,00	ativo
Kamilly Azevedo da Silva	Guitarra	R$ 387,00	ativo
Pedro Alves Pereira	Guitarra	R$ 447,00	ativo
Pedro Gabriel da França Rocha Pinto	Guitarra	R$ 373,00	ativo
Davi Guilherme De Souza Chaves Ribeiro	Harmonia	R$ 127,00	ativo
Miguel Bittencourt Costa	Harmonia	R$ 149,00	ativo
Barbara Ribeiro Alves	Home Studio	R$ 499,00	ativo
Eduardo França Tristão Batista	Minha Banda Para Sempre	null	ativo
Vitoria Vivia dos Santos Costa	Piano	R$ 0,00	ativo
Davi Guilherme De Souza Chaves Ribeiro	Teclado	R$ 367,00	ativo
Gabriel Mello Leal Rabelo de Oliveira	Teclado	R$ 334,00	ativo
Gabriel Negreiros Carvalho	Violão	R$ 315,00	ativo
Lis Dal Mora Mello	Violão	R$ 300,00	ativo
Rayane Bianca dos Santos Stoianof Leite	Violão	R$ 353,00	trancado
Possíveis marcações erradas:
Carlos Eduardo Garcia do Nascimento (Canto, 2º curso, valor R$ 0,00): Tipo matrícula é SEGUNDO_CURSO mas valor é 0. Se é 2º curso pagante, deveria ter valor > 0. Se é gratuito, talvez não devesse ser SEGUNDO_CURSO com conta_como_pagante=true.
Vitoria Vivia dos Santos Costa (Piano, 2º curso, valor R$ 0,00): Mesmo caso.
Eduardo França Tristão Batista (Minha Banda, 2º curso, valor null): Segundo curso em banda com valor nulo.
4. Trancados — Listagem Nominal
Aluno	Curso	Tipo Matrícula	2º Curso?	Deve contar?
Adriana Vitor Pim	Teclado	REGULAR	Não	✅ Sim (1º curso)
Beatriz Cardoso Schmitz	Canto	REGULAR	Não	✅ Sim (1º curso)
Ester Santos do Amaral	Canto	REGULAR	Não	✅ Sim (1º curso)
Jonatas Viana Carvalho	Canto	REGULAR	Não	✅ Sim (1º curso)
Rayane Bianca dos Santos Stoianof Leite	Violão	SEGUNDO_CURSO	Sim	⚠️ Dependente de regra
Divergência: Banco tem 5, relatório operacional mostra 2. Se o relatório exclui 2º curso: 5 - 1 = 4. Ainda faltam 2 registros para bater com o relatório. Possíveis explicações:

Relatório usa data de corte (apenas trancados do mês de maio)
Relatório exclui trancados de longa data (ex: trancados antes de 2026)
5. Evasões / Aviso Prévio — Confirmação de Bug
BUG CONFIRMADO em vw_kpis_retencao_mensal

sql
-- CTE evasoes_dedup na view retencao (SQL atual do banco):
WHERE m.tipo = ANY (ARRAY['evasao', 'nao_renovacao', 'aviso_previo'])
total_evasoes = 21 (8 evasão + 5 não renovação + 8 aviso prévio)
evasoes_interrompidas = 8 ✅
avisos_previos = 8 ✅
nao_renovacoes = 5 ✅
A view vw_kpis_gestao_mensal está CORRETA:

sql
WHERE m.tipo = ANY (ARRAY['evasao', 'nao_renovacao'])
-- total_evasoes = 13 ✅
Recomendação: A view retencão deve espelhar a lógica da view gestão. O aviso prévio deve ser excluído de total_evasoes (pode permanecer como campo separado avisos_previos).

6. Saída Auditável — Tabela Consolidada
Unidade: Campo Grande
Item	Valor view	Valor query direta	Valor regra validada	Status	Causa provável	Correção
total_alunos_ativos	499	565 registros	499	✅ OK	View exclui 2º curso	—
total_alunos_pagantes	475	475	475	✅ OK	Filtro conta_como_pagante	—
bolsistas integrais	14	14	14	✅ OK	Codigo BOLSISTA_INT	—
bolsistas parciais	10	10	10	✅ OK	Codigo BOLSISTA_PARC	—
matrículas banda	41	41 (todos 2º curso)	?	⚠️ PENDENTE	Todos em banda são 2º curso	Validar com Alf
matrículas 2º curso pagante	66 (view)	27 (correto)	27-28	❌ DIVERGENTE	View não exclui banda/bolsista	Corrigir view
trancados	—	5	2 (relatório)	❌ DIVERGENTE	Critério desconhecido da equipe	Validar com Hugo
novas matrículas	23	23	23	✅ OK	CTE matriculas_mes	—
evasões	13 (gestão) / 21 (retenção)	13 = 8+5	13	❌ BUG SQL	Retenção soma aviso prévio	Remover aviso_previo da CTE
não renovações	—	5	5	✅ OK	mov_admin tipo=nao_renovacao	—
avisos prévios	—	8	8 (não conta)	✅ OK	Campo separado	—
renovações	61 (gestão) / 38 (retenção)	38	38	❌ DIVERGENTE	tabela renovacoes incompleta	Corrigir trigger/população
taxa renovação	100% (ambas)	—	88,4%	❌ BUG SQL/DADO	Não há nao_renovado na tabela	Inserir não-renovações
churn rate	2.74% (gestão) / 4.42% (retenção)	—	2.74%	⚠️ PENDENTE	Retenção usa evasões=21	Corrigir após fix evasões
ticket médio	385.35	—	385.35	✅ OK	Deduplica por pessoa	—
MRR	176.695,73	176.695,73	176.695,73	✅ OK	Soma parcelas pagantes	—
inadimplência %	1.26%	1.16% (6 alunos)	1.16%	⚠️ LEVE	Arredondamento view	—
dados_mensais snapshot	defasado	—	—	⚠️ DESATUALIZADO	Não recalculado maio	Clicar "Recalcular"
7. Classificação das Divergências
Bugs de SQL / View
vw_kpis_retencao_mensal — total_evasoes inclui aviso prévio
Impacto: Churn rate inflado (4.42% vs 2.74% correto)
Fix: Remover 'aviso_previo' da CTE evasoes_dedup
Risco: Alto (KPI de retenção está errado no frontend quando consome essa view)
vw_kpis_retencao_mensal — taxa_renovacao = 100%
Impacto: Retenção aparece perfeita quando não é
Fix: Usar movimentacoes_admin como fonte de não-renovação OU popular tabela renovacoes com status='nao_renovado'
Risco: Alto
vw_kpis_gestao_mensal — taxa_renovacao = 100%
Impacto: Mesmo problema acima, via tabela renovacoes
Fix: Corrigir trigger de sincronização ou mudar view para usar movimentacoes_admin
Risco: Alto
vw_kpis_gestao_mensal — segundo_curso não separa banda/bolsista
Impacto: Card "Total 2º Curso" mostra 66 em vez de 27-28
Fix: Adicionar campo segundo_curso_pagante com filtros excluindo banda e bolsista
Risco: Médio
Bugs de Frontend / Rótulo
Percentual Kids/School usa denominador inconsistente
O frontend calcula: total_la_kids / total_alunos_ativos → 214/499
Mas total_la_kids vem de query direta em TODOS os registros (565), enquanto total_alunos_ativos é da view (499, sem 2º curso)
Se houver crianças no 2º curso, o percentual está matematicamente inconsistente
Risco: Médio
Tooltip do card "Alunos Pagantes" no frontend diz "exclui segundo curso"
Mas total_alunos_pagantes = 475 já vem da view com esse filtro. O tooltip está correto.
O tooltip do card "Total Alunos Ativos" diz "excluindo segundo curso" — correto.
Dados Sujos no Banco
Tabela renovacoes não tem não-renovações de maio/2026
61 registros, todos status='renovado', 0 nao_renovado
O trigger trg_sync_movimentacoes_admin deveria ter inserido 5 registros nao_renovado
Risco: Alto (afeta views e relatórios)
evasoes_v2 vazia para maio/2026 em Campo Grande
0 registros para maio/2026 (330 históricos, todos pré-2026)
Trigger pode não estar funcionando, ou movimentações foram inseridas sem passar pelo trigger
Risco: Médio (views já foram reescritas para usar movimentacoes_admin, mas evasoes_v2 perdeu a função de fonte de verdade)
Alunos de 2º curso com valor_parcela = 0 ou null
Carlos Eduardo Garcia do Nascimento (Canto, 2º curso): valor R$ 0,00
Vitoria Vivia dos Santos Costa (Piano, 2º curso): valor R$ 0,00
Eduardo França Tristão Batista (Minha Banda, 2º curso): valor null
Se são 2º curso pagantes, o valor deveria ser > 0
Risco: Baixo (afeta MRR/ticket médio se entram no cálculo)
Pontos para Hugo / Equipe Validarem
Relatório operacional mostra 2 trancados — qual critério?
Banco tem 5. Se exclui 2º curso: 4. Ainda faltam 2.
Hugo precisa confirmar se o relatório filtra por data de trancamento ou outro critério.
Relatório operacional mostra 28 matrículas de 2º curso
Isso bate com a regra Alf (excluindo banda 38 e bolsista 2 → 27-28 restantes)
Hugo precisa confirmar se essa é a regra desejada para o relatório
KPI "Banda" no Analytics — deve incluir 2º curso?
Atualmente todos os 41 alunos de banda são 2º curso
O modal de banda no frontend busca is_projeto_banda = true sem filtrar is_segundo_curso
Hugo/Alf precisam definir se o card Banda mostra:
Todos os alunos em projetos de banda (41, como está hoje), ou
Apenas alunos cujo 1º curso é banda (0, já que não há alunos com banda como 1º curso)
Pontos que Dependem do Alf
Definição de "Alunos Ativos" inclui trancados?
Alf já validou: "Sim, alunos ativos inclui trancados"
Mas o nome "Ativos" pode confundir operacionalmente. Considerar rótulo "Alunos Base".
Kids/School percentual sobre matrículas ou pessoas?
Alf validou: "percentual sobre matrículas, não sobre alunos únicos"
Mas o frontend calcula kids (214) / total_alunos_ativos (499) = 43%
Se uma mesma criança faz 2 cursos, conta 2x no numerador (kids) e 1x no denominador (se um dos cursos é excluído como 2º curso). Isso é matematicamente inconsistente.
Precisa validar se a query de idade deve incluir ou excluir 2º curso.
Segundo curso pagante correto = 27?
Alf validou: "Segundo curso só conta quando aluno pagante faz segundo/terceiro curso pagando. Banda/projeto não deve inflar."
O cálculo de 27 bate com essa regra. Precisa de aprovação para mudar a view.
Resumo Executivo
Prioridade	Problema	Impacto	Ação Imediata
🔴 Alta	View retenção soma aviso prévio em evasões	Churn rate falso (4.42%)	Corrigir SQL evasoes_dedup
🔴 Alta	Taxa renovação = 100% (ambas views)	Retenção parece perfeita	Corrigir fonte de não-renovações
🟡 Média	Segundo curso: view 66 vs real 27	KPI de 2º curso inflado	Validar regra com Alf antes de corrigir view
🟡 Média	Trancados: 5 vs relatório 2	Base inconsistente	Hugo validar critério do relatório
🟡 Média	Banda: todos os 41 são 2º curso	Conceito de banda ambíguo	Alf definir se banda no 2º curso conta
🟢 Baixa	dados_mensais defasado	Snapshot histórico desatualizado	Recalcular snapshot maio/2026
Próximos passos recomendados:

Corrigir vw_kpis_retencao_mensal (remover aviso_previo)
Investigar trigger trg_sync_movimentacoes_admin — por que não inseriu não-renovações em renovacoes?
Validar com Alf a regra de segundo curso (27) e banda (41)
Validar com Hugo o critério de trancados no relatório operacional
Recalcular snapshot de maio/2026 em dados_mensais