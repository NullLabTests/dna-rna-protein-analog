from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from belief_agent.state import BeliefState


Message = dict[str, str]


@dataclass
class ReflectionResult:
    proposition: str
    original_confidence: float
    updated_confidence: float
    critique: str
    new_evidence: list[str] = field(default_factory=list)
    new_contradictions: list[str] = field(default_factory=list)
    accepted: bool = True


def reflect(
    agent: Any,
    llm_call: Callable[[list[Message]], str],
    depth: int = 1,
) -> list[ReflectionResult]:
    """Run structured reflection on an agent's beliefs.

    Parameters
    ----------
    agent : BeliefAgent
        The agent whose beliefs will be reflected upon.
    llm_call : Callable
        A function that takes a list of messages and returns a string.
    depth : int
        Number of reflection iterations (default 1).

    Returns
    -------
    list[ReflectionResult]
        One result per belief per iteration.
    """
    results: list[ReflectionResult] = []
    if depth < 1:
        return results

    for proposition, belief in list(agent.beliefs.items()):
        result = _reflect_on_belief(proposition, belief, llm_call)
        if result.accepted:
            result.accepted = _decide_acceptance(result, llm_call)
        if result.accepted:
            agent.update_belief(
                proposition,
                confidence=result.updated_confidence,
                contradictions=(
                    belief.contradictions + result.new_contradictions
                ),
                evidence=belief.evidence + result.new_evidence,
            )
        results.append(result)

    if depth > 1:
        results.extend(reflect(agent, llm_call, depth=depth - 1))

    return results


def _reflect_on_belief(
    proposition: str,
    belief: BeliefState,
    llm_call: Callable[[list[Message]], str],
) -> ReflectionResult:
    prompt = (
        f"Critique the following belief held with confidence {belief.confidence:.2f}:\n"
        f'  "{proposition}"\n\n'
        f"Evidence:\n"
        + ("\n".join(f"  - {e}" for e in belief.evidence) or "  (none)")
        + "\n\nContradictions:\n"
        + ("\n".join(f"  - {c}" for c in belief.contradictions) or "  (none)")
        + "\n\nProvide:\n"
        "1. A brief critique.\n"
        "2. Any new evidence (one item).\n"
        "3. Any new contradictions (one item).\n"
        "4. An updated confidence (0.0-1.0).\n\n"
        "Return as JSON: "
        '{"critique":"...","new_evidence":["..."],"new_contradictions":["..."],"updated_confidence":0.X}'
    )
    raw = llm_call([{"role": "user", "content": prompt}])
    import json

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return ReflectionResult(
            proposition=proposition,
            original_confidence=belief.confidence,
            updated_confidence=belief.confidence,
            critique="Could not parse LLM reflection output.",
            new_evidence=[],
            new_contradictions=[],
            accepted=False,
        )
    if not isinstance(data, dict):
        return ReflectionResult(
            proposition=proposition,
            original_confidence=belief.confidence,
            updated_confidence=belief.confidence,
            critique="LLM returned non-dict JSON.",
            new_evidence=[],
            new_contradictions=[],
            accepted=False,
        )
    return ReflectionResult(
        proposition=proposition,
        original_confidence=belief.confidence,
        updated_confidence=data.get("updated_confidence", belief.confidence),
        critique=data.get("critique", ""),
        new_evidence=data.get("new_evidence", []),
        new_contradictions=data.get("new_contradictions", []),
    )


def _decide_acceptance(
    result: ReflectionResult,
    llm_call: Callable[[list[Message]], str],
) -> bool:
    prompt = (
        f"Should the following reflection be accepted?\n\n"
        f"Proposition: {result.proposition}\n"
        f"Original confidence: {result.original_confidence:.2f}\n"
        f"Updated confidence: {result.updated_confidence:.2f}\n"
        f"Critique: {result.critique}\n\n"
        'Answer "yes" or "no" as JSON: {"accept": true/false}'
    )
    raw = llm_call([{"role": "user", "content": prompt}])
    import json

    try:
        data = json.loads(raw)
        return data.get("accept", True)
    except (json.JSONDecodeError, KeyError):
        return True


def auto_update(
    agent: Any,
    llm_call: Callable[[list[Message]], str],
    threshold: float = 0.3,
) -> list[ReflectionResult]:
    """Auto-reflect on low-confidence beliefs only."""
    low = {b.proposition for b in agent.list_beliefs() if b.confidence < threshold}
    if not low:
        return []
    results: list[ReflectionResult] = []
    for proposition, belief in list(agent.beliefs.items()):
        if proposition not in low:
            continue
        result = _reflect_on_belief(proposition, belief, llm_call)
        if result.accepted:
            result.accepted = _decide_acceptance(result, llm_call)
        if result.accepted:
            agent.update_belief(
                proposition,
                confidence=result.updated_confidence,
                contradictions=(belief.contradictions + result.new_contradictions),
                evidence=belief.evidence + result.new_evidence,
            )
        results.append(result)
    return results


def human_review(
    result: ReflectionResult,
    human_feedback: str,
    accepted: bool | None = None,
) -> ReflectionResult:
    """Apply human feedback to a reflection result."""
    result.critique += f"\n[Human feedback: {human_feedback}]"
    if accepted is not None:
        result.accepted = accepted
    return result
