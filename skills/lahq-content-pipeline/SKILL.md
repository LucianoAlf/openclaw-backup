---
name: lahq-content-pipeline
description: Produzir carrosséis, posts e peças visuais LAHQ para LA Music School, LA Music Kids e SonoraMente usando repo canônico, brand guides, design systems, refs ouro, logos oficiais e o workflow novo baseado em skills. Use quando o usuário pedir carrossel, post, feed, story, peça visual ou conteúdo de marca LA Music/School/Kids/SonoraMente.
---

# LAHQ Content Pipeline

Use esta skill para criar conteúdo visual das marcas LA Music sem carregar o LAHQ inteiro no prompt.

Princípio central: **o repo é a fonte da verdade; esta skill é direção criativa + guardrails.**

## Fonte da verdade

Repo local:

```bash
/root/.openclaw/workspace/repos/la-hq-agents
```

Para copy/caption, hashtags, empacotamento e publicação Instagram, carregar também:

- `/root/.openclaw/workspace/skills/lahq-copy-publication/SKILL.md`

Use essa skill quando o usuário pedir publicar, agendar, subir no Instagram, feed, stories, reels, vídeos, legendas, CTA ou hashtags.

Antes de produzir:

```bash
git status --short --branch
git pull --ff-only origin main
```

Se houver mudança local não sua, pare e avise antes de sobrescrever.

## Arquivos por marca

Leia só o que a marca pedida exigir.

### LA Music School

Para School, carregar também a skill específica antes de produzir:

- Skill específica: `/root/.openclaw/workspace/skills/lahq-school-content/SKILL.md`

Arquivos canônicos da marca:

- Runbook: `docs/runbooks/LAHQ_SCHOOL_CARROSSEL.md`
- Brand guide: `shared/brand-guides/brand-la-music-school.md`
- DS: `shared/design-systems/la-music-school-design-system-v2-abril-2026.html`
- Índice DS: `shared/design-systems/LA_MUSIC_SCHOOL_DS_CANONICAL.md`
- Logos: `shared/brand-assets/logos/school/`
- Fontes: `shared/brand-assets/fonts/school/`
- Refs: `shared/design-systems/references/la-music-school-v2-gold/`

### LA Music Kids

- Brand guide: `shared/brand-guides/brand-la-music-kids.md`
- DS: `shared/design-systems/la-music-kids-design-system.html`
- Índice DS: `shared/design-systems/LA_MUSIC_KIDS_DS_CANONICAL.md`
- Logos: `shared/brand-assets/logos/kids/`
- Fontes: `shared/brand-assets/fonts/kids/`
- Refs: `shared/design-systems/references/la-music-kids-v2-gold/`

### SonoraMente

- Brand guide: `shared/brand-guides/brand-sonoramente.md`
- DS: `shared/design-systems/sonoramente-design-system.html`
- Logos: `shared/brand-assets/logos/sonoramente/`

## Guardrails obrigatórios

- Usar logo oficial. Nunca reconstruir logo com texto, fonte ou formas.
- Para School, `LA` de fundo/composição é sempre SVG oficial solo; nunca `LA` digitado.
- Usar cores, fontes e tom da marca consultada.
- Não misturar elementos visuais entre School, Kids e SonoraMente.
- Comparar com refs ouro antes de aprovar.
- Reprovar visual genérico, stock demais, ilegível ou fora da marca.

## Liberdade criativa

A skill não é receita fixa. Use direção de arte.

### Logo como composição

A logo completa oficial é assinatura de marca. O símbolo solo é recurso gráfico.

- manter a logomarca completa oficial presente e legível, especialmente em School;
- não usar o símbolo `LA` grande como substituto da logomarca completa;
- variar tamanho, posição, opacidade, corte e rotação leve do símbolo solo;
- usar versão colorida, vazada ou monocromática conforme contraste;
- deixar o símbolo solo grande, vazando a tela, atrás de halftone/glow/gradiente/sombra;
- fazer parecer parte da composição, não carimbo repetido;
- antes de renderizar, definir posição/escala do símbolo card a card; se vários cards ficarem com LA no mesmo lado/tamanho, reprovar e variar.

### Imagens

Imagens são recurso de impacto, não regra de quantidade — e não são lugar para economizar quando o tema pede.

A capa precisa vender o carrossel: se o tema pedir, comece com uma foto forte, grande, desejável, com cara de campanha.

Escolha livremente conforme conceito:

- foto hero grande;
- close de mão, instrumento, microfone, corpo ou gesto;
- músico em palco/aula/estúdio;
- recorte dramático;
- collage quando fizer sentido;
- card tipográfico sem foto.

Não fixar “2 fotos”, “4 fotos” ou alternância com/sem foto. Use quantas imagens a direção pedir. O erro é repetir fórmula visual sem intenção.

Para carrossel técnico/instrumental, evitar reaproveitar a mesma imagem em vários cards. Cada lâmina deve ter função visual própria quando possível: hero, macro da técnica, detalhe do instrumento, professor/aluno, palco, prática/metrônomo, CTA. A imagem deve vender sensação, energia e desejo.

### Carrossel contínuo

Quando fizer sentido, criar sensação de arte única recortada em cards:

- planejar composição horizontal antes de exportar;
- deixar foto, forma, textura ou símbolo atravessar de um card para outro;
- cada card ainda precisa funcionar sozinho;
- usar como recurso premium, não padrão obrigatório.

## Workflow novo baseado em skills

As skills substituem o pipeline legado de agentes. Não depender de nomes/personas antigas nem tentar ressuscitar o fluxo multiagente.

1. **Direção** — conceito, objetivo, estrutura, ritmo e direção visual.
2. **Copy com arco** — antes do layout, escrever a progressão do carrossel: tese → tensão → desenvolvimento → resolução → CTA. Se parecer lista de dicas soltas, reprovar.
3. **Imagem/asset certo** — gerar/selecionar imagens sem texto, sem logo e sem watermark. A imagem precisa provar o assunto, não só “ficar bonita”. Se não houver asset certo, declarar e propor busca/produção/geração dirigida.
4. **Montagem controlada** — compor em `1080x1440`, preferencialmente HTML/CSS + assets oficiais + render headless para carrosséis premium. Não usar IA para gerar card final com texto/logo/layout embutido.
5. **QA** — checar marca, legibilidade, coerência visual e entrega. Olhar o preview grid antes de enviar; se aparecer padrão mecânico repetido (ex.: LA sempre no mesmo canto/tamanho), revisar.

### Regra de execução pesada

Não rodar várias gerações de imagem, Chrome ou render pesado dentro do chat principal quando houver risco de travar a conversa. Para produção pesada, usar worker/subtarefa/fila, avisar status e manter o chat responsivo.

## QA final antes de entregar

Antes de enviar ao usuário, olhar o preview grid como diretora criativa, não só como render técnico.

Perguntas obrigatórias:

- A capa dá vontade de passar pro lado?
- A primeira lâmina tem força de campanha ou parece template?
- A composição varia de verdade entre os cards?
- O uso de foto está a favor da ideia, sem fórmula fixa nem reaproveitamento preguiçoso?
- O símbolo/logo está integrado à direção de arte, não carimbado?
- A marca é reconhecível mesmo sem explicar?
- O texto é legível no celular?
- O copy tem gancho, frase curta e CTA claro?
- Existe arco entre as lâminas ou são cards soltos?
- A imagem/asset prova o assunto específico?
- Isso faz o olho brilhar?

Se a resposta honesta for “não”, revise antes de entregar.

## Entrega

Para carrossel:

- PNGs individuais;
- preview grid;
- pacote `.tar.gz` quando houver múltiplos arquivos;
- nota curta do que foi gerado.

Salvar em:

```bash
/root/.openclaw/workspace/outputs/<slug-do-projeto>/
```
