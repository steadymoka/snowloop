<p align="right">
  <strong>English</strong> | <a href="./README.ko.md">한국어</a>
</p>

# snowloop

Autonomous agent orchestration plugin for Claude Code.

The agent self-governs through a `.snowloop/` protocol and evolves its own process over time.

## Install

```
/plugin marketplace add steadymoka/snowloop
/plugin install snowloop@steadymoka-snowloop
```

## Quick Start

```
/snowloop:init                       # scaffold .snowloop/, choose mode (dev / plan)
/snowloop:heartbeat                  # run one autonomous cycle
/loop 10m /snowloop:heartbeat        # auto-repeat every 10 minutes
```

## Skills

| Skill | Description |
|-------|-------------|
| `/snowloop:init` | Initialize `.snowloop/` in your project. Choose dev or plan mode |
| `/snowloop:heartbeat` | Read PROTOCOL.md and execute one autonomous cycle |
| `/snowloop:status` | Dashboard — heartbeat count, backlog depth, anomaly flags |
| `/snowloop:retro` | Immediate retrospective — metrics, anomaly detection, protocol improvement proposals |
| `/snowloop:evolve` | Protocol evolution analysis — patch effectiveness, lateral thinking options |

## Modes

### Dev Mode

Build verification, testing strategy, and code patrol.

- 3-level Definition of Done (L1 build → L2 functional → L3 integration)
- Proactive Work tiers: Health Audit → User Scenario → Integration Check → Code Patrol → Gap Analysis
- Phase Directives: Building → Stabilizing → Shipping

### Plan Mode

Design iteration, artifact management, and feedback loops.

- Output structure: `specs/`, `wireframes/`, `research/`
- Date-prefixed naming: `YYYY-MM-DD-<name>.<ext>`
- Proactive Work tiers: Design Improvement → Cross-pollination → Competitive Analysis → Consistency Audit → Implementation Prep
- Phase Directives: Exploring → Converging → Implementing

## How It Works

```
Heartbeat Cycle (each cycle):
  Check State → Process COMMS → Execute BACKLOG → Write LOG → RETRO Check

Self-Evolution (improvements found in RETRO):
  Stagnation Detection → Oscillation Detection → Regression Detection
  → Wonder Gap Analysis → Protocol Patch apply/propose
```

### .snowloop/ Structure

```
.snowloop/
├── MISSION.md       # Mission definition, DoD, Proactive Work
├── PROTOCOL.md      # Autonomous operation protocol (self-evolution target)
├── COMMS.md         # Human ↔ Agent communication ([→agent] / [→human])
├── BACKLOG.md       # Task list (P0~P3 priority)
├── PROGRESS.md      # Current heartbeat count, task state
├── LOG.md           # Work history
├── RETRO.md         # Retrospective records
└── EVOLUTION.md     # Protocol change history
```

## Self-Evolution

Every 10 heartbeats, a retrospective runs automatically. When it discovers process improvements, it patches PROTOCOL.md directly.

| Type | Description | How Applied |
|------|-------------|-------------|
| Parameter Patch | Threshold/count adjustments | Direct PROTOCOL.md edit |
| Structural Patch | Add/remove steps or rules | Propose via COMMS → auto-approve |
| Question | Challenge process assumptions | Escalate to patch after 3 repeats |
| Revert | Metrics worsened after patch | Auto-detect + rollback |

### Anomaly Detection

- **Stagnation**: Same task stuck for 3+ heartbeats, or 3 consecutive idle cycles
- **Oscillation**: Same patch applied → reverted → applied again (A→B→A pattern)
- **Regression**: Metrics worsened after a protocol patch (distinguished from pre-existing issues)
- **Wonder**: Socratic questioning of process assumptions ("What haven't we tested?")

### Safety Rails

Prevents the agent from weakening its own quality standards:

- Cannot lower Definition of Done levels
- Cannot remove Proactive Work tiers
- Cannot extend RETRO intervals
- All three require explicit human approval to change

## License

MIT
