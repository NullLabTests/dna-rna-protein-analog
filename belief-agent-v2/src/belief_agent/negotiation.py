from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable

from belief_agent.state import BeliefState


Message = dict[str, str]


@dataclass
class Goal:
    description: str
    priority: float = 1.0  # 0.0 (low) – 1.0 (critical)
    constraints: list[str] = field(default_factory=list)
    tradeoffs: list[str] = field(default_factory=list)


@dataclass
class NegotiationProposal:
    goal: Goal
    proposed_action: str
    estimated_satisfaction: float  # 0.0 – 1.0
    tradeoffs: list[str] = field(default_factory=list)


@dataclass
class NegotiationResult:
    issue: str
    proposals: list[NegotiationProposal] = field(default_factory=list)
    consensus_action: str | None = None
    consensus_satisfaction: float = 0.0
    unresolved_goals: list[str] = field(default_factory=list)


def rank_goals(
    goals: list[Goal],
    llm_call: Callable[[list[Message]], str] | None = None,
) -> list[Goal]:
    """Return goals sorted by priority (highest first)."""
    if llm_call:
        prompt = (
            "Rank the following goals by importance (1 = most important).\n"
            + "\n".join(f'  {i}. "{g.description}" (priority={g.priority})' for i, g in enumerate(goals))
            + '\n\nReturn as JSON array: [{"index":0,"rank":1}, ...]'
        )
        raw = llm_call([{"role": "user", "content": prompt}])
        try:
            data = json.loads(raw)
            if not isinstance(data, list):
                raise TypeError("expected JSON array")
            indices = {item["index"]: item["rank"] for item in data}
            return sorted(goals, key=lambda g: indices.get(goals.index(g), 999))
        except (json.JSONDecodeError, KeyError):
            pass
    return sorted(goals, key=lambda g: g.priority, reverse=True)


def negotiate(
    agents: list[Any],
    issue: str,
    goals: list[Goal],
    llm_call: Callable[[list[Message]], str],
    max_rounds: int = 3,
) -> NegotiationResult:
    """Multi-agent negotiation to resolve conflicting goals.

    Parameters
    ----------
    agents : list[BeliefAgent]
    issue : str
    goals : list[Goal]
        Shared list of goals; each agent may hold different priorities.
    llm_call : Callable
    max_rounds : int

    Returns
    -------
    NegotiationResult
    """
    ranked = rank_goals(goals, llm_call)
    result = NegotiationResult(issue=issue)

    for round_num in range(1, max_rounds + 1):
        proposals: list[NegotiationProposal] = []

        for agent in agents:
            prompt = (
                f"Negotiation round {round_num}/{max_rounds} on: {issue}\n\n"
                f"Your name: {agent.name}\n\n"
                "Goals (ranked by priority):\n"
                + "\n".join(
                    f'  {i+1}. "{g.description}" (priority={g.priority})'
                    for i, g in enumerate(ranked)
                )
                + "\n\n"
                + f"Your current beliefs: {agent._belief_context()}\n\n"
                "Propose an action that satisfies as many high-priority "
                "goals as possible, with tradeoffs noted.\n"
                "Return as JSON: "
                '{"goal_index":0,"action":"...","satisfaction":0.X,"tradeoffs":["..."]}'
            )
            raw = agent.llm_call([{"role": "user", "content": prompt}])
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue

            gi = data.get("goal_index", 0)
            goal = ranked[gi] if gi < len(ranked) else ranked[0]
            proposals.append(
                NegotiationProposal(
                    goal=goal,
                    proposed_action=data.get("action", ""),
                    estimated_satisfaction=data.get("satisfaction", 0.5),
                    tradeoffs=data.get("tradeoffs", []),
                )
            )

        # consensus: pick proposal with highest average satisfaction
        if proposals:
            best = max(proposals, key=lambda p: p.estimated_satisfaction)
            result.proposals = proposals
            result.consensus_action = best.proposed_action
            result.consensus_satisfaction = best.estimated_satisfaction

        # check for early consensus
        if result.consensus_satisfaction >= 0.8:
            break

    # identify unresolved goals
    if result.consensus_action:
        resolved = {p.goal.description for p in result.proposals}
        for g in ranked:
            if g.description not in resolved:
                result.unresolved_goals.append(g.description)

    return result


def find_tradeoffs(
    agent: Any,
    goal_a: Goal,
    goal_b: Goal,
    llm_call: Callable[[list[Message]], str],
) -> list[str]:
    """Find tradeoffs between two conflicting goals."""
    prompt = (
        f"Find tradeoffs between these two goals:\n\n"
        f'Goal A: "{goal_a.description}" (priority={goal_a.priority})\n'
        f'Goal B: "{goal_b.description}" (priority={goal_b.priority})\n\n'
        "Suggest specific tradeoffs that could partially satisfy both.\n"
        'Return as JSON: {"tradeoffs":["...","..."]}'
    )
    raw = llm_call([{"role": "user", "content": prompt}])
    try:
        data = json.loads(raw)
        return data.get("tradeoffs", [])
    except json.JSONDecodeError:
        return []


def suggest_compromise(
    proposals: list[NegotiationProposal],
    llm_call: Callable[[list[Message]], str],
) -> str | None:
    """Suggest a compromise from a set of proposals."""
    prompt = (
        "Given these negotiation proposals, suggest a compromise that "
        "combines elements from each:\n\n"
        + "\n".join(
            f'  - Goal: "{p.goal.description}", Action: "{p.proposed_action}", '
            f"Satisfaction: {p.estimated_satisfaction:.2f}, Tradeoffs: {p.tradeoffs}"
            for p in proposals
        )
        + '\n\nReturn as JSON: {"compromise":"..."}'
    )
    raw = llm_call([{"role": "user", "content": prompt}])
    try:
        data = json.loads(raw)
        return data.get("compromise")
    except json.JSONDecodeError:
        return None
