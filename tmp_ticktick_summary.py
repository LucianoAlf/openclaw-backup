import os, requests, json
from datetime import datetime
from zoneinfo import ZoneInfo
base='https://api.ticktick.com/open/v1'
token=os.environ.get('TICKTICK_TOKEN')
headers={'Authorization': f'Bearer {token}', 'Content-Type':'application/json'}
projects=[('67158c51db647de6536f46dc','Contas Pessoais'),('643c0518525047536b6594d0','Pessoal Alf'),('643c0518525047536b6594d1','Trabalho Operacional'),('67fbc6398f08b12415f506c4','Mentorias')]
sp=ZoneInfo('America/Sao_Paulo')
today=datetime(2026,5,30,tzinfo=sp).date()
print('TODAY_LOCAL', today)

def conv(s):
    if not s:
        return None
    s=s.replace('Z','+0000')
    for fmt in ('%Y-%m-%dT%H:%M:%S.%f%z','%Y-%m-%dT%H:%M:%S%z'):
        try:
            return datetime.strptime(s, fmt).astimezone(sp)
        except Exception:
            pass
    return None

for pid,pname in projects:
    data=requests.get(f'{base}/project/{pid}/data', headers=headers, timeout=30).json()
    tasks=data.get('tasks',[])
    print(f'\n## {pname} ({pid}) count={len(tasks)}')
    for t in tasks:
        due_dt=conv(t.get('dueDate'))
        comp_dt=conv(t.get('completedTime'))
        status=t.get('status')
        overdue = (status != 2 and due_dt and due_dt.date() < today)
        due_today = (due_dt and due_dt.date() == today)
        completed_today = (comp_dt and comp_dt.date() == today)
        print(json.dumps({
            'title': t.get('title'),
            'status': status,
            'due_local': due_dt.isoformat() if due_dt else None,
            'completed_local': comp_dt.isoformat() if comp_dt else None,
            'repeatFlag': t.get('repeatFlag'),
            'isAllDay': t.get('isAllDay'),
            'priority': t.get('priority'),
            'overdue': overdue,
            'due_today': due_today,
            'completed_today': completed_today,
            'project': pname,
        }, ensure_ascii=False))
