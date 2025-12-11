# 📜 프로젝트 기여 가이드 (Contribution Guide)

## 1. ⚙️ 개발 환경 및 기본 규칙

- **언어 및 프레임워크:** Python (Flask), TypeScript (React, Vite), Styled Components
- **패키지 관리:** `npm` (`package.json` 참조)
- **스타일 규칙:** 기존 코드의 스타일(띄어쓰기, 세미콜론 사용 등)을 최대한 따르며, 일관성을 유지합니다.

---

## 2. 🌳 Git 및 브랜치 관리 (GitFlow 기반)

본 프로젝트는 **GitFlow 전략**을 기반으로 합니다. 모든 기여는 명확한 브랜치 전략을 따라야 합니다.

### A. 메인 브랜치

- `develop`: 다음 출시 버전을 준비하는 통합 브랜치. 모든 개발 작업의 **병합(Merge) 목표** 브랜치 입니다.

### B. 기능 개발 브랜치 (Feature Branch)

모든 새로운 기능, 버그 수정, 개선 사항은 `develop`에서 분기된 별도의 브랜치에서 진행해야 합니다.

- **브랜치 명명 규칙: 커밋타입 + 이슈넘버 + 이슈이름**
    - **신규 기능 (Feature):** `feature/#이슈번호_[이슈이름]`
        - (e.g., `feature/#57-Change_Graph_Auxiliary_Line`)
    - **버그 수정 (fix):** `fix/#이슈번호_[간결한_설명]`
        - (e.g., `fix/#50_fix-type-error`)
    - **코드 개선 (Chore/Refactor):** `chore/#이슈번호_[이슈이름]`
        - (e.g., `chore/#53-백엔드_프론트엔드_데이터_전달_방식`)

---

## 3. 📝 커밋 메시지 규칙 (Conventional Commits)

커밋 메시지는 명확하게 작성하여 코드 변경 내역을 쉽게 추적할 수 있도록 합니다.

- **형식:** `커밋타입: 제목`
- **타입 (Type):** 다음 중 하나를 사용합니다.
    - `feature`: 새로운 기능 추가 (e.g., `feature: 1시간 단위로 가공된 API 데이터 연동`)
    - `fix`: 버그 수정 (e.g., `fix: 미세먼지 컨플릭트 해결)`
    - `refactor`: 코드 리팩토링, 기능 변경 없음 (e.g., `refactor: app.py 리팩토링`)
    - `chore`: 빌드 설정, 라이브러리 업데이트, 주석 삭제 등 (e.g., `chore: 불필요 파일 삭제`)
    - `style`: 코드 포맷팅, 세미콜론, 공백 등 (기능 변경 없음)

---

## 4. 🚀 기여 프로세스 (Pull Request, PR)

코드가 완성되면 `develop` 브랜치로 병합하기 위해  PR(Pull Request)을 생성해야 합니다.

1. **PR 목표:** **항상 기능을 개발한 브랜치 → `develop` 브랜치**로 PR을 생성합니다.
2. **PR 본문 작성:** 다음 항목을 포함하여 리뷰어가 쉽게 이해할 수 있도록 상세히 작성합니다.
    - **PR 제목:** 커밋 메시지 규칙(`feature: ...`)을 따릅니다.
    - **관련 이슈 번호:** (예: Closes #84)
    - **주요 변경 사항:** 무엇을, 왜 변경했는지 설명합니다.
    - **스크린샷:** UI 변경이 있는 경우, **Before & After 스크린샷**을 첨부합니다.
3. **코드 리뷰:** 리뷰어 2명의 승인(Approve)을 받은 후, `develop` 브랜치에 병합합니다.

---

## 5. ⚠️ 프론트엔드/백엔드 주의 사항

### A. 프론트엔드 (React/TS)

- **타입 정의 우선:** 새로운 데이터 필드(예: `air_pollution`)를 사용하기 전, `src/types/weather.ts` 파일을 먼저 업데이트하여 **TypeScript 오류를 방지**합니다.
- **스타일 분리:** **JSX 내부의 인라인 스타일** 사용을 지양하고, `WeatherPage.styles.ts` 파일에 `styled-components`를 정의하여 최대한 스타일을 분리합니다.

### B. 백엔드 (Python/Flask)

- **환경 변수:** API 키는 `.env` 파일을 통해 로드하고, 코드를 공개 저장소에 푸시하지 않도록 주의합니다.
- **Geocoding/API 호출:** 새로운 함수(`get_coordinates` 등)를 구현할 때, API 호출 실패에 대비하여 반드시 `try...except` 블록을 사용하고, `res.raise_for_status()`를 통해 **HTTP 오류를 처리**합니다.
- **데이터 필터링:** API에서 가져온 원본 데이터를 그대로 사용하지 않고, 반드시 `process_data` 함수를 거쳐 **프론트엔드에 필요한 필드만** 정제하여 반환합니다.