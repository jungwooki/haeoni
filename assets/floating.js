(() => {
  const menu = document.querySelector('.floating-contact');
  if (!menu) return;
  const button = menu.querySelector('.quick-toggle');
  const links = menu.querySelector('.floating-links');
  button.hidden = false;
  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', String(!open));
    button.setAttribute('aria-label', open ? '빠른 메뉴 펼치기' : '빠른 메뉴 접기');
    button.textContent = open ? '문의' : '접기';
    links.hidden = open;
  });
})();
