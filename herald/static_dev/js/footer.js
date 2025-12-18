document.addEventListener('DOMContentLoaded', function () {
  const footer = document.querySelector('footer');
  const serverTimeStr = footer ? footer.dataset.serverTime : null;

  const serverDate = serverTimeStr ? Date.parse(serverTimeStr) : null;
  const now = Date.now();

  let displayDate = new Date(now);

  if (serverDate) {
    const diffTime = Math.abs(serverDate - now);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    displayDate = new Date(diffDays < 1 ? now : serverDate);
  }

  const yearSpan = document.getElementById('year');
  if (yearSpan) {
    yearSpan.textContent = displayDate.getFullYear();
  }
});
