# Auditoria Alfredo — Windsurf v3 saneamento ciclo de vida CG/Maio

Data: 2026-05-31
Arquivos auditados:
- `SIMULACAO_SANEAMENTO_CG---4d44bcc6-7785-4e0a-8d86-51c3a33aec95.sql`
- `UPDATES-COM-GUARDS_Campo_Grande_Maio_2026-V3---2a997d33-a6b5-4d57-ba8b-be919e92d934.sql`

## Veredito

**Não aprovar execução ainda.**

A regra de negócio foi corrigida, mas os arquivos v3 ainda têm dois problemas técnicos objetivos:

1. A seção 1 do SQL de simulação parece ter erro de sintaxe por parêntese faltando em `no_snapshot_virt`.
2. Os asserts do update estão implementados de forma errada: `GET DIAGNOSTICS ROW_COUNT` após vários `UPDATE`s só retorna a contagem do último `UPDATE`, não a soma do grupo.

## Pontos corrigidos na v3

- Removido `curso_id IS NOT NULL` como filtro global: correto.
- `curso_id NULL` virou alerta de qualidade, não exclusão automática: correto.
- Giovanna id 1619 preservada no snapshot: correto.
- Arthur id 47 mantém `data_saida='2026-01-09'` na lógica proposta: correto conceitualmente.
- Grupo D separado: Maria 1450 e Ana Julia 1378 com corte técnico; Alan/Leamsi sem update: correto.
- Números esperados agora batem conceitualmente:
  - antes: 515 / 485 / 582 / 45
  - após 28 correções: 500 / 474 / 567 / 43
  - após regra banda: 495 / 473 / 567 / 43

## Blocker 1 — provável erro de sintaxe na simulação

Na seção 1, campo `no_snapshot_virt`, existe um `AND (` aberto que não é fechado antes do `THEN`:

```sql
CASE WHEN a.data_matricula <= (SELECT dt FROM fim_mes)
      AND (
        ...
        OR (c.id IS NULL AND (...))
     THEN 'SIM' ELSE 'NÃO' END AS no_snapshot_virt
```

Precisa fechar a expressão:

```sql
        OR (c.id IS NULL AND (...))
      )
     THEN 'SIM' ELSE 'NÃO' END AS no_snapshot_virt
```

Se o arquivo inteiro for rodado como instruído, deve falhar nessa seção.

## Blocker 2 — asserts do update estão errados

Exemplo Grupo A:

```sql
UPDATE alunos ... id = 106;
UPDATE alunos ... id = 85;
...
UPDATE alunos ... id = 1377;

GET DIAGNOSTICS v_count = ROW_COUNT;
IF v_count != 16 THEN RAISE EXCEPTION ...
```

Em PL/pgSQL, `ROW_COUNT` retorna apenas linhas afetadas pelo **último comando SQL**. No Grupo A, isso deve retornar `1`, não `16`.

Consequência:
- Grupo A vai dar exception `esperado 16, obtido 1`.
- Como exception aborta o bloco, o saneamento inteiro não será aplicado.
- Isso é seguro, mas inviabiliza a execução.

O mesmo problema existe em:
- Grupo C: espera 5, mas pega só último update = 1.
- Grupo D: espera 2, mas pega só último update = 1.
- Grupo E: espera 2, mas pega só último update = 1.

## Verificação de guards no banco atual

Checagem read-only feita via REST: todos os guards esperados batem no estado atual.

- A: 16/16
- B: 1/1
- C: 5/5
- D: 2/2
- E: 2/2

Ou seja: o problema não é o dado atual; é a forma de contar updates dentro do DO block.

## Correção recomendada

Opção melhor: trocar vários updates individuais por `UPDATE ... FROM (VALUES ...) ... RETURNING` e contar o `RETURNING`.

Exemplo Grupo A:

```sql
WITH expected(id, nova_data_saida) AS (
  VALUES
    (106, DATE '2026-03-05'),
    (85,  DATE '2026-04-25'),
    ...
    (1377, DATE '2026-04-01')
), updated AS (
  UPDATE alunos a
  SET data_saida = e.nova_data_saida,
      updated_at = NOW()
  FROM expected e
  WHERE a.id = e.id
    AND a.unidade_id = v_unidade
    AND a.status = 'inativo'
    AND a.data_saida IS NULL
  RETURNING a.id
)
SELECT COUNT(*) INTO v_count FROM updated;

IF v_count != 16 THEN
  RAISE EXCEPTION 'GRUPO A: esperado 16 updates, obtido %', v_count;
END IF;
```

Para Grupo C, usar `VALUES(id, data_saida_esperada)`:

```sql
WITH expected(id, data_saida_esperada) AS (...), updated AS (...)
```

Alternativa menor: acumular manualmente após cada update:

```sql
v_count := 0;
UPDATE ...;
GET DIAGNOSTICS v_rows = ROW_COUNT;
v_count := v_count + v_rows;
...
```

Mas a opção com `VALUES + RETURNING` é mais limpa e menos propensa a erro.

## Prompt para Windsurf

```text
V3 corrigiu a regra de negócio, mas ainda não aprovar execução por dois problemas técnicos.

1) SIMULACAO: na seção 1, campo no_snapshot_virt, parece faltar fechar o parêntese do AND (...) antes do THEN. Rodar o arquivo inteiro deve dar erro de sintaxe. Corrigir.

2) UPDATE: os asserts estão errados. GET DIAGNOSTICS ROW_COUNT após vários UPDATEs retorna só o último UPDATE, não a soma do grupo.
Assim Grupo A vai retornar 1 e falhar contra esperado 16; Grupo C/D/E também falham.

Corrigir usando UPDATE ... FROM (VALUES ...) ... RETURNING e SELECT COUNT(*) INTO v_count FROM updated; ou acumular ROW_COUNT depois de cada update.

Preferência: usar VALUES + RETURNING por grupo:
- Grupo A: VALUES(id, nova_data_saida), guard unidade/status='inativo'/data_saida IS NULL, assert 16.
- Grupo B: update único, assert 1.
- Grupo C: VALUES(id, data_saida_esperada), guard unidade/status='ativo'/data_saida=data_saida_esperada, assert 5.
- Grupo D: VALUES(id), guard unidade/status='inativo'/data_saida IS NULL, set data_saida='2026-05-31', assert 2.
- Grupo E: VALUES(id), mesmo guard, assert 2.

Checagem read-only no banco atual confirmou que os guards esperados batem: A=16, B=1, C=5, D=2, E=2.

Não executar update/RPC/backfill. Gerar v4.
```
