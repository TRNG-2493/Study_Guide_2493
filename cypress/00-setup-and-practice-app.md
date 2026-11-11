# Cypress Course: Setup and Practice App

This file has everything students need before Lecture 1: the project structure, the practice app and the Cypress configuration. Every lecture's demos and exercises run against this one project.

**Tested versions:** Cypress 16.2.1, Node.js 22, `@simonsmith/cypress-image-snapshot` 11.0.0.

---

## 1. Project structure

```
cypress-course/
├── package.json
├── cypress.config.js
├── app/                          # the practice website
│   ├── index.html                # home: delayed message + counter
│   ├── login.html                # login form
│   ├── dashboard.html            # shown after login
│   ├── todo.html                 # todo list: type, click, check, select
│   ├── products.html             # loads products from an API (for cy.intercept)
│   ├── styles.css
│   └── api/products.json         # the "API" response
└── cypress/
    ├── e2e/
    │   ├── lecture1-foundations.cy.js
    │   ├── lecture2-locate-interact-assert.cy.js
    │   ├── lecture3-organizing.cy.js
    │   ├── lecture4-debugging.cy.js
    │   ├── lecture5-recording.cy.js
    │   ├── lecture5-visual.cy.js
    │   ├── exercises/            # starter files with TODOs
    │   └── solutions/            # completed exercises
    ├── fixtures/
    │   ├── users.json
    │   └── products.json
    └── support/
        ├── e2e.js                # loaded before every spec
        └── commands.js           # custom commands
```

## 2. Setup steps

```bash
mkdir cypress-course && cd cypress-course
# create the files in this document, then:
npm install
```

Run the app and Cypress in **two terminals**:

```bash
# Terminal 1: serve the practice app at http://localhost:8080
npm start

# Terminal 2: open the Cypress runner
npx cypress open
```

In the runner, choose **E2E Testing**, pick a browser, and click a spec file.

| Command | What it does |
|---|---|
| `npm start` | Serves the app at http://localhost:8080 |
| `npx cypress open` | Opens the interactive runner (headed) |
| `npx cypress run` | Runs every spec headless in the terminal |
| `npm run cy:run:demos` | Runs only the lecture demo specs |
| `npm run cy:run:solutions` | Runs only the exercise solutions |

> The Lecture 4 exercise contains tests that fail on purpose, so a full `npx cypress run` reports failures. Use the scripts above to run demos or solutions only.

## 3. Practice app accounts

| Username | Password |
|---|---|
| `student` | `cypress123` |
| `admin` | `admin123` |

Every element the tests use has a `data-cy` attribute, for example `<button data-cy="login-submit">`.

---

## 4. Project files

### package.json

```json
{
  "name": "cypress-course",
  "version": "1.0.0",
  "description": "Practice app and demo specs for a 5-lecture Cypress course",
  "private": true,
  "scripts": {
    "start": "http-server app -p 8080 -c-1",
    "cy:open": "cypress open",
    "cy:run": "cypress run",
    "cy:run:demos": "cypress run --spec \"cypress/e2e/*.cy.js\"",
    "cy:run:solutions": "cypress run --spec \"cypress/e2e/solutions/*.cy.js\""
  },
  "devDependencies": {
    "@simonsmith/cypress-image-snapshot": "^11.0.0",
    "cypress": "^16.2.1",
    "http-server": "^14.1.1"
  }
}
```

### cypress.config.js

Comments show which lecture each setting belongs to. You can give students the full file on day one.

```js
const { defineConfig } = require('cypress');
// Lecture 5: visual testing plugin
const { addMatchImageSnapshotPlugin } = require('@simonsmith/cypress-image-snapshot/plugin');

module.exports = defineConfig({
  e2e: {
    // Lecture 1: lets us write cy.visit('/') instead of the full URL
    baseUrl: 'http://localhost:8080',

    // Lecture 5: turns on Cypress Studio (recording user actions)
    experimentalStudio: true,

    setupNodeEvents(on, config) {
      // Lecture 4: cy.task('log', 'message') prints to the terminal
      on('task', {
        log(message) {
          console.log(message);
          return null;
        },
      });

      // Lecture 5: registers cy.matchImageSnapshot()
      addMatchImageSnapshotPlugin(on);

      return config;
    },
  },

  // Lecture 4: video is off by default; set to true to record runs
  video: false,
});
```

### cypress/support/e2e.js

```js
// Runs before every spec file. Load custom commands here.
import './commands';

// Lecture 5: adds cy.matchImageSnapshot()
import { addMatchImageSnapshotCommand } from '@simonsmith/cypress-image-snapshot/command';

addMatchImageSnapshotCommand({
  failureThreshold: 0.02,        // allow up to 2% of pixels to differ
  failureThresholdType: 'percent',
});
```

### cypress/support/commands.js

```js
// Lecture 3: custom commands

// Logs in through the UI.
Cypress.Commands.add('login', (username, password) => {
  cy.visit('/login.html');
  cy.get('[data-cy=username]').type(username);
  cy.get('[data-cy=password]').type(password, { log: false }); // hide the password in the Command Log
  cy.get('[data-cy=login-submit]').click();
});

// Logs in once and reuses the session (localStorage) in later tests.
Cypress.Commands.add('loginWithSession', (username, password) => {
  cy.session([username, password], () => {
    cy.login(username, password);
    cy.url().should('include', '/dashboard.html');
  });
});

// Adds a todo on the Todos page.
Cypress.Commands.add('addTodo', (text) => {
  cy.get('[data-cy=new-todo]').type(`${text}{enter}`);
});

// Shorthand for cy.get('[data-cy=...]').
Cypress.Commands.add('getByCy', (value) => cy.get(`[data-cy=${value}]`));
```

### cypress/fixtures/users.json

```json
{
  "valid": [
    { "username": "student", "password": "cypress123" },
    { "username": "admin", "password": "admin123" }
  ],
  "invalid": { "username": "student", "password": "wrong-password" }
}
```

### cypress/fixtures/products.json

```json
[
  { "id": 101, "name": "Test Product A", "price": 10 },
  { "id": 102, "name": "Test Product B", "price": 20.5 }
]
```

---

## 5. Practice app files

### app/index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Cypress Practice App</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <nav data-cy="nav">
    <a href="index.html" data-cy="nav-home">Home</a>
    <a href="login.html" data-cy="nav-login">Login</a>
    <a href="todo.html" data-cy="nav-todo">Todos</a>
    <a href="products.html" data-cy="nav-products">Products</a>
  </nav>
  <main>
    <h1 data-cy="page-title">Cypress Practice App</h1>
    <p>A small site for practising Cypress tests.</p>

    <section class="card">
      <h2>Delayed message</h2>
      <p>The message appears 1.5 seconds after you click.</p>
      <button data-cy="show-message">Show message</button>
      <p data-cy="message" class="success" hidden>Hello from Cypress!</p>
    </section>

    <section class="card">
      <h2>Counter</h2>
      <button class="secondary" data-cy="decrement">-</button>
      <span class="count" data-cy="count">0</span>
      <button data-cy="increment">+</button>
    </section>
  </main>

  <script>
    const message = document.querySelector('[data-cy=message]');
    document.querySelector('[data-cy=show-message]').addEventListener('click', () => {
      setTimeout(() => { message.hidden = false; }, 1500);
    });

    const count = document.querySelector('[data-cy=count]');
    document.querySelector('[data-cy=increment]').addEventListener('click', () => {
      count.textContent = Number(count.textContent) + 1;
    });
    document.querySelector('[data-cy=decrement]').addEventListener('click', () => {
      count.textContent = Number(count.textContent) - 1;
    });
  </script>
</body>
</html>
```

### app/login.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Login | Cypress Practice App</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <nav data-cy="nav">
    <a href="index.html" data-cy="nav-home">Home</a>
    <a href="login.html" data-cy="nav-login">Login</a>
    <a href="todo.html" data-cy="nav-todo">Todos</a>
    <a href="products.html" data-cy="nav-products">Products</a>
  </nav>
  <main>
    <h1 data-cy="page-title">Login</h1>
    <form class="card" data-cy="login-form" novalidate>
      <label for="username">Username</label>
      <input type="text" id="username" name="username" data-cy="username">

      <label for="password">Password</label>
      <input type="password" id="password" name="password" data-cy="password">

      <label><input type="checkbox" data-cy="remember"> Remember me</label>

      <p class="error" data-cy="login-error" hidden></p>
      <button type="submit" data-cy="login-submit">Log in</button>
    </form>
    <p>Practice accounts: <code>student / cypress123</code> and <code>admin / admin123</code></p>
  </main>

  <script>
    const USERS = { student: 'cypress123', admin: 'admin123' };
    const form = document.querySelector('[data-cy=login-form]');
    const error = document.querySelector('[data-cy=login-error]');

    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const username = document.querySelector('[data-cy=username]').value.trim();
      const password = document.querySelector('[data-cy=password]').value;

      if (!username || !password) {
        error.textContent = 'Username and password are required';
        error.hidden = false;
        return;
      }
      if (USERS[username] !== password) {
        error.textContent = 'Invalid username or password';
        error.hidden = false;
        return;
      }
      localStorage.setItem('user', username);
      window.location.href = 'dashboard.html';
    });
  </script>
</body>
</html>
```

### app/dashboard.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Dashboard | Cypress Practice App</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <nav data-cy="nav">
    <a href="index.html" data-cy="nav-home">Home</a>
    <a href="login.html" data-cy="nav-login">Login</a>
    <a href="todo.html" data-cy="nav-todo">Todos</a>
    <a href="products.html" data-cy="nav-products">Products</a>
  </nav>
  <main>
    <h1 data-cy="page-title">Dashboard</h1>
    <section class="card">
      <p data-cy="welcome"></p>
      <button class="secondary" data-cy="logout">Log out</button>
    </section>
  </main>

  <script>
    const user = localStorage.getItem('user');
    if (!user) {
      window.location.href = 'login.html';
    } else {
      document.querySelector('[data-cy=welcome]').textContent = `Welcome, ${user}!`;
    }
    document.querySelector('[data-cy=logout]').addEventListener('click', () => {
      localStorage.removeItem('user');
      window.location.href = 'login.html';
    });
  </script>
</body>
</html>
```

### app/todo.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Todos | Cypress Practice App</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <nav data-cy="nav">
    <a href="index.html" data-cy="nav-home">Home</a>
    <a href="login.html" data-cy="nav-login">Login</a>
    <a href="todo.html" data-cy="nav-todo">Todos</a>
    <a href="products.html" data-cy="nav-products">Products</a>
  </nav>
  <main>
    <h1 data-cy="page-title">Todos</h1>
    <section class="card">
      <form data-cy="todo-form">
        <input type="text" placeholder="What needs to be done?" data-cy="new-todo">
        <button type="submit" data-cy="add-todo">Add</button>
      </form>

      <ul class="todos" data-cy="todo-list"></ul>

      <div class="toolbar">
        <span data-cy="todo-count"></span>
        <label for="filter" style="margin:0">Show</label>
        <select id="filter" data-cy="filter">
          <option value="all">All</option>
          <option value="active">Active</option>
          <option value="completed">Completed</option>
        </select>
        <button class="secondary" data-cy="clear-completed">Clear completed</button>
      </div>
    </section>
  </main>

  <script>
    let todos = [
      { text: 'Install Cypress', done: true },
      { text: 'Write first test', done: false }
    ];
    const list = document.querySelector('[data-cy=todo-list]');
    const input = document.querySelector('[data-cy=new-todo]');
    const filter = document.querySelector('[data-cy=filter]');
    const countEl = document.querySelector('[data-cy=todo-count]');

    function render() {
      list.innerHTML = '';
      todos
        .map((todo, index) => ({ ...todo, index }))
        .filter((todo) => filter.value === 'all'
          || (filter.value === 'active' && !todo.done)
          || (filter.value === 'completed' && todo.done))
        .forEach((todo) => {
          const li = document.createElement('li');
          li.setAttribute('data-cy', 'todo-item');
          if (todo.done) li.classList.add('completed');

          const checkbox = document.createElement('input');
          checkbox.type = 'checkbox';
          checkbox.checked = todo.done;
          checkbox.setAttribute('data-cy', 'todo-toggle');
          checkbox.addEventListener('change', () => { todos[todo.index].done = checkbox.checked; render(); });

          const span = document.createElement('span');
          span.textContent = todo.text;
          span.setAttribute('data-cy', 'todo-text');

          const del = document.createElement('button');
          del.textContent = 'Delete';
          del.className = 'danger';
          del.setAttribute('data-cy', 'todo-delete');
          del.addEventListener('click', () => { todos.splice(todo.index, 1); render(); });

          li.append(checkbox, span, del);
          list.appendChild(li);
        });
      const left = todos.filter((t) => !t.done).length;
      countEl.textContent = `${left} ${left === 1 ? 'item' : 'items'} left`;
    }

    document.querySelector('[data-cy=todo-form]').addEventListener('submit', (event) => {
      event.preventDefault();
      const text = input.value.trim();
      if (!text) return;
      todos.push({ text, done: false });
      input.value = '';
      render();
    });
    filter.addEventListener('change', render);
    document.querySelector('[data-cy=clear-completed]').addEventListener('click', () => {
      todos = todos.filter((t) => !t.done);
      render();
    });
    render();
  </script>
</body>
</html>
```

### app/products.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Products | Cypress Practice App</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <nav data-cy="nav">
    <a href="index.html" data-cy="nav-home">Home</a>
    <a href="login.html" data-cy="nav-login">Login</a>
    <a href="todo.html" data-cy="nav-todo">Todos</a>
    <a href="products.html" data-cy="nav-products">Products</a>
  </nav>
  <main>
    <h1 data-cy="page-title">Products</h1>
    <input type="text" placeholder="Search products" data-cy="search">
    <p data-cy="loading">Loading products...</p>
    <p class="error" data-cy="error" hidden>Could not load products</p>
    <p data-cy="empty" hidden>No products found</p>
    <ul class="products" data-cy="product-list"></ul>
  </main>

  <script>
    const list = document.querySelector('[data-cy=product-list]');
    const search = document.querySelector('[data-cy=search]');
    const empty = document.querySelector('[data-cy=empty]');
    let products = [];

    function render() {
      const term = search.value.trim().toLowerCase();
      const shown = products.filter((p) => p.name.toLowerCase().includes(term));
      list.innerHTML = '';
      shown.forEach((p) => {
        const li = document.createElement('li');
        li.setAttribute('data-cy', 'product');
        li.innerHTML = `<strong data-cy="product-name"></strong><br><span class="price" data-cy="product-price"></span>`;
        li.querySelector('[data-cy=product-name]').textContent = p.name;
        li.querySelector('[data-cy=product-price]').textContent = `$${p.price.toFixed(2)}`;
        list.appendChild(li);
      });
      empty.hidden = shown.length > 0;
    }

    fetch('api/products.json')
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => { products = data; render(); })
      .catch(() => { document.querySelector('[data-cy=error]').hidden = false; })
      .finally(() => { document.querySelector('[data-cy=loading]').hidden = true; });

    search.addEventListener('input', render);
  </script>
</body>
</html>
```

### app/styles.css

```css
* { box-sizing: border-box; }
body { margin: 0; font-family: Arial, Helvetica, sans-serif; background: #f4f6f8; color: #1f2933; }
nav { display: flex; gap: 16px; padding: 14px 24px; background: #1f2933; }
nav a { color: #fff; text-decoration: none; font-weight: bold; }
nav a:hover { text-decoration: underline; }
main { max-width: 720px; margin: 24px auto; padding: 0 16px; }
.card { background: #fff; border: 1px solid #d9e2ec; border-radius: 8px; padding: 16px; margin-bottom: 16px; }
button { padding: 8px 14px; border: 0; border-radius: 6px; background: #2563eb; color: #fff; cursor: pointer; font-size: 14px; }
button.secondary { background: #64748b; }
button.danger { background: #dc2626; padding: 4px 10px; }
input[type=text], input[type=password], select { padding: 8px; border: 1px solid #9aa5b1; border-radius: 6px; font-size: 14px; }
label { display: block; margin: 10px 0 4px; }
.error { color: #b91c1c; }
.success { color: #15803d; }
.count { display: inline-block; min-width: 40px; text-align: center; font-size: 20px; }
ul.todos { list-style: none; padding: 0; }
ul.todos li { display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid #e4e7eb; }
ul.todos li.completed span { text-decoration: line-through; color: #9aa5b1; }
ul.todos li span { flex: 1; }
.toolbar { display: flex; gap: 12px; align-items: center; margin-top: 12px; }
ul.products { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
ul.products li { background: #fff; border: 1px solid #d9e2ec; border-radius: 8px; padding: 12px; }
.price { color: #2563eb; font-weight: bold; }
```

### app/api/products.json

```json
[
  { "id": 1, "name": "Wireless Mouse", "price": 24.99 },
  { "id": 2, "name": "Mechanical Keyboard", "price": 89.5 },
  { "id": 3, "name": "USB-C Hub", "price": 39 },
  { "id": 4, "name": "Laptop Stand", "price": 45.25 }
]
```
