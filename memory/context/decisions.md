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

*Adicione decisões conforme forem sendo tomadas.*
*Última atualização: 2026-05-29*
