#!/usr/bin/env python3
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
import re

BASE = Path('/root/.openclaw/workspace/memory/governanca')
STREAK = BASE / 'streak.md'
DAILY = BASE / 'daily-log.md'

TZ = timezone(timedelta(hours=-3))
CIRCLE = [
    'quintela','juliana','krissya','yuri','rayan','rose','ana paula','hugo','anne','bianca',
    'matheus','rafael bastos','gustavo','cleiton','kailane','andreza','vitória','vitoria','pet','jereh','clayton'
]
VERBS = [
    'cobra','cobrar','cobrei','cobrado','verifica','verificar','verifiquei','manda','mandar','falar','fala com',
    'cadê','cade','precisa','preciso disso','me mostra','tá pronto','ta pronto','como tá','como ta','feedback',
    'decidi','decidir','defini','fechei','escolhi','alinha','alinhar'
]

def now_local():
    return datetime.now(timezone.utc).astimezone(TZ)

def game_date():
    now = now_local()
    if now.hour < 7:
        now = now - timedelta(days=1)
    return now.strftime('%Y-%m-%d')

def ensure_files():
    BASE.mkdir(parents=True, exist_ok=True)
    if not STREAK.exists():
        STREAK.write_text('# CEO Quest Streak\n\n## Status atual\n- Streak ativo: 0 dias\n- Maior streak histórico: 0 dias\n- Última quebra: —\n- Última pausa: —\n\n## Histórico diário\n\n| Data | Status | Streak | Evidência |\n|---|---|---:|---|\n')
    if not DAILY.exists():
        DAILY.write_text('# Log Diário — CEO Quest\n')

def parse_streak_value(text, label):
    m = re.search(rf'- {re.escape(label)}: (.+)', text)
    return m.group(1).strip() if m else None

def set_line(text, label, value):
    pattern = rf'- {re.escape(label)}: .*'
    repl = f'- {label}: {value}'
    if re.search(pattern, text):
        return re.sub(pattern, repl, text)
    return text

def ensure_day_block(today):
    text = DAILY.read_text() if DAILY.exists() else '# Log Diário — CEO Quest\n'
    if f'## {today}' not in text:
        text += f'\n## {today}\n\n### Ações de cobrança/verificação com time\n- (vazio)\n\n### Decisões tomadas\n- (vazio)\n\n### Tarefas criadas/atualizadas\n- (vazio)\n\n### Ações pessoais\n- (vazio)\n\n### Skips / pausas\n- (vazio)\n'
        DAILY.write_text(text)

def append_daily(kind, message):
    today = game_date()
    ensure_day_block(today)
    text = DAILY.read_text()
    section_map = {
        'acao': '### Ações de cobrança/verificação com time',
        'decisao': '### Decisões tomadas',
        'tarefa': '### Tarefas criadas/atualizadas',
        'pessoal': '### Ações pessoais',
        'pausa': '### Skips / pausas',
    }
    section = section_map[kind]
    parts = re.split(rf'(?m)^## {re.escape(today)}\n', text, maxsplit=1)
    if len(parts) < 2:
        return
    prefix, rest = parts[0], parts[1]
    next_day = re.search(r'(?m)^## \d{4}-\d{2}-\d{2}$', rest)
    if next_day:
        current = rest[:next_day.start()]
        suffix = rest[next_day.start():]
    else:
        current = rest
        suffix = ''
    pattern = rf'({re.escape(section)}\n)(.*?)(\n### |\Z)'
    m = re.search(pattern, current, flags=re.S)
    if not m:
        return
    body = m.group(2)
    entry = f'- {now_local().strftime("%H:%M")} — {message}\n'
    if message in body:
        return
    if '- (vazio)\n' in body:
        body = body.replace('- (vazio)\n', entry)
    else:
        body += entry
    current = current[:m.start(2)] + body + current[m.end(2):]
    DAILY.write_text(prefix + f'## {today}\n' + current + suffix)

def detect(msg):
    low = msg.lower()
    person = any(name in low for name in CIRCLE)
    verb = any(v in low for v in VERBS)
    if person and verb:
        return 'acao'
    if any(v in low for v in ['decidi','defini','fechei','escolhi']):
        return 'decisao'
    if any(v in low for v in ['academia','meditei','meditação','meditacao','li ','leitura','caminhada']):
        return 'pessoal'
    if any(v in low for v in ['pausa','tô fora','to fora','doente','viagem','luto']):
        return 'pausa'
    return None

def record_message(msg):
    kind = detect(msg)
    if kind:
        append_daily(kind, msg)

def get_day_text(today):
    text = DAILY.read_text() if DAILY.exists() else ''
    m = re.search(rf'(?ms)^## {re.escape(today)}\n(.*?)(^## \d{{4}}-\d{{2}}-\d{{2}}\n|\Z)', text)
    return m.group(1) if m else ''

def day_has_action(day_text):
    m = re.search(r'### Ações de cobrança/verificação com time\n(.*?)(\n### |\Z)', day_text, flags=re.S)
    if not m:
        return False
    body = m.group(1)
    return '- ' in body and '(vazio)' not in body

def close_day():
    ensure_files()
    today = game_date()
    day_text = get_day_text(today)
    has_action = day_has_action(day_text)
    stext = STREAK.read_text()
    active = int(parse_streak_value(stext, 'Streak ativo').split()[0])
    best = int(parse_streak_value(stext, 'Maior streak histórico').split()[0])
    weekday = now_local().strftime('%A').lower()
    status='quebrou'
    evidence='sem ação CEO registrada'
    if weekday == 'saturday':
        status='congelado'
        evidence='sábado — streak congelada'
    elif has_action:
        active += 1
        best = max(best, active)
        status='contou'
        m = re.search(r'### Ações de cobrança/verificação com time\n- ([^\n]+)', day_text)
        evidence = m.group(1) if m else 'ação CEO registrada'
    else:
        active = 0
        stext = set_line(stext, 'Última quebra', f'{today} (motivo: sem ação CEO registrada)')
    stext = set_line(stext, 'Streak ativo', f'{active} dias')
    stext = set_line(stext, 'Maior streak histórico', f'{best} dias')
    table = f'| {today} | {status} | {active} | {evidence} |\n'
    if table not in stext:
        stext += table
    STREAK.write_text(stext)
    print(f'{status}: {active} dias')

def risk_check():
    today = game_date()
    day_text = get_day_text(today)
    print('RISK' if not day_has_action(day_text) else 'SAFE')

if __name__ == '__main__':
    ensure_files()
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'
    if cmd == 'record':
        record_message(' '.join(sys.argv[2:]))
    elif cmd == 'close-day':
        close_day()
    elif cmd == 'risk-check':
        risk_check()
    else:
        print('usage: ceo-quest-streak.py record <msg> | close-day | risk-check')
