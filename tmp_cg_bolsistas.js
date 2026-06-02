const fs=require('fs');
const env=fs.readFileSync('/root/.openclaw/workspace/.env','utf8');
const envv=n=>env.match(new RegExp('^'+n+'=(.+)$','m'))?.[1]?.trim();
const url=envv('LAREPORT_SUPABASE_URL'); const key=envv('LAREPORT_SUPABASE_SERVICE_ROLE')||envv('LAREPORT_SUPABASE_ANON_KEY');
async function get(path){ const r=await fetch(`${url}/rest/v1/${path}`,{headers:{apikey:key,Authorization:`Bearer ${key}`}}); const t=await r.text(); if(!r.ok) throw new Error(r.status+' '+t); return JSON.parse(t); }
(async()=>{
 const CG='2ec861f6-023f-4d7b-9927-3960ad8c2a92';
 const alunos=await get(`alunos?select=id,nome,status,is_segundo_curso,tipo_matricula_id,valor_parcela,cursos:curso_id(nome,is_projeto_banda),tipos_matricula:tipo_matricula_id(codigo,nome)&unidade_id=eq.${CG}&status=in.(ativo,trancado,aviso_previo)&tipo_matricula_id=in.(3,4)&order=nome&limit=1000`);
 const pessoa={};
 for(const a of alunos){
  pessoa[a.nome]??={nome:a.nome,tipos:new Set(),linhas:0,cursos:[]};
  pessoa[a.nome].tipos.add(a.tipos_matricula?.codigo||a.tipo_matricula_id);
  pessoa[a.nome].linhas++;
  pessoa[a.nome].cursos.push(`${a.cursos?.nome||'—'} R$${a.valor_parcela ?? 'NULL'} segundo=${a.is_segundo_curso} banda=${a.cursos?.is_projeto_banda}`);
 }
 const rows=Object.values(pessoa).map(p=>({nome:p.nome,tipos:[...p.tipos].join(','),linhas:p.linhas,cursos:p.cursos.join(' | ')}));
 console.log('registros',alunos.length,'pessoas',rows.length);
 console.table(rows);
 const counts={};
 for(const r of rows){ counts[r.tipos]=(counts[r.tipos]||0)+1; }
 console.log(counts);
})();
