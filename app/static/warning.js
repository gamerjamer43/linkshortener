document.addEventListener('DOMContentLoaded', () => {
  const proceedBtn = document.getElementById('proceedBtn');
  const countdownDiv = document.getElementById('countdown');
  const targetEl = document.getElementById('targetUrl');
  const target = targetEl ? (targetEl.dataset.target || targetEl.textContent.trim()) : null;

  let countdown = 5;
  if (!proceedBtn || !countdownDiv) return;

  proceedBtn.style.opacity = '0.5';
  proceedBtn.style.pointerEvents = 'none';
  proceedBtn.setAttribute('aria-disabled', 'true');

  countdownDiv.textContent = `If you really want to... continue in ${countdown} seconds. BE CAREFUL!`;

  const timer = setInterval(() => {
    countdown--;
    if (countdown >= 0) countdownDiv.textContent = `If you really want to... continue in ${countdown} seconds. BE CAREFUL!`;
    if (countdown < 0) {
      clearInterval(timer);
      proceedBtn.style.opacity = '1';
      proceedBtn.style.pointerEvents = 'auto';
      proceedBtn.removeAttribute('aria-disabled');
      countdownDiv.textContent = '';
    }
  }, 1000);

  proceedBtn.addEventListener('click', function () {
    console.log('user proceeded to external link:', target);
  });
});
