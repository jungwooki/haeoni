# -*- coding: utf-8 -*-
"""Render source-backed internal medicine articles; pure standard library."""
from pathlib import Path
from publication_review import public_html
from html import escape
import json,re
from clinical_visuals import CONFIG, source_image, feature_cards, care_flow
from internal_reading import reading_tabs
ROOT=Path(__file__).resolve().parents[1]
PAGES=json.loads((ROOT/'content/internal-pages.json').read_text())+json.loads((ROOT/'content/digestive-pages.json').read_text())
MOVING=set(json.loads((ROOT/'content/moving-photos.json').read_text()))
GROUPS=[('소화기내과',['digestive','functional-digestive','upper-digestive','lower-digestive']),('호흡기 진료와 관리',['respiratory','cotton-care']),('비염·축농증',['rhinitis','nose-function','diagnosis','rhinitis-treatment']),('기침·천식',['cough','cough-treatment']),('감기·중이염',['cold','otitis'])]
DESCS={'respiratory':'알레르기, 면역, 호흡기 질환을 함께 살핍니다.','cotton-care':'코와 목의 관리, 매일의 작은 습관에서 시작합니다.','rhinitis':'비염은 치료와 생활관리를 함께 생각해야 합니다.','nose-function':'호흡부터 방어까지, 코의 역할을 알아봅니다.','diagnosis':'증상과 몸의 상태를 함께 살피는 해온의 변증진단 안내.','rhinitis-treatment':'코의 증상 조절과 기능 회복을 함께 살핍니다.','cough':'반복되는 기침, 원인과 양상부터 차근차근 살핍니다.','cough-treatment':'기침의 양상과 시기에 따른 치료·생활관리 안내.','cold':'감기·독감에 대한 한의학적 관점과 생활관리 안내.','otitis':'귀의 불편감부터 원인과 증상, 치료까지 알아봅니다.'}
LABELS={'rhinitis':{1:'비염, 치료와 관리의 관점'},'nose-function':{1:'비염에 관한 기존 조사 자료'},'diagnosis':{1:'변증진단과 일반적인 코 상태'},'rhinitis-treatment':{1:'만성 비염의 영향과 치료 방향'},'cough-treatment':{2:'진료 전 준비와 생활관리'}}
def figure(item):
 return f'<figure class="clinical-figure"><img src="{item["path"]}" alt="{escape(item["alt"],quote=True)}" width="{item["width"]}" height="{item["height"]}" loading="lazy"></figure>'

def render_item(i):
 if i['type']=='image':return figure(i)
 if i['type']=='text':return '<div class="source-text">'+public_html(i['html'])+'</div>'
 if i['type']=='link':return f'<a class="article-resource" href="{escape(i["url"],quote=True)}">{escape(i["label"])} <span aria-hidden="true">↗</span></a>'
 if i['type']=='embed':
  url=escape(i['url'],quote=True)
  return f'<div class="document-resource"><iframe src="{url}" title="{i["title"]}" loading="lazy" allowfullscreen></iframe><a class="article-resource" href="{url}" target="_blank" rel="noopener noreferrer">안내자료를 새 창에서 보기 ↗</a></div>'
 return ''
def photo_links(entries):
 cards=[]
 for page,label in entries:
  item=next((i for sec in page['sections'] for i in sec['items'] if i['type']=='image' and i['path'] in MOVING),None)
  if item is None:continue
  cards.append('<article class="photo-guide"><div class="photo-motion"><a href="'+page['file']+'"><img src="'+item['path']+'" alt="'+escape(item['alt'],quote=True)+'" width="'+str(item['width'])+'" height="'+str(item['height'])+'" loading="lazy"></a></div><h3><a href="'+page['file']+'">'+label+' <span aria-hidden="true">→</span></a></h3></article>')
 return '<div class="photo-guide-grid">'+''.join(cards)+'</div>'
def nav(current):
 parts=[]
 for title,slugs in GROUPS:
  links=''.join(f'<a href="{p["file"]}"'+(' aria-current="page"' if p['slug']==current else '')+'>'+p['title']+'</a>' for slug in slugs for p in PAGES if p['slug']==slug)
  parts.append('<div><h3>'+title+'</h3>'+links+'</div>')
 return ''.join(parts)
# Editorial summaries are deliberately separate from the captured source material.
SUMMARIES={
 'respiratory':('어디서부터 상담해야 할지 막막하다면', '가장 불편한 증상부터 이야기해 주세요.', ['코·목·기침 중 가장 불편한 부위', '증상이 시작된 때와 반복되는 상황', '지금까지 받은 검사와 치료']),
 'cotton-care':('코와 목의 관리를 알아보고 있다면', '관리 방법과 적용 여부를 먼저 확인하세요.', ['약솜관리는 어떻게 진행되는지', '내 증상에도 적용할 수 있는지', '관리 전후 어떤 점을 확인할지']),
 'rhinitis':('코막힘과 콧물이 반복된다면', '언제, 어떤 불편이 반복되는지가 중요합니다.', ['하루 중 코가 가장 불편한 시간', '수면과 일상에서 느끼는 불편', '치료와 생활관리에 대한 궁금한 점']),
 'nose-function':('코의 역할이 궁금하다면', '코의 기능부터 차근차근 이해하세요.', ['코가 호흡에서 맡는 역할', '현재 느끼는 코의 불편함', '진료와 생활관리에서 살펴볼 점']),
 'diagnosis':('내 코의 상태를 알고 싶다면', '사진만으로 내 상태를 판단하지 마세요.', ['현재 느끼는 증상을 먼저 설명하기', '진찰 결과를 의료진과 함께 확인하기', '유형별 설명은 이해를 돕는 자료로 보기']),
 'rhinitis-treatment':('비염 치료를 고민하고 있다면', '치료 목표를 구체적으로 이야기해 보세요.', ['가장 먼저 줄이고 싶은 불편함', '기존 치료 과정에서 궁금했던 점', '치료 경과와 관리 방법을 확인하는 시점']),
 'cough':('기침이 반복되어 걱정된다면', '기침이 이어지는 양상을 기록하세요.', ['기침이 시작된 때와 잦아지는 시간', '가래 등 함께 느끼는 증상', '복용 중인 약과 지금까지의 검사']),
 'cough-treatment':('기침 치료 과정을 알고 싶다면', '현재의 불편과 이후의 관리 계획을 함께 확인하세요.', ['지금 가장 불편한 증상', '치료 중 달라진 점과 남아 있는 불편', '기존 처방과 함께 확인할 사항']),
 'cold':('감기 증상으로 진료를 준비한다면', '증상의 시작과 변화를 알려주세요.', ['증상이 시작된 날짜', '열·콧물·기침 등 증상의 변화', '복용한 약의 이름과 복용 시간']),
 'otitis':('귀가 불편하거나 잘 들리지 않는다면', '말로 표현하기 어려운 불편도 함께 살핍니다.', ['귀의 불편함이 시작된 시점', '평소와 다르게 느끼는 소리나 반응', '이전에 받은 진료와 검사 결과'])
}
CHOICES=[('rhinitis','코막힘·콧물이 반복돼요','비염의 이해와 치료 안내'),('cough','기침이 계속돼요','기침·천식의 유형과 진료 안내'),('cold','감기 증상이 있어요','감기·독감과 생활관리 안내'),('otitis','귀가 아프거나 먹먹해요','중이염의 증상과 진료 안내')]
for _page in PAGES:
 if _page['slug'] not in SUMMARIES:
  _cfg=CONFIG[_page['file']]
  SUMMARIES[_page['slug']]=('속의 불편으로 진료를 준비한다면',_cfg['headline'],_cfg['points'])
  DESCS[_page['slug']]=_page['description']

def patient_summary(page):
 context,title,points=SUMMARIES[page['slug']]
 return '<section class="patient-summary" aria-label="먼저 확인하세요"><p class="eyebrow">먼저 확인하세요 · '+context+'</p><h2>'+title+'</h2><ul>'+''.join('<li>'+escape(t)+'</li>' for t in points)+'</ul><a href="#guide-0" class="summary-link">자세한 안내 읽기 <span aria-hidden="true">↓</span></a></section>'

def internal_item(item,page,idx,seen):
 if item['type']=='image':return source_image(item,page['file'],idx,seen)
 return render_item(item)

def build_internal(write,link):
 cards=''
 for n,(label,slugs) in enumerate(GROUPS,1):
  cards+=f'<section class="internal-topic-group"><p class="eyebrow">GUIDE / 0{n}</p><h3>{label}</h3>'
  cards+=''.join(link(p['file'],p['title']+' <span aria-hidden="true">→</span>','topic-link') for slug in slugs for p in PAGES if p['slug']==slug)+'</section>'
 choices=''.join(f'<a class="symptom-card" href="internal-{slug}.html"><span class="choice-number">0{n}</span><h3>{title}</h3><p>{desc}</p><span class="choice-action">안내 보기 <span aria-hidden="true">→</span></span></a>' for n,(slug,title,desc) in enumerate(CHOICES,1))
 digestive_choices=[('functional-digestive','식후 더부룩함·조기 포만감','기능성 위장질환과 담적'),('upper-digestive','속쓰림·신물·명치 불편','상부소화기질환'),('lower-digestive','복통·설사·변비','하부소화기질환')]
 digestive=''.join(f'<a class="digestive-choice" href="internal-{slug}.html"><span>0{n}</span><div><h3>{label}</h3><p>{symptom}</p></div><b aria-hidden="true">→</b></a>' for n,(slug,symptom,label) in enumerate(digestive_choices,1))
 content='<section class="section internal-hub"><div class="container">'+care_flow('internal')+'<section id="care-paths"><div class="internal-section-heading"><div><p class="eyebrow">내게 맞는 진료 안내</p><h2>호흡기부터 소화기까지.</h2></div><p>가장 가까운 불편을 선택해 보세요.</p></div>'+feature_cards('internal')+'</section><section class="digestive-entry" id="digestive-guides"><div><p class="eyebrow">DIGESTIVE CARE</p><h2>속이 불편할 때,<br>어디서부터 살펴볼까요?</h2><p>기능과 증상의 양상, 불편한 부위에 따라 안내합니다.</p><a class="underlined-link" href="internal-digestive.html">소화기내과 전체 안내 →</a></div><div class="digestive-choices">'+digestive+'</div></section><section id="symptom-guides" class="symptom-guides"><div class="internal-section-heading"><div><p class="eyebrow">RESPIRATORY CARE</p><h2>코·목·기침이 불편하다면.</h2></div></div><div class="symptom-grid">'+choices+'</div></section><section id="all-guides"><div class="internal-section-heading"><div><p class="eyebrow">EXPLORE THE GUIDE</p><h2>한방내과 전체 안내</h2></div></div><div class="internal-topic-grid">'+cards+'</div></section></div></section>'
 write('clinic-internal.html','한방내과',content,group='진료 분야',desc='호흡기·소화기 건강, 검사와 변증진단을 함께 보는 진료.',eyebrow='INTERNAL MEDICINE')
 for page in PAGES:
  chapters=[];toc=[];seen=set()
  for idx,section in enumerate(page['sections']):
   label=LABELS.get(page['slug'],{}).get(idx,section['title']).replace('I ','',1)
   if page['slug']=='diagnosis' and 2<=idx<=7:label=f'유형 {idx-1} · 진찰 소견과 증상'
   toc.append(f'<a href="#guide-{idx}"><span>{idx+1:02}</span>{escape(label)}</a>')
   items=section['items']
   if page['slug']=='diagnosis' and 2<=idx<=7:
    images=''.join(internal_item(i,page,idx,seen) for i in items if i['type']=='image')
    words=''.join(render_item(i) for i in items if i['type']!='image')
    body='<div class="diagnosis-stage"><div class="stage-images">'+images+'</div><div>'+words+'</div></div>'
   else:body=''.join(internal_item(i,page,idx,seen) for i in items)
   body=re.sub(r'<h3>(.*?)</h3>',r'<h2>\1</h2>',body,count=1,flags=re.S)
   chapters.append(f'<details class="source-chapter" id="guide-{idx}"><summary><span>{idx+1:02}</span>{escape(label)}<b aria-hidden="true">＋</b></summary><div class="reading-section">{body}</div></details>')
  contents='<details class="on-this-page" open><summary>이 페이지 목차 <span aria-hidden="true">＋</span></summary><nav aria-label="본문 목차">'+''.join(toc)+'</nav></details>'
  sidebar='<aside class="reading-sidebar"><a class="reading-home" href="clinic-internal.html">한방내과 전체 안내 <span aria-hidden="true">↗</span></a><nav aria-label="한방내과 세부 안내">'+nav(page['slug'])+'</nav></aside>'
  mobile='<div class="internal-mobile-tools"><a href="clinic-internal.html">← 한방내과 전체</a><details class="mobile-reading-nav"><summary>다른 안내 보기 <span aria-hidden="true">＋</span></summary><nav aria-label="모바일 한방내과 세부 안내">'+nav(page['slug'])+'</nav></details></div>'
  related='<nav class="article-pagination" aria-label="다음 안내">'+link('clinic-internal.html','← 한방내과 전체')
  next_page=PAGES[(PAGES.index(page)+1)%len(PAGES)]
  related+=link(next_page['file'],'다음 안내 · '+next_page['title']+' →')+'</nav>'
  note='<p class="clinical-note">이 안내는 건강에 대한 이해를 돕는 참고 정보입니다. 증상과 질환에 대한 정확한 판단은 의료진의 진료가 필요합니다.</p>'
  content='<section class="section reading-wrap"><div class="container">'+mobile+'<div class="reading-layout">'+sidebar+'<article class="reading-article">'+reading_tabs(page,chapters)+note+related+'</article></div></div></section>'
  write(page['file'],page['title'],content,group='한방내과',desc=DESCS[page['slug']],eyebrow='INTERNAL MEDICINE · HEALTH GUIDE')
