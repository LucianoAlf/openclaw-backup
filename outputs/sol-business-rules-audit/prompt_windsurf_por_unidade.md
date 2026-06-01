# Prompt Windsurf — auditoria por unidade LA Report

Use este prompt separadamente para cada unidade: Campo Grande, Recreio e Barra.

```md
Você é o agente do LA Music Performance Report. Vamos auditar divergências por unidade, não consolidado.

Unidade: [CAMPO GRANDE / RECREIO / BARRA]
Período: Maio/2026

Premissas validadas pelo Alf, fonte final da regra de negócio:

1. “Alunos ativos” inclui alunos trancados.
2. Kids/School deve ser percentual sobre matrículas, não sobre alunos únicos.
3. Pagantes excluem bolsista integral, bolsista parcial e não pagante.
4. Segundo curso só conta quando aluno pagante faz segundo/terceiro curso pagando.
   - Bolsista parcial não conta em segundo curso.
   - Banda/projeto também não deve inflar segundo curso pagante.
5. Evasões operacionais = cancelamentos/evasão + não renovação.
   - Aviso prévio não é evasão.
6. Taxa renovação = renovações / (renovações + não renovações).
7. Mês corrente deve priorizar views em tempo real; `dados_mensais` é snapshot/fechamento e pode estar defasado.
8. `movimentacoes_admin` provavelmente é fonte operacional de evasões, mas `evasoes_v2` precisa ser auditada porque guarda histórico/tempo de permanência.

Tarefa:

Para a unidade [UNIDADE], Maio/2026, levante:

## 1. Números atuais no banco/view/frontend
- total_alunos_ativos
- total_alunos_pagantes
- bolsistas integrais
- bolsistas parciais
- matrículas ativas
- matrículas banda
- matrículas segundo curso pagante correto
- trancados
- novas matrículas
- evasões/cancelamentos
- não renovações
- avisos prévios
- renovações realizadas
- taxa renovação
- churn
- ticket médio
- MRR
- inadimplência

## 2. Divergências
Compare:
- `vw_kpis_gestao_mensal`
- `vw_kpis_retencao_mensal`
- `dados_mensais`
- queries diretas em `alunos`
- queries diretas em `movimentacoes_admin`
- `evasoes_v2`
- código frontend `TabGestao.tsx`

## 3. Segundo curso
Liste nominalmente os registros que estão como `is_segundo_curso=true`, agrupando:
- pagante regular que deve contar
- bolsista parcial/integral que NÃO deve contar
- banda/projeto que NÃO deve contar
- possíveis marcações erradas

## 4. Trancados
Liste nominalmente todos os registros com `status='trancado'` e diga quais deveriam contar no relatório operacional.

## 5. Evasões / aviso prévio
Confirme se alguma view ainda soma aviso prévio em evasão. Se sim, marque como bug.

## 6. Saída auditável
Responda neste formato:

### Unidade: [UNIDADE]

| Item | Valor view | Valor query direta | Valor regra validada | Status | Causa provável | Correção |
|---|---:|---:|---:|---|---|---|

Depois liste:
- Bugs de SQL/view
- Bugs de frontend/rótulo
- Dados sujos no banco
- Pontos para Hugo/equipe validarem
- Pontos que dependem do Alf
```
