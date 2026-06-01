# Validação visual — Arthur Souza Del Bosco

Data: 2026-05-31
Fonte: prints enviados pelo Alf do Emusys.

## Evidência visual

Aluno: Arthur Souza Del Bosco.

Na aba Cursos/Matrícula:
- Curso: Bateria — Módulo 1.
- Status exibido: Interrompido.
- Contrato selecionado: Abr/2025 a Nov/2025.
- Turma: Bateria T, sábado 12:00–12:50, Sala 8 Bateria.
- Professor: Gabriel Barbosa Rufino Otávio.
- Não há mais aulas agendadas.
- 0 parcelas, 0 pagas, 0 vencidas, 0% presença no contrato selecionado.

Na aba Histórico/Registros:
- Registro em 09/01/2026 às 15:19 por Gabriela Leal:
  - “Matrícula finalizada por Gabriela Leal”
  - “Bateria - Dificuldade Financeira”
  - Observação: “O aluno havia sido retirado do sistema em Fevereiro/2025 mas devido a uma instabilidade no sistema do Emusys voltou a ser contabilizado nos números. Como havia sido contabilizado anteriormente, não será considerado para os cálculos”
  - Data da última aula: 29/11/2025.

## Conclusão

A evidência visual confirma que Arthur id 47 não deve contar como ativo/pagante em Maio/2026.

O saneamento aplicado no LA Report está correto para Arthur:
- `status='inativo'`
- manter `data_saida='2026-01-09'`

## Impacto na reconciliação

Arthur explica a diferença de 1 pagante entre o relatório antigo/status-based e a base saneada:
- 475 → 474.

A segunda diferença discutida (Barbara id 49) não é resolvida por esses prints; Barbara foi corrigida pelo Alf como aluna ativa em produção musical e não deve ser excluída cegamente por `is_projeto_banda=true`.
