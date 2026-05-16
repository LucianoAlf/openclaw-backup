const fs=require('fs');
const https=require('https');
const text=fs.readFileSync('/root/.openclaw/workspace/.env','utf8');
const token=(text.match(/^TICKTICK_TOKEN=(.+)$/m)||[])[1].trim();
const url='https://api.ticktick.com/open/v1/project/67158c51db647de6536f46dc/data';
const tz='America/Sao_Paulo';
const nowUtc=new Date('2026-05-15T11:30:00Z');
function localYMD(date){
  return new Intl.DateTimeFormat('en-CA',{timeZone:tz,year:'numeric',month:'2-digit',day:'2-digit'}).format(date);
}
function parseTickDate(s){ return s ? new Date(s) : null; }
function addDaysYMD(ymd, days){
  const [y,m,d]=ymd.split('-').map(Number);
  const dt=new Date(Date.UTC(y,m-1,d));
  dt.setUTCDate(dt.getUTCDate()+days);
  return dt.toISOString().slice(0,10);
}
https.get(url,{headers:{Authorization:'Bearer '+token}},res=>{
  let data='';
  res.on('data',d=>data+=d);
  res.on('end',()=>{
    if(res.statusCode!==200){ console.log('STATUS',res.statusCode); console.log(data); return; }
    const obj=JSON.parse(data);
    const today=localYMD(nowUtc);
    const plus7=addDaysYMD(today,7);
    const tasks=obj.tasks.filter(t=>t.status===0).map(t=>{
      const due=parseTickDate(t.dueDate);
      const dueLocal=due?localYMD(due):null;
      return {...t,dueLocal};
    });
    const overdue=tasks.filter(t=>t.dueLocal && t.dueLocal < today).sort((a,b)=>a.dueLocal.localeCompare(b.dueLocal));
    const todayTasks=tasks.filter(t=>t.dueLocal && t.dueLocal === today).sort((a,b)=>a.dueLocal.localeCompare(b.dueLocal));
    const next7=tasks.filter(t=>t.dueLocal && t.dueLocal > today && t.dueLocal <= plus7).sort((a,b)=>a.dueLocal.localeCompare(b.dueLocal));
    console.log(JSON.stringify({today,plus7,overdue:overdue.map(t=>({title:t.title,due:t.dueLocal,content:t.content})),todayTasks:todayTasks.map(t=>({title:t.title,due:t.dueLocal,content:t.content})),next7:next7.map(t=>({title:t.title,due:t.dueLocal,content:t.content}))},null,2));
  });
}).on('error',e=>{console.error('ERR',e); process.exit(1);});
