---
name: init
description: "Initialize autonomous agent protocol in current project. Scaffolds .tars/ directory with core-based templates, creates heartbeat command, guard hook, and configures permissions. Supports solo and team execution modes."
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# /tars:init — 자율 에이전트 프로토콜 초기화

이 스킬은 현재 프로젝트에 `.tars/` 자율 운영 환경을 설치합니다.

## 실행 절차

### Step 1: Core 스캔

`${CLAUDE_SKILL_DIR}/../../cores/` 하위 디렉토리를 스캔합니다.
- `shared`, `team` 디렉토리는 제외
- 각 디렉토리에서 `core.json`을 읽어 유효성 검증:
  - `core.json` 존재 여부
  - 필수 필드: `name`, `label`, `description`
  - `PROTOCOL.md` 존재 여부
  - `MISSION.md` 존재 여부
- 유효하지 않은 core는 제외하고 경고 출력

### Step 2: 정보 수집

사용자에게 다음을 질문합니다 (AskUserQuestion 사용):

1. **실행 방식**: `solo` (단일 에이전트) 또는 `team` (팀 에이전트)
   - solo: 하나의 에이전트가 하나의 core로 자율 운영
   - team: orchestrator + core별 전문 에이전트가 협업

2. **Core 선택**:
   - solo → 단일 선택. Step 1에서 스캔한 core 목록을 선택지로 제시 (core.json의 `label`과 `description` 사용)
   - team → 복수 선택 (multiSelect). 팀에 포함할 core들을 선택

3. **프로젝트명**: 프로젝트의 이름 (MISSION.md의 `{PROJECT_NAME}`에 사용)

4. **미션 설명**: 한 줄로 프로젝트의 목적 (MISSION.md의 `{MISSION_DESCRIPTION}`에 사용)

5. **Core별 추가 질문**: 선택된 core의 `core.json` → `placeholders` 배열을 확인하여, 각 placeholder에 대해 질문
   - `prompt` 필드를 질문 텍스트로 사용
   - `example` 필드를 참고 안내로 표시
   - 예: dev core 선택 시 → `BUILD_CMD`, `TEST_CMD`, `LINT_CMD` 질문

### Step 3: 디렉토리 생성

```bash
mkdir -p .tars/protocol
mkdir -p .tars/logs/archive
mkdir -p .tars/logs/backlog-archive
```

**`.tars/.version`** 생성:
- `${CLAUDE_SKILL_DIR}/../../.claude-plugin/plugin.json`에서 version 읽기
- Write:
```json
{
  "version": "{plugin_version}",
  "core": "{core_name}",
  "core_version": "{core.json의 version}",
  "execution": "{solo 또는 team}",
  "team_cores": [],
  "initialized_at": "{현재 ISO 타임스탬프}",
  "upgraded_at": null,
  "upgrade_history": []
}
```
- team 모드일 경우: `team_cores`에 선택된 core 이름 배열 설정 (예: `["dev", "design"]`)
- solo 모드일 경우: `team_cores`는 빈 배열

**core.json의 `extra_dirs`** 처리:
- 선택된 core의 `extra_dirs` 배열에 있는 각 경로에 대해:
  ```bash
  mkdir -p .tars/{dir}
  ```

### Step 4: 템플릿 복사 및 플레이스홀더 치환

tars 플러그인의 cores 디렉토리에서 파일을 읽고, 내용을 프로젝트의 `.tars/`에 Write합니다.

> **템플릿 경로**: `${CLAUDE_SKILL_DIR}/../../cores/`

#### Solo 모드

**Core별 파일:**
- `cores/{core_name}/MISSION.md` → `.tars/protocol/MISSION.md`
  - `{PROJECT_NAME}` → 사용자 입력값
  - `{MISSION_DESCRIPTION}` → 사용자 입력값
  - core.json placeholders의 각 `{KEY}` → 사용자 입력값
- `cores/{core_name}/PROTOCOL.md` → `.tars/protocol/PROTOCOL.md`

#### Team 모드

**Orchestrator 프로토콜:**
- `cores/team/ORCHESTRATOR_PROTOCOL.md` → `.tars/protocol/PROTOCOL.md`

**Team 모드에서 MISSION.md:**
- team_cores 중 **첫 번째 core**의 MISSION.md를 기반으로 생성
- 플레이스홀더 치환 동일

**공통 파일 (solo/team 동일):**
- `cores/shared/COMMS.md` → `.tars/COMMS.md`
- `cores/shared/BACKLOG.md` → `.tars/BACKLOG.md`
- `cores/shared/PROGRESS.md` → `.tars/PROGRESS.md`
  - `{CORE}` → 선택한 core 이름 (team이면 `team:{core1}+{core2}`)
- `cores/shared/LOG.md` → `.tars/logs/LOG.md`
- `cores/shared/RETRO.md` → `.tars/logs/RETRO.md`
- `cores/shared/MILESTONES.md` → `.tars/MILESTONES.md`

**core.json의 `extra_templates`** 처리:
- 각 항목의 `source`를 cores/ 기준으로 읽고, `dest`를 .tars/ 기준으로 Write

**EVOLUTION.md** (`.tars/protocol/EVOLUTION.md`에 직접 생성):
```markdown
# Protocol Evolution Log
> RETRO에서 발견한 시스템 개선을 추적합니다.
> Type: parameter-patch | structural-patch | revert | question
> Status: applied | proposed | reverted | resolved

| # | Heartbeat | Type | Change | Reason | Status |
|---|-----------|------|--------|--------|--------|
```

**backlog-archive/INDEX.md** (`.tars/logs/backlog-archive/INDEX.md`에 직접 생성):
```markdown
# Backlog Archive Index
> 완료된 티켓 아카이브 목록

(비어 있음)
```

### Step 5: Team 에이전트 생성 (team 모드만)

team 모드 선택 시에만 실행합니다.

#### 5a. _workspace 디렉토리

```bash
mkdir -p .tars/_workspace
```

#### 5b. 전문 에이전트 생성

`.claude/agents/` 디렉토리 생성.

선택된 각 core에 대해:
1. `cores/team/core-agent.md` 템플릿 읽기
2. 플레이스홀더 치환:
   - `{CORE_LABEL}` → core.json의 `label`
   - `{CORE_DESCRIPTION}` → core.json의 `description`
3. `.claude/agents/{core_name}-agent.md`에 Write

#### 5c. Orchestrator 에이전트 생성

1. `cores/team/orchestrator-agent.md` 템플릿 읽기
2. `{AGENT_LIST}` 치환 → 에이전트 목록 마크다운:
   ```
   - **dev-agent**: 개발 — 빌드 검증, 코드 패트롤, 테스트 전략
   - **design-agent**: 기획 — 디자인 이터레이션, 산출물 관리
   ```
3. `.claude/agents/orchestrator.md`에 Write

### Step 6: BACKLOG 초기 티켓 등록

`.tars/BACKLOG.md`의 Active 섹션에 추가:
```markdown
- [ ] P2 | ops/init-001 | MISSION.md 커스터마이징 — 프로젝트에 맞게 DoD, Testing Strategy, Constraints 수정
```

### Step 7: .claude/ 설정

**`.claude/commands/heartbeat.md`** 생성:
```markdown
.tars/protocol/PROTOCOL.md를 읽고 Heartbeat Cycle을 정확히 실행하세요.
현재 heartbeat 수는 .tars/PROGRESS.md에서 확인합니다.
실행이 끝나면 PROGRESS.md의 heartbeat 수를 +1 합니다.
```

**`.claude/guard.py`** 생성:
- `${CLAUDE_SKILL_DIR}/../../hooks/guard.py` 파일 내용을 읽기
- `{PROJECT_DIR}` 플레이스홀더를 현재 프로젝트의 절대 경로로 치환
- `.claude/guard.py`에 Write

**`.claude/settings.local.json`** 생성 또는 병합:
- 이미 존재하면 기존 내용을 읽고 병합
- 없으면 새로 생성
- 추가할 내용:
```json
{
  "permissions": {
    "allow": [
      "Bash(mkdir:*)",
      "Bash(ls:*)",
      "Bash(git:*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|NotebookEdit|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/guard.py"
          }
        ]
      }
    ]
  }
}
```

### Step 8: .gitignore 설정

- 프로젝트 루트의 `.gitignore` 확인
- 이미 `# tars` 섹션이 있으면 스킵
- 없으면 `${CLAUDE_SKILL_DIR}/../../cores/shared/gitignore.snippet` 내용을 읽고 `.gitignore` 끝에 추가
- `.gitignore`가 없으면 snippet 내용으로 새로 생성

### Step 9: 완료 메시지

#### Solo 모드

```
## tars 초기화 완료

**Core**: {core_name} ({core_label})
**프로젝트**: {project_name}
**실행 방식**: solo

### 생성된 파일
- .tars/ — 자율 운영 프로토콜 디렉토리
- .claude/commands/heartbeat.md — heartbeat 커맨드
- .claude/guard.py — 파일 수정 가드
- .claude/settings.local.json — 퍼미션 + 훅 설정

### 다음 단계
1. `.tars/protocol/MISSION.md`를 프로젝트에 맞게 커스터마이징
2. `.tars/BACKLOG.md`에 작업 티켓 등록
3. `/tars:heartbeat` 또는 `/loop 10m /tars:heartbeat`로 자율 운영 시작
```

#### Team 모드

```
## tars 팀 초기화 완료

**Core**: {team_cores 목록}
**프로젝트**: {project_name}
**실행 방식**: team

### 생성된 파일
- .tars/ — 자율 운영 프로토콜 디렉토리
- .claude/agents/orchestrator.md — 팀 조율자
- .claude/agents/{core}-agent.md — 전문 에이전트 (각 core별)
- .claude/commands/heartbeat.md — heartbeat 커맨드
- .claude/guard.py — 파일 수정 가드

### 다음 단계
1. `.tars/protocol/MISSION.md`를 프로젝트에 맞게 커스터마이징
2. `.tars/BACKLOG.md`에 작업 티켓 등록
3. `/tars:heartbeat`로 orchestrator가 팀을 조율합니다
```

## 주의사항
- 이미 `.tars/` 디렉토리가 존재하면 사용자에게 경고하고 덮어쓸지 확인
- `.claude/settings.local.json`은 기존 설정을 보존하며 병합
- 모든 파일 Write 시 절대 경로 사용
