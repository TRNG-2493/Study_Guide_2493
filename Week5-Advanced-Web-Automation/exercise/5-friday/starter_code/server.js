// Zero-dependency static server for the QE Shop app (Node 18+).
//   npm start            -> http://localhost:4173  (normal app)
//   npm run start:diff   -> same, with the DELIBERATE visual difference switched on (DIFF=on)
//   PORT=5000 npm start  -> another port (then also change baseUrl in cypress.config.js)
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, 'app');
const PORT = Number(process.env.PORT) || 4173;
const DIFF = String(process.env.DIFF || '').toLowerCase() === 'on';
const TYPES = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.json': 'application/json',
};

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const headers = { 'Cache-Control': 'no-store' };

  if (url.pathname === '/config.js') {
    res.writeHead(200, { ...headers, 'Content-Type': TYPES['.js'] });
    return res.end(`window.QESHOP_DIFF = ${DIFF};`);
  }

  const rel = url.pathname === '/' ? 'index.html' : decodeURIComponent(url.pathname).replace(/^\/+/, '');
  const file = path.normalize(path.join(ROOT, rel));
  if (!file.startsWith(ROOT + path.sep)) { res.writeHead(403, headers); return res.end('Forbidden'); }

  fs.readFile(file, (err, data) => {
    if (err) { res.writeHead(404, { ...headers, 'Content-Type': 'text/plain' }); return res.end('Not found'); }
    res.writeHead(200, { ...headers, 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
    res.end(data);
  });
});

server.listen(PORT, () => {
  console.log(`QE Shop running at http://localhost:${PORT}  (deliberate visual diff: ${DIFF ? 'ON' : 'off'})`);
});
