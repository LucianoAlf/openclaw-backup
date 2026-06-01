Não aplique ainda. A lógica de negócio está quase aprovada, mas a migration v2 tem dois blockers técnicos.

BLOCKER 1 — assinatura da função mudou.

A função atual no banco é:

```sql
recalcular_dados_mensais(p_ano integer, p_mes integer, p_unidade_id uuid)
```

A migration v2 criou:

```sql
recalcular_dados_mensais(p_unidade_id uuid, p_ano integer, p_mes integer)
```

Isso não substitui corretamente a função atual; cria uma sobrecarga diferente. Como o frontend chama:

```ts
supabase.rpc('recalcular_dados_mensais', {
  p_ano: ano,
  p_mes: mes,
  p_unidade_id: unidade
})
```

pode ficar ambíguo ou continuar usando a função antiga.

Corrija mantendo a assinatura original:

```sql
CREATE OR REPLACE FUNCTION public.recalcular_dados_mensais(
  p_ano integer,
  p_mes integer,
  p_unidade_id uuid
)
```

BLOCKER 2 — SECURITY DEFINER sumiu.

A função atual é `SECURITY DEFINER`. A migration v2 não tem isso.

Corrija para manter:

```sql
LANGUAGE plpgsql
SECURITY DEFINER
```

Pode adicionar também:

```sql
SET search_path = public
```

se isso não quebrar o padrão do projeto.

Pontos aprovados da lógica:
- novas_matriculas com filtros canônicos
- churn com base atual
- taxa_renovacao via movimentacoes_admin
- reajuste_parcelas via valor_parcela_anterior / valor_parcela_novo
- não gravar faturamento_estimado nem saldo_liquido porque são GENERATED ALWAYS

Ressalva não bloqueante:
- ticket_medio ainda pode divergir da view live porque a função exclui segundo curso, enquanto a view agrupa por aluno/pessoa e soma parcelas. Não precisa resolver nesta migration, mas registrar para próxima auditoria.

Depois de corrigir esses dois blockers, mande a migration revisada para nova aprovação. Não aplicar ainda.
