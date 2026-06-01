# Validação visual — Plínio da Silva Bezerra Neto

Data: 2026-05-31
Fonte: prints enviados pelo Alf.

## Evidência visual

No LA Report:
- Aluno: Plínio da Silva Bezerra Neto.
- Curso: Canto.
- Valor: R$ 345.
- Há uma linha/indicação marcada como **2º curso**.
- A linha principal aparece como **evadido**.
- A linha expandida/2º curso aparece como **ativo**.

Na tela de curso/contrato:
- Canto Módulo 1 aparece como **Interrompido**.
- Contrato Jan/2026 a Abr/2026.
- Sem aulas agendadas.
- 0 parcelas exibidas no contrato selecionado.

## Conclusão

A evidência reforça que Plínio não deve ser usado automaticamente para inflar `alunos_ativos`/`alunos_pagantes` por regra de pessoa.

Ele está marcado como 2º curso no LA Report e, ao mesmo tempo, a matrícula/contrato aparece interrompida. Isso parece sujeira/duplicidade de ciclo de vida:
- linha regular/primária evadida/interrompida;
- linha 2º curso ainda ativa indevidamente.

## Implicação para Cascade/Windsurf

A auditoria por pessoa do Cascade errou ao tratar Plínio como prova de que “segundo curso único ativo deve contar”. No caso específico, Plínio precisa ser saneado/reconciliado nominalmente, não contado como pagante.
