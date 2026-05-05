# Operacional Pessoal — Skill de Briefings e Fechamento

## O que é

Esta skill define a trilha operacional pessoal do Alf, separada do CEO Quest.

Objetivo:
- abrir o dia com agenda real
- mostrar contas do dia
- revisar a semana de forma prática
- cobrar o que ficou aberto no dia anterior
- fechar o dia com visão operacional clara

## Regra-mãe

O operacional pessoal **não é jogo**.

Ele consulta o TickTick real para responder:
- o que tem hoje
- o que venceu
- o que ficou sem baixa
- o que precisa reagendar

Nunca misturar com:
- streak
- performance CEO
- pendência viva do jogo
- narrativa gamificada

## Janelas oficiais

### 7h — Briefing operacional pessoal
Entregar:
- compromissos de hoje
- contas de hoje
- visão curta da semana
- agenda real

### 7h30 — Pendências do dia anterior
Entregar:
- contas vencidas
- compromissos/ações sem baixa
- itens que precisam reagendamento

### 19h30 — Fechamento operacional pessoal
Entregar:
- o que foi concluído
- o que ficou aberto
- o que precisa reagendar

## Fonte única

TickTick real via API oficial.

Listas principais:
- Contas Pessoais — `67158c51db647de6536f46dc`
- Pessoal Alf — `643c0518525047536b6594d0`
- Trabalho Operacional — `643c0518525047536b6594d1`
- Mentorias — `67fbc6398f08b12415f506c4`

## Regras críticas

1. Não responder por memória.
2. Não inferir compromisso sem ler TickTick.
3. Não misturar com CEO Quest.
4. Se consulta falhar, dizer que falhou.
5. Entregar mensagem limpa, sem prefixo técnico.
6. Se não houver itens numa seção, dizer isso explicitamente.
7. Ao criar novo compromisso a partir de print/áudio, checar conflito antes.
8. Deduplicar itens semanticamente idênticos no briefing e nas pendências.
9. A resposta final deve conter apenas o texto que o Alf deve receber, sem cabeçalho operacional escondido.

## Regra de captura de compromisso

Quando o Alf manda print, áudio ou trecho de conversa:
- não sair criando compromisso automaticamente se houver ambiguidade
- pedir clarificação mínima se faltar:
  - assunto do compromisso
  - duração estimada
  - confirmação de que é para agendar
- antes de criar, checar conflito de agenda no TickTick

## Regra de conflito

Antes de qualquer novo compromisso:
- olhar o que já existe no horário
- verificar colisão direta
- verificar se a duração estimada invade outro compromisso
- se houver dúvida, perguntar antes de gravar
