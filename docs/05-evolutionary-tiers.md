# Evolutionary Tiers: T1–T5 (and beyond)

Building on the BIOISO framework (Ghiringhelli, 2026) and DarwinNet's dual-loop architecture.

## The ladder

Each tier adds exactly one primitive the tier below cannot express.

### T1 — Fixed-rule dispatch

**What it does**: Static routing. Deterministic edges. No model calls in control flow.

**Biological analog**: Structural proteins (collagen, keratin) — they do their job without regulation.

**Agent analog**: Hardcoded if-else pipelines, YAML workflows with no LLM branches. A CI/CD pipeline.

**Examples**: Traditional workflow engines (Prefect, Temporal for deterministic DAGs).

### T2 — Stochastic search / loop engineering

**What it adds**: An agent loop with a model deciding the next action. The scheduler has `|U| <= 1` (one active unit, arXiv:2604.11378).

**Biological analog**: A single transcription unit — RNA polymerase runs along DNA producing one transcript.

**Agent analog**: ReAct loop, Claude Code / Codex CLI / OpenCode — one agent, one loop, tools, verifier.

**Examples**: Most current coding agents (2025-26).

### T3 — Hyper-heuristic selection / graph engineering

**What it adds**: Multiple specialized agents (nodes) coordinated through explicit edges. The scheduler has `|U| >= 1` (parallel ready set).

**Biological analog**: A gene regulatory network — multiple transcription units coordinated by regulatory signals.

**Agent analog**: Org Graph + Work Graph. LangGraph, ADK, AutoGen GraphFlow.

**Examples**: Multi-agent systems with role specialization (2026+).

### T4 — Surrogate-model optimization / self-sensing

**What it adds**: The graph monitors its own performance and adjusts node parameters (not topology) based on a learned model of what works.

**Biological analog**: Epigenetic regulation — histone modifications, DNA methylation that change expression patterns without changing the genome.

**Agent analog**: Auto-tuning of prompts, temperature, tool selection, retry strategies based on accumulated execution history.

**Examples**: DSPy optimizers, auto-prompt tuning.

### T5 — Structural self-modification / self-rewriting graph

**What it adds**: The graph modifies its own topology — adding, removing, or rewiring nodes and edges based on evolutionary pressure.

**Biological analog**: Evolution by natural selection + horizontal gene transfer — the genome itself changes across generations.

**Agent analog**: An agent system that, after a task, reflects on its architecture and generates a new, improved version of itself for the next task.

**Examples**: BIOISO's meiosis mechanism, MorphoAgent's 25-gene regulatory network for role differentiation.

## Beyond T5: Open frontiers

| Tier | What it adds | Biological analog | Status |
|------|-------------|-------------------|--------|
| T6 | Meta-telos: the system chooses its own objectives | Consciousness? | Pure theory |
| T6' | Harness evolution: the runtime itself evolves | Ecosystem selection | Speculative |
| T7 | Substrate independence: cross-platform migration | Horizontal transfer across kingdoms | Speculative |

## The DarwinNet connection

DarwinNet (arXiv:2604.01236) implements a tri-layered architecture that maps cleanly:

| DarwinNet layer | Function | T-level |
|----------------|----------|---------|
| L0 (Physical Anchor) | Immutable constraints | T1 |
| L1 (Fluid Cortex) | WASM-based fast-path execution | T2–T3 |
| L2 (Darwin Cortex) | LLM-driven slow-path synthesis | T4–T5 |

Their **Intent-to-Bytecode (I2B)** mechanism with dual-loop architecture (outer for cognitive synthesis, inner for hot-swap) is a practical implementation of T4→T5: the system evolves its own protocol logic at runtime.

The **Protocol Solidification Index (PSI)** measures how far a protocol has "solidified" from slow reasoning (System 2) to fast execution (System 1) — a metric for evolutionary maturity.

## How a skill harness bridges tiers

A skill harness like opencode or Claude Code sits at T2 currently. By adding:
- Explicit state schema (T3)
- Execution history analysis for auto-tuning (T4)
- Post-hoc graph rewriting based on reflection (T5)

...it can climb the tiers without changing the runtime. The skill definition IS the genome.