# Sol — Sync contrato, checklist e canais para VPS

Data: 2026-05-29 UTC
Host: `lahq`
Workspace remoto: `/home/sol/.openclaw/workspace`

## Backup remoto criado

- `/home/sol/.openclaw/workspace/backups/alfredo-sync-20260529T000813Z`

## Arquivos sincronizados

- `/home/sol/.openclaw/workspace/REGRAS_CONTRATUAIS.md`
- `/home/sol/.openclaw/workspace/CANAIS_E_INSTANCIAS.md`
- `/home/sol/.openclaw/workspace/templates/checklist-administrativo-contratual-whatsapp.md`

## Skills sincronizadas

Diretório remoto:

- `/home/sol/.openclaw/workspace/skills/`

Skills enviadas:

- `sol-atendimento`
- `sol-cobranca`
- `sol-frequencia`
- `sol-sucesso-aluno`
- `sol-bi-admin`
- `sol-comunidades-whatsapp`
- `sol-human-takeover`
- `_registry.md`

## Canais/instâncias configurados em documentação

- Sol Atendimento — `(21) 3955-4415`
- Sol Sucesso do Aluno — `(21) 2342-5316`

Regra central:

- mesma Sol;
- mesmo tom;
- mesmas bases;
- intenções diferentes por canal;
- visibilidade separada entre atendimento operacional e sucesso do aluno.

## Restart e verificação

Gateway reiniciado manualmente na VPS.

Healthcheck OK:

```json
{"ok":true,"status":"live"}
```

Skills verificadas como ready:

- `sol-atendimento`
- `sol-human-takeover`
- `sol-sucesso-aluno`

## Smoke tests

### Smoke 1 — canais

Prompt:

> Quais são as duas instâncias/canais da Sol, seus números e a diferença entre Atendimento e Sucesso do Aluno?

Resposta validada:

- Sol Atendimento — `(21) 3955-4415`
- Sol Sucesso do Aluno — `(21) 2342-5316`
- Atendimento resolve operação; Sucesso cuida da jornada e risco de saída.

### Smoke 2 — reposição por viagem sem linguagem jurídica

Prompt:

> Um responsável pede reposição porque viajou. Como você responde em linguagem próxima, sem falar “pelo contrato”?

Resposta validada:

> “Entendi 😊
>
> Nesse caso, como foi viagem, vou encaminhar para a equipe da unidade verificar direitinho a possibilidade de reposição e disponibilidade de horário, tá?
>
> Me confirma, por favor, o nome do aluno e a data da aula perdida?”

Resultado: PASS.

## Observação

Nenhuma automação nova foi ativada. O sync colocou conhecimento, regras, templates e skills no workspace/runtime da Sol.

O próximo passo recomendado é revisar fluxo real de envio do checklist pós-matrícula e decidir se começa em dry-run ou envio assistido por humano.
