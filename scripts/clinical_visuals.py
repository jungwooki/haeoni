# -*- coding: utf-8 -*-
"""Shared visual-first department intros and unique source-image placement."""
from pathlib import Path
from html import escape as esc
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/'content/visual-guides.json').read_text())
ARTICLES=sum([json.loads((ROOT/'content'/name).read_text()) for name in ['internal-pages.json','family-pages.json','digestive-pages.json']],[])
CANONICAL={};PLACEMENTS={};_hashes={};_cache={}
def register(image,page,anchor):
 path=image['path']
 if path not in _cache:_cache[path]=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
 canonical=_hashes.setdefault(_cache[path],path);CANONICAL[path]=canonical
 PLACEMENTS.setdefault(canonical,(page,anchor))
 return canonical
for page,cfg in CONFIG.items():
 if cfg.get('image'):
  path=register(cfg['image'],page,'visual-intro')
  assert PLACEMENTS[path]==(page,'visual-intro'),('duplicate opening image',page,path)
 for n,feature in enumerate(cfg.get('features',[])):
  path=register(feature['image'],page,'feature-'+str(n))
  assert PLACEMENTS[path]==(page,'feature-'+str(n)),('duplicate feature image',page,path)
for page in ARTICLES:
 for idx,section in enumerate(page['sections']):
  for item in section['items']:
   if item['type']=='image':register(item,page['file'],'guide-'+str(idx))

def image_html(item,opening=False):
 path=CANONICAL[item['path']];alt=esc(item['alt'],quote=True)
 priority='fetchpriority="high"' if opening else 'loading="lazy"'
 # Inline diagrams and source charts retain their full original extent.
 return f'<div class="visual-image-frame"><img src="{path}" alt="{alt}" width="{item["width"]}" height="{item["height"]}" {priority}></div>'

def source_image(item,page,idx,seen):
 path=CANONICAL[item['path']];owner,anchor=PLACEMENTS[path]
 token=(owner,anchor,path)
 if token in seen:return ''
 seen.add(token)
 if (page,'guide-'+str(idx))!=(owner,anchor):
  return ''
 return '<figure class="clinical-figure">'+image_html(item)+'</figure>'

def diagram(cfg,title):
 digestive=cfg.get('diagram') in ['upper-digestive','lower-digestive']
 if digestive:
  organ='<path d="M147 30v70c0 28 32 20 33-2 25-14 63 10 62 48-1 43-42 55-66 42-23-12-21-30-44-28-13 1-16 11-17 24"/>' if cfg['diagram']=='upper-digestive' else '<path d="M106 75q-25 0-25 25v100q0 20 22 20h118q23 0 23-23V100q0-25-25-25H106zm14 42h76q20 0 20 17t-20 17h-60q-20 0-20 17t20 17h60m-33 35v29"/>'
  icon=f'<svg viewBox="0 0 320 270" role="img" aria-label="{esc(title,quote=True)} 증상 위치 개념도"><rect x="30" y="15" width="260" height="240" rx="95" fill="#f4e7d5"/><g fill="none" stroke="#b56d4d" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">{organ}</g></svg>'
 else:
  icon='<svg viewBox="0 0 320 150" role="img" aria-label="기록과 진찰, 상담을 연결하는 진료 개념도"><path d="M58 76H263" stroke="#c3b59f" stroke-width="2" stroke-dasharray="5 7"/><g fill="#fffaf2" stroke="#8eaa99" stroke-width="2"><circle cx="60" cy="75" r="38"/><circle cx="160" cy="75" r="38"/><circle cx="260" cy="75" r="38"/></g><g fill="none" stroke="#547665" stroke-width="3" stroke-linecap="round"><path d="M48 53h24v44H48zm6 14h12m-12 10h12m-12 10h8M150 58v22q0 16 14 16t14-16v-9m-31-13h6m22 0h6M245 62h30v21h-12l-10 9v-9h-8z"/></g></svg>'
 return '<figure class="visual-diagram">'+icon+'<ol>'+''.join('<li><span>'+str(n)+'</span>'+esc(p)+'</li>' for n,p in enumerate(cfg['points'],1))+'</ol></figure>'

def visual_hero(name,title,group_url,group):
 cfg=CONFIG[name];hub=name.startswith('clinic-');headline=cfg['headline']
 breadcrumbs=f'<nav class="breadcrumbs" aria-label="현재 위치"><a href="index.html">홈</a><span>/</span><a href="{group_url}">{group}</a><span>/</span><span aria-current="page">{esc(title)}</span></nav>'
 if cfg.get('image'):
  visual='<figure class="visual-opening-photo">'+image_html(cfg['image'],True)+'</figure>'
 else:visual=diagram(cfg,title)
 copy=('<p class="eyebrow">'+esc(title)+' · HAEON CARE</p><h1>'+headline+'</h1><p class="visual-lead">'+esc(cfg['description'])+'</p>') if hub else ('<p class="eyebrow">'+esc(group)+' · HEALTH GUIDE</p><h1>'+esc(title)+'</h1><p class="visual-lead">'+esc(headline)+'</p>')
 points='<ul class="visual-keypoints">'+''.join('<li>'+esc(p)+'</li>' for p in cfg['points'])+'</ul>'
 action='#care-paths' if hub else '#reading-overview' if name.startswith('internal-') else '#guide-0'
 return '<section class="clinical-visual-hero '+('visual-hub' if hub else 'visual-article')+'" id="visual-intro"><div class="container">'+breadcrumbs+'<div class="visual-opening-grid"><div class="visual-opening-copy">'+copy+points+f'<a class="visual-primary" href="{action}">'+('내게 맞는 안내 찾기' if hub else '자세한 내용 읽기')+' <span aria-hidden="true">↓</span></a></div>'+visual+'</div></div></section>'

def feature_cards(dept):
 return '<div class="warm-photo-grid">'+''.join(f'<a class="warm-photo-card" id="feature-{n}" href="{f["url"]}"><img src="{CANONICAL[f["image"]["path"]]}" alt="{esc(f["image"]["alt"],quote=True)}" width="{f["image"]["width"]}" height="{f["image"]["height"]}" loading="lazy"><div><h3>{f["title"]}</h3><span>자세히 보기 →</span></div></a>' for n,f in enumerate(CONFIG['clinic-'+dept+'.html']['features']))+'</div>'

def care_flow(dept):
 if dept=='internal':
  title='검사와 변증진단, 두 시각을 함께 봅니다.'
  nodes=[('객관적으로 확인','진찰과 기존 검사 결과를 검토하고, 필요한 검사를 판단합니다.'),('패턴으로 이해','증상·식사·수면·배변 등 몸의 반응을 한의학적으로 살핍니다.'),('함께 설명','검사 소견과 패턴을 종합해 치료와 관리의 방향을 이야기합니다.')]
 elif dept=='child':
  title='아이의 변화를 함께 이해하는 진료.'
  nodes=[('듣고 관찰하기','아이의 불편과 보호자가 느낀 변화를 듣습니다.'),('상태 확인하기','진찰과 성장 기록, 필요한 검사 결과를 살핍니다.'),('일상으로 이어가기','진료 계획과 집에서 챙길 부분을 함께 이야기합니다.')]
 else:
  title='지금의 시기와 일상을 함께 살핍니다.'
  nodes=[('변화 듣기','생애주기와 현재의 불편을 편안하게 나눕니다.'),('함께 살피기','진찰과 기존 검사, 치료 과정을 함께 검토합니다.'),('방향 정하기','몸의 상태와 일상에 맞는 진료 방향을 설명합니다.')]
 return '<section class="care-flow"><p class="eyebrow">해온의 진료를 이해하는 세 단계</p><h2>'+title+'</h2><ol>'+''.join('<li><span>'+f'{n:02}'+'</span><h3>'+h+'</h3><p>'+p+'</p></li>' for n,(h,p) in enumerate(nodes,1))+'</ol></section>'
