"""API educativa local. Python 3.11+. No es un servicio de producción."""
import argparse
import hashlib
import json
import re
import secrets
import sqlite3
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
SEDES = ["villaflora", "gran_aki_solanda", "solanda_la_j", "san_bartolo"]
LOCK = threading.Lock()


def normalize(data):
    if not isinstance(data, dict):
        return {"valid": False, "eligible": False, "errors": ["object_required"], "data": {}}
    out = dict(data)
    out["name"] = " ".join(str(data.get("name") or "").split())
    out["email"] = str(data.get("email") or "").strip().lower()
    out["sede"] = str(data.get("sede") or "").strip().lower()
    out["consent"] = data.get("consent") is True
    errors = []
    for field in ("event_id", "lead_id", "name"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(field + "_required")
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", out["email"]):
        errors.append("email_invalid")
    if out["sede"] not in SEDES:
        errors.append("sede_invalid")
    if type(data.get("consent")) is not bool:
        errors.append("consent_boolean_required")
    return {"valid": not errors, "eligible": not errors and out["consent"],
            "errors": errors, "data": out}


def stamp():
    return datetime.now(timezone.utc).isoformat()


class LabServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, addr, key, db_path):
        super().__init__(addr, Handler)
        self.key = key
        self.db_path = db_path
        self.failures = {}
        self.leads = json.loads((ROOT / "datos/leads.json").read_text(encoding="utf-8"))
        with self.db() as con:
            con.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, idem TEXT UNIQUE NOT NULL, digest TEXT NOT NULL, body TEXT NOT NULL, created_at TEXT NOT NULL)")
            con.execute("CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY, body TEXT NOT NULL, created_at TEXT NOT NULL)")

    def db(self):
        return sqlite3.connect(self.db_path, timeout=10)


class Handler(BaseHTTPRequestHandler):
    server_version = "AutomationLab/1.0"

    def log_message(self, fmt, *args):
        # No imprime cuerpos, tokens ni parámetros de consulta.
        print(self.command, urlparse(self.path).path, flush=True)

    def send_json(self, status, obj, extra=None):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, str(v))
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def authorized(self):
        got = self.headers.get("Authorization", "")
        expected = "Bearer " + self.server.key
        if not secrets.compare_digest(got, expected):
            self.send_json(401, {"error": "unauthorized"})
            return False
        return True

    def read_json(self):
        n = int(self.headers.get("Content-Length", "0"))
        if n > 65536:
            raise ValueError("body_too_large")
        data = json.loads(self.rfile.read(n).decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("object_required")
        return data

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            return self.send_json(200, {"ok": True, "version": "1.0"})
        if not self.authorized():
            return
        q = parse_qs(parsed.query)
        if parsed.path == "/catalog":
            return self.send_json(200, {"sedes": [{"id": s, "label": s.replace("_", " ").title()} for s in SEDES]})
        if parsed.path == "/leads":
            try:
                offset = int(q.get("offset", ["0"])[0])
                limit = int(q.get("limit", ["2"])[0])
                if offset < 0 or not 1 <= limit <= 100:
                    raise ValueError()
            except ValueError:
                return self.send_json(400, {"error": "pagination_invalid"})
            end = offset + limit
            more = end < len(self.server.leads)
            return self.send_json(200, {"data": self.server.leads[offset:end],
                "next_offset": end if more else None,
                "next_path": f"/leads?offset={end}&limit={limit}" if more else None,
                "total": len(self.server.leads)})
        if parsed.path == "/unstable":
            case = q.get("case", ["demo"])[0][:80]
            try:
                failures = max(0, min(5, int(q.get("failures", ["2"])[0])))
                code = int(q.get("code", ["503"])[0])
                if code not in (429, 503):
                    raise ValueError()
            except ValueError:
                return self.send_json(400, {"error": "simulation_invalid"})
            with LOCK:
                attempt = self.server.failures.get(case, 0) + 1
                self.server.failures[case] = attempt
            if attempt <= failures:
                return self.send_json(code, {"error": "simulated", "attempt": attempt}, {"Retry-After": "2"})
            return self.send_json(200, {"ok": True, "attempt": attempt})
        if parsed.path == "/tasks":
            with self.server.db() as con:
                rows = con.execute("SELECT id,body,created_at FROM tasks ORDER BY id").fetchall()
            return self.send_json(200, {"data": [{"task_id": r[0], **json.loads(r[1]), "created_at_task": r[2]} for r in rows], "count": len(rows)})
        if parsed.path == "/audit":
            with self.server.db() as con:
                rows = con.execute("SELECT id,body,created_at FROM audit ORDER BY id").fetchall()
            return self.send_json(200, {"data": [{"audit_id": r[0], "record": json.loads(r[1]), "created_at": r[2]} for r in rows], "count": len(rows)})
        return self.send_json(404, {"error": "not_found"})

    def do_POST(self):
        if not self.authorized():
            return
        try:
            body = self.read_json()
        except (ValueError, UnicodeError):
            return self.send_json(400, {"error": "json_invalid_or_too_large"})
        path = urlparse(self.path).path
        if path == "/validate":
            return self.send_json(200, normalize(body))
        if path == "/audit":
            with self.server.db() as con:
                cur = con.execute("INSERT INTO audit(body,created_at) VALUES(?,?)", (json.dumps(body, sort_keys=True), stamp()))
            return self.send_json(201, {"audit_id": cur.lastrowid})
        if path == "/tasks":
            idem = self.headers.get("Idempotency-Key", "").strip()
            if not idem or len(idem) > 180:
                return self.send_json(400, {"error": "idempotency_key_required"})
            validated = normalize(body)
            if not validated["eligible"]:
                return self.send_json(422, {"error": "lead_not_eligible", "errors": validated["errors"]})
            # Contrato intencional: el cuerpo enviado debe ser idéntico en un replay.
            canonical = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
            with LOCK, self.server.db() as con:
                row = con.execute("SELECT id,digest FROM tasks WHERE idem=?", (idem,)).fetchone()
                if row:
                    if row[1] != digest:
                        return self.send_json(409, {"error": "idempotency_conflict"})
                    return self.send_json(200, {"task_id": row[0], "replayed": True})
                cur = con.execute("INSERT INTO tasks(idem,digest,body,created_at) VALUES(?,?,?,?)", (idem, digest, canonical, stamp()))
            return self.send_json(201, {"task_id": cur.lastrowid, "replayed": False})
        if path == "/classify":
            # Simulador determinista. No llama a ningún modelo de IA.
            text = str(body.get("text") or "").lower()
            suspicious = any(s in text for s in ("ignora", "ignore", "system prompt", "revela", "token", "contraseña"))
            category = "agendar" if any(s in text for s in ("cita", "agendar")) else "informacion"
            if suspicious:
                category = "revision"
            return self.send_json(200, {"category": category, "confidence": 0.95 if not suspicious else 0.0,
                "needs_human": True, "simulated": True})
        return self.send_json(404, {"error": "not_found"})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--db", default=str(ROOT / "lab/lab.sqlite3"))
    args = parser.parse_args()
    key_file = ROOT / "lab/token.txt"
    if not key_file.exists():
        key_file.write_text(secrets.token_urlsafe(32), encoding="utf-8")
        key_file.chmod(0o600)
    key = key_file.read_text(encoding="utf-8").strip()
    print(f"Laboratorio en http://{args.host}:{args.port}", flush=True)
    print("Token local en lab/token.txt. No lo publiques.", flush=True)
    LabServer((args.host, args.port), key, args.db).serve_forever()


if __name__ == "__main__":
    main()
