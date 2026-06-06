# Revisão Final Alfredo — P8/P11 Snapshot `dados_mensais`

> Status: revisão técnica da proposta v2  
> Decisão: **NÃO executar migration ainda**  
> Próxima etapa: **SELECT-only + ajustes finais na proposta**

---

## Veredito

A proposta v2 corrigiu os pontos principais da v1, mas **ainda não está aprovada para execução**.

A direção está correta:

- congelamento de snapshot;
- audit trail/versionamento mínimo antes de qualquer overwrite;
- frontend bloqueando ou alertando recálculo de mês congelado;
- descongelamento auditado com motivo obrigatório.

Mas ainda existem riscos técnicos que precisam ser corrigidos antes de qualquer migration, alteração de banco, RPC, view ou função.

---

## 1. Frontend referencia coluna que não existe

Na proposta v2, o frontend faz:

```ts
.select('congelado, congelado_em, congelado_por')
```

Mas a migration proposta só cria:

```sql
congelado BOOLEAN DEFAULT false,
congelado_em TIMESTAMPTZ
```

Ou seja: `congelado_por` não existe.

### Correção necessária

Escolher uma das opções:

### Opção A — criar a coluna

```sql
ALTER TABLE dados_mensais
  ADD COLUMN IF NOT EXISTS congelado_por UUID NULL;
```

E, se fizer sentido:

```sql
ALTER TABLE dados_mensais
  ADD COLUMN IF NOT EXISTS congelado_por_contexto TEXT DEFAULT 'unknown';
```

### Opção B — remover do frontend

Trocar:

```ts
.select('congelado, congelado_em, congelado_por')
```

Por:

```ts
.select('congelado, congelado_em')
```

### Recomendação Alfredo

Criar `congelado_por` e `congelado_por_contexto`, porque congelar snapshot também é uma ação sensível e precisa rastreabilidade.

---

## 2. `congelar_snapshot` também precisa audit trail

A proposta v2 auditou o descongelamento, mas o congelamento ainda faz apenas:

```sql
UPDATE dados_mensais
SET congelado = true, congelado_em = NOW()
```

Isso é insuficiente.

Congelar um mês também é uma decisão operacional importante. Precisa registrar:

- quem congelou;
- quando congelou;
- contexto da execução;
- motivo/operação.

### Correção necessária

Antes de congelar, registrar evento no histórico ou em tabela de auditoria.

Exemplo conceitual:

```sql
INSERT INTO dados_mensais_historico (
  original_id,
  unidade_id,
  ano,
  mes,
  versao,
  alunos_ativos,
  alunos_pagantes,
  matriculas_ativas,
  matriculas_banda,
  matriculas_2_curso,
  novas_matriculas,
  evasoes,
  churn_rate,
  ticket_medio,
  tempo_permanencia,
  taxa_renovacao,
  inadimplencia,
  reajuste_parcelas,
  copiado_em,
  copiado_por,
  copiado_por_contexto,
  motivo
)
SELECT
  id,
  unidade_id,
  ano,
  mes,
  COALESCE((
    SELECT MAX(versao) + 1
    FROM dados_mensais_historico h
    WHERE h.unidade_id = dados_mensais.unidade_id
      AND h.ano = dados_mensais.ano
      AND h.mes = dados_mensais.mes
  ), 1),
  alunos_ativos,
  alunos_pagantes,
  matriculas_ativas,
  matriculas_banda,
  matriculas_2_curso,
  novas_matriculas,
  evasoes,
  churn_rate,
  ticket_medio,
  tempo_permanencia,
  taxa_renovacao,
  inadimplencia,
  reajuste_parcelas,
  NOW(),
  auth.uid(),
  CASE
    WHEN auth.uid() IS NOT NULL THEN 'auth_user'
    WHEN current_user = 'service_role' THEN 'service_role'
    WHEN current_setting('application_name', true) LIKE '%cron%' THEN 'cron'
    ELSE 'unknown'
  END,
  'CONGELAMENTO'
FROM dados_mensais
WHERE ano = p_ano
  AND mes = p_mes
  AND (p_unidade_id IS NULL OR unidade_id = p_unidade_id);
```

Depois disso, fazer o `UPDATE` de congelamento.

---

## 3. Funções `SECURITY DEFINER` precisam `search_path`

A proposta cria funções com:

```sql
LANGUAGE plpgsql
SECURITY DEFINER
```

Mas não define `search_path`.

Isso é risco clássico em PostgreSQL: função `SECURITY DEFINER` sem `search_path` fixo pode ser vulnerável a resolução indevida de objetos.

### Correção necessária

Adicionar em todas as funções `SECURITY DEFINER`:

```sql
SET search_path = public;
```

Exemplo:

```sql
CREATE OR REPLACE FUNCTION public.congelar_snapshot(...)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  ...
END;
$$;
```

Aplicar em:

- `recalcular_dados_mensais`
- `congelar_snapshot`
- `descongelar_snapshot`
- qualquer futura função de restore/rollback

---

## 4. RLS/permissões dependem de confirmação real da estrutura

A proposta sugere políticas usando:

```sql
perfis_usuario
usuario_id
unidade_id
perfil = 'admin'
```

Mas isso precisa ser confirmado antes.

Não dá para assumir que a tabela, colunas e papéis existem exatamente assim.

### SELECT-only necessário

Antes de escrever RLS definitivo, rodar:

```sql
SELECT
  table_name,
  column_name,
  data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('perfis_usuario', 'usuarios', 'profiles', 'user_profiles')
ORDER BY table_name, ordinal_position;
```

E também:

```sql
SELECT
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;
```

### Correção necessária

Só propor RLS final depois de confirmar:

- nome real da tabela de perfis;
- coluna real de usuário;
- coluna real de unidade;
- como o sistema identifica admin;
- se gestor de unidade existe como papel;
- se service role vai executar cron/funções.

---

## 5. SELECT-only precisa ser executado antes da migration

A proposta v2 ainda está baseada em inferência documental.

Antes de qualquer execução, rodar e revisar os SELECTs para confirmar:

- se `dados_mensais` é tabela;
- constraints reais;
- generated columns reais;
- definição real de `recalcular_dados_mensais`;
- se `snapshot_dados_mensais` ainda existe;
- se cron legado ainda existe/está ativo;
- se abril/maio existem em `dados_mensais`;
- se há duplicidade por `(unidade_id, ano, mes)`;
- tamanho da tabela;
- estrutura real de permissões/perfis;
- chamadas frontend para recálculo.

---

## 6. Ajustes finais exigidos na proposta v3

A próxima versão da proposta deve corrigir:

1. `congelado_por` inexistente no frontend/schema;
2. audit trail também no `congelar_snapshot`;
3. `SET search_path = public` em todas as funções `SECURITY DEFINER`;
4. RLS/permissões só após SELECT-only da estrutura real;
5. confirmar generated columns antes de decidir copiar ou não copiar `faturamento_estimado` e `saldo_liquido`;
6. manter auto-congelamento como opcional, sem ativar cron;
7. manter restore/backfill como proposta futura, sem execução automática.

---

## 7. Status por item

| Item | Status |
|---|---|
| Canônico documental | Quase aprovado |
| SELECT-only P8/P11 | Aprovado para rodar |
| Migration v2 | Não aprovada para execução |
| Congelamento | Direção aprovada, implementação precisa ajuste |
| Audit trail | Direção aprovada, precisa cobrir congelamento também |
| Descongelamento auditado | Boa direção |
| Frontend | Precisa corrigir coluna inexistente |
| RLS/permissões | Precisa SELECT-only antes |
| Cron automático dia 5 | Ainda não aprovado |

---

## 8. Próxima entrega esperada

Entregar somente:

1. resultado dos SELECTs P8/P11;
2. proposta migration v3 corrigida;
3. diff técnico da v2 para v3;
4. política de permissões baseada na estrutura real;
5. plano de execução em staging antes de produção.

---

## 9. Proibido nesta etapa

- Não executar migration.
- Não alterar banco.
- Não alterar view/RPC.
- Não rodar backfill.
- Não executar `CREATE OR REPLACE FUNCTION`.
- Não executar `CREATE TABLE`.
- Não executar `ALTER TABLE`.
- Não executar `UPDATE`, `DELETE`, `INSERT`.
- Não ativar cron.
- Não mexer em produção.

A próxima etapa continua sendo:

**SELECT-only + proposta v3 revisada.**

---

## Mensagem curta para o Cascade/Windsurf

V2 melhorou, mas ainda não executar.

Corrigir antes:

1. frontend referencia `congelado_por`, mas a coluna não existe;
2. `congelar_snapshot` precisa audit trail igual ao descongelamento;
3. funções `SECURITY DEFINER` precisam `SET search_path = public`;
4. RLS depende de confirmar estrutura real de `perfis_usuario`/perfis via SELECT-only;
5. manter auto-congelamento como opcional, sem ativar cron.

Próxima etapa segue SELECT-only. Migration só depois desses ajustes e resultados revisados.
