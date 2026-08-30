const path = require('path');
const crypto = require('crypto');
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Shared classroom password gate. Required because this instance may be
// reachable from the public internet (e.g. remote students) - without it,
// anyone who stumbles on the URL could reach a live credential-harvesting
// page. Set DEMO_USER / DEMO_PASS env vars to choose your own; otherwise a
// random password is generated and printed to the server log on startup.
const DEMO_USER = process.env.DEMO_USER || 'instructor';
const DEMO_PASS = process.env.DEMO_PASS || crypto.randomBytes(5).toString('hex');

function requireAuth(req, res, next) {
  const header = req.headers.authorization || '';
  const [scheme, token] = header.split(' ');

  if (scheme === 'Basic' && token) {
    const [user, pass] = Buffer.from(token, 'base64').toString().split(':');
    if (user === DEMO_USER && pass === DEMO_PASS) {
      return next();
    }
  }

  res.set('WWW-Authenticate', 'Basic realm="Social Engineering Demo"');
  return res.status(401).send('Authentication required.');
}

app.use(requireAuth);

// In-memory only: nothing is ever written to disk or to a database.
// All captured data disappears the moment the server process stops,
// and can be wiped on demand from the instructor dashboard.
const captures = [];

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Warn loudly in the server console so nobody forgets what this is for.
console.log('');
console.log('================================================================');
console.log(' DEMO ENVIRONMENT - Social Engineering / Phishing classroom demo');
console.log(' For local / isolated classroom network use only.');
console.log(' Do NOT expose this server to the public internet.');
console.log(' Do NOT target real people who have not consented.');
console.log('================================================================');
console.log(` Access credentials -> user: ${DEMO_USER}  password: ${DEMO_PASS}`);
console.log('================================================================');
console.log('');

app.get('/', (req, res) => {
  res.redirect('/login.html');
});

app.post('/api/capture', (req, res) => {
  const { username, password } = req.body || {};

  if (typeof username !== 'string' || typeof password !== 'string') {
    return res.status(400).json({ ok: false, error: 'Missing username/password' });
  }

  const entry = {
    id: Date.now() + '-' + Math.random().toString(36).slice(2, 8),
    username,
    password,
    timestamp: new Date().toISOString(),
    ip: req.ip,
  };

  captures.push(entry);
  io.emit('new-capture', entry);

  // Respond exactly like a real phishing page would: no error, so the
  // "victim" (the volunteer/student) doesn't realize anything's wrong yet.
  res.json({ ok: true });
});

app.get('/api/captures', (req, res) => {
  res.json({ ok: true, captures });
});

app.post('/api/clear', (req, res) => {
  captures.length = 0;
  io.emit('cleared');
  res.json({ ok: true });
});

// Socket.io handles its own transport path outside the Express middleware
// chain, so requireAuth above does not cover it - gate it separately here.
io.use((socket, next) => {
  const header = socket.handshake.headers.authorization || '';
  const [scheme, token] = header.split(' ');

  if (scheme === 'Basic' && token) {
    const [user, pass] = Buffer.from(token, 'base64').toString().split(':');
    if (user === DEMO_USER && pass === DEMO_PASS) {
      return next();
    }
  }

  next(new Error('unauthorized'));
});

io.on('connection', (socket) => {
  socket.emit('init', { captures });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Login demo page :  http://localhost:${PORT}/login.html`);
  console.log(`Instructor dashboard: http://localhost:${PORT}/dashboard.html`);
  console.log('');
});
