#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check generated pages, navigation, assets, anchors and source preservation."""
from page_routes import is_hub
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
from publication_review import public_html, edited_text, OVERRIDES
from clinical_visuals import WITHHELD
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.refs=[];self.h1=0;self.words=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  for k in ['href','src']:
   if a.get(k):self.refs.append(a[k])
 def handle_data(self,s):self.words.append(s)
names=json.loads((ROOT/'content/generated-pages.json').read_text());pages={}
for name in names:
 p=Page();p.feed((ROOT/name).read_text());pages[name]=p
 assert p.h1==1,(name,'h1 count')
 assert len(set(p.ids))==len(p.ids),(name,'duplicate IDs')
 for ref in p.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  dest=ROOT/unquote(u.path) if u.path else ROOT/name
  assert dest.is_file() and dest.stat().st_size,(name,ref)
for name,p in pages.items():
 for ref in p.refs:
  u=urlsplit(ref)
  if not u.scheme and u.fragment:
   dest=u.path or name
   if dest in pages:assert u.fragment in pages[dest].ids,(name,ref)
 for required in ['departments.html','01_2.team.html','01_1.about.html','time.html']:
  assert required in p.refs,(name,required)
# Every word of each captured doctor profile remains in the rendered page.
def normalize(t):return re.sub(r'\s+','',t).replace('\u2800','')
for slug,raw in json.loads((ROOT/'content/doctors-original.json').read_text()).items():
 rendered=normalize(' '.join(pages['doctor-'+slug+'.html'].words))
 for line in raw.splitlines()[1:]:assert normalize(line) in rendered,(slug,line)
print(f'PASS: {len(names)} pages; local links/assets; anchor targets; shared navigation; 4 complete doctor profiles.')
# Check complete source text and all diagnostic/educational images, not just file counts.
for article in json.loads((ROOT/'content/internal-pages.json').read_text())+json.loads((ROOT/'content/family-pages.json').read_text())+json.loads((ROOT/'content/digestive-pages.json').read_text()):
 page=pages[article['file']]
 rendered=normalize(' '.join(page.words))
 for section in article['sections']:
  for item in section['items']:
   if item['type']=='text':
    reviewed=Page();reviewed.feed(public_html(item['html']))
    assert normalize(' '.join(reviewed.words)) in rendered,(article['file'],'reviewed source text omitted',item.get('text','')[:60])
 for section in article['sections']:
  for item in section['items']:
   if item['type']=='image' and item['path'] not in WITHHELD:
    from clinical_visuals import CANONICAL, PLACEMENTS
    canonical=CANONICAL[item['path']]
    owner,anchor=PLACEMENTS[canonical]
    assert canonical in pages[owner].refs,(owner,item['path'])
    assert anchor in pages[owner].ids,(owner,'missing image placement')
   if item['type'] in ['link','embed']:assert item['url'].replace('https://haeoni.com/d','care-diagnostic.html') in page.refs,(article['file'],item['url'])
for name in json.loads((ROOT/'content/floating-pages.json').read_text()):
 s=(ROOT/name).read_text();p=Page();p.feed(s)
 assert s.count('class="floating-contact"')==1,(name,'floating menu missing/duplicated')
 assert p.ids.count('floating-links')==1,(name,'duplicate quick menu ID')
 for ref in ['assets/styles/shared/floating.css','assets/scripts/shared/floating.js','https://pf.kakao.com/_sYeKE','https://m.booking.naver.com/booking/6/bizes/150330','01_3.location.html']:
  assert ref in p.refs,(name,ref)
print('PASS: internal, pediatric and women’s reviewed text and retained images/resources present; floating menu on every published page.')
for route in json.loads((ROOT/'content/family-routes.json').read_text()):
 assert route['target'] in pages,route
print('PASS: all 46 original pediatric/women’s menu destinations mapped.')

# Every opening has a meaningful photo/diagram; source images are unique across departments.
from collections import Counter
from clinical_visuals import CONFIG
images=[]
for name,cfg in CONFIG.items():
 html=(ROOT/name).read_text()
 images+=re.findall(r'<img[^>]+src="([^"]+)"',html)
 assert 'assets/scripts/clinical/internal.js' in html and 'assets/styles/clinical/clinical-visuals.css' in html,name
 assert 'id="visual-intro"' in html and 'class="visual-keypoints"' in html,name
 if cfg.get('image'):assert cfg['image']['path'] in pages[name].refs,name
 else:assert 'class="visual-diagram"' in html,name
 if not is_hub(name):assert 'class="internal-mobile-tools"' in html,name
counts=Counter(p for p in images if not p.endswith('/logo.jpg'))
assert all(n==1 for n in counts.values()),[(p,n) for p,n in counts.items() if n>1]
import hashlib
assert len({hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in counts})==len(counts),'duplicate image content'
for slug in ['digestive','functional-digestive','upper-digestive','lower-digestive']:
 name='internal-'+slug+'.html'
 assert name in pages and name in pages['clinic-internal.html'].refs,name
 assert name in pages['sitemap.html'].refs,name
print(f'PASS: {len(CONFIG)} visual openings; {len(counts)} unique images; 4 linked digestive guides; mobile menus.')
# Shared menu order, explicit specialty destinations, original clinic photographs.
import hashlib
expected=['한방내과','소아과','부인과','체질보약','통증재활','다이어트','스포츠 MPS']
for name in names:
 html=(ROOT/name).read_text()
 strip=re.search(r'<nav class="department-bar".*?</nav>',html,re.S).group(0)
 positions=[strip.index(label) for label in expected]
 assert positions==sorted(positions),(name,'department order')
 assert 'assets/styles/shared/unified.css' in html,(name,'shared styles')
 assert 'https://haeonw.com' in strip and 'https://haeon.sportsmps.com/' in strip
 assert 'specialty-diet' in strip and 'specialty-sports' in strip
assert 'hero-play' not in (ROOT/'index.html').read_text()
for photo in json.loads((ROOT/'content/clinic-photo-inventory.json').read_text()):
 assert hashlib.sha256((ROOT/photo['path']).read_bytes()).hexdigest()==photo['sha256']
 if photo['width']>500:
  assert any(photo['path'] in p.refs for p in pages.values()),('clinic photo not displayed',photo['path'])
for p in json.loads((ROOT/'content/family-pages.json').read_text()):
 if p['slug'].startswith('women-'):
  html=(ROOT/p['file']).read_text()
  assert 'tabbed-reading' in html and 'source-chapter' in html
print('PASS: unified menus; specialty links; clinic source image integrity and display; women’s reading tabs; no playback toggle.')

# Public guides must not expose withdrawn/planned offerings or silently lose source mappings.
guide_data=json.loads((ROOT/'content/care-guides.json').read_text())
for kind,items in guide_data.items():
 if not isinstance(items,list):continue
 html=(ROOT/f'care-{kind}.html').read_text()
 assert html.count('class="care-notice"')==1,(kind,'footer notice')
 assert html.count('class="care-entry"')==sum(x.get('publication_status','current')=='current' for x in items)
 for item in items:
  anchor='id="item-'+item['id']+'"'
  assert (anchor in html)==(item.get('publication_status','current')=='current'),item['id']
  assert item['caution'] and item['limit'],item['id']
 for forbidden in ['대학병원급','재생 속도를 30%','감염 걱정 없음','위험 원천 차단']:
  assert forbidden not in html,(kind,forbidden)
 source=json.loads((ROOT.parent/'emr/guides'/f'{kind}.json').read_text())['data']
 mapped=[sid for item in items for sid in item['source_ids'] if not sid.startswith('USER_')]
 assert sorted(mapped)==sorted(x['id'] for x in source),(kind,'source coverage')
for name in names:
 assert 'href="care.html"' in (ROOT/name).read_text(),(name,'shared care menu')
print('PASS: care source coverage; planned/withdrawn offerings excluded; cautions and shared entry links.')

# An old domain must never reappear in a published navigation/resource URL.
for name,p in pages.items():
 for ref in p.refs:
  assert urlsplit(ref).hostname not in ('haeoni.com','www.haeoni.com'),(name,ref)
redirects=json.loads((ROOT/'content/legacy-redirects.json').read_text())
for name,target in redirects.items():
 assert target in pages and 'url='+target in (ROOT/name).read_text(),(name,target)
# Every scoped editorial replacement remains tied to its original captured block.
import hashlib
for item in OVERRIDES:
 assert hashlib.sha256(item['original_html'].encode()).hexdigest()==item['source_sha256']
 reviewed=Page();reviewed.feed(public_html(item['html']))
 assert normalize(' '.join(reviewed.words)) in normalize(' '.join(pages[item['page']].words)),item['page']
print('PASS: old-domain links absent; legacy routes redirect; reviewed public copy present.')

for image_path in WITHHELD:
 assert not any(image_path in p.refs for p in pages.values()),image_path
print('PASS: withheld clinical charts remain outside public pages.')
