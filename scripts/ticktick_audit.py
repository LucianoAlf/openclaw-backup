#!/usr/bin/env python3
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from zoneinfo import ZoneInfo
from urllib.request import Request, urlopen

TZ = ZoneInfo('America/Sao_Paulo')
UTC = ZoneInfo('UTC')
BASE = 'https://api.ticktick.com/open/v1'
PROJECTS = {
    'contas': ('67158c51db647de6536f46dc', 'Contas Pessoais'),
    'pessoal': ('643c0518525047536b6594d0', 'Pessoal Alf'),
    'trabalho': ('643c0518525047536b6594d1', 'Trabalho Operacional'),
    'mentorias': ('67fbc6398f08b12415f506c4', 'Mentorias'),
}

@dataclass
class TaskView:
    project_key: str
    project_name: str
    title: str
    status: int
    local_date: Optional[str]
    local_time: Optional[str]
    raw_due: Optional[str]
    raw_start: Optional[str]


def load_token() -> str:
    env_path = Path('/root/.openclaw/workspace/.env')
    for line in env_path.read_text().splitlines():
        if line.startswith('TICKTICK_TOKEN='):
            token = line.split('=', 1)[1].strip()
            if token:
                return token
    raise RuntimeError('TICKTICK_TOKEN ausente em /root/.openclaw/workspace/.env')


def fetch_project(project_id: str, token: str) -> dict:
    req = Request(f'{BASE}/project/{project_id}/data', headers={'Authorization': f'Bearer {token}'})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def parse_dt(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    for fmt in ('%Y-%m-%dT%H:%M:%S.%f%z', '%Y-%m-%dT%H:%M:%S%z'):
        try:
            return datetime.strptime(value, fmt).astimezone(TZ)
        except ValueError:
            continue
    if len(value) == 10:
        return datetime.strptime(value, '%Y-%m-%d').replace(tzinfo=TZ)
    raise ValueError(f'Data inválida: {value}')


def normalize(task: dict, project_key: str, project_name: str) -> TaskView:
    due = parse_dt(task.get('dueDate'))
    start = parse_dt(task.get('startDate'))
    chosen = due or start
    return TaskView(
        project_key=project_key,
        project_name=project_name,
        title=task.get('title', ''),
        status=int(task.get('status', 0)),
        local_date=chosen.strftime('%Y-%m-%d') if chosen else None,
        local_time=chosen.strftime('%H:%M') if chosen and not task.get('isAllDay') else None,
        raw_due=task.get('dueDate'),
        raw_start=task.get('startDate'),
    )


def collect() -> List[TaskView]:
    token = load_token()
    out: List[TaskView] = []
    for key, (pid, name) in PROJECTS.items():
        data = fetch_project(pid, token)
        for task in data.get('tasks', []):
            out.append(normalize(task, key, name))
    return out


def report() -> dict:
    now = datetime.now(TZ)
    today = now.date()
    week_end = today + timedelta(days=6)
    tasks = collect()

    def in_range(t: TaskView, start, end):
        if not t.local_date:
            return False
        d = datetime.strptime(t.local_date, '%Y-%m-%d').date()
        return start <= d <= end

    today_items = [t.__dict__ for t in tasks if t.status == 0 and t.local_date == today.isoformat()]
    week_items = [t.__dict__ for t in tasks if t.status == 0 and in_range(t, today, week_end)]
    overdue = [t.__dict__ for t in tasks if t.project_key == 'contas' and t.status == 0 and t.local_date and datetime.strptime(t.local_date, '%Y-%m-%d').date() < today]

    return {
        'generatedAt': now.isoformat(),
        'today': today.isoformat(),
        'weekEnd': week_end.isoformat(),
        'todayItems': today_items,
        'weekItems': week_items,
        'overdueContas': overdue,
    }


if __name__ == '__main__':
    json.dump(report(), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write('\n')
