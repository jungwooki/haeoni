(() => {
  const mobile = document.querySelector('.internal-mobile-tools details');
  if (mobile) {
    document.addEventListener('click', event => {
      if (!mobile.contains(event.target)) mobile.open = false;
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && mobile.open) {
        mobile.open = false;
        mobile.querySelector('summary').focus();
      }
    });
  }
})();

// Progressive tabs: without JavaScript, all sections and native disclosures work.
(() => {
  const root = document.querySelector('.tabbed-reading');
  if (!root) return;
  const nav = root.querySelector('.reading-tabs');
  const tabs = [...nav.querySelectorAll('a')];
  const panels = tabs.map(tab => document.getElementById(tab.hash.slice(1)));
  nav.setAttribute('role', 'tablist');
  tabs.forEach((tab, i) => {
    tab.setAttribute('role', 'tab');
    tab.setAttribute('aria-controls', panels[i].id);
    panels[i].setAttribute('role', 'tabpanel');
    panels[i].tabIndex = 0;
  });
  function activate(index) {
    tabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === index));
      tab.tabIndex = i === index ? 0 : -1;
      panels[i].hidden = i !== index;
    });
  }
  function revealHash(scroll = true) {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target || !root.contains(target)) return;
    const panel = target.closest('.reading-tab-panel');
    const index = panels.indexOf(panel);
    if (index < 0) return;
    activate(index);
    for (let node = target; node && node !== panel; node = node.parentElement) {
      if (node.tagName === 'DETAILS') node.open = true;
    }
    if (scroll) requestAnimationFrame(() => target.scrollIntoView({block: 'start', behavior: 'instant'}));
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', event => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      activate(index);
      history.replaceState(null, '', tab.hash);
    });
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      tabs[next].focus();
      tabs[next].click();
    });
  });
  activate(0);
  revealHash();
  window.addEventListener('hashchange', () => revealHash());
  let printState;
  window.addEventListener('beforeprint', () => {
    if (printState) return;
    const details = [...root.querySelectorAll('details')];
    printState = {hidden: panels.map(p => p.hidden), details: details.map(d => [d, d.open])};
    panels.forEach(p => { p.hidden = false; });
    details.forEach(d => { d.open = true; });
  });
  window.addEventListener('afterprint', () => {
    if (!printState) return;
    panels.forEach((p, i) => { p.hidden = printState.hidden[i]; });
    printState.details.forEach(([d, open]) => { d.open = open; });
    printState = null;
  });
})();
