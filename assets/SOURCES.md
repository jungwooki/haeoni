# 첫 화면 리뉴얼 자료

2026-09-12 확인. 기존 상세 페이지는 수정하지 않고, 홈에서 연결합니다.

## 스타일
- https://haeon.sportsmps.com/
- Pretendard 1.3.9, 네이비 #1e293b, 블루 #2563eb, 카카오 노랑 #fee500.

## 기존 haeoni.com에서 가져온 이미지 (원본 그대로 저장)
- images/brand/logo.jpg: https://cdn.imweb.me/thumbnail/20260826/3fbefcf7d95b8.jpg
- images/spaces/original-hero-2.jpg: https://cdn.imweb.me/thumbnail/20251205/f3f4801984723.jpg
- images/people/original-hero-1.jpg: https://cdn.imweb.me/thumbnail/20251204/6e354b8e97a56.jpg

## 내용 및 연결
- 모토와 비전: 사용자 제공 내용.
- 가업, 공감, 학술교류, 진료 분야, 주소, 대표전화, 사업자번호: https://haeoni.com/ 및 폴더 내 01_1.about.html.
- 개원 연도: 01_1.about.html.
- 카카오톡: 기존 로컬 상세 페이지 및 참고 사이트에 기재된 https://pf.kakao.com/_sYeKE.
- 네이버 예약: 참고 사이트에 기재된 예약 ID 150330.
- 기존 로컬 소아 안내 파일(02-1.clinic_child.html)은 둘러보기 내용이 들어 있어 기존 홈페이지 /kids로 연결.
- 로컬 위치 안내(01_3.location.html)는 빈 파일이므로 기존 홈페이지 /93으로 연결.
- 실제 사진이 아닌 외부 스톡 사진을 사용하는 로컬 둘러보기 대신 기존 홈페이지 /92로 연결.

## 편집 및 미리보기
- index.html: 문구, 이미지, 링크.
- assets/styles/shared/home.css: 데스크톱 및 모바일 레이아웃.
- assets/scripts/shared/home.js: 모바일 메뉴 닫기와 Escape 키 처리.
- index.html을 직접 열거나, haeoni.com 폴더에서 python3 -m http.server로 확인.
- CSS와 이미지 경로는 상대경로. Pretendard 글꼴 로딩에는 인터넷 연결이 필요하며 시스템 글꼴 폴백 포함.
- 첫 화면만 리뉴얼한 단계로 연결된 상세 페이지의 디자인은 기존 상태.

## 2026-09-12 다중 페이지 확장
- 인사말 /86, 의료진 /165 및 4개 원장 팝업, 역사 /87, 시간 /time, 공간 /92, 위치 /93, 사회공헌 /142: https://haeoni.com
- 원장 프로필 사진은 기존 메인 페이지에 표시된 각 원장별 이미지 URL에서 원본 다운로드: doctor-lee.jpg (20250731/6cfba1b61688d.jpg), doctor-jung.jpg (20250731/80aa1cb99bdb9.jpg), doctor-han.jpg (20250801/bf8c943efdc87.jpg), doctor-cho.jpg (20250731/4618b2bf06bb4.jpg).
- tour-01.jpg~tour-13.jpg: /92의 cdn.imweb.me/thumbnail/20251207/ 공간 사진. 원본 HTML의 순서대로 저장.
- 원문·상태·추가 조사 범위는 ../MIGRATION.md 및 ../content/ 참조.

## 한방내과 상세 안내 이관
- 기존 사이트의 /rhini1, /rhini50, /79, /rhinitis1, /126, /rhini7, /153, /rhini9, /131, /141, /rhini3, /rhini14 확인.
- 2쌍의 중복 본문을 정리하여 고유한 상세 안내 10개로 연결.
- 사진·도해 20개의 원본 URL과 실제 크기: ../content/internal-assets.json.
- 본문·사진·관련 자료 링크 대응 및 범위: ../INTERNAL_MIGRATION.md.
- 상담: 기존 카카오톡 채널. 예약: 기존 네이버 예약 ID 150330. 길찾기: 로컬 01_3.location.html.

## 소아과·부인과 및 추가 사진

`content/family-assets.json`은 기존 haeoni.com의 원본 이미지 URL 65개와 로컬 파일을 대응합니다. `content/internal-assets.json`은 23개입니다. 배경·갤러리 추가 대조는 `content/supplemental-images.json`에 기록했습니다. 생성형 이미지는 사용하지 않았습니다.
