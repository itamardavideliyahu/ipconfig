const form = document.getElementById('login-form');
const submitBtn = document.getElementById('submit-btn');
const statusMsg = document.getElementById('status-msg');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  submitBtn.disabled = true;
  submitBtn.textContent = 'מתחבר...';
  statusMsg.textContent = '';

  try {
    await fetch('/api/capture', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
  } catch (err) {
    // Even on network error, continue to the reveal below - this is a
    // teaching demo, not a real attack, so we don't hide failures from
    // the student running it.
  }

  // Immediate debrief: this is the entire point of the exercise -
  // showing the "victim" exactly what just happened.
  form.style.display = 'none';
  statusMsg.innerHTML =
    '<div class="reveal">' +
    '<strong>🎓 זו הייתה הדגמה של מתקפת הנדסה חברתית (Phishing)</strong><br/><br/>' +
    'דף זה חיקה עמוד התחברות מוכר, ומה שהזנת (שם המשתמש והסיסמה) נשלח כרגע ' +
    'לשרת ומוצג בזמן אמת במסך המרצה.<br/><br/>' +
    'בתקיפה אמיתית, זה המקום שבו התוקף היה גונב את פרטי ההתחברות שלך ' +
    'משתמש בהם כדי להתחבר לחשבון האמיתי שלך.<br/><br/>' +
    '<em>לעולם אל תזין/י פרטי התחברות אמיתיים באתר שקישור אליו הגיע ' +
    'ב-SMS/מייל/הודעה ללא אימות זהות השולח וכתובת האתר.</em>' +
    '</div>';
});
