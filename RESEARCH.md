# polymer — Research Scaffold

This document frames polymer as a research program: testable hypotheses, experimental protocols, and open problems at the intersection of computational biology, agent architecture, and software evolution.

## Research questions

### Q1: Is the central dogma a valid predictive model for agent architecture?

**Hypothesis**: The central dogma's information-flow constraints predict failure modes in agent systems. Systems that violate the directionality (e.g., allowing output to directly rewrite config without verification) will show higher drift rates.

**Experiment**: Build two versions of a multi-step agent — one that respects the DNA→RNA→Protein barrier (no output→config feedback without human gate), one that allows direct feedback. Run 100 tasks each. Measure task completion rate, output consistency, and config drift.

### Q2: Does the C1-FFL motif suppress agent errors multiplicatively?

**Hypothesis**: A generator-verifier pair (C1-FFL) reduces error as `e_X * e_Y` when failure modes are independent, vs. `e_X + e_Y` for sequential processing.

**Experiment**: Vary the independence of generator and verifier (same model, different models, different modalities). Measure error rates for each configuration. Compare to the predicted multiplicative suppression.

### Q3: Do graph-engineered systems outlast loop-engineered systems?

**Hypothesis**: Over repeated task executions (generations), systems with explicit graph topology converge faster and drift less than single-loop systems.

**Experiment**: Deploy a loop system and a graph system (LangGraph or ADK) for the same task category. Measure per-generation: token cost, wall-clock time, success rate, and config drift. Run for 50+ generations.

### Q4: Can agent systems evolve their own topology?

**Hypothesis**: An agent system with a meta-critic that rewrites its own graph structure (BIOISO T5) will outperform fixed-topology systems on tasks with variable structure.

**Experiment**: Create a dynamic graph system that, after each task, proposes a structural modification (add node, remove node, rewire edge). Compare to a fixed-graph baseline on a mixed task set.

### Q5: Is there a "genetic code" for agent composition?

**Hypothesis**: Agent composition patterns (sequence, parallel, verification, fan-out, etc.) can be mapped to a finite alphabet analogous to the genetic code. If so, composition errors follow predictable patterns.

**Experiment**: Analyze real-world agent configs (like the 835 in arXiv:2604.11767) for recurring composition patterns. Check if pattern frequencies follow a Zipf distribution (evidence of a finite-element ontology).

## Experimental protocol template

```
1. Define the task family (N tasks, known ground truth)
2. Define the graph architecture (nodes, edges, state schema)
3. Define metrics:
   - Token cost per task
   - Wall-clock time per task
   - Success rate (pass/fail against ground truth)
   - Structural stability (does config change between runs?)
   - Error type distribution (hallucination, loop, refusal, etc.)
4. Run N iterations (N >= 30 for statistical power)
5. Log complete execution traces
6. Analyze: which errors are structural (graph topology) vs. stochastic (model)?
```

## Key references for research direction

| Paper | Key idea | Connection to polymer |
|-------|----------|----------------------|
| arXiv:2607.04240 | Biological motifs as typed interfaces | Formalizes C1-FFL, adaptive immunity motifs for agents |
| arXiv:2604.11767 | λ_A — unifying agent calculus | Gives formal semantics to the "translation" step |
| arXiv:2602.20064 | LLMbda — info flow for agents | Formalizes the Weismann barrier (information-flow control) |
| arXiv:2604.11378 | Agent loops as single-ready schedulers | Formalizes the loop→graph transition |
| BIOISO (Ghiringhelli) | T1–T5 evolutionary tiers | Gives the ladder for evolutionary complexity |
| MorphoAgent (Feng, Chang) | Drosophila development as agent architecture | Proof that whole-organism biology maps to agents |
| DarwinNet | Self-evolving network protocols | Shows T5 evolution works in practice |
| operon-ai | Reference implementations of biological motifs | Production code for motifs 1-7 |
| Software Periodic Table | 115-element ontology of software atoms | The "amino acids" of software composition |

## Publication targets

- Position paper: "Biology's Central Dogma as a Formal Model for Agent Architecture" — suitable for a workshop or arXiv
- Empirical study: "Feed-Forward Verification Motifs Suppress Agent Errors Multiplicatively" — experimental results
- System paper: "Polymer: A Bio-Inspired Harness for Self-Evolving Agent Graphs" — implementation + evaluation