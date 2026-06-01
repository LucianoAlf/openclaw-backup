# Regras candidatas — Sol / LA Report v0

> Status inicial: extraído do repo LAperformanceReport + inventário Supabase. Ainda precisa validação antes de virar skill canônica.

## Alunos / matrícula

### `[CANDIDATA]` Tabela `alunos` representa matrículas, não pessoas
- Uma pessoa com 2 cursos pode ter 2 linhas.
- Identidade aproximada de pessoa: `nome + unidade_id`.
- Segundo curso legítimo exige curso diferente; mesmo curso duplicado tende a ser duplicata.
- Fonte: `.claude/memory/regras-negocio.md`.

### `[CANDIDATA]` Bolsistas e não pagantes não entram nos KPIs financeiros principais
- Tipos citados: `bolsista_integral`, `bolsista_parcial`, `nao_pagante`.
- Docs antigas também citam códigos `BOLSISTA_INT`, `BOLSISTA_PARC`, `BANDA`.
- Precisamos mapear nomes/códigos reais no banco.
- Fonte: `.claude/memory/regras-negocio.md`, `docs/KPIs_LA_MUSIC_PERFORMANCE_REPORT.md`.

### `[CANDIDATA]` Projeto de banda não entra em carteira regular/score/médias de turma
- Curso com `cursos.is_projeto_banda = true` deve ser excluído de vários KPIs de professor e carteira.
- Fonte: `.claude/memory/regras-negocio.md`, `.claude/memory/metricas.md`.

## LTV / permanência

### `[CANDIDATA]` LTV/tempo de permanência só conta quando a pessoa saiu de todos os cursos
- Se cancelou um curso mas continua em outro, não conta como saída final para LTV.
- Fonte: `.claude/memory/regras-negocio.md`, `.claude/memory/metricas.md`.

### `[CANDIDATA]` Permanência mínima de 4 meses
- Saídas com `tempo_permanencia_meses < 4` são excluídas.
- Fonte: `.claude/memory/regras-negocio.md`, `docs/KPIs_LA_MUSIC_PERFORMANCE_REPORT.md`.

### `[CANDIDATA]` Passagens são independentes
- Saiu e voltou = nova passagem, não soma tudo em uma permanência única.
- Taxa de retorno = % pessoas com 2+ passagens.
- Fonte: `.claude/memory/regras-negocio.md`.

## Churn / evasão

### `[CANDIDATA]` Churn corporativo
```text
churn = evasoes_periodo / (alunos_inicio_periodo + novas_matriculas_periodo) * 100
```
- Exclui banda e tipos não pagantes conforme contexto.
- Fonte: `.claude/memory/metricas.md`.

### `[CANDIDATA]` Score do professor só penaliza motivos marcados para score
- `motivos_saida.conta_score_professor = true`.
- Motivo NULL sem match não conta.
- Fonte canônica provável: RPC `get_kpis_professor_periodo` + `.claude/memory/metricas.md`.

### `[CANDIDATA]` Vínculo professor-aluno não é apagado quando aluno sai
- `professor_atual_id` fica como histórico.
- Então carteira atual sempre precisa filtrar `alunos.status = 'ativo'`.
- Fonte: `.claude/memory/regras-negocio.md`, `.claude/memory/metricas.md`.

## Comercial

### `[CANDIDATA]` Bolsista integral e não pagante não entram no pipeline comercial
- Fonte: `.claude/memory/regras-negocio.md`.

### `[DIVERGENTE]` Conversão do professor pode passar de 100%
- Fórmula atual tem assimetria:
  - denominador exige `experimental_realizada = true`;
  - numerador aceita convertido sem `faltou_experimental`.
- Decisão pendente: corrigir operação no Emusys ou mudar fórmula.
- Fonte: `.claude/memory/regras-negocio.md`, `.claude/memory/metricas.md`.

### `[CANDIDATA]` Ticket médio de passaporte exclui valor zero
```text
ticket_medio_passaporte = SUM(valor_passaporte) / COUNT(*) WHERE valor_passaporte > 0
```
- Fonte: `.claude/memory/metricas.md`.

## Renovação

### `[CANDIDATA]` Taxa de renovação
```text
taxa_renovacao = renovacoes / (renovacoes + nao_renovacoes + aviso_previo) * 100
```
- Fonte: `.claude/memory/metricas.md`.

### `[CANDIDATA]` Reajuste médio
```text
AVG((valor_parcela_novo - valor_parcela_anterior) / valor_parcela_anterior * 100)
```
- Fonte: `.claude/memory/regras-negocio.md`, `.claude/memory/metricas.md`.

## Datas

### `[CANDIDATA]` Datas de negócio sempre em BRT / America/Sao_Paulo
- Fonte: `.claude/memory/regras-negocio.md`.

## Evidência visual — prints Analytics Campo Grande Mai/2026

### `[DUVIDA]` Base de alunos por produto não fecha com total ativo
- Print mostra `Total Alunos Ativos = 499`.
- `LA Music Kids = 214 (43%)` e `LA Music School = 351 (70%)`.
- Soma Kids + School = 565 e percentuais somam 113%.
- Pode ser sobreposição por matrícula/produto/segundo curso ou erro de base.
- Precisa validar se produto é classificação exclusiva ou se aluno/matrícula pode contar em mais de um grupo.

### `[DUVIDA]` Alunos pagantes: denominador 479 vs total ativo 499
- Print mostra `Alunos Pagantes = 475 / 479 (99%)`.
- Total ativo do mesmo print = 499.
- `499 - 14 bolsistas integrais - 10 bolsistas parciais = 475`, então o numerador parece excluir integrais e parciais.
- O denominador 479 ainda precisa ser explicado.
- Validar se bolsista parcial deve ser excluído de pagantes ou incluído proporcionalmente.

### `[CANDIDATA]` Saldo líquido
```text
saldo_liquido = novas_matriculas - evasoes
```
- Print: `23 - 13 = 10`, bate com tela.

### `[DUVIDA]` ARR não é simplesmente MRR inteiro x 12 após arredondamento
- Print: `MRR = R$ 176.696`; `ARR = R$ 2.120.349`.
- `176.696 x 12 = 2.120.352`, diferença de R$ 3.
- Provável cálculo com centavos antes de arredondar, mas precisa validar.

### `[DUVIDA]` Inadimplência usa base diferente de previsto-realizado simples
- Print: previsto `R$ 176.696`, realizado `R$ 174.638`, diferença `R$ 2.058`.
- Diferença/previsto ≈ 1,16%, mas tela mostra `1,3%`.
- Precisa localizar fórmula real.

### `[DUVIDA]` Ticket médio não bate com MRR / alunos pagantes do card
- Print: `Ticket Médio = R$ 385`; `MRR = R$ 176.696`; pagantes `475`.
- `MRR / 475 ≈ R$ 372`.
- Precisa descobrir denominador/filtro do ticket médio.

### `[CANDIDATA]` Taxa de renovação
```text
taxa_renovacao = renovacoes / (renovacoes + nao_renovacoes) * 100
```
- Print: `38 / (38 + 5) = 88,37%`, bate com `88,4%`.
- Observação: aviso prévio aparece separado e aparentemente não entra nessa taxa.

### `[DUVIDA]` Churn possivelmente usa base de pagantes, não total ativo
- Print: `Total evasões = 13`, `Churn = 2,7%`.
- `13 / 499 = 2,61%` ≈ 2,6%.
- `13 / 475 = 2,74%` ≈ 2,7%.
- Indício de que churn pode usar base pagante, mas precisa confirmar na view/RPC.

### `[DUVIDA]` MRR perdido muito abaixo do ticket médio
- Print: `MRR perdido = R$ 1.719`; `total evasões = 13` → média ≈ R$ 132.
- Ticket médio exibido = R$ 385.
- Precisa validar se MRR perdido considera só cancelamentos, exclui não renovações, usa mensalidade líquida/descontos, ou há evasões sem valor.

## Evidência operacional — Relatório Administrativo Campo Grande 30/05/2026

### `[CANDIDATA]` Separação oficial entre alunos e matrículas
- Relatório diário da equipe separa:
  - `Alunos ativos = 499`
  - `Matrículas ativas = 565`
- Isso explica por que Kids + School pode passar do total de alunos: a contagem por produto parece ser por matrícula/curso, não por pessoa.
- Regra candidata: dashboards precisam deixar explícito quando contam pessoa (`alunos`) vs matrícula (`matrículas`).

### `[CANDIDATA]` Não pagantes = bolsistas integrais + bolsistas parciais
- Relatório: não pagantes = 24; bolsistas integrais = 14; bolsistas parciais = 10.
- `14 + 10 = 24`.
- Portanto, pelo relatório operacional, bolsista parcial está sendo tratado como não pagante para esse KPI.

### `[CANDIDATA]` Pagantes = ativos - não pagantes
- Relatório: ativos 499; não pagantes 24; pagantes 475.
- `499 - 24 = 475`.

### `[CANDIDATA]` Matrículas especiais dentro das matrículas ativas
- Matrículas ativas: 565.
- Matrículas em banda: 41.
- Matrículas de 2º curso: 28.
- Coral: 0.
- Precisa validar se banda e segundo curso estão incluídos dentro das 565 e quando são excluídos de KPIs.

### `[CANDIDATA]` Renovação do mês
- Total previsto: 43.
- Realizadas: 38.
- Não renovações: 5.
- Pendentes: 0.
- Taxa: `38 / 43 = 88,4%`.
- Equivalente a `38 / (38 + 5)` quando pendentes = 0.

### `[DIVERGENTE]` Avisos prévios
- Relatório administrativo: avisos prévios para sair em junho = 7.
- Print do dashboard: aviso prévio = 8.
- Pode ser diferença de data/hora, unidade, status, mês de referência ou inclusão de outro aviso.
- Precisa auditar fonte do card no frontend/view.

### `[CANDIDATA]` Evasões do mês
- Total evasões: 13.
- Interrompido: 8.
- Não renovou: 5.
- Interrompido 2º curso/bolsista/banda: 0.
- Transferência: 0.
- Bate com dashboard: cancelamentos 8 + não renovações 5 = 13.

## Validação do Alf — Campo Grande / 2026-05-31

### `[CANONICA]` Alunos ativos incluem trancados
- Definição validada pelo Alf: KPI “Alunos ativos” inclui alunos com status `ativo` + `trancado`.
- Observação: o nome “ativos” pode continuar se essa for a linguagem operacional da LA, mas a skill deve documentar que trancados entram na base.

### `[CANONICA]` Percentual Kids/School deve ser sobre matrículas
- Definição validada pelo Alf: Kids/School deve ser percentual sobre matrículas, não sobre alunos únicos.
- Correção recomendada no frontend: denominador de Kids/School deve ser `matriculas_ativas`/total de registros elegíveis, não `total_alunos_ativos` sem segundo curso.

### `[CANONICA]` Segundo curso
- Definição validada pelo Alf: segundo curso é quando aluno pagante faz segundo/terceiro curso pagando.
- Número correto Campo Grande em maio/2026: 28.
- Bolsista parcial não conta como segundo curso, mesmo se aparecer marcada no banco.
- Caso real: Vitória, funcionária/bolsista parcial, aparece elevando contagem para 29 no LA Report, mas não deve contar.
- Correção recomendada: segundo curso deve exigir pagante/regular e excluir bolsista integral/parcial, banda e não pagantes.

### `[CANONICA]` Trancados
- Número correto Campo Grande em maio/2026: 2.
- Banco/query direta mostrando 5 indica filtro ausente, dado sujo ou trancamento não elegível para relatório.
- Precisa listar os 5 registros para comparar com equipe/Hugo.

### `[EM AUDITORIA]` Fonte oficial de evasões
- Alf indicou que a fonte de verdade operacional provavelmente é `movimentacoes_admin`.
- Mas `evasoes_v2` contém histórico importante, especialmente tempo de permanência na saída.
- Decisão pendente: não aposentar `evasoes_v2` sem auditoria; precisa entender sincronização/histórico e talvez manter `movimentacoes_admin` como origem operacional + `evasoes_v2` como histórico analítico.

## Correção após novos prints frontend — Administrativo CG Mai/2026

### `[CANONICA]` Frontend Administrativo exibe trancados corretamente como 2
- Novos prints mostram Administrativo/Resumo com `Trancados = 2` e Lançamento Rápido/Movimentações com `Trancamento = 2`.
- Portanto, a divergência “banco 5 vs relatório 2” não significa que o frontend esteja errado; provavelmente está usando outro critério/fonte operacional correta.
- A auditoria deve separar: query bruta `alunos.status='trancado'` retorna 5, mas frontend operacional/relatório retorna 2.

### `[CANONICA]` Frontend Administrativo exibe renovação corretamente
- Novos prints mostram `Renovações = 38`, `Não renovação = 5`, `Taxa de renovação = 88,4%`.
- Portanto, o frontend visível está correto; o bug está nas views/SQL ou em campos não usados diretamente pelo card final.

### `[CANONICA]` Frontend Administrativo exibe evasões corretamente
- Novos prints mostram `Cancelamentos = 8`, `Não renovação = 5`, `Evasões = 13`, `Churn = 2,7%`, base `13 / 475`.
- Portanto, o frontend visível está correto; o problema de `vw_kpis_retencao_mensal.total_evasoes = 21` não está vazando para esse card final, ou o frontend corrige/recalcula.

### `[CANONICA]` Kids/School fecham com matrículas ativas
- Novos prints confirmam `Matrículas Ativas = 565`.
- Analytics mostra Kids 214 + School 351 = 565.
- Portanto, os cards Kids/School estão corretos como contagem de matrículas. Ajuste necessário é só garantir rótulo/denominador percentual sobre matrículas, não alunos únicos.

## Revisão de regra — Percentual Kids/School

### `[CORRIGIDA]` Percentual Kids/School deve ser sobre alunos ativos/pessoas, não matrículas brutas
- Alf questionou corretamente em 2026-05-31: matrículas incluem segundo curso, bandas e outros registros, então usar matrículas como denominador pode distorcer a leitura estratégica.
- Revisão: o KPI de mix Kids/School deve responder “qual perfil da base de alunos ativos?”, portanto o denominador deve ser alunos ativos/base de pessoas, não matrículas brutas.
- Para não duplicar aluno com segundo curso/banda, numerador e denominador devem usar a mesma base: alunos ativos incluindo trancados, excluindo segundo curso/projeto/banda quando necessário para representar pessoa.
- Problema atual do print: Kids 214 + School 351 = 565, mas total alunos ativos = 499; isso indica numerador por matrículas e denominador por alunos, gerando 43% + 70% = 113%.
- Regra ainda precisa fechar tecnicamente: como classificar pessoa que tem Kids + School ou múltiplos cursos? Possíveis critérios: idade atual principal, curso principal, ou segmento da matrícula principal.

## Tooltips do frontend — Analytics CG Mai/2026

### `[EVIDENCIA]` Total Alunos Ativos tooltip
- Texto: “Total de alunos com status ativo, excluindo segundo curso. Inclui pagantes e bolsistas.”
- Observação: tooltip fala status ativo; Alf validou que KPI inclui trancados também. Tooltip pode estar incompleto se trancados entram.

### `[EVIDENCIA]` Alunos Pagantes tooltip
- Texto: “Alunos ativos com tipo de matrícula pagante (exclui bolsistas integrais e segundo curso).”
- Observação: tooltip não cita bolsista parcial, mas regra validada pelo Alf exclui bolsista parcial também.

### `[EVIDENCIA]` LA Music Kids tooltip
- Texto: “Alunos com classificação LAMK (até 12 anos).”
- Observação: tooltip fala alunos/classificação, não matrículas. Se o número 214 vem de matrícula bruta, há divergência com o tooltip.

### `[EVIDENCIA]` LA Music School tooltip
- Texto: “Alunos com classificação EMLA (acima de 12 anos).”
- Observação: tooltip fala alunos/classificação, não matrículas. Se o número 351 vem de matrícula bruta, há divergência com o tooltip.

### `[DUVIDA]` Critério LAMK/EMLA
- Frontend tooltip usa classificação LAMK/EMLA, não simplesmente idade atual.
- Precisa validar se classificação vem do tipo de matrícula/segmento do curso ou idade calculada.
- Regra de negócio ainda pendente: Kids/School deve classificar alunos únicos pela classificação principal LAMK/EMLA, excluindo segundo curso, ou contar matrículas por classificação?

### `[CANONICA]` Matrículas Ativas
- Tooltip recebido: “Total de matrículas ativas incluindo primeiro curso, segundo curso, banda e coral.”
- Card Campo Grande Mai/2026: `Matrículas Ativas = 565`, com breakdown `28 2º curso | 41 banda | 0 coral`.
- Regra: matrícula ativa é contagem de registros/matrículas, incluindo primeiro curso, segundo curso pagante, banda e coral.
- Essa métrica é diferente de `Total Alunos Ativos` (499), que representa base de alunos/pessoas excluindo segundo curso.

### `[CANONICA]` Breakdown de matrículas ativas — Campo Grande Mai/2026
- Total matrículas ativas: 565.
- Segundo curso: 28.
- Banda: 41.
- Coral: 0.
- Portanto, o número correto de segundo curso operacional no frontend é 28; a query bruta `is_segundo_curso=true` com 66 mistura banda/bolsistas/outros registros que não pertencem ao KPI operacional de segundo curso pagante.

## Fonte técnica Kids/School — TabGestao.tsx

### `[CONFIRMADO]` Kids/School não vem de view; vem de query direta no frontend
- Arquivo: `src/components/GestaoMensal/TabGestao.tsx`.
- Linhas auditadas: bloco próximo de `alunosAtivosQuery`.
- Query atual:
  - tabela `alunos`
  - select `idade_atual, unidade_id`
  - filtro `status in ('ativo','trancado')`
  - filtro unidade quando selecionada
  - **não filtra `is_segundo_curso`**
- Cálculo atual:
  - Kids = `idade_atual <= 11`
  - School = `idade_atual >= 12`
- Resultado CG Maio/2026:
  - query atual: 565 linhas; Kids 214; School 351.
  - query corrigida excluindo segundo curso: 499 linhas; Kids 204; School 295.

### `[BUG FRONTEND]` Kids/School usa base diferente do Total Alunos Ativos
- Total Alunos Ativos da view exclui segundo curso: 499.
- Kids/School query atual inclui segundo curso: 565.
- Correção provável: adicionar `.or('is_segundo_curso.is.null,is_segundo_curso.eq.false')` na query de Kids/School, ou mover o cálculo para a view `vw_kpis_gestao_mensal` com os mesmos filtros.
- Após correção esperada em CG: Kids 204, School 295, total 499.

## Correção aplicada — Kids/School

### `[CORRIGIDO]` Frontend Kids/School alinhado com base de alunos ativos
- Print pós-correção recebido em 2026-05-31.
- Campo Grande Maio/2026 agora mostra:
  - Total Alunos Ativos: 499
  - LA Music Kids: 204 — 41%
  - LA Music School: 295 — 59%
- Soma Kids + School = 499, fechando com Total Alunos Ativos.
- Regra confirmada: Kids/School nessa área é distribuição da base de alunos ativos, não distribuição de matrículas.

## Auditoria — Reajuste Médio em tempo real

### `[PROBLEMA]` Card Reajuste Médio mostra 0.0% apesar de renovações com aumento
- Print recebido em 2026-05-31 mostra `Reajuste Médio = 0.0%`.
- Tooltip: “Percentual médio de aumento aplicado nas renovações do mês. Indica o poder de precificação.”
- Detalhamento operacional mostra renovações com +11%, +12%, etc.

### `[EVIDENCIA]` Fontes auditadas Campo Grande / Maio 2026
- `vw_kpis_gestao_mensal.reajuste_medio = 0.0`.
- `dados_mensais.reajuste_parcelas = 0.0`, além de outros campos defasados (`alunos_pagantes=481`, `novas_matriculas=29`).
- Tabela `renovacoes`: 61 linhas `status=renovado`, mas `valor_parcela_novo` majoritariamente nulo e `percentual_reajuste` nulo/0; média = 0.
- Tabela `movimentacoes_admin`: 38 linhas `tipo=renovacao`, batendo com relatório operacional; 25 com valores anterior/novo preenchidos.
- Média calculada em `movimentacoes_admin`:
  - todos com valor anterior/novo: ~12,44%.
  - apenas aumentos positivos: ~12,95%.
  - aumentos positivos diluídos por todas as 38 renovações: ~8,18%.

### `[CANONICA EM ANDAMENTO]` Mês atual não deve depender de snapshot
- Alf validou em 2026-05-31 que métricas do mês atual devem refletir movimentos operacionais em tempo real.
- `dados_mensais` deve existir como histórico/fechamento, mas não ser fonte viva do mês corrente quando houver tabela operacional.

### `[PENDENTE]` Regra exata do denominador do Reajuste Médio
- Tooltip fala “aumento aplicado”, então recomendação inicial: média apenas dos aumentos positivos aplicados.
- Alternativa: média de todas as renovações com valor anterior/novo, incluindo zero/queda.
- Alternativa 2: diluir por todas as renovações do mês, tratando sem aumento/sem valor como 0.
- Precisa validação final do Alf antes de canonizar.

### `[CANONICA]` Denominador do Reajuste Médio
- Alf validou em 2026-05-31: valor com 0 não é para considerar.
- Reajuste Médio deve considerar somente renovações com aumento positivo.
- Registros com reajuste 0 ou sem valor anterior/novo ficam fora da média.
- Para Campo Grande/Maio 2026, auditoria preliminar indicou média esperada aproximada de 12,95% se calculada a partir de `movimentacoes_admin` com aumentos positivos.
- Antes de corrigir, Windsurf deve investigar e constatar a causa com queries no repo e banco.

## Diagnóstico Windsurf confirmado — Reajuste Médio

### `[CONFIRMADO]` Causa raiz
- Card frontend: `src/components/GestaoMensal/TabGestao.tsx`, `dados.reajuste_pct`.
- Para mês atual, o campo vem de `vw_kpis_gestao_mensal.reajuste_medio`.
- Definição real da view usa `renovacoes.percentual_reajuste`.
- Tabela `renovacoes` está com poucos `percentual_reajuste` preenchidos e todos os preenchidos em 0; por isso a view retorna 0 para todas as unidades.
- Fonte operacional real para o reajuste visível no detalhamento é `movimentacoes_admin`, com `tipo='renovacao'`, `valor_parcela_anterior` e `valor_parcela_novo`.

### `[CANONICA]` Reajuste Médio
- Considerar somente renovações com aumento positivo.
- Ignorar reajuste 0.
- Ignorar registros sem `valor_parcela_anterior` ou `valor_parcela_novo`.
- Fonte atual recomendada: `movimentacoes_admin`.
- Valores esperados Maio/2026:
  - Campo Grande: 12,95%.
  - Recreio: 10,41%.
  - Barra: 8,70%.

### `[CUIDADO]` Correção mínima
- Não substituir a CTE `renovacoes_mes` inteira sem revisar `renovacoes`, `total_contratos` e `taxa_renovacao`.
- O mais seguro agora é criar/usar uma CTE separada `reajuste_mes` baseada em `movimentacoes_admin` e trocar apenas o campo final `reajuste_medio`.
- `taxa_renovacao` e contagem de renovações seguem como auditoria separada.
