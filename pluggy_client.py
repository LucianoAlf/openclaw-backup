#!/usr/bin/env python3
"""
pluggy_client.py — Cliente Pluggy Open Finance para Personal Finance LA
========================================================================
Integração via MeuPluggy para acesso a dados bancários reais.
Uso: python3 pluggy_client.py [comando]

Comandos:
  overview      Resumo consolidado de todas as contas
  accounts      Lista todas as contas de todos os bancos
  transactions  Lista transações recentes (últimos 30 dias)
  investments   Lista investimentos
  identity      Dados de identidade do titular
  export        Exporta tudo em JSON para integração
"""

import os
import json
import sys
from datetime import datetime, timedelta
from typing import Optional
import urllib.request
import urllib.error

CONFIG = {
    "client_id": os.getenv("PLUGGY_CLIENT_ID", "7e544456-d812-4d0c-be73-8cf9675db6c1"),
    "client_secret": os.getenv("PLUGGY_CLIENT_SECRET", "85df1630-217d-47dd-adbf-4809e5e66c02"),
    "base_url": "https://api.pluggy.ai",
    "items": {
        "nubank":       "cfebab8e-cedd-4213-b814-526595923fa8",
        "itau":         "eb16fd2f-de41-43e6-bc5d-48908dab7ef0",
        "c6_bank":      "0bc6a06f-2182-4afa-8b4d-e33943a9000b",
        "mercado_pago": "d673d702-737c-46e9-aba8-73587b583e25",
    }
}


class PluggyClient:
    def __init__(self, client_id=None, client_secret=None):
        self.client_id = client_id or CONFIG["client_id"]
        self.client_secret = client_secret or CONFIG["client_secret"]
        self.base_url = CONFIG["base_url"]
        self.api_key: Optional[str] = None
        self.api_key_expires: Optional[datetime] = None
        self.items = dict(CONFIG["items"])

    def _request(self, method, path, data=None, auth=True):
        url = f"{self.base_url}{path}"
        headers = {"Content-Type": "application/json"}
        if auth:
            self._ensure_api_key()
            headers["X-API-KEY"] = self.api_key
        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if e.fp else ""
            print(f"  ✗ Erro {e.code} em {path}: {error_body[:200]}", file=sys.stderr)
            return {}
        except Exception as e:
            print(f"  ✗ Erro de conexão: {e}", file=sys.stderr)
            return {}

    def _get(self, path, params=None):
        if params:
            qs = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
            path = f"{path}?{qs}"
        return self._request("GET", path)

    def _post(self, path, data):
        return self._request("POST", path, data, auth=False)

    def _ensure_api_key(self):
        if self.api_key and self.api_key_expires and datetime.now() < self.api_key_expires:
            return
        self.authenticate()

    def authenticate(self):
        resp = self._post("/auth", {"clientId": self.client_id, "clientSecret": self.client_secret})
        self.api_key = resp.get("apiKey")
        self.api_key_expires = datetime.now() + timedelta(hours=1, minutes=50)
        if not self.api_key:
            raise RuntimeError("Falha na autenticação Pluggy")
        return self.api_key

    def get_accounts(self, item_id):
        resp = self._get("/accounts", {"itemId": item_id})
        return resp.get("results", [])

    def get_all_accounts(self):
        all_accounts = {}
        for bank, item_id in self.items.items():
            all_accounts[bank] = {"item_id": item_id, "accounts": self.get_accounts(item_id)}
        return all_accounts

    def get_transactions(self, account_id, from_date=None, to_date=None, page_size=50, page=1):
        params = {"accountId": account_id, "pageSize": page_size, "page": page}
        if from_date: params["from"] = from_date
        if to_date: params["to"] = to_date
        return self._get("/transactions", params)

    def get_all_transactions(self, days=30, page_size=100):
        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        all_txns = {}
        for bank, item_id in self.items.items():
            accounts = self.get_accounts(item_id)
            bank_txns = []
            for acc in accounts:
                page, total_pages = 1, 1
                while page <= total_pages:
                    resp = self.get_transactions(acc["id"], from_date=from_date, page_size=page_size, page=page)
                    total_pages = resp.get("totalPages", 1)
                    for txn in resp.get("results", []):
                        txn["_bank"] = bank
                        txn["_accountName"] = acc["name"]
                        txn["_accountType"] = acc["type"]
                        bank_txns.append(txn)
                    page += 1
            all_txns[bank] = bank_txns
        return all_txns

    def get_investments(self, item_id):
        resp = self._get("/investments", {"itemId": item_id})
        return resp.get("results", [])

    def get_all_investments(self):
        all_inv = {}
        for bank, item_id in self.items.items():
            inv = self.get_investments(item_id)
            if inv: all_inv[bank] = inv
        return all_inv

    def get_identity(self, item_id):
        return self._get("/identity", {"itemId": item_id})

    def get_overview(self):
        overview = {
            "data_consulta": datetime.now().isoformat(),
            "titular": None,
            "bancos": {},
            "totais": {"saldo_contas": 0, "divida_cartoes": 0, "investimentos": 0, "patrimonio_liquido": 0}
        }
        first_item = list(self.items.values())[0]
        identity = self.get_identity(first_item)
        if identity:
            overview["titular"] = {"nome": identity.get("fullName"), "cpf": identity.get("document")}

        for bank, item_id in self.items.items():
            accounts = self.get_accounts(item_id)
            bank_data = {"contas": [], "cartoes": [], "saldo_total": 0, "divida_total": 0}
            for acc in accounts:
                entry = {"id": acc["id"], "nome": acc["name"], "numero": acc.get("number"),
                         "saldo": acc["balance"], "tipo": acc["type"], "subtipo": acc.get("subtype")}
                if acc["type"] == "BANK":
                    bank_data["contas"].append(entry)
                    bank_data["saldo_total"] += acc["balance"]
                    overview["totais"]["saldo_contas"] += acc["balance"]
                elif acc["type"] == "CREDIT":
                    credit = acc.get("creditData", {}) or {}
                    entry.update({"limite": credit.get("creditLimit"), "disponivel": credit.get("availableCreditLimit"),
                                  "vencimento": credit.get("balanceDueDate"), "pagamento_minimo": credit.get("minimumPayment"),
                                  "bandeira": credit.get("brand")})
                    bank_data["cartoes"].append(entry)
                    bank_data["divida_total"] += acc["balance"]
                    overview["totais"]["divida_cartoes"] += acc["balance"]
            overview["bancos"][bank] = bank_data

        for bank, item_id in self.items.items():
            investments = self.get_investments(item_id)
            total_inv = sum(inv.get("balance", 0) for inv in investments)
            if total_inv > 0:
                overview["bancos"][bank]["investimentos_total"] = total_inv
                overview["totais"]["investimentos"] += total_inv

        overview["totais"]["patrimonio_liquido"] = (
            overview["totais"]["saldo_contas"] + overview["totais"]["investimentos"] - overview["totais"]["divida_cartoes"]
        )
        return overview


def fmt_brl(value):
    sign = "-" if value < 0 else ""
    return f"{sign}R$ {abs(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def print_overview(overview):
    t = overview["totais"]
    titular = overview.get("titular") or {}
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║         💰 PERSONAL FINANCE LA — OVERVIEW                   ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    if titular:
        print(f"║  Titular: {titular.get('nome','?'):<50} ║")
    print(f"║  Data:    {overview['data_consulta'][:19]:<50} ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  🏦 Saldo em contas:      {fmt_brl(t['saldo_contas']):>30}  ║")
    print(f"║  💳 Dívida cartões:       {fmt_brl(t['divida_cartoes']):>30}  ║")
    print(f"║  📈 Investimentos:        {fmt_brl(t['investimentos']):>30}  ║")
    print(f"║  ─────────────────────────────────────────────────────────  ║")
    print(f"║  🎯 Patrimônio líquido:   {fmt_brl(t['patrimonio_liquido']):>30}  ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    for bank, data in overview["bancos"].items():
        print(f"\n  ┌─ {bank.upper().replace('_', ' ')}")
        for c in data["contas"]:
            print(f"  │  🏦 {c['nome']:<40} {fmt_brl(c['saldo']):>15}")
        for cc in data["cartoes"]:
            bandeira = f" ({cc.get('bandeira','')})" if cc.get('bandeira') else ""
            print(f"  │  💳 {cc['nome']:<40} {fmt_brl(cc['saldo']):>15}{bandeira}")
        inv = data.get("investimentos_total", 0)
        if inv > 0:
            print(f"  │  📈 Investimentos: {fmt_brl(inv):>35}")
        print(f"  └{'─'*55}")
    print()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "overview"
    client = PluggyClient()
    print("  🔑 Autenticando com Pluggy API...")
    client.authenticate()
    print("  ✓ Autenticado\n")

    if cmd == "overview":
        overview = client.get_overview()
        print_overview(overview)
    elif cmd == "accounts":
        for bank, data in client.get_all_accounts().items():
            print(f"\n  {bank.upper()}:")
            for acc in data["accounts"]:
                print(f"    {acc['type']:<8} {acc['name']:<45} {fmt_brl(acc['balance']):>15}")
    elif cmd == "transactions":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        all_txns = client.get_all_transactions(days=days)
        for bank, txns in all_txns.items():
            if not txns: continue
            print(f"\n  {bank.upper()} ({len(txns)} transações):")
            for txn in sorted(txns, key=lambda x: x.get("date",""), reverse=True)[:15]:
                color = "🔴" if txn.get("amount",0) < 0 else "🟢"
                print(f"    {txn.get('date','')[:10]} {color} {fmt_brl(txn.get('amount',0)):>14}  {txn.get('description','?')[:40]}")
    elif cmd == "investments":
        for bank, investments in client.get_all_investments().items():
            total = sum(i.get("balance",0) for i in investments)
            print(f"\n  {bank.upper()} — {fmt_brl(total)}")
            for inv in investments:
                print(f"    {inv.get('subtype',inv.get('type','?')):<15} {fmt_brl(inv.get('balance',0)):>14}  {inv.get('name','?')[:50]}")
    elif cmd == "export":
        out = sys.argv[2] if len(sys.argv) > 2 else "pluggy_export.json"
        data = {"exported_at": datetime.now().isoformat(), "overview": client.get_overview(),
                "transactions": client.get_all_transactions(30), "investments": client.get_all_investments()}
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        print(f"  ✓ Exportado para {out}")


if __name__ == "__main__":
    main()
