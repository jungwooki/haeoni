(() => {
  const menu = document.querySelector('.header-language');
  if (!menu) return;
  const korean = menu.querySelector('.language-ko');
  const japanese = menu.querySelector('.language-ja');
  const flag = menu.querySelector('.language-flag');
  const status = menu.querySelector('.language-status');
  const key = 'haeon-language';
  let desired = 'ko';
  let loading = false;
  let timer;
  const remember = (lang) => {
    try { sessionStorage.setItem(key, lang); } catch (_) { /* Storage may be disabled. */ }
  };
  const message = (text) => {
    status.textContent = text;
    status.hidden = !text;
  };
  const showLanguage = (lang) => {
    flag.src = (lang === 'ja' ? japanese : korean).querySelector('img').src;
    menu.querySelector('.language-code').textContent = lang.toUpperCase();
    korean.toggleAttribute('aria-current', lang === 'ko');
    japanese.toggleAttribute('aria-current', lang === 'ja');
    (lang === 'ja' ? japanese : korean).setAttribute('aria-current', 'true');
  };
  const isJapanese = () => document.documentElement.classList.contains('translated-ltr') ||
    document.documentElement.classList.contains('translated-rtl');
  const failed = () => {
    clearInterval(timer);
    loading = false;
    menu.removeAttribute('aria-busy');
    message('번역을 불러오지 못했습니다. 잠시 후 日本語를 다시 선택해 주세요. 翻訳を読み込めません。もう一度お試しください。');
    menu.open = true;
  };
  const translate = () => {
    desired = 'ja';
    remember('ja');
    if (loading) return;
    loading = true;
    menu.setAttribute('aria-busy', 'true');
    message('일본어로 번역 중입니다… 翻訳中…');
    let elapsed = 0;
    let requested = false;
    timer = setInterval(() => {
      if (desired !== 'ja') { clearInterval(timer); return; }
      const select = document.querySelector('#google-translate-element .goog-te-combo');
      if (select && !requested) {
        select.value = 'ja';
        select.dispatchEvent(new Event('change', { bubbles: true }));
        requested = true;
      }
      if (isJapanese()) {
        clearInterval(timer);
        loading = false;
        menu.removeAttribute('aria-busy');
        showLanguage('ja');
        message('');
        menu.open = false;
      } else if ((elapsed += 250) >= 20000) failed();
    }, 250);
    if (!document.getElementById('haeon-translate-script')) {
      window.haeonTranslateReady = () => {
        try {
          new window.google.translate.TranslateElement({
            pageLanguage: 'ko', includedLanguages: 'ja', autoDisplay: false
          }, 'google-translate-element');
        } catch (_) { failed(); }
      };
      const script = document.createElement('script');
      script.id = 'haeon-translate-script';
      script.src = 'https://translate.google.com/translate_a/element.js?cb=haeonTranslateReady';
      script.onerror = () => { script.remove(); failed(); };
      document.head.appendChild(script);
    }
  };
  japanese.addEventListener('click', (event) => {
    event.preventDefault();
    translate();
  });
  korean.addEventListener('click', (event) => {
    // Legacy Google proxy pages must return to the original site's URL.
    if (location.hostname.endsWith('.translate.goog')) {
      event.preventDefault();
      location.assign(korean.dataset.original + location.hash);
      return;
    }
    event.preventDefault();
    desired = 'ko';
    remember('ko');
    clearInterval(timer);
    // Google uses both host-only and domain cookies; clear every applicable scope.
    const domains = location.hostname.split('.');
    const paths = location.pathname.split('/');
    while (paths.length) {
      const path = paths.join('/') || '/';
      document.cookie = `googtrans=; Max-Age=0; path=${path}`;
      for (let i = 0; i < domains.length - 1; i++) {
        document.cookie = `googtrans=; Max-Age=0; path=${path}; domain=${domains.slice(i).join('.')}`;
      }
      paths.pop();
    }
    location.reload();
  });
  if (location.hostname.endsWith('.translate.goog')) {
    showLanguage('ja');
    korean.href = korean.dataset.original;
  } else {
    try { desired = sessionStorage.getItem(key) || 'ko'; } catch (_) { /* Use Korean. */ }
    if (desired === 'ja' || /(?:^|;\s*)googtrans=\/ko\/ja(?:;|$)/.test(document.cookie)) translate();
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
