# Skill completa — sol-la-report-business-rules

Estrutura esperada:

```txt
skills/sol-la-report-business-rules/
├── SKILL.md
└── references/
    ├── regras-canonicas.md
    ├── pendencias-bloqueadores.md
    ├── p8-p11-snapshot.md
    └── checklist-sql-seguro.md
```

---

## Arquivo: SKILL.md

```md
---
name: sol-la-report-business-rules
description: "Use obrigatoriamente ao trabalhar no LA Music Performance Report/Sol: KPIs, regras de negócio, SQL, RPCs, views, dashboard, funil comercial, professores, alunos, evasão, MRR, ticket, inadimplência, Kids/School, dados_mensais ou snapshot. Impõe regras canônicas validadas pelo Alf, separa legado de bug e bloqueia alterações perigosas sem SELECT-only e aprovação."
---

# Sol — Regras de Negócio LA Report

Esta skill é a fonte operacional da Sol para regras de negócio do **LA Music Performance Report**.

Use antes de:

- escrever SQL/RPC/view/migration;
- calcular KPIs;
- alterar dashboard/frontend;
- responder sobre métricas;
- auditar divergências;
- propor correções em `dados_mensais`, `vw_kpis_gestao_mensal`, evasões, ticket, MRR, inadimplência ou funil.

---

## Regra de autoridade

Quando houver conflito:

1. **Regra validada pelo Alf** vence.
2. `references/regras-canonicas.md` é a fonte canônica atual.
3. Banco real deve ser verificado com **SELECT-only**.
4. Código atual é evidência, não verdade absoluta.
5. Documento antigo divergente vira **legado**.
6. Código divergente vira **possível bug**.

Nunca transforme sujeira de banco, fallback antigo ou comportamento legado em regra oficial.

---

## Travas de segurança

Sem aprovação explícita do Alf, é proibido:

- executar migration;
- executar `ALTER`, `CREATE`, `DROP`, `UPDATE`, `DELETE`, `INSERT`;
- rodar backfill;
- criar/substituir view ou RPC;
- ativar cron;
- mexer em produção;
- apagar dados;
- arquivar aluno com `DELETE FROM alunos`.

Quando a tarefa envolver banco, primeiro gerar/rodar apenas **SELECT-only** e revisar resultados.

---

## Referências obrigatórias

Leia conforme a tarefa:

- `references/regras-canonicas.md` — regras validadas e status atual.
- `references/pendencias-bloqueadores.md` — pontos ainda não fechados.
- `references/p8-p11-snapshot.md` — `dados_mensais`, congelamento, audit trail, SELECT-only.
- `references/checklist-sql-seguro.md` — checklist antes de qualquer SQL/migration.

Para qualquer alteração que afete métrica, consulte primeiro `regras-canonicas.md`.

Para `dados_mensais`, snapshot, cron, fechamento mensal ou histórico, consulte primeiro `p8-p11-snapshot.md`.

---

## Decisões já validadas pelo Alf

Resumo rápido:

- Churn: `evasoes / alunos_pagantes * 100`.
- Inadimplência: `% cabeças = qtd_inadimplentes / alunos_pagantes * 100`.
- Ticket médio: por pessoa, `MRR / COUNT(DISTINCT pagantes)`.
- Canto Coral: usar `cursos.is_coral`; filtro por nome é legado.
- Bolsista parcial: não conta como pagante e não entra no ticket médio.
- Passaporte: não entra no MRR; é receita à parte.
- Conversão professor: só experimentais realizadas pelo professor contam; matrícula sem experimental não entra.
- LTV: `ticket_medio * tempo_permanencia_meses`.
- Kids/School: `idade_atual <= 11` LAMK; `idade_atual >= 12` EMLA.

---

## Pendências abertas

Ainda não fechar como canônico final sem nova validação:

- P8/P11 `dados_mensais`: SELECT-only liberado; migration v3 aprovada só como desenho técnico; produção travada.
- Taxa de renovação: confirmar se `aviso_previo` entra no denominador.
- Taxa de conversão geral do funil: `novas / total_leads` vs `novas / leads_com_exp`.

---

## Comportamento esperado da Sol

Quando encontrar divergência:

1. classificar como `validada`, `inferida`, `pendente` ou `legado/bug`;
2. apontar evidência;
3. propor SELECT-only se precisar validar;
4. não corrigir automaticamente;
5. pedir aprovação antes de qualquer alteração destrutiva ou produtiva.

Frase-guia:

> Documento antigo divergente = legado. Código divergente = possível bug. Regra validada pelo Alf = canônica.
```

---

## Arquivo: references/regras-canonicas.md

```md
# Regras Canônicas — LA Music Performance Report

## Status

Este arquivo resume as regras validadas para Sol e outros agentes.

Classificação:

- ✅ Validada pelo Alf
- 📋 Inferida do código atual
- ❓ Pendente de validação
- 🚫 Legado / não usar / possível bug

---

## Pessoa, matrícula e alunos

- 📋 `alunos` armazena matrículas, não pessoas.
- 📋 Identidade operacional: `LOWER(TRIM(nome)) + unidade_id`.
- 📋 Nome sozinho pode colidir; dois nomes iguais na mesma unidade exigem checagem humana.
- 📋 Segundo curso = matrícula adicional de outro curso.
- 📋 Mesmo `curso_id` duplicado para a mesma pessoa = duplicata, não segundo curso.

### Total alunos ativos

- 📋 Base = pessoas, não matrículas.
- 📋 Inclui `ativo` + `trancado`.
- 📋 Exclui `is_segundo_curso = true`.
- 🚫 `COUNT(*)` para ativos/pagantes é possível bug.

### Matrículas ativas

- 📋 Base = registros.
- 📋 Inclui primeiro curso, segundo curso, banda e coral.

---

## Pagantes, MRR e ticket

### Pagantes

Excluem:

- bolsista integral;
- bolsista parcial;
- não pagante;
- segundo curso no card de pagantes, para não duplicar pessoa;
- banda/projeto;
- coral;
- valor de parcela zero.

✅ Bolsista parcial não conta como pagante e não entra no ticket médio.

### Ticket médio

✅ Ticket médio canônico: por pessoa.

```sql
MRR / COUNT(DISTINCT pagantes)
```

### MRR

✅ Passaporte não entra no MRR.  
MRR = recorrência de parcelas/mensalidades.  
Passaporte = receita à parte.

---

## Evasão, churn e renovação

### Evasão

- 📋 Evasão = `evasao` + `nao_renovacao` em `movimentacoes_admin`.
- 📋 Aviso prévio não é evasão.
- 📋 Trancamento não é evasão.
- 🚫 Não usar `evasoes_v2` como fonte viva.

### Churn

✅ Fórmula canônica:

```sql
evasoes / alunos_pagantes * 100
```

### Taxa de renovação

❓ Ainda pendente:

- código atual: `renovacoes / (renovacoes + nao_renovacoes)`;
- possível canônico: `renovacoes / (renovacoes + nao_renovacoes + aviso_previo)`.

Não alterar sem validação do Alf.

---

## Kids / School

✅ Fonte canônica: `idade_atual`.

- LAMK/Kids: `idade_atual <= 11`.
- EMLA/School: `idade_atual >= 12`.

❓ Qualquer uso de `classificacao` textual deve ser tratado como possível fonte desatualizada até alinhamento.

---

## Canto coral e banda

### Banda

- 📋 Canônico operacional: `cursos.is_projeto_banda = true`.
- 🚫 Filtros por nome como `ILIKE '%banda%'` ou `ILIKE '%power kids%'` são legado temporário.

### Canto Coral

✅ Regra validada: criar/usar `cursos.is_coral`.

🚫 Filtro por nome (`ILIKE '%canto coral%'`) é legado frágil e deve ser substituído.

---

## Aulas experimentais e funil

- 📋 A experimental conta quando é realizada, não quando é agendada.
- 📋 `experimentais_realizadas`: status `experimental_realizada` ou `matriculado`.
- 📋 `experimentais_agendadas`: inclui `experimental_agendada`, `experimental_realizada`, `matriculado`.
- ❓ Banco usando `data_contato` em vez de `data_experimental_realizada` é pendência/possível bug.

### Conversão geral do funil

❓ Pendente:

- `novas / total_leads`; ou
- `novas / leads_com_exp`.

Não fechar sem validação.

---

## Professores

### Carteira professor

- 📋 Conta alunos com `professor_atual_id` e `status = 'ativo'`.
- 📋 Inclui segundo curso como matrícula.
- 📋 Não inclui banda.
- 📋 Não inclui `trancado`.

### Conversão professor

✅ Fórmula canônica:

```sql
matriculas_pos_experimental / experimentais_realizadas * 100
```

✅ Apenas matrículas originadas de experimental realizada por aquele professor entram no numerador.

🚫 Cálculo que permite taxa >100% por matrícula sem experimental é bug/legado.

---

## LTV / permanência

✅ Fórmula LTV:

```sql
ticket_medio * tempo_permanencia_meses
```

📋 Regra “saiu de tudo”: só conta quando aluno encerra todas as matrículas.

📋 Excluir passagens menores que 4 meses.

---

## Arquivamento

📋 Arquivamento técnico: mover para `alunos_arquivados` e remover de `alunos`.

🚫 Ação destrutiva. Nunca executar sem autorização explícita do Alf.
```

---

## Arquivo: references/pendencias-bloqueadores.md

```md
# Pendências e Bloqueadores — LA Report / Sol

## Bloqueadores atuais

### P8/P11 — Snapshot `dados_mensais`

Status:

- ✅ Migration v3 aprovada como desenho técnico.
- ✅ SELECT-only liberado.
- 🚫 Produção travada.

Proibido ainda:

- migration;
- ALTER/CREATE/UPDATE/DELETE/INSERT;
- backfill;
- cron;
- produção.

Próximo passo: rodar `verificacao-p8-p11-select-only.md`, revisar resultado e só depois decidir staging/migration.

---

## Pendências de regra

### Taxa de renovação

❓ Confirmar se `aviso_previo` entra no denominador.

Não tratar como regra fechada.

### Taxa de conversão geral do funil

❓ Confirmar denominador:

- `novas / total_leads`; ou
- `novas / leads_com_exp`.

Não alterar dashboard/funil sem validação.

---

## Pendências técnicas importantes

- Padronizar `cursos.is_coral` e remover filtro por nome.
- Padronizar Kids/School por `idade_atual` onde hoje usa `classificacao`.
- Corrigir fonte de data de experimental para data realizada, não `data_contato`.
- Remover `evasoes_v2` como fonte viva.
- Corrigir qualquer `COUNT(*)` usado para alunos ativos/pagantes quando deveria ser pessoa.
```

---

## Arquivo: references/p8-p11-snapshot.md

```md
# P8/P11 — Snapshot `dados_mensais`

## Status

- ✅ Decisão de negócio: histórico mensal deve ser preservado.
- ✅ Recalcular mês passado não pode sobrescrever sem audit trail.
- ✅ Não executar backfill automático.
- ✅ Migration v3 aprovada como desenho técnico.
- ✅ SELECT-only liberado.
- 🚫 Produção travada até revisão dos resultados e aprovação final.

---

## Problema

`dados_mensais` permite UPSERT por `(unidade_id, ano, mes)`.  
Recalcular um mês passado pode alterar retroativamente o histórico.

O Alf relatou perda/alteração de abril.

---

## Direção aprovada

Implementar, futuramente e só após aprovação:

1. congelamento de snapshot;
2. audit trail/versionamento mínimo antes de overwrite;
3. descongelamento auditado com motivo;
4. frontend bloqueando ou alertando recálculo de mês congelado.

---

## Migration v3

Aprovada apenas como desenho técnico.

Ainda depende de:

- resultado dos SELECTs;
- confirmação da estrutura real;
- confirmação de RLS/perfis;
- definição de meses a congelar;
- staging antes de produção.

---

## SELECT-only obrigatório

Antes de qualquer execução, confirmar:

- `dados_mensais` é tabela ou view;
- colunas reais;
- constraints/índices;
- generated columns;
- definição real de `recalcular_dados_mensais`;
- existência de `snapshot_dados_mensais`;
- cron ativo/inativo;
- dados de abril/maio;
- duplicidades por `(unidade_id, ano, mes)`;
- tamanho da tabela;
- estrutura real de perfis/RLS;
- chamadas frontend de recálculo.

---

## Proibições

Até aprovação final:

- não executar migration;
- não alterar banco;
- não criar tabela;
- não alterar função;
- não ativar cron;
- não executar backfill;
- não mexer em produção.
```

---

## Arquivo: references/checklist-sql-seguro.md

```md
# Checklist SQL Seguro — LA Report / Sol

Antes de qualquer SQL:

## 1. Classificar a ação

- SELECT-only?
- Documental?
- Frontend fallback?
- View/RPC/function?
- Migration?
- Backfill?
- Produção?

Se não for SELECT-only/documental, precisa aprovação explícita.

---

## 2. Verificar fonte da regra

- A regra foi validada pelo Alf?
- Está em `regras-canonicas.md`?
- É inferência do código?
- É documento antigo?
- É comportamento legado?

Documento antigo divergente = legado.  
Código divergente = possível bug.

---

## 3. Para métricas de alunos

Checar:

- pessoa vs matrícula;
- `COUNT(DISTINCT nome)` vs `COUNT(*)`;
- segundo curso;
- banda/projeto;
- coral;
- bolsistas;
- valor zero;
- passaporte;
- unidade.

---

## 4. Para evasões/churn

Checar:

- usar `movimentacoes_admin`;
- incluir `evasao` + `nao_renovacao`;
- excluir aviso prévio;
- excluir trancamento;
- deduplicar por pessoa/unidade/mês;
- não usar `evasoes_v2` como fonte viva.

---

## 5. Para financeiro

Checar:

- MRR não inclui passaporte;
- ticket médio é por pessoa;
- inadimplência é percentual de pessoas/cabeças;
- bolsista parcial não entra em pagantes/ticket;
- `sem_parcela` tratado corretamente.

---

## 6. Para produção

Antes de qualquer execução real:

- SELECT-only rodado;
- resultados revisados;
- diff gerado;
- staging testado;
- rollback planejado;
- aprovação explícita do Alf.

Sem isso, não executar.
```
