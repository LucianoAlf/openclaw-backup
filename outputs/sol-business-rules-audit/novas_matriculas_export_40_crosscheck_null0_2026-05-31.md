# Cross-check — export_40 novas matrículas x casos valor NULL/0

Data: 2026-05-31
Arquivo: `/root/.openclaw/media/inbound/relatorio_exportado_40---29f6ce87-2534-4646-8728-cbbf270f0d11.csv`

## Resultado do CSV export_40

O CSV contém **23 matrículas em maio/2026**, todas com mensalidade positiva:

- 22 alunos com R$447,00
- 1 aluno com R$520,00 (Heitor Seixas da Rocha)

Isso bate com o número já validado de **23 novas matrículas** em CG/Maio.

## Cruzamento com os casos `valor_parcela NULL/0` do LA Report

Casos suspeitos/reconciliados:

- Ana Clara Lima Santos Pinto
- Anna Clara de Souza Iorio Sales / Sales Silva
- Sofia Elaile da Silva Campos
- Sofia Lauermann Silva
- Sarah Christina Mendes Silva
- Valkiria Carvalho Baeta
- Bruna Damasceno De Castro / Castro

Nenhum desses nomes aparece no CSV `export_40` de novas matrículas de maio.

## Datas no LA Report para os casos positivos/pedentes

- Ana Clara Lima Santos Pinto — data_matricula 2025-05-28
- Anna Clara de Souza Iorio Sales — data_matricula 2024-07-12
- Sofia Elaile da Silva Campos — data_matricula 2026-04-30
- Sofia Lauermann Silva — data_matricula 2026-04-27
- Sarah Christina Mendes Silva — data_matricula 2026-04-02
- Valkiria Carvalho Baeta — data_matricula 2026-04-22
- Bruna Damasceno De Castro — data_matricula 2026-02-27

Conclusão: estes alunos são reais e ativos, mas **não são novas matrículas de maio** segundo o `export_40`. São alunos de meses anteriores que aparecem como ativos/pagantes no Emusys, porém com `valor_parcela` NULL/0 ou duplicidade no LA Report.

## Implicação

O `export_40` valida separadamente o KPI de **23 novas matrículas**. Ele não resolve a divergência de pagantes 475/470/471, porque os casos NULL/0 não estão entre as matrículas novas de maio.

A divergência de pagantes segue sendo problema de cadastro/valor/sincronização em alunos ativos já existentes.
