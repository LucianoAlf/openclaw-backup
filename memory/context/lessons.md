# Lições Aprendidas

> 🔒 Estratégicas = permanentes (padrões que sempre valem)
> ⏳ Táticas = expiram em 30 dias (workarounds, bugs, configs temporárias)

---

## 🔒 Estratégicas

### LAHQ School — design system não é checklist
2026-05-13: Alf corrigiu que a queda de qualidade veio também de não consultar de verdade o Design System visual/interativo da School para puxar componentes e elementos. Não basta usar cores, Prompt, logo e halftone. Antes de criar peças School, abrir as refs ouro + DS completo e extrair componentes concretos: grids, selos, barras, shapes, labels, diagonais, máscaras, ritmos, variações de card e regras de composição. Se a peça parece template genérico, é porque o DS não foi usado como biblioteca visual.


### Antes de qualquer mudança de DNS/nameservers
Checar todos os subdomínios e registros ativos. Perguntar ao Alf quais serviços dependem do domínio. Ter plano de rollback. **Origem:** incidente Cloudflare 01/04/2026 — derrubou n8n, NocoDB, webhooks críticos por horas.

### Credenciais nunca em chat
Se o usuário mandar token/senha no chat: salvar imediatamente no `.env`, alertar para revogar/trocar o token exposto, nunca deixar no histórico de mensagem.

### Alf é o piloto — a LA não voa sem ele
Aprendido da forma difícil em 2017. Não sugerir delegação total de gestão da LA para terceiros. Ele precisa estar no centro.

### A separação é feature, não bug
Cada sistema tem um domínio único. Não sugerir fusão de sistemas distintos. A fragmentação é intencional e estratégica.

### Nunca presumir o que Alf quer com ideia solta
Quando ele joga uma ideia no ar — perguntar: "Quer capturar pra depois ou já puxo o fio agora?" Nunca presumir que quer execução imediata.

### LAHQ School: skill não é enfeite, é processo obrigatório
Erro de 13/05/2026: Alfredo leu as skills, mas bypassou o workflow criativo e gerou carrossel técnico/E2E com qualidade baixa. Para LAHQ School, antes de registrar/publicar qualquer output: consultar runbook + DS canônico + refs ouro, montar direção Nina, copy Theo, composição Diego, e reprovar internamente se o QA não bater pelo menos 8,5. Teste E2E técnico não pode ser apresentado como peça criativa final.

### Mike/LAHQ: habilidade carregada não garante execução correta
2026-05-20/21: Mike tinha skills instaladas/ready, mas nem sempre elas entravam no prompt ou viravam método real. Em agente especializado, validar três camadas: skill existe, skill é carregada no contexto e o agente segue a ordem operacional. Para conteúdo School: carregar skill/runbook/DS/brand guide/refs, fazer preflight, montar HTML/CSS, renderizar e olhar preview grid antes de chamar de final.

### LAHQ School técnico: imagem precisa provar o assunto
2026-05-20: Em conteúdo técnico de guitarra/palhetada, Mike usou imagem com leitura de cantora/performance genérica. Isso destrói credibilidade. Foto bonita mas errada reprova. Palhetada precisa mostrar mão, palheta, cordas, braço do instrumento, gesto técnico, professor corrigindo ou recurso visual equivalente. Se não houver asset certo, dizer que não há asset certo e pedir/buscar/gerar dirigido.

### LAHQ carrossel: copy precisa ter arco, não cards soltos
2026-05-21: Alf rejeitou carrossel voz/palco por parecer template, com textos ruins e frases soltas. Antes de renderizar, a copy precisa formar campanha com tese → tensão → progressão → resolução → CTA. Se as lâminas parecem dicas independentes sem ligação narrativa, reprovar no preflight.

### LAHQ visual pesado bloqueia conversa se rodar no chat principal
2026-05-21: `image_generate`/render pesado deixou Mike em `blocked_tool_call` e travou o Telegram. Para agentes conversacionais, render/imagem/Chrome devem ir para worker assíncrono, subtarefa ou fila com status, nunca várias gerações pesadas diretas no chat principal.

---

## ⏳ Táticas (revisar/deletar após 30 dias)

### [2026-04-03] memory_search funciona nativamente
Desde março 2026, busca semântica não precisa de chave externa. A OpenAI configurada no `.env` deixa os embeddings mais precisos, mas não é obrigatória.

---

*Revisão mensal: deletar táticas vencidas.*
*Última atualização: 2026-05-21*
