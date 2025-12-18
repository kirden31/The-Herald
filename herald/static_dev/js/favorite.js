document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.favorite-form').forEach(form => {
    if (form.dataset.inited) return;
    form.dataset.inited = '1';

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = form.querySelector('.favorite-btn');
      const originalHTML = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';

      const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

      const url = form.action || '/news/save-favorite/';

      try {
        const response = await fetch(url, {
          method: 'POST',
          body: new FormData(form),
          headers: {
            'X-CSRFToken': csrfToken,
          }
        });

        const result = await response.json();

        if (response.ok) {
          if (result.status === 'added') {
            btn.className = 'btn btn-sm btn-warning favorite-btn';
            btn.innerHTML = '<i class="bi bi-bookmark-star-fill"></i> В избранном';
          } else if (result.status === 'removed') {
            btn.className = 'btn btn-sm btn-outline-warning favorite-btn';
            btn.innerHTML = '<i class="bi bi-bookmark"></i> Сохранить';
          }
        } else {
          btn.innerHTML = originalHTML;
          alert('Не удалось обновить избранное.');
        }
      } catch (err) {
        btn.innerHTML = originalHTML;
        alert('Ошибка сети.');
      } finally {
        btn.disabled = false;
      }
    });
  });
});