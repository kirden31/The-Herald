document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.favorite-form').forEach(form => {
    if (form.dataset.inited) return;
    form.dataset.inited = '1';

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = form.querySelector('.favorite-btn');
      const icon = btn.querySelector('i');
      const status = btn.querySelector('.favorite-status');
      btn.disabled = true;

      const originalIconClass = icon.className;
      icon.className = 'spinner-border spinner-border-sm';

      const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
      const url = form.action || '/news/save-favorite/';

      try {
        const response = await fetch(url, {
          method: 'POST',
          body: new FormData(form),
          headers: { 'X-CSRFToken': csrfToken }
        });

        const result = await response.json();

        if (response.ok) {
          if (result.status === 'added') {
            icon.className = 'bi bi-bookmark-star-fill';
            status.textContent = '✔️';
          } else if (result.status === 'removed') {
            icon.className = 'bi bi-bookmark';
            status.textContent = '❌';
          }
        } else {
          icon.className = originalIconClass;
          alert('Failed to update favorites');
        }
      } catch (err) {
        icon.className = originalIconClass;
        alert('Network error');
      } finally {
        btn.disabled = false;
      }
    });
  });
});
