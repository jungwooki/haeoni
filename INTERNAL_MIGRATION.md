# 한방내과 이관 기록

## 범위

- 기존 한방내과 세부 메뉴 12개를 확인하고 10개의 고유 안내 본문으로 정리했습니다.
- /79와 /rhinitis1은 같은 비염 본문, /rhini9와 /131은 같은 기침 본문입니다. 같은 내용은 한 페이지로 통합했습니다.
- 해당 안내의 본문 텍스트, 사진·도해 20개, 진료 안내를 보존했습니다. 기존 홈페이지 건강칼럼의 제목·글 링크·썸네일 영역은 요청에 따라 제거했습니다.
- 반복되는 상단 사이트 메뉴 및 하단 상담/홍보 블록은 공통 메뉴·푸터·상담 메뉴로 구성했습니다.
- 연결된 게시판 개별 글의 본문은 이번 범위에서 재작성하지 않고 원래 글로 연결합니다.
- 호흡기 안내자료 ISSUU 임베드와 새 창 보기 링크를 보존했습니다. 자료 서비스의 가용성은 외부 사이트에 따릅니다.
- 원본의 의학적 설명·통계·표현을 새 의학적 주장으로 확대하거나 최신 수치로 갱신하지 않았습니다.

## 파일

- content/internal-source/: 12개 원본 페이지 HTML.
- content/internal-pages.json: 렌더링할 본문, 이미지 위치, 목차/제목, 원문 비교 자료.
- content/internal-assets.json: 사진·도해 20개의 원본 URL, 로컬 경로, 실제 크기.
- scripts/internal_pages.py: 한방내과 첫 페이지와 상세 페이지 생성.
- assets/internal.css: 읽기용 본문, 목차, 단계별 사진 및 모바일 레이아웃.
- scripts/floating_menu.py, assets/floating.css, assets/floating.js: 전체 HTML의 세로형 상담·예약·길찾기 메뉴.

## 검증

- 본문 위젯별 전체 텍스트가 새 HTML에 포함되는지 대조.
- 사진과 관련 자료 링크의 누락 여부 확인.
- 기존 의료진 원문 보존 및 전체 생성 페이지 로컬 링크·내부 앵커 검사.
- 공개 대상 HTML 38개에 플로팅 메뉴가 정확히 한 번 존재하는지 검사.

| 원본 | 새 파일 |
|---|---|
| https://haeoni.com/rhini1 | rhini1.html |
| https://haeoni.com/rhini50 | internal-cotton-care.html |
| https://haeoni.com/rhinitis1 | internal-rhinitis.html |
| https://haeoni.com/126 | internal-nose-function.html |
| https://haeoni.com/rhini7 | internal-diagnosis.html |
| https://haeoni.com/153 | internal-rhinitis-treatment.html |
| https://haeoni.com/131 | internal-cough.html |
| https://haeoni.com/141 | internal-cough-treatment.html |
| https://haeoni.com/rhini3 | internal-cold.html |
| https://haeoni.com/rhini14 | internal-otitis.html |
| https://haeoni.com/79 | internal-rhinitis.html |
| https://haeoni.com/rhini9 | internal-cough.html |
| https://haeoni.com/rhinitis | clinic-internal.html |

## 2026-09-12 리뉴얼

한방내과 메인과 10개 상세 안내를 환자 중심의 증상 탐색과 핵심 요약 구조로 개편. 반복 진료실 사진과 허브의 재사용 사진을 제거하고, 원문 도해는 보존했다. 같은 이미지가 여러 원문에 등장하면 최초 배치로 연결한다. 파일명이 다른 동일 사진도 SHA-256으로 판별하며 한방내과 내 실제 이미지 22개는 각 한 번만 표시한다. 확대 모달은 같은 원본을 자세히 보는 용도다.

모바일에는 한방내과 전체/다른 안내 메뉴와 하단 상담/예약/오시는 길을 명시적으로 표시한다. 생성기의 원문 보존 및 전체 사이트 연결 검사와 별도로 브라우저에서 좁은 화면, 목차 이동, 모달 및 키보드 동작을 확인한다.

## 세 진료과 시각 자료 개편 및 소화기 확장

한방내과 메인은 실제 한의사 사진과 호흡기·소화기·검사 사진 카드, 검사와 변증진단을 연결한 과정 도표를 사용한다. 기존 호흡기 상세 10개에도 첫 화면 시각 자료를 배치했다. 사진·그림 중복은 소아과·부인과까지 포함한 `clinical_visuals.py`의 공통 배치로 관리한다. 앞선 기록의 22개 사진 배치 방식은 이 구성으로 대체되었다.

신규 페이지: `internal-digestive.html`, `internal-functional-digestive.html`, `internal-upper-digestive.html`, `internal-lower-digestive.html`. 본문은 새로 작성했으며, 일반적인 증상·필요한 평가·한의학적 패턴진단·진료 준비를 안내한다. 근거 자료는 `content/digestive-sources.json`에 별도로 기록한다.
