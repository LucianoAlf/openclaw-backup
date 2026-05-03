# NotebookLM — Estado da Integração

## Status atual
- **Auth:** ✅ funcional
- **List notebooks:** ✅ funcional
- **GET_NOTEBOOK / use / source list / ask:** ❌ falhando

## Diagnóstico atual
A ponte com o NotebookLM ficou **parcialmente funcional**.

### O que funcionou
- instalação do `notebooklm-py`
- instalação do Playwright/Chromium
- carregamento de sessão via `storage_state.json`
- autenticação válida
- listagem dos notebooks

### O que falhou
- abrir notebook específico (`use` / `GET_NOTEBOOK`)
- listar fontes de notebook
- fazer perguntas/query no notebook
- export de metadata dependente de `GET_NOTEBOOK`

## Causa mais provável
Bug/upstream drift na lib `teng-lin/notebooklm-py` na camada de `GET_NOTEBOOK` (RPC `rLM1Ne`).

---

## Evidências / issues relacionadas

### Issue #114
- **Título:** `RPC GET_NOTEBOOK failed`
- Padrão semelhante ao observado:
  - list funciona
  - auth funciona
  - `GET_NOTEBOOK` falha

### Issue #294
- **Título:** `RPC GET_NOTEBOOK returns null result (rLM1Ne)`
- Padrão muito próximo do nosso caso:
  - `list` funciona
  - `auth check --test` funciona
  - `use`, `source list`, `metadata` e operações dependentes de notebook falham

---

## Estado operacional deixado pronto

### Sessão
- `storage_state.json` está pronto e funcional para auth/list

### Symlink
- o symlink em `/root/.notebooklm/storage_state.json` foi criado e **deve permanecer como está**

### Regra
**Não mexer no `storage_state.json` nem no symlink por agora.**
A base de autenticação já está plantada para retomada futura.

---

## Como retomar quando houver fix upstream

Quando a lib for corrigida:

1. atualizar `notebooklm-py`
2. manter o mesmo `storage_state.json`
3. manter o mesmo symlink já criado
4. retestar nesta ordem:
   - `auth check --test`
   - `list`
   - `use <notebook_id>`
   - `source list`
   - `ask "do que esse notebook trata?"`
   - `metadata --json`

### Observação
A parte mais difícil (sessão/autenticação) já foi vencida.
Se houver fix upstream, a retomada deve ser rápida.

---

## Casos de uso pretendidos

### 1. Mentorias
- consolidar material de leitura
- resumir fontes
- organizar conhecimento por mentorado/tema

### 2. Resumos
- resumir notebooks inteiros
- gerar sínteses rápidas de materiais estudados
- preparar briefings

### 3. Estudos e pesquisa
- usar notebooks como base de estudo
- consultar temas específicos
- conectar aprendizado a projetos e decisões

---

## Conclusão
A integração com o NotebookLM está em estado de **ponte parcial validada**:
- autenticação e listagem funcionando
- acesso profundo ao notebook bloqueado por bug conhecido da lib / drift da API interna

Prioridade atual: **pausada**, aguardando correção upstream ou alternativa confiável.
