# Contrato LA Music — extração para Sol

Data: 2026-05-28
Fonte: contrato padrão LA Music Kids / LA Music School, modelo nº 2363/2023.

## Arquivos criados

- Contrato original recebido salvo em: `memory/projects/sol/contratos/contrato-la-music-normalizado-2023.md`
- Regras contratuais limpas/operacionais criadas em: `memory/projects/sol/REGRAS_CONTRATUAIS.md`

## Tratamento de dados sensíveis

O contrato recebido contém dados pessoais de exemplo real. Esses dados **não foram levados** para o arquivo operacional `REGRAS_CONTRATUAIS.md`.

O arquivo operacional contém apenas regras de negócio.

## Regras críticas extraídas

### Módulo/aulas
- Módulo garante 40 aulas.
- Aula regular: 1x por semana, 50 minutos.
- Atraso do aluno não estende aula.
- Feriados/recessos não reduzem as 40 aulas.

### Pagamento
- À vista ou parcelado.
- Cartão recorrente via Emusys ou cheques.
- Atraso: multa de 2% + juros de 1% ao mês pro rata.
- Atraso pode implicar perda de desconto.
- Atraso superior a 30 dias pode gerar rescisão automática/suspensão.

### Reposição
- Falta do aluno só gera reposição por motivo de saúde com atestado.
- Reposição deve acontecer em até 30 dias corridos da falta.
- Reposição agendada não pode ser desmarcada; falta na reposição = aula ministrada.
- Faltas sem atestado não geram reposição contratual.
- LA Pass prevê 2 reposições extras por módulo para faltas não médicas.

### Troca de horário
- Solicitação à secretaria.
- Só efetiva após mínimo de 10 aulas ininterruptas.
- Depende de disponibilidade.
- Contratante continua pagando enquanto aguarda novo horário.

### Cancelamento/rescisão
- Solicitação pode ocorrer a qualquer momento.
- Formalização presencialmente na secretaria ou por e-mail.
- Não é aceita via WhatsApp.
- Parcelas vencidas devem estar quitadas.
- Sem comunicação formal, cobrança continua mesmo sem frequência.
- Aviso prévio: 2 parcelas — mês atual + mês seguinte.
- Durante aviso prévio, aluno pode frequentar aulas.
- Pagamento à vista: restituição proporcional após aviso prévio, taxa de 15% sobre total, prazo 45 dias após fim do aviso prévio.

### Trancamento
- 1 vez por pacote de 40 aulas.
- Máximo 30 dias corridos.
- Solicitação por escrito e presencialmente na secretaria.
- Parcela do mês continua devida.
- Acima de 30 dias, rescisão conforme aviso prévio.

### Renovação/reajuste
- Renovação automática por períodos de 40 aulas.
- Escola notifica com mínimo de 30 dias.
- Para não renovar, contratante avisa com mínimo de 15 dias.
- Silêncio = aceitação tácita.
- Reajuste comunicado com mínimo de 30 dias.

### Direito de imagem
- Contrato autoriza uso de imagem, mas autorização pode ser revogada por escrito.
- Recusa/revogação não impede participação em atividades/eventos.

## Skills locais atualizadas

Foram atualizadas localmente, ainda não instaladas na VPS nesta etapa:

- `memory/projects/sol/skills-alfredo/sol-atendimento/SKILL.md`
- `memory/projects/sol/skills-alfredo/sol-cobranca/SKILL.md`
- `memory/projects/sol/skills-alfredo/sol-frequencia/SKILL.md`
- `memory/projects/sol/skills-alfredo/sol-sucesso-aluno/SKILL.md`

Essas skills passaram a referenciar `REGRAS_CONTRATUAIS.md`.

## Recomendação

Antes de instalar na VPS, validar com Alf se:

1. o contrato de 2023 continua sendo regra oficial atual;
2. a régua operacional de cobrança (D+1/D+5/D+10/D+15) convive com regra contratual de 30 dias;
3. LA Pass de 2 reposições extras ainda está vigente para todos os planos;
4. cancelamento realmente deve seguir “não aceita WhatsApp” como regra atual operacional;
5. trancamento presencial ainda é exigência atual.
