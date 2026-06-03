const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({path:'/root/.openclaw/workspace/.env'});
require('dotenv').config({path:'/root/.openclaw/workspace/repos/LAperformanceReport/.env'});
const url=process.env.LAREPORT_SUPABASE_URL || process.env.SUPABASE_URL;
const key=process.env.LAREPORT_SUPABASE_SERVICE_ROLE || process.env.SUPABASE_SERVICE_ROLE || process.env.LAREPORT_SUPABASE_ANON_KEY;
const supabase=createClient(url,key,{auth:{persistSession:false}});
const CG='2ec861f6-023f-4d7b-9927-3960ad8c2a92';
async function allRows(query, pageSize=1000){
  let out=[]; for(let from=0;;from+=pageSize){
    const {data,error}=await query.range(from, from+pageSize-1);
    if(error) throw error; out=out.concat(data||[]); if(!data || data.length<pageSize) break;
  } return out;
}
(async()=>{
  console.log('--- vw_kpis_gestao_mensal CG Jun/2026 ---');
  let {data:view,error:e1}=await supabase.from('vw_kpis_gestao_mensal').select('*').eq('unidade_id',CG).eq('ano',2026).eq('mes',6);
  if(e1) console.error(e1); else console.log(JSON.stringify(view,null,2));

  console.log('--- dados_mensais CG Jun/2026 ---');
  let {data:dm,error:e2}=await supabase.from('dados_mensais').select('*').eq('unidade_id',CG).eq('ano',2026).eq('mes',6);
  if(e2) console.error(e2); else console.log(JSON.stringify(dm,null,2));

  const alunos = await allRows(supabase.from('alunos').select('id,nome,status,idade_atual,is_segundo_curso,valor_parcela,data_matricula,data_saida,unidade_id,tipo_matricula_id,curso_id,tipos_matricula(codigo,conta_como_pagante,entra_ticket_medio),cursos(nome,is_projeto_banda)').eq('unidade_id',CG).in('status',['ativo','trancado']).order('nome'));
  const ativosOnly = alunos.filter(a=>a.status==='ativo');
  const ativoTranc = alunos;
  function summarize(rows,label){
    const kids=rows.filter(a=>a.idade_atual!=null && Number(a.idade_atual)<=11);
    const school=rows.filter(a=>a.idade_atual!=null && Number(a.idade_atual)>=12);
    const semIdade=rows.filter(a=>a.idade_atual==null);
    const segundo=rows.filter(a=>a.is_segundo_curso===true);
    const banda=rows.filter(a=>a.tipos_matricula?.codigo==='BANDA' || a.cursos?.is_projeto_banda===true);
    const bolsInt=rows.filter(a=>a.tipos_matricula?.codigo==='BOLSISTA_INT');
    const bolsParc=rows.filter(a=>a.tipos_matricula?.codigo==='BOLSISTA_PARC');
    const pagantes=rows.filter(a=>a.tipos_matricula?.conta_como_pagante===true);
    const pagantesSem2=rows.filter(a=>a.tipos_matricula?.conta_como_pagante===true && a.is_segundo_curso!==true);
    console.log(`--- ${label} ---`);
    console.log({total:rows.length,kids:kids.length,school:school.length,semIdade:semIdade.length,segundo:segundo.length,banda:banda.length,bolsInt:bolsInt.length,bolsParc:bolsParc.length,pagantes:pagantes.length,pagantesSem2:pagantesSem2.length});
    if(semIdade.length) console.table(semIdade.map(a=>({id:a.id,nome:a.nome,status:a.status,idade:a.idade_atual,tipo:a.tipos_matricula?.codigo,curso:a.cursos?.nome,segundo:a.is_segundo_curso,valor:a.valor_parcela})));
  }
  summarize(ativosOnly,'alunos status=ativo');
  summarize(ativoTranc,'alunos status in ativo,trancado');

  console.log('--- movimentacoes_admin jun/CG evasao/nao_renovacao ---');
  const mov = await allRows(supabase.from('movimentacoes_admin').select('id,data,tipo,aluno_id,alunos(nome),motivo_saida_id,motivos_saida(nome),origem,criado_em').eq('unidade_id',CG).gte('data','2026-06-01').lt('data','2026-07-01').in('tipo',['evasao','nao_renovacao']).order('data'));
  console.log('count',mov.length); console.table(mov.map(m=>({data:m.data,tipo:m.tipo,aluno:m.alunos?.nome,motivo:m.motivos_saida?.nome,origem:m.origem,criado:m.criado_em})));

  console.log('--- alunos nomes 5 saídas reais ---');
  const nomes=['Daniel Oliveira dos Santos','Eduardo Knupp Gomes','Heloisa Nogueira Delgado','Hugo Sena da Cruz','Nicolas Faria dos Santos'];
  for(const nome of nomes){
    const {data,error}=await supabase.from('alunos').select('id,nome,status,idade_atual,is_segundo_curso,data_saida,tipo_matricula_id,curso_id,cursos(nome),tipos_matricula(codigo,conta_como_pagante)').eq('unidade_id',CG).ilike('nome',`%${nome}%`);
    if(error) console.error(error); else console.log(nome, data);
  }
})();
