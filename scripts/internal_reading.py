# -*- coding: utf-8 -*-
"""Compact patient-facing tables with accessible, progressive reading tabs."""
from html import escape as esc
from clinical_visuals import CONFIG
ROWS={
'respiratory':[('코·목','막힘·콧물·목의 불편','불편한 부위와 시간'),('기침','기침·가래의 변화','시작한 때와 반복 상황'),('진료','검사·진찰과 생활','기존 검사와 치료 기록')],
'cotton-care':[('관리 부위','코와 목의 상태','가장 불편한 곳'),('진행 과정','약솜관리 방법','진행 방법에 대한 질문'),('적용 상담','현재 상태에 맞는 관리','이전 치료 경험')],
'rhinitis':[('증상','코막힘·콧물·재채기','특히 불편한 시간'),('진찰','코 안의 상태','이전에 받은 검사'),('일상','수면과 생활의 불편','줄이고 싶은 불편')],
'nose-function':[('호흡','공기가 드나드는 통로','코로 숨 쉬기 불편한 때'),('점막','코 안의 상태와 기능','건조함 등 느끼는 변화'),('관리','진료와 생활관리','자주 반복되는 불편')],
'diagnosis':[('검사·진찰','코 안의 소견','기존 검사 결과'),('증상·생활','불편의 양상과 변화','언제, 얼마나 불편한지'),('패턴진단','정보를 종합한 한의학적 해석','유형에 대한 의료진 설명')],
'rhinitis-treatment':[('치료 목표','현재 가장 불편한 증상','먼저 줄이고 싶은 불편'),('경과 확인','치료 전후의 변화','호전되거나 남아 있는 증상'),('일상 관리','생활에서 챙길 부분','수면과 일상의 변화')],
'cough':[('기간','언제부터 이어졌는지','처음 시작한 시점'),('양상','가래 등 동반 증상','하루 중 잦아지는 시간'),('진료 이력','기존 검사와 복용 중인 약','검사 결과·약 이름')],
'cough-treatment':[('불편이 심할 때','현재 증상과 조절 목표','기침·가래의 변화'),('안정되는 동안','남은 불편과 관리 방향','일상에서 달라진 점'),('치료 상담','기존 처방과 함께 확인','현재 복용 중인 약')],
'cold':[('시작','증상이 시작된 날짜','처음 느낀 불편'),('변화','열·콧물·기침의 경과','날짜별 증상 변화'),('진료 준비','복용한 약과 기존 진료','약 이름과 복용 시간')],
'otitis':[('불편','통증·먹먹함 등 귀의 증상','시작 시점과 변화'),('관찰','소리와 반응의 변화','평소와 다른 모습'),('진찰','귀의 상태와 기존 검사','진료·검사 기록')],
'digestive':[('기능성 위장질환·담적','식후 불편과 생활의 패턴','더부룩함·일찍 배부른 느낌'),('상부소화기','식도·위 주변의 불편','속쓰림·신물·명치 불편'),('하부소화기','복통과 배변의 변화','설사·변비·배변 전후 차이')],
'functional-digestive':[('식후 불편','포만감·명치의 불편','식사와 증상의 관계'),('원인 확인','기존 검사와 추가 평가 필요성','검사 결과와 복용 중인 약'),('패턴진단','증상·식욕·배변·수면','일상에서 반복되는 양상')],
'upper-digestive':[('위치와 느낌','속쓰림·신물·명치 불편','어디가 어떻게 불편한지'),('나타나는 때','식사·눕는 자세와의 관계','증상 시간과 상황'),('확인할 자료','기존 내시경 등 검사 결과','검사와 치료 이력')],
'lower-digestive':[('복통','배변 전후 달라지는 불편','통증의 위치와 시간'),('배변','횟수와 변의 형태','설사·변비 등 변화'),('생활과 진료','식사·수면·약물·기존 검사','며칠간의 기록')]
}
def reading_tabs(page,chapters,rows=None,preparation=None):
 cfg=CONFIG[page['file']]
 table='<div class="care-table-wrap"><table class="care-summary-table" role="table"><caption>진료에서 함께 살펴볼 내용</caption><thead><tr role="row"><th scope="col">구분</th><th scope="col">살펴볼 점</th><th scope="col">알려주실 내용</th></tr></thead><tbody>'+''.join('<tr role="row"><th scope="row" role="rowheader">'+esc(a)+'</th><td role="cell" data-label="살펴볼 점">'+esc(b)+'</td><td role="cell" data-label="알려주실 내용">'+esc(c)+'</td></tr>' for a,b,c in (ROWS[page['slug']] if rows is None else rows))+'</tbody></table></div>'
 flow='<ol class="reading-flow">'+''.join('<li><span>'+f'{n:02}'+'</span><strong>'+esc(label)+'</strong></li>' for n,label in enumerate(cfg['points'],1))+'</ol>'
 overview='<h2>'+esc(cfg['headline'])+'</h2>'+flow+table
 prep='<h2>진료 전, 세 가지만 준비해 주세요.</h2><div class="visit-note-grid"><div><span>01</span><h3>증상의 기록</h3><p>가장 불편한 점과 시작한 시점, 반복되는 상황을 알려주세요.</p></div><div><span>02</span><h3>검사와 치료 이력</h3><p>기존 검사 결과와 복용 중인 약을 함께 확인합니다.</p></div><div><span>03</span><h3>꼭 묻고 싶은 질문</h3><p>치료 목표와 생활관리 등 궁금했던 점을 편하게 이야기해 주세요.</p></div></div>'
 if preparation is not None:prep=preparation
 if page['slug'] in ['functional-digestive','upper-digestive','lower-digestive']:
  # Keep the already-authored warning signs visible in the preparation tab as well.
  prep+='<p class="reading-callout">갑작스럽거나 심한 증상은 예약을 기다리기보다 먼저 진료를 받으세요. 자세한 안내에서 빠른 평가가 필요한 증상을 확인할 수 있습니다.</p>'
 panels=[('overview','한눈에 보기',overview),('details','자세한 안내','<h2>궁금한 항목을 펼쳐보세요.</h2><p class="reading-tab-lead">필요한 설명과 자료를 주제별로 확인할 수 있습니다.</p>'+''.join(chapters)),('prepare','진료 준비',prep)]
 links='<nav class="reading-tabs" aria-label="안내 내용 선택">'+''.join(f'<a id="reading-tab-{key}" href="#reading-{key}">{label}</a>' for key,label,_ in panels)+'</nav>'
 return '<div class="tabbed-reading">'+links+''.join(f'<section class="reading-tab-panel" id="reading-{key}" aria-labelledby="reading-tab-{key}">{body}</section>' for key,_,body in panels)+'</div>'
