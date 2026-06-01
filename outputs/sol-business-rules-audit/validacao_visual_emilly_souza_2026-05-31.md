# Validação visual — Emilly Souza de Oliveira

Data: 2026-05-31
Origem: prints enviados pelo Alf no Telegram

## Identificação

- Nome na tela do Emusys: **Emilly Souza De Oliveira**
- LA Report: id **106**
- Curso exibido: **Canto**
- Status exibido no Emusys: **Interrompido**
- Nível: **Aluno Iniciante 1**
- Contrato exibido: **Fev/2025 a Fev/2026**
- Plano: **Anual**
- Parcelas: **11 parcelas de R$ 387,00; 11 pagas; 0 vencidas**
- Presença: **84%**
- Turma exibida: **Canto T**, sábado 09:00 às 09:50, Sala 6 Kids
- Professor exibido: **Gabriel Santos Teixeira da Silva**

## Conclusão

O print confirma que Emilly Souza de Oliveira é **ex-aluna/interrompida** no Emusys.

Havia divergência de data:
- CSV Emusys ex-alunos: `Interrompido em 2026-03-05`
- LA Report / movimentações_admin previamente observado: evasão em `2026-03-07`

**Decisão do Alf:** a data correta é **2026-03-05**.

Para o snapshot de Maio/2026, a diferença não altera o resultado: Emilly deve estar fora do estoque de ativos. Para saneamento histórico fino, usar 2026-03-05 como data efetiva de saída.

## Recomendação

- Preencher `alunos.data_saida` para id 106 com `2026-03-05`.
- Não criar nova movimentação retroativa duplicada.
