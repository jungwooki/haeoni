(() => {
  const menu = document.querySelector('.header-language');
  if (!menu) return;
  const korean = menu.querySelector('.language-ko');
  const japanese = menu.querySelector('.language-ja');
  const translated = location.hostname.endsWith('.translate.goog');
  if (translated) {
    menu.querySelector('.language-flag').textContent = '🇯🇵';
    menu.querySelector('.language-code').textContent = 'JA';
    korean.removeAttribute('aria-current');
    japanese.setAttribute('aria-current', 'true');
    korean.href = korean.dataset.original;
    korean.addEventListener('click', (event) => {
      event.preventDefault();
      location.assign(korean.dataset.original + location.hash);
    });
  }
  document.addEventListener('click', (event) => {
    if (!menu.contains(event.target)) menu.open = false;
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu.open) {
      menu.open = false;
      menu.querySelector('summary').focus();
    }
  });
})();
