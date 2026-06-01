# Emusys CSV ativos export_39 — reconciliação 475 → 474

Data: 2026-05-31
Arquivo: `/root/.openclaw/media/inbound/relatorio_exportado_39---674ca6b2-8324-4f59-a097-257be42fbeb4.csv`

## Contagem do CSV

- Linhas/alunos ativos no CSV: **499**.
- Nomes únicos: **499**.
- Matrículas em andamento por ocorrência textual: **569**.
- Projetos/banda no CSV por `Curso(s)`:
  - Minha Banda Para Sempre: 32
  - Power Kids: 13
  - Total: 45

Observação: o CSV de ativos do Emusys não traz `tipo_matricula`/bolsa de forma suficiente para reproduzir exatamente o KPI “pagantes” do LA Report/relatório ADM. Contar mensalidade positiva no CSV dá 479, não 475, porque há regras internas de tipo de matrícula/bolsa/não pagante no LA Report.

## Evidências nominais

### Barbara Ribeiro Alves

No CSV ativo export_39:
- Barbara Ribeiro Alves aparece como ativa.
- Matrículas em andamento:
  - Minha Banda Para Sempre — mensalidade 0,00
  - Home Studio — mensalidade 520,00
- Qtd operacional: duas matrículas ativas, sendo uma aula regular pagante.

No LA Report/Supabase:
- id 49: Minha Banda Para Sempre, ativo, Regular/pagante, `is_projeto_banda=true`, `is_segundo_curso=false`.
- id 1413: Home Studio, ativo, Segundo Curso/pagante, `is_projeto_banda=false`, `is_segundo_curso=true`, valor 499.

Conclusão: Barbara deve continuar contando como pessoa ativa/pagante uma vez. Ela não explica a diferença 475→474.

### Arthur Souza Del Bosco

No CSV ativo export_39:
- Arthur Souza Del Bosco **não aparece**.

No CSV de ex-alunos anterior:
- Arthur Souza Del Bosco aparece como Bateria interrompido em 09/01/2026.

Nos prints do Emusys:
- Histórico confirma matrícula finalizada e observação de instabilidade que o fez voltar a ser contabilizado indevidamente; não deveria ser considerado nos cálculos.

No LA Report/Supabase:
- Antes do saneamento v4, o guard do update provou que Arthur estava `status='ativo'` com `data_saida='2026-01-09'`.
- Após saneamento: `status='inativo'`, `data_saida='2026-01-09'`.

Conclusão: Arthur explica a queda visível de 1 pagante no relatório status-based: 475→474.

## Conclusão operacional

A justificativa para ADMs/DM deve ser:

> A diferença de 475 para 474 pagantes foi a correção do Arthur Souza Del Bosco, que aparecia como ativo no LA Report por inconsistência, mas no Emusys consta como interrompido/ex-aluno desde 09/01/2026. A Barbara Ribeiro Alves continua ativa/pagante, com Minha Banda Para Sempre e Home Studio em andamento, e não foi removida da base.

## Bloqueio

Não gerar migration de `recalcular_dados_mensais` baseada em exclusão cega de `is_projeto_banda=true`. A regra precisa ser por pessoa:
- aluno só banda/projeto gratuito pode não contar como pagante/curso;
- aluno com curso regular ativo, mesmo que esse curso esteja como segundo curso, deve contar uma vez como ativo/pagante.
