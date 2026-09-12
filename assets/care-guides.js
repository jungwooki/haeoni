(() => {
  const input = document.querySelector('#care-search');
  const category = document.querySelector('#care-category');
  if (!input || !category) return;
  const entries = [...document.querySelectorAll('.care-entry')];
  const normalize = value => value.normalize('NFKC').replace(/\s/g, '').toLocaleLowerCase('ko');
  const filter = () => {
    const term = normalize(input.value);
    let count = 0;
    entries.forEach(entry => {
      entry.hidden = !(normalize(entry.dataset.name).includes(term) && (!category.value || category.value === entry.dataset.category));
      if (!entry.hidden) count++;
    });
    document.querySelector('.care-count').textContent = `${count}개 항목`;
    document.querySelector('.care-no-results').hidden = count !== 0;
  };
  const openHash = () => {
    const target = document.getElementById(location.hash.slice(1));
    if (target?.classList.contains('care-entry')) {
      input.value = ''; category.value = ''; filter(); target.open = true;
      target.scrollIntoView({block: 'start'});
    }
  };
  document.querySelector('.care-filters').hidden = false;
  input.addEventListener('input', filter);
  category.addEventListener('change', filter);
  window.addEventListener('hashchange', openHash);
  openHash();
})();
