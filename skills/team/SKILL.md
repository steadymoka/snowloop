---
name: team
description: 기존 solo 프로젝트에 팀 에이전트 구성을 추가합니다. orchestrator + core별 전문 에이전트를 생성합니다.
---

# /tars:team

기존 solo 프로젝트에 팀 에이전트 구성을 추가합니다.

## 사전 조건

- `.tars/` 디렉토리가 존재해야 합니다 (`/tars:init`으로 초기화된 상태)
- `.tars/.version` 파일이 존재해야 합니다

## 실행 절차

### Step 1: 현재 상태 확인

1. `.tars/.version` 읽기
2. 이미 `execution: "team"`이면 → 안내 메시지 출력 후 종료
3. 현재 core 확인 (예: "dev")

### Step 2: 팀 core 선택

`${CLAUDE_SKILL_DIR}/../../cores/` 하위 디렉토리를 스캔합니다 (`shared`, `team` 제외).

각 디렉토리의 `core.json`을 읽어서 유효한 core 목록을 구성합니다:
- `core.json` 필수 필드: `name`, `label`, `description`
- `PROTOCOL.md` 존재 확인
- `MISSION.md` 존재 확인

AskUserQuestion으로 팀에 포함할 core를 **복수 선택** 받습니다:
- 현재 core는 기본 선택으로 표시
- 각 core의 `label`과 `description`을 선택지에 표시

### Step 3: 에이전트 정의 생성

#### 3a. `.claude/agents/` 디렉토리 생성

프로젝트의 `.claude/agents/` 디렉토리가 없으면 생성합니다.

#### 3b. 전문 에이전트 생성

선택된 각 core에 대해:

1. `${CLAUDE_SKILL_DIR}/../../cores/team/core-agent.md` 템플릿 읽기
2. 플레이스홀더 치환:
   - `{CORE_LABEL}` → core.json의 `label`
   - `{CORE_DESCRIPTION}` → core.json의 `description`
3. `.claude/agents/{core_name}-agent.md`에 저장

#### 3c. Orchestrator 에이전트 생성

1. `${CLAUDE_SKILL_DIR}/../../cores/team/orchestrator-agent.md` 템플릿 읽기
2. `{AGENT_LIST}` → 선택된 에이전트 목록으로 치환:
   ```
   - **dev-agent**: 개발 — 빌드 검증, 코드 패트롤
   - **design-agent**: 기획 — 디자인 이터레이션, 산출물 관리
   ```
3. `.claude/agents/orchestrator.md`에 저장

### Step 4: Orchestrator 프로토콜 설치

1. `${CLAUDE_SKILL_DIR}/../../cores/team/ORCHESTRATOR_PROTOCOL.md` 읽기
2. `.tars/protocol/PROTOCOL.md`를 orchestrator 프로토콜로 **교체**
   - 기존 solo PROTOCOL.md는 `.tars/protocol/PROTOCOL_solo_backup.md`로 백업

### Step 5: _workspace 디렉토리 생성

`.tars/_workspace/` 디렉토리를 생성합니다.

### Step 6: .version 업데이트

`.tars/.version` 파일을 수정합니다:
- `execution` → `"team"`
- `team_cores` → 선택된 core 이름 배열 (예: `["dev", "design"]`)

### Step 7: 완료 안내

```
✅ 팀 에이전트 구성이 완료되었습니다.

생성된 에이전트:
- .claude/agents/orchestrator.md (팀 조율자)
- .claude/agents/dev-agent.md (개발 전문)
- .claude/agents/design-agent.md (기획 전문)

실행 방법:
/tars:heartbeat 으로 orchestrator가 팀을 조율합니다.
```
