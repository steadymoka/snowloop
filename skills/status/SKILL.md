---
name: status
description: "Display compact dashboard of current autonomous operation state. Shows progress, backlog depth, heartbeat count, latest retro metrics, and anomaly flags."
allowed-tools: Read, Glob
---

# /tars:status — 운영 대시보드

## 실행 절차

### 1. 파일 읽기
다음 파일을 읽습니다:
- `.tars/PROGRESS.md` — 현재 heartbeat, 현재 작업, core
- `.tars/BACKLOG.md` — 백로그 깊이 (미완료 티켓 수)
- `.tars/logs/LOG.md` — 최근 3개 heartbeat 기록
- `.tars/logs/RETRO.md` — 최신 RETRO (있으면)
- `.tars/COMMS.md` — From Human / From Agent 메시지 수
- `.tars/protocol/EVOLUTION.md` — 최근 프로토콜 변경 (있으면)
- `.tars/MILESTONES.md` — Milestone 상태 (active/done/dropped 수)

### 2. 대시보드 출력

```
## tars status

| 항목 | 값 |
|------|-----|
| Core | {dev/design/...} |
| Heartbeat | #{n} |
| Current Task | {task or 없음} |
| Phase | {phase} |
| Backlog | {n}개 (P0: {n}, P1: {n}, P2: {n}, P3: {n}) |
| Milestones | active: {n}개, done: {n}개 |
| COMMS | From Human: {n}개, From Agent: {n}개 |
| Last RETRO | #{n} (ratio: {n}%) |
| Protocol Patches | {n}개 (applied: {n}, reverted: {n}) |

### 최근 활동 (3 heartbeats)
- HB#{n}: {요약}
- HB#{n}: {요약}
- HB#{n}: {요약}
```

### 3. 이상 징후 플래그

다음 조건에서 경고를 표시합니다:

- **RETRO 예정**: heartbeat % 10 >= 8 → "RETRO가 곧 실행됩니다 (HB#{다음 10 배수})"
- **높은 idle 비율**: 최신 RETRO의 productive_ratio < 50% → "생산성 경고: idle 비율이 높습니다"
- **오래된 COMMS**: From Agent에 3 heartbeat 이상 된 메시지 → "미응답 메시지가 있습니다"
- **Stagnation**: 같은 task가 3 heartbeat 이상 → "동일 작업 장기 진행 중"
- **미응답 Protocol Patch**: COMMS에 `[PROTOCOL-PATCH]`가 1 heartbeat 이상 대기 → "프로토콜 패치 대기 중"
- **Milestone 과부하**: active Milestone 3개 이상 → "Milestone이 너무 많습니다 (active: {n}개)"
- **Milestone 정체**: active Milestone이 있는데 10 HB 동안 해당 Milestone 관련 `[MILESTONE]` COMMS가 없고 BACKLOG 태스크 완료도 없음 → "Milestone 정체: 진전 없이 10 HB 경과"

## 에러 핸들링

- `.tars/` 디렉토리가 없으면: "tars이 초기화되지 않았습니다. `/tars:init`을 먼저 실행하세요."
