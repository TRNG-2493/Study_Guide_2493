"""Tiny static server for the exercise app (standard library only, works offline).

Manual exploration:   python serve.py            -> http://127.0.0.1:8765/
Custom port:          python serve.py 9000

The pytest suite starts its own copy automatically (see tests/conftest.py), so you do NOT
need to run this before `pytest`. Use it when you want to click around the form yourself.
"""
from __future__ import annotations

import functools
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

APP_DIR = Path(__file__).parent / "app"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):  # keep test output clean
        pass


def make_server(port: int = 0) -> ThreadingHTTPServer:
    """Create (but do not start) a server on 127.0.0.1. port=0 picks a free port."""
    handler = functools.partial(QuietHandler, directory=str(APP_DIR))
    return ThreadingHTTPServer(("127.0.0.1", port), handler)


def start_in_thread(port: int = 0) -> tuple[ThreadingHTTPServer, str]:
    server = make_server(port)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


if __name__ == "__main__":
    chosen = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    srv = make_server(chosen)
    print(f"Serving {APP_DIR} at http://127.0.0.1:{chosen}/  (Ctrl+C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
