# Emusys CSV — Ativos / Em andamento — Campo Grande — Cross-check 28 casos

Data: 2026-05-31
Arquivo: `/root/.openclaw/media/inbound/relatorio_exportado_37---b67f075b-fd3b-4a64-88ca-25d38a6bad10.csv`
Encoding detectado: ISO-8859-1 / Latin-1

## Leitura do arquivo

- Linhas/alunos no CSV: **499**
- Todas as linhas contêm `Em Andamento` em `Matriculas / Situação`.
- Soma de `Qtd de Matriculas`: **569**
- Isso sugere que o CSV é um relatório de alunos/matrículas em andamento no Emusys, e bate em quantidade de pessoas com o `Total Alunos Ativos` validado no LA Report (**499**), mas não necessariamente com a mesma composição nominal.

## Resultado contra os 28 casos do saneamento

| Lote | ID LA Report | Nome LA Report | Encontrado no CSV Emusys? | Evidência |
|---|---:|---|---|---|
| A1 | 106 | Emilly Souza de Oliveira | NÃO | Ausente; já havia evasão em 2026-03-07 |
| B1 | 1450 | Maria Eduarda de Lima Bomfim Pedro | SIM | `Maria Eduarda de Lima  Bomfim Pedro`, Em Andamento, mensalidade 0,00, conclusão 09/03/2027 |
| B2 | 85 | Davi Borges da Silva Nascimento | NÃO | Ausente |
| B2 | 94 | Davi Rosendo Chaves Vieira | NÃO | Ausente |
| B2 | 131 | Gabriel Pereira Morais | NÃO | Ausente |
| B2 | 137 | Georgie Jefferson de Mello Basílio | NÃO | Ausente |
| B2 | 149 | Guilherme Gama Clavelario Nunes | NÃO | Ausente |
| B2 | 165 | Heitor Thadeu Caciano | NÃO | Ausente |
| B2 | 224 | Laura Peres de Souza | NÃO | Ausente |
| B2 | 258 | Luís Rafael Sousa dos Santos | NÃO | Ausente |
| B2 | 270 | Manuela Piveta Schulz | NÃO | Ausente |
| B2 | 327 | Murilo Martellote de Assis | NÃO | Ausente |
| B2 | 354 | Pedro Martellote de Assis | NÃO | Ausente |
| B2 | 384 | Sophia Maciel Magalhaes | NÃO | Ausente |
| B2 | 945 | Luciano da Silva Bernardino | NÃO | Ausente |
| B2 | 11 | Alexandre Wallace Bispo Oliveira | NÃO | Ausente |
| B2 | 118 | Felipe Marques Gevezier | NÃO | Ausente |
| B2 | 1375 | Alan Samico do Nascimento | SIM | Em Andamento, mensalidade 0,00, conclusão 15/08/2026 |
| B2 | 1377 | Alexandre de Sousa Serra | NÃO | Ausente |
| B2 | 1378 | Ana Julia de Oliveira Gomes | SIM | `Ana Júlia de Oliveira Gomes`, Em Andamento, mensalidade 0,00, conclusão 15/08/2026 |
| B2 | 1393 | Leamsi Guedes de Sant'anna | SIM | `Leamsi Guedes de Sant'Anna`, Em Andamento, mensalidade 0,00, conclusão 15/08/2026 |
| B2 | 1598 | Alexandre Dos Santos | NÃO | Ausente |
| B3 | 31 | Anne Krissya Cordeiro da Silva Noé | SIM | Em Andamento, 2 matrículas, conclusão 06/04/2027 e 16/02/2027 |
| B3 | 263 | Luiza Mazeliah do Nascimento | SIM | Em Andamento, mensalidade 520,00, conclusão 12/02/2027 |
| B3 | 405 | Vicente Dias Botelho | SIM | Em Andamento, 3 matrículas, mensalidades 447,00 / 0,00 |
| B4 | 47 | Arthur Souza Del Bosco | NÃO | Ausente |
| B4 | 323 | Miguel Santos Borges | SIM | Em Andamento, mensalidade 447,00, conclusão 26/09/2026 |
| B4 | 949 | Cassyo L P Silva | SIM | CSV: `Cassyo Lucas Prado Silva`, Em Andamento, mensalidade 447,00, conclusão 19/12/2026 |

## Implicação importante

O CSV **derruba a hipótese anterior de aplicar `data_saida = 2026-05-31` em todos os inativos sem movimentação**.

Quatro alunos que estavam no grupo `status='inativo' + data_saida NULL` aparecem como ativos/em andamento no Emusys:

- Maria Eduarda de Lima Bomfim Pedro — id 1450
- Alan Samico do Nascimento — id 1375
- Ana Júlia de Oliveira Gomes — id 1378
- Leamsi Guedes de Sant'Anna — id 1393

Esses casos não devem receber `data_saida`. O correto provável é corrigir `status` no LA Report para ativo ou reconciliar a origem, mantendo-os como não pagantes/bolsistas/projeto conforme regra.

## Recomendações revisadas

### Seguros com evidência
- Emily id 106: preencher `data_saida = '2026-03-07'`, pois há evasão real e ela não aparece no CSV ativo.
- Anne id 31, Luiza id 263, Vicente id 405, Miguel id 323, Cassyo id 949: aparecem ativos no Emusys; limpar `data_saida = NULL` parece correto, com validação do Alf.
- Arthur id 47: não aparece no CSV ativo; se LA Report está `status='ativo'`, provável corrigir status para `inativo` e NÃO limpar `data_saida`.

### Requerem decisão revisada
- Maria id 1450, Alan id 1375, Ana Júlia id 1378, Leamsi id 1393: aparecem ativos no Emusys apesar de estarem inativos no LA Report; não aplicar `data_saida=2026-05-31`. Avaliar `status='ativo'` e manter não pagantes/bolsistas/projeto.
- Os demais 17 B2 ausentes do CSV podem receber `data_saida='2026-05-31'` como corte técnico de estoque Maio, mas não como história perfeita Jan–Abr, e sem criar `movimentacoes_admin` retroativa.

## Atenção sobre total

- LA Report live: 499 ativos / 475 pagantes.
- CSV Emusys: 499 linhas em andamento.
- Mas a composição nominal não é idêntica: existem alunos no CSV que estão inativos no LA Report e alunos ativos no LA Report que não aparecem no CSV.
- Portanto, antes de qualquer SQL, o próximo passo correto é uma reconciliação nominal CSV x Supabase, não só os 28 casos.

Arquivo bruto de comparação auxiliar salvo em:
`outputs/sol-business-rules-audit/emusys_csv_vs_lareport_snapshot_cg_maio_2026.json`
