# agent-browser — smoke test 2026-05-22

Repo: https://github.com/vercel-labs/agent-browser
Package: `agent-browser@0.27.0`
License: Apache-2.0

## Instalação

- Instalado globalmente via npm: `agent-browser 0.27.0`
- Também instalado em sandbox local: `/root/.openclaw/workspace/research/agent-browser-test/smoke`
- Chrome for Testing baixado por `agent-browser install`:
  - `/root/.agent-browser/browsers/chrome-149.0.7827.22`
  - tamanho aprox.: 379 MB

## Testes executados

### 1. Navegação básica

Comandos:

```bash
agent-browser open https://example.com
agent-browser get title
agent-browser get url
agent-browser snapshot
agent-browser eval 'document.querySelector("h1")?.textContent'
agent-browser screenshot example.png
agent-browser close
```

Resultado: PASS.

### 2. Formulário local + batch

Página local com input e botão; comando batch abriu, preencheu, clicou e leu resultado.

Resultado esperado/lido: `OK alf@test.com`.

Resultado: PASS.

## Observações

- É bem leve no uso como CLI: binário Rust + CDP, sem Playwright/Puppeteer no runtime.
- Ainda baixa um Chrome completo, então não é “zero peso” em disco.
- Snapshot com refs `@e1`, `@e2` é parecido com o fluxo ideal para agente.
- `batch` é útil para reduzir overhead de vários comandos.
- Tem skills próprias embutidas: `core`, `electron`, `slack`, `dogfood`, `agentcore`, `vercel-sandbox`.

## Veredito inicial

Promissor. Serve bem como CLI rápida para automações isoladas, testes e scripts. Para OpenClaw, não substitui automaticamente o browser tool atual, mas vale ter como ferramenta auxiliar para fluxos CLI/agent-worker.
