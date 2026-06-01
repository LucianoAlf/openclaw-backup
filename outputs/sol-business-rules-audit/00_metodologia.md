# Metodologia — Skill de Regras de Negócio da Sol / LA Report

Objetivo: extrair, validar e versionar as regras de negócio reais da LA Music usadas pela Sol, evitando cálculo bruto direto do banco.

## Princípio
Nenhuma regra vira “canônica” só porque apareceu no código ou no banco. Ela passa por 4 níveis:

1. **Encontrada** — apareceu em doc, SQL, view, RPC, frontend ou edge function.
2. **Cruzada** — a mesma regra foi localizada em pelo menos duas fontes, ou em uma fonte executável confiável.
3. **Validada pelo Alf** — regra de negócio confirmada explicitamente.
4. **Canônica** — entra na skill/segundo cérebro e passa a orientar a Sol.

## Fontes por prioridade
1. Confirmação do Alf.
2. SQL/RPC/view em produção no Supabase.
3. Edge functions e hooks que processam dados reais.
4. Documentação interna `.claude/memory/*.md` e `docs/*.md`.
5. Frontend, cards e componentes.
6. Dados brutos do banco, apenas como evidência, nunca como regra final.

## Artefatos da auditoria
- `supabase_inventory.md` — inventário do banco via OpenAPI/PostgREST.
- `sql_objects_from_repo.md` — views/funções/triggers encontradas nas migrations SQL.
- `repo_top_arquivos_regras.md` — arquivos do repo com maior densidade de termos de regra.
- `repo_regra_hits.tsv` — índice bruto de ocorrências para rastreabilidade.
- `regras_candidatas_v0.md` — regras extraídas, ainda com status.
- `duvidas_para_alf_e_windsurf.md` — lacunas que precisam de validação.
- Futuro: `skills/sol-business-rules/SKILL.md` — skill enxuta com referência aos arquivos canônicos.

## Status de regra
- `[CANONICA]` confirmada e pronta para skill.
- `[CANDIDATA]` forte, mas ainda precisa validação.
- `[DIVERGENTE]` fontes discordam.
- `[DUVIDA]` não dá para confiar sem perguntar.

## Regra de ouro
Se a Sol não souber a regra, ela deve responder “não tenho regra validada para esse KPI ainda”, não calcular bruto e fingir certeza.
