# Emusys CSV — Ativos + Ex-alunos — Cross-check dos 28 casos

Data: 2026-05-31

## Arquivos analisados

1. Ativos / Em andamento:
   - `/root/.openclaw/media/inbound/relatorio_exportado_37---b67f075b-fd3b-4a64-88ca-25d38a6bad10.csv`
   - 499 linhas
   - todas com `Em Andamento`
   - soma `Qtd de Matriculas` = 569

2. Ex-alunos:
   - `/root/.openclaw/media/inbound/relatorio_exportado_38---1f966e39-19bb-48a3-9af2-9e4eebaed369.csv`
   - 1490 linhas
   - eventos extraídos: 1624 `Interrompido`, 159 `Concluído`

## Resultado consolidado dos 28 casos

| ID | Nome | CSV ativos | CSV ex-alunos | Leitura |
|---:|---|---|---|---|
| 106 | Emilly Souza de Oliveira | — | Interrompido em 2026-03-05 | Ex-aluna; Alf validou 2026-03-05 como data correta de saída |
| 1450 | Maria Eduarda de Lima Bomfim Pedro | Em andamento até 2027-03-09 | — | Ativa no Emusys; não preencher `data_saida` |
| 85 | Davi Borges da Silva Nascimento | — | Concluído em 2026-04-25; histórico anterior também existe | Ex-aluno; usar saída 2026-04-25 |
| 94 | Davi Rosendo Chaves Vieira | — | Concluído em 2026-04-01 | Ex-aluno; usar saída 2026-04-01 |
| 131 | Gabriel Pereira Morais | — | Concluído em 2026-03-03 | Ex-aluno; usar saída 2026-03-03 |
| 137 | Georgie Jefferson de Mello Basílio | — | Concluído em 2026-05-07 | Ex-aluno; usar saída 2026-05-07 |
| 149 | Guilherme Gama Clavelario Nunes | — | Concluído em 2026-05-04 | Ex-aluno; usar saída 2026-05-04 |
| 165 | Heitor Thadeu Caciano | — | Concluído em 2026-04-11 | Ex-aluno; usar saída 2026-04-11 |
| 224 | Laura Peres de Souza | — | Concluído em 2026-04-02 | Ex-aluno; usar saída 2026-04-02 |
| 258 | Luís Rafael Sousa dos Santos | — | Concluído em 2026-05-06 | Ex-aluno; usar saída 2026-05-06 |
| 270 | Manuela Piveta Schulz | — | Concluído em 2026-04-02; histórico anterior também existe | Ex-aluna; usar saída 2026-04-02 |
| 327 | Murilo Martellote de Assis | — | Interrompido em 2026-03-06; histórico anterior também existe | Ex-aluno; usar saída 2026-03-06 |
| 354 | Pedro Martellote de Assis | — | Interrompido em 2026-03-06; histórico anterior também existe | Ex-aluno; usar saída 2026-03-06 |
| 384 | Sophia Maciel Magalhaes | — | Concluído em 2026-04-10 | Ex-aluna; usar saída 2026-04-10 |
| 945 | Luciano da Silva Bernardino | — | — | Validado pelo Alf: aluno excluído/não matriculado; não contar como ativo/pagante |
| 11 | Alexandre Wallace Bispo Oliveira | — | Concluído em 2026-03-14 | Ex-aluno; usar saída 2026-03-14 |
| 118 | Felipe Marques Gevezier | — | Interrompido em 2026-03-02 e 2026-03-23 | Ex-aluno; usar saída efetiva 2026-03-23 se última matrícula encerrada nessa data |
| 1375 | Alan Samico do Nascimento | Em andamento até 2026-08-15 | — | Ativo no Emusys; não preencher `data_saida` |
| 1377 | Alexandre de Sousa Serra | — | Interrompido em 2026-04-01 | Ex-aluno; usar saída 2026-04-01 |
| 1378 | Ana Julia de Oliveira Gomes | Em andamento até 2026-08-15 | — | Ativa no Emusys; não preencher `data_saida` |
| 1393 | Leamsi Guedes de Sant'anna | Em andamento até 2026-08-15 | — | Ativo no Emusys; não preencher `data_saida` |
| 1598 | Alexandre Dos Santos | — | — | Validado pelo Alf: excluído do Emusys e inativo no LA Report; não contar como ativo/pagante |
| 31 | Anne Krissya Cordeiro da Silva Noé | Em andamento até 2027-04-06 e 2027-02-16 | — | Ativa no Emusys; limpar `data_saida` |
| 263 | Luiza Mazeliah do Nascimento | Em andamento até 2027-02-12 | — | Ativa no Emusys; limpar `data_saida` |
| 405 | Vicente Dias Botelho | Em andamento até 2026-12-12, 2027-03-18 e 2026-08-15 | — | Ativo no Emusys; limpar `data_saida` |
| 47 | Arthur Souza Del Bosco | — | Interrompido em 2026-01-09 | Ex-aluno; não limpar `data_saida`; status deve ser inativo |
| 323 | Miguel Santos Borges | Em andamento até 2026-09-26 | — | Ativo no Emusys; limpar `data_saida` |
| 949 | Cassyo L P Silva | Em andamento até 2026-12-19 (`Cassyo Lucas Prado Silva`) | — | Ativo no Emusys; limpar `data_saida` |

## Contagem dos 28

- Confirmados como ex-alunos no CSV ex-alunos: **17**
- Confirmados como ativos/em andamento no CSV ativos: **9**
- Não encontrados nos dois CSVs e resolvidos por validação do Alf: **2** (`Luciano da Silva Bernardino`, `Alexandre Dos Santos`)

## Mudança importante de decisão

O plano anterior de preencher `data_saida='2026-05-31'` para todos os inativos sem movimentação está **errado** após os CSVs.

O correto agora é:

1. Usar as datas reais do CSV ex-alunos para os encontrados como ex.
2. Não preencher `data_saida` em quem aparece no CSV de ativos.
3. Corrigir status/data no LA Report conforme o Emusys, mas só depois de uma reconciliação nominal completa, porque o total 499 bate, mas a composição nominal diverge.

## Ações recomendadas — sem executar ainda

### Preencher `data_saida` com data real do Emusys
Candidatos:
- 85 → 2026-04-25
- 94 → 2026-04-01
- 131 → 2026-03-03
- 137 → 2026-05-07
- 149 → 2026-05-04
- 165 → 2026-04-11
- 224 → 2026-04-02
- 258 → 2026-05-06
- 270 → 2026-04-02
- 327 → 2026-03-06
- 354 → 2026-03-06
- 384 → 2026-04-10
- 11 → 2026-03-14
- 118 → 2026-03-23 (se última matrícula encerrada nessa data)
- 1377 → 2026-04-01
- 47 → 2026-01-09 (já possui data_saida antiga; corrigir status para inativo)

### Casos com divergência/atenção
- 106 Emilly: divergência resolvida pelo Alf; usar `data_saida = 2026-03-05`.
- 945 Luciano da Silva Bernardino: validado pelo Alf como excluído/não matriculado; se não houver data real, usar `2026-05-31` como corte técnico de estoque.
- 1598 Alexandre Dos Santos: validado pelo Alf como excluído do Emusys e inativo no LA Report; se não houver data real, usar `2026-05-31` como corte técnico de estoque.

### Manter/reativar como ativos no LA Report
- 1450 Maria Eduarda
- 1375 Alan Samico
- 1378 Ana Júlia
- 1393 Leamsi
- 31 Anne
- 263 Luiza
- 405 Vicente
- 323 Miguel
- 949 Cassyo

## Próximo passo correto

Fazer reconciliação nominal completa entre:
- CSV Emusys ativos (499)
- CSV Emusys ex-alunos (1490)
- `alunos` no Supabase LA Report para Campo Grande

Só depois gerar SQL final. Não rodar RPC/backfill ainda.

Arquivo JSON auxiliar:
`outputs/sol-business-rules-audit/emusys_csv_active_ex_crosscheck_28_2026-05-31.json`
