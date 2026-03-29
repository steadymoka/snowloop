# tars

자율 에이전트 운영 플러그인 — `.tars/` 프로토콜을 통해 에이전트가 스스로 진화합니다.

## 사용 가능한 Skills

| Skill | 설명 |
|-------|------|
| `/tars:init` | 프로젝트에 `.tars/` 디렉토리를 초기화합니다. core 선택, solo/team 실행 방식 설정. |
| `/tars:heartbeat` | 한 사이클을 실행합니다 — COMMS 확인, BACKLOG 처리, PROGRESS 갱신, LOG 기록. |
| `/tars:status` | 현재 세션 상태를 요약합니다 (진행 중 태스크, heartbeat 수, 미처리 메시지). |
| `/tars:retro` | 회고를 즉시 실행합니다. 무엇이 잘 됐고, 무엇을 개선할지 기록합니다. |
| `/tars:evolve` | 프로토콜 자체를 개선합니다 — 템플릿, 훅, 스킬을 수정하고 버전을 올립니다. |
| `/tars:upgrade` | 기존 .tars/ 프로젝트를 최신 플러그인 버전으로 업그레이드합니다. |
| `/tars:team` | 기존 solo 프로젝트에 팀 에이전트 구성을 추가합니다. |

## Quick Start

```
1. /tars:init                      ← .tars/ 생성 및 core 선택
2. core 선택 (dev / design / ...)
3. 실행 방식 선택 (solo / team)
4. /tars:heartbeat                 ← 수동 실행
   또는
   /loop 10m /tars:heartbeat       ← 자동 반복 실행
```

## Core 시스템

tars는 **core** 단위로 에이전트의 운영 프로토콜을 정의합니다.

| Core | 설명 |
|------|------|
| `dev` | 빌드 검증, 코드 패트롤, 테스트 전략 중심 |
| `design` | 디자인 이터레이션, 산출물 관리, 피드백 루프 중심 |

커뮤니티 core 추가: `cores/` 디렉토리에 `core.json` + `PROTOCOL.md` + `MISSION.md`를 복사하면 자동 인식됩니다.

## 핵심 원칙

- `.tars/` 파일이 에이전트의 유일한 진실 공급원(source of truth)입니다.
- 에이전트는 COMMS를 통해 사람과 소통하고, BACKLOG로 작업을 관리합니다.
- 모든 작업은 LOG에 기록되며, 주기적으로 RETRO를 통해 개선됩니다.
