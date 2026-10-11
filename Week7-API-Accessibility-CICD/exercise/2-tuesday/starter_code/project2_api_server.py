"""Stand-in "Project 2 API" for Week 7 exercises (standard library only).

Run:  python project2_api_server.py          (listens on http://127.0.0.1:8000)
Reset data any time with: POST /admin/reset  (admin token) or restart the server.

Swap this out for your real Project 2 API when it is available; the exercises
only rely on the contract documented in each day's brief.

Users: tester/tester123 (role=user), admin/admin123 (role=admin)
"""
import json, re, secrets, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

USERS = {"tester": ("tester123", "user"), "admin": ("admin123", "admin")}
SEED = [
    {"id": 1, "name": "Notebook", "price": 4.5, "category": "office", "stock": 100},
    {"id": 2, "name": "Desk Lamp", "price": 24.99, "category": "home", "stock": 15},
    {"id": 3, "name": "USB Cable", "price": 7.0, "category": "electronics", "stock": 250},
    {"id": 4, "name": "Headphones", "price": 59.0, "category": "electronics", "stock": 0},
    {"id": 5, "name": "Stapler", "price": 9.99, "category": "office", "stock": 40},
]
STATE = {"items": [], "next_id": 6, "tokens": {}}

def reset():
    STATE["items"] = [dict(i) for i in SEED]
    STATE["next_id"] = 6
    STATE["tokens"] = {}
reset()

def validate_item(d, partial=False):
    errs = {}
    if not partial or "name" in d:
        if not isinstance(d.get("name"), str) or not d["name"].strip():
            errs["name"] = "required non-empty string"
    if not partial or "price" in d:
        p = d.get("price")
        if isinstance(p, bool) or not isinstance(p, (int, float)) or p < 0:
            errs["price"] = "required number >= 0"
    if not partial or "category" in d:
        if d.get("category") not in ("office", "home", "electronics"):
            errs["category"] = "one of office, home, electronics"
    if "stock" in d and (not isinstance(d["stock"], int) or isinstance(d["stock"], bool) or d["stock"] < 0):
        errs["stock"] = "integer >= 0"
    return errs

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, body=None, headers=None):
        data = b"" if body is None else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Request-Id", secrets.token_hex(4))
        for k, v in (headers or {}).items(): self.send_header(k, v)
        self.end_headers()
        if code != 204: self.wfile.write(data)
    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n else b""
        if not raw: return {}
        try: return json.loads(raw)
        except ValueError: return None
    def _user(self):
        h = self.headers.get("Authorization", "")
        if not h.startswith("Bearer "): return None
        return STATE["tokens"].get(h[7:])
    def _need_auth(self, role=None):
        u = self._user()
        if not u:
            self._send(401, {"error": "unauthorized"}, {"WWW-Authenticate": "Bearer"}); return None
        if role and u["role"] != role:
            self._send(403, {"error": "forbidden"}); return None
        return u
    def _route(self, method):
        u = urlparse(self.path); path = u.path.rstrip("/") or "/"; q = parse_qs(u.query)
        if path == "/health" and method == "GET": return self._send(200, {"status": "ok"})
        if path == "/auth/login" and method == "POST":
            b = self._body()
            if not isinstance(b, dict): return self._send(400, {"error": "invalid JSON"})
            usr = USERS.get(b.get("username"))
            if not usr or usr[0] != b.get("password"): return self._send(401, {"error": "bad credentials"})
            t = secrets.token_hex(16); STATE["tokens"][t] = {"username": b["username"], "role": usr[1]}
            return self._send(200, {"token": t, "token_type": "Bearer", "role": usr[1]})
        if path == "/admin/reset" and method == "POST":
            if not self._need_auth("admin"): return
            tokens = dict(STATE["tokens"]); reset(); STATE["tokens"] = tokens
            return self._send(200, {"status": "reset"})
        if path == "/items" and method == "GET":
            items = STATE["items"]
            if "category" in q: items = [i for i in items if i["category"] == q["category"][0]]
            if "q" in q: items = [i for i in items if q["q"][0].lower() in i["name"].lower()]
            try:
                page = int(q.get("page", ["1"])[0]); limit = int(q.get("limit", ["10"])[0])
                assert page >= 1 and 1 <= limit <= 50
            except (ValueError, AssertionError):
                return self._send(400, {"error": "page>=1 and 1<=limit<=50 required"})
            s = (page - 1) * limit
            return self._send(200, {"total": len(items), "page": page, "limit": limit, "items": items[s:s + limit]})
        if path == "/items" and method == "POST":
            if not self._need_auth(): return
            b = self._body()
            if not isinstance(b, dict): return self._send(400, {"error": "invalid JSON"})
            errs = validate_item(b)
            if errs: return self._send(422, {"error": "validation failed", "details": errs})
            if any(i["name"].lower() == b["name"].lower() for i in STATE["items"]):
                return self._send(409, {"error": "item name already exists"})
            it = {"id": STATE["next_id"], "name": b["name"], "price": b["price"], "category": b["category"], "stock": b.get("stock", 0)}
            STATE["next_id"] += 1; STATE["items"].append(it)
            return self._send(201, it, {"Location": f"/items/{it['id']}"})
        m = re.fullmatch(r"/items/(\d+)", path)
        if m:
            iid = int(m.group(1)); it = next((i for i in STATE["items"] if i["id"] == iid), None)
            if method == "GET":
                return self._send(200, it) if it else self._send(404, {"error": "item not found"})
            if method in ("PUT", "PATCH"):
                if not self._need_auth(): return
                if not it: return self._send(404, {"error": "item not found"})
                b = self._body()
                if not isinstance(b, dict): return self._send(400, {"error": "invalid JSON"})
                errs = validate_item(b, partial=(method == "PATCH"))
                if errs: return self._send(422, {"error": "validation failed", "details": errs})
                for k in ("name", "price", "category", "stock"):
                    if k in b: it[k] = b[k]
                if method == "PUT": it.setdefault("stock", 0)
                return self._send(200, it)
            if method == "DELETE":
                if not self._need_auth("admin"): return
                if not it: return self._send(404, {"error": "item not found"})
                STATE["items"].remove(it); return self._send(204)
        if path in ("/items", "/health", "/auth/login") or m:
            return self._send(405, {"error": "method not allowed"})
        return self._send(404, {"error": "route not found"})
    def do_GET(self): self._route("GET")
    def do_POST(self): self._route("POST")
    def do_PUT(self): self._route("PUT")
    def do_PATCH(self): self._route("PATCH")
    def do_DELETE(self): self._route("DELETE")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"Project 2 stand-in API on http://127.0.0.1:{port}  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
