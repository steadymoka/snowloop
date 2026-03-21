<!-- EN: Dev mode mission template. Defines 3-level DoD (build/functional/integration), testing strategy, proactive work tiers, and phase directives. -->
# Mission: {PROJECT_NAME}

> {MISSION_DESCRIPTION}

---

## Definition of Done (DoD)

### L1: 빌드 통과
- `{BUILD_CMD}` 성공
- 새 에러/경고 없음

### L2: 기능 검증
- `{TEST_CMD}` 전체 통과
- 변경 범위 내 엣지 케이스 확인
- `{LINT_CMD}` 통과

### L3: 통합 검증
- 관련 모듈 간 통합 동작 확인
- 성능 회귀 없음
- 문서 갱신 (필요 시)

---

## Testing Strategy

> 프로젝트에 맞게 커스터마이징하세요.

- **단위 테스트**: 비즈니스 로직 중심
- **통합 테스트**: 외부 의존성 경계
- **E2E 테스트**: 핵심 사용자 시나리오

---

## Proactive Work (백로그가 비었을 때)

> 우선순위 순서대로 실행. 한 단계에서 발견한 이슈는 BACKLOG에 티켓으로 등록.

1. **Health Audit**: 빌드/테스트/린트 실행, 미해결 경고 정리
2. **User Scenario Walkthrough**: 핵심 사용자 플로우를 시뮬레이션하며 갭 발견
3. **Integration Check**: 모듈 간 계약(인터페이스, 타입, API) 정합성 확인
4. **Code Patrol**: 변경 이력 기반 코드 품질 점검 (PROTOCOL.md의 Code Patrol 절차 따름)
5. **Gap Analysis**: MISSION 대비 미구현/미검증 영역 식별

---

## Phase Directives

### Building (기능 구현 중)
- 티켓 단위로 작업, DoD L1 충족 후 다음 진행
- 대규모 변경 시 중간 커밋 권장

### Stabilizing (안정화)
- DoD L2/L3 집중
- 새 기능보다 기존 기능의 견고함 우선
- Proactive Work 적극 실행

### Shipping (출시 준비)
- 파괴적 변경 금지
- 크리티컬 버그만 수정
- 문서/변경 로그 최종 점검

---

## Constraints

> 프로젝트에 맞게 커스터마이징하세요.

- 프로젝트 디렉토리 밖 파일 수정 금지
- 사용자 확인 없는 파괴적 변경 금지
- 보안 민감 정보 커밋 금지
