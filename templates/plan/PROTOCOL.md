<!-- EN: Plan mode autonomous operation protocol. Defines heartbeat cycle with output management, retrospective process, design iteration guide, and self-evolution rules. -->
# Protocol: Plan Mode

> 이 파일은 기획 모드 자율 운영 프로토콜입니다. Heartbeat마다 이 문서를 읽고 정확히 따릅니다.
> **Self-Evolution 대상**: RETRO에서 발견한 개선은 이 문서를 직접 수정합니다.

---

## Heartbeat Cycle

매 heartbeat에서 다음을 순서대로 실행합니다:

### 1. 상태 확인
1. PROGRESS.md 읽기 → 현재 heartbeat 수, 현재 작업 확인
2. COMMS.md의 Pending 섹션 확인 → `[→agent]` 메시지가 있으면 최우선 처리
3. BACKLOG.md 읽기 → 다음 작업 결정

### 2. 작업 실행
- **COMMS 메시지 있음**: 메시지 지시에 따라 행동. 완료 후 Processed로 이동
- **BACKLOG 티켓 있음**: 최고 우선순위 티켓 선택, 작업 실행
  - PROGRESS.md에 현재 작업 갱신
  - DoD 기준 충족 확인 (MISSION.md 참조)
  - 완료 시 BACKLOG에서 `[x]` 체크
- **BACKLOG 비어 있음**: Proactive Work 실행 (MISSION.md 참조)
  - 발견한 이슈/아이디어는 BACKLOG에 새 티켓으로 등록

### 3. 산출물 관리
- 새 산출물 생성 시 → `.snowloop/output/drafts/`에 먼저 작성
- 리뷰 완료된 산출물 → 카테고리 폴더로 이동
- INDEX.md 갱신 (새 항목 추가 또는 Status 변경)

### 4. 기록
- LOG.md에 heartbeat 기록 추가:
  ```
  ### HB#{n} — {YYYY-MM-DD HH:MM}
  - **작업**: {작업 요약}
  - **산출물**: {생성/수정된 산출물 경로} (해당 시)
  - **결과**: {성공/실패/진행중}
  - **다음**: {다음 heartbeat 예정 작업}
  ```
- PROGRESS.md의 heartbeat 카운트 +1

### 5. RETRO 체크
- heartbeat 카운트가 10의 배수이면 → RETRO 실행 (아래 "회고 프로토콜" 참조)

### 6. COMMS 정리
- Processed 섹션에서 5개 초과 항목 삭제 (오래된 것부터)

### 7. LOG 아카이브
- LOG.md 항목이 50개 초과 시 → `.snowloop/logs/log-{date}.md`로 이동

---

## 회고 프로토콜 (10 heartbeat마다)

### 메트릭 산출
최근 10개 heartbeat의 LOG를 분석:
- `productive_count`: 산출물 생성/수정한 heartbeat 수
- `idle_count`: Proactive Work만 한 heartbeat 수
- `blocked_count`: 피드백 대기/차단된 heartbeat 수
- `productive_ratio`: productive_count / 10
- `output_count`: 기간 내 생성된 산출물 수

### Stagnation Detection
- **Spinning**: 같은 산출물을 3 heartbeat 이상 수정 → 완성 기준 재점검
- **Idle streak**: idle 3연속 → COMMS에 `[→human]` 방향 전환 제안
- **Declining productivity**: 3개 연속 RETRO에서 productive_ratio 하락 → 전략 재검토 제안

### Oscillation Detection
- EVOLUTION.md에서 같은 영역의 patch→revert 2회 반복 → `[LATERAL-THINK]` 제안

### Regression Detection
- 직전 patch 적용 후 메트릭 악화 → patch 되돌리고 EVOLUTION.md에 REVERTED 기록

### Wonder (Gap Analysis)
- "기획 프로세스에서 아직 검증하지 않은 가정은 무엇인가?"
- 발견된 gap은 EVOLUTION.md에 `question` 타입으로 기록
- 3개 RETRO에서 같은 질문 반복 → structural-patch 대상으로 승격

### RETRO 기록
RETRO.md에 추가:
```
## RETRO #{n} — HB#{start}~#{end} — {date}

### 메트릭
| 항목 | 값 |
|------|-----|
| Productive | {n}/10 |
| Idle | {n}/10 |
| Blocked | {n}/10 |
| Ratio | {n}% |
| Tickets 완료 | {n}개 |
| Tickets 추가 | {n}개 |
| Outputs | {n}개 |

### Anomaly
- {감지된 이상 징후 또는 "없음"}

### 잘 된 점
- ...

### 개선할 점
- ...

### 프로세스 질문 (Wonder)
- ...

### 액션
- [ ] ...
```

---

## 디자인 이터레이션 가이드

### 이터레이션 사이클
1. **초안 생성**: drafts/에 빠르게 작성
2. **자가 검토**: MISSION.md의 DoD 기준으로 점검
3. **피드백 요청**: COMMS에 `[→human]` 리뷰 요청
4. **반영**: 피드백 기반 수정
5. **확정**: 카테고리 폴더로 이동, INDEX 갱신

### 크로스폴리네이션
- 산출물 간 연결: wireframe → spec 참조 확인
- 용어 일관성: 같은 개념에 다른 이름 사용 여부 점검
- 패턴 일관성: 유사 화면/기능의 UI 패턴 통일

### 인덱스 유지보수
- 매 heartbeat에서 INDEX.md의 정합성 확인
- 존재하지 않는 파일 참조 제거
- Status 갱신 누락 점검

---

## 서브에이전트 디스패치 계약

서브에이전트를 사용할 때:
- 명확한 태스크 정의: "무엇을 하고, 완료 조건은 무엇인지" 명시
- 결과 검증: 서브에이전트 결과를 반드시 검증 후 반영
- LOG 기록: 서브에이전트 사용 시 LOG에 "Sub-agent: {목적}" 기록

---

## Protocol Evolution (자가 발전)

RETRO에서 시스템적 개선(일회성 수정이 아닌 반복 패턴)을 발견하면:

1. **분류**: parameter-patch | structural-patch | question
2. **Parameter patch** (임계값 변경, 횟수 조정 등):
   - 이 PROTOCOL.md에 직접 적용
   - EVOLUTION.md에 기록 (Status: applied)
   - LOG에 "Protocol-patch: {변경 요약}" 기록
3. **Structural patch** (단계 추가/제거, 새 규칙):
   - COMMS에 `[→human] [PROTOCOL-PATCH]` 태그로 제안
   - 자동승인: 1 heartbeat 대기 후 인간 반응 없으면 적용
   - 적용 시 EVOLUTION.md 기록
4. **Question** (프로세스 가정에 대한 질문):
   - EVOLUTION.md에 기록 (Status: proposed)
   - 3회 반복 시 structural-patch로 승격
5. **Revert**: 패치 후 다음 RETRO에서 메트릭 악화 시 되돌림
   - EVOLUTION.md에 원본 패치를 REVERTED로 갱신
   - 되돌림 사유를 Reason에 기록
6. **Oscillation 탈출**: 같은 패치의 적용→revert가 2회 반복되면
   - 해당 영역은 parameter-patch 불가로 판정
   - COMMS에 `[→human] [LATERAL-THINK]` 태그로 구조적 재설계 제안

### Safety Rails
- DoD 기준 하향 금지
- Proactive Work 단계 제거 금지
- RETRO 주기 연장 금지
- 위 3가지는 human 명시 승인 없이 변경 불가
