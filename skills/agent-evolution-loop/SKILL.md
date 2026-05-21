---
name: agent-evolution-loop
description: Use quando o usuário falar de aprendizado do agente, sonhos/dreaming, feedback virando memória, evolução de comportamento, criação/ajuste de skills a partir de feedback recorrente, perfil comportamental/tom de usuário ou organização de memórias. Gatilhos: feedback, aprender, memória, sonho, dreaming, skill nova, autodesenvolvimento, perfil do usuário, tom de voz do usuário.
---

# Agent Evolution Loop

Objetivo: transformar feedback real em melhoria persistente do agente.

## Loop obrigatório

1. **Feedback** — capturar crítica, preferência, correção ou elogio com contexto.
2. **Memória** — registrar em arquivo apropriado:
   - feedback visual/copy: `memory/feedback/*.md`
   - preferência/comportamento do usuário: `memory/context/people.md` ou `USER.md`
   - regra permanente: `memory/context/decisions.md`
   - erro que não pode repetir: `memory/context/lessons.md`
   - projeto específico: `memory/projects/*.md`
3. **Dreaming** — deixar o Dreaming consolidar sinais recorrentes em `DREAMS.md` e promover para `MEMORY.md` quando forte.
4. **Regra** — se o padrão for claro, atualizar AGENTS/MEMORY/arquivo de projeto.
5. **Skill** — se o padrão vira procedimento repetível, criar ou editar skill enxuta.

## Quando virar skill

Criar/editar skill quando acontecer pelo menos um:
- mesmo erro repetiu 2+ vezes;
- feedback define procedimento reutilizável;
- tarefa exige checklist específico;
- existe padrão de qualidade que precisa ser aplicado sempre;
- o agente está “viciando” numa solução e precisa de guardrail operacional.

## Perfil comportamental do usuário

Quando observar preferência estável de comunicação:
- tom, velocidade, tolerância a detalhe;
- palavras/frases que o usuário usa;
- tipo de resposta que irrita ou ajuda;
- nível de autonomia esperado;
- critérios de qualidade subjetivos.

Registrar em memória sem imitar de forma caricata. O objetivo é ficar na mesma onda, não fazer teatro.

## Regra de segurança

Dreaming e evolução nunca justificam:
- burlar confirmação humana;
- criar acesso novo;
- mexer em credencial/produção/financeiro sem autorização;
- transformar conteúdo sensível em skill pública.

## Saída esperada ao receber feedback

Responder curto:
- o que aprendeu;
- onde registrou;
- o que muda na próxima execução;
- se precisa virar skill agora ou só memória por enquanto.
