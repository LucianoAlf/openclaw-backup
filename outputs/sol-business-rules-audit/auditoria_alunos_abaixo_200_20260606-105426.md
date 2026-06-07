# Auditoria — alunos com parcela positiva abaixo de R$200

Gerado em UTC: 2026-06-06T10:54:26

Escopo: SELECT-only. Alunos com status ativo/trancado, valor_parcela > 0 e < 200.

## Resumo

- Total de linhas/matrículas abaixo de R$200: **18**
- OK_EXCLUIDO_PELO_TIPO: **15**
- SEGUNDO_CURSO_ABAIXO_200_VERIFICAR: **2**
- RISCO_REGULAR_ABAIXO_200: **1**

Por unidade:
- Barra: **2**
- Campo Grande: **14**
- Recreio: **2**

## Casos de risco/prioridade

- **Kailane Marcos Barbosa** — Barra — Canto — R$190.0 — tipo `Regular`/`REGULAR` — conta_pagante=True — entra_ticket=True — classificação: **RISCO_REGULAR_ABAIXO_200**
- **Davi Guilherme De Souza Chaves Ribeiro** — Campo Grande — Harmonia — R$127.0 — tipo `Segundo Curso`/`SEGUNDO_CURSO` — conta_pagante=True — entra_ticket=True — classificação: **SEGUNDO_CURSO_ABAIXO_200_VERIFICAR**
- **Miguel Bittencourt Costa** — Campo Grande — Harmonia — R$149.0 — tipo `Segundo Curso`/`SEGUNDO_CURSO` — conta_pagante=True — entra_ticket=True — classificação: **SEGUNDO_CURSO_ABAIXO_200_VERIFICAR**

## Lista completa

| Nome | Unidade | Curso | Valor | Tipo | Pagante? | Ticket? | Classificação |
|---|---|---:|---:|---|---:|---:|---|
| Kailane Marcos Barbosa | Barra | Canto | R$190.0 | Regular | True | True | RISCO_REGULAR_ABAIXO_200 |
| Davi Guilherme De Souza Chaves Ribeiro | Campo Grande | Harmonia | R$127.0 | Segundo Curso | True | True | SEGUNDO_CURSO_ABAIXO_200_VERIFICAR |
| Miguel Bittencourt Costa | Campo Grande | Harmonia | R$149.0 | Segundo Curso | True | True | SEGUNDO_CURSO_ABAIXO_200_VERIFICAR |
| Leonardo Castro | Barra | Canto | R$180.0 | Bolsista Parcial | False | False | OK_EXCLUIDO_PELO_TIPO |
| Vinícius Lopa Mendes Rezende de Macedo | Campo Grande | Power Kids | R$40.0 | Matrícula em Banda | False | False | OK_EXCLUIDO_PELO_TIPO |
| Ana Mel Henrique da Silva | Campo Grande | Teclado | R$137.0 | Bolsista Parcial | False | False | OK_EXCLUIDO_PELO_TIPO |
| João Lucas Henrique da Silva | Campo Grande | Bateria | R$137.0 | Bolsista Parcial | False | False | OK_EXCLUIDO_PELO_TIPO |
| Ana Beatriz Da Conceição Pereira | Campo Grande | Canto | R$147.0 | Bolsista Parcial | False | False | OK_EXCLUIDO_PELO_TIPO |
| Jhonatan Samuel Vicente Silveira | Campo Grande | Guitarra | R$170.0 | Bolsista Parcial | False | False | OK_EXCLUIDO_PELO_TIPO |
| Jonathan de Lima Santos | Campo Grande | Canto | R$170.0 | Bolsista Parcial | False | False | OK_EXCLUIDO_PELO_TIPO |
| Laura Turques Tavares | Campo Grande | Musicalização para Bebês | R$170.0 | Bolsista Parcial | False | False | OK_EXCLUIDO_PELO_TIPO |
| Lucas Souza dos Santos | Campo Grande | Bateria | R$170.0 | Bolsista Parcial | False | False | OK_EXCLUIDO_PELO_TIPO |
| Maria Luiza Nogueira Leal | Campo Grande | Canto | R$190.0 | Bolsista Parcial | False | False | OK_EXCLUIDO_PELO_TIPO |
| Rayane Bianca dos Santos Stoianof Leite | Campo Grande | Violão | R$190.0 | Bolsista Parcial | False | False | OK_EXCLUIDO_PELO_TIPO |
| Sarah Ferreira dos Santos | Campo Grande | Canto | R$190.0 | Bolsista Parcial | False | False | OK_EXCLUIDO_PELO_TIPO |
| Vitoria Vivia dos Santos Costa | Campo Grande | Bateria | R$190.0 | Bolsista Parcial | False | False | OK_EXCLUIDO_PELO_TIPO |
| Larissa Bheattriz Barbosa Santos | Recreio | Canto | R$190.0 | Bolsista Parcial | False | False | OK_EXCLUIDO_PELO_TIPO |
| Daniel Eustáquio de Jesus | Recreio | Bateria | R$192.5 | Bolsista Parcial | False | False | OK_EXCLUIDO_PELO_TIPO |