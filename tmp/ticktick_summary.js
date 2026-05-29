const token = process.env.TICKTICK_TOKEN;
const projects = [
  {id:'69f6081a51b4d58f4ef754d6', name:'🔥 CEO Quest'},
  {id:'643c0518525047536b6594d1', name:'💼 Trabalho Operacional'},
  {id:'67fbc6398f08b12415f506c4', name:'💡 Mentorias'},
  {id:'643c0518525047536b6594d0', name:'🏠 Pessoal Alf'},
  {id:'67158c51db647de6536f46dc', name:'💸 Contas Pessoais'},
  {id:'69f60b5351b4d58f4ef755a4', name:'🎬 Emusys Academy'},
];
const today = '2026-05-28';
function dOnly(s){ return s ? String(s).slice(0,10) : ''; }
(async()=>{
  for (const p of projects) {
    const r = await fetch(`https://api.ticktick.com/open/v1/project/${p.id}/data`, {headers:{Authorization:`Bearer ${token}`}});
    const data = await r.json();
    console.log(`## ${p.name} (${p.id})`);
    const tasks = Array.isArray(data) ? data : (data.tasks || data); 
    // Some APIs return an object with tasks/items; handle both.
    const list = Array.isArray(tasks) ? tasks : [];
    const open = list.filter(t => t.status !== 2);
    const interesting = open.filter(t => dOnly(t.dueDate) <= today || !t.dueDate).slice(0,20);
    console.log(`open=${open.length} interesting=${interesting.length}`);
    for (const t of interesting) {
      console.log(`- [${t.status===2?'x':' '}] ${t.title} | due=${dOnly(t.dueDate)||'—'} | pri=${t.priority ?? '—'} | kind=${t.kind||''}`);
      if (t.items && t.items.length) {
        const openItems = t.items.filter(i=>i.status!==2);
        for (const i of openItems.slice(0,10)) console.log(`  * [ ] ${i.title}`);
      }
    }
  }
})().catch(e=>{console.error(e); process.exit(1);});
