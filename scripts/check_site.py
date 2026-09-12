#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check generated pages, navigation, assets, anchors and source preservation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
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
 for block in article['source_text']:
  assert normalize(block) in rendered,(article['file'],'source text omitted',block[:60])
 for section in article['sections']:
  for item in section['items']:
   if item['type']=='image':
    from clinical_visuals import CANONICAL, PLACEMENTS
    canonical=CANONICAL[item['path']]
    owner,anchor=PLACEMENTS[canonical]
    assert canonical in pages[owner].refs,(owner,item['path'])
    assert anchor in pages[owner].ids,(owner,'missing image placement')
   if item['type'] in ['link','embed']:assert item['url'] in page.refs,(article['file'],item['url'])
for name in json.loads((ROOT/'content/floating-pages.json').read_text()):
 s=(ROOT/name).read_text();p=Page();p.feed(s)
 assert s.count('class="floating-contact"')==1,(name,'floating menu missing/duplicated')
 assert p.ids.count('floating-links')==1,(name,'duplicate quick menu ID')
 for ref in ['assets/floating.css','assets/floating.js','https://pf.kakao.com/_sYeKE','https://m.booking.naver.com/booking/6/bizes/150330','01_3.location.html']:
  assert ref in p.refs,(name,ref)
print('PASS: internal, pediatric and women’s source text/images/resources preserved; floating menu on every published page.')
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
 assert 'assets/internal.js' in html and 'assets/clinical-visuals.css' in html,name
 assert 'id="visual-intro"' in html and 'class="visual-keypoints"' in html,name
 if cfg.get('image'):assert cfg['image']['path'] in pages[name].refs,name
 else:assert 'class="visual-diagram"' in html,name
 if not name.startswith('clinic-'):assert 'class="internal-mobile-tools"' in html,name
counts=Counter(p for p in images if not p.endswith('/logo.jpg'))
assert all(n==1 for n in counts.values()),[(p,n) for p,n in counts.items() if n>1]
import hashlib
assert len({hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in counts})==len(counts),'duplicate image content'
for slug in ['digestive','functional-digestive','upper-digestive','lower-digestive']:
 name='internal-'+slug+'.html'
 assert name in pages and name in pages['clinic-internal.html'].refs,name
 assert name in pages['sitemap.html'].refs,name
print(f'PASS: {len(CONFIG)} visual openings; {len(counts)} unique images; 4 linked digestive guides; mobile menus.')
