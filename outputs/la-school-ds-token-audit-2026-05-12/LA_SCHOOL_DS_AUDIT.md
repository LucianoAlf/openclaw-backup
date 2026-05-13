# LA Music School — Auditoria DS para Skill

Fonte analisada:
- Link: https://design-system-la-music.netlify.app
- HTML anexado pelo Alf: `/root/.openclaw/media/inbound/la-music-design-system---8b287cb8-bb46-484d-9b31-127d7e6c2011.html`
- Canônico local conferido: `repos/la-hq-agents/shared/design-systems/LA_MUSIC_SCHOOL_DS_CANONICAL.md`

## Correções do Alf incorporadas
1. Logomarca principal deve ficar no topo centralizado em todos os cards.
2. Container/card pink é recurso bom, mas não pode aparecer em todos os cards.
3. Skill precisa usar o vocabulário inteiro do Design System, não só pink card + foto.

## Tokens oficiais
- `#E91451` Pink Primary — marca, CTA, pills, palavra-chave.
- `#373435` Dark LA — texto/logo em fundo claro.
- `#B01545` Pink Shade — halftone/gradientes.
- `#740A28` Pink Deep — sombra, marca d’água, profundidade.
- `#F06292` Pink Light — detalhes suaves.
- `#0A0A0A` Black — fundo dark.
- `#141414` Black Soft — cards/sombras.
- `#E8E8E8` Gray Light — fundo claro canônico; não usar cream/bege.
- `#9E9E9E` Gray Mid — textos auxiliares.
- `#FFFFFF` White — texto/outline.
- Fonte única: Prompt, pesos 100/300/400/500/600/700/900.

## Vocabulário visual obrigatório
1. Logo principal no topo — regra de consistência.
2. Footer pill + listras — fechamento recorrente.
3. Halftone orgânico — textura dominante; nunca grid morto.
4. Marca d’água LA solo/outline — grande, sangrando, integrada.
5. Texto sólido + outline — assinatura tipográfica.
6. Container pink inclinado — usar com parcimônia.
7. Chevrons »»» — detalhe de movimento.
8. Padrão de + — textura secundária.
9. Pill de contato — CTA inline/WhatsApp/@.

## Temas para alternância
- Dark Mode — foto, palco, instrumento, atmosfera.
- Pink Gradient — capa/convite/impacto.
- Light Mode — conteúdo educativo mais respirado.
- Pink Solid — CTA final/chamada direta.

## Regra para a skill `lahq-school-content`
A skill não deve gerar layout fixo. Ela deve obrigar a escolha consciente por card:
- header: logo oficial topo/centro;
- tema do card: dark, pink gradient, light ou pink solid;
- recurso dominante: foto, halftone, watermark LA, outline type, pink container, CTA pill;
- fechamento: footer pill + listras quando fizer sentido;
- QA: se todos os cards usam o mesmo container pink ou mesma lógica, reprovar.

## Imagens geradas para aprovação
- `01-tokens-paleta.png`
- `02-vocabulario-visual.png`
- `03-temas.png`
- `04-anatomia-post.png`
- `05-regras-skill.png`
- `06-componentes-aprovacao.png`
- `contact-sheet.png`
