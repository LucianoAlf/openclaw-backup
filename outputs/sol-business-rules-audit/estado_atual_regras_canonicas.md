# Estado atual — regras canônicas e pendências LA Report / Sol

Atualizado em 2026-05-31.

## Canônico 100% validado

1. Alunos ativos incluem trancados.
2. Base de alunos ativos exclui segundo curso para não duplicar pessoa.
3. Matrículas ativas são registros/matrículas e podem ser maiores que alunos.
4. Matrículas ativas incluem primeiro curso, segundo curso, banda e coral.
5. Kids/School, no card de Analytics > Gestão, é percentual sobre a base de alunos ativos/pessoas, não sobre matrículas brutas.
6. Kids/School deve usar a mesma base do Total Alunos Ativos: inclui trancados e exclui segundo curso.
7. Pagantes excluem bolsista integral, bolsista parcial e não pagante.
8. Bolsista parcial não conta como pagante.
9. Segundo curso = aluno pagante fazendo 2º/3º curso pagando.
10. Segundo curso não inclui banda/projeto nem bolsista.
11. Aviso prévio não é evasão.
12. Evasão = cancelamento + não renovação.
13. Taxa renovação = renovações / (renovações + não renovações).
14. Barra do card é meta, não denominador operacional. Ex.: 475 / 479 → 479 é meta do mês.
15. Mês corrente usa tempo real/view; `dados_mensais` é snapshot/fechamento.
16. `dados_mensais` pode ficar defasado antes de recalcular/fechar.

## Resolvido/corrigido

- Kids/School em Campo Grande/Maio foi corrigido para 204 Kids + 295 School = 499 alunos ativos.

## Ainda precisa validar / resolver

1. Evasões: arquitetura entre `movimentacoes_admin` e `evasoes_v2`.
2. Segundo curso CG: regra clara, mas fechar nominalmente o número 28.
3. Trancados CG: regra correta é 2, mas banco bruto mostra 5; identificar quais 3 não entram e por quê.
4. Comercial: regra de matrícula comercial, passaporte pago, comissão e matrícula feita por professor.
5. Legado: mapa de tabelas atuais, históricas úteis e lixo perigoso.
