# PRD — Sprint 19: Camada Pedagógica do LA Organizer

## Metadados
- **Produto:** LA Organizer
- **Sprint:** 19
- **Título:** Camada Pedagógica
- **Status:** Draft para validação
- **Dependência anterior:** Sprint 18 — Integridade de Agenda e Execução
- **Próxima prioridade mapeada:** Sprint 20 — Gerência

---

## 1. Problema

Depois da consolidação da camada operacional replicável por departamento e da coordenação conversacional via TOM, o próximo gargalo da LA Music está no domínio pedagógico.

Hoje, o Pedagógico funciona com forte dependência de WhatsApp, memória contextual, relação pessoal e hierarquia implícita. Isso gera risco de:

- cobranças fora de escopo
- encaminhamentos errados
- ruído entre School e Kids
- perda de contexto em casos de aluno/professor/responsável
- dependência excessiva da cabeça dos coordenadores
- baixa rastreabilidade das pendências pedagógicas

O problema central não é ausência de task manager.

O problema central é:

> o Pedagógico precisa de uma camada de governança que respeite hierarquia, subdomínios e contexto humano.

---

## 2. Tese de produto

O Pedagógico não deve nascer como “mais um departamento operacional”.

Ele deve nascer como:

> **camada de coordenação pedagógica em rede, com alçadas reais e roteamento contextual**

Essa camada precisa representar:
- coordenação pedagógica
- assistentes pedagógicos
- mentores pedagógicos
- professores
- School x Kids
- especialidades transversais
- demandas pedagógicas reais

Ou seja:
- não é só fila
- não é só task
- não é só chat

É coordenação pedagógica estruturada.

---

## 3. Objetivo da Sprint 19

Implementar o primeiro MVP do departamento **Pedagógico** dentro da camada operacional replicável do LA Organizer, reutilizando o motor já criado e adicionando:

- estrutura de pessoas e papéis
- regras de alçada
- tipos de demanda pedagógica
- roteamento School x Kids
- skill conversacional `pedagogico.md`
- piloto controlado com coordenação + assistentes

Sem criar tela nova obrigatória no MVP.

---

## 4. Escopo

### 4.1 Incluído
- novo departamento `pedagogico`
- request types do Pedagógico
- definição de papéis operacionais do MVP
- definição de hierarquia e alçadas
- skill `pedagogico.md`
- integração com `/mais/operacoes`
- piloto com coordenação e assistentes
- entrada de professores como origem/destinatário de demanda

### 4.2 Não incluído
- novo módulo visual exclusivo do Pedagógico
- sistema de avaliação pedagógica complexo
- dashboard pedagógico analítico avançado
- automação específica de eventos
- modelagem profunda de histórico pedagógico do aluno
- expansão total do papel dos professores como operadores plenos
- auditoria ou implementação de Eventos

---

## 5. Estrutura organizacional oficial do MVP

### 5.1 Camada superior
- **Alf**
- **Anne**

Atuam acima da coordenação pedagógica.

### 5.2 Coordenação pedagógica
Mesmo nível hierárquico:
- **Juliana** — Coordenadora da LA Music School
- **Quintela** — Coordenador da LA Music Kids

### 5.3 Assistentes pedagógicos
- **Leo** — Barra
- **Ramon** — Recreio + Bandas
- **Dai** — Campo Grande
- **Matheus Felipe** — LA Music Kids
- **Jordan** — eventos + bateria
- **Rodrigo** — cordas

### 5.4 Mentores pedagógicos
- **Peterson**
- **Kinho**
- **Renan**

### 5.5 Professores
No MVP:
- podem abrir demandas
- podem receber demandas
- não delegam
- não cobram como camada formal de governança

---

## 6. Papéis operacionais do MVP

### 6.1 `pedagogical_lead`
Representa:
- Juliana
- Quintela

Permissões esperadas:
- criar demanda
- delegar demanda
- cobrar assistentes
- cobrar mentores
- cobrar professores
- acompanhar execução
- escalar casos
- redirecionar entre School e Kids

### 6.2 `pedagogical_assistant`
Representa:
- Leo
- Ramon
- Dai
- Matheus Felipe
- Jordan
- Rodrigo

Permissões esperadas:
- abrir demanda
- registrar pendência
- encaminhar para coordenação
- cobrar professores
- operar dentro do próprio escopo

### 6.3 `pedagogical_mentor`
Representa:
- Peterson
- Kinho
- Renan

Permissões esperadas:
- orientar
- aconselhar
- apoiar coordenação
- apoiar professores
- abrir demanda se necessário

Restrição crítica:
- **não delega** no MVP

### 6.4 `teacher`
Papel externo ao núcleo de governança.

Pode:
- abrir demanda
- receber demanda
- acionar coordenação ou assistente

Não pode:
- delegar
- cobrar formalmente
- atuar como operador pleno da malha de governança

---

## 7. Subdomínios do Pedagógico

### 7.1 School
Responsável principal:
- Juliana

Escopo:
- adolescentes e adultos
- operação pedagógica da LA Music School

### 7.2 Kids
Responsável principal:
- Quintela

Escopo:
- bebês e crianças até 11 anos
- operação pedagógica da LA Music Kids

### 7.3 Especialidades transversais
Existem apoios/especialidades que atravessam os subdomínios:
- bandas
- bateria
- cordas
- cultura
- eventos pedagógicos
- unidade

Esses apoios não anulam School/Kids. Eles orbitam em torno dessa divisão principal.

---

## 8. Tipos iniciais de demanda

### 8.1 `acompanhamento-professor`
Casos:
- cobrança de relatório
- retorno pendente
- ajuste de condução
- acompanhamento de performance

### 8.2 `apoio-ao-aluno`
Casos:
- falta recorrente
- dificuldade pedagógica
- ajuste de trilha
- caso sensível

### 8.3 `alinhamento-de-turma`
Casos:
- troca de turma
- mudança de professor
- encaixe
- redistribuição

### 8.4 `alinhamento-com-responsavel`
Casos:
- devolutiva pedagógica
- orientação sobre trilha
- alinhamento de situação do aluno

### 8.5 `evento-pedagogico`
Casos:
- banda/show pedagógico
- preparação pedagógica para recital/show
- demandas pedagógicas ligadas a eventos

Restrição:
- não substitui o motor geral de Eventos

### 8.6 `pendencia-pedagogica`
Tipo coringa controlado para exceções.

### 8.7 `suporte-ao-professor` (opcional)
Casos:
- material
- reparo
- necessidade de apoio aberta por professor

Observação:
Pode ser ativado já no MVP ou absorvido depois em integração com o fluxo operacional já existente.

---

## 9. Regras de alçada

### 9.1 Coordenação
Juliana e Quintela podem:
- delegar para assistentes
- delegar para professores
- cobrar assistentes
- cobrar mentores
- cobrar professores
- receber demandas de professores

### 9.2 Assistentes
Assistentes podem:
- cobrar professores
- abrir demandas
- escalar casos para coordenação
- operar no próprio domínio

Assistentes não têm poder irrestrito de coordenação horizontal ampla.

### 9.3 Mentores
Mentores podem:
- orientar
- apoiar
- aconselhar
- abrir demanda quando necessário

Mentores não podem:
- delegar
- funcionar como chefia operacional do fluxo

### 9.4 Professores
Professores podem:
- abrir demanda para coordenação
- abrir demanda para assistentes
- receber demanda

Professores não podem:
- delegar
- cobrar como governança formal

---

## 10. Roteamento conversacional esperado

### 10.1 Origem das demandas
Demandas podem partir de:
- coordenação
- assistentes
- mentores
- professores
- Alf / Anne

### 10.2 Roteamento padrão
- School → prioriza Juliana
- Kids → prioriza Quintela
- casos de unidade/especialidade → priorizam assistente adequado
- casos de orientação/cultura → podem envolver mentor
- professores → falam com assistente ou coordenação

### 10.3 Regra de prioridade
Quando houver ambiguidade:
1. respeitar School x Kids
2. respeitar escopo da pessoa
3. respeitar autoridade formal
4. evitar mandar para mentor algo que é cobrança formal

---

## 11. UX / PWA

### Decisão de produto
O Pedagógico entra no MVP via a mesma camada `/mais/operacoes`.

### Implicações
Não criar nova tela agora.
Reaproveitar:
- abas por departamento
- fila operacional existente
- detalhe operacional
- filtros existentes

### Adições esperadas
- nova aba/entrada do departamento Pedagógico
- novos tipos de demanda
- filtros por subdomínio quando necessário
- associação com responsáveis padrão e contexto correto

---

## 12. Skill `pedagogico.md`

### Objetivo
Ensinar o TOM a:
- compreender School x Kids
- respeitar alçada
- distinguir coordenação, assistente, mentor e professor
- encaminhar corretamente
- evitar cobrança por quem não tem autoridade
- diferenciar evento pedagógico de Eventos como motor geral

### Exemplos de comandos esperados
- “cobra o professor X sobre o relatório de aula”
- “alinha com a Juliana o planejamento do recital”
- “fala com o assistente pedagógico da Barra”
- “abre pendência pedagógica do aluno Y”
- “isso é Kids, leva pro Quintela”
- “isso é School, manda pra Juliana”

---

## 13. Hipótese de modelagem técnica

### Estrutura base
Reaproveitar:
- `departments`
- `department_request_types`
- `tasks`
- skill layer
- `/mais/operacoes`

### Seed esperado
- department: `pedagogico`
- request types pedagógicos
- responsáveis associados conforme desenho do departamento

### Decisão importante
Não criar nova entidade principal no banco para Pedagógico no MVP.

---

## 14. Piloto inicial

### Participantes do piloto
- Juliana
- Quintela
- assistentes pedagógicos

### Participação dos mentores
- entra como apoio/orientação
- sem poder pleno de delegação

### Participação dos professores
- origem/destinatário de demanda
- sem operar como coordenação

### Objetivos do piloto
Validar:
- hierarquia real
- cobertura dos tipos de demanda
- eficiência do roteamento
- clareza entre School e Kids
- adequação do papel de professores e mentores

---

## 15. Critérios de sucesso

A Sprint 19 será bem-sucedida se:

1. o Pedagógico puder operar dentro do motor atual sem módulo paralelo
2. School e Kids estiverem claramente diferenciados
3. Juliana e Quintela conseguirem atuar como leads formais
4. assistentes conseguirem operar dentro de seu escopo
5. mentores não gerarem confusão de autoridade
6. professores conseguirem abrir demandas sem virar camada de governança
7. o TOM roteie corretamente a maioria dos casos do piloto

---

## 16. Riscos

### 16.1 Confusão entre School e Kids
Mitigação:
- explicitar no seed e na skill

### 16.2 Mentores parecerem chefes operacionais
Mitigação:
- regra explícita: mentor orienta, não delega

### 16.3 Professores ganharem poder demais no MVP
Mitigação:
- manter papel de origem/destinatário, não de governança

### 16.4 Escopo inflar cedo demais
Mitigação:
- manter MVP enxuto
- sem nova tela
- sem analytics pedagógico agora

### 16.5 Evento pedagógico colidir com motor de Eventos
Mitigação:
- tratar evento pedagógico apenas como demanda pedagógica
- manter auditoria de Eventos como etapa separada futura

---

## 17. Dependências e roadmap

### Dependência anterior
- Sprint 18 concluída e estável

### Próximas prioridades
1. Sprint 19 — Pedagógico
2. Sprint 20 — Gerência
3. Auditoria obrigatória de Eventos
4. Sprint específica de Eventos só depois da auditoria

---

## 18. Resumo executivo

A Sprint 19 do Pedagógico é a primeira expansão da camada operacional para um domínio em que:
- hierarquia pesa muito
- contexto humano pesa muito
- subdomínios internos são decisivos

Por isso, o foco não é interface nova.

O foco é:
> **papel certo, pessoa certa, autoridade certa e roteamento certo**.
