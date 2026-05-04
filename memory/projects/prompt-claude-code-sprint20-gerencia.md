# Prompt — Claude Code — Sprint 20 Gerência

Quero implementar a **Sprint 20 — Camada de Gerência do LA Organizer**.

Leia primeiro estes documentos como fonte de verdade:

1. `memory/projects/sprint20-gerencia-documento-base.md`
2. `memory/projects/prd-sprint20-gerencia.md`
3. `memory/projects/sprint19-pedagogico-documento-base.md`
4. `memory/projects/prd-sprint19-pedagogico.md`
5. `memory/projects/la-organizer-camada-operacional-replicavel-por-departamento.md`
6. `memory/projects/prd-coordenacao-conversacional-via-tom.md`
7. `memory/projects/spec-base-sprint17-active-coordination-context.md`
8. `docs/superpowers/specs/2026-05-03-sprint15-operacoes-design.md`
9. `docs/superpowers/specs/2026-05-03-sprint16-coordenacao-conversacional-design.md`
10. `docs/superpowers/specs/2026-05-03-sprint17-acc-design.md`

Objetivo da sprint:
Implementar o departamento **Gerência** dentro da camada operacional replicável do LA Organizer, respeitando a autoridade transversal dos gerentes e sem confundir esse domínio com Pedagógico, Comercial ou Operação pura.

---

## Contexto de produto

A Gerência deve ser modelada como uma **camada de articulação relacional e operação humana da unidade**.

Ela não substitui as áreas da escola.
Ela coordena, acompanha, cobra e integra respostas entre áreas quando o caso envolve:
- retenção
- risco de evasão
- pais/responsáveis insatisfeitos
- experiência da unidade
- problemas de atendimento
- recuperação de aluno
- articulação entre recepção, secretaria, comercial, pedagógico, atendimento etc.

---

## Estrutura oficial do MVP

### Camada superior
- Alf
- Anne

### Gerentes por unidade
- Jereh — Campo Grande — `5521985525984`
- Clayton — Recreio (interino cobrindo licença maternidade da Fabi) — `5521990450802`
- Krissya — Barra — `5521966875271`

Todos respondem a Alf e Anne.

---

## Regra crítica de alçada

O gerente pode:
- cobrar atendimento
- cobrar recepção
- cobrar professores
- cobrar comercial
- solicitar suporte à coordenação pedagógica
- falar diretamente com pais/alunos
- acionar financeiro
- acionar marketing
- cobrar pré-atendimento
- cobrar secretaria
- cobrar coordenadores locais

Isso significa que a Gerência nasce como uma camada de **alçada transversal ampla da unidade**.

---

## Tipos iniciais de demanda

Implementar estes request types para o departamento `gerencia`:

1. `risco-de-evasao`
2. `recuperacao-de-aluno`
3. `alinhamento-com-responsavel`
4. `problema-de-atendimento`
5. `experiencia-da-unidade`
6. `negociacao-relacional`
7. `pendencia-gerencial`
8. `articulacao-interna`

---

## Direção arquitetural obrigatória

### 1. Reaproveitar o motor existente
Não criar módulo paralelo.
Não criar nova entidade principal no banco sem necessidade muito forte.
Usar a arquitetura já consolidada nas sprints anteriores.

### 2. `/mais/operacoes` continua sendo o ponto de entrada
A Gerência entra na camada atual, não em outra área.

### 3. Distinguir Gerência de Pedagógico
Esse é um dos pontos mais importantes desta sprint.

#### Pedagógico
- qualidade pedagógica
- professores no eixo pedagógico
- jornada de aprendizado
- School x Kids

#### Gerência
- retenção
- relacionamento com pais/alunos
- experiência da unidade
- articulação entre áreas
- conflitos relacionais/operacionais

### 4. Gerência não é Comercial puro
Se o caso for pipeline/comercial puro, não force na Gerência.
Mas se for permanência, retenção, negociação relacional e experiência, a Gerência deve assumir protagonismo.

### 5. Não misturar com Eventos
Essa sprint não implementa Eventos.
Se houver casos tangenciais, tratar só como demanda gerencial/relacional ligada à experiência.

---

## O que eu quero que você produza

Quero que você me entregue a sprint em fatias, com design e depois execução.

### Entregáveis esperados
1. **Documento técnico/design da Sprint 20**
2. **Plano por fatias**
3. **Modelagem/seed do departamento `gerencia`**
4. **Skill `gerencia.md`**
5. **Integração com o motor/TOM**
6. **Ajustes em `/mais/operacoes` se realmente necessários**
7. **Validação técnica + smoke tests**

---

## O que precisa existir no design

### A. Papel operacional principal
Modelar o gerente como articulador transversal da unidade.

### B. Regras de autoridade
Garantir que o comportamento do sistema respeite que o gerente pode:
- cobrar áreas da unidade
- acionar famílias
- mobilizar comercial, pedagógico, marketing e financeiro quando necessário

### C. Tipos de demanda coerentes
Os request types precisam refletir retenção, experiência e articulação.

### D. Casos reais que o TOM deve entender
Exemplos mínimos:
- “esse aluno está em risco de evasão”
- “fala com a Krissya sobre esse pai insatisfeito”
- “abre uma demanda de recuperação desse aluno”
- “isso virou problema de atendimento”
- “aciona a gerência da unidade”
- “preciso articular recepção, secretaria e coordenação nesse caso”

---

## Restrições

- não inventar CRM gigante
- não inflar com analytics avançado agora
- não quebrar a separação entre Gerência e Pedagógico
- não quebrar a camada replicável por departamento
- não misturar com Eventos nesta sprint

---

## Pergunta principal da execução

Quero que você trate esta sprint como:

> **a formalização operacional da autoridade transversal da unidade**

E desenhe a solução a partir disso.

---

## Sua tarefa agora

1. Ler os documentos citados.
2. Propor o **design técnico da Sprint 20**.
3. Quebrar em **fatias implementáveis**.
4. Apontar riscos, decisões abertas e ordem recomendada.
5. Só depois partir para implementação.

Quero resposta objetiva, técnica e sem floreio.
