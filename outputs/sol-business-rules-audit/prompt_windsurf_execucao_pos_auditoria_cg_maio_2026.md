Cascade, acabou a fase de auditoria exploratória. Agora precisamos transformar o que foi validado em regra técnica, views corretas e base para a Sol auditar inconsistências automaticamente.

IMPORTANTE:
- Não aplicar UPDATE em dados.
- Não rodar RPC.
- Não executar backfill.
- Não rodar Barra/Recreio.
- Não hardcodar nomes de alunos em regra de produção.
- Gerar patch/migration e SQLs de validação para revisão do Alfredo/Alf antes de aplicar em produção.

Contexto final validado — Campo Grande / Maio 2026 após limpeza manual do Alf:

- alunos ativos: 496
- alunos pagantes: 470
- matrículas ativas: 561
- matrículas banda/projeto: 41
- segundo curso operacional: 27
- coral: 0
- novas matrículas: 23
- evasões: 13
- churn: 2,77%

Correção importante sobre segundo curso:
- A view bruta chegou a mostrar 65 linhas com `is_segundo_curso=true`.
- Esse número está bruto e mistura banda/projeto.
- Desses 65, 38 são banda/projeto.
- O número operacional correto do card é:
  `matriculas_2_curso = is_segundo_curso=true AND is_projeto_banda=false`
  Resultado esperado: 27.
- Banda/projeto deve ficar somente em `matriculas_banda`, esperado: 41.

O que foi descoberto na auditoria:

1. Bruna Damasceno
- Havia duplicidade por variação de nome/cadastro.
- Linha zerada removida/corrigida.
- Restou uma Bruna pagante real.

2. Carlos Eduardo Garcia do Nascimento
- Permuta/parceria.
- Bolsista integral nos dois cursos.
- Não pagante.

3. Miguel Gomes Biancamano
- Professor/bolsista integral.
- Não pagante.

4. Matheus Reis da Silva Gaspar
- Estagiário/bolsista integral.
- Não pagante.

5. Marcos da Silva Saturnino
- Professor bolsista integral.
- Não frequenta mais as aulas.
- Foi colocado como inativo.

Pendências reais de auditoria, não regras definitivas:

1. Ana Clara Lima Santos Pinto
- Faz aula.
- LA Report está com valor zerado/nulo.
- Gabi removeu/moveu faturas.
- Precisa auditoria de faturas.

2. Anna Clara de Souza Iorio Sales
- Caso semelhante à Ana Clara.
- Valor zerado/nulo e faturas removidas/movidas.
- Precisa auditoria de faturas.

3. Sofia Elaile da Silva Campos
- Aluna nova de Violino.
- Matriculada em abril.
- Pagou passaporte.
- Começa/paga primeira mensalidade em junho.
- Não tratar como erro simples de pagante zero.

4. Sofia Lauermann Silva
- Aluna nova de Canto.
- Pagou passaporte.
- Começa/paga primeira mensalidade em junho.
- Não tratar como erro simples de pagante zero.

Regras de negócio para implementar/alinhar:

1. Métricas de pessoa:
- `alunos_ativos` é métrica por pessoa/aluno, não por matrícula bruta.
- `alunos_pagantes` é métrica por pessoa/aluno, não por matrícula bruta.
- Como ainda não há `pessoa_id` confiável, usar uma chave provisória documentada:
  `COALESCE(NULLIF(emusys_student_id,''), nome_normalizado, upper(trim(nome)))`
  e gerar alerta quando houver possível duplicidade por nome/telefone/Emusys.

2. Snapshot base de linhas válidas:
Usar como base:
- `status IN ('ativo','trancado')`
- `data_matricula <= fim_mes`
- `(data_saida IS NULL OR data_saida > fim_mes)`

Não usar apenas status.
Não usar apenas data.
Não usar `curso_id IS NOT NULL` como filtro global.
Não excluir banda/projeto dos KPIs de pessoa de forma cega.

3. `alunos_ativos`:
- contar pessoas distintas no snapshot base.
- incluir trancados.
- incluir aluno com banda/projeto quando for participação ativa.
- não duplicar por segundo curso.

4. `alunos_pagantes`:
- contar pessoas distintas no snapshot base que tenham pelo menos uma linha com `tipos_matricula.conta_como_pagante=true`.
- Bolsista integral, bolsista parcial, não pagante, professor/estagiário/permuta não devem contar.
- Não usar `valor_parcela > 0` como única regra global, porque aluno novo/passaporte/fatura movida pode ficar com valor nulo mesmo tendo contrato/fluxo válido.
- `valor_parcela > 0` deve ser usado como alerta/auditoria financeira, não como única fonte de verdade do KPI de pagantes contratuais.

5. `matriculas_ativas`:
- métrica de linha/matrícula.
- contar todas as linhas do snapshot base.
- esperado CG/Mai: 561.

6. `matriculas_banda`:
- métrica de linha.
- `cursos.is_projeto_banda=true`.
- esperado CG/Mai: 41.

7. `matriculas_2_curso`:
- métrica de linha.
- `is_segundo_curso=true AND COALESCE(cursos.is_projeto_banda,false)=false`.
- esperado CG/Mai: 27.
- Não usar o bruto `is_segundo_curso=true`, porque isso dá 65 e mistura banda/projeto.

8. `dados_mensais` / `recalcular_dados_mensais`:
- Preservar assinatura:
  `recalcular_dados_mensais(p_ano integer, p_mes integer, p_unidade_id uuid)`
- Preservar `SECURITY DEFINER`.
- Não tentar inserir/atualizar colunas geradas (`faturamento_estimado`, `saldo_liquido`).
- Alinhar a função com as mesmas regras acima.
- Não executar a função ainda. Só gerar migration/patch para revisão.

9. `vw_kpis_gestao_mensal`:
- Alinhar a view com as mesmas regras acima.
- A view deve expor o número operacional correto de segundo curso: 27, não 65 bruto.
- Se for necessário manter o número bruto, criar coluna separada claramente nomeada, por exemplo `total_segundo_curso_bruto`, mas o card deve usar `total_segundo_curso_operacional`.

10. Camada de auditoria para Sol:
Criar proposta de view/SQL read-only para inconsistências, sem alterar dados, com alertas nominais como:
- aluno ativo/pagante com `valor_parcela IS NULL OR valor_parcela=0`;
- aluno com passaporte pago e primeira mensalidade futura;
- aluno com faturas removidas/movidas;
- bolsista/professor/estagiário/permuta marcado como pagante;
- segundo curso zerado contaminando pessoa;
- duplicidade por nome similar/telefone/Emusys ID;
- curso divergente entre fontes;
- aluno ativo sem frequência/pagamento real;
- aluno inativo sem `data_saida` ou com lifecycle inconsistente.

Se a tabela de faturas/competência do Emusys ainda não existir no banco, documentar isso como dependência estrutural e propor a tabela/carga necessária. A Sol precisa de faturas por competência para diferenciar:
- ativo operacional;
- pagante contratual;
- pagante financeiro da competência;
- bolsista/permutado;
- sujeira operacional.

Entregáveis esperados:

1. Migration/patch SQL para corrigir `vw_kpis_gestao_mensal` e `recalcular_dados_mensais`, sem executar.
2. SQL de validação read-only com resultado esperado para CG/Mai:
   - ativos = 496
   - pagantes = 470
   - matrículas = 561
   - banda = 41
   - segundo curso operacional = 27
   - novas = 23
   - evasões = 13
3. Relatório técnico explicando as regras implementadas.
4. SQL/view de auditoria da Sol para inconsistências nominais.
5. Lista de riscos/pendências antes de rodar backfill.

Não aplicar no banco ainda. Primeiro entregar para auditoria do Alfredo/Alf.
