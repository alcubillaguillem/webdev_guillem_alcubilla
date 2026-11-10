// My groups screen: loading, empty, error and success states.
const loading = document.getElementById('groups-loading');
const empty = document.getElementById('groups-empty');
const errorBox = document.getElementById('groups-error');
const list = document.getElementById('groups-list');

async function loadGroups() {
  try {
    const response = await fetch('/api/groups');
    if (response.status === 401) {
      window.location.href = '/login';
      return;
    }
    if (!response.ok) throw new Error();
    const { groups } = await response.json();
    loading.hidden = true;
    if (groups.length === 0) {
      empty.hidden = false;
      return;
    }
    for (const group of groups) {
      const item = document.createElement('li');
      item.className = 'card';
      const name = document.createElement('span');
      name.textContent = group.name;  // textContent, never innerHTML: a group name is user input
      const role = document.createElement('span');
      role.className = 'muted';
      role.textContent = group.role === 'owner' ? 'Owner' : 'Member';
      item.append(name, role);
      list.append(item);
    }
    list.hidden = false;
  } catch {
    loading.hidden = true;
    errorBox.textContent = 'Your groups could not be loaded. Reload the page to try again.';
    errorBox.hidden = false;
  }
}

document.getElementById('logout').addEventListener('click', async () => {
  await fetch('/api/auth/logout', { method: 'POST' });
  window.location.href = '/login';
});

loadGroups();
