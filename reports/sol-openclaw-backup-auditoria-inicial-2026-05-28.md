# Auditoria inicial — Sol OpenClaw Backup

Data: 2026-05-28
Repo: https://github.com/LucianoAlf/sol-openclaw-backup
Visibilidade: privado
Branch padrão: main
Clone local: `/root/.openclaw/workspace/repos/sol-openclaw-backup`

## Escopo

Auditoria somente leitura do repositório da Sol. Nenhuma alteração foi feita no repo remoto.

## Estrutura encontrada

Projeto Node/TypeScript `sol-adm` com:

- Fastify/webhook
- Telegram polling
- WhatsApp via UAZAPI
- Supabase via `@supabase/supabase-js`
- OpenAI para LLM, áudio e imagem
- Scheduler via `node-cron`
- Workspace próprio versionado em `workspace/`
- Backups diários versionados em `backups/YYYY-MM-DD/*.tar.gz`

Arquivos centrais:

- `workspace/IDENTITY.md`
- `workspace/SOUL.md`
- `workspace/AGENTS.md`
- `workspace/MAPA.md`
- `workspace/MEMORY.md`
- `workspace/USER.md`
- `src/context-builder.ts`
- `src/tools/index.ts`
- `src/tools/supabase.ts`
- `src/tools/lareport.ts`
- `src/tools/shell.ts`
- `src/session.ts`

## Estado funcional

- `npm ci`: OK
- `npm test -- --runInBand`: OK, mas sem testes encontrados
- `npm run build`: OK

## Achados importantes

### 1. Repo contém backups compactados com `.env` real dentro

Os arquivos abaixo estão versionados:

- `backups/2026-05-26/sol-adm-20260526T225356Z.tar.gz`
- `backups/2026-05-27/sol-adm-20260527T210001Z.tar.gz`

Dentro deles existe `LA-Organizer/.env` com nomes de credenciais reais detectados:

- `SUPABASE_SERVICE_ROLE_KEY`
- `UAZAPI_TOKEN`
- `WEBHOOK_SECRET`
- `CLAUDE_CODE_OAUTH_TOKEN_EXPIRED`
- `OPENAI_API_KEY`
- `SUPABASE_ANON_KEY`
- `INTERNAL_API_SECRET`
- `GEMINI_API_KEY`
- `LA_REPORT_SERVICE_ROLE_KEY`
- `ELEVENLABS_API_KEY`

Não expus valores. O risco é alto porque os segredos estão no histórico Git dentro de tarballs.

### 2. Sol tem ferramenta master de shell

`src/tools/index.ts` habilita `execute_shell` para contexto `master`.

`src/tools/shell.ts` usa `execSync(command)` com blocklist simples. Isso reduz alguns riscos, mas não é sandbox real. Dá para contornar blocklists desse tipo com variações de shell se o agente for induzido ou se o prompt falhar.

### 3. Sol usa Supabase service key no modo master

`src/tools/index.ts` cria `supabase_query` com `SUPABASE_SERVICE_KEY`.

`src/tools/supabase.ts` tenta restringir a SELECT/WITH e bloqueia palavras como delete/drop/update/insert. Mas chama RPC `exec_sql`, dependendo do lado do banco para segurança real. Se a função SQL não for estritamente read-only, o risco existe.

### 4. Atendimento aluno usa MCP/RPC read-only mais correto

`src/tools/lareport.ts` usa `LAREPORT_ANON_KEY` + RPC `exec_readonly_sql`, o que é mais alinhado ao relato do Hugo.

### 5. Prompts atuais ainda dão liberdade excessiva no master

`workspace/AGENTS.md` diz que a Sol pode executar comandos shell, criar cron, fazer git push e salvar memória. Isso precisa ser revisado antes de ampliar uso.

`workspace/IDENTITY.md` afirma: “Tenho acesso root a VPS. Não existe restrição de filesystem ou crontab.” Essa frase é perigosa como identidade operacional.

### 6. Docker monta Docker socket dentro do container

`docker-compose.yml` monta:

- `/var/run/docker.sock:/var/run/docker.sock`

Com shell disponível, isso equivale a uma superfície de controle muito ampla do host/container. Precisa ser justificado ou removido.

## Relação com PRD segundo cérebro

O PRD v2.2 diz que a Sol deve:

- ler `shared/ + areas/atendimento/`
- escrever somente em `inbox/sol/`
- não acessar diretoria
- não executar mudança crítica sem aprovação humana
- usar 1Password como origem de segredos
- não colocar secrets no GitHub

O repo atual ainda não está alinhado com isso. Ele está mais parecido com um agente técnico/admin com shell e service keys do que com uma Sol restrita de Atendimento/Sucesso/Cobrança.

## Recomendação imediata

Antes de transferir para o segundo cérebro:

1. Parar de versionar tarballs com `.env`.
2. Remover os tarballs do histórico Git ou rotacionar todas as credenciais vazadas.
3. Confirmar se o repo privado foi acessado só por pessoas autorizadas.
4. Revisar `AGENTS.md` e `IDENTITY.md` para retirar linguagem de root/liberdade total.
5. Trocar o modo master para ferramentas mais restritas.
6. Separar:
   - Sol atendimento/aluno: read-only + escalar humano;
   - Sol admin: consulta + relatório;
   - Sol operador: ações externas só com aprovação.
7. Validar no Supabase se `exec_sql` é realmente read-only ou substituir por RPC estritamente read-only.
8. Remover Docker socket se não houver necessidade real.
9. Criar `PERMISSOES.md` da Sol conforme PRD.
10. Criar `sol-atendimento`, `sol-cobranca`, `sol-satisfacao` como skills/processos antes de ativar automações.

## Status

Auditoria inicial concluída. Próximo passo seguro: pedir confirmação do Alf antes de qualquer limpeza no repo, rotação de credenciais, alteração de prompt ou mudança em produção.
