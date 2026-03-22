---
name: heartbeat
description: "Execute one autonomous heartbeat cycle. Reads .snowloop/protocol/PROTOCOL.md and follows it exactly. Use with /loop for continuous operation."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
---

# /snowloop:heartbeat — 자율 운영 1 사이클

## 실행 절차

1. `.snowloop/protocol/PROTOCOL.md` 파일을 읽습니다
2. PROTOCOL.md의 "Heartbeat Cycle" 섹션을 **정확히** 따릅니다
3. 각 단계(상태 확인 → 작업 실행 → 기록 → RETRO 체크 → COMMS 정리 → LOG 아카이브)를 순서대로 실행합니다

## 에러 핸들링

- `.snowloop/protocol/PROTOCOL.md`가 없으면: "snowloop이 초기화되지 않았습니다. `/snowloop:init`을 먼저 실행하세요." 출력 후 종료
- `.snowloop/PROGRESS.md`가 없으면: 위와 동일
- 작업 실행 중 에러 발생 시: LOG에 에러 기록, 다음 heartbeat로 넘기기

## 연속 운영

`/loop 10m /snowloop:heartbeat` 명령으로 10분마다 자동 실행할 수 있습니다.

## 핵심 원칙

- PROTOCOL.md가 유일한 진실의 원천입니다
- 이 스킬은 **위임**만 합니다 — 판단은 PROTOCOL.md에 따릅니다
- PROTOCOL.md가 self-evolution으로 변경되면 다음 heartbeat부터 새 프로토콜을 따릅니다
