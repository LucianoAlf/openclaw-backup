# Auditoria — Migration recalcular_dados_mensais v2

Data: 2026-05-31
Arquivo auditado: `/root/.openclaw/media/inbound/Migration_recalcular_dados_mensais-v2---9ee2289f-d7b7-4558-a854-251cd36ff77f.sql`

## Veredito

Não aplicar ainda.

A lógica de negócio principal está quase correta, mas a migration tem blockers técnicos.

## Blocker 1 — assinatura da função mudou

Função atual no banco:

```sql
recalcular_dados_mensais(p_ano integer, p_mes integer, p_unidade_id uuid)
```

Migration v2 cria:

```sql
recalcular_dados_mensais(p_unidade_id uuid, p_ano integer, p_mes integer)
```

Em PostgreSQL, a identidade da função considera os tipos e a ordem dos argumentos. Portanto isso não substitui com segurança a função atual; cria uma sobrecarga diferente.

Risco:

- a função antiga continua existindo;
- PostgREST/Supabase RPC pode ficar ambíguo, porque o frontend chama por nomes:

```ts
supabase.rpc('recalcular_dados_mensais', {
  p_ano: ano,
  p_mes: mes,
  p_unidade_id: unidade
})
```

- pode gerar erro de função ambígua ou continuar chamando a versão antiga.

Correção obrigatória:

```sql
CREATE OR REPLACE FUNCTION public.recalcular_dados_mensais(
  p_ano integer,
  p_mes integer,
  p_unidade_id uuid
)
```

Manter a assinatura original.

## Blocker 2 — SECURITY DEFINER sumiu

Função atual no banco é:

```sql
LANGUAGE plpgsql
SECURITY DEFINER
```

Migration v2 está:

```sql
LANGUAGE plpgsql
AS $$
```

Sem `SECURITY DEFINER`.

Risco:

- a RPC pode perder permissão dependendo do usuário/session role;
- mesmo que compile, o botão de recalcular no frontend pode quebrar.

Correção obrigatória:

```sql
LANGUAGE plpgsql
SECURITY DEFINER
```

Ideal também definir `SET search_path = public`, mas pelo menos manter o comportamento atual.

## Pontos aprovados

Ajustes de regra estão corretos:

- `novas_matriculas` exclui segundo curso, banda/projeto, coral e bolsistas.
- `churn_rate` usa base atual (`v_evasoes / v_alunos_pagantes`).
- `taxa_renovacao` usa `movimentacoes_admin`: renovação / (renovação + não renovação).
- `reajuste_parcelas` usa colunas reais `valor_parcela_anterior` e `valor_parcela_novo`.
- Não tenta gravar `faturamento_estimado` nem `saldo_liquido`, que são `GENERATED ALWAYS`.

## Ressalva não bloqueante — ticket médio

A função atual/v2 calcula ticket médio excluindo segundo curso:

```sql
COALESCE(a.is_segundo_curso, false) = false
```

Já a view live `vw_kpis_gestao_mensal` calcula ticket por pessoa somando parcelas do aluno agrupado, o que pode incluir segundo curso no valor total do aluno.

Isso não foi introduzido pela v2, mas deve entrar na próxima auditoria de consistência entre snapshot e live.

## Prompt recomendado ao Windsurf

Não aplicar ainda. Corrigir migration mantendo assinatura e SECURITY DEFINER.
