# Auditoria runtime Sol via SSH — 2026-05-28

Host: `lahq` / `89.116.73.186`
Usuário auditado: `sol`
Workspace: `/home/sol/.openclaw/workspace`

## Arquivos lidos

- `/home/sol/.openclaw/workspace/SOUL.md`
- `/home/sol/.openclaw/workspace/AGENTS.md`
- `/home/sol/.openclaw/workspace/MEMORY.md`
- `/home/sol/.openclaw/workspace/HEARTBEAT.md`
- `/home/sol/.openclaw/workspace/MASTERS.md`
- `/home/sol/.openclaw/openclaw.json` com segredos redigidos
- scripts principais em `/home/sol/.openclaw/workspace/scripts/`

## Achado central

A Sol atual é uma mistura de:

1. assistente de atendimento/sucesso;
2. agente BI/LA Report;
3. operador técnico/admin com shell completo.

Ela ainda não tem uma visão de negócio robusta da LA Music. O `SOUL.md` é mais uma regra de tom/resposta curta do que uma personalidade estratégica.

## SOUL.md atual

Pontos bons:

- tom empático e natural;
- mensagens curtas para alunos;
- personalização por primeiro nome, curso e unidade;
- orientação para não narrar processo para admin.

Limitações:

- centrado no Hugo/admin, não no Alf/LA Music;
- não descreve missão da Sol dentro da jornada do aluno;
- não define papel como Farmer AI, retenção, sucesso, cobrança cuidadosa e relacionamento;
- não traz valores LA: paixão, empatia, coragem, excelência;
- não diferencia atendimento de aluno, professor, recepção, gerente, Hugo e Alf;
- não tem regra forte de escalonamento por risco de evasão, inadimplência, reclamação ou dados sensíveis.

## AGENTS.md atual

Permite fazer direto:

- responder dúvidas informativas;
- consultar Supabase preferencialmente via MCP/read-only;
- salvar decisão/configuração em memória;
- executar shell, criar arquivos e configurar cron.

Pede antes:

- alterar registro de aluno;
- operações financeiras;
- enviar mensagem em nome de outra pessoa.

Red lines corretas:

- não cancelar matrícula autonomamente;
- não negociar desconto sem aprovação;
- não compartilhar CPF/dados bancários/sensíveis;
- não inventar informações contratuais;
- não executar comando destrutivo sem confirmação.

Problemas:

- shell/criação de cron é amplo demais para a Sol operacional;
- fallback com service key está permitido em texto;
- seção de Skills e Memória está quebrada/incompleta (`leia .`, caminhos vazios);
- faltam permissões por papel/canal;
- falta regra explícita: alunos e equipe nunca recebem dados de outros alunos;
- falta `PERMISSOES.md` no modelo do PRD segundo cérebro.

## MEMORY.md atual

Confirma:

- OpenClaw na porta `19790`;
- Telegram ativo com `@Sol_adm_bot`;
- Supabase LA Performance Report ativo;
- worker BI ativo em `/home/sol/.openclaw/workspace/scripts/lareport-sol-worker.js`;
- MCP read-only `lareport-readonly` via `lareport-readonly-mcp.sh`;
- role `lume_readonly.ouqwbbermlzqqvtqwlul` com segredo local;
- métricas canônicas em `memory/la-music-metricas.md`;
- masters: Hugo e Luciano.

## openclaw.json — pontos relevantes

- agentId: `main`, nome `Sol`;
- modelo: `openai-codex/gpt-5.5`;
- tools perfil `coding`;
- `exec` em `host: gateway`, `security: full`, `ask: on-miss`;
- alsoAllow: browser, edit, exec, message, process, read, write, web_search, web_fetch, memory, cron;
- Telegram com DM allowlist só para Hugo (`8623872779`) mas grupo `-1003443031930` aberto sem exigir menção;
- MCP `sol-acesso-restrito` aponta para `lareport-readonly-mcp.sh`.

## MCP read-only

Script `lareport-readonly-mcp.sh`:

- carrega segredo de `/home/sol/.openclaw/secrets/lareport-readonly.env`;
- monta conexão Postgres pooler;
- executa `@modelcontextprotocol/server-postgres`.

Permissão do segredo: `rw-------`, proprietário `sol` — bom.

## Worker BI

Script `lareport-sol-worker.js`:

- roda como processo ativo do usuário `sol`;
- usa service role do LA Report via env de `/opt/LA-Organizer/.env`;
- escuta fila/conversas BI;
- chama Sol local via OpenClaw;
- escreve respostas/status em tabelas BI;
- possui autoaprendizado que atualiza/cria playbooks em `bi_ai_query_playbooks`.

Risco: apesar do MCP read-only, o worker tem service role e capacidade de escrita em playbooks/conversas. Isso precisa ficar separado conceitualmente da Sol Atendimento.

## HEARTBEAT.md

Rotinas descritas:

- faltas consecutivas;
- inadimplência diária;
- alunos sumidos;
- renovações próximas;
- aniversariantes;
- monitoramento de backup.

As rotinas estão conceitualmente boas, mas ainda parecem dry-run/relatório. Precisa confirmar se algum cron OpenClaw está realmente executando isso.

## Cron real do usuário sol

`crontab -l` mostrou principalmente rotinas do `/opt/LA-Organizer`, não mostrou diretamente o backup Sol 21:00 UTC. Pode estar em outro usuário/sistema ou divergente da documentação.

## Backups

`backup-status.json` confirma último push GitHub OK em 2026-05-27.

Script `run-backup-with-status.sh` ainda inclui explicitamente:

- `/opt/LA-Organizer/.env`
- `/opt/LA-Organizer/.env.example`

Isso confirma que o backup empacota `.env` real dentro do tarball antes de enviar ao GitHub privado.

## Permissões de filesystem

- `/home/sol/.openclaw`: `700`, bom.
- `/home/sol/.openclaw/secrets`: `755`, poderia ser mais restrito.
- segredo `lareport-readonly.env`: `600`, bom.
- `/home/sol/.openclaw/workspace`: `755`.
- `/home/sol/backups/sol-adm`: `755`.

## Conclusão

O Hugo construiu uma Sol tecnicamente capaz, com BI real e OpenClaw funcional, mas o desenho atual mistura escopos. Antes de reescrever o `SOUL.md`, vale separar a Sol em três camadas:

1. Sol Atendimento — fala com aluno/responsável, curta, segura, empática;
2. Sol Farmer/CS — alertas, retenção, renovação, NPS, risco de evasão;
3. Sol BI/Admin — consultas e relatórios para Hugo/Alf/equipe, com acesso técnico controlado.

A reescrita do `SOUL.md` deve trazer visão de negócio real, mas o maior ajuste operacional está em `AGENTS.md` e em um novo `PERMISSOES.md`.

## Próximas ações recomendadas

1. Reescrever `SOUL.md` com identidade de Farm AI LA Music.
2. Reescrever `AGENTS.md` corrigindo seções quebradas e reduzindo autonomia operacional.
3. Criar `PERMISSOES.md` com matriz por perfil: aluno, responsável, professor, recepção, gerente, Hugo, Alf.
4. Separar docs: `BI.md`, `ATENDIMENTO.md`, `COBRANCA.md`, `RENOVACAO.md`, `ESCALONAMENTO.md`.
5. Revisar `openclaw.json`: avaliar se Sol precisa mesmo de `exec security full` e `cron` no agente principal.
6. Confirmar onde está o cron de backup 21:00 UTC.
7. Ajustar backup para não incluir `.env` real quando for saneamento oficial.
