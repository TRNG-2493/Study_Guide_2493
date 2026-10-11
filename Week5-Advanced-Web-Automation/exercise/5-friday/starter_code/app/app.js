/* QE Shop: tiny stand-in app under test for the 5-friday exercise.
   Selector contract: every interactive element has a data-test attribute (ids/classes exist too, on purpose,
   so that a recorder has messier choices than you should keep). */
(function () {
  var USERS = { standard_user: 'secret_sauce', locked_out_user: 'secret_sauce' };
  var PRODUCTS = [
    { slug: 'trail-backpack', name: 'Trail Backpack', price: 29.99, img: 'backpack.svg', desc: 'Carries a laptop and a lunch.' },
    { slug: 'bike-light', name: 'Bike Light', price: 9.99, img: 'light.svg', desc: 'Rechargeable, very bright.' },
    { slug: 'bolt-tshirt', name: 'Bolt T-Shirt', price: 15.99, img: 'tshirt.svg', desc: 'Soft cotton, classic fit.' },
    { slug: 'fleece-jacket', name: 'Fleece Jacket', price: 49.99, img: 'jacket.svg', desc: 'Warm layer for cold mornings.' }
  ];
  var KEY_CART = 'qeshop-cart', KEY_DIFF = 'qeshop-diff';

  function $(sel) { return document.querySelector(sel); }
  function store(fn, fallback) { try { return fn(); } catch (e) { return fallback; } }
  function money(n) { return '$' + n.toFixed(2); }
  function getCart() { return store(function () { return JSON.parse(localStorage.getItem(KEY_CART) || '[]'); }, []); }
  function setCart(c) { store(function () { localStorage.setItem(KEY_CART, JSON.stringify(c)); }); }
  function byslug(s) { return PRODUCTS.filter(function (p) { return p.slug === s; })[0]; }
  function cookie(name) { var m = document.cookie.match('(?:^|; )' + name + '=([^;]*)'); return m ? decodeURIComponent(m[1]) : null; }

  // Deliberate-diff toggle
  var q = new URLSearchParams(location.search).get('diff');
  store(function () { if (q === 'on') localStorage.setItem(KEY_DIFF, 'on'); if (q === 'off') localStorage.removeItem(KEY_DIFF); });
  if (window.QESHOP_DIFF === true || store(function () { return localStorage.getItem(KEY_DIFF); }) === 'on') {
    document.documentElement.classList.add('rebrand');
  }

  function header() {
    var n = getCart().length;
    return '<header class="top"><span class="brand" data-test="brand">QE Shop</span><nav>' +
      '<a href="/cart.html" data-test="shopping-cart-link" id="cart-link" class="cart_link">Cart' +
      (n ? '<span class="badge" data-test="shopping-cart-badge" id="cart-badge">' + n + '</span>' : '') + '</a>' +
      '<button data-test="logout" id="logout">Log out</button></nav></header>';
  }
  function requireSession() {
    if (!cookie('session-username')) { location.replace('/'); return false; }
    return true;
  }
  function wireHeader() {
    var b = $('[data-test="logout"]');
    if (b) b.addEventListener('click', function () {
      document.cookie = 'session-username=; Max-Age=0; path=/';
      location.href = '/';
    });
  }

  var page = document.body.getAttribute('data-page');

  if (page === 'login') {
    $('[data-test="login-button"]').addEventListener('click', function (e) {
      e.preventDefault();
      var u = $('[data-test="username"]').value, p = $('[data-test="password"]').value, err = $('[data-test="error"]');
      if (!u) { err.textContent = 'Error: Username is required'; err.hidden = false; return; }
      if (!p) { err.textContent = 'Error: Password is required'; err.hidden = false; return; }
      if (u === 'locked_out_user' && USERS[u] === p) { err.textContent = 'Error: Sorry, this user has been locked out'; err.hidden = false; return; }
      if (USERS[u] !== p) { err.textContent = 'Error: Username and password do not match'; err.hidden = false; return; }
      document.cookie = 'session-username=' + encodeURIComponent(u) + '; path=/';
      location.href = '/inventory.html';
    });
    return;
  }

  if (!requireSession()) return;
  document.getElementById('top').innerHTML = header();
  wireHeader();

  if (page === 'inventory') {
    var list = $('[data-test="inventory-list"]');
    function render() {
      var cart = getCart();
      list.innerHTML = PRODUCTS.map(function (p) {
        var inCart = cart.indexOf(p.slug) > -1;
        return '<div class="card inventory_item" data-test="inventory-item">' +
          '<img src="/img/' + p.img + '" alt="' + p.name + '" width="200" height="130">' +
          '<div class="name inventory_item_name" data-test="inventory-item-name">' + p.name + '</div>' +
          '<p class="desc">' + p.desc + '</p>' +
          '<div class="price" data-test="inventory-item-price">' + money(p.price) + '</div>' +
          '<button class="btn btn-primary btn_inventory" data-test="' + (inCart ? 'remove-' : 'add-to-cart-') + p.slug + '">' +
          (inCart ? 'Remove' : 'Add to cart') + '</button></div>';
      }).join('');
      document.getElementById('top').innerHTML = header();
      wireHeader();
      PRODUCTS.forEach(function (p) {
        var btn = $('[data-test="add-to-cart-' + p.slug + '"]') || $('[data-test="remove-' + p.slug + '"]');
        btn.addEventListener('click', function () {
          var c = getCart(), i = c.indexOf(p.slug);
          if (i > -1) c.splice(i, 1); else c.push(p.slug);
          setCart(c); render();
        });
      });
    }
    // DYNAMIC CONTENT (changes on every load / every second): your visual tests must deal with these two
    var lu = $('[data-test="last-updated"]');
    function tick() { lu.textContent = 'Prices updated: ' + new Date().toLocaleTimeString('en-GB'); }
    tick(); setInterval(tick, 1000);
    $('[data-test="visitors-online"]').textContent = 'Visitors online: ' + (100 + Math.floor(Math.random() * 900));
    render();
  }

  if (page === 'cart') {
    var cart = getCart(), box = $('[data-test="cart-list"]');
    box.innerHTML = cart.length ? cart.map(function (s) {
      var p = byslug(s);
      return '<div class="row inventory_item" data-test="inventory-item"><span data-test="inventory-item-name">' + p.name +
        '</span><span data-test="inventory-item-price">' + money(p.price) + '</span></div>';
    }).join('') : '<p data-test="cart-empty">Your cart is empty.</p>';
    $('[data-test="checkout"]').addEventListener('click', function () { location.href = '/checkout.html'; });
    $('[data-test="continue-shopping"]').addEventListener('click', function () { location.href = '/inventory.html'; });
  }

  if (page === 'checkout') {
    var total = getCart().reduce(function (t, s) { return t + byslug(s).price; }, 0);
    $('[data-test="subtotal-label"]').textContent = 'Item total: ' + money(total);
    $('[data-test="finish"]').addEventListener('click', function (e) {
      e.preventDefault();
      var err = $('[data-test="error"]');
      var f = $('[data-test="firstName"]').value, l = $('[data-test="lastName"]').value, z = $('[data-test="postalCode"]').value;
      if (!f) { err.textContent = 'Error: First Name is required'; err.hidden = false; return; }
      if (!l) { err.textContent = 'Error: Last Name is required'; err.hidden = false; return; }
      if (!z) { err.textContent = 'Error: Postal Code is required'; err.hidden = false; return; }
      store(function () { sessionStorage.setItem('qeshop-order', String(100000 + Math.floor(Math.random() * 900000))); });
      location.href = '/complete.html';
    });
  }

  if (page === 'complete') {
    $('[data-test="order-number"]').textContent = 'Order #' + (store(function () { return sessionStorage.getItem('qeshop-order'); }) || '000000'); // DYNAMIC
    setCart([]);
    document.getElementById('top').innerHTML = header();
    wireHeader();
  }
})();
