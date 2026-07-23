# Biological Motifs → Agent Patterns

Based on arXiv:2607.04240 ("Biological Motifs for Agentic Control") and the broader gene-regulatory-network (GRN) literature.

## Motif 1: Coherent Feed-Forward Loop (C1-FFL)

**Biology**: A transcription factor X activates Y, and both X and Y activate Z (AND gate). This filters out transient signal pulses — only persistent input triggers output.

**Agent analog**: A generator agent (X) produces candidate output, a verifier agent (Y) independently checks it, and the result (Z) fires only if both agree. This is **redundant verification** or "two-person rule."

**Error suppression**: Under independent error rates `e_X`, `e_Y`, the joint error is `e_X * e_Y` — multiplicative suppression. This is the formal basis for reviewer-gate patterns.

**Implementation**: `reviewer_gate` in operon-ai, or a LangGraph node with conditional edge requiring two approvals.

## Motif 2: Negative Autoregulation (NAR)

**Biology**: A transcription factor represses its own production. This speeds up response time and stabilizes expression levels.

**Agent analog**: An agent that self-limits its own iterations — a "done check" that short-circuits further looping when a quality threshold is met.

**Implementation**: The termination oracle in λ_A's ReAct rule. A verifier that returns "done" before the budget is exhausted.

## Motif 3: Adaptive Immunity (Layered Defense)

**Biology**: Innate (fast, pattern-based) + adaptive (slow, specific) immune responses. The adaptive system remembers pathogens for faster future response.

**Agent analog**: A two-layer guard system:
- **Innate**: syntactic checks, schema validation, blocklist matching (fast, no LLM call)
- **Adaptive**: semantic verification, prompt-injection detection (slow, LLM-based)

**Memory**: Blocked attack patterns are stored for future innate-level blocking.

## Motif 4: Mitochondrial Signaling (Resource Governance)

**Biology**: Mitochondria produce ATP and signal cellular stress. When energy is low, they trigger AMPK signaling that downregulates anabolic processes.

**Agent analog**: A token/resource budget monitor that:
- Tracks cumulative spend across all nodes in the graph
- Signals when approaching limits
- Downregulates expensive operations (long context, many tool calls)
- Can abort or degrade gracefully

**Implementation**: Budget in the shared graph state, checked on every edge crossing.

## Motif 5: Endosymbiosis (Neuro-Symbolic Integration)

**Biology**: Mitochondria were once free-living bacteria that became incorporated into eukaryotic cells. They retain their own DNA and replicate independently.

**Agent analog**: A symbolic reasoning engine (constraint solver, theorem prover, database) embedded within an LLM agent system. It retains its own "genome" (rules, facts) and operates semi-independently.

**Implementation**: A `symbolic` tool that the LLM calls but cannot modify. The symbolic engine's state persists across sessions.

## Motif 6: Morphogen Diffusion (Spatial Coordination)

**Biology**: Morphogens (BMP, Shh, Wnt) diffuse across developing tissue, forming concentration gradients that determine cell fate based on position.

**Agent analog**: Spatial or contextual signals that degrade with "distance" in the agent system:
- Information decay across handoffs (each edge loses fidelity)
- Priority gradients (high-priority tasks recruit more resources)
- Role differentiation based on "position" in the processing pipeline

## Motif 7: Lateral Inhibition (Role Differentiation)

**Biology**: Notch-Delta signaling between neighboring cells amplifies small initial differences into binary cell fates (e.g., neuron vs. support cell).

**Agent analog**: When two agents could handle the same task, a competitive signal amplifies the better-suited one and inhibits the other. This is dynamic role assignment without a central scheduler.

## Motif 8: Quorum Sensing (Scalable Coordination)

**Biology**: Bacteria release autoinducer molecules. When concentration crosses a threshold, the entire population simultaneously changes behavior (biofilm formation, bioluminescence).

**Agent analog**: When the number of active agents / pending tasks crosses a threshold, the system switches coordination modes:
- Below threshold: direct communication
- Above threshold: hierarchical routing, gossip protocol

## Implementation notes

These motifs compose. A single graph can simultaneously use:
- C1-FFL for verification (motif 1)
- NAR for self-limiting loops (motif 2)
- Adaptive immunity for safety (motif 3)
- Mitochondrial signaling for budget (motif 4)

See `operon-ai` library for reference implementations of these patterns.