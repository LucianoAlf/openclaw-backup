# Auditoria — 19 casos com parcela NULL/0

Origem: prints enviados pelo Alf em 2026-06-01.
Objetivo: separar casos de banda/projeto vs casos que precisam investigação individual no Emusys, LAHQ e banco.

## Regra operacional inicial

- Power Kids = banda/projeto.
- Minha Banda Para Sempre = banda/projeto.
- Casos REGULAR com curso comum e valor NULL/0 precisam investigação cadastral/financeira.
- Caso SEGUNDO_CURSO com curso comum e `is_projeto_banda=false` precisa investigação individual.

---

## A) Prováveis banda/projeto — validar como tratamento financeiro especial

| # | Nome | Curso | Valor | Tipo/grupo no print | Observação |
|---|------|-------|-------|---------------------|------------|
| 3 | Barbara Ribeiro Alves | Minha Banda Para Sempre | NULL | REGULAR | Curso é banda, mas está como REGULAR. Verificar tipo_matricula/cadastro. |
| 6 | Alexandre Ayres Filho | Power Kids | 0,00 | SEGUNDO_CURSO | Banda/projeto. |
| 7 | Alice Roza Baltar | Power Kids | NULL | SEGUNDO_CURSO | Banda/projeto. |
| 8 | Antonia Scucio Giudi da Rocha | Power Kids | NULL | SEGUNDO_CURSO | Banda/projeto. |
| 9 | Eduardo França Tristão Batista | Minha Banda Para Sempre | NULL | SEGUNDO_CURSO | Banda/projeto. |
| 10 | Gabriel Gomes Chaves | Power Kids | 0,00 | SEGUNDO_CURSO | Banda/projeto. |
| 11 | Julia da Costa de Oliveira | Power Kids | NULL | SEGUNDO_CURSO | Banda/projeto. |
| 12 | Maria Miranda Pereira | Power Kids | 0,00 | SEGUNDO_CURSO | Banda/projeto. |
| 13 | Marina de Albuquerque Bulhões Silva | Power Kids | NULL | SEGUNDO_CURSO | Banda/projeto. |
| 14 | Miguel Bittencourt Costa | Power Kids | 0,00 | SEGUNDO_CURSO | Banda/projeto. |
| 15 | Pedro Alves Pereira | Power Kids | 0,00 | SEGUNDO_CURSO | Banda/projeto. |
| 16 | Pedro Gabriel da França Rocha Pinto | Power Kids | 0,00 | SEGUNDO_CURSO | Banda/projeto. |
| 17 | Vicente Dias Botelho | Power Kids | 0,00 | SEGUNDO_CURSO | Banda/projeto. |
| 18 | Vinícius Lopa Mendes Rezende de Macedo | Power Kids | NULL | SEGUNDO_CURSO | Banda/projeto. |

### Hipótese para este bloco
Esses casos provavelmente não devem compor ticket médio como pagantes normais se forem projeto/cortesia/passaporte/banda embutida. O ponto é conferir se o cadastro financeiro está coerente e se a regra do LAHQ/banco reconhece isso.

---

## B) Casos não-banda — investigar aluno por aluno

| # | Nome | Curso | Valor | Tipo/grupo no print | Observação |
|---|------|-------|-------|---------------------|------------|
| 1 | Ana Clara Lima Santos Pinto | Canto | NULL | REGULAR | Já apareceu como pendência; precisa conferir Emusys/LAHQ/DB. |
| 2 | Anna Clara de Souza Iorio Sales | Teclado | 0,00 | REGULAR | Já apareceu como pendência; precisa conferir Emusys/LAHQ/DB. |
| 4 | Sofia Elaile da Silva Campos | Violino | NULL | REGULAR | Regular com NULL; provável erro de valor/cadastro. |
| 5 | Sofia Lauermann Silva | Canto | NULL | REGULAR | Regular com NULL; provável erro de valor/cadastro. |
| 19 | Vitória Vívia dos Santos Costa | Piano | 0,00 | SEGUNDO_CURSO | Não é banda (`is_projeto_banda=false`). Pode ser segundo curso legítimo, bolsa/cortesia ou erro. |

---

## C) Ordem sugerida de checagem

Para cada aluno:

1. Emusys
   - matrícula ativa/inativa;
   - curso principal e curso extra;
   - plano/valor real;
   - bolsa, cortesia, passaporte, banda ou pacote;
   - responsável/pagante.

2. LAHQ
   - tipo_matricula;
   - conta_como_pagante;
   - entra_ticket_medio;
   - status_pagamento;
   - valor_parcela recebido/salvo.

3. Banco de dados
   - linha de matrícula correta;
   - duplicidade;
   - valor NULL vs 0;
   - is_projeto_banda;
   - regra que está classificando como REGULAR/SEGUNDO_CURSO.

---

## D) Decisão provável por bloco

- Banda/projeto: não corrigir como mensalidade comum antes de confirmar a regra. O ajuste provável é classificação/regra financeira, não cobrar valor.
- Regular NULL/0: provável erro de cadastro/sync/valor_parcela.
- Vitória Vívia: caso avulso; precisa decidir se é segundo curso gratuito legítimo ou erro de classificação/valor.
