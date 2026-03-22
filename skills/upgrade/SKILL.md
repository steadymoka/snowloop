---
name: upgrade
description: "Upgrade existing .snowloop/ project to match current plugin version. Adds missing files, appends new PROTOCOL.md sections, and updates .version tracking."
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# /snowloop:upgrade — 프로토콜 업그레이드

기존 `.snowloop/` 프로젝트를 현재 플러그인 버전에 맞게 업그레이드합니다.

## 실행 절차

### Step 1: 사전 검사

1. `.snowloop/` 디렉토리 존재 확인. 없으면:
   > "snowloop이 초기화되지 않았습니다. `/snowloop:init`을 먼저 실행하세요."
2. 플러그인 버전 읽기: `${CLAUDE_SKILL_DIR}/../../.claude-plugin/plugin.json`의 `version`
3. 설치된 버전 읽기: `.snowloop/.version` (JSON)
   - `.version` 파일이 없으면 → version `"0.1.0"`, mode를 `.snowloop/PROGRESS.md`의 `**Mode**:` 값에서 추출
4. 버전 비교:
   - 같으면 → "이미 최신 버전입니다 (v{version})." 출력 후 종료
   - 플러그인 < 설치 → "설치된 버전이 플러그인보다 높습니다. 다운그레이드는 지원되지 않습니다." 출력 후 종료

### Step 2: 변경 사항 미리보기 (Dry Run)

#### 2a: 새 파일 감지
현재 플러그인 템플릿에 있지만 프로젝트에 없는 파일 목록 작성.

체크 대상:
- `.snowloop/EVOLUTION.md`
- `.snowloop/backlog-archive/INDEX.md`
- `.snowloop/output/` 디렉토리 + `INDEX.md` (design 모드만)
- 향후 추가될 새 파일

#### 2b: PROTOCOL.md 새 섹션 감지
1. `.snowloop/PROTOCOL.md`를 `## ` 기준으로 섹션 헤딩 추출
2. 모드별 템플릿 `${CLAUDE_SKILL_DIR}/../../templates/{mode}/PROTOCOL.md`를 같은 방식으로 추출
3. 템플릿에 있지만 사용자 파일에 없는 `## ` 헤딩 = 추가 대상

#### 2c: .gitignore 감지
- `${CLAUDE_SKILL_DIR}/../../templates/shared/gitignore.snippet`의 각 줄이 `.gitignore`에 있는지 확인

#### 출력 형식
```
## snowloop upgrade 미리보기
v{old} → v{new}

### 새 파일 생성
- .snowloop/EVOLUTION.md
- (또는 "없음")

### PROTOCOL.md 새 섹션
- + "## Emergency Protocol"
- (또는 "없음")

### .gitignore
- 새 규칙 {n}줄 추가
- (또는 "변경 없음")

### 건드리지 않는 파일
LOG, RETRO, BACKLOG, COMMS, PROGRESS, EVOLUTION(기존 내용),
MISSION, PROTOCOL(기존 섹션), backlog-archive/, logs/, output/(기존 산출물)
```

사용자에게 확인을 요청합니다. 거부하면 종료.

### Step 3: 적용

#### 3a: 새 파일 생성
- 템플릿에서 읽어서 `.snowloop/`에 Write
- design 모드: output 디렉토리 구조 생성 (없는 경우)

#### 3b: PROTOCOL.md 섹션 추가
- 템플릿에만 있는 새 섹션을 `.snowloop/PROTOCOL.md` 끝에 append
- 각 섹션 앞에 `---` 구분자 추가
- 기존 내용은 절대 수정하지 않음
- self-evolution이 다음 RETRO에서 정리함

#### 3c: .gitignore 갱신
- `# snowloop` 섹션이 있으면 해당 섹션에 누락 줄 추가
- 없으면 snippet 전체를 끝에 추가

#### 3d: .version 갱신
`.snowloop/.version`에 Write:
```json
{
  "version": "{new_version}",
  "mode": "{mode}",
  "initialized_at": "{기존값 또는 unknown}",
  "upgraded_at": "{현재 ISO 타임스탬프}",
  "upgrade_history": [
    ...기존 항목,
    { "from": "{old}", "to": "{new}", "at": "{timestamp}" }
  ]
}
```

> `.version`은 반드시 마지막에 Write합니다. 중간 실패 시 재실행 가능.

### Step 4: EVOLUTION.md 기록

EVOLUTION.md 테이블에 행 추가:
```
| {next_seq} | - | upgrade | snowloop v{old} → v{new} | Plugin upgrade | applied |
```

### Step 5: 완료 보고

```
## snowloop 업그레이드 완료

v{old} → v{new}

### 적용된 변경
- {각 항목 요약}

### 다음 단계
- PROTOCOL.md에 새로 추가된 섹션을 확인하세요
- 다음 RETRO에서 self-evolution이 새 섹션을 평가합니다
```

## 주의사항
- 사용자 데이터 파일(LOG, RETRO, BACKLOG, COMMS, PROGRESS, EVOLUTION 기존 내용)은 절대 수정하지 않습니다
- PROTOCOL.md는 새 섹션만 append합니다. 기존 섹션은 건드리지 않습니다
- MISSION.md는 수정하지 않습니다 (사용자 커스텀 값 보존)
- `.version` 파일은 반드시 마지막에 Write합니다
- Dry run에서 사용자가 거부하면 아무 것도 변경하지 않습니다
