"""Safe local load test for a LOGIN endpoint (standard library only).

WARNING: this script starts its OWN tiny server on 127.0.0.1 and sends traffic only
to it. There is intentionally no option to choose another host. NEVER copy this idea
to point load at a third-party site, a shared environment or a system you do not own.
Doing so can disrupt services and may be illegal.

Usage: python load_login_local.py [--users 10] [--think 0.2] [--ramp 2] [--steady 5]
"""
import argparse
import statistics
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        time.sleep(0.01)  # simulated work: about 10 ms per request
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, *args):
        pass


def user_loop(url, start_at, stop_at, think, results, lock):
    time.sleep(max(0, start_at - time.time()))
    while time.time() < stop_at:
        began = time.perf_counter()
        ok = True
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                resp.read()
        except (urllib.error.URLError, OSError):
            ok = False
        elapsed = time.perf_counter() - began
        with lock:
            results.append((elapsed, ok, time.time()))
        time.sleep(think)


def percentile(sorted_values, pct):
    index = max(0, min(len(sorted_values) - 1, round(pct / 100 * len(sorted_values)) - 1))
    return sorted_values[index]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--users", type=int, default=10)
    parser.add_argument("--think", type=float, default=0.2, help="seconds between requests")
    parser.add_argument("--ramp", type=float, default=2.0, help="seconds to start all users")
    parser.add_argument("--steady", type=float, default=5.0, help="seconds of steady state")
    args = parser.parse_args()
    if args.users > 200:
        raise SystemExit("Refusing more than 200 virtual users for this teaching script.")

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_address[1]}/login"

    results, lock = [], threading.Lock()
    t0 = time.time()
    stop_at = t0 + args.ramp + args.steady
    threads = []
    for i in range(args.users):
        start_at = t0 + args.ramp * i / max(1, args.users)
        th = threading.Thread(target=user_loop, args=(url, start_at, stop_at, args.think, results, lock))
        th.start()
        threads.append(th)
    for th in threads:
        th.join()
    server.shutdown()

    steady = [r for r in results if r[2] >= t0 + args.ramp]
    times = sorted(r[0] * 1000 for r in steady)
    errors = sum(1 for r in steady if not r[1])
    print(f"users={args.users} think={args.think}s ramp={args.ramp}s steady={args.steady}s")
    print(f"requests (steady state): {len(steady)}")
    print(f"p50={statistics.median(times):.1f} ms  p95={percentile(times, 95):.1f} ms  p99={percentile(times, 99):.1f} ms")
    print(f"throughput={len(steady) / args.steady:.1f} req/s  error rate={100 * errors / len(steady):.2f} %")


if __name__ == "__main__":
    main()
