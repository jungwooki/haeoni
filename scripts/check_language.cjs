// Exercise asynchronous translation and recovery without contacting Google.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, '../assets/scripts/shared/language.js'), 'utf8');
function setup(saved = 'ko') {
  const elements = {};
  function element(extra = {}) {
    return Object.assign({ attrs: {}, listeners: {}, textContent: '', hidden: true,
      setAttribute(k,v) { this.attrs[k] = v; }, removeAttribute(k) { delete this.attrs[k]; },
      toggleAttribute(k,on) { if (on) this.attrs[k] = ''; else delete this.attrs[k]; },
      addEventListener(k,fn) { this.listeners[k] = fn; },
      querySelector(k) { return elements[k]; }
    }, extra);
  }
  elements['.language-ko'] = element({dataset: {original: 'https://haeoni.com/index.html'}, querySelector: () => ({src:'kr.svg'})});
  elements['.language-ja'] = element({querySelector: () => ({src:'jp.svg'})});
  for (const name of ['.language-flag','.language-code','.language-status','summary']) elements[name] = element();
  const menu = element({ open: true });
  let tick, script, combo, translated = false, reloads = 0;
  const cookies = [];
  const document = {querySelector: s => s === '.header-language' ? menu : combo,
    documentElement: {classList: {contains: () => translated}},
    addEventListener() {}, createElement: () => element({remove() { script = null; }}),
    getElementById: () => script, head: {appendChild(s) { script = s; }} };
  Object.defineProperty(document, 'cookie', {get: () => '', set: v => cookies.push(v)});
  const context = { document, location: {hostname: 'haeoni.com', pathname: '/index.html', hash: '', reload() { reloads++; }},
    sessionStorage: {getItem: () => saved, setItem: (_,v) => {saved = v;}},
    setInterval(fn) { tick = fn; return 1; }, clearInterval() { tick = null; }, Event: class {}, window: {} };
  vm.runInNewContext(source, context);
  return { elements, menu, cookies, context, click(name) {elements[name].listeners.click({preventDefault(){}});},
    tick() { if(tick) tick(); }, script: () => script, saved: () => saved, reloads: () => reloads,
    ready() { combo = { value: '', dispatchEvent() { translated = true; } }; } };
}
let app = setup();
assert.equal(app.script(), undefined, 'Korean must not load third-party translation');
app.click('.language-ja');
assert.match(app.script().src, /translate_a\/element.js/);
app.tick();
assert.notEqual(app.elements['.language-code'].textContent, 'JA', 'Do not claim translation before completion');
app.ready(); app.tick();
assert.equal(app.elements['.language-code'].textContent, 'JA');
assert.equal(app.elements['.language-flag'].src, 'jp.svg');
assert.equal(app.saved(), 'ja');
assert.equal(app.menu.open, false);
app.click('.language-ko');
assert.equal(app.saved(), 'ko'); assert.equal(app.reloads(), 1);
assert(app.cookies.some(c => c.includes('Max-Age=0; path=/; domain=haeoni.com')));
app = setup('ja'); assert(app.script(), 'Continue Japanese on next page');
app.script().onerror(); assert.equal(app.menu.open, true);
assert.match(app.elements['.language-status'].textContent, /다시 선택/);
app.click('.language-ja'); assert(app.script(), 'Retry after script failure');
for(let i=0;i<80;i++) app.tick();
assert.match(app.elements['.language-status'].textContent, /다시 선택/);
assert.equal(app.menu.attrs['aria-busy'], undefined);
console.log('PASS: lazy loading, delayed translation, language persistence, Korean restoration, load failure/retry and timeout.');
