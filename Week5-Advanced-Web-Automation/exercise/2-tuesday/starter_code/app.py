#!/usr/bin/env python3
"""
QE Practice Shop - the local test site for the Tuesday exercise (standard library only).

Run it by hand to explore the pages in your own browser:

    python app.py            # then open http://127.0.0.1:8000/

The tests start the same server by themselves (see support.py), so you do NOT need to run this
for pytest. You are not expected to read or change this file; it is the "application under test".
Your job is to automate it from the outside.
"""

import json
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

# Single source of truth: renders the table AND the CSV export (so the export is an independent oracle
# for what the table shows after sorting, paging and searching).
ORDERS = [
    ("1001", "Maria Lopez", "10.50", "Paid"),
    ("1002", "John Smith", "20.00", "Pending"),
    ("1003", "Ann Lee", "5.25", "Paid"),
    ("1004", "Joanna Kim", "12.25", "Pending"),
    ("1005", "Chen Wei", "40.00", "Paid"),
    ("1006", "Dara Okafor", "7.75", "Pending"),
    ("1007", "Eve Martin", "15.00", "Paid"),
    ("1008", "Farid Haddad", "33.10", "Paid"),
    ("1009", "Grace Hall", "9.99", "Pending"),
    ("1010", "Hugo Silva", "18.40", "Paid"),
    ("1011", "Iris Novak", "27.60", "Pending"),
    ("1012", "Jon Park", "3.50", "Paid"),
]
CSV_HEADER = "Order,Customer,Total,Status"

NAV = ('<nav><a href="/">Home</a> | <a href="/orders">Orders</a> | <a href="/checkout">Checkout</a> | '
       '<a href="/delivery">Delivery</a> | <a href="/components">Components</a> | <a href="/import">Import</a></nav><hr>')

# ----------------------------------------------------------------------------------------------
# /orders : sortable + searchable + paginated table, row action, CSV export
# ----------------------------------------------------------------------------------------------
ORDERS_PAGE = r"""<title>Orders</title>__NAV__<h1>Orders</h1>
<input id="search" placeholder="Search orders" aria-label="Search orders">
<p id="summary"></p>
<table id="orders">
  <caption>All orders</caption>
  <thead><tr>
    <th scope="col" data-key="order">Order</th><th scope="col" data-key="customer">Customer</th>
    <th scope="col" data-key="total">Total</th><th scope="col" data-key="status">Status</th>
    <th scope="col">Actions</th></tr></thead>
  <tbody></tbody>
</table>
<p><button id="prev">Previous</button> <span id="label"></span> <button id="next">Next</button></p>
<p><a id="export" href="/export-orders.csv" download>Export CSV</a></p>
<script>
  const DATA = __DATA__;
  const PAGE_SIZE = 5;
  let q = '', sortKey = null, asc = true, page = 0;

  function filtered() {
    let rows = DATA.filter(r => Object.values(r).join(' ').toLowerCase().includes(q));
    if (sortKey) {
      rows = rows.slice().sort((a, b) => {
        const x = a[sortKey], y = b[sortKey];
        const c = (sortKey === 'total' || sortKey === 'order') ? parseFloat(x) - parseFloat(y) : x.localeCompare(y);
        return asc ? c : -c;
      });
    }
    return rows;
  }
  function render() {
    const rows = filtered();
    const pages = Math.max(1, Math.ceil(rows.length / PAGE_SIZE));
    if (page >= pages) page = pages - 1;
    const slice = rows.slice(page * PAGE_SIZE, page * PAGE_SIZE + PAGE_SIZE);
    const tb = document.querySelector('#orders tbody');
    tb.innerHTML = slice.length ? slice.map(r =>
      '<tr><td>' + r.order + '</td><td>' + r.customer + '</td><td>' + r.total + '</td><td>' + r.status + '</td><td>' +
      (r.status === 'Paid' ? '<button class="refund" data-order="' + r.order + '">Refund</button>' : '') + '</td></tr>'
    ).join('') : '<tr><td colspan="5">No orders found</td></tr>';
    document.getElementById('label').textContent = 'Page ' + (page + 1) + ' of ' + pages;
    document.getElementById('prev').disabled = page === 0;
    document.getElementById('next').disabled = page >= pages - 1;
    const pend = DATA.filter(r => r.status === 'Pending');
    const sum = pend.reduce((s, r) => s + Math.round(parseFloat(r.total) * 100), 0) / 100;
    document.getElementById('summary').textContent = pend.length + ' pending orders, total ' + sum.toFixed(2);
  }
  document.getElementById('search').addEventListener('input', e => { q = e.target.value.toLowerCase(); page = 0; render(); });
  document.getElementById('next').onclick = () => { page++; setTimeout(render, 150); };   // simulated network delay
  document.getElementById('prev').onclick = () => { page--; setTimeout(render, 150); };
  document.querySelectorAll('#orders th[data-key]').forEach(th => {
    th.style.cursor = 'pointer';
    th.addEventListener('click', () => {
      asc = (sortKey === th.dataset.key) ? !asc : true; sortKey = th.dataset.key; page = 0;
      document.querySelectorAll('#orders th').forEach(o => o.removeAttribute('aria-sort'));
      th.setAttribute('aria-sort', asc ? 'ascending' : 'descending');
      render();
    });
  });
  document.querySelector('#orders tbody').addEventListener('click', e => {
    if (!e.target.classList.contains('refund')) return;
    DATA.find(r => r.order === e.target.dataset.order).status = 'Refunded';
    render();
  });
  render();
</script>"""

# ----------------------------------------------------------------------------------------------
# /checkout : nested iframes + new tab + popup
# ----------------------------------------------------------------------------------------------
CHECKOUT_PAGE = r"""<title>Checkout</title>__NAV__<h1>Checkout</h1>
<p>Order total: <strong id="total">32.25</strong></p>
<p><a id="terms" href="/terms" target="_blank" rel="opener">Terms of Service</a> <span id="terms-status">Terms: not accepted</span></p>
<p><button id="help">Help</button> <a href="/orders">View orders</a></p>
<h2>Payment</h2>
<iframe title="Secure card payment" src="/pay-frame" width="520" height="330"></iframe>
<p id="payment-status" role="status">Payment: not started</p>
<button id="place" disabled>Place order</button>
<p id="confirmation" role="status"></p>
<script>
  let termsOk = false, payOk = false;
  const refresh = () => { document.getElementById('place').disabled = !(termsOk && payOk); };
  document.getElementById('help').onclick = () => window.open('/help', 'help', 'width=400,height=300');
  window.addEventListener('message', e => {
    if (e.data === 'terms-accepted') {
      termsOk = true; document.getElementById('terms-status').textContent = 'Terms: accepted';
    }
    if (e.data === 'payment-approved') {
      payOk = true; document.getElementById('payment-status').textContent = 'Payment: approved';
    }
    refresh();
  });
  document.getElementById('place').onclick = async () => {
    const r = await fetch('/api/place-order', { method: 'POST' });
    const j = await r.json();
    document.getElementById('confirmation').textContent = 'Order confirmed: ' + j.id;
  };
</script>"""

PAY_FRAME = r"""<title>Card form</title><h3>Card details</h3>
<label for="card">Card number</label> <input id="card" autocomplete="off">
<button id="go">Continue</button>
<p id="err" role="alert"></p>
<p id="verified" role="status"></p>
<div id="slot"></div>
<script>
  document.getElementById('go').onclick = () => {
    const digits = document.getElementById('card').value.replace(/\s/g, '');
    const err = document.getElementById('err');
    if (!/^\d{16}$/.test(digits)) { err.textContent = 'Invalid card number'; return; }
    err.textContent = '';
    // the verification iframe is added late, like a real 3-D Secure challenge
    setTimeout(() => {
      document.getElementById('slot').innerHTML =
        '<iframe title="Bank verification" src="/pay-3ds" width="460" height="150"></iframe>';
    }, 500);
    window.last4 = digits.slice(-4);
  };
  window.addEventListener('message', e => {
    if (e.data === '3ds-ok') {
      document.getElementById('verified').textContent = 'Verified card ending ' + window.last4;
      window.parent.postMessage('payment-approved', '*');
    }
  });
</script>"""

PAY_3DS = r"""<title>Bank</title><h4>Bank verification</h4>
<label for="otp">One-time code</label> <input id="otp">
<button id="ok">Approve payment</button>
<p id="bank-err" role="alert"></p>
<script>
  document.getElementById('ok').onclick = () => {
    if (document.getElementById('otp').value === '123456') { window.parent.postMessage('3ds-ok', '*'); }
    else { document.getElementById('bank-err').textContent = 'Wrong code'; }
  };
</script>"""

TERMS_PAGE = r"""<title>Terms of Service</title><h1>Terms of Service</h1><p>Be kind to the test environment.</p>
<button id="agree">I agree</button>
<script>
  document.getElementById('agree').onclick = () => {
    if (window.opener) window.opener.postMessage('terms-accepted', '*');
    setTimeout(() => window.close(), 200);   // closing a beat later lets Playwright's click() finish cleanly
  };
</script>"""

# ----------------------------------------------------------------------------------------------
# /delivery : native date input + custom calendar widget (uses the browser clock for "today")
# ----------------------------------------------------------------------------------------------
DELIVERY_PAGE = r"""<title>Delivery</title>__NAV__<h1>Delivery</h1>
<p id="today"></p>
<label for="invoice">Invoice date</label>
<input type="date" id="invoice" min="2000-01-01" max="2030-12-31"> <output id="invoice-shown"></output>
<br>
<label for="delivery">Delivery date</label> <input id="delivery" readonly placeholder="Select a date">
<div id="cal" role="dialog" aria-label="Choose date" hidden>
  <button class="prev" aria-label="Previous month">&lt;</button> <span class="title" aria-live="polite"></span>
  <button class="next" aria-label="Next month">&gt;</button> <div class="grid"></div>
</div>
<p id="chosen"></p>
<script>
  const months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const pad = n => String(n).padStart(2, '0');
  const iso = d => d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
  const now = new Date();                                    // page.clock can fake this
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  document.getElementById('today').textContent = 'Today is ' + iso(today);
  document.getElementById('invoice').addEventListener('change', e =>
    document.getElementById('invoice-shown').textContent = 'Invoice dated ' + e.target.value);

  const input = document.getElementById('delivery'), cal = document.getElementById('cal');
  const title = cal.querySelector('.title'), grid = cal.querySelector('.grid');
  let view = new Date(today.getFullYear(), today.getMonth(), 1);
  function render() {
    title.textContent = months[view.getMonth()] + ' ' + view.getFullYear();
    grid.innerHTML = '';
    const days = new Date(view.getFullYear(), view.getMonth() + 1, 0).getDate();
    for (let day = 1; day <= days; day++) {
      const d = new Date(view.getFullYear(), view.getMonth(), day);
      const b = document.createElement('button');
      b.textContent = day;
      b.setAttribute('aria-label', months[view.getMonth()] + ' ' + day + ', ' + view.getFullYear());
      b.disabled = d < today;                                // delivery cannot be in the past
      b.addEventListener('click', () => {
        input.value = iso(d); cal.hidden = true;
        document.getElementById('chosen').textContent = 'Delivery on ' + iso(d);
      });
      grid.appendChild(b);
    }
  }
  input.addEventListener('click', () => { cal.hidden = false; render(); });
  cal.querySelector('.prev').onclick = () => { view.setMonth(view.getMonth() - 1); render(); };
  cal.querySelector('.next').onclick = () => { view.setMonth(view.getMonth() + 1); render(); };
</script>"""

# ----------------------------------------------------------------------------------------------
# /components : shadow DOM (open roots) + one closed root (stretch)
# ----------------------------------------------------------------------------------------------
COMPONENTS_PAGE = r"""<title>Components</title>__NAV__<h1>Fulfilment board</h1>
<order-card order="1003" customer="Ann Lee"></order-card>
<order-card order="1005" customer="Chen Wei"></order-card>
<order-card order="1008" customer="Farid Haddad"></order-card>
<h2>Audit</h2>
<audit-badge></audit-badge> <p id="audit-out"></p>
<script>
  class OrderCard extends HTMLElement {
    connectedCallback() {
      const root = this.attachShadow({ mode: 'open' });
      root.innerHTML = `<style>.card{border:1px solid #999;padding:8px;margin:6px;width:260px}</style>
        <div class="card"><h3>Order ${this.getAttribute('order')}: ${this.getAttribute('customer')}</h3>
        <span class="state" role="status">Processing</span>
        <button class="ship">Mark shipped</button></div>`;
      root.querySelector('.ship').addEventListener('click', () => {
        root.querySelector('.state').textContent = 'Shipped';
      });
    }
  }
  customElements.define('order-card', OrderCard);

  class AuditBadge extends HTMLElement {            // CLOSED root: host.shadowRoot === null
    constructor() {
      super();
      const r = this.attachShadow({ mode: 'closed' });
      r.innerHTML = '<button class="audit">Run audit</button>';
      r.querySelector('button').addEventListener('click',
        () => { document.getElementById('audit-out').textContent = 'Audited'; });
    }
  }
  customElements.define('audit-badge', AuditBadge);
</script>"""

# ----------------------------------------------------------------------------------------------
# /import : file upload (input in the DOM, plus an input created on demand)
# ----------------------------------------------------------------------------------------------
IMPORT_PAGE = r"""<title>Import</title>__NAV__<h1>Import orders</h1>
<label>Orders CSV <input id="csv" type="file" accept=".csv"></label>
<p><button id="pick">Pick file...</button> <small>(creates a file input on demand)</small></p>
<p id="import-result" role="status"></p>
<script>
  async function send(file) {
    const msg = document.getElementById('import-result'); msg.textContent = '';
    const fd = new FormData(); fd.append('file', file);
    const r = await fetch('/api/import', { method: 'POST', body: fd });
    const j = await r.json();
    msg.textContent = r.ok ? 'Imported ' + j.imported + ' orders from ' + j.filename : 'Rejected: ' + j.error;
  }
  document.getElementById('csv').addEventListener('change', e => { if (e.target.files.length) send(e.target.files[0]); });
  document.getElementById('pick').onclick = () => {
    const input = document.createElement('input'); input.type = 'file';
    input.onchange = () => { if (input.files.length) send(input.files[0]); };
    input.click();
  };
</script>"""

HELP_PAGE = "<title>Help</title><h1>Help centre</h1><p>Call us.</p>"
INDEX_PAGE = "<title>QE Practice Shop</title>__NAV__<h1>QE Practice Shop</h1><p>Pick a page from the menu.</p>"


def _data_json() -> str:
    return json.dumps([dict(order=o, customer=c, total=t, status=s) for o, c, t, s in ORDERS])


def build_pages() -> dict:
    pages = {
        "/": INDEX_PAGE, "/orders": ORDERS_PAGE.replace("__DATA__", _data_json()),
        "/checkout": CHECKOUT_PAGE, "/pay-frame": PAY_FRAME, "/pay-3ds": PAY_3DS,
        "/terms": TERMS_PAGE, "/help": HELP_PAGE, "/delivery": DELIVERY_PAGE,
        "/components": COMPONENTS_PAGE, "/import": IMPORT_PAGE,
    }
    return {k: v.replace("__NAV__", NAV) for k, v in pages.items()}


PAGES = build_pages()


def parse_upload(content_type: str, body: bytes):
    """Return (filename, file_bytes) of the first file part of a multipart/form-data body."""
    m = re.search(r'boundary=([^;]+)', content_type)
    if not m:
        return None, b""
    boundary = b"--" + m.group(1).strip('"').encode()
    for part in body.split(boundary):
        head, sep, content = part.partition(b"\r\n\r\n")
        fn = re.search(rb'filename="([^"]*)"', head)
        if sep and fn:
            return fn.group(1).decode(), content.rsplit(b"\r\n", 1)[0]
    return None, b""


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body: bytes, ctype="text/html; charset=utf-8", headers=None):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status, obj):
        self._send(status, json.dumps(obj).encode(), "application/json")

    def _route(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        path = urlparse(self.path).path

        if path == "/export-orders.csv":
            out = CSV_HEADER + "\n" + "".join(",".join(o) + "\n" for o in ORDERS)
            return self._send(200, out.encode(), "text/csv",
                              {"Content-Disposition": 'attachment; filename="orders.csv"'})
        if path == "/api/place-order" and self.command == "POST":
            return self._json(201, {"id": "ORD-2001"})
        if path == "/api/import" and self.command == "POST":
            name, content = parse_upload(self.headers.get("Content-Type", ""), body)
            if not name or not name.lower().endswith(".csv"):      # the server must validate again
                return self._json(415, {"error": "only .csv files are accepted"})
            lines = content.decode("utf-8", "replace").splitlines()
            if not lines or lines[0].strip() != CSV_HEADER:
                return self._json(422, {"error": "unexpected header"})
            return self._json(200, {"imported": len([ln for ln in lines[1:] if ln.strip()]), "filename": name})

        page = PAGES.get(path)
        if page is None:
            return self._send(404, b"<title>404</title><h1>Page not found</h1>")
        return self._send(200, page.encode("utf-8"))

    do_GET = _route
    do_POST = _route

    def log_message(self, *args):
        pass


def make_server(port: int = 0) -> ThreadingHTTPServer:
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    srv = make_server(port)
    print(f"QE Practice Shop on http://127.0.0.1:{srv.server_address[1]}/  (Ctrl+C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
