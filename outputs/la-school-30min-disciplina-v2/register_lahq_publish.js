require('dotenv').config({ path: '/home/lahq/.env' });
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);
const OFFICE_ID = 'a1b2c3d4-0001-4000-8000-000000000001';
const TINA_ID = 'c3d4e5f6-0007-4000-8000-000000000007';

const brand = 'la-music-school';
const localDir = '/tmp/lahq-30min-disciplina-v2';
const parentTaskId = crypto.randomUUID();

const legenda = `30 minutos por dia podem mudar completamente sua relação com o instrumento — se você souber o que fazer com esse tempo.

O erro não é estudar pouco.
É estudar sem direção, repetir tudo no automático e achar que evolução vem só de “tocar mais”.

Salva esse mapa e testa por 7 dias:

• 5 min pra aquecer e definir o alvo
• 10 min de técnica lenta e limpa
• 10 min aplicando em música real
• 5 min anotando erro, progresso e próximo passo

Quer evoluir com direção de verdade?
Agende uma aula experimental na LA Music School.

Link na bio. 🎸`;

const hashtags = [
  'LAMusicSchool',
  'AulaDeMusica',
  'EstudoMusical',
  'RotinaDeEstudo',
  'Guitarra',
  'Violao',
  'Canto',
  'Bateria',
  'MusicaRJ',
  'EscolaDeMusica',
  'CampoGrandeRJ',
  'RecreioDosBandeirantes',
  'BarraDaTijuca'
];

(async () => {
  const files = fs.readdirSync(localDir)
    .filter(f => /^la-school-30min-v2-\d{2}\.png$/.test(f))
    .sort();
  if (files.length !== 8) throw new Error(`Esperava 8 PNGs, achei ${files.length}`);

  const { error: parentErr } = await supabase.from('tasks').insert({
    id: parentTaskId,
    agent_id: TINA_ID,
    type: 'carousel',
    status: 'completed',
    brand,
    input: {
      tema: 'Rotina de estudo de 30 minutos por dia para músicos',
      briefing: 'Carrossel aprovado pelo Alf para publicação no Instagram @lamusicschool',
      total_slides: 8,
    },
    output: { source: 'alfredo-openclaw-local' },
  });
  if (parentErr) throw new Error(`Insert parent task: ${parentErr.message}`);

  const fileUrls = [];
  for (const f of files) {
    const slide = f.match(/-(\d{2})\.png$/)[1];
    const storagePath = `${brand}/${parentTaskId}/slide-${slide}.png`;
    const buf = fs.readFileSync(path.join(localDir, f));
    const { error } = await supabase.storage.from('outputs').upload(storagePath, buf, {
      contentType: 'image/png',
      upsert: true,
    });
    if (error) throw new Error(`Upload ${f}: ${error.message}`);
    const { data } = supabase.storage.from('outputs').getPublicUrl(storagePath);
    fileUrls.push(data.publicUrl);
  }

  const { data: output, error: outErr } = await supabase.from('outputs').insert({
    task_id: parentTaskId,
    office_id: OFFICE_ID,
    type: 'carousel',
    format: 'png',
    brand,
    title: 'Rotina de estudo — 30 min todo dia',
    theme: 'Rotina de estudo de 30 minutos por dia para músicos',
    file_urls: fileUrls,
    total_slides: fileUrls.length,
    status: 'ready',
    approval_status: 'approved',
    rendered_by: 'alfredo-openclaw-local-v2-1080x1440',
    published: false,
  }).select().single();
  if (outErr) throw new Error(`Insert output: ${outErr.message}`);

  const { data: task, error: taskErr } = await supabase.from('tasks').insert({
    agent_id: TINA_ID,
    parent_task_id: parentTaskId,
    type: 'publishing',
    status: 'pending',
    brand,
    input: { output_id: output.id, legenda, hashtags },
  }).select().single();
  if (taskErr) throw new Error(`Insert task: ${taskErr.message}`);

  console.log(JSON.stringify({ parentTaskId, outputId: output.id, taskId: task.id, fileUrls }, null, 2));
})();
