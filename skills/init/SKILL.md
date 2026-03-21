---
name: init
description: "Initialize autonomous agent protocol in current project. Scaffolds .snowloop/ directory with mode-specific templates (dev or plan), creates heartbeat command, guard hook, and configures permissions."
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# /snowloop:init — 자율 에이전트 프로토콜 초기화

이 스킬은 현재 프로젝트에 `.snowloop/` 자율 운영 환경을 설치합니다.

## 실행 절차

### Step 1: 정보 수집

사용자에게 다음을 질문합니다 (AskUserQuestion 사용):

1. **모드 선택**: `dev` (개발) 또는 `plan` (기획)
   - dev: 빌드 검증, 코드 패트롤, 테스트 전략 중심
   - plan: 디자인 이터레이션, 산출물 관리, 피드백 루프 중심

2. **프로젝트명**: 프로젝트의 이름 (MISSION.md의 `{PROJECT_NAME}`에 사용)

3. **미션 설명**: 한 줄로 프로젝트의 목적 (MISSION.md의 `{MISSION_DESCRIPTION}`에 사용)

4. **(dev 모드만)** 빌드/테스트/린트 커맨드:
   - `{BUILD_CMD}`: 예) `npm run build`, `cargo build`, `./gradlew build`
   - `{TEST_CMD}`: 예) `npm test`, `cargo test`, `./gradlew test`
   - `{LINT_CMD}`: 예) `npm run lint`, `cargo clippy`, `./gradlew ktlintCheck`

### Step 2: 디렉토리 생성

```bash
mkdir -p .snowloop/logs
mkdir -p .snowloop/backlog-archive
```

plan 모드인 경우 추가:
```bash
mkdir -p .snowloop/output/specs
mkdir -p .snowloop/output/wireframes
mkdir -p .snowloop/output/research
mkdir -p .snowloop/output/drafts
```

### Step 3: 템플릿 복사 및 플레이스홀더 치환

snowloop 플러그인의 템플릿 디렉토리에서 파일을 읽고, 내용을 프로젝트의 `.snowloop/`에 Write합니다.

> **템플릿 경로**: `${CLAUDE_SKILL_DIR}/../../templates/`

**모드별 파일:**
- `${CLAUDE_SKILL_DIR}/../../templates/{mode}/MISSION.md` → `.snowloop/MISSION.md`
  - `{PROJECT_NAME}` → 사용자 입력값
  - `{MISSION_DESCRIPTION}` → 사용자 입력값
  - dev 모드: `{BUILD_CMD}`, `{TEST_CMD}`, `{LINT_CMD}` → 사용자 입력값
- `${CLAUDE_SKILL_DIR}/../../templates/{mode}/PROTOCOL.md` → `.snowloop/PROTOCOL.md`

**공통 파일:**
- `${CLAUDE_SKILL_DIR}/../../templates/shared/COMMS.md` → `.snowloop/COMMS.md`
- `${CLAUDE_SKILL_DIR}/../../templates/shared/BACKLOG.md` → `.snowloop/BACKLOG.md`
- `${CLAUDE_SKILL_DIR}/../../templates/shared/PROGRESS.md` → `.snowloop/PROGRESS.md`
  - `{MODE}` → 선택한 모드 (dev 또는 plan)
- `${CLAUDE_SKILL_DIR}/../../templates/shared/LOG.md` → `.snowloop/LOG.md`
- `${CLAUDE_SKILL_DIR}/../../templates/shared/RETRO.md` → `.snowloop/RETRO.md`

**EVOLUTION.md** (직접 생성):
```markdown
# Protocol Evolution Log
> RETRO에서 발견한 시스템 개선을 추적합니다.
> Type: parameter-patch | structural-patch | revert | question
> Status: applied | proposed | reverted | resolved

| # | Heartbeat | Type | Change | Reason | Status |
|---|-----------|------|--------|--------|--------|
```

**plan 모드 추가 파일:**
- `${CLAUDE_SKILL_DIR}/../../templates/shared/OUTPUT_INDEX.md` → `.snowloop/output/INDEX.md`

**backlog-archive/INDEX.md** (직접 생성):
```markdown
# Backlog Archive Index
> 완료된 티켓 아카이브 목록

(비어 있음)
```

### Step 4: BACKLOG 초기 티켓 등록

`.snowloop/BACKLOG.md`의 Active 섹션에 추가:
```markdown
- [ ] P2 | ops/init-001 | MISSION.md 커스터마이징 — 프로젝트에 맞게 DoD, Testing Strategy, Constraints 수정
```

### Step 5: .claude/ 설정

**`.claude/commands/heartbeat.md`** 생성:
```markdown
.snowloop/PROTOCOL.md를 읽고 Heartbeat Cycle을 정확히 실행하세요.
현재 heartbeat 수는 .snowloop/PROGRESS.md에서 확인합니다.
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
        "matcher": "Write|Edit|NotebookEdit",
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

### Step 6: .gitignore 설정

- 프로젝트 루트의 `.gitignore` 확인
- 이미 `# snowloop` 섹션이 있으면 스킵
- 없으면 `${CLAUDE_SKILL_DIR}/../../templates/shared/gitignore.snippet` 내용을 읽고 `.gitignore` 끝에 추가
- `.gitignore`가 없으면 snippet 내용으로 새로 생성

### Step 7: 완료 메시지

```
## snowloop 초기화 완료

**모드**: {mode}
**프로젝트**: {project_name}

### 생성된 파일
- .snowloop/ — 자율 운영 프로토콜 디렉토리
- .claude/commands/heartbeat.md — heartbeat 커맨드
- .claude/guard.py — 파일 수정 가드
- .claude/settings.local.json — 퍼미션 + 훅 설정

### 다음 단계
1. `.snowloop/MISSION.md`를 프로젝트에 맞게 커스터마이징
2. `.snowloop/BACKLOG.md`에 작업 티켓 등록
3. `/snowloop:heartbeat` 또는 `/loop 10m /snowloop:heartbeat`로 자율 운영 시작
```

## 주의사항
- 이미 `.snowloop/` 디렉토리가 존재하면 사용자에게 경고하고 덮어쓸지 확인
- `.claude/settings.local.json`은 기존 설정을 보존하며 병합
- 모든 파일 Write 시 절대 경로 사용
