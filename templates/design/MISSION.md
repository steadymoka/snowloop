<!-- EN: Design mode mission template. Defines artifact-based DoD, output management structure, proactive work tiers, feedback system, and phase directives. -->
# Mission: {PROJECT_NAME}

> {MISSION_DESCRIPTION}

---

## Definition of Done (DoD)

### 산출물 기준
- 요구되는 아티팩트가 `.snowloop/output/` 하위에 존재
- 산출물이 INDEX.md에 등록됨
- Status가 `final`로 표기됨

### 품질 기준
- 핵심 사용자 시나리오가 산출물에 반영됨
- 기술적 실현 가능성이 검토됨
- 이해관계자 피드백이 반영됨 (해당 시)

---

## Output 관리

### 저장 구조
```
.snowloop/output/
├── specs/          # 스펙 문서, 기능 정의서, PRD
├── wireframes/     # 와이어프레임, 목업, UI 플로우
├── research/       # 경쟁 분석, 사용자 리서치, 기술 조사
├── drafts/         # 작성 중인 초안 (gitignore 대상)
└── INDEX.md        # 산출물 목록
```

### 네이밍 규칙
`YYYY-MM-DD-<descriptive-name>.<ext>`
예: `2026-03-21-login-flow-wireframe.md`

### 라이프사이클
1. `drafts/`에 초안 작성
2. 리뷰 완료 → 카테고리 폴더로 이동
3. INDEX.md에 등록 (Status: final)

---

## Proactive Work (백로그가 비었을 때)

1. **기존 디자인 개선**: 현재 산출물의 약점 분석, 대안 제시
2. **크로스폴리네이션**: 다른 산출물 간 일관성/연결성 점검
3. **경쟁 분석**: 유사 제품/서비스 리서치
4. **일관성 감사**: UI/UX 패턴, 용어, 톤 일관성 점검
5. **구현 준비**: 기획 산출물 → 개발 티켓 변환 준비

---

## Phase Directives

### Exploring (탐색)
- 넓게 조사, 다양한 대안 탐색
- 산출물은 drafts/에 자유롭게 생성
- 판단 유보, 양 우선

### Converging (수렴)
- 대안 비교 평가, 최적안 선택
- drafts/ → 카테고리 폴더로 승격
- 피드백 반영, 품질 다듬기

### Implementing (구현 전환)
- 확정된 기획을 개발 티켓으로 변환
- 기술 스펙 구체화
- 핸드오프 문서 준비

---

## 피드백 시스템

### 투표 패턴 (선택)
대안 비교 시 `votes.json` 활용 가능:
```json
{
  "topic": "로그인 플로우",
  "options": ["A: 소셜 로그인 우선", "B: 이메일 우선"],
  "votes": []
}
```
COMMS `From Agent`에 투표 요청 → 응답 반영

---

## Constraints

- 프로젝트 디렉토리 밖 파일 수정 금지
- 기획 결정의 근거를 산출물에 명시
- 사용자 확인 없는 방향 전환 금지
