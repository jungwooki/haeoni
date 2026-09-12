# -*- coding: utf-8 -*-
"""Homepage carousel, kept in the build source so regeneration preserves edits."""
SLIDES=[
 ('original-hero-2.jpg','해온한의원 진료실과 진찰 장비','한의원 진료실','이 진료실에서,<br>당신의 이야기로<br>진료를 시작합니다.','어디가 불편한지, 어떤 하루를 보내고 계신지.<br>해온의 진료는 당신의 이야기를 듣는 데서 시작합니다.','departments.html','해온의 진료 살펴보기','1920','1080'),
 ('room-ultrasound.jpg','초음파 장비가 마련된 해온한의원 스포츠진료실','정밀초음파 · 각종 검사','객관적인 검사로,<br>몸의 상태를<br>더 깊이 살핍니다.','정밀초음파와 각종 검사로 객관적인 정보를 확인합니다.<br>진찰에서 들은 이야기와 함께 몸의 상태를 살핍니다.','01_4.tour.html','진료·검사 공간 보기','1920','1080'),
 ('original-hero-1.jpg','해온한의원 4인 의료진','해온의 한의사','검사 결과에<br>당신의 이야기를<br>더합니다.','<strong>18년째, 20만 건 이상의 진료 경험.</strong><br>그 경험 위에 당신의 일상과 마음을 함께 담아,<br>해온의 한의사가 진료의 방향을 설명합니다.','01_2.team.html','의료진 만나보기','1920','900')
]
def home_hero():
 slides=[]
 for i,(photo,alt,label,title,desc,url,action,width,height) in enumerate(SLIDES):
  state='' if i==0 else ' hidden'
  priority=' fetchpriority="high"' if i==0 else ' decoding="async"'
  slides.append(f'''<div class="home-slide" id="home-slide-{i+1}" role="group" aria-roledescription="슬라이드" aria-label="{i+1} / 3 · {label}"{state}>
<div class="home-slide-photo"><img src="assets/images/{photo}" alt="{alt}" width="{width}" height="{height}"{priority}></div>
<div class="container home-slide-inner"><div class="home-slide-copy"><p class="eyebrow">HAEON · CARE &amp; DIAGNOSIS</p><p class="home-slide-label">{label}</p><h2>{title}</h2><p class="home-slide-description">{desc}</p><a class="button button-white" href="{url}">{action} <span aria-hidden="true">→</span></a></div></div></div>''')
 choices=''.join(f'<button type="button" class="hero-choice" aria-controls="home-slide-{i+1}" aria-label="{i+1}번 슬라이드: {s[2]}" aria-pressed="{"true" if i==0 else "false"}"><span>0{i+1}</span>{s[2]}</button>' for i,s in enumerate(SLIDES))
 return '''<section class="home-carousel" aria-label="해온의 진료와 검사 소개" aria-roledescription="캐러셀"><h1 class="hero-sr-only">진료실에서 검사까지, 당신의 이야기를 더하는 해온한의원</h1>'''+''.join(slides)+'''<div class="home-carousel-controls" hidden><div class="container"><div class="hero-choices" aria-label="슬라이드 선택">'''+choices+'''</div><div class="hero-transport"><span class="hero-count" aria-hidden="true">01 / 03</span><button type="button" class="hero-prev" aria-label="이전 슬라이드">←</button><button type="button" class="hero-next" aria-label="다음 슬라이드">→</button></div></div></div><p class="hero-sr-only hero-announcement" aria-live="polite" aria-atomic="true"></p></section>'''
