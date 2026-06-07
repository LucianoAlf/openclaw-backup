# LA Report — Correção mínima do Ticket Médio por Pessoa

## Objetivo

Corrigir **somente** o cálculo de `ticket_medio` na view `public.vw_kpis_gestao_mensal`.

Não alterar MRR, novas matrículas, churn, evasões, alunos ativos, alunos pagantes, matrículas, renovação ou qualquer outro KPI neste patch.

---

## Regra canônica validada pelo Alf

**Ticket médio = soma das parcelas recorrentes dos alunos pagantes por pessoa / quantidade de pessoas pagantes.**

Regras:

1. Aluno com múltiplos cursos conta como **1 pessoa** no denominador.
2. Segundo curso de aluno pagante entra no **numerador/faturamento**, mas não duplica a pessoa no denominador.
3. Bolsista integral e bolsista parcial ficam fora do numerador e do denominador.
4. Banda/projeto e coral ficam fora do ticket médio.
5. Parcela zero/nula fica fora do ticket médio.
6. Chave de pessoa: `LOWER(TRIM(nome)) + unidade_id`.
7. Não usar `AVG(valor_parcela)` por linha/matrícula como ticket médio.

Exemplo validado:

- Bateria: R$380
- Canto: R$355
- Teclado: R$367
- Harmonia: R$127

Total: R$1.229.

Esse aluno entra como **1 aluno pagante de R$1.229**, não como 4 linhas.

---

## Arquivos enviados

1. `patch-minimo-ticket-medio-por-pessoa.sql`
   - Migration proposta.
   - Altera apenas o CTE financeiro da view para calcular `ticket_medio` por pessoa.
   - Mantém `mrr` e `tempo_permanencia_medio` no mesmo padrão da view atual.

2. `validacao-ticket-medio-patch-minimo.sql`
   - SELECT-only.
   - Serve para validar que o novo ticket muda, mas MRR e demais KPIs permanecem iguais.

3. `resultado-validacao-ticket-medio-patch-minimo.json`
   - Resultado da validação SELECT-only já executada pelo Alfredo.

---

## Resultado da validação SELECT-only

Validação executada em 2026-06-06.

| Unidade | Ticket atual | Ticket novo | Diferença | MRR atual | MRR recalculado bloco atual | Diff MRR |
|---|---:|---:|---:|---:|---:|---:|
| Barra | 424,72 | 447,58 | +22,86 | 99.810,15 | 99.810,15 | 0,00 |
| Campo Grande | 369,55 | 387,15 | +17,60 | 170.734,23 | 170.734,23 | 0,00 |
| Recreio | 409,77 | 436,91 | +27,14 | 131.946,70 | 131.946,70 | 0,00 |

Também devem permanecer iguais na validação:

- `novas_matriculas`
- `total_alunos_pagantes`
- `total_alunos_ativos`
- `total_segundo_curso`
- `matriculas_ativas`
- `total_evasoes`
- `churn_rate`

---

## Patch frontend obrigatório separado

No arquivo:

`src/components/App/Alunos/ModalFichaAluno.tsx`

Trocar:

```ts
const tipoMatriculaId = cursoSelecionadoEhBanda ? 5 : 2;
```

Por:

```ts
const tipoMatriculaId = cursoSelecionadoEhBanda
  ? 5
  : ([3, 4].includes(formData.tipo_matricula_id)
    ? formData.tipo_matricula_id
    : 2);
```

Motivo:

- Banda/projeto → tipo 5.
- Bolsista integral/parcial → preservar 3/4.
- Pagante regular com segundo curso → tipo 2.

Não usar simplesmente `formData.tipo_matricula_id` para todos, porque aluno regular com segundo curso perderia a marcação de segundo curso.

---

## Travas

Não executar se qualquer uma destas acontecer:

1. `patch-minimo-ticket-medio-por-pessoa.sql` alterar MRR em relação à view atual.
2. `patch-minimo-ticket-medio-por-pessoa.sql` zerar ou alterar `novas_matriculas`.
3. Qualquer KPI além de `ticket_medio` mudar sem justificativa explícita.
4. Frontend continuar com `cursoSelecionadoEhBanda ? 5 : 2`.
5. Migration tentar excluir segundo curso do MRR.

---

## Ordem recomendada

1. Rodar `validacao-ticket-medio-patch-minimo.sql` no Supabase.
2. Confirmar que `diff_mrr_view_vs_bloco = 0` em todas as unidades.
3. Confirmar que `novas_matriculas` e demais KPIs permanecem iguais.
4. Aplicar patch do frontend.
5. Testar criação de segundo curso:
   - aluno bolsista parcial/integral deve preservar tipo 3/4;
   - aluno pagante regular deve virar tipo 2;
   - banda deve virar tipo 5.
6. Só então pedir aprovação explícita do Alf para aplicar a migration da view.

---

## Observação importante

Este patch não resolve a sujeira operacional de parcelas zeradas/nulas nem duplicatas do Recreio. Isso é outro fluxo/auditoria.

Este patch resolve apenas o bug matemático do ticket médio por linha em vez de por pessoa.
