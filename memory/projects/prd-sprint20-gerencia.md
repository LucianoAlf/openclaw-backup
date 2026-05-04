# PRD — Sprint 20: Camada de Gerência do LA Organizer

## Metadados
- **Produto:** LA Organizer
- **Sprint:** 20
- **Título:** Camada de Gerência
- **Status:** Draft para validação
- **Dependência anterior:** Sprint 19 — Pedagógico
- **Próxima etapa obrigatória após esta frente:** Auditoria de Eventos

---

## 1. Problema

A LA Music já possui frentes pedagógicas, comerciais e operacionais bem identificáveis, mas existe um domínio transversal da unidade que não cabe completamente em nenhuma dessas camadas: a **Gerência**.

Hoje, muitos casos de retenção, experiência, articulação entre setores e relacionamento com pais/alunos dependem de comunicação dispersa, improviso ou memória contextual dos líderes. Isso gera:

- conflitos sem rastreabilidade
- retenção reativa demais
- tratamento inconsistente de pais/alunos insatisfeitos
- demora em mobilizar as áreas certas
- pouca visibilidade sobre problemas de experiência da unidade
- sobreposição confusa entre gerência, atendimento, pedagógico e comercial

O problema não é apenas “falta de tarefa”.

O problema central é:

> falta uma camada explícita de governança relacional da unidade.

---

## 2. Tese de produto

A Gerência deve ser modelada como:

> **camada de articulação relacional e operação humana da unidade**

Ela existe para coordenar e destravar o que acontece na interface entre:
- aluno
- responsável
- atendimento
- recepção
- secretaria
- relacionamento
- professores
- coordenação local
- comercial
- pedagógico
- financeiro
- marketing

Não substitui essas áreas.
Ela integra, cobra, acompanha e organiza respostas.

---

## 3. Objetivo da Sprint 20

Implementar o departamento **Gerência** dentro da camada operacional replicável do LA Organizer, reutilizando o motor atual e adicionando:

- papéis de gerência por unidade
- autoridade transversal explícita
- taxonomia inicial de demandas gerenciais
- skill conversacional `gerencia.md`
- piloto controlado com os gerentes das unidades

Sem criar módulo visual separado no MVP.

---

## 4. Escopo

### 4.1 Incluído
- novo departamento `gerencia`
- request types da Gerência
- modelagem das alçadas transversais da função
- skill `gerencia.md`
- integração via `/mais/operacoes`
- piloto com gerentes das três unidades

### 4.2 Não incluído
- novo dashboard exclusivo da Gerência
- analytics avançado de retenção
- CRM completo
- automação de Eventos
- modelagem completa de jornada do aluno
- substituição do Comercial ou do Pedagógico

---

## 5. Pessoas e estrutura do MVP

### Camada superior
- **Alf**
- **Anne**

Todos os gerentes respondem a Alf e Anne.

### Gerentes por unidade
- **Jereh** — Campo Grande — `5521985525984`
- **Clayton** — Recreio (interino cobrindo licença maternidade da Fabi) — `5521990450802`
- **Krissya** — Barra — `5521966875271`

---

## 6. Natureza da autoridade da Gerência

Foi definido que o gerente pode:
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

### Interpretação estrutural
A Gerência é uma camada de autoridade transversal da unidade, com poder legítimo de articulação entre setores.

---

## 7. Áreas e papéis abaixo/ao redor da Gerência

No fluxo real, a Gerência interage diretamente com:
- recepção
- professores
- atendimento
- relacionamento
- pré-atendimento
- secretaria
- coordenadores locais

Essas áreas não são “donas” da Gerência. Elas orbitam no seu campo de articulação dentro da unidade.

---

## 8. Tipos iniciais de demanda

### 8.1 `risco-de-evasao`
Casos:
- aluno em risco de saída
- sinais de afastamento
- quebra de vínculo
- risco de cancelamento

### 8.2 `recuperacao-de-aluno`
Casos:
- tentativa de reativação
- reconquista
- recuperação de vínculo
- retorno de aluno afastado

### 8.3 `alinhamento-com-responsavel`
Casos:
- conversa com pai/mãe/responsável
- mediação de expectativa
- devolutiva relacional
- ajuste de percepção sobre a experiência

### 8.4 `problema-de-atendimento`
Casos:
- falha no atendimento
- ruído de recepção
- problema de retorno
- reclamação operacional do contato com a unidade

### 8.5 `experiencia-da-unidade`
Casos:
- conflito de experiência na unidade
- percepção ruim do ambiente ou do serviço
- fricções na vivência presencial

### 8.6 `negociacao-relacional`
Casos:
- negociação sensível de permanência
- construção de alternativa de retenção
- tratativa relacional que não é só comercial

### 8.7 `pendencia-gerencial`
Tipo coringa controlado para exceções.

### 8.8 `articulacao-interna`
Casos:
- necessidade de acionar múltiplas áreas
- articulação entre recepção, secretaria, comercial, coordenação, atendimento etc.
- problemas transversais da unidade

---

## 9. Regras de alçada

### 9.1 Gerente
Pode:
- cobrar áreas da unidade
- acionar pais/alunos
- acionar comercial
- acionar marketing
- acionar financeiro
- solicitar apoio pedagógico
- integrar múltiplas frentes

### 9.2 Regra de identidade
A Gerência não substitui a liderança técnica de cada área.
Ela atua como camada de coordenação e destrave.

### 9.3 Regra de fronteira
Quando o caso for claramente pedagógico, o fluxo deve envolver o Pedagógico.
Quando o caso for claramente gerencial/relacional, o dono é Gerência.
Quando o caso for híbrido, a Gerência pode articular e o Pedagógico pode apoiar.

---

## 10. Roteamento conversacional esperado

### Origem das demandas
Podem partir de:
- gerente
- Alf / Anne
- recepção
- atendimento
- relacionamento
- secretaria
- professores
- coordenadores locais
- pais/alunos/responsáveis via contato recebido

### Destino das demandas
Podem ir para:
- gerente da unidade
- recepção
- atendimento
- relacionamento
- comercial
- coordenação pedagógica
- marketing
- financeiro
- secretaria
- coordenadores locais

### Regra de prioridade
Se o caso envolver:
- risco de saída → Gerência
- pai/responsável insatisfeito → Gerência
- falha de experiência → Gerência
- dificuldade pedagógica pura → Pedagógico
- caso híbrido → Gerência coordena + Pedagógico apoia quando necessário

---

## 11. UX / PWA

### Decisão
A Gerência deve entrar pela mesma camada `/mais/operacoes`.

### Implicações
Sem módulo novo agora.
Sem dashboard separado no MVP.
Sem quebrar a lógica da camada replicável.

### Adições esperadas
- departamento Gerência
- request types próprios
- responsáveis por unidade
- filtros e detalhes coerentes com a malha atual

---

## 12. Skill `gerencia.md`

### Objetivo
Ensinar o TOM a:
- entender Gerência como articulação relacional da unidade
- distinguir demanda gerencial de demanda pedagógica
- distinguir retenção de comercial puro
- acionar o gerente certo da unidade
- escalar corretamente áreas de apoio
- entender pais/alunos como centro do caso quando for relacional

### Exemplos de comandos esperados
- “esse aluno está em risco de evasão”
- “fala com a Krissya sobre esse pai insatisfeito”
- “abre uma demanda de recuperação desse aluno”
- “isso virou problema de atendimento”
- “aciona a gerência da unidade”
- “preciso articular recepção, secretaria e coordenação nesse caso”

---

## 13. Hipótese técnica

### Reaproveitar a arquitetura atual
Usar:
- `departments`
- `department_request_types`
- `tasks`
- skill layer
- `/mais/operacoes`

### Seed esperado
- department: `gerencia`
- request types da Gerência
- responsáveis por unidade

### Regra principal
Não criar nova entidade principal no banco para o MVP da Gerência.

---

## 14. Piloto inicial

### Participantes
- Jereh
- Clayton
- Krissya

### Interações esperadas no piloto
- recepção
- atendimento
- relacionamento
- secretaria
- comercial
- coordenação pedagógica

### Objetivos do piloto
Validar:
- se a taxonomia cobre os principais casos
- se a fronteira com Pedagógico ficou clara
- se a autoridade transversal faz sentido no uso real
- se os fluxos de retenção e experiência são acionáveis

---

## 15. Critérios de sucesso

A Sprint 20 será bem-sucedida se:

1. Gerência operar no motor atual sem módulo paralelo
2. o sistema distinguir Gerência de Pedagógico com clareza suficiente
3. os gerentes conseguirem agir como articuladores reais da unidade
4. os principais casos de retenção/experiência puderem ser roteados corretamente
5. a skill da Gerência reduzir ambiguidade de comando
6. a camada de autoridade transversal ficar usável sem inflar demais o escopo

---

## 16. Riscos

### 16.1 Confusão com Comercial
Mitigação:
- deixar claro que a Gerência trabalha retenção e experiência, não pipeline comercial puro

### 16.2 Confusão com Pedagógico
Mitigação:
- explicitar fronteiras no PRD e na skill

### 16.3 Escopo virar CRM gigante
Mitigação:
- manter MVP enxuto, operacional e baseado em demanda

### 16.4 Gerência virar “categoria genérica de tudo”
Mitigação:
- taxonomia inicial bem definida
- `pendencia-gerencial` como coringa controlado, não buraco negro

---

## 17. Dependências e roadmap

### Dependência anterior
- Sprint 19 do Pedagógico desenhada/estável

### Próximas etapas
1. Sprint 20 — Gerência
2. Auditoria obrigatória de Eventos
3. Só depois sprint específica de Eventos

---

## 18. Resumo executivo

A Sprint 20 deve formalizar a Gerência como o elo de coordenação relacional da unidade.

O foco não é criar mais uma fila qualquer.

O foco é:

> **dar forma operacional à autoridade transversal que já existe na prática**

para lidar com retenção, experiência, conflitos e articulação entre áreas.
