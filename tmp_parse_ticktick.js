const fs = require('fs');
const data = JSON.parse(fs.readFileSync('/tmp/ticktick_project.json', 'utf8'));
const today = '2026-06-07';
const tz = 'America/Sao_Paulo';
const localDate = iso => new Date(iso).toLocaleDateString('en-CA', { timeZone: tz });
const items = data.tasks
  .filter(t => t.status === 0)
  .map(t => ({ title: t.title, content: t.content || '', date: localDate(t.dueDate), dueDate: t.dueDate, priority: t.priority || 0 }))
  .sort((a, b) => a.date.localeCompare(b.date) || b.priority - a.priority || a.title.localeCompare(b.title));
const overdue = items.filter(x => x.date < today);
const todayItems = items.filter(x => x.date === today);
const next7 = items.filter(x => x.date > today && x.date <= '2026-06-14');
console.log(JSON.stringify({ overdue, todayItems, next7 }, null, 2));
