# 해온한의원 공개 빌드 구현과 배포 검토 보고서

공개 전용 빌드와 독립 검증을 구현했고, 승인된 실제 Vercel preview에서 제외 자료 404와 정책 이동을 확인했다. 디자인·81개 본문·정책 원문·의료진 정보·기존 공개 자산은 변경하지 않았다. 운영 배포와 git push, 검색엔진 등록은 수행하지 않았다.

**운영 사이트에는 아직 이 수정이 반영되지 않았다.** 의료 원고 오류와 녹용 표현은 미승인 후보만 작성했으며 기존 원고를 바꾸거나 후보를 게시하지 않았다. 의료 관련 P0 전체가 해소된 상태가 아니다.

## Git와 배포 기준선

- Git HEAD: `93ecccaf8b2a46e1dc379cc0e34326939e9e4797`. 기존 사용자 미추적 문서·config·skills·audit를 보존했다.
- 운영 배포: `dpl_HAka2QhgByhhw2DX3HGfmPTt6Pa9`. Preview 생성 후 `haeoni.com` 조회에서도 동일한 production 배포와 커밋이었다. 도메인 연결·보호 설정을 변경하지 않았다.
- Preview: [해온 공개 빌드 검토](https://haeoni-6uyr2ty4r-haeons-projects.vercel.app/), ID `dpl_4PRof7zDAcVcAQv9RkKpGXyTf7Nk`, READY, target null인 preview이며 alias는 비어 있다. 기존 Vercel 인증 보호를 유지한다.
- 기존 HTML·자산·content 379개 파일 해시를 기록했고 작업 종료 시 변경 0개를 확인했다. 원문 백업·감사 근거·공개 제외 이미지도 삭제하지 않았다.

## 검토 단위와 변경 파일

| 단위 | 파일 | 역할 |
| --- | --- | --- |
| 공개 빌드 | `scripts/build_public.py`, `scripts/public_files.py`, `scripts/build_site.py`, `config/public-files.json`, `.gitignore` | 격리 생성, 경로·심볼릭 링크 검사, 명시적 허용 목록, 참조 그래프, 원본 보존, dist 분리 |
| 독립 검증 | `scripts/check_public.py`, `scripts/test_public.py`, `scripts/serve_public.py`, `config/public-regression.json` | 81개 본문·자산·해시·앵커·SEO·동선·정책·제외 경로·라우팅 검사 |
| EMR 분리 | `scripts/check_site.py`, `scripts/check_care_source.py` | 기존 공개 회귀 검사를 외부 EMR 의존 없이 완료; 원자료 ID 대조는 명시적 별도 검사 |
| 배포와 URL 설계 | `vercel.json`, `config/vercel-p1-routing.candidate.json`, `config/legacy-routing-review.json`, `reviews/VERCEL_ROUTING_DESIGN_2026-10-12.md` | dist 출력, 정책 쿼리 이동, preview noindex, 미승인 P1 명세 분리 |
| 의료 검토와 운영 문서 | `reviews/MEDICAL_COPY_CANDIDATES_2026-10-12.md`, 이 보고서, `README.md` | 게시 금지 후보·검토 항목·명령·제한·롤백 |

패치는 `audit/2026-10-12/implementation/patches/`에서 위 단위로 검토할 수 있다. 로컬 커밋이나 원격 PR은 만들지 않았다.

## 공개 빌드 동작

`python3 scripts/build_site.py --public`은 기존 생성기를 임시 작업 폴더에서 실행한다. 기존 root 생성 방식도 유지되지만 Vercel buildCommand는 `--public`을 사용한다. 생성 결과가 현재 루트 HTML과 바이트 단위로 다르면 빌드를 실패시켜 수동 편집·원고 변경을 조용히 덮어쓰지 않는다.

본문 81개와 이동용 HTML 11개는 명시적 파일명 목록이다. 자산도 148개를 명시적으로 승인한 목록이다. HTML의 src·href·poster·srcset·inline CSS, CSS url·import와 폰트, 정적 JS import를 추적한 실제 의존 그래프가 허용 목록과 **정확히** 같아야 통과한다. 사용되지 않는 파일이나 새로 참조된 미승인 파일은 실패한다. 전체 assets 또는 저장소를 배포 폴더에 복사하지 않는다.

공개 제외 이미지가 참조되거나 허용 목록에 들어가면 실패한다. 숨김·경로 이탈·심볼릭 링크·없거나 빈 파일도 실패한다. 임시 산출물을 검증한 뒤 dist로 옮기며 독립 검사 실패 시 dist를 제거한다. 실패한 재빌드가 이전 산출물을 남기지 않도록 빌드 시작 시 기존 dist를 무효화한다.

현재 `config/public-regression.json`은 안전성 변경의 콘텐츠·디자인 기준선이다. 모든 공개 파일의 원본·산출물·기준선 SHA-256이 같아야 한다. 의료 후보를 자동 승인하거나 기존 원고에 덧붙이지 않는다. 향후 승인된 변경은 생성 입력과 기준선 갱신을 함께 검토해야 한다.

## 검사 결과

| 검사 | 결과 | 범위와 근거 |
| --- | --- | --- |
| 공개 빌드 | 통과 | 본문 81개, fallback 11개, 자산 148개, 총 240개. `public-build-manifest.json` |
| 독립 공개 SEO 검사 | 통과 | 링크·앵커·메타·H1·모바일 메뉴·상담·예약·정책·해시·파일 경계·설정. 외부 EMR 없음 |
| HTTP와 부정 입력 검사 | 11개 테스트 통과 | 로컬 240개 파일 GET 200·바이트 동일, 내부 경로 GET·HEAD 404, 정책 307·본문 보존, 구 URL 404, P1 후보의 네 rewrite·308 체인, 누락·제외·심볼릭 링크·경로 이탈·CSS 폰트·srcset |
| 기존 check_site | 전체 통과 | 81개·4인 의료진·진료 원문·사진·매핑·탭·게시 제외·편집 override 보존. 외부 EMR 조회 제거 |
| 기존 check_assets | 통과 | 165개 보관 자산 ID·해시·카탈로그·참조 검사. 공개 출력은 이 중 148개만 포함 |
| 로컬 브라우저 | 통과 | 홈·내과·소아·부인과·위치·의료진 6개 페이지 × 1440·390·320px, 18개 화면에서 가로 넘침·깨진 이미지 없음 |
| 인터랙션 | 통과 | 모바일 전체 메뉴 열기·닫기, 자세한 안내 탭, 펼친 본문, 진료 준비에서 Home 키, `#guide-1` 직접 진입 시 해당 탭·본문 열기, 개인정보 쿼리 도착 |
| 실제 preview HTTP | 134건 통과 | 본문 81개·CSS/JS 19개·정책 쿼리 4개 최종 200, 제외 이미지 8개·내부 자료 14개·미승인 짧은/구/없는 URL 8개 404. 모두 noindex |
| 실제 preview 브라우저 | 통과 | 홈 렌더링·기존 이미지 표시·가로 넘침 없음. 예약 링크는 확인만 하고 예약 제출 안 함 |

실제 preview HTML은 Vercel이 문서 끝에 추가한 **동일 배포 ID의 정확한 피드백 스크립트 한 개** 때문에 원시 해시가 다르다. 그 고정 suffix만 분리한 81개 본문과 정책 조회 4개의 콘텐츠 해시는 로컬과 일치했다. 다른 스크립트나 임의 본문 차이는 무시하지 않았다. 19개 CSS/JS는 원시 내용 해시가 그대로 일치했다. 원시·콘텐츠 해시와 suffix 여부를 `preview-http.json`에 기록했다.

실제 preview 조회는 인증 connector가 redirect를 따라간 결과다. 올바른 정책 본문과 final 200을 확인했지만 첫 307과 전체 Location 체인을 직접 관측한 검사로 표현하지 않는다. 첫 307·추적 쿼리 유지·루프는 로컬 HTTP에서 확인했다. 실제 제외 경로는 인증을 통과한 앱 응답의 404이며 SSO 보호 페이지를 404로 오인한 결과가 아니다.

브라우저 검사는 viewport·이미지·동작의 표본 검사이며 81개 모두의 시각 검사나 CWV 측정은 아니다. 공개 패키지의 모든 148개 자산은 로컬에서 HTTP와 해시로 검사했으며 실제 preview에서는 19개 CSS/JS, 홈 이미지 표시와 배포 패키지를 확인했다. 실사용 성능·실제 검색 색인·예약 완료는 검증 범위에 포함하지 않는다.

## 실제 preview 방식과 제한

사용자가 별도로 승인한 preview만 생성했다. 로컬에서 만든 240개 공개 파일을 dist 아래에 업로드하고 Vercel의 outputDirectory도 dist로 지정했다. 내부 원문·scripts·audit·skills·검토 문서·의료 후보는 업로드하지 않았다.

Preview 패키지는 이미 빌드된 파일이므로 패키지 안 vercel.json의 buildCommand·installCommand는 빈 문자열이다. 라우팅·헤더·outputDirectory는 동일하다. API의 target을 생략하면 preview가 된다는 문서 규칙을 사용했고 응답 target null·alias 없음으로 확인했다. 처음의 잘못된 프로젝트 ID와 지원되지 않는 target 값 요청 두 건은 400으로 거절됐으며 배포를 만들지 않았다. 이후 올바른 프로젝트와 문서화된 preview 기본값으로 성공했다. [Vercel 배포 API](https://vercel.com/docs/rest-api/deployments/create-a-new-deployment)

이 preview는 공개 파일 경계와 라우팅을 실제 Vercel에서 검증한다. 소스 전체를 업로드해 Vercel 빌드 머신에서 Python 생성기까지 실행한 검증은 아니다. **운영 소스 배포 승인 전에는 full-source preview에서 Python·buildCommand·outputDirectory를 추가 검증해야 한다.** 원격 project settings나 production alias를 변경하지 않았으며 운영 배포의 ID·커밋도 유지된다.

인증 보호는 끄지 않았다. 연결 계정의 Vercel 인증 조회가 만든 임시 접근을 사용했으며 장기 bypass secret·사용자 인증 정보를 소스·보고서·증거 파일에 저장하지 않았다. 일반 공개 요청은 Vercel 인증으로 이동한다. Preview의 색인 제외 헤더도 확인했다.

## 감사 항목별 현재 상태

| 항목 | 구현 또는 준비 상태 | 운영 상태 |
| --- | --- | --- |
| P0 공개 제외 자료 접근 | 공개 파일 경계 구현, 로컬·preview 404 확인 | 기존 운영에는 미반영 |
| P0 정책 쿼리 | 4개 조건부 정책 이동 구현, 원문 보존·preview 목적 본문 확인 | 기존 운영에는 미반영 |
| P0 절박유산 오류 | 오류 표시·안전 안내 원고 후보·근거·승인 기록 작성 | 기존 원고 유지, 의료진 승인 대기 |
| P0 녹용 우월 표현 | 광고·근거 검토 항목과 최소 표현 후보 분리 | 기존 원고 유지, 의료진·광고 검토 대기 |
| P1 짧은 진료 URL | 네 rewrite와 슬래시 308 후보·로컬 검사 완료 | active 설정·preview에 미적용 |
| P1 구 URL 71개 | 개별 승인 대기 명세, 적용 false | 일괄 redirect 없음 |
| P1 canonical·robots·XML·서버 이동·사업 증빙 | 기존 감사와 설계 제약 보존 | 후속 검토 필요; 이번에는 구현하지 않음 |
| P1 외부 EMR 검사 의존 | 공개 필수 검사 분리·전체 통과 | 코드 검토 후 적용 가능 |

SEO 검사 통과는 알려진 canonical 누락 81개가 해결됐다는 뜻이 아니다. 이를 알려진 P1 부채로 출력하고 잘못된 홈 canonical·noindex를 추가하지 않는 안전성을 검사한다. 검색 등록·색인 요청·성과 개선을 주장하지 않는다.

## 위험요소와 운영 승인 범위

1. 생성기와 root HTML의 드리프트는 의도적으로 빌드를 막는다. 승인된 원고 편집 후에도 root 생성본과 허용 목록·해시 기준선 갱신이 필요하다.
2. 동적으로 계산하는 새 JS 자산 경로는 정적 추적으로 충분히 발견하지 못할 수 있다. 새 동적 로딩 도입 시 실제 브라우저 네트워크와 목록을 함께 검토한다. 현재 코드에서는 필요한 로컬 자산과 이미지 동작이 유지됐다.
3. 외부 Pretendard CDN·번역·예약·상담 서비스는 기존대로 외부 의존이다. 외부 폰트를 다운로드·교체하거나 실제 예약을 생성하지 않았다.
4. 의료 후보는 공개 패키지에 없다. 현재 본문에 남은 오류·광고 검토 항목은 의료진 승인 후 별도 변경해야 한다. 기술 변경만 운영 반영하는 승인은 의료 원고 승인으로 해석하지 않는다.
5. P1 후보 설정은 active 파일과 혼동하지 않도록 별도 경로에 보관한다. 전체 cleanUrls·71개 일괄 redirect·전체 홈 canonical을 활성화하지 않는다.
6. 원문 파일을 공개 URL에서 제거해도 원본 보관 파일은 남는다. 로컬 파일 접근 권한과 의료·개인정보 검토는 별도 책임 범위다.

현재 제출하는 승인 대상은 **공개 파일 경계와 정책 라우팅의 기술 변경**이다. 운영 배포, 소스 업로드 preview, P1 라우팅 활성화, 의료 후보 게시를 각각 별도 범위로 승인해야 한다. 이번 턴에서는 운영 배포를 진행하지 않는다.

## 롤백 계획

운영 반영 후 문제가 있더라도 감사 당시 배포로 곧바로 되돌리면 공개 제외 자료 접근이 재개될 수 있다. 안전한 롤백 기준은 **기존 81개 본문·자산을 유지하면서 동일한 공개 허용 목록과 dist 경계를 적용한 패키지**다. 현재 검사된 preview와 파일 해시 manifest를 복구 후보의 기준으로 보관한다.

정책 이동의 문제가 확인되면 승인 범위 안에서 정책 규칙만 이전 검토 상태로 되돌리고 공개 파일 경계는 유지한다. CSS·JS 누락이 있으면 원본을 변경하는 대신 필요한 승인 자산을 목록에 추가하고 빌드·회귀 검사를 다시 수행한다. 원문과 제외 이미지를 함께 복사하는 임시 복구는 금지한다.

로컬 변경은 단위별 패치 역적용 또는 파일별 검토로 되돌릴 수 있다. 기존 사용자 미추적 문서와 audit 근거를 보존하고 `git reset --hard`·`git clean`으로 전체 workspace를 지우지 않는다. 운영의 promote·rollback도 승인 없이 실행하지 않는다.

## 승인 이후 절차

1. 기술 변경 범위와 full-source preview 업로드 여부를 확인한다. 의료 후보는 승인 전 게시하지 않는다.
2. Full-source preview에서 Vercel 빌드 로그의 Python 실행, 공개 빌드 성공, 출력 dist, 공개 제외 404, 정책 목적 본문, 정상 페이지·자산을 확인한다. 기존 내부 보고서와 원문이 출력에 없는지 검사한다.
3. 승인된 운영 배포 후 public HTML·자산 200, 제외 자료 404, policy 쿼리 목적지, 기존 URL 404와 noindex의 운영 적용 여부를 검사한다. 운영 custom domain에 noindex가 있으면 통과시키지 않는다.
4. 의료진 승인 원고와 구 URL 승인 대응표는 별도 변경·검사·승인으로 다룬다. 검색엔진 등록은 별도 명시 승인 후 수행한다.

## 근거 파일

`audit/2026-10-12/implementation/`의 baseline.json, public-build-manifest.json, test-results.json, browser-responsive.json, preview-http.json, preview-deployment.json, source-preservation.json 및 단위별 patches가 근거다. 이 파일과 reviews 문서는 공개 목록에 없고 preview에서 대표 경로 404를 확인했다.
