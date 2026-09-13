(() => {
  const hero = document.querySelector('.home-carousel');
  if (!hero) return;
  const slides = [...hero.querySelectorAll('.home-slide')];
  const choices = [...hero.querySelectorAll('.hero-choice')];
  let current = 0, paused = false, visible = true, timer;
  const sync = () => {
    clearTimeout(timer);
    if (!paused && visible && !document.hidden) timer = setTimeout(() => show(current + 1), 6000);
  };
  const show = (index, manual = false) => {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => {
      slide.hidden = i !== current;
      slide.classList.toggle('is-entering', i === current);
      choices[i].setAttribute('aria-pressed', String(i === current));
    });
    hero.querySelector('.hero-count').textContent = `0${current + 1} / 03`;
    if (manual) {
      hero.querySelector('.hero-announcement').textContent = slides[current].getAttribute('aria-label');
    }
    sync();
  };
  choices.forEach((choice, i) => choice.addEventListener('click', () => show(i, true)));
  hero.querySelector('.hero-prev').addEventListener('click', () => show(current - 1, true));
  hero.querySelector('.hero-next').addEventListener('click', () => show(current + 1, true));
  hero.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      // Keep focus on a persistent control before hiding the current slide.
      if (slides[current].contains(document.activeElement)) choices[current].focus();
      show(current + (event.key === 'ArrowRight' ? 1 : -1), true);
    }
  });
  hero.addEventListener('focusin', event => {
    paused = slides[current].contains(event.target); sync();
  });
  hero.addEventListener('focusout', () => { setTimeout(() => { paused = slides[current].contains(document.activeElement); sync(); }, 0); });
  document.addEventListener('visibilitychange', sync);
  if ('IntersectionObserver' in window) new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting; sync();
  }).observe(hero);
  let start;
  hero.addEventListener('touchstart', event => {
    if (event.target.closest('a,button') || event.touches.length !== 1) { start = null; return; }
    start = [event.touches[0].clientX, event.touches[0].clientY];
  }, {passive: true});
  hero.addEventListener('touchend', event => {
    if (!start) return;
    const dx = event.changedTouches[0].clientX - start[0];
    const dy = event.changedTouches[0].clientY - start[1];
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) show(current + (dx < 0 ? 1 : -1), true);
    start = null;
  }, {passive: true});
  hero.addEventListener('touchcancel', () => { start = null; });
  hero.querySelector('.home-carousel-controls').hidden = false;
  sync();
})();
