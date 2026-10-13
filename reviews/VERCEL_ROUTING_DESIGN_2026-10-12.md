# 해온한의원 정책 라우팅과 진료 URL 이전 설계

정책 쿼리 수정은 `vercel.json`에 구현했으며 승인된 preview에서 확인했다. 네 진료 짧은 주소는 별도 후보 설정으로만 작성했다. 기존 구 메뉴 71개는 승인 대기 명세에만 있으며 활성 redirect에 추가하지 않았다.

## 현재 구현된 정책 라우팅

| 경로와 조건 | 도착 페이지 | 코드 | 상태 |
| --- | --- | --- | --- |
| `/` 또는 `/index.html`, `mode=privacy` | `/privacy.html` | 307 | 로컬 첫 응답 및 실제 preview 최종 본문 확인 |
| `/` 또는 `/index.html`, `mode=policy` | `/terms.html` | 307 | 로컬 첫 응답 및 실제 preview 최종 본문 확인 |
| 다른 mode 또는 일반 추적 쿼리 | 원래 페이지 | 기존 동작 | 임의 이동 없음 |

조건은 `has: [{type: query, key: mode, value: ...}]`로 지정했다. source에는 쿼리 문자열을 쓰지 않는다. 정책 대상 파일에도 mode가 전달될 수 있으나 정책 페이지에는 이 이동 규칙이 없으므로 루프가 없다. 정책 HTML과 `content/privacy-original.txt`는 바꾸지 않았다. 개인정보처리방침과 웹사이트 이용 안내의 법적 최신성 검토는 별도 업무다.

영구 이동 승인과 정책 최신성 확인 전이므로 307을 사용한다. 다른 추적 쿼리의 전달은 로컬 fixture에서 검사했다. 실제 preview 조회 도구는 redirect를 따라가므로 첫 이동 상태·전체 Location 체인 검증과는 구분한다. 실제 preview에서 네 쿼리 경로 모두 올바른 정책 HTML 내용과 일치하는 것을 확인했다.

Vercel의 `has`는 `vercel dev`에서 완전히 재현되지 않을 수 있다. 실제 preview가 조건부 라우팅의 검증 근거다. [Vercel redirects 조건](https://vercel.com/docs/project-configuration/vercel-json#redirects)

## 네 진료 짧은 URL 후보

| 후보 source | 내부 rewrite | 끝 슬래시 정리 |
| --- | --- | --- |
| `/kids10` | `/kids10.html` | `/kids10/` → `/kids10` 308 |
| `/rhini1` | `/rhini1.html` | `/rhini1/` → `/rhini1` 308 |
| `/woman1` | `/woman1.html` | `/woman1/` → `/woman1` 308 |
| `/pain1` | `/pain1.html` | `/pain1/` → `/pain1` 308 |

설정은 `config/vercel-p1-routing.candidate.json`에 있다. 로컬 HTTP 검사에서 각 짧은 주소의 본문이 `.html`과 일치하고 슬래시 이동 뒤에도 쿼리가 유지됨을 확인했다. **이 설정은 active `vercel.json`과 실제 preview에 적용하지 않았다.** Preview에서 네 짧은 주소는 현재처럼 404다.

기존 81개 본문 링크와 `.html` 접근은 유지한다. 전체 `cleanUrls` 활성화, `.html`의 영구 이동, www·홈·canonical 통합은 기존 유입과 선호 URL 결정 후 별도 변경으로 검토한다. 이 후보는 짧은 주소 접근 복구만 다루며 canonical 문제를 해결했다고 주장하지 않는다.

## 구 URL 71개 승인 대기

`config/legacy-routing-review.json`은 기존 인벤토리의 자체 도메인 상대 URL 71행을 보존한다. 각 행의 approval은 pending, enabled_in_active_config는 false다. 감사 당시 old_status 404와 대응 후보를 기록하되 유입 자료는 미확인으로 남겼다.

`/152`는 소아 허약체질과 체질보약 문맥, `/kids10` 등은 과거 세부 안내와 현재 허브의 차이가 있어 자동 대응을 금지한다. `/93`·`/165`·`/time`처럼 의미가 명확해 보이는 주소도 최신 내용과 유입을 확인한 뒤 개별 승인한다. 미이관·게시판·상담 URL에는 대체 기능 또는 404/410 유지 의도를 확인한다.

승인 후에만 특정 행을 active 설정으로 옮기고 첫 응답 301/308, 최종 canonical 200, 본문 의미, 쿼리·앵커, 호스트·슬래시·체인·루프를 검사한다. 구 URL 전체를 홈으로 이동하거나 목록 전체를 자동 적용하지 않는다. 현재 11개 HTML 이동 fallback도 유지했으며 서버 이동 전환은 별도 검토다.

## 공개 범위와 preview

active 설정은 `outputDirectory: dist`, `cleanUrls: false`를 사용한다. `dist/`에 없는 내부 경로는 실제 404로 남으며 SPA 홈 fallback이 없다. `.vercel.app` 호스트에 `X-Robots-Tag: noindex, nofollow`를 적용하고 기존 Vercel 인증 보호를 유지한다. 커스텀 운영 도메인에 noindex를 넣지 않는다. 향후 커스텀 스테이징 도메인을 추가하면 별도 색인 제외 조건을 검토해야 한다.

실제 preview는 로컬에서 생성·검사한 공개 패키지만 업로드했다. 내부 build scripts를 업로드하지 않으므로 preview용 설정의 buildCommand·installCommand는 빈 문자열이고 outputDirectory는 동일한 dist다. 운영용 소스 빌드 설정을 바꾸거나 프로젝트 설정을 업데이트하지 않았다. 소스 생성기의 Vercel 빌드 머신 실행은 이번 preview와 별도 검증 범위다.
