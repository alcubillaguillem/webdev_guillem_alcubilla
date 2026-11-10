// Sign-in form: loading, error and success states.
const form = document.getElementById('login-form');
const button = document.getElementById('login-button');
const errorBox = document.getElementById('login-error');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  errorBox.hidden = true;
  button.disabled = true;
  button.textContent = 'Signing in…';
  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: form.email.value, password: form.password.value }),
    });
    if (response.ok) {
      window.location.href = '/groups';
      return;
    }
    const body = await response.json().catch(() => ({}));
    showError(body.error || 'Could not sign in. Try again.');
  } catch {
    showError('The server cannot be reached. Check your connection and try again.');
  }
});

function showError(message) {
  errorBox.textContent = message;
  errorBox.hidden = false;
  button.disabled = false;
  button.textContent = 'Sign in';
}
