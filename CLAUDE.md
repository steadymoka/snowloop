# snowloop

자율 에이전트 운영 플러그인 — `.snowloop/` 프로토콜을 통해 에이전트가 스스로 진화합니다.

## 사용 가능한 Skills

| Skill | 설명 |
|-------|------|
| `/snowloop:init` | 프로젝트에 `.snowloop/` 디렉토리를 초기화하고 운영 모드를 선택합니다. |
| `/snowloop:heartbeat` | 한 사이클을 실행합니다 — COMMS 확인, BACKLOG 처리, PROGRESS 갱신, LOG 기록. |
| `/snowloop:status` | 현재 세션 상태를 요약합니다 (진행 중 태스크, heartbeat 수, 미처리 메시지). |
| `/snowloop:retro` | 회고를 즉시 실행합니다. 무엇이 잘 됐고, 무엇을 개선할지 기록합니다. |
| `/snowloop:evolve` | 프로토콜 자체를 개선합니다 — 템플릿, 훅, 스킬을 수정하고 버전을 올립니다. |
| `/snowloop:upgrade` | 기존 .snowloop/ 프로젝트를 최신 플러그인 버전으로 업그레이드합니다. |

## Quick Start

```
1. /snowloop:init          ← .snowloop/ 생성 및 모드 선택
2. 모드 선택 (dev / design)
3. /snowloop:heartbeat     ← 수동 실행
   또는
   /loop 10m /snowloop:heartbeat   ← 자동 반복 실행
```

## 핵심 원칙

- `.snowloop/` 파일이 에이전트의 유일한 진실 공급원(source of truth)입니다.
- 에이전트는 COMMS를 통해 사람과 소통하고, BACKLOG로 작업을 관리합니다.
- 모든 작업은 LOG에 기록되며, 주기적으로 RETRO를 통해 개선됩니다.
