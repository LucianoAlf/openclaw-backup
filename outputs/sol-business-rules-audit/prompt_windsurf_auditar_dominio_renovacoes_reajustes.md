```md
Pausa na correção do Reajuste Médio. Antes de aplicar patch, vamos auditar o domínio inteiro de Renovações/Reajustes/Não Renovações para não criar remendo em produção.

IMPORTANTE:
- LA Report está em produção.
- Não alterar nada ainda.
- Não aplicar patch SQL ainda.
- Objetivo: mapear fonte canônica e risco antes de corrigir.

## Contexto
Já confirmamos que o card Reajuste Médio está errado:
- Frontend usa `dados.reajuste_pct` em `TabGestao.tsx`.
- Para mês atual vem de `vw_kpis_gestao_mensal.reajuste_medio`.
- A view calcula por `renovacoes.percentual_reajuste`.
- `renovacoes.percentual_reajuste` está nulo/0.
- `movimentacoes_admin` tem os valores operacionais reais de reajuste.

Mas não quero corrigir só `reajuste_medio` antes de entender o domínio, porque a mesma CTE/mesma área pode impactar:
- renovações realizadas;
- contratos/renovações totais;
- taxa de renovação;
- não renovações;
- relatórios administrativos;
- Programa Fideliza/score se usar a mesma fonte.

## Regra já validada pelo Alf — Reajuste Médio
- Considerar somente renovações com aumento positivo.
- Reajuste 0 não entra.
- Registro sem `valor_parcela_anterior` ou `valor_parcela_novo` não entra.
- Fonte operacional candidata: `movimentacoes_admin` com `tipo='renovacao'`.

Valores esperados Maio/2026 pelo cálculo operacional:
- Campo Grande: 12,95%
- Recreio: 10,41%
- Barra: 8,70%

## O que investigar agora

### 1. Mapear todas as fontes do domínio
Investigue e responda para cada tabela:

#### `renovacoes`
- Quem escreve nela? Frontend? trigger? função? sync?
- Quais telas usam?
- Quais views usam?
- Qual o propósito original: operacional vivo, histórico, agenda de contratos, ou legado?
- Por que Campo Grande/Maio tem 61 renovadas enquanto `movimentacoes_admin` tem 38?
- Esses 61 incluem duplicidade, contratos futuros, importação, registros sem valores ou outro conceito?

#### `movimentacoes_admin`
- Quem escreve nela?
- Quais telas usam?
- Quais views usam?
- Ela é hoje a fonte operacional real para renovação/evasão/não renovação?
- Ela tem todos os campos necessários para regra canônica?

#### `dados_mensais`
- Confirmar que é snapshot/histórico/fechamento, não fonte viva do mês corrente.
- Quais telas ainda usam `dados_mensais` mesmo no mês atual?

### 2. Mapear views/RPCs envolvidas
Inspecionar definição real em produção de:
- `vw_kpis_gestao_mensal`
- `vw_kpis_retencao_mensal`
- qualquer view/RPC que calcule taxa de renovação, renovações, não renovações, reajuste médio, churn, evasões.

Para cada uma, responder:
- Fonte usada para renovações.
- Fonte usada para não renovações.
- Fonte usada para reajuste.
- Fonte usada para taxa de renovação.
- Se usa `renovacoes`, `movimentacoes_admin`, `evasoes_v2`, `dados_mensais` ou mistura.

### 3. Mapear frontend/telas envolvidas
Buscar no repo usos de:
- `renovacoes`
- `movimentacoes_admin`
- `reajuste_medio`
- `percentual_reajuste`
- `taxa_renovacao`
- `renovacoes_realizadas`
- `nao_renovacoes`

Responder quais telas/card dependem disso, especialmente:
- Analytics > Gestão (`TabGestao.tsx`)
- Retenção/Planilha
- Professores/Retenção
- Administrativo/Programa Fideliza
- Dashboard/Snapshot/Relatórios WhatsApp

### 4. Comparar números de Maio/2026 por unidade
Para Campo Grande, Recreio e Barra, montar tabela comparativa:

- `renovacoes`:
  - total linhas
  - status renovado
  - não renovado/se houver
  - com percentual positivo
  - média positiva

- `movimentacoes_admin`:
  - tipo renovacao
  - tipo nao_renovacao
  - reajustes positivos
  - média positiva

- views atuais:
  - `vw_kpis_gestao_mensal.renovacoes`
  - `vw_kpis_gestao_mensal.taxa_renovacao`
  - `vw_kpis_gestao_mensal.reajuste_medio`
  - `vw_kpis_retencao_mensal.renovacoes_realizadas`
  - `vw_kpis_retencao_mensal.nao_renovacoes`
  - `vw_kpis_retencao_mensal.taxa_renovacao`

### 5. Diagnóstico arquitetural
Responder claramente:
1. Qual tabela deveria ser fonte canônica viva para renovações/reajustes/não renovações?
2. `renovacoes` deve ser corrigida/sincronizada ou aposentada como fonte de KPI?
3. `movimentacoes_admin` deve virar fonte canônica da retenção operacional?
4. Há risco de corrigir só `reajuste_medio` e deixar `renovacoes/taxa_renovacao` inconsistentes?
5. Qual correção mínima coerente resolve o domínio sem refatorar o sistema inteiro?

## Saída esperada
Antes de qualquer correção, enviar:
- mapa de fontes;
- lista de arquivos/telas impactadas;
- lista de views/RPCs impactadas;
- tabela comparativa por unidade;
- recomendação de arquitetura;
- plano de correção em etapas, separando:
  1. patch seguro imediato;
  2. correção estrutural;
  3. limpeza/legado futura.

## Regra de segurança
Não aplicar SQL, migration ou alteração de frontend ainda.
Só investigar e recomendar.
```
