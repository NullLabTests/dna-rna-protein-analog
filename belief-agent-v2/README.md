# Belief-Agent v2

**Add explicit belief states, structured reflection loops, and human negotiation to any LLM agent.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

Belief-Agent is a lightweight Python framework that wraps any LLM (OpenAI, Anthropic, DeepSeek, local models, …) with a **belief state** that tracks confidence, evidence, and contradictions. It adds **structured reflection** (self-critique loops) and **multi-agent negotiation** (goal ranking, tradeoffs, compromises) — all with optional human-in-the-loop.

## Architecture

```
┌───────────────────────────────────────────────────────────┐
│                     BeliefAgent                           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Belief State Map  (proposition → BeliefState)      │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │Proposition│  │Proposition│  │Proposition│        │  │
│  │  │Confidence │  │Confidence │  │Confidence │        │  │
│  │  │Evidence[] │  │Evidence[] │  │Evidence[] │        │  │
│  │  │Contradict.│  │Contradict.│  │Contradict.│        │  │
│  │  └──────────┘  └──────────┘  └──────────┘          │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │  LLM Call    │  │  Reflection  │  │  Negotiation     │ │
│  │  (any model) │  │  (critique)  │  │  (ranking/trade) │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
└───────────────────────────────────────────────────────────┘
```

## Quick Start

```python
from belief_agent import BeliefAgent, BeliefState
from belief_agent.reflection import reflect
from belief_agent.negotiation import Goal, negotiate

# 1. Wrap any LLM
def my_llm(messages):
    # calls OpenAI / Anthropic / DeepSeek / etc.
    return "...response..."

agent = BeliefAgent(llm_call=my_llm, name="my-agent")

# 2. Adopt beliefs
agent.adopt(BeliefState("AGI is 10 years away", confidence=0.6))

# 3. Interact
reply = agent("What do you think about AI timelines?")

# 4. Reflect
reflect(agent, my_llm, depth=2)

# 5. Negotiate with another agent
other = BeliefAgent(llm_call=my_llm, name="other")
goals = [Goal("Accuracy"), Goal("Speed")]
result = negotiate([agent, other], "Model choice", goals, my_llm)
```

## Features

### BeliefState
| Method | Description |
|--------|-------------|
| `merge(other)` | Combine two beliefs on the same proposition |
| `contradict(stmt)` | Add a contradiction, halving confidence |
| `support(evidence)` | Add supporting evidence (+0.1 confidence) |
| `to_dict()` / `from_dict()` | Serialize to/from dict |
| `to_json()` / `from_json()` | Serialize to/from JSON |
| `is_confident(threshold=0.7)` | Check if confidence ≥ threshold |
| `is_contradicted()` | Check if has contradictions |

### BeliefAgent
| Method | Description |
|--------|-------------|
| `adopt(belief)` | Add or merge a belief |
| `update_belief(prop, **kw)` | Update belief attributes |
| `get_belief(prop)` | Get belief by proposition |
| `remove_belief(prop)` | Remove a belief |
| `list_beliefs(min_conf, only_contradicted)` | Filtered listing |
| `reflect()` | Ask agent to reflect on its own beliefs |
| `negotiate(other_agent, issue)` | Two-agent negotiation |

### Reflection
| Function | Description |
|----------|-------------|
| `reflect(agent, llm, depth)` | Structured self-critique loop |
| `auto_update(agent, llm, threshold)` | Reflect on low-confidence only |
| `human_review(result, feedback, accepted)` | Override with human judgment |

### Negotiation
| Function | Description |
|----------|-------------|
| `rank_goals(goals, llm)` | Sort goals by priority |
| `negotiate(agents, issue, goals, llm)` | Multi-agent consensus |
| `find_tradeoffs(agent, goal_a, goal_b, llm)` | Identify tradeoffs |
| `suggest_compromise(proposals, llm)` | Generate compromise |

## Comparison: Vanilla Agent vs Belief-Agent

| Aspect | Vanilla Agent | Belief-Agent |
|--------|--------------|--------------|
| State | Ephemeral chat history | Explicit belief map |
| Confidence | None | 0.0–1.0 per belief |
| Contradictions | Lost / overwritten | Tracked explicitly |
| Reflection | None (or manual) | Structured self-critique |
| Human feedback | Hard to inject | `human_review()` hook |
| Multi-agent | Ad-hoc prompting | `negotiate()` with goals, tradeoffs, consensus |
| Serialization | None | JSON round-trip |
| Model support | Provider-specific | Model-agnostic (`llm_call`) |

## Examples

- `examples/basic_usage.py` — manual adoption, interaction, serialization
- `examples/reflection_loop.py` — structured reflection with human override
- `examples/negotiation_demo.py` — two agents negotiate an architecture decision

## Notebooks

| Notebook | Description |
|----------|-------------|
| `notebooks/01_basic_usage.ipynb` | Core data model and agent wrapper |
| `notebooks/02_reflection_in_action.ipynb` | Reflection loops and auto-update |
| `notebooks/03_negotiation_scenarios.ipynb` | Goal ranking, tradeoffs, compromise |
| `notebooks/04_advanced_multi_agent.ipynb` | Combined multi-agent workflow |

## Installation

```bash
pip install belief-agent
```

For development:

```bash
git clone https://github.com/anomalyco/belief-agent
cd belief-agent
pip install -e ".[dev]"
```

## Testing

```bash
pytest tests/ -v
```

## License

MIT
