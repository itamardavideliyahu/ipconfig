const socket = io();
const tbody = document.getElementById('captures-body');
const emptyMsg = document.getElementById('empty-msg');
const clearBtn = document.getElementById('clear-btn');
const loginUrlEl = document.getElementById('login-url');

loginUrlEl.textContent = window.location.origin + '/login.html';

function renderCaptures(captures) {
  tbody.innerHTML = '';
  captures.forEach((c) => addRow(c, false));
  emptyMsg.classList.toggle('hidden', captures.length > 0);
}

function addRow(entry, animate) {
  const tr = document.createElement('tr');
  if (animate) tr.classList.add('new-row');

  const time = new Date(entry.timestamp).toLocaleTimeString('he-IL');

  tr.innerHTML =
    '<td>' + time + '</td>' +
    '<td class="username"></td>' +
    '<td class="password"></td>';

  // Set via textContent (not innerHTML) so captured input can never be
  // interpreted as HTML/script - it's still untrusted user input.
  tr.children[1].textContent = entry.username;
  tr.children[2].textContent = entry.password;

  tbody.prepend(tr);
  emptyMsg.classList.add('hidden');
}

socket.on('init', ({ captures }) => {
  renderCaptures(captures);
});

socket.on('new-capture', (entry) => {
  addRow(entry, true);
});

socket.on('cleared', () => {
  renderCaptures([]);
});

clearBtn.addEventListener('click', async () => {
  if (!confirm('למחוק את כל הנתונים שנאספו בהדגמה?')) return;
  await fetch('/api/clear', { method: 'POST' });
});
