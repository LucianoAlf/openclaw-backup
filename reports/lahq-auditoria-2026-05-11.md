# Relatório de Auditoria — LA HQ

**Data:** 2026-05-11  
**Modo:** leitura / auditoria, sem alterações em VPS, GitHub ou repositórios  
**Auditor:** Alfredo / OpenClaw  

---

## 1. Fontes avaliadas

| Fonte | Local | Status de acesso | Papel atual |
|---|---|---:|---|
| GitHub | `LucianoAlf/la-hq-agents` | Acessível | Repo público/versionado, mas incompleto |
| VPS LAHQ | `89.116.73.186:/home/lahq` | Acessível via SSH | Ambiente real do pipeline antigo |
| OpenClaw workspace | `187.127.9.25:/root/.openclaw/workspace/repos/la-hq-agents` | Local | Cópia com ajustes novos de ontem |
| Project Knowledge Claude | Arquivos no Claude | Não acessível diretamente por mim | Fonte histórica/manual a comparar com Claude |

---

## 2. Diagnóstico executivo

A fonte da verdade do LA HQ está dividida.

Hoje existem **quatro fontes parciais**:

1. **GitHub**: tem só a camada de agentes/contexto e está incompleto.
2. **VPS `/home/lahq/agents-repo`**: repo Git limpo, com commits/contextos que podem estar parcialmente à frente/fora de sincronia.
3. **VPS `/home/lahq/scripts`**: contém o **código real do pipeline**, mas está fora do Git.
4. **OpenClaw workspace**: contém os assets/design systems/refinamentos mais recentes feitos ontem, ainda não versionados.

Conclusão direta: **não dá para criar uma skill confiável do Alfredo ainda sem consolidar a fonte da verdade**.

---

## 3. GitHub `LucianoAlf/la-hq-agents`

### Estado remoto real

`refs/heads/main` no GitHub aponta para:

```text
f8553fe7e601059a568cd5dd5300ab58b30a375a
```

Na cópia local do OpenClaw, esse commit aparece como:

```text
f8553fe fix: substituir Pixa/Nano Banana por Gemini API (Imagen 3/4)
8ce2232 LA HQ - 34 skills + 8 SOULs + 4 brand guides + 4 checklists + 3 DS
```

### Conteúdo principal versionado

O GitHub contém basicamente:

- `atlas/`, `carla/`, `diego/`, `luna/`, `mike/`, `nina/`, `theo/`, `tina/`
- `SOUL.md` de agentes
- `skills/*.md`
- `shared/brand-guides/`
- `shared/checklists/`
- `shared/design-systems/`
- `output-teste/`
- `test-slide.png`

### Problema

O GitHub **não contém o código operacional real**:

- `nina.js`
- `theo.js`
- `luna.js`
- `diego.js`
- `mike.js`
- `tina.js`
- `nina-approve.js`
- pipelines soltos `pipeline-carrossel*.js`

Ou seja: GitHub versiona o “cérebro/contexto”, mas não versiona a “mão/execução”.

---

## 4. VPS LAHQ — `/home/lahq`

### Host

```text
IP: 89.116.73.186
Hostname: srv1586784
Base: /home/lahq
Usuário SSH usado: root
```

### Estrutura principal

```text
/home/lahq
├── agents/          # cópia operacional dos agentes, com diferenças e backups
├── agents-repo/     # único Git repo encontrado na VPS
├── scripts/         # código real do pipeline, fora do Git
├── docs/            # PRD/roadmap antigos
├── output/          # outputs gerados
├── node_modules/
├── package.json
├── pipeline-carrossel*.js
├── pipeline-v*.js
├── test*.js
└── patch*.py
```

---

## 5. VPS — `/home/lahq/agents-repo`

### Status Git observado

```text
## main...origin/main [ahead 2]
```

### Commits na VPS

```text
8b2a0e3 skills: montagem-carrossel v2 (DS como fonte única de tokens)
f449601 fix: substituir Pixa/Nano Banana por Gemini API (Imagen 3/4) em todas as skills
8ce2232 LA HQ - 34 skills + 8 SOULs + 4 brand guides + 4 checklists + 3 DS
```

### Observação importante

A VPS enxerga `origin/main` como `8ce2232`, mas o GitHub real hoje está em `f8553fe`.  
Isso indica que o `origin/main` local da VPS está **desatualizado/stale** ou que houve histórico equivalente com hash diferente.

### Diferença `origin/main..HEAD` na VPS

Arquivos alterados nos 2 commits locais da VPS:

```text
M diego/skills/montagem-carrossel.md
M luna/SOUL.md
M luna/skills/geracao-imagens.md
M luna/skills/gestao-media-library.md
M luna/skills/tratamento-imagens.md
M shared/integracoes-compartilhadas.md
```

Resumo estatístico:

```text
6 files changed, 85 insertions(+), 421 deletions(-)
```

### Interpretação

- Um commit da VPS parece ser equivalente/conceitualmente igual ao commit que já está no GitHub sobre troca de Pixa/Nano Banana por Gemini API.
- O commit `8b2a0e3` sobre `montagem-carrossel v2` parece ser conteúdo importante que pode **não estar no GitHub atual**.
- Antes de qualquer push/pull automático, é preciso comparar conteúdo, não só hash.

---

## 6. VPS — `/home/lahq/scripts`

Esta é a parte mais crítica.

### Arquivos principais atuais

```text
scripts/nina.js
scripts/theo.js
scripts/luna.js
scripts/diego.js
scripts/mike.js
scripts/tina.js
scripts/nina-approve.js
scripts/tina-monitor.js
```

### Checksums dos scripts principais

```text
9fc7f2bf... scripts/nina.js
ca5b3216... scripts/theo.js
b560a62c... scripts/luna.js
c8c529b2... scripts/diego.js
da79d0a3... scripts/mike.js
a1d174b6... scripts/tina.js
db25f671... scripts/nina-approve.js
25b0b92a... scripts/tina-monitor.js
```

### Backups acumulados

Há muitos backups em `scripts/`, especialmente do Diego:

```text
scripts/diego.js.backup-20260420
scripts/diego.js.backup-20260420-fontfix
scripts/diego.js.backup-20260420-prompt-rewrite
scripts/diego.js.backup-20260420-prompt-v2
scripts/diego.js.backup-20260420-prompt-v2c
scripts/diego.js.backup-20260421-selfreview
scripts/diego.js.backup-20260421-retry
scripts/diego.js.backup-20260421-madelina
scripts/diego.js.backup-20260421-compress
```

Também há backups de:

```text
nina.js
nina-approve.js
luna.js
theo.js
mike.js
tina.js
```

### Problema

O código mais importante do pipeline está fora do Git.  
Se a VPS morrer, isso pode se perder.

---

## 7. VPS — arquivos soltos na raiz

Existem múltiplos scripts/pipelines soltos em `/home/lahq`:

```text
pipeline-carrossel.js
pipeline-carrossel-v2.js
pipeline-carrossel-v3.js
pipeline-carrossel-v4.js
pipeline-v4-final.js
pipeline-v5.js
fix-claude-call.js
test-luna-gemini.js
test-luna-v3.js
test-render.js
test-slide-opus.js
test-stdin.js
patch-diego-prompt-v2.py
patch-diego-prompt-v2b.py
patch-diego-prompt-v2c.py
```

### Interpretação

A VPS contém um histórico vivo de experimentos.  
Alguns arquivos podem ser úteis como referência, mas não devem continuar soltos na raiz.

---

## 8. VPS — `agents/` vs `agents-repo/`

`agents/` e `agents-repo/` **não são iguais**.

Diferenças encontradas em:

- Carla skills
- Diego `SOUL.md` e skills
- Luna `SOUL.md` e skills
- Nina `SOUL.md` e skills
- Theo newsletter
- Design systems compartilhados
- Checklists
- Estruturas extras em `agents/`:
  - `brand-assets/`
  - `brands/`
  - `brand-guides.DEPRECATED-20260420/`
  - `shared/skills/`
  - vários `.backup-*`

### Interpretação

`agents/` parece ser uma área operacional/editada manualmente, enquanto `agents-repo/` é a tentativa de repo limpo.  
Mas hoje não dá para assumir que `agents-repo/` é mais correto sem comparar conteúdo.

---

## 9. OpenClaw workspace — repo local

Local:

```text
/root/.openclaw/workspace/repos/la-hq-agents
```

Status:

```text
## main...origin/main
 M shared/brand-guides/brand-la-music-kids.md
 M shared/design-systems/la-music-kids-design-system.html
?? ALFREDO_ANALISE_INICIAL.md
?? docs/
?? shared/design-systems/LA_MUSIC_KIDS_DS_CANONICAL.md
?? shared/design-systems/LA_MUSIC_SCHOOL_DS_CANONICAL.md
?? shared/design-systems/la-music-kids-v2/
?? shared/design-systems/la-music-school-design-system-v2-abril-2026.html
?? shared/design-systems/la-music-school-v2/
?? shared/design-systems/references/
```

### Conteúdo novo relevante aqui

- DS canônico LA Music School v2
- DS canônico LA Music Kids v2
- logos oficiais School
- logos oficiais Kids
- refs ouro School
- refs Kids / Chatiops v8 / referências corretas
- PRDs novos em `docs/prd/`
- `ALFREDO_ANALISE_INICIAL.md`

### Tamanho dos novos assets/design systems

```text
shared/design-systems total aproximado: 60 MB
la-music-kids-v2: 46 MB
la-music-school-v2: 8.7 MB
references/la-music-school-v2-gold: 780 KB
```

### Interpretação

A workspace do OpenClaw virou a fonte mais nova para DS/refs, mas ainda está **não commitada**.

---

## 10. Problemas críticos

| Problema | Impacto | Prioridade |
|---|---|---:|
| `/home/lahq/scripts` fora do Git | Perda do código real se VPS morrer | Alta |
| GitHub incompleto | Não é fonte da verdade | Alta |
| `agents/` vs `agents-repo/` divergentes | Ambiguidade do que está correto | Alta |
| OpenClaw com DS/refs não commitados | Trabalho novo pode se perder | Alta |
| Remote Git da VPS tinha token embutido | Risco de segurança | Alta |
| Muitos backups soltos | Ruído e risco de usar versão errada | Média |
| Outputs/testes versionados ou soltos | Repo poluído | Média |

---

## 11. Recomendação de arquitetura

### Fonte da verdade desejada

GitHub deve virar a fonte oficial.

### VPS LAHQ deve virar

Ambiente de execução/deploy, não lugar onde código nasce sem versionamento.

### OpenClaw/Alfredo deve virar

Orquestrador e executor via skill enxuta, lendo o repo oficial.

---

## 12. Estrutura sugerida para o repo consolidado

```text
la-hq-agents/
├── agents/
│   ├── nina/
│   ├── theo/
│   ├── luna/
│   ├── diego/
│   ├── tina/
│   ├── mike/
│   ├── carla/
│   └── atlas/
├── scripts/
│   ├── nina.js
│   ├── theo.js
│   ├── luna.js
│   ├── diego.js
│   ├── tina.js
│   ├── mike.js
│   ├── nina-approve.js
│   └── tina-monitor.js
├── pipelines/
│   ├── carousel.js
│   └── experiments/
├── shared/
│   ├── brand-guides/
│   ├── checklists/
│   └── design-systems/
├── docs/
│   └── prd/
├── references/
│   └── archived-outputs/
└── package.json
```

Observação: a estrutura atual usa agentes na raiz (`nina/`, `theo/` etc.). Dá para manter assim para não quebrar tudo agora. A reorganização acima é o estado ideal, não precisa ser feita de uma vez.

---

## 13. Plano incremental recomendado

### Fase 0 — Segurança

1. Criar backup compactado de `/home/lahq` antes de qualquer alteração.
2. Corrigir remote Git da VPS para remover token embutido.
3. Rotacionar token antigo se ele ainda estiver ativo.

### Fase 1 — Congelar estado atual

1. Copiar `/home/lahq/scripts` para uma área de staging versionável.
2. Registrar checksums dos scripts atuais.
3. Registrar lista de backups, mas não versionar todos como código ativo.

### Fase 2 — Comparar contextos

1. Comparar `agents/` vs `agents-repo/` arquivo por arquivo.
2. Comparar `agents-repo` VPS vs GitHub real.
3. Comparar OpenClaw workspace vs GitHub.
4. Comparar Project Knowledge Claude vs arquivos do repo.

### Fase 3 — Consolidar GitHub

1. Trazer commit útil da VPS: `montagem-carrossel v2`.
2. Trazer scripts reais para o repo.
3. Trazer DS/refs novos do OpenClaw.
4. Criar `.gitignore` para outputs, backups e lixo operacional.
5. Fazer commit limpo por assunto.

### Fase 4 — Skill do Alfredo

Criar skill `lahq-content-pipeline` com:

- quando usar
- onde está o repo oficial
- como escolher marca: School/Kids/SonoraMente/Grupo
- como consultar DS canônico
- como rodar pipeline
- como fazer QA
- como entregar pacote final

A skill **não deve copiar toda a documentação**. Ela deve apontar para os arquivos canônicos do repo.

---

## 14. Decisão recomendada agora

Não mexer ainda em conteúdo criativo.

Próxima ação segura:

> Fazer backup de `/home/lahq` e depois criar uma branch/staging local para trazer `/home/lahq/scripts` para dentro do repo sem apagar nada.

---

## 15. Status final

Auditoria inicial concluída.  
Nenhuma alteração feita nos repositórios ou na VPS, além de leitura via SSH.
