# -*- coding: utf-8 -*-
"""Public-facing, conservatively edited companion to the EMR guides."""
from pathlib import Path
from html import escape as e
import json
from care_editorial import process_reading, prescription_reading, variant_details, catalog_reading
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'content/care-guides.json').read_text())
NOTICE='진료의 이해를 돕기 위한 안내입니다. 검사·처방·치료는 개인의 상태와 의료진의 판단에 따라 달라지며, 효과와 부작용에는 개인차가 있습니다.'
LINKS=[('care-process.html','진료 과정'),('care-diagnostic.html','진단검사'),('care-prescription.html','한약처방'),('care-treatment.html','치료방법')]
PANELS=[('process','진료 과정','이야기를 듣는 시간부터 경과를 확인하는 진료까지.','assets/images/renewal/eb753b27d10c44.jpg'),('diagnostic','진단검사','무엇을 확인하는 검사인지, 결과는 어떻게 이해해야 하는지.','assets/images/room-ultrasound.jpg'),('prescription','한약처방','처방 이름을 살펴보고, 복용 전 확인할 내용을 알아보세요.','assets/images/tour-13.jpg'),('treatment','치료방법','진행 방법과 함께 적용 전 확인할 사항을 안내합니다.','assets/images/tour-08.jpg')]
def notice():return '<p class="care-notice">'+NOTICE+'</p>'
def navigation(current):return '<nav class="care-guide-nav" aria-label="해온의 진료 안내"><a href="care.html">해온의 진료</a>'+''.join(f'<a href="{u}"'+(' aria-current="page"' if u==current else '')+'>'+t+'</a>' for u,t in LINKS)+'</nav>'
def cards():return '<div class="care-guide-cards">'+''.join(f'<a class="care-guide-card" href="care-{key}.html"><img src="{img}" alt="해온한의원 진료 공간" loading="lazy"><div><span class="eyebrow">0{i+1}</span><h3>{title}</h3><p>{desc}</p><span class="care-card-action">자세히 보기 →</span></div></a>' for i,(key,title,desc,img) in enumerate(PANELS))+'</div>'
def home_section():return '<section class="section care-home"><div class="container"><div class="section-heading"><div><p class="eyebrow">해온의 진료</p><h2>충분히 듣고, 필요한 정보를 살피고,<br>진료의 방향을 설명합니다.</h2></div><p class="section-description">한의학적 진찰과 필요한 검사 결과를 함께 살펴<br>환자분의 상태에 맞는 치료를 계획합니다.</p></div>'+cards()+'</div></section>'
def related(name):
 if not name.startswith(('clinic-','internal-','child-','women-')):return ''
 return '<section class="care-related"><div class="container"><h2>진료가 궁금하신가요?</h2><p>검사와 치료의 진행 방법, 진료 전 확인할 내용을 살펴보세요.</p><div>'+''.join(f'<a href="{u}">{t} →</a>' for u,t in LINKS)+'</div></div></section>'
def overview():return '<section class="section"><div class="container"><div class="care-introduction"><p class="eyebrow">듣고 · 살피고 · 설명하고 · 함께 확인합니다</p><h2>진료의 시작은<br>환자분의 이야기입니다.</h2><p>증상이 언제 시작되었는지, 일상에서 어떤 불편이 있는지 먼저 듣습니다. 진찰과 필요한 검사에서 얻은 정보를 함께 살펴 치료를 계획하고, 이후의 변화를 확인합니다.</p><p>검사나 치료의 종류보다 중요한 것은 지금의 상태에 무엇이 필요한지 설명하고 함께 결정하는 과정입니다.</p></div>'+cards()+notice()+'</div></section>'
def process():
 steps=[('이야기를 듣습니다','가장 불편한 증상, 시작된 시기와 반복되는 상황을 이야기해 주세요. 생활·수면·식사, 이전 진료 경험도 함께 살핍니다.'),('몸의 상태를 살핍니다','문진과 진찰을 통해 현재 상태를 살피고, 추가 확인이 필요한 내용을 정리합니다.'),('필요한 검사를 설명합니다','검사가 필요한 경우 확인하려는 내용과 한계, 준비사항을 먼저 안내합니다. 모든 검사를 일괄적으로 시행하는 것은 아닙니다.'),('치료 계획을 함께 정합니다','치료를 고려하는 이유와 진행 방법, 주의사항 및 비용을 설명합니다. 궁금한 점이나 부담되는 부분을 말씀해 주세요.'),('경과를 함께 확인합니다','이전과 달라진 점, 남아 있는 불편과 이상 반응을 확인합니다. 상태에 따라 계획을 조정하거나 추가 평가·의뢰를 안내합니다.')]
 return '<section class="section"><div class="container care-guide-shell">'+navigation('care-process.html')+'<div class="care-process-layout"><img src="assets/images/renewal/eb753b27d10c44.jpg" alt="해온한의원 상담 모습" loading="lazy"><ol class="care-steps">'+''.join(f'<li><span>0{i+1}</span><div><h2>{title}</h2><p>{desc}</p></div></li>' for i,(title,desc) in enumerate(steps))+'</ol></div><section class="care-preparation"><h2>진료 전 준비하면 좋은 것</h2><p>복용 중인 약·한약·건강기능식품 목록, 알레르기와 수술 이력, 이전 검사 결과가 있으면 가져오세요. 임신·수유 여부도 알려주세요.</p></section>'+process_reading()+notice()+'</div></section>'
REFS={
'diagnostic':[],
'prescription':[('일본동양의학회 · 日本東洋医学会','https://www.jsom.or.jp/'),('한약 사용과 간 손상 관련 국내 연구 · Frontiers in Pharmacology (2025)','https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2025.1498124/full')],
 'treatment':[('침 치료 안전성 · NCCIH','https://www.nccih.nih.gov/health/acupuncture-effectiveness-and-safety'),('척추 수기 치료 안전성 · NCCIH','https://www.nccih.nih.gov/health/spinal-manipulation-what-you-need-to-know'),('부항 안전성 · NCCIH','https://www.nccih.nih.gov/health/cupping'),('봉독 약침 이상반응 문헌 검토','https://pubmed.ncbi.nlm.nih.gov/35448847/')]
}
def treatment_details(item):
 if not item.get('procedure'):return ''
 return '<section class="care-treatment-details"><h3>진행 방법</h3><p>'+e(item['procedure'])+'</p><h3>쉽게 이해하기</h3><p>'+e(item['explanation'])+'</p></section>'

def catalog(kind):
 title=dict((key,t) for key,t,_,_ in PANELS)[kind];items=[x for x in DATA[kind] if x.get('publication_status','current')=='current'];cats=list(dict.fromkeys(c for x in items for c in x.get('categories',[x['category']])))
 intro={'diagnostic':'검사마다 한의학적 해석, 범위가 다릅니다. 결과는 한의학적 문진, 진찰과 함께 이해합니다.','treatment':'진료에서 설명을 들은 치료가 어떤 방식인지 확인해 보세요. 적용 전 주의사항도 함께 살펴보실 수 있습니다.','prescription':'처방명을 가나다순으로 살펴볼 수 있습니다. 실제 제형·구성·복용법과 보험 적용 여부는 진료 시 확인합니다.'}[kind]
 if kind=='prescription':items=sorted(items,key=lambda x:x['name'])
 out='<section class="section"><div class="container care-guide-shell">'+navigation('care-'+kind+'.html')+catalog_reading(kind)+'<p class="care-catalog-intro">'+intro+'</p><div class="care-filters" hidden><div><label for="care-search">'+title+(' 이름·약재·키워드 검색' if kind=='prescription' else ' 이름·키워드 검색' if kind=='treatment' else ' 이름 검색')+'</label><input id="care-search" type="search" placeholder="검색어를 입력하세요" autocomplete="off"></div><div><label for="care-category">분류</label><select id="care-category"><option value="">전체</option>'+''.join('<option>'+e(c)+'</option>' for c in cats)+'</select></div></div><p class="care-count" aria-live="polite">'+str(len(items))+'개 항목</p><div class="care-catalog">'
 for x in items:
  notes='' if kind=='prescription' else '<h3>함께 알아두세요</h3><p>'+e(x["limit"])+'</p><div class="care-entry-caution"><h3>진료 전 확인할 사항</h3><p>'+e(x["caution"])+'</p></div>'
  keywords='<div class="care-treatment-keywords"><h3>관련 키워드</h3><p>'+e(x['keywords'])+'</p></div>' if kind=='treatment' else ''
  out+=f'<details class="care-entry" id="item-{e(x["id"])}" data-category="{e(x["category"])}" data-name="{e(x["name"])}" data-categories="{e(json.dumps(x.get("categories",[x["category"]]),ensure_ascii=False))}" data-search="{e(x["name"]+" "+x.get("keywords", "")+" "+" ".join(v["ingredients"]+" "+v.get("keywords", "") for v in x.get("variants",[])))}"><summary><span><small>{e(x["category"])}</small><strong>{e(x["name"])}</strong></span><span class="care-entry-toggle" aria-hidden="true">＋</span></summary><div class="care-entry-content">{keywords}<p>{e(x["description"])}</p>{variant_details(x)}{treatment_details(x) if kind=="treatment" else ""}{notes}</div></details>'
 out+='</div><p class="care-no-results" hidden>일치하는 항목이 없습니다. 검색어나 분류를 바꿔보세요.</p>'
 if REFS[kind]:
  out+='<details class="care-references"><summary>안내에 참고한 자료</summary><ul>'+''.join(f'<li><a href="{u}" target="_blank" rel="noopener noreferrer">{t} ↗</a></li>' for t,u in REFS[kind])+'</ul><p>일반적인 검사·안전성 정보를 위한 자료이며, 특정 장비·제품이나 개인의 치료 효과를 보장하는 근거는 아닙니다.</p></details>'
 out+=notice()+'</div></section>'
 return out

def build_care(write):
 write('care.html','해온의 진료',overview(),group='해온의 진료',desc='한의학적 진찰과 필요한 검사 결과를 함께 살펴, 진료의 방향을 설명합니다.',eyebrow='HAEON CARE')
 write('care-process.html','진료 과정',process(),group='해온의 진료',desc='처음 오시는 날부터 경과를 확인하는 진료까지.',eyebrow='HAEON CARE')
 for kind,title in [('diagnostic','진단검사'),('prescription','한약처방'),('treatment','치료방법')]:
  write('care-'+kind+'.html',title,catalog(kind),group='해온의 진료',desc='진료에서 만나는 '+title+'의 종류와 확인할 내용을 안내합니다.',eyebrow='HAEON CARE')
