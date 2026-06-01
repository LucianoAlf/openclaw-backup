# Teste vivo API Emusys — 2026-05-31

## Ambiente
- `.env` contém `EMUSYS_BASE_URL` e `EMUSYS_TOKEN`.
- Base detectada: `https://api.emusys.com.br/v1`.
- Token não foi exposto nem salvo neste relatório.

## Resultado do comando pedido
`GET $EMUSYS_BASE_URL/leads/`

Resultado:
- HTTP 400
- Corpo: `Endpoint inválido.`

Conclusão: `/leads/` não é endpoint válido nessa API. Pelos docs, leads ficam sob `/crm/...` e não há GET de listagem de leads documentado.

## Varredura read-only de endpoints
Endpoints que responderam como rota válida, mas com token rejeitado (`token invalido!`):
- `GET /crm/campos`
- `GET /professores`
- `GET /usuarios`
- `GET /disciplinas`
- `GET /instrumentos`
- `GET /crm/opcoes_como_conheceu`
- `GET /aulas?data_hora_inicial=...&data_hora_final=...&limite=1`
- `GET /cursos` (não apareceu no OpenAPI paths, mas a rota respondeu como existente antes de barrar token)

Endpoints testados que retornaram `Endpoint inválido`:
- `GET /crm/leads`
- `GET /leads/`
- `GET /alunos`
- `GET /alunos/`
- `GET /matriculas`
- `GET /matriculas/`
- `GET /contratos`
- `GET /turmas`
- `GET /financeiro`
- `GET /financeiro/pagamentos`
- `GET /pagamentos`
- `GET /recebimentos`
- `GET /frequencia`
- `GET /presencas`

## Diagnóstico
- Host/API alcançável.
- `.env` está carregando as variáveis.
- Token atual não autentica nos endpoints válidos.
- Próximo passo: confirmar no painel Emusys se a API está ativada e copiar o Token da Escola/API, não token de usuário/sessão.

## Mapa de capacidade esperado com token válido
- Alunos/matrículas: não há GET documentado; ciclo de matrícula aparece via webhooks (`matricula_nova`, `matricula_renovacao`, `matricula_trancamento`, `matricula_finalizacao`). Para histórico antigo, provável necessidade de CSV/export ou endpoint privado.
- Frequência/presença: `GET /aulas` por período deve trazer aulas com alunos/professores e campos de presença/horário de presença.
- Pagamentos/financeiro: nenhum endpoint REST encontrado. Webhook/Matricula traz valor/tipo_pagamento, mas não recebimentos/baixas/inadimplência.
- Cursos/turmas: `GET /disciplinas`, `GET /instrumentos`, possivelmente `GET /cursos`; `/turmas` não existe como GET simples.
