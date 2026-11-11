// Shared code for the logged-in pages
const PRODUCTS = [
  { name: "Backpack",   price: 29.99 },
  { name: "Bike Light", price: 9.99 },
  { name: "T-Shirt",    price: 15.99 },
  { name: "Jacket",     price: 49.99 },
  { name: "Onesie",     price: 7.99 },
];

if (!localStorage.getItem("user")) {
  location.replace("login.html");
}

function getCart() { return JSON.parse(localStorage.getItem("cart") || "[]"); }
function saveCart(cart) { localStorage.setItem("cart", JSON.stringify(cart)); renderHeader(); }
function money(n) { return "$" + n.toFixed(2); }
function priceOf(name) { return PRODUCTS.find((p) => p.name === name).price; }

function renderHeader() {
  document.querySelector("#cart-link").textContent = `Cart (${getCart().length})`;
}

document.addEventListener("DOMContentLoaded", () => {
  const header = document.createElement("header");
  header.innerHTML = `
    <strong>Practice Store</strong>
    <nav>
      <a href="products.html">Products</a>
      <a id="cart-link" href="cart.html">Cart (0)</a>
      <button id="logout">Log out</button>
    </nav>`;
  document.body.prepend(header);
  renderHeader();
  document.querySelector("#logout").addEventListener("click", () => {
    localStorage.clear();
    location.href = "login.html";
  });
});