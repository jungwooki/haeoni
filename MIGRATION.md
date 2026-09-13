# 홈페이지 이관 현황

확인일: 2026-09-12. 기존 주 메뉴 73개를 기준으로 작성. 전체 콘텐츠 이관 완료를 의미하지 않습니다. 게시판 글, 첨부파일, 동적 팝업, PDF/ISSUU 자료, 외부 클리닉의 하위 콘텐츠는 각 분야 이관 시 별도 조사합니다.

## 이번 단계

- 공통 메뉴·푸터와 반응형 레이아웃: 31개 HTML.
- 의료진: 기존 팝업 4개에서 인사말·약력·연구·강의 본문 모두 보존하여 개별 페이지 생성.
- 진료 분야: 7개 독립 안내/목차 페이지. 한방내과는 세부 안내 10개를 로컬 HTML로 이관. 다른 분야는 원본에 연결하며 상세 본문 이관 대기.
- 한의원 소개·역사·사회공헌: 기존 텍스트 보존. 부속 이미지 추가 이관은 별도 검토.
- 방문 안내: 시간·주차·현재 2층 주소 반영. 둘러보기 공간사진 13장 이관.

## 원문과 보존

- content/legacy/: 작업 전 로컬 HTML 전체 보존.
- content/source-content.json: 메뉴 73개 URL의 추출 텍스트 블록과 이미지 URL. 외부 클리닉 등 다른 구조의 페이지는 텍스트 블록이 비어 있을 수 있어 본문 확보 완료로 간주하지 않음.
- content/doctors-original.json: 기존 의료진 팝업 4명의 본문 원문.
- content/source/: 이번에 읽은 한의원 소개/이용 안내 원본 HTML.

## 충돌·추가 확인 사항

- /93 본문은 2층, 하단 옛 주소는 10층으로 충돌. 현재 홈페이지 및 /time 기준 2층 9호를 사용.
- /86 인사말의 2025년 이전 예정 표현, /87의 연인원 통계, 조내경 원장 인사말의 “7년째”는 원문에 남아 있음. 현재 실적/재직연수로 재해석하지 않도록 작성 당시 기록임을 표시.
- 기존 로컬 02-1.clinic_child.html은 소아과가 아닌 공간 소개 내용. 소아과 원본은 /kids 및 /kids10 기준으로 이관 예정.
- 원장별 진료일정, 일요일/공휴일 일정은 별도 문의. 임의 생성하지 않음.
- 병원 규모, 입원병동, 7개 별도 조직, 모든 환자 4인 공동진료 등 확인되지 않은 운영 사실을 추가하지 않음.

## 다음 작업 순서

1. 한방내과: 주요 세부 안내 10개 이관 완료. 연관 게시물·자료집 상세 이관은 추후 별도.
2. 소아과: 통합 관점 → 소아치료·한약 → 허약체질 → 호흡기·파파증후군 → 성장.
3. 부인과: 생애주기 → 임신준비·난임 → 산후 → 유산회복 → 여성질환.
4. 비만 → 체질관리 → 통증재활 → 스포츠 MPS.
5. 게시판·자료·비급여·개인정보 등 잔여 콘텐츠와 기존 URL 호환 정책.


## 한방내과 상세 이관

기존 세부 메뉴 12개를 중복 정리하여 10개 안내로 구성. 사진·도해 20개, 본문 목차, 관련 안내 연결을 포함. 세부 근거는 [INTERNAL_MIGRATION.md](INTERNAL_MIGRATION.md) 참조. 공개 대상 HTML 38개에 상담·예약·오시는 길 플로팅 메뉴 적용.

| 기존 메뉴 | 원본 | 새 페이지 | 상태 |
|---|---|---|---|
| 한의원소개 | /about | 01_1.about.html | 소개 본문 이관 / 부속 이미지 추가 검토 |
| 인사드립니다. | /86 | 01_1.about.html | 소개 본문 이관 / 부속 이미지 추가 검토 |
| 의료진 소개 | /165 | 01_2.team.html | 이관 |
| 역사와 전통 | /87 | history.html | 소개 본문 이관 / 부속 이미지 추가 검토 |
| 진료시간 안내 | /time | time.html | 이관 |
| 둘러보기 | /92 | 01_4.tour.html | 이관 |
| 오시는 길 | /93 | 01_3.location.html | 이관 |
| 사회공헌 프로그램 | /142 | contribution.html | 소개 본문 이관 / 부속 이미지 추가 검토 |
| 소아청소년 | /kids | kids10.html | 분야별 목차 구축 / 상세 본문 미이관 |
| 한방소아과 안내 | /kids10 | child-overview.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 소아진료, 통합적 관점으로 | /120 | child-integrated.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 소아침, 뜸, 한약 | /144 | child-treatments.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 소아치료의 종류 | /kids3 | child-treatments.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 한약 처방의 특징 | /146 | child-herbal-prescription.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 한약 복용방법, 주의사항 | /kids5 | child-herbal-guide.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 허약체질 클리닉 | /152 | child-constitution.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 허약아 유형과 보약 | /147 | child-constitution.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 녹용의 역할 | /kids4 | child-antler.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 호흡기질환 클리닉 | /155 | child-respiratory.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 계절별 감기와 가정관리 | /154 | child-respiratory.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 감기 예방 방법들 | /156 | child-cold-prevention.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 감기의 치료관리 | /rhini4 | child-cold-care.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 호흡기감염병 치료관리 | /157 | child-infections.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 파파증후군 | /169 | child-pfapa.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 파파증후군 한의학적접근 | /170 | child-pfapa-care.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 키성장 클리닉 | /kids7 | child-growth.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 키성장 부진? | /148 | child-growth.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 키성장부진 유형 | /149 | child-growth-causes.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 키성장 진단 | /151 | child-growth-diagnosis.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 키성장 치료 | /150 | child-growth-care.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 여성 | /woman | woman1.html | 분야별 목차 구축 / 상세 본문 미이관 |
| 한방부인과 안내 | /woman1 | women-overview.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 생애주기별 건강관리 | /61 | women-life-stages.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 난임 및 임신준비 | /64 | women-pregnancy-planning.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 임신준비 | /100 | women-pregnancy-planning.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 난임은 불임과 다릅니다. | /101 | women-infertility.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 난임을 치료하는 방법 | /104 | women-infertility-care.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 여성의 난임 | /102 | women-female-infertility.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 남성의 난임 | /139 | women-male-infertility.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 난임시술과 한의약치료병행 | /138 | women-assisted-reproduction.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 임신중 출산 과정까지 | /106 | women-pregnancy.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 산후 클리닉 | /65 | women-postpartum.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 산후조리는 잘 해야합니다 | /107 | women-postpartum.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 산후에 변화하는 몸 | /108 | women-body-changes.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 산후, 예방과 치료 | /109 | women-postpartum-care.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 산후 조리 방법 | /110 | women-postpartum-lifestyle.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 자연친화적 육아안내 | /113 | women-parenting.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 유산회복 클리닉 | /66 | women-miscarriage.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 유산 원인과 몸의 변화 | /114 | women-miscarriage.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 유산후 생활관리 | /115 | women-miscarriage-lifestyle.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 계류유산과 중절수술 후 치료 | /116 | women-miscarriage-surgery.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 반복유산 치료와 착상탕 | /117 | women-recurrent-loss.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 여성질환 클리닉 | /62 | women-uterus-ovaries.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 자궁과 난소의 질병 | /96 | women-uterus-ovaries.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| PMS 스트레스와 마음의 병 | /98 | women-pms-stress.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 수족냉증, 찬 체질 | /99 | women-cold-sensitivity.html | 본문·사진 이관 / 연관 게시물·자료 원본 연결 |
| 내과비염 | /rhinitis | clinic-internal.html | 세부 안내 10개 로컬 연결 |
| 호흡기내과 안내 | /rhini1 | rhini1.html | 한방내과 본문·사진 이관 / 연관 게시물·안내책자는 원본 연결 |
| 코목 5분약솜 | /rhini50 | internal-cotton-care.html | 한방내과 본문·사진 이관 / 연관 게시물·안내책자는 원본 연결 |
| 비염축농증 클리닉 | /79 | internal-rhinitis.html | 한방내과 본문·사진 이관 / 연관 게시물·안내책자는 원본 연결 |
| 비염? | /rhinitis1 | internal-rhinitis.html | 한방내과 본문·사진 이관 / 연관 게시물·안내책자는 원본 연결 |
| 코가 하는 일 | /126 | internal-nose-function.html | 한방내과 본문·사진 이관 / 연관 게시물·안내책자는 원본 연결 |
| 6단계 진단 | /rhini7 | internal-diagnosis.html | 한방내과 본문·사진 이관 / 연관 게시물·안내책자는 원본 연결 |
| 비염 치료는 이렇게 | /153 | internal-rhinitis-treatment.html | 한방내과 본문·사진 이관 / 연관 게시물·안내책자는 원본 연결 |
| 기침천식 클리닉 | /rhini9 | internal-cough.html | 한방내과 본문·사진 이관 / 연관 게시물·안내책자는 원본 연결 |
| 기침의 유형 | /131 | internal-cough.html | 한방내과 본문·사진 이관 / 연관 게시물·안내책자는 원본 연결 |
| 기침의 유형별 치료 | /141 | internal-cough-treatment.html | 한방내과 본문·사진 이관 / 연관 게시물·안내책자는 원본 연결 |
| 감기 클리닉 | /rhini3 | internal-cold.html | 한방내과 본문·사진 이관 / 연관 게시물·안내책자는 원본 연결 |
| 중이염 클리닉 | /rhini14 | internal-otitis.html | 한방내과 본문·사진 이관 / 연관 게시물·안내책자는 원본 연결 |
| 통증 스포츠MPS | https://haeon.sportsmps.com/ | clinic-sports.html | 분야별 목차 구축 / 상세 본문 미이관 |
| DIET | https://haeonw.com | clinic-weight.html | 분야별 목차 구축 / 상세 본문 미이관 |
| 소통 | /community | — | 원본 연결 / 상세 이관 대기 |
| 상담 및 예약 | /counsel | — | 원본 연결 / 상세 이관 대기 |

소아과·부인과 본문 및 사진 이관: [FAMILY_MIGRATION.md](FAMILY_MIGRATION.md). 세 진료과의 사진·도해 88개를 로컬에 보관합니다.
