<p align="right">
  <a href="./README.md">English</a> | <strong>한국어</strong>
</p>

# snowloop

Claude Code용 자율 에이전트 운영 플러그인.

`.snowloop/` 프로토콜을 통해 에이전트가 자율 운영하고, 스스로 프로토콜을 진화시킵니다.

## 설치

```
/plugin marketplace add steadymoka/snowloop
/plugin install snowloop@steadymoka-snowloop
```

## 빠른 시작

```
/snowloop:init                       # .snowloop/ 생성, 모드 선택 (dev / design)
/snowloop:heartbeat                  # 자율 운영 1 사이클
/loop 10m /snowloop:heartbeat        # 10분마다 자동 반복
```

### 자율 운영 모드

완전한 자율 운영을 위해 `--dangerously-skip-permissions` 플래그로 Claude Code를 실행합니다:

```bash
claude --dangerously-skip-permissions
```

`/snowloop:init`이 설치하는 `guard.py` 훅이 프로젝트 디렉토리 밖 파일 수정을 차단하므로, 자율 운영 중에도 프로젝트 범위 내에서 안전하게 동작합니다.

## Skills

| Skill | 설명 |
|-------|------|
| `/snowloop:init` | 프로젝트에 `.snowloop/` 초기화. dev(개발) 또는 design(기획) 모드 선택 |
| `/snowloop:heartbeat` | PROTOCOL.md를 읽고 1회 자율 사이클 실행 |
| `/snowloop:status` | 현재 상태 대시보드 — heartbeat 수, 백로그, 이상 징후 |
| `/snowloop:retro` | 즉시 회고 — 메트릭 산출, anomaly 탐지, 프로토콜 개선 제안 |
| `/snowloop:evolve` | 프로토콜 진화 분석 — 패치 효과 비교, lateral thinking 옵션 |
| `/snowloop:upgrade` | 기존 .snowloop/ 프로젝트를 최신 플러그인 버전으로 업그레이드 |

## 모드

### Dev 모드

빌드 검증, 테스트 전략, 코드 패트롤 중심.

- DoD 3레벨 (L1 빌드 → L2 기능검증 → L3 통합검증)
- Proactive Work: Health Audit → User Scenario → Integration Check → Code Patrol → Gap Analysis
- Phase Directives: Building → Stabilizing → Shipping

### Design 모드

디자인 이터레이션, 산출물 관리, 피드백 루프 중심.

- 산출물 구조: `specs/`, `wireframes/`, `research/`
- 날짜 프리픽스 네이밍: `YYYY-MM-DD-<name>.<ext>`
- Proactive Work: 기존 디자인 개선 → 크로스폴리네이션 → 경쟁 분석 → 일관성 감사 → 구현 준비
- Phase Directives: Exploring → Converging → Implementing

## 작동 방식

```
Heartbeat Cycle (매 사이클):
  상태 확인 → COMMS 처리 → BACKLOG 작업 → LOG 기록 → RETRO 체크

Self-Evolution (RETRO에서 발견한 개선):
  Stagnation Detection → Oscillation Detection → Regression Detection
  → Wonder Gap Analysis → Protocol Patch 적용/제안
```

### .snowloop/ 구조

```
.snowloop/
├── COMMS.md         # Human ↔ Agent 소통 (From Human / From Agent)
├── BACKLOG.md       # 작업 목록 (P0~P3)
├── PROGRESS.md      # 현재 heartbeat, 작업 상태
├── protocol/        # 에이전트 설정 (자주 보지 않음)
│   ├── MISSION.md   # 미션 정의, DoD, Proactive Work
│   ├── PROTOCOL.md  # 자율 운영 프로토콜 (self-evolution 대상)
│   └── EVOLUTION.md # 프로토콜 변경 이력
├── logs/            # 기록
│   ├── LOG.md       # 작업 이력
│   ├── RETRO.md     # 회고 기록
│   ├── archive/     # 오래된 LOG 아카이브
│   └── backlog-archive/
│       └── INDEX.md
└── output/          # 기획 모드 산출물
    ├── specs/
    ├── wireframes/
    ├── research/
    └── INDEX.md
```

## Self-Evolution

RETRO(10 heartbeat마다 자동)에서 프로세스 개선을 발견하면 PROTOCOL.md를 자동 수정합니다.

| Type | 설명 | 적용 방식 |
|------|------|-----------|
| Parameter Patch | 임계값/횟수 조정 | PROTOCOL.md 직접 수정 |
| Structural Patch | 단계 추가/제거 | COMMS에 제안 → 자동승인 |
| Question | 프로세스 가정 질문 | 3회 반복 시 patch로 승격 |
| Revert | 메트릭 악화 시 되돌림 | 자동 감지 + 되돌림 |

### Anomaly Detection

- **Stagnation**: 같은 작업 3+ heartbeat 정체, 또는 idle 3연속
- **Oscillation**: 같은 패치의 적용→revert 반복 (A→B→A 패턴)
- **Regression**: 프로토콜 패치 후 메트릭 악화 (기존 문제와 구분)
- **Wonder**: 프로세스 가정에 대한 소크라테스식 질문 ("아직 검증 안 한 것은?")

### Safety Rails

자가 품질 기준 완화를 방지합니다:

- DoD 레벨 하향 금지
- Proactive Work 제거 금지
- RETRO 주기 연장 금지
- 위 3가지는 human 명시 승인 없이 변경 불가

## 라이선스

MIT
