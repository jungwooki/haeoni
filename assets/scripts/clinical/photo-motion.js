// A gentle movement of original photographs. Text and medical diagrams stay still.
(() => {
  const photos = [...document.querySelectorAll('.photo-motion')];
  if (!photos.length) return;
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = preference.matches;
  const control = document.createElement('button');
  control.type = 'button';
  control.className = 'photo-motion-control';
  const update = () => {
    document.body.classList.toggle('photos-paused', paused);
    control.textContent = paused ? '사진 움직임 재생' : '사진 움직임 멈춤';
    control.setAttribute('aria-pressed', String(paused));
  };
  control.addEventListener('click', () => { paused = !paused; update(); });
  const host = document.querySelector('.page-hero .container');
  if (host) host.append(control);
  preference.addEventListener('change', event => { paused = event.matches; update(); });
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => entry.target.classList.toggle('photo-in-view', entry.isIntersecting));
  }, { threshold: .12 });
  photos.forEach(photo => observer.observe(photo));
  update();
})();
