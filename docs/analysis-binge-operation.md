# @binge 운영 분석 리포트

> 분석 대상: `.tars/` HB#1 ~ HB#162 (2026-03-22 ~ 2026-03-24)
> tars v0.2.2, dev mode

---

## 요약

162 heartbeat 동안 에이전트는 M1~M8 마일스톤을 완료하고 M10/M16/M17/M9 구현까지 마쳤으나,
**마일스톤 승인 대기로 인한 idle 고착**이 반복되고 있다.
COMMS.md 캐시 문제로 사람의 메시지를 놓치는 케이스가 발생하며,
Proactive Work가 "문제 찾기"에 한정되어 안정된 코드베이스에서 할 일이 사라지는 구조적 한계가 있다.

---

## 1. COMMS.md 캐시 — 사람의 메시지를 놓침

### 현상

`/loop`으로 heartbeat를 반복 실행할 때, 사람이 COMMS.md의 `From Human`에 메시지를 썼는데
에이전트가 다음 heartbeat에서 이를 읽지 못하는 케이스 발생.

### 원인

같은 세션에서 heartbeat가 반복되면 context가 누적되고, context compression 시
이전에 Read한 COMMS.md 내용이 압축된 context에 남는다.
다음 heartbeat에서 프로토콜이 "COMMS.md 확인"이라고 지시하지만,
에이전트가 **이미 읽은 내용을 신뢰하고 Read 도구를 다시 호출하지 않을 수 있다.**

```
HB#N:   Read(COMMS.md) → "From Human: (비어 있음)"
         ↓ context에 결과 캐시
사람:    COMMS.md에 메시지 작성
         ↓
HB#N+1: 프로토콜 "COMMS.md 확인" → 에이전트가 캐시된 "비어 있음"을 신뢰 → 메시지 놓침
```

COMMS는 사람 → 에이전트의 **유일한 소통 채널**이므로, 이 문제는 치명적이다.

### 제안

프로토콜의 상태 확인 단계를 수정:

```diff
### 1. 상태 확인
-1. PROGRESS.md 읽기 → 현재 heartbeat 수, 현재 작업 확인
-2. COMMS.md 확인:
+1. **Read 도구로** PROGRESS.md 읽기 → 현재 heartbeat 수, 현재 작업 확인
+2. **Read 도구로** COMMS.md 읽기 (이전 context의 캐시를 신뢰하지 않는다):
```

"확인"이 아니라 **"Read 도구로 읽기"**를 명시해서, 에이전트가 반드시 파일을 다시 읽도록 강제.
BACKLOG.md, MILESTONES.md도 동일하게 적용.

---

## 2. COMMS에 CLARIFY 섹션 추가 — 입력 품질 정제

### 문제

COMMS `From Human`에 들어오는 메시지가 모호할 때, 에이전트가 자의적으로 해석하고 바로 구현한다.
결과물이 의도와 다르면 뒤집히고, 이를 반복하면 디자인 방향이 3번 바뀌는 식의 낭비가 발생한다.
(EVOLUTION #6, #7이 이 문제를 proposed로 올렸으나 미해결)

**Garbage in, garbage out** — 프로토콜이 아무리 정교해도 입력이 모호하면 결과도 흔들린다.

### 해결: 사람이 넣는 위치로 처리 방식을 결정

COMMS.md에 `From Human (CLARIFY)` 섹션을 추가.
사람이 **어디에 쓰느냐**로 에이전트의 처리 방식이 달라진다:

```markdown
### From Human
(명확한 지시 — 즉시 실행)

### From Human (CLARIFY)
(아이디어/방향/모호한 요청 — 에이전트가 정제 후 실행)
```

### 프로토콜 흐름

```
From Human          → 즉시 실행 (기존과 동일)
From Human (CLARIFY) → 구조화(현재 상태 / 해석 / 구현 계획)
                     → From Agent에 [CLARIFY] 태그로 게시
                     → 1 HB 무응답 시 해석대로 진행
                     → 수정 오면 반영 후 진행
```

### 기대 효과

- 사람은 쓰는 내용을 바꿀 필요 없음. 위치만 선택
- 에이전트가 자의적 해석으로 구현 → 뒤집힘 패턴 방지
- EVOLUTION #6(UX 변경 전 확인), #7(브레인스토밍 규칙)이 자연스럽게 해결됨

---

## 3. PROGRESS.md — 세션 노트 방치와 필드 오염

### 현재 상태

```
Heartbeat: 162
Current Task: 없음
Phase: Building          ← 2번 중복 기재 (다른 값)
Proactive Step: Health Audit  ← 2번 중복 기재 (다른 값)
```

아래에 72줄의 세션 노트가 있으나, HB#80 이후 82 heartbeat 동안 갱신되지 않았다.

### 문제 진단

| 문제 | 설명 |
|------|------|
| **필드 중복** | Phase/Mode/Proactive Step이 2벌 존재. 첫 번째는 "Integration Check", 두 번째는 "Health Audit" — 어느 것이 맞는지 불분명. 템플릿에는 1벌만 있으므로 corruption |
| **세션 노트 방치** | HB#80 이후 82 heartbeat 동안 갱신되지 않음 |
| **Proactive Step 미갱신** | 실제로는 Gap Analysis까지 진행했지만 필드가 갱신되지 않음 |

### PROGRESS.md의 역할

PROTOCOL.md Heartbeat Cycle의 1단계가 `PROGRESS.md 읽기`이다.
매 heartbeat의 시작점이며, Proactive Step 필드(EVOLUTION #5에서 추가)는 이 파일에만 존재하는 고유 정보.
**제거하면 프로토콜의 시작 흐름을 바꿔야 하므로 제거는 부적절.**

### 제안: 축소 + 정비

- 세션 노트 제거. heartbeat마다 자동 갱신되는 필드로 한정
- 중복 필드 정리 규칙 추가 (또는 init 스킬의 템플릿 버그 수정)

```markdown
# Progress

**Heartbeat**: 162
**Current Task**: 없음
**Phase**: Building
**Mode**: dev
**Proactive Step**: Gap Analysis
**Idle Streak**: 2
```

---

## 2. Idle 고착 — Proactive Work가 "문제 찾기"에 한정됨

### idle 발생 이력

| 구간 | idle HB 수 | 원인 | 탈출 |
|------|-----------|------|------|
| HB#125~133 | 11 | BACKLOG 0, 마일스톤 승인 대기 | CronDelete |
| HB#141~143 | 3 | 동일 | CronDelete (3-idle 규칙 작동) |
| HB#161~162 | 2+ | 동일 | 진행 중 |

### 근본 원인

```
BACKLOG 소진 → Proactive Work 5단계 완료 → 문제 없음 → idle
                                                         ↑
                                          lint 0, build ✅, test ✅
                                          찾을 문제가 없다
```

idle 3회 자동 loop 중단 규칙은 HB#143에서 작동했으므로 **감지 자체는 정상**.
문제는 중단 전까지 "문제 없음" Proactive Work를 반복 실행하며 idle HB를 쌓는 것.

### Proactive Work의 구조적 한계

현재 5단계(Health Audit → User Scenario → Integration Check → Code Patrol → Gap Analysis)는
모두 **"문제를 찾는"** 관찰 활동이다. 이미 안정된 코드베이스에서는 매번 "이슈 없음"으로 끝난다.

**"가치를 만드는"** 작업이 빠져 있다:
- 테스트 커버리지 확대
- 리팩터링 (중복 제거, 추상화 개선)
- 성능 최적화 (번들 사이즈, 쿼리)
- 기술 부채 해소 (TODO/FIXME)

### 제안

Proactive Work에 6단계 **"Improvement"** 추가:
- 관찰(1~5단계)에서 문제가 없을 때, 기존 코드의 품질을 능동적으로 높이는 작업
- 단, Safety Rail 필요: 사람이 모르는 대규모 리팩터링은 금지. BACKLOG 등록 후 실행

---

## 3. EVOLUTION.md — 에스컬레이션은 작동하나, re-raise가 안 됨

### 현재 상태

8개 항목 중:
- **해결됨 2개**: #1(upgrade), #3(upgrade)
- **에스컬레이션됨 1개**: #2 → #5(structural-patch, applied). 단 #2의 status가 "proposed"로 미갱신
- **미해결 4개**: #4, #6, #7, #8

| # | HB | 내용 | 실제 상태 |
|---|-----|------|----------|
| 2 | 10 | Proactive Work 추적 방식 | **해결됨** (#5로 승격·적용). status만 미갱신 |
| 4 | 20 | Milestone 자동 티켓 생성 | proposed |
| 6 | 30 | UX 변경 전 브레인스토밍 필수 | proposed |
| 7 | 40 | 브레인스토밍 COMMS 규칙 | proposed |
| 8 | 50 | BACKLOG 소진 후 전략 | proposed |

### "경로가 없다"는 틀렸다

프로토콜에 `3개 RETRO에서 같은 질문 반복 → structural-patch 승격`이 명시되어 있고,
#2→#5가 실제로 이 경로를 탔다.

나머지 4개가 에스컬레이션되지 않은 이유: 프로토콜의 조건은 "같은 질문이 3개 RETRO에서 **독립적으로 다시 제기**"되는 것이지, "proposed로 남아있으면 자동 승격"이 아니다. 다시 떠올라야 승격되는 구조.

### 실제 문제

Wonder에서 한 번 나온 질문이 다시 제기되지 않으면 영원히 proposed로 남는다.
"이 질문이 아직 유효한가?" 를 확인하는 메커니즘이 없다.

### 제안

- proposed 항목에 "마지막 언급 HB" 필드 추가
- N HB 이상 re-raise 없으면 자동으로 `resolved(stale)` 처리
- 또는 RETRO에서 이전 proposed 항목을 명시적으로 리뷰하는 스텝 추가

---

## 4. Milestone 승인 대기 — 프로토콜 vs 현실의 시간 스케일 차이

### 현상

- M17: COMMS에 `[MILESTONE]` 전송 → 5 HB(~50분) 무응답 → auto-delete → 10 HB 재전송 금지
- M10, M9: 118 HB(~20시간) 동안 active 상태

### 프로토콜의 설계 의도

auto-delete 후 "LOG에 기록하고 계속 작업한다"가 정의된 행동이므로,
**"다음 행동이 없다"는 이전 분석은 부정확**. 계속 작업하되, 작업이 없으면 idle이 되는 것.

### 실제 문제

프로토콜의 시간 단위(heartbeat, ~10분)와 사람의 응답 시간(시간~일)이 맞지 않는다.
5 HB(~50분) 타임아웃은 사람이 응답하기엔 너무 짧고,
타임아웃을 15 HB로 늘려도 사람이 자리에 없으면 같은 결과.

### Stagnation 감지 갭

RETRO anomaly에 "Active milestone, 20+ HB no progress"가 정의되어 있지만,
M10/M9는 **구현이 완료**된 상태이므로 "no progress"에 해당하지 않는다.
"구현 완료 + 승인 대기"라는 상태에 대한 anomaly가 정의되어 있지 않다.

### 제안

- "구현 완료 + 승인 대기 N HB" 상태를 별도 anomaly로 정의
- 감지 시: COMMS에 리마인더가 아니라, **에이전트가 자체적으로 "승인 없이 done 처리" 또는 "drop 제안"**을 판단할 수 있는 규칙 추가
- 승인 필요 마일스톤과 자체 완료 가능 마일스톤을 구분하는 것도 고려

---

## 5. Phase 전환 — 조건이 불명확하나 실해는 없었음

Phase Directives(Building/Stabilizing/Shipping)가 MISSION.md에 정의되어 있으나,
**전환 조건과 전환 주체**가 명시되어 있지 않다.

다만 162 HB 동안 사람이 계속 새 마일스톤(M10, M16, M17)을 요청했으므로
Building이 맞았고, 전환하지 않은 것이 오류는 아니다.
RETRO #5에서 Stabilizing 전환을 제안했지만, 이후 새 작업이 들어와서 Building으로 유지된 것이 실상.

### 제안

- 심각도 낮음. Phase 전환 조건을 PROTOCOL.md에 간단히 명시하는 정도
- 예: "BACKLOG 0 + 새 마일스톤 요청 없음 + Proactive Work 이슈 0 → Stabilizing 전환 제안"

---

## 6. 기타 발견

### BACKLOG 완료 항목 적체

Completed 섹션에 40개 이상 쌓여있으나, 실질적 영향은 파일이 길어지는 정도.
backlog-archive 메커니즘은 존재(phase-1~3). 하우스키핑 수준.

### RETRO 액션 아이템 미추적

매 RETRO에 `### 액션` 체크박스가 생성되지만, 다음 RETRO에서 확인하는 절차가 없다.
프로토콜 갭이 맞으나 실질적 영향도는 낮음.

### PROGRESS.md 필드 중복 (corruption)

Phase/Mode/Proactive Step이 2벌 기재. 템플릿에는 1벌만 있으므로 초기화 또는 갱신 시 발생한 버그.

### 디자인 방향 뒤집힘 (M17)

> RETRO #16: "Scene Card 이미지 → 제거 → 사이드바 강화 등 디자인 방향이 3번 바뀜"

프로토콜 문제라기보다 사람-에이전트 소통 문제. 게이트를 추가해도 사람이 "일단 해봐"라면 같은 결과.
EVOLUTION #6에 이미 이 질문이 proposed로 있다.

### HB#52~76 세션 갭

LOG에 24 HB 분량 누락. 일회성 세션 중단으로 추정. 세션 재개 마커를 추가하면 추적 가능.

### CLAUDE.md가 거의 비어있음

`@binge/CLAUDE.md`에 프로젝트명만 있다.
에이전트가 162 HB 동안 쌓은 프로젝트 지식이 CLAUDE.md에 반영되지 않고 있다.

---

## 개선 우선순위

| 순위 | 항목 | 영향도 | 변경 대상 |
|------|------|--------|----------|
| 1 | **COMMS.md 캐시 방지 — "Read 도구로 읽기" 명시** | 치명 | PROTOCOL.md 상태 확인 |
| 2 | **COMMS에 CLARIFY 섹션 추가 — 입력 품질 정제** | 높음 | COMMS.md 템플릿 + PROTOCOL.md |
| 3 | **Proactive Work에 "Improvement" 단계 추가** | 높음 | MISSION.md 템플릿 |
| 4 | **"구현 완료 + 승인 대기" anomaly 정의** | 높음 | PROTOCOL.md RETRO 섹션 |
| 5 | **PROGRESS.md 축소** (세션 노트 제거, 필드 정비) | 중간 | 템플릿 + PROTOCOL.md |
| 6 | **EVOLUTION proposed 항목 stale 처리 규칙** | 중간 | PROTOCOL.md Evolution 섹션 |
| 7 | **Phase 전환 조건 명시** | 낮음 | PROTOCOL.md |
| 8 | **BACKLOG 완료 항목 아카이브 규칙** | 낮음 | PROTOCOL.md |
