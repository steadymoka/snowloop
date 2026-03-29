---
name: retro
description: "Run immediate retrospective outside the regular 10-heartbeat cycle. Analyzes LOG for metrics, detects stagnation/oscillation/regression patterns, generates Wonder questions, and records to RETRO.md and EVOLUTION.md."
allowed-tools: Read, Write, Edit, Glob
---

# /tars:retro — 즉시 회고

정규 10 heartbeat 주기 외에 즉시 회고를 실행합니다.

## 실행 절차

### 1. 데이터 수집

다음 파일을 읽습니다:
- `.tars/logs/LOG.md` — 전체 (또는 최근 10개 heartbeat)
- `.tars/BACKLOG.md` — 현재 백로그 상태
- `.tars/logs/RETRO.md` — 이전 RETRO 기록들 (패턴 분석용)
- `.tars/protocol/EVOLUTION.md` — 프로토콜 변경 이력
- `.tars/PROGRESS.md` — 현재 heartbeat 수
- `.tars/MILESTONES.md` — active/done Milestone 상태 및 생성일

### 2. 메트릭 산출

최근 10개 heartbeat (또는 마지막 RETRO 이후)의 LOG를 분석:

| 메트릭 | 설명 |
|--------|------|
| `productive_count` | 실제 작업 완료한 heartbeat 수 |
| `idle_count` | Proactive Work만 한 heartbeat 수 |
| `blocked_count` | 차단/실패한 heartbeat 수 |
| `productive_ratio` | productive_count / 전체 × 100% |
| `tickets_completed` | 기간 내 완료된 티켓 수 |
| `tickets_added` | 기간 내 추가된 티켓 수 |

### 3. Anomaly Detection

#### A. Stagnation Detection
- **Spinning**: 같은 티켓이 3+ heartbeat 동안 current task → "SPINNING 감지: {ticket}이 {n} heartbeat째 진행 중"
- **Idle streak**: idle 3연속 → "IDLE STREAK: 의미있는 작업이 없습니다. 방향 전환을 제안합니다."
- **Declining productivity**: 이전 RETRO 대비 productive_ratio 하락이 3회 연속 → "DECLINING: 생산성이 지속 하락 중"

#### B. Oscillation Detection
- EVOLUTION.md에서 같은 영역의 applied→reverted 패턴이 2회 이상 → "OSCILLATION: {영역}에서 patch↔revert 반복. parameter-patch로 해결 불가. structural-patch 필요."

#### C. Regression Detection
- 마지막 protocol patch 적용 이후 메트릭 비교
- 악화된 항목이 있으면: "REGRESSION: {patch}가 {메트릭}을 악화시켰습니다. Revert를 제안합니다."
- 핵심: 패치 전에도 안 좋았던 건 regression이 아님 — 패치 후 나빠진 것만 보고

#### D. Wonder (Gap Analysis)
- 메트릭 분석 후 스스로 질문:
  > "이 프로세스에서 아직 검증하지 않은 가정은 무엇인가?"
- 현재 heartbeat 주기, Proactive Work 순서, RETRO 빈도 등에 대한 질문 생성
- 이전 RETRO의 Wonder 질문과 비교 → 반복되는 질문 식별

#### E. Milestone Stagnation
- active Milestone이 20 HB 이상 변화 없으면 (생성 이후 `[MILESTONE]` COMMS 없고 Status 변경 없음):
  "MILESTONE STAGNATION: M{n} '{title}'이 {n} HB째 변화 없음. 방향 재검토 또는 drop을 제안합니다."
- status의 10 HB 조기 경고보다 상위 단계. retro에서 구조적으로 다루며, COMMS `From Agent`에 drop 또는 조건 재정의를 제안한다.

### 4. RETRO 기록

`logs/RETRO.md`의 **맨 위**에 추가 (최신이 위):

```markdown
## RETRO #{n} — HB#{start}~#{end} — {date}

### 메트릭
| 항목 | 값 |
|------|-----|
| Productive | {n}/{total} |
| Idle | {n}/{total} |
| Blocked | {n}/{total} |
| Ratio | {n}% |
| Tickets 완료 | {n}개 |
| Tickets 추가 | {n}개 |

### Anomaly
- {감지된 이상 징후 또는 "없음"}

### 잘 된 점
- ...

### 개선할 점
- ...

### 프로세스 질문 (Wonder)
- {gap analysis 결과}

### Milestone 진행
- {각 active/done Milestone의 상태와 경과 HB 또는 완료일}

### 액션
- [ ] {개선 액션들}
```

### 5. EVOLUTION.md 갱신

- Anomaly에서 프로토콜 개선이 필요한 경우 → `protocol/EVOLUTION.md`에 행 추가
- Wonder에서 반복되는 질문 → `question` 타입으로 기록
- Regression 감지 시 → revert 행 추가 + `protocol/PROTOCOL.md` 되돌림 제안

### 6. 프로토콜 패치 제안

Anomaly 또는 Wonder에서 프로토콜 변경이 필요하다고 판단되면:
- **Parameter patch**: `protocol/PROTOCOL.md`에 직접 적용 + `protocol/EVOLUTION.md` 기록
- **Structural patch**: COMMS `From Agent`에 `[PROTOCOL-PATCH]` 제안

### 7. 결과 출력

분석 결과를 사용자에게 컴팩트하게 출력합니다.

## 에러 핸들링

- LOG가 비어있거나 heartbeat가 0이면: "기록이 부족합니다. heartbeat를 먼저 실행하세요."
- `.tars/` 없으면: "tars이 초기화되지 않았습니다."
