# Reconciliação — 475 vs 473 pagantes — Campo Grande/Maio 2026

Data: 2026-05-31

## Pergunta do Alf

Alf questionou: o relatório administrativo da unidade Campo Grande em 30/05/2026 mostrava 475 alunos pagantes, mas a simulação pós-saneamento + regra banda apontou 473. Onde estão os 2?

## Resposta nominal

Os 2 são:

1. **Arthur Souza Del Bosco — id 47**
   - Antes do saneamento, estava `status='ativo'`, `tipo_matricula=Regular`, portanto entrava no relatório vivo/status-based como pagante.
   - Foi validado no saneamento que deve ficar `status='inativo'` e manter `data_saida='2026-01-09'`.
   - Sai da base após limpeza de ciclo de vida.
   - Impacto: 475 → 474.

2. **Barbara Ribeiro Alves — id 49**
   - Está `status='ativo'`, `tipo_matricula=Regular`, `curso='Minha Banda Para Sempre'`, `is_projeto_banda=true`.
   - Entra como pagante na regra antiga/status-based do relatório.
   - Sai se a nova regra “banda/projeto-only não conta como aluno ativo/pagante de curso” for aplicada.
   - Impacto: 474 → 473.

## Camadas de contagem

| Base / regra | Pagantes |
|---|---:|
| Relatório administrativo antes do saneamento | 475 |
| Mesma lógica após saneamento de Arthur | 474 |
| Após saneamento + exclusão de projeto/banda de pagantes | 473 |

## Observação importante

A simulação `495/473/567/43` não é a mesma métrica do relatório administrativo original `499/475/565/41`.

Ela mistura:
- fechamento histórico por `data_matricula/data_saida`;
- saneamento de ciclo de vida;
- nova regra excluindo projeto/banda de `alunos_ativos`/`alunos_pagantes`.

Portanto, não deve ser tratada como substituto automático do relatório da unidade sem validação explícita da regra final.

## Decisão operacional recomendada

Pausar a migration de `recalcular_dados_mensais` até reconciliar nominalmente:
- se Barbara deve ou não contar como pagante no fechamento;
- se `matriculas_banda` histórica deve ser 43 (por data) ou 41 (por status atual/relatório vivo);
- se `dados_mensais` deve preservar o fechamento validado da unidade ou recalcular historicamente com dados saneados.
