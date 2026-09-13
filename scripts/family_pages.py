# -*- coding: utf-8 -*-
"""Source-backed pediatric and women's health hubs and reading pages."""
from pathlib import Path
from html import escape
import json,re
from internal_pages import render_item
from child_reading import child_reading
from internal_reading import reading_tabs
from clinical_visuals import source_image, feature_cards, care_flow
ROOT=Path(__file__).resolve().parents[1]
PAGES=json.loads((ROOT/'content/family-pages.json').read_text())
ROUTES={p['source'].replace('https://haeoni.com',''):p['target'] for p in json.loads((ROOT/'content/family-routes.json').read_text())}
GROUPS={
'child':[('소아 진료와 한약',['overview','integrated','treatments','herbal-prescription','herbal-guide']),('허약체질과 보약',['constitution','antler']),('감기·호흡기·반복 발열',['respiratory','cold-prevention','cold-care','infections','pfapa','pfapa-care']),('키성장과 발달',['growth','growth-causes','growth-diagnosis','growth-care'])],
'women':[('여성의 생애주기',['overview','life-stages']),('임신 준비와 난임',['pregnancy-planning','infertility','infertility-care','female-infertility','male-infertility','assisted-reproduction','pregnancy']),('산후 회복과 육아',['postpartum','body-changes','postpartum-care','postpartum-lifestyle','parenting']),('유산 후 회복',['miscarriage','miscarriage-lifestyle','miscarriage-surgery','recurrent-loss']),('여성질환과 일상 관리',['uterus-ovaries','pms-stress','cold-sensitivity'])]}
META={'child':('소아과','CHILD & ADOLESCENT','아이의 오늘을 살피고,<br>건강한 내일을 함께.','아이의 성장과 발달, 반복되는 감기와 허약체질까지. 진료와 치료에 대한 이해부터 가정에서의 관리까지 안내합니다.'),'women':('부인과','WOMEN’S HEALTH','여성의 삶을 따라,<br>세심하게 함께합니다.','생애주기마다 달라지는 몸과 마음. 임신 준비와 출산, 회복의 시간부터 일상 속 여성 건강까지 함께 살핍니다.')}
def selected(dept,slugs):return [p for slug in slugs for p in PAGES if p['slug']==dept+'-'+slug]
def navigation(dept,current):
 return ''.join('<div><h3>'+title+'</h3>'+''.join('<a href="'+p['file']+'"'+(' aria-current="page"' if p['file']==current else '')+'>'+p['title']+'</a>' for p in selected(dept,slugs))+'</div>' for title,slugs in GROUPS[dept])
def women_summary_rows(slug):
 if 'miscarriage' in slug or 'recurrent-loss' in slug:
  return [('현재 상태','출혈·통증·발열과 회복 경과','산부인과 진료 결과와 처치 내용'),('진료 이력','이전 임신과 유산 경험','검사 결과와 복용 중인 약'),('회복 계획','휴식·일상 복귀와 다음 상담','생활에서 필요한 도움과 궁금한 점')]
 if 'postpartum' in slug or 'body-changes' in slug or 'parenting' in slug:
  return [('출산 후 경과','통증·출혈·피로 등 현재의 변화','출산 시점과 방법, 기존 진료 내용'),('수유와 복용약','수유 상태와 함께 사용하는 약','약·한약·건강기능식품 목록'),('일상 회복','수면·식사와 돌봄 부담','가장 불편한 점과 필요한 도움')]
 if 'infertility' in slug or 'assisted' in slug or 'planning' in slug:
  return [('부부의 진료 이력','기존 난임 평가와 치료 과정','양측 검사 결과와 복용약'),('월경과 생활','월경 주기·수면·식사 등 변화','최근 기록과 가장 불편한 점'),('진료 일정','진행 중인 시술과 병행 여부','담당 의료진의 안내와 예정 일정')]
 if slug=='women-pregnancy':
  return [('임신 경과','임신 주수와 산전 진료 내용','산부인과 검사 결과'),('현재의 불편','소화·통증 등 증상과 변화','증상이 시작된 시점과 심한 정도'),('처방 상담','복용 필요성과 성분 확인','현재 약·한약·건강기능식품 목록')]
 return [('증상의 기록','월경·통증·냉감 등 현재 불편','언제 시작되어 어떻게 달라졌는지'),('진료 이력','검사·치료와 병력','검사 결과 및 복용약'),('생활 상태','수면·식사·활동과 스트레스','일상에서 부담되는 점과 질문')]

def build_family(write,link):
 for dept,(name,en,headline,desc) in META.items():
  articles=[p for p in PAGES if p['slug'].startswith(dept+'-')]
  cards=''.join('<section class="internal-topic-group"><p class="eyebrow">'+f'{n:02} / {en}'+'</p><h2>'+title+'</h2>'+''.join(link(p['file'],p['title']+' →','topic-link') for p in selected(dept,slugs))+'</section>' for n,(title,slugs) in enumerate(GROUPS[dept],1))
  content='<section class="section family-hub"><div class="container">'+care_flow(dept)+'<section id="care-paths"><div class="internal-section-heading"><div><p class="eyebrow">나의 이야기에서 시작하는 진료</p><h2>'+('아이와 함께 읽는 건강 안내' if dept=='child' else '지금의 나에게 맞는 건강 안내')+'</h2></div></div>'+feature_cards(dept)+'</section><section class="family-all-guides"><h2>'+name+' 전체 안내</h2><div class="internal-topic-grid">'+cards+'</div></section><div class="team-principles"><h2>편안하게 이야기해 주세요.</h2><p>네 명의 의료진이 진료의 관점과 경험을 나누며 몸과 마음에 귀 기울입니다.</p>'+link('01_2.team.html','4인의 의료진 만나보기 →','underlined-link')+'</div></div></section>'
  write('clinic-'+dept+'.html',name,content,group='진료 분야',desc=desc,eyebrow=en)
  for n,p in enumerate(articles):
   chapters=[];toc=[];seen=set()
   for idx,s in enumerate(p['sections']):
    label=s['title'];toc.append(link('#guide-'+str(idx),escape(label)))
    body=''.join(source_image(i,p['file'],idx,seen) if i['type']=='image' else render_item(i) for i in s['items']);body=re.sub(r'<h3>(.*?)</h3>',r'<h2>\1</h2>',body,count=1,flags=re.S)
    if dept in ['child','women']:
     chapters.append(f'<details class="source-chapter" id="guide-{idx}"><summary><span>{idx+1:02}</span>{escape(label)}<b aria-hidden="true">＋</b></summary><div class="reading-section">{body}</div></details>')
    else:
     chapters.append(f'<section class="reading-section" id="guide-{idx}"><div class="section-index">{idx+1:02}<span>{escape(label)}</span></div>{body}</section>')
   nav=navigation(dept,p['file']);home='clinic-'+dept+'.html'
   sidebar='<aside class="reading-sidebar">'+link(home,name+' 전체 안내 ↗','reading-home')+'<nav aria-label="'+name+' 세부 안내">'+nav+'</nav></aside>'
   mobile='<div class="internal-mobile-tools">'+link(home,'← '+name+' 전체')+'<details class="mobile-reading-nav"><summary>다른 안내 보기 <span aria-hidden="true">＋</span></summary><nav aria-label="모바일 '+name+' 세부 안내">'+nav+'</nav></details></div>'
   contents='<details class="on-this-page" open><summary>이 페이지에서 살펴볼 내용</summary><nav aria-label="본문 목차">'+''.join(toc)+'</nav></details>'
   related='<nav class="article-pagination" aria-label="다음 안내">'+link(home,'← '+name+' 전체')+link(articles[(n+1)%len(articles)]['file'],articles[(n+1)%len(articles)]['title']+' →')+'</nav>'
   note='<p class="clinical-note">이 안내는 건강에 대한 이해를 돕는 참고 정보입니다. 증상과 질환에 대한 정확한 판단은 의료진의 진료가 필요합니다.</p>'
   reading=child_reading(p,chapters) if dept=='child' else reading_tabs(p,chapters,rows=women_summary_rows(p['slug']))
   content='<section class="section reading-wrap"><div class="container">'+mobile+'<div class="reading-layout">'+sidebar+'<article class="reading-article">'+reading+note+related+'</article></div></div></section>'
   write(p['file'],p['title'],content,group=name,desc='진료의 이해에서 일상 속 관리까지, 해온이 함께합니다.',eyebrow=en+' · HEALTH GUIDE')
