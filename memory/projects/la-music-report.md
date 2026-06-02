# LA Music Report

- **Status:** ✅ Em produção
- **Stack:** Supabase, React/TypeScript, Tailwind
- **Descrição:** Plataforma central de KPIs e gestão — 78 KPIs, 7 domínios, Chrome Extension WhatsApp
- **Próximo passo:** monitorar e manter
- **Bloqueios:** nenhum conhecido

## 2026-06-01 — Nomenclatura operacional

- Sistema correto: **LA Report**.
- Agente/dev no Windsurf: **Cascade**.
- Evitar “LAHQ” para esse fluxo de investigação financeira/ticket de alunos.
- Evitar “Mutsaf”; foi erro de nomenclatura.

## 2026-06-01 — Hipótese de arquitetura: banda/projeto vs segundo curso

Alf identificou conflito conceitual no formulário de aluno: a UI mostra apenas `is_segundo_curso` (“É segundo curso”), então alunos de banda/projeto acabam marcados como segundo curso, embora operacionalmente banda/projeto não seja segundo curso financeiro.

Achado no código:
- `ModalFichaAluno.tsx` tem checkbox `is_segundo_curso`, mas não expõe marcação de banda/projeto no aluno.
- `cursos.is_projeto_banda` existe e é configurável em `ConfigPage.tsx`.
- `AlunosPage.tsx` já separa banda por `cursos.is_projeto_banda === true` e segundo curso como `is_segundo_curso && !is_projeto_banda`.
- Migration `20260331_auto_detect_segundo_curso_banda.sql` detecta banda por nome `ILIKE '%banda%'`, o que não pega nomes como Power Kids. Isso pode explicar Power Kids entrando apenas como segundo curso.

Direção provável: manter banda/projeto como propriedade do curso (`cursos.is_projeto_banda`) e ajustar UI/automação/regras para não tratar esses casos como segundo curso financeiro.

## 2026-06-01 — Correção aplicada por Cascade: banda/projeto vs segundo curso

Cascade confirmou a raiz e aplicou correções cirúrgicas no LA Report:

- Problema: `is_segundo_curso` (tabela `alunos`) estava sendo usado como conceito financeiro de curso adicional, enquanto `is_projeto_banda` (tabela `cursos`) representa projeto/banda. A UI só oferecia “É segundo curso”, levando Power Kids/Minha Banda Para Sempre a cair no fluxo de segundo curso.
- Correções aplicadas:
  - `TabelaAlunos.tsx`: coluna Parcela exibe valor do curso pagante quando principal é banda/projeto com NULL/0.
  - `AlunosPage.tsx`: promoção do curso pagante para principal na tabela quando principal é banda/projeto zerado; totalPagantes agora conta `DISTINCT nome` com `conta_como_pagante=true` e `valor_parcela > 0`, independente de `is_segundo_curso`.
  - `TabProfessoresNew.tsx`: ticket médio usa `Set(nome)` em vez de excluir `is_segundo_curso` cegamente.
  - `TabGestao.tsx`: fallback de KPIs usa `Set(nome)` e exige `valor_parcela > 0` para pagantes.
- Type-check passou nos arquivos editados; erro restante em `scripts/importar_historico_ltv.js` é encoding não relacionado.
- Pendência técnica recomendada: UI/formulário deve distinguir explicitamente “curso adicional financeiro” de “projeto de banda”, baseado em `curso_id`/`cursos.is_projeto_banda`, para a operação não precisar usar checkbox de segundo curso em casos de banda.
- Pendência data-level: tipo de matrícula de banda/projeto no banco idealmente deveria ter `conta_como_pagante=false` e `entra_ticket_medio=false`; isso é ajuste cadastral/dados, não só código.

## 2026-06-01 — Incidente pós-correção banda/segundo curso: card Gestão Maio/2026 errado

Alf percebeu no print do Dashboard/Gestão/Alunos, Campo Grande, Mai/2026: Total Alunos Ativos = Alunos Pagantes = 466; Banda = 0; Bolsistas Integrais/Parciais = 0.

Auditoria direta no Supabase LA Report mostrou que o banco NÃO zerou bandas/bolsistas:
- `tipos_matricula`: REGULAR, SEGUNDO_CURSO, BOLSISTA_INT/PARC e BANDA continuam corretos; BANDA com `conta_como_pagante=false` e `entra_ticket_medio=false`.
- Cursos `is_projeto_banda=true`: Power Kids, Minha Banda Para Sempre, GarageBand, Percussion Kids, Canto Coral, Teoria Musical, Circuito de Férias 1/2.
- Leitura completa de alunos ativos/trancados/aviso: 1.232 registros.
- Campo Grande raw atual: 555 registros, 492 pessoas, 464 pessoas pagantes por valor positivo, 29 registros bolsistas/26 pessoas bolsistas, 40 registros de banda/35 pessoas banda, 27 registros segundo curso.
- `dados_mensais` CG Mai/2026 contém valores corretos: `alunos_ativos=492`, `alunos_pagantes=466`, `matriculas_ativas=556`, `matriculas_banda=41`, `matriculas_2_curso=64`.

Bug encontrado no código local `DashboardPage.tsx`: para período histórico usando `dados_mensais`, o map faz:
- `total_alunos_ativos: d.alunos_pagantes || 0`
- `total_alunos_pagantes: d.alunos_pagantes || 0`
Isso explica ativo=pagante no print. O problema é mapeamento/cálculo de dashboard histórico, não migration destrutiva no banco.

Próxima orientação ao Cascade: não mexer mais no banco; corrigir Dashboard/Gestão para usar campos corretos de `dados_mensais` (`alunos_ativos`, `alunos_pagantes`, `matriculas_banda`, `matriculas_2_curso`) e tratar bolsistas via fonte oficial ou adicionar snapshot no histórico, sem fallback zerado enganoso.

## 2026-06-01 — Confirmação do Alf: bug persiste em Maio/2026

Alf confirmou por print que o problema persiste em Maio/2026: Dashboard/Gestão continua exibindo 466 tanto para alunos ativos quanto para alunos pagantes. Isso reforça que a correção necessária é no mapeamento/fonte do Dashboard histórico, não na migration de banda/segundo curso.

Direção: pedir ao Cascade para corrigir explicitamente o branch histórico do Dashboard que lê `dados_mensais`, usando `alunos_ativos` para Total Alunos Ativos e `alunos_pagantes` para Pagantes. Não tratar como problema de snapshot visual/cache.

## 2026-06-01 — Débito pago: UI separa Projeto/Banda de Segundo Curso

Cascade aplicou ajuste arquitetural no LA Report para separar visual/operacionalmente projeto/banda de segundo curso financeiro:

- `ModalFichaAluno.tsx`: quando curso principal muda, detecta `is_projeto_banda=true`, zera `is_segundo_curso` e seta `tipo_matricula_id=5`.
- Checkbox “É segundo curso”: quando o curso principal é banda/projeto, a UI exibe badge “Projeto/Banda” em vez de induzir marcação como segundo curso.
- Outros cursos: cards agora exibem badge “Projeto/Banda” ou “2º curso” conforme categoria.
- Adicionar curso: se o curso selecionado for banda, salva com `tipo_matricula_id=5` e `is_segundo_curso=null` automaticamente.
- `ModalNovoAluno.tsx`: adicionou `tipo_matricula_id` ao formData; ao selecionar curso banda/projeto, ajusta tipo para 5 e preserva na inserção.
- Interfaces atualizadas (`TabelaAlunos.tsx`, `ModalFichaAluno.tsx`, `ModalNovoAluno.tsx`) para carregar `is_projeto_banda`.
- Type-check passou nos arquivos alterados; erros restantes são preexistentes no script `importar_historico_ltv.js` por encoding.

Print validado pelo Alf mostra cards de Outros Cursos com badge “Projeto/Banda” para Power Kids e Minha Banda Para Sempre. Atenção futura: um Power Kids apareceu com valor R$40 no print; validar se isso é regra real, taxa simbólica, dado residual ou deve ser zerado/excluído do ticket.

## 2026-06-01 — Correção aplicada: histórico do Dashboard/Gestão

Cascade identificou e corrigiu o bug real dos dados históricos:

Arquivos afetados:
- `src/components/App/Dashboard/DashboardPage.tsx`
- `src/components/GestaoMensal/TabGestao.tsx`
- `src/hooks/useKPIsGestao.ts`

Problema corrigido:
- Histórico estava mapeando `total_alunos_ativos = d.alunos_pagantes` e `total_alunos_pagantes = d.alunos_pagantes`.
- `TabGestao` também zerava `total_bolsistas_integrais`, `total_bolsistas_parciais` e `total_banda` no histórico.
- `useKPIsGestao` repetia inversão no fallback histórico e no comparativo de mês anterior.

Regra arquitetural aplicada:
- Mês fechado/histórico usa snapshot de `dados_mensais`.
- Mês atual usa fonte viva/operacional.
- Fallback só recalcula quando não existe snapshot em `dados_mensais`.

Mapeamento histórico corrigido:
- `total_alunos_ativos = d.alunos_ativos`
- `total_alunos_pagantes = d.alunos_pagantes`
- `total_banda = d.matriculas_banda`
- `total_bolsistas_integrais = d.bolsistas_integrais`
- `total_bolsistas_parciais = d.bolsistas_parciais`

Validação esperada para Campo Grande/Maio 2026:
- Alunos Ativos: 492
- Alunos Pagantes: 466
- Matrículas Ativas: 556
- Banda: 41
- 2º Curso: 64

Type-check segue com erro preexistente em `scripts/importar_historico_ltv.js`, não causado por essa correção.

## 2026-06-01 — Histórico ainda errado: matrículas e bolsistas Maio/CG

Após correção do mapeamento ativos/pagantes, Alf apontou novos erros no Dashboard/Gestão Campo Grande/Maio 2026:
- `Novas Matrículas` aparece 21, mas fechamento validado pelo Alf é **23**.
- `Bolsistas Integrais` e `Bolsistas Parciais` aparecem 0, mas banco atual mostra bolsistas ativos em CG.

Memória validada anteriormente após Marcos inativo: CG/Maio fechamento canônico parcial:
- alunos ativos: 496
- alunos pagantes: 470
- matrículas ativas: 561
- banda/projeto: 41
- segundo curso operacional: 27
- coral: 0
- novas matrículas: 23
- evasões: 13
- churn: 2,77%

Auditoria direta atual no banco para CG (ativo/trancado/aviso) retornou bolsistas por pessoa:
- 26 pessoas bolsistas total
- 16 `BOLSISTA_INT`
- 10 `BOLSISTA_PARC`
- 29 registros de matrícula bolsista (alguns com segundo curso/linha extra)

Hipótese: `dados_mensais` não tem colunas de bolsistas ou está sem snapshot desses campos; o frontend mapeia `d.bolsistas_integrais/parciais`, que não existem/estão null, gerando 0. Além disso, `dados_mensais.novas_matriculas=21` está desatualizado contra fechamento validado de 23.

Próximo passo: Cascade deve auditar e corrigir a fonte histórica/snapshot, não apenas frontend. É preciso versionar/backfillar os campos históricos necessários em `dados_mensais` ou definir uma fonte histórica confiável, e atualizar CG/Maio com fechamento validado.

## 2026-06-01 — Guardrail para plano de backfill histórico dados_mensais

Cascade propôs adicionar colunas `bolsistas_integrais` e `bolsistas_parciais` em `dados_mensais`, atualizar `recalcular_dados_mensais` e rodar recalc/backfill para 2026.

Avaliação operacional: não aprovar backfill em massa ainda. Risco alto de reescrever histórico Jan-Abr/2026 com estado atual da tabela `alunos`, caso a função não use fonte temporal confiável. Mês fechado deve permanecer snapshot do fechamento, não recálculo retroativo do cadastro atual.

Guardrail aprovado:
- Pode criar colunas faltantes, preferencialmente com migration versionada.
- Pode atualizar função de cálculo, mas antes precisa mostrar SQL da função e provar que calcula por competência/data histórica, não pelo status atual.
- Pode rodar dry-run/SELECT para Maio/2026 e comparar com fechamento validado do Alf antes de UPDATE/UPSERT.
- Não rodar recalc para Jan-Abr/2026 ou meses anteriores sem matriz de comparação e fonte temporal confiável.
- Backfill de bolsistas históricos só é confiável se houver snapshot/fonte histórica; se usar estado atual, deve ficar marcado como aproximação, não verdade histórica.

Alerta: recalc mostrado por Cascade para CG/Maio retornou `alunos_ativos=489`, `alunos_pagantes=463`, `matriculas_ativas=552`, `matriculas_banda=40`, `novas_matriculas=23`, `matriculas_2_curso=27`, `evasoes=13`. Isso diverge de números validados anteriormente em memória (ex.: 496/470/561 ou snapshot anterior 492/466/556), então precisa validação nominal antes de aceitar como fechamento definitivo.

## 2026-06-01 — Regressão Kids/School calculando sobre matrículas/segundo curso

Alf enviou print mostrando LA Music Kids = 206 (42%) e LA Music School = 320 (65%). A soma 206+320=526 ultrapassa a base de alunos ativos, sinal de que voltou a contar segundo curso/banda/matrículas em vez de pessoas ativas.

Regra canônica já validada: Kids/School é distribuição sobre a mesma base de `Total Alunos Ativos` (pessoas), incluindo trancados se entram na base, excluindo segundo curso e banda/projeto para não duplicar pessoa. Não é distribuição sobre matrículas ativas.

Prompt recomendado ao Cascade: corrigir cards Kids/School para usar fonte histórica/snapshot coerente com `alunos_ativos` ou cálculo por pessoa distinta com a mesma base, nunca somar linhas de matrícula/segundo curso.

## 2026-06-01 — Relatório Cascade: segurança histórica e regressão Kids/School

Cascade reportou:
- `recalcular_dados_mensais` é baseada em competência (`data_matricula <= fim_mes` e `data_saida IS NULL OR data_saida > fim_mes`, status ativo/trancado), mas consulta os registros atuais da tabela `alunos`; portanto respeita data de competência, mas correções retroativas de cadastro podem mudar o passado.
- Dry-run CG/Maio 2026 divergiu do snapshot pós-recalc por 1 em ativos/pagantes/matrículas: dry-run 488/462/551 vs snapshot 489/463/552; novas_matriculas=23 e evasões=13.
- Regressão Kids/School encontrada em `TabGestao.tsx:696-711`: query não exclui banda/projeto, não filtra período histórico, não deduplica por pessoa (`DISTINCT nome`) e conta registros/matrículas.
- Colunas `bolsistas_integrais` e `bolsistas_parciais` foram adicionadas em `dados_mensais`; nenhum backfill executado.

Decisão recomendada ao Alf: aprovar apenas a correção A (Kids/School frontend), por ser leitura/UI e corrigir regressão clara. Não aprovar ainda B (alterar função `recalcular_dados_mensais`) nem C (backfill), até validação nominal e decisão sobre confiabilidade histórica.

## 2026-06-01 — Alf rejeita remendo em bolsistas sem resolver arquitetura histórica

Alf deixou claro que não quer apenas mexer no cálculo de bolsistas dentro de `recalcular_dados_mensais` se isso continuar baseado no estado atual da tabela `alunos`. O problema central é maior: dado histórico precisa representar o fechamento do mês, não o cadastro atual filtrado retroativamente.

Resposta recomendada ao Cascade:
- Não aplicar o diff dos bolsistas ainda.
- A etapa B é tecnicamente plausível para card de bolsistas, mas continua sendo remendo se a função recalcula passado com cadastro atual.
- Antes de mexer, investigar a causa raiz da queda de 470 para 463 e definir arquitetura de snapshot/fechamento mensal imutável com retificação controlada.
- Exigir auditoria nominal dos 7 pagantes perdidos e matriz de fonte por KPI: snapshot fechado vs cálculo vivo.

## 2026-06-01 — Cascade confirma contaminação histórica por cadastro vivo

Cascade auditou e confirmou: histórico está sendo contaminado. `recalcular_dados_mensais` respeita competência (`data_matricula <= fim_mes`, `data_saida > fim_mes`), mas lê os registros atuais de `alunos`. Assim, alterações feitas em 01/06 em `tipo_matricula`, `is_segundo_curso`, `curso_id`, `status` ou `data_saida` mudam retroativamente Maio.

Exemplos encontrados no audit_log:
- Vitória Vívia dos Santos Costa: `tipo_matricula_id` Regular → Bolsista Parcial em 2026-06-01 23:25; sai de pagantes de Maio.
- Matheus Reis da Silva Gaspar: Regular → Bolsista Integral em 2026-06-01 00:04; sai de pagantes de Maio.
- Miguel Gomes Biancamano: Regular → Bolsista Integral em 2026-06-01 00:03; sai de pagantes de Maio.
- Guilherme Martins Santos: ativo → evadido com `data_saida=2026-06-01`; não deveria afetar Maio se regra data_saida > fim_mes estiver correta, mas evidencia mudanças pós-fechamento.

Cascade ainda não fechou os 7 nomes exatos que explicam queda de 470 para 463. Próximo passo recomendado: auditoria nominal dos 7 pagantes perdidos, sem aplicar patch/recalc/backfill.

Arquitetura recomendada pelo Cascade e alinhada com Alf/Alfredo:
- `dados_mensais` deve virar fechamento oficial mensal congelado, não snapshot regravável silenciosamente.
- Mês atual usa cálculo vivo.
- Mês fechado usa snapshot congelado.
- Retificação histórica deve ser processo separado com antes/depois, motivo, autor, timestamp e lista nominal impactada.
- Frontend nunca deve recalcular histórico a partir de `alunos`.

## 2026-06-01 — Coração da gambiarra encontrado: duas rotinas conflitantes gravam dados_mensais

Cascade investigou a transição 470 -> 466 às 03:00 e encontrou a causa principal:
- `audit_log` mostra `dados_mensais` CG/Maio atualizado em `2026-06-01 03:00:00.066604+00` por `usuario=system`, `origem=system`, `acao=UPDATE`.
- A mudança bate mais com a função antiga/problematica `fechar_dados_mensais` do que com `recalcular_dados_mensais`.
- Antes, às 02:56:22, snapshot estava correto pela regra nova: `496/470/561/41/27/23`.
- Às 03:00, rotina automática sobrescreveu com regra antiga: `492/466/556/41/64/21`.
- `matriculas_2_curso` pulou de 27 para 64 porque `fechar_dados_mensais` conta todo `is_segundo_curso=true` e não exclui banda/projeto.
- `novas_matriculas` caiu de 23 para 21 porque `fechar_dados_mensais` usa regra antiga/mais rígida (`tm.conta_como_pagante=true`, sem filtros refinados de banda/coral e usando cadastro atual).

Diagnóstico: existem múltiplas rotinas escrevendo `dados_mensais` com regras divergentes. A transição 470 -> 466 não foi principalmente nominal; foi sobrescrita automática por rotina antiga/incompatível, provavelmente `fechar_dados_mensais`.

Próximo passo seguro: rastrear quem chama `fechar_dados_mensais` (cron, trigger, botão, edge function, RPC encadeada) antes de aplicar qualquer patch. Depois desativar/substituir rotina antiga por fluxo único de fechamento mensal imutável com retificação controlada.

## 2026-06-01 — Chamador exato da sobrescrita histórica encontrado

Cascade localizou o chamador que sobrescreveu `dados_mensais` às 03:00:
- `pg_cron` job `snapshot_dados_mensais_mensal`
- schedule: `0 3 1 * *`
- comando: `SELECT snapshot_dados_mensais(EXTRACT(YEAR FROM (CURRENT_DATE - INTERVAL '1 day'))::INTEGER, EXTRACT(MONTH FROM (CURRENT_DATE - INTERVAL '1 day'))::INTEGER);`

A função `snapshot_dados_mensais` é uma segunda calculadora antiga/incompatível, distinta de `recalcular_dados_mensais`, e grava na mesma tabela `dados_mensais` com `ON CONFLICT DO UPDATE`.

Problemas da função antiga:
- `matriculas_2_curso`: conta `status='ativo' AND is_segundo_curso=true`, sem excluir banda/projeto.
- `novas_matriculas`: usa `leads WHERE status IN ('matriculado','convertido')`, não a regra refinada baseada em alunos.
- usa status/contagens atuais e lógica antiga.

Diagnóstico final desta etapa: a transição 470 -> 466 às 03:00 foi causada por `pg_cron` chamando `snapshot_dados_mensais`, que sobrescreveu o snapshot correto das 02:56 com regra antiga.

Próximo passo recomendado: mapear todas as rotinas que escrevem `dados_mensais`, decidir qual fica, qual desativa e qual vira retificação explícita. Não aplicar patch ainda sem mapa completo.

## 2026-06-01 — Mapa completo das rotinas que escrevem dados_mensais

Cascade finalizou o mapa de escritores de `dados_mensais`:

1. `snapshot_dados_mensais`
- Chamado por `pg_cron` job `snapshot_dados_mensais_mensal` (`0 3 1 * *`).
- Usa regra antiga/incompatível.
- Recomendação: desativar/substituir.

2. `recalcular_dados_mensais(p_ano,p_mes,p_unidade_id)`
- Chamada manual/RPC SQL.
- Regra mais refinada.
- Candidata a rotina oficial de fechamento/retificação controlada, desde que com preview, diff, aprovação e audit log.

3. `fechar_dados_mensais(p_ano,p_mes)`
- Legado/sob demanda.
- Regra antiga/conflitante.
- Recomendação: descontinuar.

4. `upsert_dados_mensais`
- Chamado manualmente pelo app via `supabase.rpc`, arquivo `src/hooks/useSupabaseMutations.ts`.
- Upsert parcial; não recalcula base completa.
- Recomendação: virar retificação explícita com diff/log/aprovação.

5. `sync_evasao_to_dados_mensais`
- Trigger em `movimentacoes_admin`; atualiza evasões/churn incrementalmente.
- Recomendação: manter só se compatível com snapshot congelado; caso contrário mover para fluxo de retificação/event sourcing.

6. Triggers de auditoria `tr_audit_dados_mensais`/`tr_audit`
- Apenas logam; manter.

7. Trigger `tr_dados_mensais_updated_at`
- Atualiza `updated_at`; manter.

Decisão recomendada: não aplicar patch ainda; pedir desenho de migration segura para desativar/substituir escritores conflitantes e consolidar fluxo único de fechamento mensal + retificação explícita.

## 2026-06-01 — Plano de substituição segura proposto por Cascade

Cascade propôs plano em fases para resolver a arquitetura histórica de `dados_mensais`:

Fase 1 — Segurança imediata:
- Neutralizar/desagendar o `pg_cron` job `snapshot_dados_mensais_mensal`.
- Não apagar `snapshot_dados_mensais` ainda.
- Rollback possível via `cron.schedule(...)` recriando o job.

Fase 2 — Fonte oficial única:
- Usar `recalcular_dados_mensais` como motor de cálculo, mas não como “grava direto”.
- Criar fluxo `preview_recalculo_dados_mensais` (não grava) e `aplicar_retificacao_dados_mensais` (grava com aprovação).
- Criar tabela `dados_mensais_retificacoes` com unidade, ano, mês, motivo, solicitante, aprovador, snapshot antes/depois, diff e timestamp.

Fase 3 — Legados:
- `fechar_dados_mensais`: marcar como deprecated e depois trocar corpo por erro explícito.
- `snapshot_dados_mensais`: manter temporariamente para compatibilidade histórica, documentar como legado e depois bloquear/renomear.
- `upsert_dados_mensais`: restringir para mês fechado; mês fechado só via retificação.
- `sync_evasao_to_dados_mensais`: no primeiro passo, trigger só atua no mês corrente; mês fechado não atualiza histórico automaticamente.

Fase 4 — Frontend/regra:
- Mês atual pode usar cálculo vivo.
- Mês fechado lê exclusivamente `dados_mensais`.
- Histórico/comparativos usam `dados_mensais`.
- Retificação via fluxo explícito, nunca cálculo implícito na tela.

Recomendação Alfredo: aprovar apenas Fase 1 primeiro, como migração isolada de contenção. Antes das fases 2-7, exigir migrations separadas, com SQL completo e testes/preview. Fase 1 não altera dados nem função, só impede a rotina antiga automática de sobrescrever fechamento.

## 2026-06-02 — Fase 1 executada: cron legado neutralizado

Cascade executou somente a contenção aprovada:
- Desagendou o `pg_cron` job legado `snapshot_dados_mensais_mensal`.
- Não alterou `snapshot_dados_mensais`.
- Não recalculou dados.
- Não mexeu em funções.
- Não alterou `dados_mensais`.

Confirmações pós-execução:
- `cron.job` não retorna mais `snapshot_dados_mensais_mensal`.
- CG/Maio em `dados_mensais` permaneceu idêntico após a migration:
  - `alunos_ativos=489`
  - `alunos_pagantes=463`
  - `matriculas_ativas=552`
  - `matriculas_banda=40`
  - `matriculas_2_curso=27`
  - `novas_matriculas=23`
  - `evasoes=13`
  - `churn_rate=2.81`
  - `ticket_medio=368.66`
  - `updated_at=2026-06-01 23:06:57.152081+00`
- Nenhuma função alterada.
- Nenhum recálculo executado.

Artefato final: `docs/MIGRACAO_FASE1_NEUTRALIZAR_CRON_SNAPSHOT_DADOS_MENSAIS.sql`, organizado em PRE-CHECK, MIGRATION, POST-CHECK e ROLLBACK.

Status: contenção aplicada; escritor automático antigo neutralizado; histórico não foi corrigido ainda, apenas protegido contra nova sobrescrita automática por esse cron. Próxima fase deve ser desenho/preview do fluxo de retificação e restauração controlada do fechamento validado, sem backfill em massa.

## 2026-06-02 — Revisão Fase 2 proposta de retificação

Alf/Cascade enviaram `MIGRACAO_FASE2_FLUXO_RETIFICACAO_DADOS_MENSAIS_PROPOSTA.sql`. Revisão Alfredo:
- Aceitar como desenho arquitetural/proposta, não como migration executável ainda.
- Pontos positivos: tabela `dados_mensais_retificacoes`, diff JSONB, contrato de preview, apply com motivo/solicitante/aprovador, rollback documentado e sem intenção de recalcular Maio.
- Ponto crítico: `preview_retificacao_dados_mensais` ainda não calcula snapshot real; retorna placeholder `PROPOSTA_NAO_EXECUTAVEL_AINDA`.
- `aplicar_retificacao_dados_mensais` depende desse preview e fica bloqueada; portanto a Fase 2 não resolve retificação operacional ainda.
- Próximo passo correto: Fase 2A, extrair a lógica de `recalcular_dados_mensais` para uma função pura/preview-only que retorne o snapshot proposto sem `UPDATE/UPSERT`; só depois revisar apply real.
- Não executar esse SQL em produção/dev como migration ainda, exceto se for apenas documentação. Primeiro revisar função pura e riscos de `upsert_dados_mensais`/`sync_evasao_to_dados_mensais` para mês fechado.

## 2026-06-02 — Revisão Fase 2A cálculo puro

Cascade enviou `MIGRACAO_FASE2A_CALCULO_PURO_SNAPSHOT_DADOS_MENSAIS_PROPOSTA.sql`. Revisão Alfredo:
- A direção está correta: separar motor de cálculo da camada de persistência.
- A função proposta `calcular_snapshot_dados_mensais(p_ano,p_mes,p_unidade_id)` não possui INSERT/UPDATE/UPSERT/DELETE e retorna JSONB; isso atende ao princípio de função pura sem side effects.
- Ainda não aprovar execução como migration: primeiro pedir versão integrada ao preview e prova/validação.
- Ponto crítico: a função ainda calcula a partir do estado atual de `alunos`; portanto é segura como preview do cálculo atual/retificação, mas não recupera sozinha o fechamento original de Maio. Para restaurar 470 será necessário comparar com snapshot validado/audit log/matriz nominal.
- Riscos mantidos: `COUNT(DISTINCT nome)` pode conflitar com homônimos; financeiro/ticket não está no escopo; `movimentacoes_admin` segue fonte das evasões.
- Próximo pedido ao Cascade: gerar Fase 2A-REV ou complemento com `preview_retificacao_dados_mensais` consumindo `calcular_snapshot_dados_mensais`, retornando snapshot_atual/snapshot_proposto/diff real, ainda sem apply e sem escrita em `dados_mensais`; incluir SQL de validação que prove ausência de side effects.

## 2026-06-02 — Fase 2A-REV normalizada sobrescrita

Cascade sobrescreveu `MIGRACAO_FASE2A_REV_PREVIEW_INTEGRADO_PROPOSTA.sql` com a versão normalizada do Alfredo. Revisão:
- O contrato foi corrigido: `snapshot_atual_dados_mensais_alunos_matriculas` monta JSONB com os mesmos campos do snapshot proposto.
- `preview_retificacao_dados_mensais` agora compara snapshot atual normalizado vs `calcular_snapshot_dados_mensais`.
- `diff_jsonb_flat` ganhou `STABLE` e `ORDER BY key`, tornando saída determinística.
- Validações ficaram comentadas/manual, não embutidas como SELECT ativo na migration.
- Apply segue bloqueado; arquivo permanece PROPOSTA.

Status recomendado: aprovar o arquivo como proposta revisada/base técnica. Ainda não executar em produção. Se for testar, primeiro aplicar em dev/staging apenas, confirmando pré-requisito `calcular_snapshot_dados_mensais`, depois rodar PRE/POST check e preview, provando que `dados_mensais.updated_at` não muda e que o diff não inclui metadata/financeiro.

## 2026-06-02 — Teste SELECT-only do preview normalizado em produção

Como Supabase branch dev veio vazio (`with_data=false`) e não havia `dados_mensais/alunos/movimentacoes_admin`, Cascade executou teste SELECT-only em produção/main, sem criar funções permanentes e sem alterar dados.

Confirmações:
- Nenhuma função criada no banco.
- Nenhum UPDATE/INSERT/UPSERT/DELETE.
- `dados_mensais` não alterado.
- PRE-CHECK e POST-CHECK idênticos; `updated_at` preservado.
- Diff limpo: não apareceu `id`, `created_at`, `updated_at`, `ticket_medio` nem financeiro.

Snapshot atual CG/Maio em `dados_mensais`: `alunos_ativos=489`, `alunos_pagantes=463`, `matriculas_ativas=552`, `matriculas_banda=40`, `matriculas_2_curso=27`, `novas_matriculas=23`, `evasoes=13`, `churn_rate=2.81`, `ticket_medio=368.66`.

Preview/cálculo vivo atual para Maio retornou: `alunos_ativos=475`, `alunos_pagantes=445`, `matriculas_ativas=538`, `matriculas_banda=40`, `matriculas_2_curso=27`, `novas_matriculas=23`, `evasoes=13`, `churn_rate=2.92`.

Conclusão: preview normalizado funciona e é read-only seguro; também prova que cálculo vivo atual diverge ainda mais do fechamento, reforçando que não deve ser usado para regravar Maio sem fonte histórica/retificação nominal. Branches vazios criados para teste (`dev-teste-fase2a`, `dev-teste-fase2a-com-dados`) podem ser deletados para parar custo, pois não foram usados.

## 2026-06-02 — Relatório forense Maio/CG recebido: fonte confiável encontrada

Cascade entregou `RELATORIO_AUDITORIA_FORENSE_MAIO_CG_2026.md`. Ponto principal: o `audit_log` preserva o `old_record` do update do cron legado às 03:00 de 01/06/2026, contendo o último snapshot válido antes da contaminação:
- `alunos_ativos=496`
- `alunos_pagantes=470`
- `matriculas_ativas=561`
- `matriculas_banda=41`
- `matriculas_2_curso=27`
- `novas_matriculas=23`
- `evasoes=13`
- `churn_rate=2.77`

Cronologia documentada:
- 31/05 23:45: `500/474/566/43/66/23/13`
- 01/06 02:56: `496/470/561/41/27/23/13` — snapshot válido.
- 01/06 03:00: cron legado sobrescreveu para `492/466/556/41/64/21/13`.
- 01/06 23:06: recálculo posterior deixou `489/463/552/40/27/23/13`.
- cálculo vivo atual: `475/445/538/40/27/23/13`.

Revisão Alfredo: relatório é suficiente para propor retificação controlada de Maio/CG usando o old_record como fonte primária. Antes de executar, pedir migration/proposta de retificação isolada: inserir log em `dados_mensais_retificacoes`, atualizar somente campos alunos/matrículas/churn do registro CG/Maio, preservar financeiro/ticket/saldo/inadimplência, incluir PRE/POST e rollback para o estado atual `489/463/552/40/27/23/13/2.81`. Atenção: corrigir no relatório a explicação de evasões de Junho — se a regra temporal usa `data_saida > fim_mes`, data_saida 01/06 não deveria excluir Maio; o problema é usar `status` atual `evadido/inativo` em vez de status histórico/competência.
