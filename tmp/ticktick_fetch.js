const token = process.env.TICKTICK_TOKEN;
const id = process.argv[2];
(async()=>{
  const r = await fetch(`https://api.ticktick.com/open/v1/project/${id}/data`, {headers:{Authorization:`Bearer ${token}`}});
  const t = await r.text();
  console.log(r.status);
  console.log(t.slice(0,4000));
})().catch(e=>{console.error(e); process.exit(1);});
