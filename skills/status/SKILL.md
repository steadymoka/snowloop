---
name: status
description: "Display compact dashboard of current autonomous operation state. Shows progress, backlog depth, heartbeat count, latest retro metrics, and anomaly flags."
allowed-tools: Read, Glob
---

# /snowloop:status — 운영 대시보드

## 실행 절차

### 1. 파일 읽기
다음 파일을 읽습니다:
- `.snowloop/PROGRESS.md` — 현재 heartbeat, 현재 작업, 모드
- `.snowloop/BACKLOG.md` — 백로그 깊이 (미완료 티켓 수)
- `.snowloop/LOG.md` — 최근 3개 heartbeat 기록
- `.snowloop/RETRO.md` — 최신 RETRO (있으면)
- `.snowloop/COMMS.md` — Pending 메시지 수
- `.snowloop/EVOLUTION.md` — 최근 프로토콜 변경 (있으면)

### 2. 대시보드 출력

```
## snowloop status

| 항목 | 값 |
|------|-----|
| Mode | {dev/plan} |
| Heartbeat | #{n} |
| Current Task | {task or 없음} |
| Phase | {phase} |
| Backlog | {n}개 (P0: {n}, P1: {n}, P2: {n}, P3: {n}) |
| Pending COMMS | {n}개 |
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
- **오래된 COMMS**: Pending에 3 heartbeat 이상 된 메시지 → "미처리 메시지가 있습니다"
- **Stagnation**: 같은 task가 3 heartbeat 이상 → "동일 작업 장기 진행 중"
- **미응답 Protocol Patch**: COMMS에 `[PROTOCOL-PATCH]`가 1 heartbeat 이상 대기 → "프로토콜 패치 대기 중"

## 에러 핸들링

- `.snowloop/` 디렉토리가 없으면: "snowloop이 초기화되지 않았습니다. `/snowloop:init`을 먼저 실행하세요."
