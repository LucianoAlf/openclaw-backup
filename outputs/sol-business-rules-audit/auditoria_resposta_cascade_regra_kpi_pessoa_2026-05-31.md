# Auditoria Alfredo — resposta Cascade `AUDITORIA_REGLA_KPI_CG_MAIO2026`

Data: 2026-05-31
Arquivos auditados:
- `AUDITORIA_REGLA_KPI_CG_MAIO2026---831f6813-d07e-46b9-a578-9f24b71b631d.md`
- `AUDITORIA_REGLA_KPI_CG_MAIO2026---ba771c8f-c0b4-49ac-af28-d6e7b797faec.sql`
- CSV ativo Emusys `relatorio_exportado_39---674ca6b2-8324-4f59-a097-257be42fbeb4.csv`
- Banco LA Report/Supabase pós-saneamento v4

## Veredito

**Não aprovar migration nem regra final ainda.**

Cascade acertou o alerta conceitual principal: KPIs de pessoa não podem ser tratados cegamente row-by-row, porque casos como Barbara podem sumir indevidamente.

Mas a proposta `499 ativos / 476 pagantes / 564 matrículas / 41 banda` **não pode virar alvo final**. Ela ainda inclui sujeira e pagante falso.

## O que está certo

1. Correto: Barbara Ribeiro Alves prova que a regra row-by-row é perigosa.
   - id 49: Minha Banda Para Sempre, `is_projeto_banda=true`, `is_segundo_curso=false`, Regular/pagante.
   - id 1413: Home Studio, `is_projeto_banda=false`, `is_segundo_curso=true`, Segundo Curso/pagante, valor 499.
   - No CSV Emusys ativo: Minha Banda Para Sempre 0,00 + Home Studio 520,00.
   - Conclusão: Barbara deve contar como pessoa ativa/pagante uma vez.

2. Correto: Arthur Souza Del Bosco explica a queda operacional 475→474 e 565→564 no relatório status-based pós-saneamento.
   - Arthur não está no CSV ativo.
   - Está no CSV ex-alunos e nos prints como interrompido em 09/01/2026.
   - Antes estava `status='ativo'` no LA Report; saneamento corrigiu para `inativo`.

3. Correto: a função por data e a view por status divergem:
   - função/data pós-saneamento: 500 ativos / 474 pagantes / 567 matrículas / 43 banda.
   - view/status pós-saneamento: 498 ativos / 474 pagantes / 564 matrículas / 41 banda.
   - Diferença função vs view em ativos: Alan 1375 e Leamsi 1393 (`status='inativo'`, `data_saida=NULL`, projetos/banda).

## Problemas críticos na resposta do Cascade

### 1) Plínio não deve ser automaticamente incluído
Cascade trata Plínio da Silva Bezerra Neto id 1361 como “único curso ativo” e diz que deveria contar.

Mas evidências contra:
- CSV ativo Emusys export_39: Plínio **não aparece**.
- CSV ex-alunos anterior: Plínio aparece como Canto interrompido em 02/05/2026.
- LA Report tem duas linhas contraditórias:
  - id 1052: Canto, Regular/pagante, `status='evadido'`, `data_saida='2026-05-02'`.
  - id 1361: Canto, Segundo Curso/pagante, `status='ativo'`, `data_saida=NULL`.

Conclusão: Plínio é provável sujeira/duplicidade de ciclo de vida, não prova de regra por pessoa. Não pode ser usado para aumentar pagantes.

### 2) Carlos Eduardo está sendo contado como pagante falso
Cascade diz que Carlos Eduardo Garcia do Nascimento não é pagante, mas a query por pessoa conta ele como pagante porque `tipo_matricula='Segundo Curso'` tem `conta_como_pagante=true`.

Evidências:
- LA Report:
  - id 1066: Contrabaixo, Bolsista Integral, não pagante.
  - id 1067: Canto, Segundo Curso, `valor_parcela=0`, `conta_como_pagante=true`.
- CSV ativo Emusys: Carlos Eduardo tem Canto/Contrabaixo/Minha Banda, mensalidade exibida `0,00`.

Conclusão: o cálculo `bool_or(conta_como_pagante=true)` está amplo demais se a linha tem `valor_parcela=0`/bolsa real. Carlos explica parte do `476` inflado.

### 3) 476 pagantes é inflado
A diferença entre row-based status pagantes (474) e pessoa-based pagantes (476) é nominalmente:
- Plínio da Silva Bezerra Neto — provável sujeira; não aparece no CSV ativo e consta como interrompido.
- Carlos Eduardo Garcia do Nascimento — mensalidade 0,00; não deveria virar pagante só por `tipo_matricula=Segundo Curso`.

Logo, `476` não deve ser aceito como target.

### 4) Adicionar `status IN ('ativo','trancado')` na função histórica é perigoso
Cascade propõe adicionar `status` ao snapshot de `recalcular_dados_mensais`.

Isso conflita com a regra já validada: `dados_mensais` é snapshot histórico; `status` atual não é histórico confiável. Para histórico, a base deve ser `data_matricula/data_saida` após saneamento, não `status` atual.

Se for relatório live/status-based, status faz sentido. Se for `dados_mensais` histórico/backfill, não pode virar regra cega.

### 5) Agrupar por `nome` é aceitável para auditoria, perigoso para migration
Para READ-ONLY pode ser usado como aproximação. Para função/migration, precisa de `pessoa_id`/chave canônica ou auditoria de homônimos/normalização, senão há risco de juntar pessoas diferentes ou separar a mesma pessoa por variação de nome.

## Números revisados pós-saneamento

Camadas atuais:

| Camada | Ativos | Pagantes | Matrículas | Banda | Observação |
|---|---:|---:|---:|---:|---|
| Relatório ADM antes do saneamento | 499 | 475 | 565 | 41 | Incluía Arthur indevidamente |
| View/status pós-saneamento | 498 | 474 | 564 | 41 | Arthur removido |
| Função/data pós-saneamento | 500 | 474 | 567 | 43 | Inclui Alan/Leamsi por `data_saida=NULL` apesar de inativos |
| Pessoa/status+data Cascade | 499 | 476 | 564 | 41 | Inflado por Plínio/Carlos |
| CSV Emusys ativo | 499 | não reproduz direto | 569 ocorrências | 45 projetos | Não traz regra de pagante LA Report |

## Próximo prompt recomendado para Cascade

Pedir nova auditoria READ-ONLY, não migration, focada em corrigir os falsos positivos:
- Plínio;
- Carlos Eduardo;
- alunos com `Segundo Curso` + `valor_parcela=0`;
- alunos ativos no LA Report ausentes do CSV ativo;
- alunos ativos no CSV ausentes/nomes divergentes no LA Report;
- diferença `564/41` vs CSV `569/45`.

## Bloqueio mantido

Não gerar/aplicar migration de `recalcular_dados_mensais` ainda.
