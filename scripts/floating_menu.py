# -*- coding: utf-8 -*-
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
def icon(path):return '<svg viewBox="0 0 24 24" aria-hidden="true">'+path+'</svg>'
chat=icon('<path d="M21 11.5a8.5 8.5 0 0 1-8.5 8.5H4l-3 2 2-6a8.5 8.5 0 1 1 18-4.5Z"/><path d="M8 10h8M8 14h5"/>')
calendar=icon('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 3v4m10-4v4M3 11h18m-13 5 3 2 5-4"/>')
pin=icon('<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="3"/>')
FLOATING=f'''<nav class="floating-contact" aria-label="상담 예약 오시는 길 빠른 메뉴"><button class="quick-toggle" type="button" aria-label="빠른 메뉴 접기" aria-expanded="true" aria-controls="floating-links" hidden>접기</button><div class="floating-links" id="floating-links"><a href="https://pf.kakao.com/_sYeKE" target="_blank" rel="noopener noreferrer" aria-label="카카오톡 상담">{chat}<span>카카오톡 상담</span></a><a href="https://m.booking.naver.com/booking/6/bizes/150330" target="_blank" rel="noopener noreferrer" aria-label="네이버 진료 예약">{calendar}<span>네이버 예약</span></a><a href="01_3.location.html" aria-label="오시는 길 안내">{pin}<span>오시는 길</span></a></div></nav>'''
ASSETS='<link rel="stylesheet" href="assets/styles/shared/floating.css"><script src="assets/scripts/shared/floating.js" defer></script>'
def install_on_legacy(generated):
 # All top-level HTML is publishable. Source archives in content/ remain untouched.
 names=[]
 for p in ROOT.glob('*.html'):
  if p.name in generated:continue
  s=p.read_text()
  if not s.strip() or 'http-equiv="refresh"' in s:continue
  if 'floating-contact' not in s:
   s=s.replace('</head>',ASSETS+'</head>')
   s=s.replace('</body>',FLOATING+'</body>')
   # Hide only the old fixed bottom reservation bars; retain menus and page content.
   def hide(match):
    classes=match.group(1)
    if 'fixed' in classes.split() and 'bottom-0' in classes.split():classes+=' legacy-contact-hidden'
    return 'class="'+classes+'"'
   s=re.sub(r'class="([^"]*)"',hide,s)
   p.write_text(s)
  names.append(p.name)
 return names
