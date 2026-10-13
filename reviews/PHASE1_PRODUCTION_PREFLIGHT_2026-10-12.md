# Phase 1 Production 배포 전 최종 검증 보고서

2026년 10월 12일 한국시간 기준, **Vercel 소스 빌드와 공개 범위·정책 라우팅의 기술 검증이 통과했다.** 로컬에서 미리 만든 dist를 업로드한 이전 Preview와 달리, 이번에는 Vercel 빌드 머신에서 Python 생성기가 직접 실행되어 dist를 만들었다. 공개 파일 240개와 내부 파일 차단을 실제 HTTP로 확인했다.

Production은 배포하지 않았으며 운영 도메인·원격 프로젝트 설정·Git main 커밋·원격 main을 유지했다. **현재 main에는 Phase 1 설정이 반영되지 않았다.** 검증된 검토 작업트리와 현재 main을 구분해야 하며, 기존 main을 그대로 재배포하는 것은 검증된 변경안의 운영 반영이 아니다. Production과 Git 반영 경로는 최종 보고서 검토 후 별도 승인 대상이다.

의료진 미승인 수정 후보는 게시하지 않았다. 본문·디자인·정책 원문·의료진 정보·기존 공개 자산과 보관 자료 379개 파일은 기존 기준선과 바이트 단위로 같다. 의료 콘텐츠의 기존 P0와 P1 URL·canonical·검색 등록 작업은 이번 승인 범위에 포함하지 않았다.

## 실제 소스 빌드와 배포 식별

| 항목 | 확인 결과 |
| --- | --- |
| 프로젝트 | `haeoni`, `prj_07fVNTSiyTNNdWA4Kt9s1Q2KuuXL` |
| 팀 | `team_4k8fGza3TZ56wuF86DuHdd0z` |
| 소스 빌드 Preview | [검증된 소스 빌드 Preview](https://haeoni-9l7cwc5ta-haeons-projects.vercel.app/) |
| Preview ID | `dpl_DYLCkTxSVBhEr9VZYGvfUzjbKqpR` |
| 배포 상태 | READY, target null인 Preview, alias 없음 |
| 실제 실행 | Vercel CLI 62.7.0 빌드 머신에서 생성기 81개 페이지 생성·독립 검사 통과 |
| 업로드 입력 | 288개 명시적 소스 파일. dist 업로드 0개 |
| 공개 출력 | 본문 81개 + 기존 HTML fallback 11개 + 자산 148개 = 240개 |
| 소스 전용 입력 | 48개. 스크립트·필수 원고/메타 입력·설정·무해한 내부 검증 표식·중복 처리용 이미지 포함 |
| 제외 이미지 | 8개 모두 소스 입력에도 없고 dist에도 없음. 원본은 로컬에 보관 |
| Production | `dpl_HAka2QhgByhhw2DX3HGfmPTt6Pa9` 유지 |
| Git 기준선 | 로컬 HEAD 및 원격 main 모두 `93ecccaf8b2a46e1dc379cc0e34326939e9e4797` |

소스 입력을 준비할 때 공개 의존 이미지 외에 중복 판별에 필요한 비공개 이미지 1개가 필요함을 확인했다. 이를 소스 입력으로만 명시하고 public-files 허용 목록에는 추가하지 않았다. 해당 이미지의 실제 Preview URL도 404였다.

원문 백업 디렉터리 전체·audit 근거·skills·의료 검토 문서를 업로드하지 않았다. 대신 audit·skills·reviews 아래에 동일한 무해한 검증 표식을 입력으로 넣어, 소스에 실제 존재해도 공개되지 않는다는 것을 확인했다. 생성에 필수인 `content/legacy/index.html`과 원고 JSON은 비공개 빌드 입력이며 실제 URL로 제공되지 않았다. 실제 환자·외부 EMR 자료를 찾거나 복사하지 않았다.

## Git와 Vercel 빌드 설정 정합성

| 확인 대상 | 실제 상태 | 판정 |
| --- | --- | --- |
| 검토 작업트리의 vercel.json | buildCommand `python3 scripts/build_site.py --public`, outputDirectory `dist`, framework null, cleanUrls false | 승인된 Phase 1 설정 유지 |
| 업로드된 소스 vercel.json | 로컬 파일과 같은 SHA-1 `572d40cf0255ceee9c7a27a1a3cedb5632e3c594` | 내용 일치 |
| Vercel 대시보드 | Framework Other, Root Directory 빈 값, Build/Output/Install override 해제 | 기존 기본값 유지; 소스 파일 설정이 우선 |
| Vercel 실행 로그 | 사전 dist 없이 생성기 실행, 81개·148개 자산·240개 공개 파일 검사 PASS, 배포 완료 | 파일 설정의 실효 동작 확인 |
| 연결 저장소 | `jungwooki/haeoni`, Vercel Git 화면에서 연결 확인 | 대상 일치 |
| 원격 main·로컬 HEAD | `git ls-remote origin refs/heads/main`과 `git rev-parse HEAD` 동일 | main 커밋 변경 없음 |
| 현재 main의 Phase 1 파일 | `git ls-tree HEAD vercel.json` 결과 없음 | **main 미반영. 자동 Git 배포 경로는 아직 갱신되지 않음** |

검토 작업트리와 **이번 소스 빌드 Preview의 실효 설정은 일치한다.** Git main과 새 설정이 이미 일치한다고 보고하지 않는다. Git push와 main 변경을 승인하지 않은 조건을 지키면서, 내용 해시로 식별되는 소스 스냅샷을 API로 Preview 배포했다. 별도 branch·commit·PR·push·프로젝트 설정 저장을 실행하지 않았다.

Vercel 파일 설정은 대시보드 기본값보다 우선하므로 대시보드의 Output Directory를 추가로 수정할 필요는 없었다. [Vercel buildCommand와 outputDirectory 설정](https://vercel.com/docs/project-configuration/vercel-json)

## 이번 단계의 변경 파일

| 파일 | 변경 목적과 영향 |
| --- | --- |
| `scripts/clinical_visuals.py` | 이미 비노출인 8개 이미지에 대한 hash registration을 건너뛰어 소스 빌드 입력에서도 해당 원본을 요구하지 않음. 공개 HTML 변화 없음 |
| `scripts/prepare_source_preview.py` | 생성에 필요한 명시적 소스만 새 임시 폴더에 준비하고 동일한 공개 빌드를 실행. 원본 삭제·Git 변경·원격 API 호출 없음 |
| `README.md` | 소스 검증 방법과 main 미반영 조건 안내 |
| `reviews/PHASE1_PRODUCTION_PREFLIGHT_2026-10-12.md` | 최종 검증·Production 영향·승인 조건·롤백 보고 |
| `audit/2026-10-12/source-build/` | 입력 해시·빌드 로그·설정 화면·검사 결과·diff 근거 |

Phase 1의 기존 `vercel.json`, public-files·public-regression 설정과 공개 빌드·검증 코드는 그대로 사용했다. 이번 변경으로 301·새 rewrite·canonical·의료 원고를 추가하지 않았다. 모든 원본 이미지·백업·기존 감사 보고서를 보존했다.

## 검사 결과

| 검사 | 결과 | 범위 |
| --- | --- | --- |
| 최소 소스 스냅샷 로컬 빌드 | PASS | 288개 소스 입력에서 생성. 제외 이미지 없이 생성기 동작. public dist 240개·원본 해시 일치 |
| 일반 작업트리 공개 빌드 | PASS | 기존 전체 보관 자산을 가진 프로젝트에서도 동일한 공개 산출물 생성 |
| 로컬 test_public.py | 11개 모두 PASS | 정상 제공·정책 307·원문 보존·비공개 GET/HEAD 404·앵커·라우팅 계약·부정 입력·후보 설정 검사 |
| check_site.py | 전체 PASS | 외부 EMR 없이 81개 페이지·4인 의료진·진료 본문·원본 사진·메뉴·탭·출판 편집 보존 |
| check_assets.py | PASS | 보관 자산 165개 검증. 공개 자산은 148개로 제한 |
| Vercel 소스 빌드 | PASS | 288개 다운로드 → 생성기 실행 → 공개 검사 PASS → /vercel/output 배포 완료. 사전 dist 입력 0개 |
| 실제 Preview HTTP | **309건 모두 PASS** | 최종 200 244건, 404 65건. 공개 파일 240개 전체·정책 쿼리 4개·소스 전용 48개·제외 이미지 8개·구/없는 URL 8개·빌드가 만든 audit 기록 1개 |
| 이미지 실제 제공 | PASS | 129개 이미지 URL 모두 200 및 image MIME 확인 |
| 텍스트 콘텐츠 무결성 | PASS | HTML 92개·CSS/JS 19개·SVG 2개·정책 조회 4개, 총 117건의 콘텐츠 해시 일치 |
| 실제 Preview 브라우저 | PASS | 6개 대표 페이지 × 1440·390·320px, 18개 화면. 가로 넘침·깨진 이미지 없음, H1 1개, 예약·상담 URL 유지 |
| 동작 검사 | PASS | 모바일 메뉴 열기/닫기, 진료 탭, 키보드 Home, #guide-1 직접 진입 시 관련 탭과 항목 열림 |
| 자료 보존 | PASS | 기존 HTML·assets·content 379개 파일 변경 0개 |

HTML에는 Vercel이 문서 끝에 삽입한 이번 배포 ID의 정확한 피드백 스크립트가 붙는다. **그 고정 suffix 한 개만** 구분한 본문 해시가 원본과 같으며 다른 변경을 무시하지 않았다. CSS/JS와 SVG는 원시 콘텐츠 해시를 대조했다. 바이너리 이미지의 원격 검사는 HTTP 상태·MIME와 브라우저 표시 검사이며, 이미지 바이트 보존은 소스·로컬·클라우드 공개 빌드의 해시 gate가 확인했다.

정책 쿼리는 `/`와 `/index.html`의 `mode=privacy`를 privacy.html, `mode=policy`를 terms.html로 연결한다. 원본 정책 파일은 동일하다. 인증 HTTP 도구는 redirect를 따라가므로 실제 첫 307과 전체 Location 체인을 관측한 결과로 표현하지 않는다. 첫 307·쿼리 보존·루프 방지는 로컬 HTTP 검사가 확인했고, 실제 Preview에서는 올바른 정책 본문·최종 200을 확인했다.

진료 페이지 최초 진입의 탭 검사는 deferred JS 초기화 후 보이는 탭을 기다린 뒤 확인했다. 화면 초기화 전에 DOM을 읽은 한 차례의 검사 호출 오류를 콘텐츠 변경으로 처리하지 않았다. 마지막에 올바른 직접 앵커·탭 상태를 다시 확인했다.

예약·상담 동선은 81개 본문의 링크·공통 메뉴 보존과 실제 브라우저의 네이버 예약·카카오톡 URL로 검사했다. 실제 예약 제출·상담 메시지 전송은 하지 않았다. 외부 예약 서비스의 전체 로그인·예약 확정 과정, CWV·실제 검색 성과는 이번 검사 범위가 아니다.

## Deployment Protection과 색인 제외

Vercel 프로젝트의 SSO 보호는 `enabled: true`, `all_except_custom_domains`로 유지됐다. 일반 인증 없는 Preview 요청은 Vercel SSO로 302 이동했다. 보호 설정을 해제하지 않고 연결된 계정의 인증 조회를 사용해 앱의 실제 200/404를 확인했다.

인증 후 검증한 309개 응답에는 Preview noindex가 있었다. 기존 `.vercel.app` 호스트 조건은 유지했고 운영 custom domain용 noindex를 추가하지 않았다. 장기 bypass secret·로그인 쿠키·환경변수를 읽거나 소스·보고서에 저장하지 않았다.

## 재현 방법과 근거

프로젝트 루트에서 실행한다. 새 destination을 사용하며 기존 임시 폴더를 삭제하거나 덮어쓰지 않는다.

```sh
python3 scripts/build_site.py --public
python3 scripts/check_public.py
python3 scripts/test_public.py
python3 scripts/check_site.py
python3 scripts/check_assets.py
python3 scripts/prepare_source_preview.py --destination /tmp/haeoni-source-preview-recheck
git rev-parse HEAD
git ls-remote origin refs/heads/main
git ls-tree HEAD vercel.json
git diff --check
```

`source-input-manifest.json`이 **원격에 전달할 입력 목록**이다. 로컬 사전 검사 중 destination 안에 생성된 dist는 이 목록에 없으며, 폴더 전체를 무조건 업로드해서는 안 된다. 이번 API 요청은 같은 프로젝트·팀, 이 목록의 288개 파일, 수정하지 않은 vercel.json을 사용했다. target을 생략해 Preview로 생성했고 projectSettings override·production alias·Git 소스를 지정하지 않았다. [Vercel 배포 API의 Preview 기본값](https://vercel.com/docs/rest-api/deployments/create-a-new-deployment)

로그는 연결된 Vercel 도구 `list_deployment_events`에 이번 ID와 팀 ID를 넘겨 조회할 수 있다. 보호된 URL의 HTTP 재현은 `web_fetch_vercel_url` 또는 인증된 Vercel CLI의 `vercel curl`을 사용한다. 보호 설정을 끄거나 인증 없는 302를 앱의 상태 코드로 집계하지 않는다.

`audit/2026-10-12/source-build/`에 다음 근거를 저장했다.

- source-input-manifest.json, source-build-preflight.json: 입력 목록·해시, 사전 dist 없음, 설정 동일성, Git 기준선.
- vercel-build-logs.json, source-tree-metadata.json: 원격 생성기 실행·PASS와 소스 파일 식별. 파일 트리 API가 일부 깊이를 생략한 부분은 전수 트리 확인으로 주장하지 않는다.
- vercel-build-settings.txt, vercel-git-settings.txt: 읽기 전용 대시보드 확인.
- local-tests.json, preview-http.json, browser-responsive.json, browser-interactions.json, final-summary.json: 종료 코드·응답·해시·동작 결과.
- production-unchanged.json, project-protection.json, source-preview.json, changes.patch: 운영·보호·Preview 식별과 이번 단계 diff.

## Production 영향과 별도 승인 조건

운영 반영 시 정상 HTML·CSS·JS·사용 이미지는 그대로 제공한다. 현재 공개되어 있는 원문·백업·스크립트·검토 문서·미사용 자산·제외 이미지 URL은 실제 404가 된다. 기존 의료 콘텐츠·의료진·디자인·상담 예약 링크·호스트·진료 URL 정책을 바꾸지 않는다. 정책 쿼리는 해당 정책 페이지로 이동한다.

**아직 운영 문제를 해결했다고 표현할 수는 없다.** Production 도메인은 기존 배포를 유지한다. 반영 대상은 이번에 검증한 소스·설정·입력 해시이며 현재의 미수정 main이 아니다. Git 배포 경로를 사용하려면 검토한 변경을 Git에 반영할 별도 승인이 필요하다. 현재 승인에 없는 push·main 변경을 실행하지 않았다.

Production 승인은 최종 보고서 확인 후 별도로 받아야 한다. Preview를 임의 promote하거나 기존 main을 재배포하지 않는다. 승인된 Production 빌드에서는 dist만 출력되는지, 정상 파일 200·내부 파일 404·정책 도착 페이지·운영 custom domain의 noindex 부재를 확인해야 한다. 의료 원고·P1 이전·canonical·검색엔진 등록 승인은 별개다.

## 롤백 계획

기존 운영 배포로 단순 rollback하면 내부 자료 공개가 되살아날 수 있다. 안전한 복구 기준은 **기존 본문·디자인·자산을 유지하며 공개 허용 목록과 dist 경계를 계속 적용하는 패키지**다. 검증된 공개 manifest와 소스 입력 해시를 보관한다.

정책 라우팅 문제가 있으면 승인된 범위에서 정책 규칙만 복구하고 공개 경계는 유지한다. 누락 자산이 확인되면 해당 자산을 개별 검토·허용하고 빌드와 공개 검사부터 다시 실행한다. 전체 assets·원문·백업을 임시로 공개 복사하지 않는다.

이번 로컬 최소 변경은 `changes.patch`로 검토하거나 파일별로 되돌릴 수 있다. 제외 이미지를 해시 등록에서 생략하는 변경을 되돌리면 최소 소스 스냅샷이 제외 원본을 다시 요구하므로 소스 준비·생성기 조건을 함께 검토해야 한다. 원본·감사 근거를 삭제하는 reset/clean은 사용하지 않는다. 운영 rollback·promote와 Git 작업은 추가 승인 없이 실행하지 않는다.
