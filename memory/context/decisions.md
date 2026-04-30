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

---

*Adicione decisões conforme forem sendo tomadas.*
*Última atualização: 2026-04-03*
