"""
GadgetHub - the OFFLINE practice site (system under test). DO NOT EDIT, and you do not
need to read it: pretend it is somebody else's web application.

It is served from memory with page.route(), so no internet is needed.
Facts you need are in the README ("The practice site").
"""
SITE_URL = "https://gadgethub.test"

LOGIN_HTML = """<!doctype html>
<html lang="en"><head><title>GadgetHub - Sign in</title></head>
<body>
  <h1>GadgetHub</h1>
  <form id="login-form" onsubmit="return false">
    <label for="email">Email</label>
    <input id="email" type="text" placeholder="you@example.com">
    <label for="pw">Password</label>
    <input id="pw" type="password" placeholder="Your password">
    <button type="submit" id="go">Sign in</button>
  </form>
  <p role="alert" data-testid="login-error" hidden></p>
  <script>
    const OK = 'tester@gadgethub.test', LOCKED = 'locked@gadgethub.test', PW = 'Passw0rd!';
    document.getElementById('go').addEventListener('click', () => {
      const e = document.getElementById('email').value.trim();
      const p = document.getElementById('pw').value;
      const err = document.querySelector('[data-testid=login-error]');
      let msg = '';
      if (!e) msg = 'Email is required';
      else if (!p) msg = 'Password is required';
      else if (e === LOCKED && p === PW) msg = 'Account locked. Contact support.';
      else if (!(e === OK && p === PW)) msg = 'Invalid email or password';
      if (msg) { err.textContent = msg; err.hidden = false; return; }
      sessionStorage.setItem('user', e);
      window.location.href = '/shop.html';
    });
  </script>
</body></html>"""

SHOP_HTML = """<!doctype html>
<html lang="en"><head><title>GadgetHub - Shop</title></head>
<body>
  <script>if (!sessionStorage.getItem('user')) window.location.href = '/';</script>
  <header>
    <h1>Shop</h1>
    <span data-testid="welcome"></span>
    <a href="#cart" aria-label="Cart">Cart <span data-testid="cart-count">0</span></a>
    <button id="out">Sign out</button>
  </header>
  <input type="search" aria-label="Search gadgets" placeholder="Search gadgets...">
  <p role="status" id="busy" hidden>Searching...</p>
  <p id="empty" hidden>No gadgets match your search.</p>
  <section id="grid"></section>
  <script>
    document.querySelector('[data-testid=welcome]').textContent =
      'Signed in as ' + (sessionStorage.getItem('user') || '');
    document.getElementById('out').addEventListener('click', () => {
      sessionStorage.clear(); window.location.href = '/';
    });
    const ITEMS = [['USB-C Hub', 39.90], ['USB-C Charger', 25.00], ['Wireless Charger', 29.00],
      ['Wireless Mouse', 19.99], ['Mechanical Keyboard', 89.00], ['Laptop Stand', 34.50],
      ['HD Webcam', 49.99], ['Noise-Cancelling Headphones', 129.00]];
    let cart = 0;
    function render(list) {
      const grid = document.getElementById('grid'); grid.innerHTML = '';
      list.forEach(([name, price]) => {
        const a = document.createElement('article'); a.className = 'card';
        a.innerHTML = '<h2>' + name + '</h2><span class="price">$' + price.toFixed(2) +
                      '</span> <button>Add to cart</button>';
        const b = a.querySelector('button');
        b.addEventListener('click', () => {
          const add = b.textContent === 'Add to cart';
          b.textContent = add ? 'Remove' : 'Add to cart';
          cart += add ? 1 : -1;
          document.querySelector('[data-testid=cart-count]').textContent = cart;
        });
        grid.appendChild(a);
      });
      document.getElementById('empty').hidden = list.length > 0;
    }
    render(ITEMS);
    document.querySelector('input[type=search]').addEventListener('input', (ev) => {
      const q = ev.target.value.trim().toLowerCase();
      document.getElementById('busy').hidden = false;
      setTimeout(() => {                      // slow "server": 600 ms
        render(ITEMS.filter(i => i[0].toLowerCase().includes(q)));
        document.getElementById('busy').hidden = true;
      }, 600);
    });
  </script>
</body></html>"""


def serve(route):
    """page.route handler: answers every request to gadgethub.test from memory."""
    html = SHOP_HTML if route.request.url.endswith("/shop.html") else LOGIN_HTML
    route.fulfill(status=200, content_type="text/html", body=html)


def install(page):
    """Attach GadgetHub to this page (call once per test, before page.goto)."""
    page.route(f"{SITE_URL}/**", serve)
