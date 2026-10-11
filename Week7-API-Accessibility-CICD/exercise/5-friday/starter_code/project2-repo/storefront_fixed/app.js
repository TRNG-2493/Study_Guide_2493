// ShopFront: tiny storefront talking to the Project 2 API (GET /items).
// Tests intercept this request with Playwright's page.route(), so no server is needed.
var API = window.SHOPFRONT_API || "http://127.0.0.1:8000";
var cartCount = 0;

function addToCart() { cartCount += 1; document.getElementById("cart-count").textContent = cartCount; }

function render(items) {
  var html = "";
  items.forEach(function (it) {
    html += '<div class="card"><img src="img/placeholder.svg" width="120" height="80" alt="' + it.name + ' product photo">' +
      '<div class="name">' + it.name + '</div>' +
      '<div class="price">$' + it.price.toFixed(2) + '</div>' +
      '<button type="button" class="btn add-btn" data-id="' + it.id + '" onclick="addToCart()">Add to cart<span class="sr-only"> ' + it.name + '</span></button></div>';
  });
  document.getElementById("products").innerHTML = html;
}

function loadItems() {
  fetch(API + "/items?limit=50")
    .then(function (r) { if (!r.ok) { throw new Error("HTTP " + r.status); } return r.json(); })
    .then(function (d) { document.getElementById("status").textContent = ""; render(d.items); })
    .catch(function () { document.getElementById("status").textContent = "Could not load products"; });
}

function subscribe() {
  var v = document.getElementById("email").value;
  var err = document.getElementById("email-error");
  var ok = document.getElementById("email-ok");
  var em = document.getElementById("email");
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) { ok.textContent = ""; err.textContent = "Please enter a valid email address"; em.setAttribute("aria-invalid", "true"); em.focus(); return; }
  err.textContent = ""; em.removeAttribute("aria-invalid"); ok.textContent = "Thanks for subscribing!";
}

document.getElementById("subscribe").addEventListener("click", subscribe);
loadItems();
