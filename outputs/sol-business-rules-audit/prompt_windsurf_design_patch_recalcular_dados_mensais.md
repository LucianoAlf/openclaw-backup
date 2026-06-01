Windsurf, boa auditoria. O diagnóstico geral está aprovado: `dados_mensais` é necessário como snapshot histórico, mas está incompleto, tem colunas zombie/hidden e a função `recalcular_dados_mensais` não reflete todas as regras canônicas.

Mas há uma correção importante do Alfredo:

Você marcou `churn_rate` como fórmula correta, mas a função usa pagantes do mês anterior:

```sql
v_evasoes / v_pagantes_anterior
```

A regra validada no caso Campo Grande/Maio foi:

```text
churn = evasões realizadas / pagantes do mês corrente
13 / 475 = 2,74% (~2,7%)
```

A função gravou/retornou 2,83% porque usa base anterior. Então antes de patchar, trate o denominador do churn como decisão explícita:

- Se churn = evasões / pagantes atuais, a função está errada.
- Se churn = evasões / base inicial/mês anterior, a view live está errada.
- Até agora, regra validada com Alf: base pagante atual.

Novo pedido: não crie migration ainda. Faça uma proposta DESIGN/READ-ONLY de patch para `recalcular_dados_mensais`, sem aplicar.

A proposta deve conter:

1. Lista exata de mudanças na função
   - sem executar.

2. Corrigir novas_matriculas com os mesmos filtros canônicos da view:
   - excluir segundo curso
   - excluir banda/projeto
   - excluir canto coral
   - excluir bolsista integral/parcial

3. Corrigir/calcular taxa_renovacao:
   - fonte: `movimentacoes_admin`
   - renovações = `tipo='renovacao'`
   - não renovações = `tipo='nao_renovacao'`
   - taxa = renovações / (renovações + não renovações)

4. Corrigir/calcular reajuste_medio/reajuste_parcelas:
   - fonte: `movimentacoes_admin`
   - somente `tipo='renovacao'`
   - só aumentos positivos
   - `valor_parcela_anterior > 0`
   - `valor_parcela_novo > valor_parcela_anterior`

5. Corrigir/gravar faturamento_estimado e saldo_liquido se essas colunas continuarem no snapshot:
   - hoje a função calcula no JSON, mas não grava no INSERT/UPDATE.

6. Avaliar inadimplencia:
   - coluna existe e é usada, mas a função não popula.
   - dizer se há fonte confiável para calcular agora ou se deve ficar fora do patch.

7. Avaliar alunos_ativos:
   - função usa `data_saida` para snapshot histórico.
   - comparar com regra operacional atual `status IN ('ativo','trancado')`.
   - propor critério correto para snapshot histórico, sem assumir.

8. Avaliar `TabGestao.tsx` depois da função:
   - usar `dados_mensais.alunos_ativos` em histórico, não `alunos_pagantes` como proxy.
   - usar `matriculas_banda` se for KPI histórico.
   - remover fallback que consulta `renovacoes`.

9. Estratégia de backfill:
   - listar meses/unidades a recalcular primeiro em ambiente seguro.
   - validar antes/depois para Jan–Mai/2026.
   - não sobrescrever histórico útil sem tabela de comparação.

Entregue apenas o plano/diff proposto. Não aplicar nada ainda.
