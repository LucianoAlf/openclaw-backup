# Decisões Permanentes

> Decisões que o Alfredo deve respeitar SEMPRE.
> Formato: O que decidiu + Por que + Data

---

### Credenciais ficam no .env, nunca em chat (01/04/2026)
Toda credencial vive no `.env` do servidor (chmod 600). Nunca hardcodar em código, markdown ou mensagem de chat. Se o Alf mandar em chat, salvar no `.env` imediatamente e alertar para revogar/trocar.

### GitHub: nunca subir .env ou dados sensíveis (01/04/2026)
`.gitignore` cobre: `.env`, `memory/`, arquivos de sessão. Push só quando Alf solicitar explicitamente.

### Domínio de serviços: maestrosdagestao.com.br, NÃO latecnology.com.br (01/04/2026)
`latecnology.com.br` tem serviços críticos (n8n, NocoDB, webhooks). Novos serviços usam `maestrosdagestao.com.br`. Antes de qualquer mudança de DNS: verificar dependências e perguntar ao Alf.

### Ações destrutivas sempre pedem confirmação (01/04/2026)
`rm`, deletar tarefas, apagar arquivos, revogar acessos — sempre confirmar antes. Preferir reversível (`trash`) quando disponível.

### Nunca executar transação financeira (01/04/2026)
Só analisar, alertar e sugerir. Nunca executar pagamento, transferência ou qualquer ação financeira.

### Publicar conteúdo público: sempre pedir aprovação antes (01/04/2026)
Redes sociais, site, qualquer coisa pública — nunca publicar sem aprovação explícita do Alf.

### Comunicação externa: equipe LA Music liberada, fora dela pede confirmação (01/04/2026)
Vitória, Cleiton, Kailane, Andreza, Krissya — contato direto liberado. Qualquer outra pessoa: confirmar antes.

### Anne usa WhatsApp, não Telegram (03/04/2026)
Lembretes, alertas e comunicação com a Anne só via WhatsApp. Jamais assumir que ela vai ver mensagem no Telegram.

### Contas pessoais: cobrar todo dia até confirmação de pagamento (03/04/2026)
Monitorar lista "💸 Contas Pessoais" no TickTick. Cobrar diariamente sobre contas atrasadas até o Alf confirmar que pagou — então marcar como concluída no TickTick.

### Compactação de memória: extrair antes de compactar (03/04/2026)
INVIOLÁVEL. Antes de qualquer compactação: extrair → lessons → decisions → people → projects → pending. Nunca compactar sem esse checklist.

### Sugerir tópico ou agente especializado quando fizer sentido (03/04/2026)
Quando perceber tarefa recorrente/isolada que não precisa do contexto completo, sugerir criar agente especializado ou novo tópico no grupo. Critério: mesma categoria de tarefa 3x+, ou contexto muito específico. Alf decide — Alfredo só orienta.

### Push pro GitHub: só quando Alf pedir (02/04/2026)
Não fazer push automático. Commitar local está liberado. Push só sob solicitação explícita.

### LAHQ: memória operacional no OpenClaw; memória de agentes no `semantic_memory` (13/05/2026)
Para o Alfredo, a memória principal continua sendo OpenClaw (`MEMORY.md`, `memory/*`, `memory_search`). No Supabase LAHQ, usar `semantic_memory` apenas para aprendizados dos agentes/pipeline LAHQ (Nina/Theo/Luna/Diego/Tina, refs, decisões de conteúdo, padrões de campanha). Não usar `shared_memory`; tabela fica deprecated para evitar duplicidade e confusão.

### LAHQ Supabase é fonte da verdade para conteúdo/assets/publicação (13/05/2026)
Para produção LAHQ — imagens estáticas, carrosséis, vídeos/Reels/Stories, outputs, assets, aprovações, publicação Instagram e métricas — usar o Supabase LAHQ como fonte de verdade. O Supabase “Agente Alfredo” fica deprecated para esse domínio.

### Mike/LAHQ: visual pesado fora do chat principal (21/05/2026)
Mike deve operar com fluxo visual separado do Telegram/chat principal. Chamadas diretas de `image_generate`, render ou Chrome no chat travaram sessão em `blocked_tool_call`, enfileiraram mensagens e deram aparência de “mudez”. O chat principal fica para direção, copy, HTML/preflight e status; imagem/render pesado vai para worker/subtarefa assíncrona.

### LAHQ School premium: HTML/CSS + assets oficiais + QA, não imagem final por IA (21/05/2026)
Carrossel School de qualidade Alfredo não deve ser peça final gerada por IA com texto/logo/layout embutido. O método canônico é: direção criativa, copy, assets oficiais ou imagem sem texto, composição em HTML/CSS controlado, render headless, preview grid e QA contra refs ouro. IA pode apoiar asset/foto, mas não substituir montagem final.

### LAHQ: refs ouro são régua, não banco de imagem (21/05/2026)
Refs ouro servem para comparar força visual, ritmo, composição, acabamento e padrão de qualidade. Não recortar/reutilizar fotos/assets das refs como matéria-prima aleatória. Se não houver asset certo, declarar o problema e propor busca, produção ou geração dirigida.

---


### Mike assume execução LAHQ/marketing; Alfredo orquestra e audita (23/05/2026)
Após teste real com `.learnings`, Dreaming, research gate, preflight, render/QA e nota 10 do Alf no carrossel de Palhetada Alternada, o bastão operacional de LAHQ/marketing fica com Mike. Alfredo não disputa execução especializada: atua como CIO/parceiro estratégico, orquestra, audita, consolida aprendizado e entra na execução LAHQ só quando o Alf chamar ou quando houver falha de arquitetura/processo.

### Sol é Farmer AI operacional, não chatbot/robô de cobrança (29/05/2026)
Sol deve ser tratada como Farmer AI da LA Music: presença operacional para Atendimento/Relacionamento, Sucesso do Aluno e BI/Gestão/Reports. Frase-raiz aprovada: “A Sol cuida do operacional para proteger o tempo humano da LA Music.” Guardrails: human takeover, anti-spam, faseamento de automação, read-only por padrão e aprovação humana para ações sensíveis.

### Fronteiras da Sol com outros agentes/papéis (29/05/2026)
Sol cuida de relacionamento, gestão, operação, presença, satisfação, cobrança operacional, renovação e experiência. Fábio fica com pedagógico profundo; Maria com financeiro macro; Mike com marketing. Quando a demanda tocar conteúdo pedagógico profundo, Sol escala para Fábio/coordenação com contexto, não resolve sozinha.

### Sol Atendimento e Sol Sucesso do Aluno são canais separados (29/05/2026)
Arquitetura aprovada: Sol Instância Atendimento `(21) 3955-4415`; Sol Instância Sucesso do Aluno `(21) 2342-5316`. Atendimento é canal do dia a dia com farmers por unidade. Sucesso do Aluno é canal dedicado e mais proativo, visível para Fabíola/Jéssica, para feedback/reclamações sensíveis sem misturar com atendimento operacional comum.

### Sol/Chatwoot: bridge externo é porteiro determinístico de segurança (30/05/2026)
Em canais externos como WhatsApp/Chatwoot, o bridge da Sol não pode ser cérebro do atendimento nem simples repassador do que a LLM decidiu. Ele deve funcionar como porteiro/validador: só envia resposta externa quando risco, permissão, handoff e conteúdo passam nas travas; casos sensíveis viram nota interna. Dados internos/agregados da LA — alunos, matrículas, pagantes, ativos, KPIs, faturamento, inadimplência, listas, rankings, scores e similares — são bloqueados por regra determinística e forçam handoff humano, mesmo que a Sol classifique como baixo risco.

### LA Report/Sol: definição canônica de evasão (31/05/2026)
No contexto de KPIs da LA Music, **Evasão** é o guarda-chuva de saída realizada do aluno: **cliente que interrompeu/cancelou no meio do contrato + cliente que não renovou ao fim do contrato**. Definições: `interrompido/evasão interrompida` = cancelou no meio do contrato; `não renovação` = não quis renovar e seguir com as aulas; `evasão/total de evasões/churn` = interrompido + não renovação. `Aviso prévio` não é evasão realizada: é sinalização/risco e deve aparecer separado até virar saída efetiva.


### LA Report/Sol: financeiro por competência não é igual a pagante contratual (03/06/2026)
Para KPIs financeiros — MRR, ticket médio, faturamento estimado/real, inadimplência por competência — separar três camadas: ativo operacional, pagante contratual e pagante financeiro da competência. `conta_como_pagante=true`, `valor_parcela>0` e existência de fatura isolada não bastam como regra universal. Antes de migration/backfill financeiro: reconciliar nominalmente faturas Emusys/LA Report, passaporte, início real, cobranças movidas/removidas, bolsistas/permutas/professores/estagiários e casos legítimos de cobrança futura. Sem lista nominal fechada, fica SELECT-only.

*Adicione decisões conforme forem sendo tomadas.*
*Última atualização: 2026-06-03*

### LA Report: mês fechado é snapshot histórico, não recálculo vivo (02/06/2026)
Para KPIs mensais da LA Music, `dados_mensais` representa fechamento histórico. Mês fechado não deve ser recalculado a partir de tabela viva (`alunos.status`, cadastros atuais, funções antigas ou cron legado) sem processo formal. Retificação histórica só pode ocorrer com motivo, fonte confiável, diff, audit log, solicitante/aprovador, rollback, transação, trava de exatamente 1 linha/escopo e aprovação explícita do Alf.

### LA Report/Sol: métricas por pessoa vs matrícula são domínios diferentes (02/06/2026)
`alunos_ativos` e `alunos_pagantes` são métricas por pessoa/aluno deduplicado. `matriculas_ativas`, `matriculas_banda` e `matriculas_2_curso` são métricas por linha/matrícula. Banda/projeto (`cursos.is_projeto_banda=true` / tipo `5 BANDA`) não é segundo curso financeiro. Aluno com curso pagante + banda conta como 1 pagante pelo curso pago; banda não conta ticket/pagante.

### LA Report/Sol: Alf valida regra de negócio; sistemas são evidências (02/06/2026)
Supabase, LA Report, Emusys, CSVs, prints, frontend e Cascade/Windsurf são evidências a cruzar. Em divergência de regra de negócio, Alf é a fonte final. Antes de migration/backfill/RPC em produção: auditoria SELECT-only, diff nominal, bloqueio de nomes hardcoded e aprovação explícita.

### LA Report/Sol: evasão depende da data real e da natureza da saída, não da data de lançamento (04/06/2026)
Movimentação lançada/importada em um mês não significa evasão real daquele mês. Para KPIs de evasão/não renovação, separar: data de lançamento/importação no sistema, data real da saída, tipo de saída e competência do KPI. Baixa antiga, duplicidade, automação Emusys indevida, saída de outro mês e finalização de segundo curso não podem contar como evasão real da escola no mês corrente. Para mês em andamento, modo tempo real usa corte operacional `CURRENT_DATE`; `fim_mes` é projeção/fechamento, não estado vivo.

### LA Report/Sol: regras canônicas de KPI validadas pelo Alf (06/06/2026)
Para o LA Music Performance Report/Sol, respeitar estas regras até nova decisão explícita do Alf: churn = `evasoes / alunos_pagantes * 100`; inadimplência = percentual de pessoas/cabeças (`qtd_inadimplentes / alunos_pagantes * 100`), não percentual de valor; ticket médio = `MRR / COUNT(DISTINCT pagantes)` por pessoa; Canto Coral deve usar flag `cursos.is_coral`, não filtro por nome; bolsista parcial não conta como pagante e não entra no ticket médio; Passaporte não entra no MRR e é receita à parte; conversão por professor só considera experimentais realizadas por aquele professor, matrícula sem experimental não entra; LTV pode ficar como `ticket_medio * tempo_permanencia_meses` no frontend por enquanto; Kids/School usa `idade_atual <= 11` para LAMK e `idade_atual >= 12` para EMLA. Documento antigo divergente é legado; código divergente é possível bug; regra validada pelo Alf é canônica.

### LA Report/Sol: `dados_mensais` não pode ser sobrescrito sem congelamento e trilha de auditoria (06/06/2026)
P8/P11 confirmou que `dados_mensais` é tabela de snapshot e que UPSERT/recalcular pode sobrescrever histórico. Antes de qualquer migration/backfill/recalcular em produção: fazer SELECT-only, confirmar funções/cron/frontend, impedir recálculo de mês fechado, adicionar congelamento/audit trail/versionamento/rollback auditado e obter aprovação explícita do Alf. Script automático de replace/migration não deve ser executado só porque foi gerado pelo Cascade/Windsurf.
