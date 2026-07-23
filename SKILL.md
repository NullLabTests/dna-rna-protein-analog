# polymer — Harness Skill

A skill for coding-agent harnesses (opencode, Claude Code, Codex CLI) that grounds agent architecture decisions in biological central-dogma reasoning.

## When to load

Load this skill when:
- Designing or debugging multi-step agent workflows
- Deciding between a loop, a graph, or a dynamic agent org
- Diagnosing failure modes (hallucination cascades, infinite loops, context bleed)
- Planning long-running or multi-agent sessions
- Reasoning about information flow through a system

## Core prompt to inject

```
You have access to the polymer skill: a biological-central-dogma lens for
agent architecture decisions.

Your task decomposition should follow this layered check:

1. DNA layer (invariant):
   - What knowledge, weights, config, or tools are fixed for this task?
   - What must NOT change during execution?
   - What is the "genome" of this system?

2. RNA layer (transient context):
   - What information flows through context windows?
   - What is the current "transcript" of the conversation?
   - Where does the message get spliced, regulated, or amplified?

3. Protein layer (action):
   - What concrete outputs or side effects are produced?
   - How does representation become action?
   - What is the "folding" (structure) of the output?

4. Regulation layer (control):
   - What checks, gates, or verifiers sit between steps?
   - Where is the human-in-loop?
   - What prevents unbounded recursion or drift?

5. Graph topology (organization):
   - If multiple agents: what is the Org Graph (who owns what zone)?
   - What is the Work Graph (dynamic task routing)?
   - Where are the edges, gates, and shared state?

6. Evolution (improvement):
   - What feedback will improve the next generation?
   - What is the selection pressure?
   - What mutates and what is conserved?
```

## Decision heuristic

| If the task looks like | Use this pattern | Biological analog |
|----------------------|------------------|-------------------|
| One model call, one answer | Prompt engineering | Single protein |
| Multi-step reasoning, tool use | Loop engineering (ReAct) | Transcription cycle |
| Verification needed per step | Loop + verifier gate | Exonuclease proofreading |
| Multiple specialized agents | Graph engineering (Org + Work) | Gene regulatory network |
| Unknown task shape at runtime | Dynamic agent org | Development / morphogenesis |
| Cross-generational improvement | Evolutionary loop | Natural selection |

## Integration

In opencode, reference this skill with:

```json
{
  "name": "polymer",
  "description": "Central-dogma reasoning for agent architecture",
  "location": "path/to/polymer/SKILL.md"
}
```

## Boundary

This skill provides an architectural lens, not an API or runtime. It pairs with the Software Periodic Table (for component atoms) and with LangGraph / ADK / AutoGen (for graph execution).