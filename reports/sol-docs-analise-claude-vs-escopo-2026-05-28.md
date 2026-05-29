# Análise — Documentos SOUL/AGENTS/PERMISSOES da Sol

Data: 2026-05-28
Base comparada:

- Auditoria runtime SSH da Sol
- Docs de capacidades enviados pelo Alf
- Escopo triplo: Adm/Gestão + Sucesso do Aluno + Relacionamento
- PRD Segundo Cérebro LAHQ v2.2
- Propostas Claude: `SOUL.md`, `AGENTS.md`, `PERMISSOES.md`

## Veredito

Os três documentos estão bons e muito melhores que os arquivos atuais da Sol na VPS. Eles já capturam a identidade principal: **Sol como Farmer AI**, com 3 modos e guardrails claros.

Mas ainda não estão completos para virar versão final. Falta incorporar parte do escopo real que Alf descreveu, principalmente:

1. relacionamento com cliente;
2. gestão/admin/reports mais ampla;
3. comunidades WhatsApp;
4. indicadores e protocolos operacionais;
5. separação técnica mais dura entre Sol Atendimento, Sol BI e Sol Operadora;
6. matriz de escalação com gerentes e responsáveis reais.

## Pontos fortes dos documentos

### SOUL.md

- Define bem a Sol como Farmer AI, não chatbot.
- Traz a frase certa: cuidar dos alunos para liberar humanos para conexão real.
- Os 3 modos estão corretos: Atendimento, Farmer/CS, BI/Admin.
- Incorpora valores LA Music: Paixão, Empatia, Coragem, Excelência.
- Traz boa regra-mãe: “Esse aluno está sendo cuidado como deveria?”
- Diferencia tom para aluno, farmer, gerente e Alf.
- Tem guardrails claros.

### AGENTS.md

- Estrutura operacional boa.
- Lista ações sem aprovação por modo.
- Bloqueios importantes aparecem.
- Traz fontes de verdade e MCP read-only.
- Corrige parte do problema do AGENTS atual, que estava quebrado.

### PERMISSOES.md

- Boa matriz inicial de leitura/escrita/aprovação.
- Alinha Sol ao PRD: futuro `lahq-empresa-brain`, escreve só `inbox/sol/`.
- Separa worker BI das consultas read-only.
- Define relação com outros agentes.

## Lacunas importantes

### 1. Escopo Relacionamento com Cliente ficou fraco

O escopo enviado pelo Alf inclui, mas os 3 docs não incorporam bem:

- pré-atendimento e informações rápidas;
- FAQ automatizado;
- confirmação de matrícula e kit boas-vindas;
- lembrete de aula experimental 24h/1h antes;
- aviso de mudança de horário/sala;
- comunicados gerais;
- reativação de ex-alunos 3–6 meses;
- indicação premiada;
- atualização cadastral a cada 6 meses;
- comprovante e segunda via via Asaas.

Isso precisa entrar em `AGENTS.md` e talvez em um `RELACIONAMENTO.md`/skill própria.

### 2. Escopo Adm/Gestão/Reports está resumido demais

Faltam explicitamente:

- relatórios diários, semanais e mensais;
- resumo executivo diário com ativos, matrículas, evasões, renovações, inadimplência;
- alerta de metas em risco por conversão, retenção, ticket médio;
- aviso prévio por unidade;
- turma vazia/subutilizada;
- ocupação de salas;
- vencimento de documentos;
- fechamento mensal assistido;
- checklist operacional com % de conclusão.

O AGENTS cita parte, mas não tudo. Para a expectativa do Alf, precisa entrar.

### 3. Escopo Sucesso do Aluno ainda não cobre tudo

Faltam ou estão pouco explícitos:

- migração excessiva de curso/instrumento;
- aluno silencioso;
- NPS trimestral segmentado por unidade/professor/tempo de casa;
- mensagens sazonais;
- aniversário de matrícula / “aniversário LA”;
- sugestão de repertório/atividade via LA Journey;
- monitoramento de satisfação do responsável;
- pesquisa de evasão pós-saída;
- briefing diário do professor com contexto do que o aluno estuda.

### 4. Comunidades WhatsApp não entrou

Já existe memória `sol-atendimento.md` sobre a Sol nas comunidades WhatsApp.

Falta incluir:

- cruzar membros da comunidade com alunos/responsáveis do banco;
- identificar quem não está na comunidade;
- gerar lista para equipe ou mensagem aprovada;
- objetivo: centralizar comunicados e reduzir dependência da memória humana.

Isso é módulo operacional relevante de comunicação/retensão.

### 5. Escalação precisa incluir gerentes reais

SOUL fala farmer + gerente, mas não nomeia gerentes.

Pelo PRD Segundo Cérebro/Tom/Gerência, gerentes relevantes:

- Jereh — Campo Grande;
- Clayton — Recreio/interino;
- Krissya — Barra e líder comercial.

Também aparece regra de que Andreza é CC obrigatório em notificações operacionais no PRD. Precisa confirmar se vale para Sol antes de colocar como regra dura.

### 6. Jéssica/Fabíola precisam ser validadas

Os docs dizem Jéssica e Fabíola como sucesso do cliente. Precisa confirmar nomes/papéis atuais com Alf/Hugo antes de virar regra canônica. Alf mencionou Jéssica; Fabíola aparece no Claude, mas precisa validação.

### 7. “Pode fazer sem aprovação” está ambicioso demais para fase atual

AGENTS/PERMISSOES dizem que pode fazer sem aprovação:

- cobrança D+1/D+3;
- alertas automáticos;
- briefing professor;
- pesquisas;
- resumo executivo diário;
- alertas de metas.

Conceitualmente ok, mas na fase atual deveria haver níveis:

- Fase 0: dry-run/relatório;
- Fase 1: envio interno para equipe;
- Fase 2: envio externo padronizado;
- Fase 3: automações multimodais/vision.

Sem isso, o documento parece autorizar operação plena antes de validação.

### 8. LGPD e consentimento precisam entrar mais forte

Falta detalhar:

- retenção de áudios/imagens/transcrições;
- quem pode ver mídia/documentos;
- não enviar dados de aluno em grupo aberto;
- mascaramento de CPF/telefone/dados financeiros;
- logs de acesso;
- direito de remoção/correção.

### 9. Human takeover / pausa de automação

Docs citam pausar mensagens quando farmer assume, mas deveria virar regra forte:

- se humano assumir conversa, Sol não envia automação concorrente;
- se ticket está aberto, Sol só sugere internamente;
- se aluno respondeu cobrança ou reclamação, suspender sequência automática até classificação.

### 10. Controle de duplicidade e janela de silêncio

Falta regra para evitar Sol mandar mensagens demais:

- limite de mensagens por aluno/dia;
- evitar cobrança + falta + NPS no mesmo dia;
- prioridade de comunicação: crise/cancelamento > pagamento > falta > relacionamento > marketing;
- janela de silêncio fora do horário, salvo urgência interna.

### 11. BI/Admin precisa de camada de confiança

Faltam regras de confiabilidade:

- sempre declarar critério usado em relatório interno;
- diferenciar dado confirmado vs estimado vs inconsistente;
- quando divergência aparece, escalar para Hugo antes de enviar relatório executivo;
- não salvar playbook como “approved” só por inferência sem validação humana, exceto quando Hugo/Alf confirma.

### 12. Shell/exec ainda está permissivo

PERMISSOES e AGENTS dizem que exec precisa aprovação do Hugo, mas openclaw runtime tem `exec security full`.

Recomendação:

- documentar que Sol não usa exec em atendimento/farmer;
- exec somente sessão técnica/admin;
- ideal: agente separado ou modo técnico separado;
- registrar uso de exec em log/diário.

### 13. Faltam critérios de qualidade de resposta

Para Sol BI/Admin:

- conclusão na primeira linha;
- separação por unidade;
- números com data de referência;
- apontar fonte/view/tabela para admin, mas esconder tecnicismo de usuários comuns;
- não responder “não sei” antes de investigar schema/read-only.

Isso já está na memória atual da Sol, mas não entrou nos documentos Claude.

## O que eu adicionaria nos documentos

### No SOUL.md

Adicionar:

- Sol não substitui relacionamento humano; ela protege a capacidade humana de se relacionar.
- “A Sol observa o invisível”: aluno silencioso, queda de presença, atraso recorrente, falta de interação.
- Módulo Relacionamento com Cliente como terceira perna real, não só atendimento.
- Comunidades WhatsApp como parte de pertencimento/comunicação.
- Frase: “Se a mensagem pode soar fria em um momento difícil, escala ou reescreve.”
- Regra anti-spam: cuidar não é bombardear.

### No AGENTS.md

Adicionar seções:

1. Fases de ativação: dry-run → interno → externo aprovado → automação plena.
2. Relacionamento com Cliente.
3. Adm/Gestão/Reports completo.
4. Sucesso do Aluno completo.
5. Comunidades WhatsApp.
6. Human takeover.
7. Controle de frequência de mensagens.
8. BI/Admin: critério, fonte e confiança.
9. Memória/inbox: o que salva e onde.

### No PERMISSOES.md

Adicionar:

- matriz por público: aluno, responsável, professor, farmer, gerente, Hugo, Alf;
- matriz por fase de ativação;
- dados permitidos/proibidos por canal;
- escrita em GitHub: somente `inbox/sol/` no futuro;
- regra de PR/aprovação para alteração de processo oficial;
- confirmação sobre Jéssica/Fabíola/gerentes/farmers.

## Itens a confirmar com Alf/Hugo antes de aplicar

1. Fabíola é aprovadora real junto com Jéssica?
2. Quem são as farmers oficiais por unidade hoje?
3. Quem recebe inadimplência D+7: farmer da unidade, financeiro, gerente ou todos?
4. Andreza deve ser CC obrigatório nas notificações da Sol também ou só em outro contexto operacional?
5. Sol pode enviar cobrança externa D+1/D+3 agora ou primeiro em dry-run?
6. Sol pode enviar briefing direto a professores agora ou primeiro para coordenação validar?
7. Quais mensagens podem sair por áudio?
8. Asaas/segunda via já existe tecnicamente ou é futuro?
9. Chatwoot existe nesse fluxo ou o runtime real é Telegram/WhatsApp/UAZAPI/Supabase?
10. Health Score já existe calculado ou precisa ser desenhado?

## Recomendação

Não aplicar os três arquivos exatamente como estão. Usar como base e gerar uma versão v2 consolidada:

- `SOUL.md` v2 — identidade e alma da Sol;
- `AGENTS.md` v2 — operação por modos, fases e guardrails;
- `PERMISSOES.md` v2 — matriz de permissões e escalação;
- criar depois skills/processos separados: `sol-atendimento`, `sol-cobranca`, `sol-satisfacao`, `sol-frequencia`, `sol-bi-admin`, `sol-comunidades-whatsapp`.
