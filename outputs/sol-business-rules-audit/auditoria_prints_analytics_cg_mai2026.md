# Auditoria de prints — Analytics Campo Grande Mai/2026

Prints recebidos em 2026-05-31.

## Tela/filtros
- Página: Analytics.
- Unidade: Campo Grande.
- Período: Mai/2026.
- Aba: Gestão.
- Subabas visíveis: Alunos, Financeiro, Retenção.

## Achados principais

1. Alunos ativos = 499.
2. Pagantes = 475 / 479 (99%).
3. Kids = 214 (43%); School = 351 (70%); Band = 41.
4. Novas matrículas = 23; evasões = 13; saldo líquido = 10.
5. Bolsistas integrais = 14; bolsistas parciais = 10.
6. Ticket médio = R$ 385 / R$ 387.
7. MRR = R$ 176.696; ARR = R$ 2.120.349.
8. Previsto = R$ 176.696; realizado = R$ 174.638; inadimplência = 1,3% / 1,5%.
9. Cancelamentos = 8; não renovações = 5; total evasões = 13.
10. Churn = 2,7% / 4,0%.
11. MRR perdido = R$ 1.719.
12. Renovações = 38; taxa renovação = 88,4% / 90,0%; aviso prévio = 8.
13. Tempo permanência = 19,6 meses.

## Divergências/pontos de validação

- Kids + School = 565, maior que total ativo 499; percentuais somam 113%.
- Pagantes 475 parece igual a 499 - 14 - 10, mas o denominador exibido é 479, não 499.
- Ticket médio não fecha com MRR / pagantes: 176.696 / 475 ≈ 372, não 385.
- ARR diverge R$ 3 de MRR arredondado x 12.
- Inadimplência 1,3% não fecha com (previsto-realizado)/previsto ≈ 1,16%.
- Churn 2,7% parece mais próximo de evasões/pagantes que evasões/ativos.
- MRR perdido médio por evasão é muito baixo comparado ao ticket médio.

## Próxima validação
Abrir o LA Report no navegador, reproduzir a tela com os mesmos filtros, inspecionar chamadas de rede e cruzar cada card com view/RPC/tabela de origem.
