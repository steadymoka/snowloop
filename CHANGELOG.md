# Changelog

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
