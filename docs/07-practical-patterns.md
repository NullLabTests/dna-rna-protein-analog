# Practical Patterns: What Works, What Lasts

This document extracts actionable patterns from the polymer framework — things you can apply today to get better, longer-lasting results from AI agents.

## Pattern 1: The Three-Layer Check

Before starting any multi-step agent task, explicitly separate:

```
DNA (fixed):    What tools, configs, and knowledge are invariant?
RNA (transient): What context needs to flow through the session?
Protein (output): What concrete artifact must be produced?
```

**Why it works**: It prevents the agent from modifying its own genome mid-execution (the source of drift), forces context budgeting (the source of context-bleed failures), and clarifies the stopping condition (output is done).

## Pattern 2: Exonuclease Verification

Insert a verification step after EVERY critical node in the graph:

```
Agent produces output → Verifier checks output → 
  PASS → continue
  FAIL → retry with error context (max N times)
  FAIL after N → escalate to human
```

**Biological analog**: DNA Polymerase III has 3'→5' exonuclease activity — it proofreads each nucleotide as it's added, correcting ~99% of errors in real-time.

**Implementation**: A `guard` node in LangGraph, a `verifier` step in your loop, or a `reviewer_gate` from operon-ai.

**Why it works**: Catches errors when they're cheapest to fix (immediately) vs. after downstream work has been built on a bad foundation.

## Pattern 3: Org Graph / Work Graph Separation

Never collapse your agent system into one graph. Maintain two:

```
Org Graph: Who owns what domain (long-lived, stable)
  - Researcher: owns domain knowledge
  - Builder: owns code generation
  - Validator: owns testing
  - Publisher: owns deployment

Work Graph: What needs doing now (per-task, ephemeral)
  - Plan → Research → Build → Test → Review → Deploy
  - Edges split/merge based on evidence
```

**Why it works**: The Org Graph gives specialization (each agent accumulates deep context in its domain). The Work Graph gives flexibility (task routing adapts to actual progress, not a rigid plan).

## Pattern 4: The Morphogen Budget

For each agent in the graph, define a resource budget that degrades with "distance" from the task origin:

```python
class MorphogenBudget:
    max_tokens_per_node: dict
    max_calls_per_tool: dict
    decay_factor_per_handoff: float = 0.8
    
    def budget_for(self, node, hop_distance):
        return self.max_tokens_per_node[node] * (decay_factor ** hop_distance)
```

**Why it works**: Prevents runaway resource consumption in deep graphs. Each handoff reduces the remaining budget, naturally limiting cascade depth.

## Pattern 5: The Feed-Forward Approval Gate

For any high-stakes output, use the C1-FFL motif:

```
Generator (X) produces candidate output
Verifier (Y) independently evaluates candidate
FINAL OUTPUT (Z) = X AND Y  # both must approve
```

**Error suppression**: If generator has error rate `e_X` and verifier has error rate `e_Y`, the combined error is `e_X * e_Y` — assuming independent failure modes.

**Implementation**: `reviewer_gate` in operon-ai, or a LangGraph conditional edge requiring two node outputs.

## Pattern 6: The Weismann Barrier

Never let execution-level output modify system-level configuration without explicit human approval.

```
Execution (protein) → logs only → human reviews → 
  APPROVED → config change possible
  REJECTED → no change
```

**Why it works**: Presents the biological Weismann barrier — acquired characteristics of the "organism" (session outputs) should not rewrite the "genome" (config, tools, prompts) without a selection gate. Violating this is how agents drift over time.

## Pattern 7: Generational Improvement Loop

After every complete run (a "generation"), run a meta-review:

```
1. Collect execution trace (the RNA transcript)
2. Identify failure modes (mutations)
3. Classify each as:
   a. Stochastic (model randomness) — ignore
   b. Structural (bad topology) — rewire the graph
   c. Config (bad tool/prompt) — update the genome
4. Apply fixes before next run
```

**Why it works**: This is natural selection applied to agent architecture. Each generation selects against structural and config errors, converging on a more robust system.

## Pattern 8: Antigenic Variation for Robustness

Rotate through multiple equivalent implementations of critical nodes:

```
Routing node: round-robin between 3 equivalent summarizers
Tool node: try API-A, fallback to API-B, fallback to local model
Verifier node: swap between regex, LLM-judge, and formal proof
```

**Why it works**: Biological pathogens use antigenic variation to evade immune detection. Similarly, using diverse implementations for critical functions prevents systemic failure from any single component's weakness. This is the agent analog of N-version programming.

## Pattern 9: Checkpoint as Synaptic Consolidation

At every edge crossing in a graph, save full state:

```python
checkpoint = {
    "node_id": current_node,
    "inputs": {k: v for k, v in inputs.items()},
    "output": output,
    "edge_to": next_node,
    "budget_remaining": budget,
    "timestamp": now()
}
```

**Why it works**: This converts short-term (context-window) memory into long-term (checkpointed) memory — the analog of synaptic consolidation in neuroscience. It enables:
- Resumability: crash at node 40 of 60; restart at node 40, not node 0
- Audit: trace exactly which input produced which output at which step
- Debug: replay a specific node with the same inputs to test changes

## Pattern 10: The Ribosome Abstraction

Treat your LLM call as a ribosome — a universal translation machine that reads one language (prompts + context) and produces another (output). This abstraction means:

- The "genetic code" (tokenization → meaning mapping) is handled by the model
- The "codon table" (prompt → response patterns) is learned, not hardcoded
- "Post-translational modification" (output parsing, validation) is separate from translation

**Practical rule**: Never put parsing logic inside the prompt. Keep the LLM as a pure translator; add structured parsing as a downstream node.

## Summary table

| Pattern | Biological analog | When to use | Complexity |
|---------|------------------|-------------|------------|
| 3-layer check | Central dogma | Always | Trivial |
| Exonuclease verification | DNA proofreading | Production systems | Low |
| Org/Work graph separation | Cell differentiation | Multi-agent | Medium |
| Morphogen budget | Developmental gradient | Deep graphs | Medium |
| Feed-forward approval | C1-FFL motif | High-stakes output | Low |
| Weismann barrier | Germline separation | Long-running agents | Low |
| Generational improvement | Evolution | Repeated tasks | High |
| Antigenic variation | Immune evasion | Critical nodes | Medium |
| Synaptic consolidation | Memory formation | Long sessions | Medium |
| Ribosome abstraction | Translation | LLM integration | Low |