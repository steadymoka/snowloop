# Changelog

## [0.2.0] - 2026-03-22

### Added

- `/snowloop:upgrade` skill for upgrading existing projects to new plugin versions
- `.snowloop/.version` tracking file (written during init)
- `.upgrade-backup/` to gitignore snippet

### Changed

- Reorganize `.snowloop/` directory structure (8 root files → 3 + subfolders)
  - `protocol/`: MISSION.md, PROTOCOL.md, EVOLUTION.md
  - `logs/`: LOG.md, RETRO.md, archive/, backlog-archive/
  - Root: COMMS.md, BACKLOG.md, PROGRESS.md only
- Autonomous mode documentation with `--dangerously-skip-permissions`

## [0.1.1] - 2026-03-21

### Changed

- Rename `plan` mode to `design` mode to avoid confusion with Claude Code's built-in plan mode
- Add English comment headers to all template files for reviewer clarity
- Add `hooks/hooks.json` with SessionStart hook for `.snowloop/` project detection
- Add `allowed-tools` and `disable-model-invocation` frontmatter to all skills
- Add `${CLAUDE_SKILL_DIR}` template paths in init skill for reliable plugin resolution
- Add component paths (`skills`, `hooks`) to `plugin.json`

## [0.1.0] - 2026-03-21

### Added

- **Plugin skeleton**: `plugin.json`, `CLAUDE.md`, `package.json`
- **5 skills**: init, heartbeat, status, retro, evolve
- **2 mode templates**: dev (빌드 검증/코드 패트롤), design (디자인 이터레이션/산출물 관리)
- **Shared templates**: COMMS (INBOX+OUTBOX 통합), BACKLOG, PROGRESS, LOG, RETRO
- **Self-evolution mechanism**: Protocol Evolution (parameter-patch, structural-patch, question, revert)
- **Anomaly detection**: stagnation, oscillation, regression detection (ouroboros 패턴 참고)
- **Wonder gap analysis**: 프로세스 가정에 대한 소크라테스식 질문
- **Guard hook**: 프로젝트 디렉토리 밖 파일 수정 차단
- **SessionStart hook**: `.snowloop/` 프로젝트 감지 시 자동 안내
- **Output management**: design 모드 산출물 구조 (`specs/`, `wireframes/`, `research/`)
- **`.gitignore` auto-setup**: init 시 자동 규칙 추가
