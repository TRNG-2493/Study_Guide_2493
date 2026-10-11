// ShopLite - tiny local practice app (no dependencies). Run: npm run app   (default http://localhost:3100)
// ASSUMPTION: stands in for the real Project 1 app. Same ideas: login form, product list, cart, checkout.
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3100;
const PUBLIC = path.join(__dirname, 'public');
const USERS = { standard_user: 'secret_sauce', locked_out_user: 'secret_sauce' };
const PRODUCTS = [
  { slug: 'sauce-backpack', name: 'Trail Backpack', price: 29.99 },
  { slug: 'sauce-bike-light', name: 'Bike Light', price: 9.99 },
  { slug: 'sauce-tshirt', name: 'Logo T-Shirt', price: 15.99 },
  { slug: 'sauce-jacket', name: 'Fleece Jacket', price: 49.99 },
  { slug: 'sauce-onesie', name: 'Baby Onesie', price: 7.99 },
  { slug: 'sauce-bottle', name: 'Steel Bottle', price: 19.99 },
];
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json' };

function readBody(req) {
  return new Promise((resolve) => {
    let data = '';
    req.on('data', (c) => (data += c));
    req.on('end', () => { try { resolve(JSON.parse(data || '{}')); } catch (e) { resolve({}); } });
  });
}
function json(res, status, obj, headers = {}) {
  res.writeHead(status, { 'Content-Type': 'application/json', ...headers });
  res.end(JSON.stringify(obj));
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost');

  if (url.pathname === '/api/products' && req.method === 'GET') {
    // Small delay on purpose: the list appears AFTER the page loads, so waiting/retry matters.
    return setTimeout(() => json(res, 200, PRODUCTS), 300);
  }
  if (url.pathname === '/api/login' && req.method === 'POST') {
    const { username, password } = await readBody(req);
    if (!username) return json(res, 400, { error: 'Username is required' });
    if (!password) return json(res, 400, { error: 'Password is required' });
    if (username === 'locked_out_user') return json(res, 403, { error: 'Sorry, this user has been locked out' });
    if (USERS[username] !== password) return json(res, 401, { error: 'Username and password do not match any user' });
    return json(res, 200, { ok: true }, { 'Set-Cookie': `session-username=${username}; Path=/` });
  }

  const file = url.pathname === '/' ? '/index.html' : url.pathname;
  const full = path.normalize(path.join(PUBLIC, file));
  if (!full.startsWith(PUBLIC) || !fs.existsSync(full) || fs.statSync(full).isDirectory()) {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    return res.end('Not found');
  }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(full)] || 'application/octet-stream' });
  fs.createReadStream(full).pipe(res);
});

server.listen(PORT, () => console.log(`ShopLite running at http://localhost:${PORT}`));
