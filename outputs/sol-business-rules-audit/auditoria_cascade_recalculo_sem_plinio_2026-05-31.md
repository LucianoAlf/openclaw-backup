# Auditoria Alfredo — Cascade recalculado sem Plínio

Data: 2026-05-31
Fonte: screenshot Cascade após validação visual do Plínio.

## Resumo Cascade

- Plínio removido como caso de negócio.
- Cascade reconheceu que Plínio era sujeira de ciclo de vida: contrato Canto interrompido no Emusys; linha id 1361 ficou ativa por falha de sincronização da evasão de 02/05.
- Números corrigidos:
  - Ativos: 498 vs ADM 499
  - Pagantes: 475 vs ADM 475
  - Matrículas: 563 vs ADM 565
- Cascade aponta Carlos Eduardo Garcia do Nascimento como caso real de diferença row-by-row vs pessoa:
  - id 1066: Contrabaixo, Bolsista Integral, não pagante
  - id 1067: Canto, Segundo Curso, valor_parcela=0, conta_como_pagante=true
  - Por pessoa, `bool_or(conta_como_pagante)` faz Carlos contar como pagante.

## Veredito Alfredo

Não aprovar migration/regra final ainda.

O número 475 voltou a bater, mas por composição diferente da ADM original:
- ADM antes do saneamento contava Arthur e não contava Carlos pela regra row-by-row.
- Cascade pós-saneamento remove Arthur e adiciona Carlos por pessoa.

Portanto, “bate 475” não significa que a regra está correta. Pode ser troca de pessoas.

## Blocker Carlos Eduardo

Carlos tem `valor_parcela=0` e CSV Emusys mostra mensalidade 0,00. A linha `Segundo Curso` tem `conta_como_pagante=true`, mas isso pode ser falso positivo de tipo de matrícula.

Antes de contar Carlos como pagante, precisa validação operacional:
- Carlos paga alguma mensalidade real?
- O segundo curso dele é pago ou bolsista/zero?
- `conta_como_pagante=true` deve valer mesmo com `valor_parcela=0`?

## Blocker ativos/matrículas

Ativos 498 vs ADM 499 e matrículas 563 vs ADM 565 não podem ficar como “provável cache”. Precisam de reconciliação nominal:
- Quem saiu da lista original ADM para a lista saneada?
- Quem entrou?
- Qual a razão de cada diferença: Arthur, Plínio, Carlos ou outro?

## Próximo pedido correto ao Cascade

Pedir ledger nominal antes/depois:
1. conjunto original ADM/status-based antes do saneamento;
2. conjunto pós-saneamento row-by-row;
3. conjunto por pessoa proposto;
4. diff nominal com motivo de cada inclusão/exclusão.

Não gerar migration ainda.
