# Sprint 20 — Gerência

## Documento-base

### 1. Contexto e tese

Depois da camada operacional replicável, da coordenação conversacional e da expansão para o Pedagógico, a próxima frente prioritária do LA Organizer é a **Gerência**.

A Gerência não é Comercial, não é Pedagógico e não é apenas Atendimento.

Ela deve ser entendida como:

> **camada de gestão relacional e operação humana da unidade**

Seu papel é coordenar o que acontece na interface entre:
- pais e alunos
- experiência da unidade
- retenção
- recuperação
- atendimento
- recepção
- relacionamento
- secretaria
- articulação entre áreas

Ela encosta em múltiplos times ao mesmo tempo e, por isso, nasce como uma camada de alta alçada transversal.

---

### 2. Estrutura hierárquica oficial do MVP Gerência

#### Camada superior
- **Alf**
- **Anne**

Todos os gerentes respondem a Alf e Anne.

#### Gerentes por unidade
- **Jereh** — Gerente de Campo Grande — `5521985525984`
- **Clayton** — Gerente interino do Recreio (cobrindo licença maternidade da Fabi) — `5521990450802`
- **Krissya** — Gerente da Barra — `5521966875271`

Os gerentes ocupam a camada de gestão da unidade.

---

### 3. Natureza da Gerência

A Gerência é uma camada de comando relacional-operacional da unidade.

Isso significa que ela pode:
- acompanhar alunos em risco
- agir em retenção e recuperação
- tratar conflitos de experiência
- acionar áreas diferentes
- alinhar responsáveis/pais
- cobrar setores humanos da operação
- articular respostas transversais entre áreas

A Gerência não substitui as outras áreas.

Ela coordena, cobra, acompanha e integra.

---

### 4. Alçadas formais do gerente

Foi definido que o gerente pode:

1. cobrar atendimento — **sim**
2. cobrar recepção — **sim**
3. cobrar professores — **sim**
4. cobrar comercial — **sim**
5. solicitar suporte à coordenação pedagógica — **sim**
6. falar diretamente com pais/alunos — **sim**
7. acionar financeiro — **sim**
8. acionar marketing — **sim**
9. cobrar pré-atendimento — **sim**
10. cobrar secretaria — **sim**
11. cobrar coordenadores locais — **sim**

### Leitura estrutural
Isso consolida a Gerência como uma camada de **articulação ampla da unidade**, com poder real de cobrança e integração entre frentes.

---

### 5. Quem está abaixo deles no fluxo

As frentes abaixo/ao redor da Gerência no fluxo são:
- recepção
- professores
- atendimento
- relacionamento
- pré-atendimento
- secretaria
- coordenadores locais

Isso reforça que a Gerência atua como eixo articulador da experiência da unidade.

---

### 6. Tipos reais de demanda já mapeados

Demandas reais já citadas:
- aluno em risco de evasão
- pai insatisfeito
- problema de atendimento
- pedido de negociação relacional
- recuperação de aluno
- conflito de experiência na unidade

Essas demandas já são suficientes para estruturar o MVP.
Outras podem surgir depois e ser incorporadas.

---

### 7. Tipos iniciais de demanda da Gerência

A lista inicial aprovada para a Sprint 20 é:

#### 7.1 `risco-de-evasao`
Usos:
- aluno sinalizando saída
- comportamento de afastamento
- risco de cancelamento
- alerta de perda de vínculo

#### 7.2 `recuperacao-de-aluno`
Usos:
- reativação
- reconquista
- tentativa de recuperação de vínculo
- reaproximação estruturada

#### 7.3 `alinhamento-com-responsavel`
Usos:
- contato com pai/mãe/responsável
- necessidade de devolutiva relacional
- mediação de expectativa

#### 7.4 `problema-de-atendimento`
Usos:
- falha de recepção
- ruído de atendimento
- problema de contato
- reclamação operacional de jornada

#### 7.5 `experiencia-da-unidade`
Usos:
- conflito de experiência
- percepção ruim de ambiente/serviço
- problema humano da jornada presencial
- situações que afetam a vivência da unidade

#### 7.6 `negociacao-relacional`
Usos:
- negociação sensível não puramente comercial
- tratativa de permanência
- construção de alternativa para retenção

#### 7.7 `pendencia-gerencial`
Tipo coringa controlado para casos que ainda não encaixam bem na taxonomia inicial.

#### 7.8 `articulacao-interna`
Usos:
- quando a gerência precisa mobilizar mais de uma área
- alinhamento entre recepção, secretaria, coordenação, atendimento, comercial etc.
- problema transversal da unidade

---

### 8. Regras de roteamento do MVP

#### 8.1 Origem das demandas
Demandas podem nascer de:
- gerentes
- Alf / Anne
- atendimento
- recepção
- relacionamento
- secretaria
- coordenadores locais
- professores
- pais/responsáveis/alunos (indiretamente, via contato recebido)

#### 8.2 Fluxo principal
- gerente → qualquer frente da unidade que demande ação
- gerente → pais/alunos diretamente, quando necessário
- gerente → pedagógico, quando o caso exigir apoio educacional
- gerente → comercial, financeiro, marketing, quando houver articulação necessária
- operação da unidade → gerente, quando houver conflito, risco ou necessidade de destrave

#### 8.3 Regra de autoridade
O gerente é uma camada formal de articulação ampla da unidade.
Não precisa “pedir permissão” para existir no fluxo.
Sua função é precisamente coordenar, acompanhar, cobrar e integrar.

---

### 9. Diferença entre Gerência e Pedagógico

Isso precisa ficar claro desde o começo.

#### Pedagógico
Olha para:
- qualidade pedagógica
- professores no eixo pedagógico
- jornada de aprendizado
- School x Kids
- coordenação + assistentes + mentores

#### Gerência
Olha para:
- saúde relacional da unidade
- retenção
- experiência do aluno/família
- atendimento e recepção
- conflitos humanos da jornada
- articulação entre áreas

Resumo:

> **Pedagógico** cuida da qualidade pedagógica.
> **Gerência** cuida da saúde relacional e operacional da unidade.

---

### 10. Hipótese de modelagem no motor do LA Organizer

A Sprint 20 deve reaproveitar a mesma base replicável criada na Sprint 15 e expandida nas sprints seguintes.

#### Estrutura prevista
- novo departamento: `gerencia`
- request types da Gerência
- responsáveis por unidade
- manutenção do ponto de entrada em `/mais/operacoes`

#### Decisão importante
O MVP da Gerência **não precisa de tela nova**.
Ele entra como camada do motor atual.

O foco é:
- taxonomia
- autoridade transversal
- skill correta
- roteamento
- piloto real

---

### 11. Hipótese de seed inicial

#### Departamento
- `gerencia`

#### Request types
- `risco-de-evasao`
- `recuperacao-de-aluno`
- `alinhamento-com-responsavel`
- `problema-de-atendimento`
- `experiencia-da-unidade`
- `negociacao-relacional`
- `pendencia-gerencial`
- `articulacao-interna`

#### Responsáveis estruturais
- Jereh = Campo Grande
- Clayton = Recreio
- Krissya = Barra

---

### 12. Hipótese de skill `gerencia.md`

A skill da Gerência deve ensinar o TOM a:
- entender o gerente como articulador transversal da unidade
- saber quando o caso é relacional/gerencial e não pedagógico
- distinguir retenção de comercial puro
- saber quando acionar pais/responsáveis
- saber quando mobilizar recepção, secretaria, atendimento, comercial, marketing, financeiro ou coordenação pedagógica
- evitar confundir demanda gerencial com evento ou demanda pedagógica

#### Exemplos de comandos esperados
- “esse aluno está em risco de evasão”
- “fala com a Krissya sobre esse pai insatisfeito”
- “abre uma demanda de recuperação desse aluno”
- “isso aqui virou problema de atendimento”
- “aciona a gerência da unidade pra resolver essa experiência”
- “preciso articular recepção, secretaria e coordenação nesse caso”

---

### 13. Piloto inicial recomendado

Primeiro piloto controlado com:
- Jereh
- Clayton
- Krissya

Com interação progressiva com:
- recepção
- atendimento
- relacionamento
- secretaria
- coordenação local
- pedagógico, quando necessário

#### Meta do piloto
Validar:
- se a taxonomia cobre os principais casos
- se a Gerência está sendo distinguida corretamente do Pedagógico
- se a autoridade transversal está bem modelada
- se o fluxo de retenção/recuperação funciona
- se os problemas de experiência da unidade são roteados corretamente

---

### 14. Relação com as próximas sprints

Roadmap consolidado:
1. **Sprint 18** — Integridade de Agenda e Execução
2. **Sprint 19** — Pedagógico
3. **Sprint 20** — Gerência
4. **Auditoria obrigatória de Eventos**
5. **Só depois** sprint específica de Eventos

#### Decisão importante sobre Eventos
Eventos continuam dependendo de auditoria prévia.
A Gerência pode tocar casos relacionados à experiência de eventos, mas isso **não substitui** a futura auditoria do motor de Eventos.

---

### 15. Resumo executivo

A Sprint 20 da Gerência deve formalizar uma camada de governança relacional da unidade.

Ela exige:
- pessoas reais por unidade
- autoridade transversal clara
- taxonomia de retenção/experiência/atendimento
- skill específica
- piloto controlado

O núcleo do MVP não é apenas o atendimento.

> O núcleo do MVP da Gerência é **articulação relacional + cobrança transversal + saúde da experiência da unidade**.
