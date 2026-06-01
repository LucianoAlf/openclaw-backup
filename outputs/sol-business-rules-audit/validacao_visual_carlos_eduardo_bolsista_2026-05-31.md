# Validação visual — Carlos Eduardo Garcia do Nascimento

Data: 2026-05-31
Fonte: prints enviados pelo Alf.

## Evidência visual

Carlos Eduardo Garcia do Nascimento aparece como aluno ativo/em andamento, mas com indicação clara de bolsista/não pagante.

Dados visíveis:
- Marcadores: Veterano e Bolsista.
- Contrabaixo — Módulo 1:
  - status ativo/em andamento;
  - professor Marcos Saturnino;
  - quinta 20:00;
  - parcela exibida como “-”.
- Canto — Módulo 1:
  - aparece como 2º curso;
  - status ativo;
  - professor Daiana Anjos;
  - sábado 09:00;
  - parcela R$ 0.
- Minha Banda Para Sempre:
  - em andamento;
  - 0 parcelas de R$ 0,00;
  - 0 pagas, 0 vencidas;
  - professor Alan Samico;
  - sábado 09:00.

## Conclusão

Carlos Eduardo é aluno ativo, mas bolsista/não pagante. O Cascade estava confundindo “Segundo Curso” com “segundo curso pago”.

A linha 1067 (`tipo_matricula=Segundo Curso`, `conta_como_pagante=true`, `valor_parcela=0`) não deve transformá-lo em pagante. O valor operacional é zero e o print confirma tag Bolsista.

## Implicação

Carlos Eduardo não pode explicar 474→475 como pagante real. Ele deve contar como ativo, mas não como pagante.
