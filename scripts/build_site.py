#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build static HTML with a shared navigation; no build dependencies required."""
from pathlib import Path
from html import escape as esc
import json,re
from urllib.parse import urlencode
from clinic_photos import photo_gallery
from pain_care import pain_page, certification
from tonic_care import tonic_page
from publication_review import public_html
from care_editorial import prescription_common
from care_guides import build_care, home_section, related, LINKS as CARE_LINKS, notice as care_notice
from floating_menu import FLOATING, ASSETS, install_on_legacy
from internal_pages import build_internal, PAGES
from home_hero import home_hero, SLIDES as HERO_SLIDES
from clinical_visuals import CONFIG as VISUAL_CONFIG, visual_hero
from family_pages import build_family, PAGES as FAMILY_PAGES, ROUTES
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/'content'/name).read_text())
EXTERNAL_CLINICS={'clinic-weight.html':('https://haeonw.com','diet'), 'clinic-sports.html':('https://haeon.sportsmps.com/','sports')}
def link(url,label,cls=''):
 extra=''
 if url in EXTERNAL_CLINICS:
  url,kind=EXTERNAL_CLINICS[url];cls+=' specialty-link specialty-'+kind
  label+=' <span aria-hidden="true">↗</span>';extra=' target="_blank" rel="noopener noreferrer" aria-label="'+esc(re.sub('<[^>]+>','',label).strip(' ↗'),quote=True)+' 별도 사이트, 새 창"'
 return f'<a class="{cls.strip()}" href="{esc(url,quote=True)}"{extra}>{label}</a>' 
depts=[('internal','한방내과','INTERNAL MEDICINE','증상을 넘어, 몸 전체의 흐름을 살핍니다.','호흡기 · 소화기 · 검사와 변증진단','/rhinitis'),('child','소아과','CHILD & ADOLESCENT','아이의 오늘과 건강한 성장을 함께 봅니다.','성장 · 허약체질 · 소아청소년 건강','/kids'),('women','부인과','WOMEN’S HEALTH','여성의 생애주기마다 세심하게 함께합니다.','여성질환 · 임신 준비 · 산후 회복','/woman'),('weight','다이어트','WEIGHT MANAGEMENT','생활과 몸의 변화를 함께 살핍니다.','체중 · 체형 · 생활 관리','https://haeonw.com'),('constitution','체질보약','CONSTITUTIONAL CARE','같은 증상도, 나의 몸에 맞게 살핍니다.','허약체질 · 보약 · 한약 처방','/152'),('pain','통증재활','PAIN & REHABILITATION','움직임의 회복에서 일상의 회복까지.','근골격 통증 · 재활 · 회복 관리','https://haeon.sportsmps.com/'),('sports','스포츠 MPS','SPORTS MPS','운동하는 몸과 마음을 함께 이해합니다.','유소년 스포츠 · 성인 운동 · MPS 평가','https://haeon.sportsmps.com/')]
depts=sorted(depts,key=lambda d:['internal','child','women','constitution','pain','weight','sports'].index(d[0]))
docs=[('lee','이정욱','대표원장 · 한방내과 겸임교수','한방내과 · 소아과 · 소아 스포츠 · 난치성질환'),('jung','정지은','한방소아과 전문의','소아청소년 · 부인과 · 비만 · 통증'),('han','한유경','원장 · 한의사','한방내과 · 재활 · 산후 여성질환 · 피부·비만'),('cho','조내경','원장 · 한의사','한방부인과 · 재활 · 피부질환 · 비만')]
about_links=[('01_1.about.html','해온의 철학·인사말'),('history.html','역사와 전통'),('contribution.html','사회공헌')]
visit_links=[('time.html','진료시간'),('01_3.location.html','오시는 길·주차'),('01_4.tour.html','공간 둘러보기'),('https://pf.kakao.com/_sYeKE','카카오톡 상담'),('https://m.booking.naver.com/booking/6/bizes/150330','네이버 예약'),('fees.html','비급여수가 안내')]
nav_groups=[('한의원 소개',about_links),('진료 분야',[(f'clinic-{d[0]}.html',d[1]) for d in depts]),('의료진',[('01_2.team.html','의료진 전체')]+[(f'doctor-{d[0]}.html',d[1]+' 원장') for d in docs]),('이용 안내',visit_links),('해온 소식',[('sitemap.html','전체 페이지')])]
nav_groups.insert(2,('해온의 진료',[('care.html','진료 안내 전체')]+CARE_LINKS))
nav_groups.append(('한방내과 세부 안내',[(p['file'],p['title']) for p in PAGES]))
def header(current):
 translate_url='https://translate.google.com/translate?'+urlencode({'sl':'ko','tl':'ja','hl':'ja','u':'https://haeoni.com/'+current})
 language_link=f'<details class="header-language notranslate" translate="no"><summary aria-label="언어 선택 / 言語選択"><span class="language-flag" aria-hidden="true">🇰🇷</span><span class="language-code">KO</span><span aria-hidden="true">⌄</span></summary><div class="language-options"><a class="language-ko" href="{current}" data-original="https://haeoni.com/{current}" lang="ko" aria-current="true"><span aria-hidden="true">🇰🇷</span> 한국어</a><a class="language-ja" href="{esc(translate_url,quote=True)}" lang="ja"><span aria-hidden="true">🇯🇵</span> 日本語<small>Google 自動翻訳</small></a></div></details>'
 parent='care.html' if current.startswith('care') else '01_2.team.html' if current.startswith('doctor-') else 'departments.html' if current.startswith(('clinic-', 'internal-', 'child-', 'women-')) else 'time.html' if current in ['01_3.location.html','01_4.tour.html'] else '01_1.about.html' if current in ['history.html','contribution.html'] else current
 groups=''.join('<section><h2>'+title+'</h2>'+''.join(link(u,n) for u,n in items)+'</section>' for title,items in nav_groups)
 nav=''.join(link(u,n,'nav-current' if parent==u else '') for u,n in [('01_1.about.html','한의원 소개'),('departments.html','진료 분야'),('care.html','해온의 진료'),('01_2.team.html','의료진'),('time.html','이용 안내')])
 strip=''.join(link('clinic-'+d[0]+'.html',d[1],'nav-current' if (current=='clinic-'+d[0]+'.html' or current.startswith(d[0]+'-')) else '') for d in depts)
 return f'''<a class="skip-link" href="#main">본문으로 바로가기</a><header class="site-header multi-header"><div class="container header-inner"><a class="brand" href="index.html" aria-label="해온한의원 홈"><img src="assets/images/logo.jpg" alt="해온한의원" width="451" height="147"></a><nav class="desktop-nav" aria-label="주 메뉴">{nav}</nav>{language_link}<details class="site-menu"><summary aria-label="전체 메뉴"><span class="menu-lines" aria-hidden="true">☰</span><span class="menu-label">전체 메뉴</span></summary><div class="mega-menu"><div class="container mega-grid">{groups}</div></div></details></div><nav class="department-bar" aria-label="진료 분야">{strip}</nav></header>'''
legacy=(ROOT/'content/legacy/index.html').read_text()
footer=re.search(r'<footer class="site-footer">.*?</footer>',legacy,re.S).group(0)
footer=footer.replace('>이용약관<','>웹사이트 이용 안내<')
footer=footer.replace('<div class="footer-links">','<div class="footer-links"><a href="sitemap.html">전체 페이지</a>')
mobile=re.search(r'<nav class="mobile-contact".*?</nav>',legacy,re.S).group(0)
cta='''<section class="shared-cta"><div class="container"><div><p class="eyebrow">HERE FOR YOU</p><h2>궁금한 점부터, 편하게 이야기해 주세요.</h2><p>4인의 의료진이 함께하는 해온한의원</p></div><div class="contact-action-group"><a class="button contact-kakao" href="https://pf.kakao.com/_sYeKE" target="_blank" rel="noopener noreferrer">카카오톡 상담 ↗</a><a class="button contact-naver" href="https://m.booking.naver.com/booking/6/bizes/150330" target="_blank" rel="noopener noreferrer">네이버 예약 ↗</a><a class="button contact-directions" href="01_3.location.html">오시는 길 →</a></div></div></section>'''
manifest=[]
def write(name,title,content,group='한의원 소개',desc='본질을 지키며 미래로 향합니다.',hero=True,eyebrow='HAEON KOREAN MEDICINE'):
 manifest.append(name)
 content+=related(name)
 if name=='index.html':content+=photo_gallery([12,13,15,17,22,24],'진료실에 오시기 전,<br>해온의 공간을 만나보세요.','입구부터 진료·검사실, 치료 공간까지.',True)
 if name=='history.html':content+=photo_gallery([4,5],'해온의 기록과 배움','기존 홈페이지에 남아 있는 가업과 학술 교류의 기록입니다.')
 if name=='01_1.about.html':content+=photo_gallery([2,3],'듣고, 살피고, 함께합니다.','기존 홈페이지에 담긴 해온의 진료 모습입니다.')
 if name=='01_4.tour.html':content=photo_gallery(list(range(12,25)),'해온의 공간을 둘러보세요.','2025년 확장 이후의 진료·검사·치료 공간입니다.')+photo_gallery([10,11],'신도림에서 이어온 시간','이전 접수 공간과 테크노마트 외관의 기록입니다.')
 group_url={'해온의 진료':'care.html','의료진':'01_2.team.html','진료 분야':'departments.html','이용 안내':'time.html','한방내과':'clinic-internal.html','소아과':'clinic-child.html','부인과':'clinic-women.html'}.get(group,'01_1.about.html')
 top=f'<section class="page-hero"><div class="container"><nav class="breadcrumbs" aria-label="현재 위치"><a href="index.html">홈</a><span>/</span><a href="{group_url}">{group}</a><span>/</span><span aria-current="page">{title}</span></nav><p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="page-lead">{desc}</p></div></section>' if hero else ''
 if name in ['clinic-constitution.html','clinic-pain.html']:
  photo='tour-04.jpg' if name=='clinic-constitution.html' else 'room-ultrasound.jpg'
  top=top.replace('<div class="container">','<div class="container common-clinic-opening">',1).replace('</div></section>',f'<figure class="common-clinic-photo"><img src="assets/images/{photo}" alt="해온한의원 진료 공간" decoding="async"></figure></div></section>')
 if name in VISUAL_CONFIG:
  top=visual_hero(name,title,group_url,group)
 html=f'''<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#1e293b"><meta name="description" content="{esc(title+' | '+desc,quote=True)}"><title>{title} | 해온한의원</title><link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" crossorigin><link rel="stylesheet" href="assets/home.css"><link rel="stylesheet" href="assets/site.css"><script src="assets/home.js" defer></script><link rel="stylesheet" href="assets/internal.css"><script src="assets/photo-motion.js" defer></script>{ASSETS}</head><body id="top">{header(name)}<main id="main">{top}{content}{cta if hero else ''}</main>{footer}{FLOATING}</body></html>'''
 if name=='index.html':
  html=html.replace('<body id="top">','<body id="top" class="home-renewal">')
  html=html.replace('</head>',f'<link rel="preload" as="image" href="assets/images/{HERO_SLIDES[0][0]}"><link rel="stylesheet" href="assets/home-hero.css"><script src="assets/home-hero.js" defer></script></head>')
 if name=='clinic-internal.html' or name.startswith('internal-'):
  html=html.replace('<body id="top">','<body id="top" class="internal-renewal">').replace('</head>','<script src="assets/internal.js" defer></script></head>')
 if name in VISUAL_CONFIG:
  html=html.replace('<body id="top">','<body id="top" class="clinic-visual">').replace('class="internal-renewal"','class="internal-renewal clinic-visual"')
  html=html.replace('</head>','<link rel="stylesheet" href="assets/clinical-visuals.css"></head>')
  if 'src="assets/internal.js"' not in html:html=html.replace('</head>','<script src="assets/internal.js" defer></script></head>')
 if name.startswith(('clinic-','internal-','child-','women-')):
  html=html.replace('<body id="top">','<body id="top" class="care-unified">')
  html=html.replace('class="clinic-visual"','class="clinic-visual care-unified"')
  html=html.replace('</head>','<link rel="stylesheet" href="assets/internal-renewal.css"></head>')
 if name=='clinic-child.html' or name.startswith('child-'):
  html=html.replace('class="clinic-visual care-unified"','class="clinic-visual care-unified child-renewal"').replace('</head>','<link rel="stylesheet" href="assets/child-renewal.css"></head>')
 html=html.replace('</head>','<link rel="stylesheet" href="assets/unified.css"><link rel="stylesheet" href="assets/care-guides.css"><link rel="stylesheet" href="assets/contact-care.css"><script src="assets/language.js" defer></script></head>')
 if name=='clinic-constitution.html':html=html.replace('</head>','<link rel="stylesheet" href="assets/tonic-care.css"></head>')
 if name.startswith('care'):
  html=html.replace('</head>','<script src="assets/care-guides.js" defer></script></head>')
  html=html.replace(care_notice(),'').replace('</main>', '<div class="container">'+care_notice()+'</div></main>')
 if name=='care-prescription.html':html=html.replace('<div class="container">'+care_notice(),'<div class="container">'+prescription_common()+care_notice())
 html=html.replace('class="nav-current"','class="nav-current" aria-current="page"')
 html=public_html(html).replace('https://haeoni.com/d','care-diagnostic.html').replace('https://haeoni.com/?mode=policy','terms.html').replace('https://haeoni.com/?mode=privacy','privacy.html')
 (ROOT/name).write_text(html)
def paras(lines):return ''.join('<p>'+esc(x)+'</p>' for x in lines if x.strip())
def prose(lines):return '<div class="prose">'+paras(lines)+'</div>'
def doc_cards():return '<div class="doctor-grid">'+''.join(f'<a class="doctor-card" href="doctor-{slug}.html"><img src="assets/images/doctor-{slug}.jpg" alt="{name} 원장" width="600" height="750" loading="lazy"><div><p class="eyebrow">{role}</p><h3>{name} <small>원장</small></h3><p>{area}</p><span class="underlined-link">인사말·약력·연구 활동 <span aria-hidden="true">↗</span></span></div></a>' for slug,name,role,area in docs)+'</div>'
def dept_cards():
 return '<div class="department-grid">'+''.join(link('clinic-'+d[0]+'.html',f'<span class="eyebrow">0{i+1} / {d[2]}</span><h3>{d[1]}</h3><p>{d[4]}</p>{certification(True) if d[0]=="pain" else ""}<span class="department-action">'+('별도 사이트' if d[0] in ['weight','sports'] else '진료 안내')+'</span>','department-card') for i,d in enumerate(depts))+'</div>'

# Homepage keeps its established visual design while every menu opens a page.
main=re.search(r'<main id="main">(.*?)</main>',legacy,re.S).group(1)
for a,b in {'href="#philosophy"':'href="01_1.about.html"','href="#care"':'href="departments.html"','href="#team"':'href="01_2.team.html"','href="#visit"':'href="01_3.location.html"','https://haeoni.com/93':'01_3.location.html','https://haeoni.com/time':'time.html'}.items():main=main.replace(a,b)
main=main.replace('2008<span>년부터</span>','4<span>인의 의료진</span>').replace('신도림에서 함께한 시간<br><strong>일상 곁의 한의원</strong>','다양한 경험과 시각<br><strong>함께하는 해온의 진료</strong>')
main=re.sub(r'<div class="care-grid">.*?</div>\s*</div>\s*</section>',dept_cards()+'</div></section>',main,count=1,flags=re.S)
main=main.replace('aria-label="아래로 내려 해온의 철학 보기"','aria-label="해온의 철학 자세히 보기"').replace('SCROLL TO EXPLORE','EXPLORE HAEON')
main=main.replace('각자의 전문성과 경험을 나누는 네 명의 한의사.','한방내과 겸임교수, 한방소아과 전문의와<br>다양한 한방병원 진료 경험을 갖춘 4인의 한의사.')
main=re.sub(r'<section class="hero".*?</section>',home_hero(),main,count=1,flags=re.S)
# The team portrait is now featured in the hero; avoid repeating it below.
main=re.sub(r'<figure class="team-image">.*?</figure>','',main,count=1,flags=re.S)
main=re.sub(r'(<section\b[^>]*\bid="team")',lambda m:home_section()+m.group(1),main,count=1) if 'id="team"' in main else main+home_section()
write('index.html','해온한의원',main,hero=False)
about=read('about-original.json')
write('01_1.about.html','해온의 철학·인사말','<section class="section"><div class="container editorial-grid"><aside><p class="eyebrow">OUR PHILOSOPHY</p><h2>가업의 뜻과 경험,<br>마음의 아픔까지.</h2><img class="editorial-image" src="assets/images/original-hero-2.jpg" alt="해온한의원 진료실" width="1920" height="1080"></aside>'+'<div>'+prose(about['86'])+'</div>'+'</div></section>',desc='3대를 이어온 진료의 마음으로, 한의학을 가꾸어 갑니다.')
write('history.html','역사와 전통','<section class="section"><div class="container editorial-grid"><aside><p class="eyebrow">PAST · PRESENT · FUTURE</p><h2>깊은 뿌리에서<br>새로운 내일로.</h2><div class="milestones"><p><strong>3대</strong> 가업의 뜻과 경험</p><p><strong>2008</strong> 신도림에서 개원</p><p><strong>2017</strong> 강의와 학술교류</p><p><strong>2025</strong> 테크노마트 2층 확장</p></div></aside>'+'<div>'+prose(about['87'])+'</div>'+'</div></section>',desc='원칙을 지키며 전통을 이어갑니다.')
write('contribution.html','사회공헌','<section class="section"><div class="container editorial-grid"><aside><p class="eyebrow">GIVING TOGETHER</p><h2>진료실 밖에서도<br>함께하는 마음.</h2></aside>'+prose(about['142'])+'</div></section>',desc='개원 이래 지속적으로 나눔을 실천합니다.')
write('01_2.team.html','4인의 의료진','<section class="section"><div class="container"><div class="section-heading"><h2>각자의 깊이,<br>함께 넓어지는 진료.</h2><p class="section-description">한방내과 겸임교수, 한방소아과 전문의와<br>한방병원 진료 경험을 갖춘 의료진이 함께합니다.<br>인사말과 약력, 연구 활동을 자세히 만나보세요.</p></div>'+doc_cards()+'<div class="team-principles"><h2>사람을 이해하는 진료</h2><p>환자의 성장과 생활, 회복 과정까지 함께 이해하려 노력합니다. 진료실 안에서의 설명과 대화, 진료 이후의 생활관리까지 중요하게 생각합니다.</p>'+link('departments.html','7개 진료 분야 살펴보기 →','underlined-link')+'</div></div></section>',group='의료진',desc='열린 마음과 각자의 경험으로, 한 사람을 세심하게 살핍니다.',eyebrow='MEDICAL TEAM')
raw=read('doctors-original.json')
headings={'약력','연구','강의','방송, 컬럼, 기고','중점 진료 분야','연구·강좌·활동','대학 강의','연구 활동','한의학회 회원','연구, 강좌, 컬럼'}
for slug,name,role,area in docs:
 lines=raw[slug].strip().splitlines()[1:];sections=[];cur=[];label='인사말'
 for line in lines:
  t=line.strip().strip('\u2800')
  if not t:continue
  if t in headings:
   if cur:sections.append((label,cur));cur=[]
   label=t
  else:cur.append(t)
 if cur:sections.append((label,cur))
 toc='<nav class="profile-toc" aria-label="원장 소개 목차">'+''.join(link(f'#profile-{i}',h) for i,(h,_) in enumerate(sections))+'</nav>'
 body=''+''.join(f'<section id="profile-{i}" class="profile-section"><h2>{h}</h2>'+prose(lines)+'</section>' for i,(h,lines) in enumerate(sections))
 content=f'<section class="section"><div class="container profile-grid"><aside><img class="profile-photo" src="assets/images/doctor-{slug}.jpg" alt="{name} 원장" width="600" height="750"><p class="eyebrow">{role}</p><h2>{name} <small>원장</small></h2><p class="profile-area">{area}</p>{toc}{link("time.html","원장별 진료일정 문의 →","underlined-link")}</aside><div>{body}</div></div><div class="container related-doctors"><h2>함께하는 의료진</h2>'+''.join(link(f'doctor-{s}.html',n+' 원장 →','button') for s,n,_,_ in docs if s!=slug)+'</div></section>'
 write(f'doctor-{slug}.html',name+' 원장',content,group='의료진',desc=role,eyebrow='PEOPLE OF HAEON')
write('departments.html','진료 분야','<section class="section"><div class="container"><div class="section-heading"><h2>7개 진료 분야,<br>삶의 여러 순간을 함께.</h2><p class="section-description">아이의 성장부터 어른의 일상까지.<br>필요한 진료 분야와 세부 안내를 찾아보세요.</p></div>'+dept_cards()+'</div></section>',group='진료 분야',desc='한의학의 기반 위에, 다양한 몸과 마음의 이야기를 살핍니다.',eyebrow='DEPARTMENTS')
rows=read('inventory.json')
# Preserve every original menu destination while detailed articles are migrated.
lookup={r['url']:r for r in rows}; child=rows[9:30];women=rows[31:56];internal=rows[57:69]
constitution=[lookup[u] for u in ['/152','/147','/kids4','/146','/kids5']]
selections={'internal':internal,'child':child,'women':women,'weight':[lookup['https://haeonw.com']],'constitution':constitution,'pain':[lookup['https://haeon.sportsmps.com/']],'sports':[lookup['https://haeon.sportsmps.com/']]}
for slug,name,en,desc,area,source in depts:
 if slug in ['internal','child','women']:continue
 if slug=='pain':
  write('clinic-pain.html','통증재활 · 스포츠 진료',pain_page(),group='진료 분야',desc='통증·재활과 스포츠 진료, 일상과 운동의 움직임을 함께 살핍니다.',eyebrow='PAIN & SPORTS CARE')
  continue
 items=selections[slug]
 links=''.join(link(ROUTES.get(r['url'], 'https://haeoni.com'+r['url'] if r['url'].startswith('/') else r['url']),esc(r['title'].replace('비만','다이어트'))+' <span aria-hidden="true">↗</span>','topic-link') for r in items)
 content=f'<section class="section"><div class="container"><div class="section-heading"><h2>{area.replace(" · ","<br>",1)}</h2><p class="section-description">궁금한 내용부터 차근차근 살펴보세요.<br>진료와 생활관리에 필요한 세부 안내를 확인하세요.</p></div><div class="topic-grid">{links}</div><div class="team-principles"><h2>몸과 마음을 함께 살피는 의료진</h2><p>증상과 생활에 귀 기울이고, 진단과 치료에 대해 충분히 설명하는 진료를 지향합니다.</p>{link("01_2.team.html","의료진 소개 →","underlined-link")}</div></div></section>'
 if slug=='constitution':content=tonic_page(links)
 write(f'clinic-{slug}.html',name,content,group='진료 분야',desc=desc,eyebrow=en)
from fees import fee_page
write('fees.html','비급여 수가표',fee_page(),group='이용 안내',desc='진료 항목별 비급여 비용을 안내합니다.',eyebrow='FEES')
# Practical information: use current 2F address, keeping the stale source in the migration log.
write('time.html','진료시간 안내','''<section class="section"><div class="container editorial-grid"><aside><p class="eyebrow">OPENING HOURS</p><h2>일상에 맞춰<br>방문하실 수 있도록.</h2><p class="aside-copy">원장별 진료시간은 별도로 문의해 주세요.</p><a class="underlined-link" href="tel:02-2111-7575">02.2111.7575 →</a></aside><div><table class="hours-table"><caption>해온한의원 진료시간</caption><thead><tr><th scope="col">요일</th><th scope="col">진료시간</th></tr></thead><tbody><tr><th scope="row">월요일·수요일</th><td>10:00–21:00</td></tr><tr><th scope="row">화요일·목요일·금요일</th><td>10:00–20:00</td></tr><tr><th scope="row">토요일</th><td>10:00–15:00</td></tr><tr><th scope="row">평일 점심시간</th><td>13:00–14:00</td></tr></tbody></table><p class="aside-copy">일요일·공휴일 및 원장별 일정은 방문 전 문의해 주세요.</p><a class="underlined-link" href="01_3.location.html">오시는 길·주차 안내 →</a></div></div></section>''',group='이용 안내',desc='신도림 테크노마트 2층에서 진료합니다.',eyebrow='VISIT HAEON')
write('01_3.location.html','오시는 길·주차','''<section class="section"><div class="container location-layout"><figure class="location-map"><a href="https://naver.me/GlJlW9S4" target="_blank" rel="noopener noreferrer" aria-label="네이버 지도에서 위치 보기 (새 창)"><img src="assets/images/location-map.png" alt="해온한의원 신도림본원 위치. 신도림역 3번 출구 지하통로 연결, 테크노마트 2층." width="1302" height="1208"></a><figcaption>네이버 지도 · 지도를 누르면 네이버 지도가 새 창에서 열립니다.</figcaption></figure><div class="location-details"><aside><p class="eyebrow">LOCATION</p><h2>신도림역과 연결된<br>테크노마트 2층.</h2><p class="aside-copy">서울시 구로구 새말로 97<br>신도림 테크노마트 2층 9호</p><a class="underlined-link" href="https://naver.me/GlJlW9S4" target="_blank" rel="noopener noreferrer">네이버 지도에서 보기 ↗</a></aside><div class="prose"><h2>지하철로 오시는 길</h2><p>1·2호선 신도림역 3번 출구 지하통로를 통해 테크노마트로 들어오세요. 엘리베이터 또는 에스컬레이터로 2층으로 올라오시면 됩니다.</p><h2>주차 안내</h2><p>테크노마트 지하 3층부터 지하 7층까지 주차장을 이용하실 수 있습니다. 주차는 3시간 무료입니다.</p><p>토요일은 주변 도로가 혼잡할 수 있으니 예약 시간보다 조금 일찍 도착해 주세요.</p><h2>2008년부터 신도림에서</h2><p>해온한의원은 2008년부터 신도림 테크노마트에서 진료하고 있습니다. 2025년 2층 확장공사를 통해 더욱 많은 분들께 세밀한 진료로 보답합니다.</p><a class="underlined-link" href="time.html">진료시간 확인 →</a></div></div></div></section>''',group='이용 안내',desc='1·2호선 신도림역 지하통로로 편하게 오세요.',eyebrow='LOCATION & PARKING')
gallery=read('gallery.json') if (ROOT/'content/gallery.json').exists() else []
photos=''.join(f'<figure><img src="assets/images/{n}" alt="해온한의원 2층 내부 공간 {i+1}" width="1920" height="{3413 if i in (2,8) else 1080}" loading="lazy"></figure>' for i,n in enumerate(gallery))
write('01_4.tour.html','공간 둘러보기','<section class="section"><div class="container"><div class="section-heading"><h2>익숙한 곳에서,<br>더 편안한 진료를.</h2><p class="section-description">2008년 개원 이래 신도림 테크노마트에서 진료하고 있습니다.<br>2025년 확장공사를 통해 더 깨끗하고 넓은 공간으로 거듭났습니다.</p></div><div class="gallery-grid">'+photos+'</div></div></section>',group='이용 안내',desc='신도림 테크노마트 2층, 해온의 공간을 만나보세요.',eyebrow='SPACE OF HAEON')
# Local legal/information destinations; imported policy is retained verbatim.
privacy_lines=(ROOT/'content/privacy-original.txt').read_text().split('Agreement',1)[-1].strip().splitlines()
write('privacy.html','개인정보처리방침','<section class="section"><div class="container prose">'+paras(privacy_lines)+'</div></section>',group='이용 안내',desc='개인정보 처리와 권리 행사에 관한 안내입니다.',eyebrow='PRIVACY')
write('terms.html','웹사이트 이용 안내','<section class="section"><div class="container prose"><h2>진료 정보의 이용</h2><p>이 홈페이지는 해온한의원의 진료 분야와 이용 정보를 제공합니다. 건강 정보는 이해를 돕기 위한 자료이며, 개인의 진단이나 처방을 대신하지 않습니다.</p><h2>상담과 예약</h2><p>상담·예약 버튼은 카카오톡과 네이버의 서비스로 연결됩니다. 해당 서비스의 이용약관과 개인정보처리방침이 적용되며, 예약 확정과 변경은 예약 서비스 또는 한의원으로 확인하세요.</p><h2>콘텐츠와 문의</h2><p>홈페이지 자료의 이용이나 내용에 관해 궁금한 사항은 해온한의원으로 문의해 주세요.</p><p><a href="tel:02-2111-7575">02-2111-7575</a></p><p><a href="privacy.html">개인정보처리방침 보기</a></p></div></section>',group='이용 안내',desc='홈페이지의 정보와 상담·예약 연결에 관한 안내입니다.',eyebrow='WEBSITE INFORMATION')
build_care(write)
build_internal(write,link)
build_family(write,link)
sitemap_groups=nav_groups+[(label+' 세부 안내',[(p['file'],p['title']) for p in FAMILY_PAGES if p['slug'].startswith(prefix)]) for prefix,label in [('child-','소아과'),('women-','부인과')]]
write('sitemap.html','전체 페이지','<section class="section"><div class="container sitemap-grid">'+''.join('<section><h2>'+t+'</h2>'+''.join(link(u,n+' <span aria-hidden="true">→</span>','topic-link') for u,n in items)+'</section>' for t,items in sitemap_groups if t!='해온 소식')+'</div></section>',desc='한의원 소개부터 진료 분야, 의료진과 이용 안내까지 한눈에.')
(ROOT/'content/generated-pages.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
legacy_names=install_on_legacy(manifest)
(ROOT/'content/floating-pages.json').write_text(json.dumps(manifest+legacy_names,ensure_ascii=False,indent=2))
print('Built',len(manifest),'pages; floating menu on',len(manifest)+len(legacy_names),'published pages')
