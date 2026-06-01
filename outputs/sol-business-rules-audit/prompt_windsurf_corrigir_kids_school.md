```md
Vamos corrigir um bug específico no LA Report, sem mexer nos cards que já estão certos.

Contexto:
- Tela: Analytics > Gestão > Campo Grande > Maio/2026.
- Card Total Alunos Ativos = 499.
- Tooltip: “Total de alunos com status ativo, excluindo segundo curso. Inclui pagantes e bolsistas.”
- Alf validou que “Alunos Ativos” inclui trancados, mas exclui segundo curso.

Problema:
- Cards LA Music Kids e LA Music School mostram:
  - Kids = 214
  - School = 351
  - soma = 565
- Mas o total de alunos ativos é 499.
- Isso acontece porque Kids/School estão usando query direta em `alunos` com `status in ('ativo','trancado')`, mas SEM excluir `is_segundo_curso`.

Fonte encontrada:
- Arquivo: `src/components/GestaoMensal/TabGestao.tsx`
- Bloco perto da query `alunosAtivosQuery`:

```ts
let alunosAtivosQuery = supabase
  .from('alunos')
  .select('idade_atual, unidade_id')
  .in('status', ['ativo', 'trancado']);
```

Depois calcula:

```ts
const totalLaKids = alunosAtivosData?.filter(a => a.idade_atual !== null && a.idade_atual <= 11).length || 0;
const totalLaAdultos = alunosAtivosData?.filter(a => a.idade_atual !== null && a.idade_atual >= 12).length || 0;
```

Validação por query:
- Query atual retorna 565 linhas:
  - Kids 214
  - School 351
- Query corrigida excluindo segundo curso retorna 499 linhas:
  - Kids 204
  - School 295

Regra canônica validada pelo Alf:
- Kids/School neste card devem seguir a mesma base de Total Alunos Ativos.
- Ou seja: alunos com status ativo/trancado, excluindo segundo curso.
- Kids/School é classificação da base de alunos, não distribuição de matrículas.
- Matrículas ativas já têm card próprio: 565, incluindo primeiro curso, segundo curso, banda e coral.

Correção solicitada:
1. Ajustar a query de Kids/School em `TabGestao.tsx` para excluir segundo curso:

```ts
let alunosAtivosQuery = supabase
  .from('alunos')
  .select('idade_atual, classificacao, unidade_id, is_segundo_curso')
  .in('status', ['ativo', 'trancado'])
  .or('is_segundo_curso.is.null,is_segundo_curso.eq.false');
```

2. Preferencialmente calcular por `classificacao` se estiver confiável:
   - LAMK = Kids
   - EMLA = School
   ou manter idade se essa for a regra atual, mas deixar consistente com tooltip.

3. Garantir que percentuais usem o mesmo denominador:
   - `dados.total_la_kids / dados.total_alunos_ativos`
   - `dados.total_la_adultos / dados.total_alunos_ativos`
   Agora isso deve fechar perto de 100%.

4. Não alterar:
   - Total Alunos Ativos = 499
   - Alunos Pagantes = 475 / 479
   - Matrículas Ativas = 565
   - Banda = 41
   - Novas matrículas = 23
   - Evasões = 13

5. Após corrigir, informar:
   - arquivos alterados
   - diff resumido
   - valores esperados para Campo Grande Maio/2026
   - se há impacto em consolidado/Recreio/Barra
```
