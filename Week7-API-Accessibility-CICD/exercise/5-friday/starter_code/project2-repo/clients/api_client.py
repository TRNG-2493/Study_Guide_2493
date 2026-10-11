import requests


class ApiClient:
    """Thin wrapper over requests.Session: base URL, default timeout, optional bearer token."""

    def __init__(self, base_url, timeout=5.0, token=None, session=None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        self.token = token

    def request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        headers = dict(kwargs.pop("headers", {}) or {})
        if self.token:
            headers.setdefault("Authorization", f"Bearer {self.token}")
        return self.session.request(method, f"{self.base_url}{path}", headers=headers, **kwargs)

    def get(self, path, **kw):
        return self.request("GET", path, **kw)

    def post(self, path, **kw):
        return self.request("POST", path, **kw)

    def put(self, path, **kw):
        return self.request("PUT", path, **kw)

    def patch(self, path, **kw):
        return self.request("PATCH", path, **kw)

    def delete(self, path, **kw):
        return self.request("DELETE", path, **kw)

    def login(self, username, password):
        """Log in and keep the token on this client. Returns the response."""
        r = self.post("/auth/login", json={"username": username, "password": password})
        if r.status_code == 200:
            self.token = r.json()["token"]
        return r

    def close(self):
        self.session.close()
