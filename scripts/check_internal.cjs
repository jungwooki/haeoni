const {chromium}=require('playwright');
const path=require('path');
const assert=require('assert');
const root=path.resolve(__dirname,'..');
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const page=await browser.newPage(); const errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 const base='file://'+root+'/';
 const files=['clinic-internal.html',...require(path.join(root,'content/internal-pages.json')).map(p=>p.file)];
 for(const width of [1440,390,320]){
  await page.setViewportSize({width,height:900});
  for(const file of files){
   await page.goto(base+file);await page.waitForTimeout(70);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`overflow ${width} ${file}`);
   await page.locator('main img').evaluateAll(imgs=>Promise.all(imgs.map(i=>{i.loading='eager';return i.decode()})));
  }
  await page.goto(base+'clinic-internal.html');
  
  await page.getByRole('link',{name:'내 증상에 맞는 안내 찾기'}).click();
  assert(await page.locator('#symptom-guides').evaluate(e=>e.getBoundingClientRect().top>=110));
  await page.goto(base+'internal-diagnosis.html');
  if(width<800){
   const menu=page.locator('.mobile-reading-nav');
   await menu.locator('summary').click();assert(await menu.evaluate(e=>e.open));
   await page.keyboard.press('Escape');assert(!(await menu.evaluate(e=>e.open)));
   await menu.locator('summary').click();
   await page.mouse.click(2,250);assert(!(await menu.evaluate(e=>e.open)));
  }
  assert.equal(await page.locator('[data-image-modal],dialog,.visual-enlarge').count(),0);

 }
 const plain=await browser.newPage({javaScriptEnabled:false,viewport:{width:390,height:844}});
 await plain.goto(base+'internal-diagnosis.html');await plain.locator('.mobile-reading-nav summary').click();
 assert(await plain.locator('.mobile-reading-nav').evaluate(e=>e.open));
 assert(await plain.locator('.visual-image-frame img').first().isVisible());
 assert.equal(errors.length,0,errors.join('\n'));
 console.log('PASS: 11 pages at 1440/390/320px; no overflow or broken images; symptom anchors; mobile menu; plain images; JavaScript-free fallback; no script errors.');
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
