---
name: evolve
description: "Manually trigger protocol evolution analysis. Reviews EVOLUTION.md history, analyzes RETRO patterns, compares patch effectiveness, and suggests protocol improvements with lateral thinking options."
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob
---

# /snowloop:evolve — 프로토콜 진화 분석

수동으로 프로토콜 진화를 트리거합니다. RETRO와 EVOLUTION 이력을 분석하여 프로토콜 개선을 제안합니다.

## 실행 절차

### 1. 데이터 수집

다음 파일을 읽습니다:
- `.snowloop/protocol/EVOLUTION.md` — 전체 변경 이력
- `.snowloop/logs/RETRO.md` — 모든 RETRO 기록
- `.snowloop/protocol/PROTOCOL.md` — 현재 프로토콜
- `.snowloop/PROGRESS.md` — 현재 heartbeat 수

### 2. Evolution 이력 분석

#### 패치 효과 분석
- 각 applied patch 이후의 RETRO 메트릭 변화 추적
- 효과적인 패치: 메트릭 개선 유지 → "유효한 진화" 표시
- 비효과적인 패치: 메트릭 변화 없음 → "중립적" 표시
- 악화시킨 패치: 이미 REVERTED됐어야 함 → 안 됐으면 revert 제안

#### 패턴 요약
- **Question 빈도**: 반복되는 질문 TOP 3
- **Patch 빈도**: 가장 자주 변경되는 PROTOCOL 영역
- **Oscillation 이력**: 과거 oscillation 기록 및 해결 여부

### 3. RETRO 패턴 분석

- productive_ratio 추세 (상승/하락/안정)
- 반복 등장하는 "개선할 점" 키워드
- 미완료 액션 아이템 목록

### 4. 프로토콜 개선 제안

분석 결과를 바탕으로 개선 목록 생성:

```markdown
## 프로토콜 진화 제안

### 즉시 적용 가능 (Parameter Patch)
1. {제안 1}: {근거}
2. {제안 2}: {근거}

### 구조적 변경 필요 (Structural Patch)
1. {제안 1}: {근거}
2. {제안 2}: {근거}

### 미해결 질문 (Wonder)
1. {질문 1} — {반복 횟수}회 등장
2. {질문 2} — {반복 횟수}회 등장
```

### 5. Lateral Thinking 옵션 (Stagnation 감지 시)

productive_ratio 추세가 하락 중이거나, oscillation이 해결되지 않았을 때:

```markdown
### Lateral Thinking 옵션

현재 프로토콜이 정체 상태입니다. 다음 관점 전환을 고려하세요:

**A. 현재 접근 유지 + 미세 조정**
- 현재 구조를 유지하되 파라미터만 조정
- 적합: 메트릭이 안정적이지만 소폭 개선 필요할 때

**B. 구조적 재설계**
- 문제 영역의 프로토콜 섹션을 재작성
- 적합: 같은 문제가 반복될 때 (oscillation)

**C. 범위 축소**
- 프로토콜의 복잡도를 줄여 핵심에 집중
- 적합: 프로토콜이 과도하게 복잡해졌을 때

**D. 가정 재검토**
- Wonder 질문들을 정면으로 답변하고 프로토콜에 반영
- 적합: 미해결 질문이 누적되었을 때
```

### 6. 사용자 선택 후 실행

사용자가 개선안을 선택하면:
- Parameter patch → `protocol/PROTOCOL.md`에 즉시 적용 + `protocol/EVOLUTION.md` 기록
- Structural patch → COMMS `From Agent`에 `[PROTOCOL-PATCH]` 제안 등록
- Lateral thinking → 선택한 옵션에 따라 구체적 변경안 생성

## 에러 핸들링

- EVOLUTION.md가 비어있으면: "아직 프로토콜 변경 이력이 없습니다. heartbeat를 먼저 충분히 실행하세요."
- RETRO가 없으면: "RETRO가 없습니다. `/snowloop:retro`를 먼저 실행하세요."
- `.snowloop/` 없으면: "snowloop이 초기화되지 않았습니다."
