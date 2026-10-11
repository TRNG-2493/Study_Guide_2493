// Shared helpers for all ShopLite pages. Cart lives in localStorage under "cart" (array of slugs).
function getCart() { try { return JSON.parse(localStorage.getItem('cart') || '[]'); } catch (e) { return []; } }
function setCart(c) { localStorage.setItem('cart', JSON.stringify(c)); renderBadge(); }
function hasSession() { return document.cookie.split('; ').some((c) => c.startsWith('session-username=')); }
function requireSession() { if (!hasSession()) location.href = '/'; }
function renderBadge() {
  const link = document.querySelector('[data-test="cart-link"]');
  if (!link) return;
  const old = link.querySelector('[data-test="cart-badge"]');
  if (old) old.remove();
  const n = getCart().length;
  if (n > 0) { // badge element exists only when the cart is not empty
    const b = document.createElement('span');
    b.className = 'badge'; b.setAttribute('data-test', 'cart-badge'); b.textContent = String(n);
    link.appendChild(b);
  }
}
function logout() { document.cookie = 'session-username=; Path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT'; location.href = '/'; }
function header(title) {
  return `<header><h1 data-test="page-title">${title}</h1><nav>
    <a href="/cart.html" data-test="cart-link">Cart</a> <button data-test="logout" onclick="logout()">Logout</button></nav></header>`;
}
