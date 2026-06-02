const fs=require('fs');
const env=fs.readFileSync('/root/.openclaw/workspace/.env','utf8');
const envv=n=>env.match(new RegExp('^'+n+'=(.+)$','m'))?.[1]?.trim();
const url=envv('LAREPORT_SUPABASE_URL'); const key=envv('LAREPORT_SUPABASE_SERVICE_ROLE')||envv('LAREPORT_SUPABASE_ANON_KEY');
async function get(path){ const r=await fetch(`${url}/rest/v1/${path}`,{headers:{apikey:key,Authorization:`Bearer ${key}`}}); const t=await r.text(); if(!r.ok) throw new Error(path+' => '+r.status+' '+t.slice(0,1000)); return JSON.parse(t); }
(async()=>{
 console.log('\nUNIDADES'); console.table(await get('unidades?select=id,codigo,nome&order=id'));
 const CG='2ec861f6-023f-4d7b-9927-3960ad8c2a92';
 console.log('\nDADOS MENSAIS CG MAI/2026'); console.table(await get(`dados_mensais?select=*&ano=eq.2026&mes=eq.5&unidade_id=eq.${CG}`));
 console.log('\nVW KPI GESTAO MAI/2026 CG'); try{ console.table(await get(`vw_kpis_gestao_mensal?select=*&ano=eq.2026&mes=eq.5&unidade_id=eq.${CG}`)); }catch(e){ console.error(e.message); }
 console.log('\nVW DASHBOARD UNIDADE CG'); try{ console.table(await get(`vw_dashboard_unidade?select=*&unidade_id=eq.${CG}`)); }catch(e){ console.error(e.message); }
})();
