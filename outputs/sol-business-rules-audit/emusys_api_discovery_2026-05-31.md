# Descoberta API Emusys — 2026-05-31

## Fonte
- Docs: https://emusys.gitbook.io/emusys/api-emusys
- OpenAPI extraído do GitBook/R2: versão 1.1.3
- Base URL: `https://api.emusys.com.br/v1`
- Auth: header `token`
- Rate limit informado: 60 req/min/IP, janela rolling.

## Conclusão principal
A documentação pública acessível **não expõe endpoint REST direto para consultar alunos/matrículas/contratos/status/histórico de aluno**.

O OpenAPI lista endpoints REST para CRM/leads, aulas, professores, usuários, disciplinas, instrumentos e opções auxiliares. Para ciclo de vida de matrícula, a documentação mostra **webhooks**, não consultas históricas.

## Endpoints REST encontrados
- `PATCH /crm/leads/por_telefone`
- `PATCH /crm/leads`
- `POST /crm/leads`
- `GET /crm/campos`
- `GET /professores`
- `GET /usuarios`
- `GET /disciplinas?tipo=`
- `GET /crm/aula_experimental/disponibilidade?data=&disciplina_id=&professor_id=`
- `POST /crm/aula_experimental`
- `GET /instrumentos`
- `POST /crm/leads/anotacao/por_telefone`
- `POST /crm/leads/anotacao`
- `GET /crm/opcoes_como_conheceu`
- `GET /aulas?data_hora_inicial=&data_hora_final=&cursor=&limite=`

## Webhooks úteis para LA Report / ciclo de vida
- `matricula_nova`
- `matricula_renovacao`
- `matricula_trancamento`
- `matricula_finalizacao`

### Payloads importantes
Objeto `Matricula` nos webhooks inclui:
- `matricula_id`
- `nome_aluno`
- `nome_responsavel`
- `data_nascimento_aluno`
- `email_aluno`, `telefone_aluno`
- `curso_id`, `nome_curso`, `nome_modulo`
- `data_primeira_aula`
- `data_ultima_aula`
- `data_matricula`
- `valor`
- `tipo_pagamento`
- `disciplinas[]` com professor, horários, primeira/última aula
- `usuario_realizou_matricula`

Webhook `matricula_finalizacao` traz:
- `finalizacao.data_ultima_aula`
- `finalizacao.motivo`
- `finalizacao.observacoes`
- `matricula`

Webhook `matricula_trancamento` traz:
- `trancamento.id`
- `trancamento.motivo`
- `trancamento.data_inicial`
- `trancamento.data_final`
- `matricula`

Webhook `matricula_renovacao` traz:
- `renovacao.data_ultima_aula`
- `matricula`

## Implicação para saneamento CG/Maio 2026
Para validar os 28 casos históricos, a API documentada provavelmente não basta se os webhooks não estavam configurados antes.

Possíveis usos:
1. Se o token permitir endpoints não documentados, testar descoberta controlada/read-only.
2. Usar `GET /aulas` de maio/2026 para verificar presença/agendamento dos 28 nomes — ajuda como evidência indireta, mas não substitui status/data_saida.
3. Melhor caminho para histórico: export CSV do Emusys com alunos/matrículas/finalizações/trancamentos/renovações, ou pedir ao suporte Emusys endpoint/relatório de matrículas.
4. Para o futuro: configurar webhooks Emusys → LA Report para capturar `matricula_nova`, `matricula_renovacao`, `matricula_trancamento`, `matricula_finalizacao` em uma tabela canônica de eventos.

## Cuidados
- Guardar token somente em `.env`, nunca em repo/memória.
- Não fazer writes no Emusys inicialmente; iniciar apenas com GETs/read-only.
- Respeitar 60 req/min; para importações usar paginação/cursor e intervalo se necessário.
