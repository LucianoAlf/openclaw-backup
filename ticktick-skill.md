# Skill Interna — TickTick (Alfredo)

## Objetivo
Padronizar como o Alfredo cria, atualiza e organiza itens no TickTick do Alf.

Essa skill é interna de operação do Alfredo.
Não é para o usuário ver como framework.
É uma regra prática para evitar bagunça, item no Inbox sem necessidade e classificação errada.

---

## Regra principal
# Nunca jogar no Inbox por comodidade se houver uma lista clara para o item.

Antes de criar qualquer item no TickTick, classificar na lista correta.
O Inbox só é aceitável quando realmente não existir categoria adequada ou quando o contexto ainda estiver ambíguo.

---

## Listas padrão do Alf

### 💡 Mentorias
Usar para:
- mentorias do Alf
- reuniões com mentorados
- preparação, follow-up e compromissos ligados a mentorias
- materiais, ajustes e pendências diretamente vinculados a mentorados

### 💼 Trabalho Alf
Usar para:
- tarefas gerais de trabalho
- atividades ligadas à LA Music, sistemas, equipe, reuniões internas, projetos, follow-ups operacionais
- qualquer item profissional que não pertença melhor a uma lista mais específica

### 🏠 Pessoal Alf
Usar para:
- compromissos e tarefas pessoais
- lembretes da vida cotidiana
- assuntos de casa, saúde, família, rotina e organização pessoal

### 💸 Contas Pessoais
Usar para:
- contas a pagar
- boletos
- cartões
- vencimentos financeiros pessoais
- qualquer item cujo foco principal seja pagamento ou obrigação financeira pessoal

### 📝 Notas Alf
Usar para:
- registros soltos
- ideias
- referências
- anotações que não são tarefa nem compromisso

---

## Regra de classificação
Ao receber um pedido do Alf, pensar nesta ordem:

### 1. É mentoria?
Se sim → **💡 Mentorias**

### 2. É conta ou pagamento pessoal?
Se sim → **💸 Contas Pessoais**

### 3. É compromisso/tarefa pessoal?
Se sim → **🏠 Pessoal Alf**

### 4. É trabalho geral?
Se sim → **💼 Trabalho Alf**

### 5. É só nota/referência/rascunho?
Se sim → **📝 Notas Alf**

### 6. Ainda está ambíguo?
Só nesse caso aceitar Inbox temporariamente — e idealmente corrigir depois.

---

## Regras operacionais

### Compromissos com data e hora
- Sempre criar com data/hora corretas
- Sempre respeitar timezone `America/Sao_Paulo`
- Sempre incluir lembretes quando o Alf pedir ou quando for claramente útil

### Quando houver categoria óbvia
- Criar direto na lista certa
- Não criar no Inbox para “mover depois”

### Quando errar a lista
- Corrigir imediatamente
- Se a API não mover corretamente, criar na lista certa e apagar o item errado

### Quando o item também existir no TOM/LA Organizer
- Isso não elimina a necessidade de classificar certo no TickTick
- TOM e TickTick podem coexistir, mas o TickTick precisa continuar organizado pelas listas do Alf

---

## Casos canônicos

### Mentoria com Levi
- tipo: compromisso de mentoria
- lista correta: **💡 Mentorias**

### Conta do Cartão C6
- tipo: conta pessoal
- lista correta: **💸 Contas Pessoais**

### Ligar para fornecedor da LA Music
- tipo: trabalho
- lista correta: **💼 Trabalho Alf**

### Comprar algo para casa
- tipo: pessoal
- lista correta: **🏠 Pessoal Alf**

### Ideia solta sobre conteúdo ou sistema
- tipo: nota
- lista correta: **📝 Notas Alf**

---

## Veto
- Não deixar item profissional em lista pessoal
- Não deixar mentoria no Inbox se já estiver clara
- Não usar Inbox como padrão preguiçoso
- Não assumir que “depois eu organizo” é aceitável
- Não confundir TOM/LA Organizer com a organização do TickTick

---

## Resultado esperado
O TickTick do Alf deve ficar:
- fácil de consultar
- coerente com as categorias reais da vida dele
- sem compromissos importantes perdidos no Inbox
- com mentorias, pessoal, contas e trabalho bem separados

Se houver dúvida, o Alfredo decide pela melhor lista possível na origem.
Se errar, corrige na hora.