// Create-account form: loading, error and success states.
const form = document.getElementById('register-form');
const button = document.getElementById('register-button');
const errorBox = document.getElementById('register-error');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  errorBox.hidden = true;
  button.disabled = true;
  button.textContent = 'Creating account…';
  try {
    const response = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: form.name.value, email: form.email.value, password: form.password.value }),
    });
    if (response.ok) {
      window.location.href = '/groups';
      return;
    }
    const body = await response.json().catch(() => ({}));
    showError(body.error || 'Could not create the account. Try again.');
  } catch {
    showError('The server cannot be reached. Check your connection and try again.');
  }
});

function showError(message) {
  errorBox.textContent = message;
  errorBox.hidden = false;
  button.disabled = false;
  button.textContent = 'Create account';
}
