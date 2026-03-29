<p align="right">
  <strong>English</strong> | <a href="./README.ko.md">한국어</a>
</p>

<h1 align="center">
  <code>tars</code>
</h1>

<p align="center">
  <a href="https://github.com/steadymoka/tars/releases"><img src="https://img.shields.io/badge/version-0.3.0-818cf8?style=flat-square" alt="version" /></a>
  <a href="https://github.com/steadymoka/tars/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-38bdf8?style=flat-square" alt="license" /></a>
  <img src="https://img.shields.io/badge/platform-Claude_Code-6366f1?style=flat-square" alt="platform" />
</p>

<p align="center">
  Autonomous agent orchestration plugin for Claude Code.<br/>
  The agent self-governs through a <code>.tars/</code> protocol and evolves its own process over time.
</p>

## Install

```
/plugin marketplace add steadymoka/tars
/plugin install tars@steadymoka-tars
```

## Quick Start

```
/tars:init                       # scaffold .tars/, choose core & execution mode
/tars:heartbeat                  # run one autonomous cycle
/loop 10m /tars:heartbeat        # auto-repeat every 10 minutes
```

### Autonomous Mode

For fully autonomous operation, start Claude Code with `--dangerously-skip-permissions`:

```bash
claude --dangerously-skip-permissions
```

The `guard.py` hook (installed by `/tars:init`) blocks file modifications **and dangerous Bash commands** outside the project directory, so autonomous operation remains safe within your project scope.

## Skills

| Skill | Description |
|-------|-------------|
| `/tars:init` | Initialize `.tars/` — choose core (dev/design/...) and execution mode (solo/team) |
| `/tars:heartbeat` | Read PROTOCOL.md and execute one autonomous cycle |
| `/tars:status` | Dashboard — heartbeat count, backlog depth, anomaly flags |
| `/tars:retro` | Immediate retrospective — metrics, anomaly detection, protocol improvement proposals |
| `/tars:evolve` | Protocol evolution analysis — patch effectiveness, lateral thinking options |
| `/tars:upgrade` | Upgrade existing `.tars/` to match current plugin version |
| `/tars:team` | Add team agent configuration to an existing solo project |

## Cores

A **core** defines how the agent operates — its protocol, mission template, and definition of done. Cores are the pluggable unit of tars.

### Built-in Cores

| Core | Description |
|------|-------------|
| `dev` | Build verification, code patrol, testing strategy. 3-level DoD (build → functional → integration) |
| `design` | Design iteration, artifact management, feedback loops. Output structure with specs/wireframes/research |

### Community Cores

Adding a community core is as simple as copying a directory:

```
cores/
├── dev/           ← built-in
├── design/        ← built-in
├── research/      ← copy a community core here
│   ├── core.json
│   ├── PROTOCOL.md
│   └── MISSION.md
└── shared/        ← reserved (common templates)
```

A core directory needs 3 files:
- `core.json` — metadata (name, label, description, placeholders)
- `PROTOCOL.md` — heartbeat cycle and operational rules
- `MISSION.md` — mission template with DoD and proactive work tiers

## Execution Modes

### Solo (default)

One agent, one core. The agent follows its core's protocol autonomously.

```
/tars:init → choose core → solo
```

### Team

An orchestrator coordinates multiple specialized agents, each powered by a different core.

```
/tars:init → choose cores → team
```

Team mode creates:
- `.claude/agents/orchestrator.md` — coordinates task distribution
- `.claude/agents/{core}-agent.md` — specialized agent per core
- `.tars/_workspace/` — shared artifact exchange between agents

You can also convert a solo project to team later:

```
/tars:team    # add team agents to an existing solo project
```

## How It Works

```
Heartbeat Cycle (each cycle):
  Read State (no cache) → Process COMMS → CLARIFY if needed → Execute BACKLOG → Write LOG → RETRO Check

Self-Evolution (improvements found in RETRO):
  Stagnation Detection → Oscillation Detection → Regression Detection
  → Wonder Gap Analysis → Protocol Patch apply/propose
```

### .tars/ Structure

```
.tars/
├── COMMS.md         # Human <> Agent communication
├── BACKLOG.md       # Task list (P0~P3 priority)
├── PROGRESS.md      # Current heartbeat count, task state
├── MILESTONES.md    # Mid-term goal checkpoints
├── protocol/
│   ├── MISSION.md   # Mission definition, DoD, Proactive Work
│   ├── PROTOCOL.md  # Autonomous operation protocol (self-evolution target)
│   └── EVOLUTION.md # Protocol change history
├── logs/
│   ├── LOG.md       # Work history
│   ├── RETRO.md     # Retrospective records
│   ├── archive/
│   └── backlog-archive/
├── _workspace/      # Team mode: agent artifact exchange
└── output/          # Design core: specs, wireframes, research
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
- **Regression**: Metrics worsened after a protocol patch
- **Wonder**: Socratic questioning of process assumptions

### Safety Rails

- Cannot lower Definition of Done levels
- Cannot remove Proactive Work tiers
- Cannot extend RETRO intervals
- All three require explicit human approval to change

## Guard Hook

The guard hook (`guard.py`) protects autonomous operation:

- **File writes**: Blocks Write/Edit/NotebookEdit outside the project directory
- **Bash commands**: Blocks dangerous commands (`rm`, `mv`, `cp`, `dd`, etc.) targeting outside the project
- **Destructive git**: Blocks `git reset --hard`, `git push --force`, `git clean -fd`, `git checkout -- .`
- **Redirects**: Blocks `>`, `>>`, `tee` writing to absolute paths outside the project
- **sudo**: Strips sudo prefix to detect the real command underneath

## License

MIT
