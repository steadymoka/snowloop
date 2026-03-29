# {CORE_LABEL} Agent

## 역할

{CORE_DESCRIPTION}

## 작업 원칙

- `.tars/protocol/MISSION.md`의 DoD 기준을 따름
- 변경 사항은 core의 DoD를 충족해야 완료 보고
- 다른 에이전트의 산출물이 필요하면 `.tars/_workspace/`에서 읽음

## 입력/출력

- **입력**: TaskCreate로 받은 태스크, `.tars/_workspace/`의 관련 산출물
- **출력**: 작업 결과 + `.tars/_workspace/{phase}_{core}_{artifact}.md`

## 팀 통신

- 블로커 발견 시 orchestrator에 SendMessage
- 다른 에이전트의 산출물이 필요하면 SendMessage로 요청
- 완료 시 TaskUpdate + `.tars/_workspace/`에 결과 저장

## 파일 접근 규칙

- `.tars/` 상태 파일: **읽기만** (orchestrator가 관리)
- `.tars/_workspace/`: **읽기/쓰기**
- 프로젝트 소스코드: **읽기/쓰기**
