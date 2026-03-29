<p align="right">
  <a href="./README.md">English</a> | <strong>한국어</strong>
</p>

<h1 align="center">
  <code>tars</code>
</h1>

<p align="center">
  <a href="https://github.com/steadymoka/tars/releases"><img src="https://img.shields.io/badge/version-0.3.0-818cf8?style=flat-square" alt="version" /></a>
  <a href="https://github.com/steadymoka/tars/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-38bdf8?style=flat-square" alt="license" /></a>
  <img src="https://img.shields.io/badge/platform-Claude_Code-6366f1?style=flat-square" alt="platform" />
</p>

<p align="center">
  Claude Code용 자율 에이전트 운영 플러그인.<br/>
  <code>.tars/</code> 프로토콜을 통해 에이전트가 자율 운영하고, 스스로 프로토콜을 진화시킵니다.
</p>

## 설치

```
/plugin marketplace add steadymoka/tars
/plugin install tars@steadymoka-tars
```

## 빠른 시작

```
/tars:init                       # .tars/ 생성, core 선택, 실행 방식 선택
/tars:heartbeat                  # 자율 운영 1 사이클
/loop 10m /tars:heartbeat        # 10분마다 자동 반복
```

### 자율 운영 모드

완전한 자율 운영을 위해 `--dangerously-skip-permissions` 플래그로 Claude Code를 실행합니다:

```bash
claude --dangerously-skip-permissions
```

`/tars:init`이 설치하는 `guard.py` 훅이 프로젝트 디렉토리 밖 파일 수정과 **위험한 Bash 명령어**를 차단하므로, 자율 운영 중에도 프로젝트 범위 내에서 안전하게 동작합니다.

## Skills

| Skill | 설명 |
|-------|------|
| `/tars:init` | `.tars/` 초기화 — core 선택 (dev/design/...), 실행 방식 선택 (solo/team) |
| `/tars:heartbeat` | PROTOCOL.md를 읽고 1회 자율 사이클 실행 |
| `/tars:status` | 현재 상태 대시보드 — heartbeat 수, 백로그, 이상 징후 |
| `/tars:retro` | 즉시 회고 — 메트릭 산출, anomaly 탐지, 프로토콜 개선 제안 |
| `/tars:evolve` | 프로토콜 진화 분석 — 패치 효과 비교, lateral thinking 옵션 |
| `/tars:upgrade` | 기존 .tars/ 프로젝트를 최신 플러그인 버전으로 업그레이드 |
| `/tars:team` | 기존 solo 프로젝트에 팀 에이전트 구성 추가 |

## Core 시스템

**core**는 에이전트의 운영 방식을 정의합니다 — 프로토콜, 미션 템플릿, 완료 기준. tars의 확장 단위입니다.

### 기본 제공 Core

| Core | 설명 |
|------|------|
| `dev` | 빌드 검증, 코드 패트롤, 테스트 전략. 3레벨 DoD (빌드 → 기능검증 → 통합검증) |
| `design` | 디자인 이터레이션, 산출물 관리, 피드백 루프. specs/wireframes/research 산출물 구조 |

### 커뮤니티 Core

커뮤니티 core 추가는 디렉토리 복사만으로 가능합니다:

```
cores/
├── dev/           ← 기본 제공
├── design/        ← 기본 제공
├── research/      ← 커뮤니티 core를 여기에 복사
│   ├── core.json
│   ├── PROTOCOL.md
│   └── MISSION.md
└── shared/        ← 예약 (공통 템플릿)
```

core 디렉토리에는 3개 파일이 필요합니다:
- `core.json` — 메타데이터 (name, label, description, placeholders)
- `PROTOCOL.md` — heartbeat 사이클과 운영 규칙
- `MISSION.md` — 미션 템플릿 (DoD, Proactive Work 포함)

## 실행 방식

### Solo (기본)

하나의 에이전트, 하나의 core. 선택한 core의 프로토콜에 따라 자율 운영합니다.

```
/tars:init → core 선택 → solo
```

### Team

orchestrator가 여러 전문 에이전트를 조율합니다. 각 에이전트는 서로 다른 core로 동작합니다.

```
/tars:init → core 복수 선택 → team
```

Team 모드가 생성하는 파일:
- `.claude/agents/orchestrator.md` — 태스크 분배 조율자
- `.claude/agents/{core}-agent.md` — core별 전문 에이전트
- `.tars/_workspace/` — 에이전트 간 산출물 교환 공간

기존 solo 프로젝트도 나중에 team으로 전환할 수 있습니다:

```
/tars:team    # 기존 solo 프로젝트에 팀 에이전트 추가
```

## 작동 방식

```
Heartbeat Cycle (매 사이클):
  상태 확인 (캐시 없이 Read) → COMMS 처리 → CLARIFY → BACKLOG 작업 → LOG 기록 → RETRO 체크

Self-Evolution (RETRO에서 발견한 개선):
  Stagnation Detection → Oscillation Detection → Regression Detection
  → Wonder Gap Analysis → Protocol Patch 적용/제안
```

### .tars/ 구조

```
.tars/
├── COMMS.md         # Human <> Agent 소통
├── BACKLOG.md       # 작업 목록 (P0~P3)
├── PROGRESS.md      # 현재 heartbeat, 작업 상태
├── MILESTONES.md    # 중기 목표 체크포인트
├── protocol/
│   ├── MISSION.md   # 미션 정의, DoD, Proactive Work
│   ├── PROTOCOL.md  # 자율 운영 프로토콜 (self-evolution 대상)
│   └── EVOLUTION.md # 프로토콜 변경 이력
├── logs/
│   ├── LOG.md       # 작업 이력
│   ├── RETRO.md     # 회고 기록
│   ├── archive/
│   └── backlog-archive/
├── _workspace/      # Team 모드: 에이전트 간 산출물 교환
└── output/          # Design core: specs, wireframes, research
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
- **Regression**: 프로토콜 패치 후 메트릭 악화
- **Wonder**: 프로세스 가정에 대한 소크라테스식 질문

### Safety Rails

- DoD 레벨 하향 금지
- Proactive Work 제거 금지
- RETRO 주기 연장 금지
- 위 3가지는 human 명시 승인 없이 변경 불가

## Guard Hook

`guard.py` 훅이 자율 운영을 보호합니다:

- **파일 쓰기**: 프로젝트 밖 Write/Edit/NotebookEdit 차단
- **Bash 명령어**: 위험 명령어(`rm`, `mv`, `cp`, `dd` 등)가 프로젝트 밖을 대상으로 할 때 차단
- **Destructive git**: `git reset --hard`, `git push --force`, `git clean -fd`, `git checkout -- .` 차단
- **리다이렉트**: `>`, `>>`, `tee`가 프로젝트 밖 절대경로로 쓸 때 차단
- **sudo**: sudo를 벗겨내고 실제 명령어를 감지

## 라이선스

MIT
