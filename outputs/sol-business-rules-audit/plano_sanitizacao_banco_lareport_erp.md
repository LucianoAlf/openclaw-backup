# Plano de Sanitização — LA Report / LA Organizer como ERP próprio

Data: 2026-05-31
Origem: decisão estratégica do Alf durante auditoria do domínio Renovações/Reajustes/Não Renovações.

## 1. Direção estratégica

O objetivo não é só corrigir KPI quebrado.

O objetivo maior é transformar a base atual — LA Report / LA Organizer / integrações com Emusys — em uma fundação confiável para um ERP próprio da LA Music, reduzindo dependência do Emusys e permitindo:

- sistema operacional próprio da escola;
- app do professor;
- agente Fábio integrado ao fluxo do professor;
- presença, conteúdo, rotina pedagógica e materiais conectados ao LA Journey;
- relatórios e KPIs sem mistura entre legado, lixo e dado vivo.

## 2. Princípio central

Não criar camadas infinitas para esconder sujeira.

Views novas podem ser usadas como patch seguro ou camada de compatibilidade temporária, mas o objetivo final é:

1. identificar fonte canônica;
2. migrar histórico útil;
3. isolar dado sujo;
4. aposentar tabelas obsoletas;
5. remover dependências antigas;
6. documentar regra canônica.

## 3. Regra de ouro para limpeza

Nada deve ser deletado diretamente em produção sem auditoria e confirmação explícita do Alf.

Mas também não devemos manter tabela lixo por medo indefinido.

Fluxo correto:

1. Inventário da tabela/view.
2. Mapa de dependências reais no repo, Supabase, edge functions, triggers, RPCs e frontend.
3. Classificação:
   - CANÔNICA: fonte viva de verdade.
   - HISTÓRICA ÚTIL: preservar/migrar.
   - LEGADO COM DEPENDÊNCIA: manter temporariamente até remover dependência.
   - LIXO/OBSOLETA: candidata a arquivar/remover.
   - DESCONHECIDA: não mexer até provar.
4. Snapshot/export antes de qualquer remoção.
5. Migration de preservação, se houver histórico útil.
6. Remoção ou renomeação controlada.
7. Validação funcional.
8. Registro em memória/regras.

## 4. Sobre views novas

Criar uma view específica pode ser aceitável quando:

- reduz risco imediato;
- não altera dados;
- estabiliza contrato do frontend;
- serve como camada temporária de compatibilidade.

Mas é ruim quando:

- cria uma terceira verdade;
- mascara tabela ruim sem plano de aposentadoria;
- deixa regras de negócio duplicadas;
- não tem owner/fonte canônica documentada.

Para o caso atual de retenção:

- Se o Windsurf estiver criando uma view nova, ela deve ser tratada como `camada de compatibilidade`, não como nova fonte canônica.
- A fonte canônica operacional continua sendo `movimentacoes_admin`, se validado pelo Alf.
- `renovacoes` deve sair dos KPIs live.
- `renovacoes` não deve ser deletada agora; precisa auditoria/migração histórica.

## 5. Domínio atual — Retenção

### Fonte canônica candidata

`movimentacoes_admin`

Tipos relevantes:

- `renovacao`
- `nao_renovacao`
- `evasao`
- `aviso_previo`
- `trancamento`

### Tabelas/views em auditoria

- `movimentacoes_admin` — candidata canônica operacional.
- `renovacoes` — legada/desatualizada para KPI, talvez útil para contratos/histórico.
- `movimentacoes` — legada/paralela; aparentemente obsoleta para Maio/2026.
- `dados_mensais` — snapshot histórico/fechamento, não live.
- `evasoes_v2` — histórico útil até 2026-02-24; não apagar sem reconciliação.
- `vw_kpis_gestao_mensal` — view de consumo analytics; precisa parar de usar `renovacoes` para retenção live.
- `vw_kpis_retencao_mensal` — precisa corrigir taxa e total de evasões.

## 6. Próximo ciclo de trabalho

### Fase 1 — Estabilizar KPI sem alterar dados

- Corrigir views/contratos de leitura para que Analytics pare de exibir número errado.
- Não deletar tabela.
- Não criar trigger de sync.
- Validar Maio/2026 por unidade.

### Fase 2 — Mapa de dependência profundo

Para cada tabela suspeita:

- onde é lida no frontend;
- onde é escrita;
- quais views usam;
- quais RPCs usam;
- quais edge functions usam;
- quais triggers/funções usam;
- volume de dados por mês/unidade;
- sobreposição com tabelas canônicas;
- lacunas de histórico.

### Fase 3 — Plano de migração/aposentadoria

Para cada tabela:

- manter como canônica;
- migrar histórico para canônica;
- congelar como arquivo histórico;
- renomear para `_legacy`;
- remover dependências;
- deletar só com aprovação explícita.

### Fase 4 — Documentar regra canônica

Só depois:

- criar skill/base da Sol;
- criar mapa de fontes canônicas;
- documentar glossário de KPIs;
- travar boas práticas para Windsurf/Hugo não recriarem o problema.

## 7. Perguntas que precisam virar decisão

1. `movimentacoes_admin` vira oficialmente tabela canônica operacional de retenção?
2. `renovacoes` será preservada como histórico/contrato ou migrada e aposentada?
3. `dados_mensais` será apenas snapshot de fechamento?
4. Qual é o padrão para tabelas legadas: renomear `_legacy`, mover para schema `archive`, ou exportar e dropar?
5. O ERP próprio deve nascer sobre LA Organizer, LA Report, ou uma camada nova unificada?

## 8. Posição técnica inicial

A direção correta é parar de empilhar remendos e começar uma sanitização controlada.

O Hugo está certo em ter medo de deletar sem mapa de dependência.
O Alf está certo em não aceitar que medo vire acúmulo eterno de lixo.

A solução é um protocolo de desativação com evidência, snapshot e validação.
