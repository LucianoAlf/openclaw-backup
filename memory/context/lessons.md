# Lições Aprendidas

> 🔒 Estratégicas = permanentes (padrões que sempre valem)
> ⏳ Táticas = expiram em 30 dias (workarounds, bugs, configs temporárias)

---

## 🔒 Estratégicas

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

---

## ⏳ Táticas (revisar/deletar após 30 dias)

### [2026-04-03] memory_search funciona nativamente
Desde março 2026, busca semântica não precisa de chave externa. A OpenAI configurada no `.env` deixa os embeddings mais precisos, mas não é obrigatória.

---

*Revisão mensal: deletar táticas vencidas.*
*Última atualização: 2026-04-03*
