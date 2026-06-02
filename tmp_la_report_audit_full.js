const fs=require('fs');
const env=fs.readFileSync('/root/.openclaw/workspace/.env','utf8');
function envv(name){ return env.match(new RegExp('^'+name+'=(.+)$','m'))?.[1]?.trim(); }
const url=envv('LAREPORT_SUPABASE_URL');
const key=envv('LAREPORT_SUPABASE_SERVICE_ROLE')||envv('LAREPORT_SUPABASE_ANON_KEY');
async function get(path){
 const r=await fetch(`${url}/rest/v1/${path}`,{headers:{apikey:key,Authorization:`Bearer ${key}`,'Prefer':'count=exact'}});
 const text=await r.text();
 if(!r.ok) throw new Error(r.status+' '+text.slice(0,1000));
 return JSON.parse(text);
}
async function getPaged(base, pageSize=1000){
 let out=[];
 for(let from=0;;from+=pageSize){
  const sep=base.includes('?')?'&':'?';
  const rows=await get(`${base}${sep}limit=${pageSize}&offset=${from}`);
  out.push(...rows);
  if(rows.length<pageSize) break;
 }
 return out;
}
(async()=>{
 const alunos=await getPaged('alunos?select=id,nome,status,is_segundo_curso,tipo_matricula_id,valor_parcela,curso_id,unidade_id,cursos:curso_id(nome,is_projeto_banda),tipos_matricula:tipo_matricula_id(codigo,nome,conta_como_pagante,entra_ticket_medio),unidades:unidade_id(codigo,nome)&status=in.(ativo,trancado,aviso_previo)',1000);
 console.log('TOTAL fetched', alunos.length);
 const byUnidade={}; const unique={};
 for(const a of alunos){
  const u=a.unidades?.codigo||a.unidade_id;
  byUnidade[u]??={registros:0,pessoas:new Set(),pessoasNaoSegundo:new Set(),pagantesPessoa:new Set(),pagantesRegistros:0,bolsistasRegistros:0,bolsistasPessoa:new Set(),bandaRegistros:0,bandaPessoa:new Set(),segundoRegistros:0,valorPositivoRegistros:0};
  const b=byUnidade[u];
  b.registros++; b.pessoas.add(a.nome);
  if(!a.is_segundo_curso) b.pessoasNaoSegundo.add(a.nome);
  if(a.tipos_matricula?.conta_como_pagante && Number(a.valor_parcela)>0) { b.pagantesRegistros++; b.pagantesPessoa.add(a.nome); }
  const bols=['BOLSISTA_INT','BOLSISTA_PARC'].includes(a.tipos_matricula?.codigo)||[3,4].includes(a.tipo_matricula_id);
  if(bols){ b.bolsistasRegistros++; b.bolsistasPessoa.add(a.nome); }
  if(a.cursos?.is_projeto_banda){ b.bandaRegistros++; b.bandaPessoa.add(a.nome); }
  if(a.is_segundo_curso) b.segundoRegistros++;
  if(Number(a.valor_parcela)>0) b.valorPositivoRegistros++;
 }
 const printable={};
 for(const [u,b] of Object.entries(byUnidade)) printable[u]={
  registros:b.registros,
  pessoas:b.pessoas.size,
  pessoasNaoSegundo:b.pessoasNaoSegundo.size,
  pagantesPessoa:b.pagantesPessoa.size,
  pagantesRegistros:b.pagantesRegistros,
  bolsistasRegistros:b.bolsistasRegistros,
  bolsistasPessoa:b.bolsistasPessoa.size,
  bandaRegistros:b.bandaRegistros,
  bandaPessoa:b.bandaPessoa.size,
  segundoRegistros:b.segundoRegistros,
  valorPositivoRegistros:b.valorPositivoRegistros
 };
 console.table(printable);
})();
