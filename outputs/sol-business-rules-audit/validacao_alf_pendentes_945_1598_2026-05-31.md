# Validação Alf — pendentes 945 e 1598

Data: 2026-05-31
Contexto: saneamento de ciclo de vida Campo Grande / Maio 2026.

## Casos pendentes resolvidos pelo Alf

| ID LA Report | Nome | Validação Alf | Implicação |
|---:|---|---|---|
| 945 | Luciano da Silva Bernardino | Aluno excluído; não está matriculado; não está no LA Report/fluxo ativo | Não contar como ativo/pagante. Como no banco auditado apareceu `status='inativo'` com `data_saida=NULL`, precisa de saneamento de ciclo de vida para não entrar no snapshot por data. |
| 1598 | Alexandre Dos Santos | Mesmo caso; aluno excluído do Emusys e está como inativo no LA Report | Não contar como ativo/pagante. Como no banco auditado apareceu `status='inativo'` com `data_saida=NULL`, precisa de saneamento de ciclo de vida para não entrar no snapshot por data. |

## Recomendação técnica

Como os dois não aparecem no CSV de ativos nem no CSV de ex-alunos, não há data histórica exata no material recebido.

Opções:
1. Se Windsurf/Emusys encontrar data real de exclusão/saída, usar essa data.
2. Se não houver data, usar `2026-05-31` como **data técnica de saneamento de estoque Maio/2026**, sem criar `movimentacoes_admin` retroativa.

## Observação

Esse ajuste é de ciclo de vida/estoque, não de evento de evasão. Não deve alterar o contador de evasões de Maio sem evidência operacional.
