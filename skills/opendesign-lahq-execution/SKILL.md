---
name: opendesign-lahq-execution
description: Execute testes e protótipos 100% Open Design para LAHQ usando daemon/web local, Codex/gpt-5.5, Design Systems user:la-music-* e skills .od/skills. Use quando o usuário pedir workflow real Open Design, validar se foi gerado pelo agente, criar peças LA Music School/Kids/SonoraMente no Open Design, ou comparar Open Design com fluxo LAHQ/Mike.
---

# Open Design LAHQ Execution

Objetivo: rodar Open Design como ferramenta real de agente, não como simples renderizador/container.

## Critério “100% Open Design”

Só declarar como 100% Open Design quando todos forem verdade:

1. Projeto criado no Open Design (`POST /api/projects` ou UI).
2. Projeto tem `skillId` e `designSystemId` corretos.
3. Run criado via Open Design daemon (`POST /api/runs`) ou submit da UI.
4. Agente local executa (`codex` + modelo esperado, normalmente `gpt-5.5`).
5. Arquivo final é criado dentro de `.od/projects/<projectId>/` pelo agente.
6. Render é validado via `/api/projects/<id>/raw/index.html` ou arquivo HTML equivalente.
7. Prova final inclui projectId, runId, status, arquivos gerados, screenshot e QA.

Se a peça foi escrita manualmente fora do run e só hospedada no Open Design, diga claramente: **não é 100% Open Design**.

## Ambiente padrão Alfredo

- Repo: `/root/.openclaw/workspace/repos/open-design`
- Daemon: `http://127.0.0.1:17456`
- Web: `http://127.0.0.1:17573`
- Node 24: `/root/.openclaw/tools/node-v24/bin`
- Projetos: `.od/projects/`
- Design Systems ativos:
  - `user:la-music-school`
  - `user:la-music-kids`
  - `user:la-music-sonoramente`
- Skill ativa inicial: `la-music-carousel`

## Checklist antes de rodar

1. Confirmar daemon/web ativos.
2. Confirmar DS LAHQ com `status: published` em `.od/design-systems/<id>/metadata.json`.
3. Usar `skillId` explícito, não confiar em seletor/estado anterior da UI.
4. Usar projeto novo por teste; não reutilizar projeto antigo.
5. Capturar `projectId` e `runId` da resposta real, não do URL antigo.

## Comando recomendado

Use o script deste skill para runs repetíveis:

```bash
node /root/.openclaw/workspace/skills/opendesign-lahq-execution/scripts/run-lahq-open-design.mjs \
  --brand kids \
  --prompt "Crie uma arte/post 1080x1350..."
```

Brands suportadas inicialmente: `school`, `kids`, `sonoramente`.

## QA mínimo

Depois do run:

- `status` deve ser `succeeded`.
- Deve existir HTML renderizável, preferencialmente `index.html`.
- Render esperado: `1080x1350`.
- Fonts devem estar `loaded` ou justificadas.
- Logos oficiais devem carregar com `ok: true`.
- Procurar proibidos: `placeholder`, `lorem`, cores erradas, termos vetados pelo DS.
- Usar análise visual para classificar: `produção`, `V1 bom`, `V1 fraco`, `rejeitado`.

## Veredito honesto

Open Design pode ser bom como atelier, mas não mascarar qualidade:

- Se tecnicamente funciona mas visualmente está fraco: “funcionou como engine; resultado é V1”.
- Se DS/skill não foi respeitado: “falhou em aderência de marca”.
- Se só precisou ajuste fino: recomendar lapidação por Mike/LAHQ.
