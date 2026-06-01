# Lista de divergências — Campo Grande — Maio/2026

Fonte: auditoria Alfredo + Windsurf + validações do Alf.

## Regras já validadas pelo Alf

- Alunos ativos incluem trancados.
- Kids/School deve ser percentual sobre matrículas.
- Pagantes excluem bolsista integral, bolsista parcial e não pagante.
- Segundo curso só conta quando aluno pagante faz segundo/terceiro curso pagando.
- Banda/projeto não deve inflar segundo curso pagante.
- Evasões operacionais = cancelamentos/evasão + não renovação.
- Aviso prévio não é evasão.
- Taxa renovação = renovações / (renovações + não renovações).
- Mês corrente usa views em tempo real; `dados_mensais` é snapshot/fechamento e pode estar defasado.

## Divergências para validar/corrigir

| Prioridade | Item | Sistema mostra | Regra/relatório correto | Status | Ação |
|---|---:|---:|---:|---|---|
| 🔴 Alta | `vw_kpis_retencao_mensal.total_evasoes` | 21 | 13 | Bug SQL confirmado | Remover `aviso_previo` da CTE de evasões |
| 🔴 Alta | Taxa renovação nas views | 100% | 88,4% | Bug SQL/dado confirmado | Usar não-renovações no cálculo ou corrigir sync/população |
| 🟡 Média | Segundo curso | 66 na view | 28 operacional | Divergência de filtro | Criar `segundo_curso_pagante` excluindo banda/bolsista/não pagante |
| 🟡 Média | Trancados | 5 no banco | 2 no relatório | Precisa equipe/Hugo | Validar critério: todos atuais, só do mês, ou outro corte |
| 🟡 Média | Kids/School % | Numerador 565 / denominador 499 | Percentual sobre matrículas | Bug frontend/rótulo | Usar denominador de matrículas |
| 🟡 Média | Banda | 41, todos 2º curso | Pendente Alf | Regra pendente | Definir se card Banda mostra todos participantes de banda |
| 🟢 Baixa | `dados_mensais` | defasado | snapshot atualizado | Operacional | Recalcular snapshot de maio/2026 |
| 🟢 Baixa/Média | `evasoes_v2` | vazia em maio/2026 | preservar histórico | Arquitetura pendente | Auditar trigger/sync com `movimentacoes_admin` |

## Pontos nominais para equipe/Hugo

### Trancados no banco: 5
- Adriana Vitor Pim — Teclado — REGULAR — 1º curso
- Beatriz Cardoso Schmitz — Canto — REGULAR — 1º curso
- Ester Santos do Amaral — Canto — REGULAR — 1º curso
- Jonatas Viana Carvalho — Canto — REGULAR — 1º curso
- Rayane Bianca dos Santos Stoianof Leite — Violão — SEGUNDO_CURSO — trancado

Relatório operacional diz 2. Precisamos saber quais 2 a equipe considera válidos e por quê.

### Segundo curso — pontos suspeitos
Windsurf encontrou 27 pagantes pela query corrigida, mas o relatório operacional fala 28. Alf indicou que Vitória/funcionária/bolsista parcial aparece indevidamente e não deve contar.

Regra esperada: segundo curso pagante deve ter aluno pagante regular, curso regular, valor válido, não banda/projeto, não bolsista.

Casos para checar:
- Carlos Eduardo Garcia do Nascimento — Canto — R$ 0,00
- Vitoria Vivia dos Santos Costa — Piano — R$ 0,00
- Eduardo França Tristão Batista — Minha Banda — valor null

## Perguntas objetivas para Hugo/equipe

1. Quais são os 2 trancados considerados no relatório de Campo Grande em maio/2026?
2. O relatório de trancados usa data de corte, período do mês, ou saldo atual?
3. A contagem de segundo curso correta é 28. Quais são os 28 nomes considerados pela equipe?
4. Dos registros marcados como segundo curso, quais devem ser excluídos por serem banda, bolsistas ou valor zero?
5. O card Banda deve mostrar todos os participantes de banda/projeto, mesmo sendo segundo curso?
6. Podemos consolidar não-renovações em `movimentacoes_admin` como fonte operacional e manter `evasoes_v2` só/histórico analítico?

---

## Atualização após novos prints do frontend Administrativo

Os novos prints mostram que algumas divergências são de **query bruta/view**, não necessariamente do frontend final:

- Frontend Administrativo mostra `Trancados = 2`, batendo com relatório da equipe.
- Frontend Administrativo mostra `Renovações = 38`, `Não renovação = 5`, `Taxa = 88,4%`, correto.
- Frontend Administrativo mostra `Cancelamentos = 8`, `Não renovação = 5`, `Evasões = 13`, `Churn = 2,7%`, correto.
- Kids + School = 565 bate com `Matrículas Ativas = 565`.

### Ajuste de interpretação
Não dizer “frontend está errado” de forma genérica. O frontend em várias telas está certo.

Problema real parece ser:
1. Algumas views têm campos errados ou ambíguos.
2. Algumas queries brutas não aplicam o mesmo critério operacional do frontend/relatório.
3. Alguns rótulos/denominadores podem confundir, especialmente Kids/School % e `475 / 479`.

### Ponto que continua precisando explicação
`Alunos Pagantes 475 / 479`:
- 475 é correto.
- 479 provavelmente é meta (`metas_kpi.alunos_pagantes`), não base operacional.
- Se usuário/equipe interpretar `/479` como denominador real, confunde.
