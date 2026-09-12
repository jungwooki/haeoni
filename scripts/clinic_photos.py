"""Original clinic photography, reviewed against the captured source pages."""
from pathlib import Path
import json
from html import escape
ROOT=Path(__file__).resolve().parents[1]
PHOTOS=json.loads((ROOT/'content/clinic-photo-inventory.json').read_text())
LABELS={2:'진료 기록을 살피는 의료진',3:'환자와 함께하는 상담',4:'해온의 전통을 담은 기록',5:'배움과 교류의 시간',10:'이전 접수 공간의 기록',11:'신도림 테크노마트 외관',12:'해온한의원 입구',13:'접수 및 대기 공간',14:'진료실로 이어지는 복도',15:'진료·검사 공간',16:'진료실',17:'진료 및 초음파 검사 공간',18:'상담과 진료 공간',19:'치료 공간',20:'치료실 복도',21:'치료실 안내 공간',22:'스포츠 진료 공간',23:'재활 진료 공간',24:'치료 준비 공간'}
def photo_gallery(indices,title,desc='',action=False):
 figures=[]
 for idx in indices:
  p=PHOTOS[idx];label=LABELS.get(idx,'해온한의원 의료진')
  figures.append(f'<figure><img src="{p["path"]}" alt="{escape(label)}" width="{p["width"]}" height="{p["height"]}" loading="lazy" decoding="async"><figcaption>{escape(label)}</figcaption></figure>')
 return '<section class="clinic-photo-section"><div class="container"><div class="section-heading"><div><p class="eyebrow">INSIDE HAEON</p><h2>'+title+'</h2></div><p class="section-description">'+desc+'</p></div><div class="clinic-photo-grid">'+''.join(figures)+'</div>'+('<a class="button" href="01_4.tour.html">병원 공간 전체 보기 →</a>' if action else '')+'</div></section>'
