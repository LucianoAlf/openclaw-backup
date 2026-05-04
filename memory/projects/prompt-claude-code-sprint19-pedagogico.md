# Prompt — Claude Code — Sprint 19 Pedagógico

Quero implementar a **Sprint 19 — Camada Pedagógica do LA Organizer**.

Leia primeiro estes documentos como fonte de verdade:

1. `memory/projects/sprint19-pedagogico-documento-base.md`
2. `memory/projects/prd-sprint19-pedagogico.md`
3. `memory/projects/la-organizer-camada-operacional-replicavel-por-departamento.md`
4. `memory/projects/prd-coordenacao-conversacional-via-tom.md`
5. `memory/projects/spec-base-sprint17-active-coordination-context.md`
6. `docs/superpowers/specs/2026-05-03-sprint15-operacoes-design.md`
7. `docs/superpowers/specs/2026-05-03-sprint16-coordenacao-conversacional-design.md`
8. `docs/superpowers/specs/2026-05-03-sprint17-acc-design.md`

Objetivo da sprint:
Implementar o departamento **Pedagógico** dentro da camada operacional replicável do LA Organizer, respeitando hierarquia, alçadas e subdomínios internos, sem criar um módulo isolado e sem quebrar o motor já existente.

---

## Contexto de produto

O Pedagógico não é só mais um departamento operacional.
Ele é o primeiro domínio onde a conversa entre pessoas, a autoridade hierárquica e o roteamento contextual importam quase tanto quanto a task.

A estrutura oficial do MVP é:

### Camada superior
- Alf
- Anne

### Coordenação pedagógica — mesmo nível
- Juliana — Coordenadora LA Music School
- Quintela — Coordenador LA Music Kids

### Abaixo deles
- assistentes pedagógicos
- mentores pedagógicos

### Professores
- podem abrir demandas
- podem abrir para assistentes pedagógicos e coordenação
- são destinatários/alvo de demanda também
- não têm poder de cobrança/delegação no MVP

### Regra crítica
- Juliana e Quintela têm o mesmo nível hierárquico
- Juliana lidera **School**
- Quintela lidera **Kids**
- mentores orientam, mas **não delegam**
- assistentes podem cobrar professores dentro do escopo
- professores não entram como governança formal no MVP

---

## Pessoas já mapeadas

### Coordenação
- Juliana — `5521981708609`
- Quintela — `5521971751320`

### Assistentes pedagógicos
- Leo — Barra — `5521992053152`
- Ramon — Recreio + Bandas — `5521999715997`
- Dai — Campo Grande — `5521986409985`
- Matheus Felipe — LA Music Kids — `5521978755351`
- Jordan — eventos + bateria — `5521981450588`
- Rodrigo — cordas — `5521997548859`

### Mentores pedagógicos / guardiões da cultura
- Peterson — `5521989366076`
- Kinho — `5521987375854`
- Renan — `5521965736779`

---

## Tipos iniciais de demanda

Implementar estes request types iniciais para o departamento `pedagogico`:

1. `acompanhamento-professor`
2. `apoio-ao-aluno`
3. `alinhamento-de-turma`
4. `alinhamento-com-responsavel`
5. `evento-pedagogico`
6. `pendencia-pedagogica`
7. `suporte-ao-professor` *(se fizer sentido já no MVP; se não, justificar)*

---

## Direção arquitetural obrigatória

### 1. Reaproveitar o motor existente
Não criar módulo paralelo.
Não criar nova entidade principal no banco sem necessidade muito forte.
Usar a arquitetura já criada na Sprint 15.

### 2. `/mais/operacoes` continua sendo o ponto de entrada
Não mover o Pedagógico para outra área.
Não criar nova tela grande agora, salvo necessidade muito bem justificada.

### 3. Modelar subdomínios internos
O Pedagógico nasce com dois subdomínios principais:
- `School`
- `Kids`

Eles precisam existir de algum modo no comportamento do sistema, no roteamento ou nos metadados operacionais.

### 4. Roteamento e alçada importam mais que UI
Se tiver trade-off entre interface bonita e regra correta de autoridade, priorize regra correta.

### 5. Evento pedagógico não é o motor de Eventos
Não misturar esta sprint com implementação da camada de Eventos.
Se necessário, tratar `evento-pedagogico` apenas como demanda pedagógica ligada a preparação/acompanhamento.

---

## O que eu quero que você produza

Quero que você me entregue a sprint em fatias, com plano de implementação e depois execução.

### Entregáveis esperados
1. **Documento técnico/design da Sprint 19**
2. **Plano por fatias**
3. **Implementação do seed/modelagem necessária**
4. **Skill `pedagogico.md`**
5. **Integração com o motor/TOM**
6. **Ajustes em `/mais/operacoes` se realmente necessários**
7. **Validação técnica + smoke tests**

---

## O que precisa existir no design

### A. Papéis operacionais do MVP
Modelar minimamente:
- `pedagogical_lead`
- `pedagogical_assistant`
- `pedagogical_mentor`
- `teacher` (como origem/destinatário, não governança)

### B. Regras de autoridade
Garantir no comportamento:
- lead delega e cobra
- assistant cobra professor no próprio escopo
- mentor orienta, não delega
- teacher abre demanda, não governa fluxo

### C. Regras School x Kids
Sistema precisa refletir:
- Juliana → School
- Quintela → Kids

### D. Casos reais que o TOM deve entender
Exemplos mínimos:
- “cobra o professor X sobre o relatório de aula”
- “alinha com a Juliana o planejamento do recital”
- “isso é Kids, leva pro Quintela”
- “abre uma pendência pedagógica do aluno Y”
- “fala com o assistente pedagógico da Barra”
- “professor tal está precisando de material”

---

## Restrições

- não inventar módulo novo sem necessidade
- não inflar escopo com analytics pedagógico
- não misturar com Events sprint agora
- não quebrar Sprint 15/16/17
- não violar o princípio da camada replicável por departamento

---

## Pergunta principal da execução

Quero que você trate esta sprint como:
> **a primeira camada departamental com complexidade relacional interna real**

e desenhe a solução em cima disso.

---

## Sua tarefa agora

1. Ler os documentos citados.
2. Propor o **design técnico da Sprint 19**.
3. Quebrar em **fatias implementáveis**.
4. Apontar riscos, decisões abertas e ordem recomendada.
5. Só depois partir para implementação.

Quero resposta objetiva, técnica e sem floreio.
