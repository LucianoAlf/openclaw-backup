#!/usr/bin/env python3
"""Ping Supabase projects so paused/free projects keep light activity.
Never prints secrets."""
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

ENV_PATH = Path('/root/.openclaw/workspace/.env')
SYSTEMS = {
    'LAHQ': 'SUPABASE_LAHQ',
    'Alfredo': 'SUPABASE_ALFREDO',
    'LA Report': 'LAREPORT_SUPABASE',
    'Studio Manager': 'STUDIOMANAGER_SUPABASE',
    'Folha de Pagamento': 'FOLHAPAGAMENTO_SUPABASE',
}

def load_env(path: Path):
    if not path.exists():
        raise FileNotFoundError(path)
    for raw in path.read_text(errors='ignore').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ[key.strip()] = value.strip().strip('"').strip("'")

def ping(name: str, prefix: str) -> tuple[bool, str]:
    url = os.getenv(prefix + '_URL')
    key = os.getenv(prefix + '_SERVICE_ROLE') or os.getenv(prefix + '_ANON_KEY')
    project_id = os.getenv(prefix + '_PROJECT_ID', '?')
    if not url or not key:
        return False, f'{name}: MISSING env project={project_id}'
    req = urllib.request.Request(
        url.rstrip('/') + '/rest/v1/',
        headers={'apikey': key, 'Authorization': 'Bearer ' + key},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            return 200 <= res.status < 300, f'{name}: OK {res.status} project={project_id}'
    except urllib.error.HTTPError as exc:
        # HTTP means DNS/project is awake, but auth/API may be wrong. Treat 2xx only as success.
        return False, f'{name}: HTTP {exc.code} project={project_id}'
    except Exception as exc:
        return False, f'{name}: ERROR {type(exc).__name__}: {exc} project={project_id}'

def main() -> int:
    load_env(ENV_PATH)
    ok_all = True
    for name, prefix in SYSTEMS.items():
        ok, msg = ping(name, prefix)
        ok_all = ok_all and ok
        print(msg)
    return 0 if ok_all else 1

if __name__ == '__main__':
    sys.exit(main())
