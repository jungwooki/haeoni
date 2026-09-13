# 사이트 자산 관리

사진 148개, CSS 12개, JavaScript 7개를 용도별로 관리합니다. 사진의 해상도·품질과 CSS 적용 순서·JavaScript 실행 순서는 유지했습니다.

```text
assets/
  images/
    brand/             로고
    people/            의료진 프로필·단체 사진
    spaces/            진료실·검사실·둘러보기
    location/          위치 안내 지도
    clinic/            기존 진료·역사 사진
    clinical/
      internal/        한방내과 설명 사진·도해
      family/          소아과·부인과 설명 사진·도해
    editorial/         페이지 대표·본문 보조 사진
  styles/
    shared/            기본 디자인·공통 메뉴·상담 버튼
    home/              홈 사진 슬라이드
    clinical/          진료과 화면
    care/              진료 과정·검사·치료 안내
  scripts/
    shared/            공통 메뉴·상담 버튼·언어 선택
    home/              홈 사진 슬라이드
    clinical/          진료과 화면 동작
    care/              진료 안내 동작
```

## 파일 찾기와 사용 현황

[`content/asset-catalog.json`](../content/asset-catalog.json)은 생성기가 자동 갱신하는 전체 자산 목록입니다.

- `id`, `path`: 공통 코드에서 사용할 ID와 실제 파일 경로
- `bytes`, `sha256`: 파일 크기와 무결성 확인값
- `used_by`: 해당 파일을 직접 참조하는 HTML 또는 CSS
- `sources`, `metadata_files`: 기존 자료에서 확인되는 원본 주소와 관련 자료 파일
- `alt_texts`, `width`, `height`: 기존 자료에 기록된 이미지 설명과 크기. 없는 정보는 추정하지 않습니다.
- `status`: `published`는 현재 참조됨, `unreferenced`는 현재 HTML/CSS의 직접 참조가 없음, `withheld`는 기존 게시 제외 목록에 포함됨
- `duplicate_groups`: 파일 내용이 완전히 같은 자산 묶음

사용되지 않는 파일과 중복 파일도 보존했습니다. `unreferenced`는 삭제해도 된다는 뜻이 아닙니다. JavaScript에서 런타임에 조합하는 URL 등은 직접 참조 집계에 포함되지 않습니다.

## 사진 교체와 재사용

기존 사진을 교체할 때는 해당 폴더에서 파일을 수정하고 연결된 본문 자료의 설명·크기도 함께 확인합니다. 기존 원본의 무결성을 기록한 사진은 원본을 보존하고 새 파일로 추가하는 방식이 적합합니다.

홈 대표 사진은 [`scripts/home_hero.py`](../scripts/home_hero.py)의 `SLIDES`, 진료 사진은 [`content/clinic-photo-inventory.json`](../content/clinic-photo-inventory.json), 각 페이지 대표 이미지는 [`content/visual-guides.json`](../content/visual-guides.json)에서 연결합니다.

공통 사진은 파일 확장자를 코드에 반복하지 않고 자산 ID로 불러올 수 있습니다. 같은 ID에 확장자가 다른 파일을 중복해서 두면 오류로 알려줍니다.

```python
from site_assets import asset_url

asset_url('images/people/doctor-lee')
# assets/images/people/doctor-lee.jpg
```

원문·백업인 `content/legacy/`, `content/legacy-before-audit/`, 각 `*-source/` 폴더는 보존했습니다. 빌드에 사용하는 과거 HTML의 자산 경로는 [`scripts/site_assets.py`](../scripts/site_assets.py)가 메모리에서 변환하며, 대응표는 [`content/asset-path-migrations.json`](../content/asset-path-migrations.json)에 있습니다.

## 생성과 검증

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
python3 scripts/check_assets.py
```

사이트 생성 시 자산 목록도 함께 갱신합니다. 목록만 다시 만들려면 `python3 scripts/asset_catalog.py`를 실행합니다. 배포할 때는 새 HTML과 `assets/` 폴더를 함께 반영해야 합니다.
