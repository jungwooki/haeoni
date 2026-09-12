# -*- coding: utf-8 -*-
"""Edited explanations drawn from the supplied process guide; no efficacy scores."""
from html import escape
import math

def prescription_common():
    return '<section class="prescription-common"><h2>함께 알아두세요 · 진료 전 확인사항</h2><p>같은 처방명이라도 제품·제형·구성·용량이 다를 수 있습니다. 복용 중인 약·한약·건강기능식품과 알레르기, 임신·수유 여부, 간·신장 질환을 알려주세요. 또한 복용 중 불편이나 이상 반응이 생기면 의료진에게 문의하세요.</p></section>'

def prescription_chart(data, name):
    labels={'qi_def':'기허','qi_stag':'기울','qi_counter':'기역','blood_def':'혈허','blood_stasis':'어혈','fluid':'수체','yin_def':'음허'}
    keys=list(labels)
    def point(i,r):
        a=i*2*math.pi/7-math.pi/2
        return f'{180+math.cos(a)*r:.1f},{180+math.sin(a)*r:.1f}'
    svg='<svg viewBox="0 0 360 360" role="img" aria-label="'+escape(name+' 처방 특성 참고도: '+', '.join(labels[k]+' '+str(data[k]) for k in keys))+'">'
    for r in [25,50,75,100]:svg+='<polygon points="'+' '.join(point(i,r) for i in range(7))+'" fill="none" stroke="#dadddf"/>'
    svg+='<polygon points="'+' '.join(point(i,data[k]) for i,k in enumerate(keys))+'" fill="#29364822" stroke="#293648" stroke-width="2"/>'
    for i,k in enumerate(keys):
        x,y=point(i,137).split(',');svg+=f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-size="14" fill="#46505c">{labels[k]} {data[k]}</text>'
    return '<figure class="prescription-chart">'+svg+'</svg><figcaption>처방 특성을 쉽게 설명한 도식이며, 치료 효과나 개인의 검사 수치를 뜻하지 않습니다.</figcaption></figure>'

def section(title, intro, cards):
    return '<section class="care-reading"><h2>'+title+'</h2><p>'+intro+'</p><div class="care-reading-grid">'+''.join('<article><h3>'+t+'</h3><p>'+p+'</p>'+('<a href="'+u+'">자세히 보기 →</a>' if u else '')+'</article>' for t,p,u in cards)+'</div></section>'

def process_reading():
    return section('해온이 진료에서 중요하게 생각하는 것', '전통적인 진찰과 검사 자료, 일상에서의 움직임을 함께 살펴봅니다.', [
        ('기본에 충실한 진료','침·뜸·부항·한약 등 한의학적 치료의 적용 여부를 진찰 후 판단합니다. 치료를 선택하는 이유와 주의사항을 함께 설명합니다.','care-treatment.html'),
        ('필요한 정보를 함께 확인','문진과 한의학적 진찰에 필요한 검사 자료를 더합니다. 초음파 영상, 혈액 수치나 설문 점수는 각각 확인할 수 있는 범위가 다릅니다.','care-diagnostic.html'),
        ('일상과 움직임까지 살피기','관절의 움직임, 운동할 때의 불편, 일상에서 반복되는 자세를 확인합니다. 치료와 함께 생활·운동에서 조절할 점을 상담합니다.','care-treatment.html#item-CHUNA_SIM')
    ]) + section('검사 결과와 한의학적 진찰을 함께 읽습니다', '검사 장비의 수치 하나로 몸 전체의 상태를 단정하지 않습니다.', [
        ('문진과 변증','추위와 더위에 대한 반응, 식사·소화·수면 등 여러 정보를 함께 살펴 한의학적으로 상태를 구분합니다. 이를 처방과 치료를 선택하는 과정에 참고합니다.','care-prescription.html'),
        ('몸의 움직임과 영상','관절의 움직임과 불편한 부위를 진찰하고, 필요한 경우 근골격계 초음파 영상 등을 함께 살펴봅니다.','care-diagnostic.html#item-USG_MSK'),
        ('검사와 상담 자료','혈구·간 관련 혈액 수치, 체성분·체수분 추정치, 심박변이도와 설문 응답을 각 검사 목적에 맞게 해석합니다.','care-diagnostic.html')
    ]) + section('처방과 치료는 어떻게 달라지나요?', '현재 불편한 증상과 진료 경과, 복용 중인 약과 생활 여건을 함께 고려합니다.', [
        ('한약 제제','가루·연조엑스·환 등 제품에 따라 형태와 구성이 다릅니다. 복용법과 건강보험 적용 여부는 실제 처방에 따라 안내합니다.','care-prescription.html'),
        ('탕약과 농축 형태','처방 구성과 제형, 복용 기간은 진찰과 경과에 따라 정합니다. 특정 제형이 모든 사람에게 더 효과적인 것은 아닙니다.','care-prescription.html'),
        ('기기를 사용하는 치료','전기·온열·냉각 등 기기의 자극 방식과 적용 부위를 확인합니다. 이온냉각치료를 포함해 각 방식의 주의사항을 안내합니다.','care-treatment.html#item-PT_ION_COOL')
    ]) + '''<section class="care-reading"><h2>경과에 따라 달라지는 진료의 초점</h2><p>근골격계 불편의 경과를 이해하기 위한 안내입니다. 모든 질환이 같은 단계를 거치거나 일정한 기간에 회복되는 것은 아닙니다.</p><div class="care-phases">''' + ''.join('<details><summary>'+t+'</summary><p>'+p+'</p></details>' for t,p in [
        ('01 · 통증과 불편이 큰 시기','통증이 시작된 상황과 부종·열감, 일상생활의 제한을 확인합니다. 추가 평가가 필요한지 먼저 살피고, 활동 조절과 치료 계획을 설명합니다.'),
        ('02 · 움직임의 변화를 확인하는 시기','통증의 변화뿐 아니라 움직일 수 있는 범위와 일상에서의 불편을 함께 확인합니다. 활동이나 운동의 범위는 상태에 맞게 조절합니다.'),
        ('03 · 일상과 운동을 이어가는 시기','반복되는 부담과 남아 있는 불편을 살피고 생활 습관, 운동 강도와 경과 확인 계획을 상담합니다. 증상이 달라지면 다시 평가합니다.')
    ])+'''</div></section><section class="care-preparation"><h2>진료하는 의료진을 만나보세요</h2><p>의료진의 인사말과 약력, 진료 분야를 확인하실 수 있습니다.</p><a href="01_2.team.html">4인의 의료진 소개 →</a></section>'''

def prescription_reading():
    return section('같은 증상에도 처방이 달라질 수 있습니다', '한의학에서는 여러 증상과 진찰 정보를 함께 살펴 상태를 구분하는 ‘변증’을 처방에 참고합니다. 같은 증상에 서로 다른 처방을, 다른 증상에 같은 처방을 고려할 수도 있습니다.', [
        ('몸의 반응을 함께 살핍니다','식사·소화·수면, 추위와 더위에 대한 반응 등 개인의 상태를 함께 확인합니다. 증상명 하나로 처방을 선택하지 않습니다.',''),
        ('형태와 구성이 다를 수 있습니다','같은 처방명이라도 제약회사·제품·제형에 따라 구성과 용량이 다를 수 있습니다. 아래 대표 약재는 일부 구성에 대한 안내이며, 실제 처방은 제품 정보와 함께 확인합니다.',''),
        ('경과를 함께 확인합니다','처방 후 달라진 점과 남아 있는 불편을 확인하고, 진찰 결과에 따라 다음 처방을 상담합니다.','')
    ])

def variant_details(item):
    if not item.get('variants'): return ''
    return '<section class="care-variants"><h3>처방 종류별 안내</h3>'+''.join('<div><h4>'+escape(v['label'])+'</h4><h5>효과·적응증 키워드</h5><p class="prescription-keywords">'+escape(v['keywords'])+'</p><h5>대표 약재</h5><p>'+escape(v['ingredients'])+'</p>'+prescription_chart(v['chart'],item['name']+' '+v['label'])+'</div>' for v in item['variants'])+'</section>'

def catalog_reading(kind):
    if kind=='prescription': return prescription_reading()
    if kind=='diagnostic':
        return section('검사마다 살펴보는 정보가 다릅니다', '불편한 증상과 진찰 내용을 바탕으로 필요한 검사를 선택합니다.', [
            ('구조와 움직임','초음파 영상에서는 관찰하는 부위의 구조를, 운동·균형 검사에서는 정해진 동작의 수행 모습을 살펴봅니다.',''),
            ('혈액 수치와 신체 지표','혈구·간 관련 수치와 체성분·체수분 등의 지표는 서로 다른 정보를 제공합니다. 검사 전후의 조건과 이전 결과를 함께 확인합니다.',''),
            ('심장 박동과 마음의 상태','심박변이도는 박동 간격의 변화이고, 심리 설문은 본인이 응답한 경험입니다. 서로 다른 자료를 상담에 참고하며 질환을 단독으로 확정하지 않습니다.','')
        ])
    return section('자극의 방식과 적용 부위를 설명합니다', '진찰에서 확인한 상태에 따라 방법·강도·범위를 정하고, 치료 중 반응을 살핍니다.', [
        ('침·뜸·부항','침 자극, 열 자극, 음압 등 서로 다른 방식을 사용합니다. 부위와 방식에 따라 피부 반응과 주의사항도 달라집니다.',''),
        ('약침·추나','약침은 사용하는 약침액과 적용 부위를, 추나는 관절·근육 상태와 수기 기법을 확인합니다. 모든 사람에게 같은 방식으로 진행하지 않습니다.',''),
        ('기기·움직임 관리','전기·온열·냉각 자극, 테이핑과 균형 훈련 등 각 방식의 목적과 적용 제한을 설명합니다. 치료 후 일상에서 느끼는 변화도 함께 확인합니다.','')
    ])
