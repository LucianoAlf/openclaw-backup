const fs=require('fs');
const env=fs.readFileSync('/root/.openclaw/workspace/.env','utf8');
function envv(name){ return env.match(new RegExp('^'+name+'=(.+)$','m'))?.[1]?.trim(); }
const url=envv('LAREPORT_SUPABASE_URL')||envv('SUPABASE_URL')||envv('VITE_SUPABASE_URL');
const key=envv('LAREPORT_SUPABASE_SERVICE_ROLE')||envv('LAREPORT_SUPABASE_ANON_KEY')||envv('SUPABASE_SERVICE_ROLE_KEY')||envv('SUPABASE_ANON_KEY')||envv('VITE_SUPABASE_ANON_KEY');
async function get(path){
 const r=await fetch(`${url}/rest/v1/${path}`,{headers:{apikey:key,Authorization:`Bearer ${key}`,'Prefer':'count=exact'}});
 const text=await r.text();
 if(!r.ok){throw new Error(r.status+' '+text.slice(0,500));}
 return JSON.parse(text);
}
(async()=>{
 const tipos=await get('tipos_matricula?select=id,codigo,nome,conta_como_pagante,entra_ticket_medio&order=id');
 console.log('\nTIPOS_MATRICULA'); console.table(tipos);
 const cursos=await get('cursos?select=id,nome,is_projeto_banda,ativo&is_projeto_banda=eq.true&order=nome');
 console.log('\nCURSOS is_projeto_banda=true:', cursos.length); console.table(cursos.map(c=>({id:c.id,nome:c.nome,ativo:c.ativo,is_projeto_banda:c.is_projeto_banda})));
 const alunos=await get('alunos?select=id,nome,status,is_segundo_curso,tipo_matricula_id,valor_parcela,curso_id,unidade_id,cursos:curso_id(nome,is_projeto_banda),tipos_matricula:tipo_matricula_id(codigo,nome,conta_como_pagante,entra_ticket_medio),unidades:unidade_id(codigo,nome)&status=in.(ativo,trancado,aviso_previo)&limit=5000');
 console.log('\nALUNOS ATIVOS/TRANCADOS/AVISO:', alunos.length);
 const byTipo={}; const byUnidade={}; const byCursoBanda={};
 for(const a of alunos){
  const t=a.tipos_matricula?.codigo||`id_${a.tipo_matricula_id}`;
  byTipo[t]=(byTipo[t]||0)+1;
  const u=a.unidades?.codigo||a.unidade_id;
  byUnidade[u]??={total:0,pagantes_tipo:0,bolsistas:0,banda:0,segundo:0,valorPositivo:0,pagantes_valor_pos:0};
  byUnidade[u].total++;
  if(a.tipos_matricula?.conta_como_pagante) byUnidade[u].pagantes_tipo++;
  if(['BOLSISTA_INT','BOLSISTA_PARC'].includes(t) || [3,4].includes(a.tipo_matricula_id)) byUnidade[u].bolsistas++;
  if(a.cursos?.is_projeto_banda) byUnidade[u].banda++;
  if(a.is_segundo_curso) byUnidade[u].segundo++;
  if(Number(a.valor_parcela)>0) byUnidade[u].valorPositivo++;
  if(a.tipos_matricula?.conta_como_pagante && Number(a.valor_parcela)>0) byUnidade[u].pagantes_valor_pos++;
  if(a.cursos?.is_projeto_banda){ const k=a.cursos.nome; byCursoBanda[k]=(byCursoBanda[k]||0)+1; }
 }
 console.log('\nBY TIPO'); console.table(byTipo);
 console.log('\nBY UNIDADE raw registros'); console.table(byUnidade);
 console.log('\nBY CURSO BANDA'); console.table(byCursoBanda);
 const bad=alunos.filter(a=>a.cursos?.is_projeto_banda && a.is_segundo_curso);
 console.log('\nBanda ainda com is_segundo_curso=true:', bad.length);
 const sampleBols=alunos.filter(a=>[3,4].includes(a.tipo_matricula_id)||['BOLSISTA_INT','BOLSISTA_PARC'].includes(a.tipos_matricula?.codigo)).slice(0,10).map(a=>({nome:a.nome,unidade:a.unidades?.codigo,curso:a.cursos?.nome,tipo:a.tipos_matricula?.codigo,valor:a.valor_parcela,segundo:a.is_segundo_curso,banda:a.cursos?.is_projeto_banda}));
 console.log('\nAmostra bolsistas'); console.table(sampleBols);
})().catch(e=>{console.error(e);process.exit(1)});
