# Orchestrator Heartbeat Protocol

> 이 프로토콜은 team 실행 방식에서 orchestrator 에이전트가 따르는 사이클입니다.

## Heartbeat 사이클

### 1. 상태 확인 (Read only)

다음 파일을 **순서대로** 읽는다:

1. `.tars/PROGRESS.md` — 현재 세션 상태, heartbeat 횟수
2. `.tars/COMMS.md` — 사람의 메시지, 에이전트 제안
3. `.tars/BACKLOG.md` — 미처리 태스크 목록

### 2. COMMS 처리

- `### From Human` 메시지가 있으면 **최우선** 처리
- 에이전트의 `[CLARIFY]` 태그 → 1 HB 후 자동 해석 적용
- `[PROTOCOL-PATCH]` → 1 HB 후 자동 적용
- 기타 자동 해결 규칙은 PROTOCOL.md의 COMMS 섹션을 따름

### 3. 태스크 분석 & 분배

BACKLOG에서 가장 높은 우선순위 태스크를 분석:

1. **태스크 분류**: 어떤 core의 전문 에이전트가 적합한지 판단
2. **의존성 확인**: 다른 에이전트의 산출물이 필요한지 확인
3. **할당 결정**: 적합한 에이전트에 TaskCreate로 작업 할당

### 4. 에이전트 디스패치

```
TaskCreate → {core}-agent에 작업 할당
SendMessage → 의존성/컨텍스트 전달
```

**디스패치 규칙**:
- 하나의 태스크는 하나의 에이전트에만 할당
- 독립적인 태스크는 병렬 디스패치 가능
- 에이전트 간 의존성이 있으면 순차 디스패치

### 5. 진행 모니터링

- TaskGet으로 에이전트 진행 상태 확인
- 블로킹 이슈 발생 시 SendMessage로 조율
- 완료된 결과를 `.tars/_workspace/`에서 수집

### 6. 결과 통합 & 기록

- 에이전트 결과물을 `.tars/_workspace/`에서 읽음
- BACKLOG 태스크 상태 갱신 (완료/진행중)
- LOG에 기록:
  ```
  - **Team**: {agent} → {task_summary}
  - **결과**: {success/fail/inprogress}
  - **산출물**: {_workspace/ 경로}
  ```

### 7. PROGRESS 갱신

- heartbeat 횟수 +1
- 활성 에이전트 상태 요약
- 다음 heartbeat 예정 작업

### 8. RETRO 체크

10 heartbeat마다 RETRO 실행:
- 팀 전체의 productive/idle/blocked 비율 분석
- 에이전트별 효율성 비교
- 병목 에이전트 식별
- 프로토콜 개선 제안

## Proactive Work (BACKLOG 비었을 때)

1. **팀 건강 점검**: 각 에이전트의 최근 결과물 품질 리뷰
2. **의존성 해소**: 에이전트 간 미해결 블로커 정리
3. **갭 분석**: MISSION 대비 미달성 영역 식별 → BACKLOG에 태스크 추가

## 파일 접근 규칙

| 파일/디렉토리 | orchestrator | 전문 에이전트 |
|---|---|---|
| `.tars/BACKLOG.md` | 읽기/쓰기 | 읽기만 |
| `.tars/COMMS.md` | 읽기/쓰기 | 읽기만 |
| `.tars/LOG.md` | 읽기/쓰기 | 읽기만 |
| `.tars/PROGRESS.md` | 읽기/쓰기 | 읽기만 |
| `.tars/protocol/MISSION.md` | 읽기만 | 읽기만 |
| `.tars/_workspace/` | 읽기/쓰기 | 읽기/쓰기 |
| 프로젝트 소스코드 | 읽기만 | 읽기/쓰기 |
