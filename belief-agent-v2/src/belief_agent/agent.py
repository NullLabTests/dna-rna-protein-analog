from __future__ import annotations

import json
from typing import Any, Callable

from belief_agent.state import BeliefState


Message = dict[str, str]  # {"role": ..., "content": ...}


class BeliefAgent:
    """Model-agnostic agent wrapper that maintains explicit belief states.

    The caller provides a ``llm_call`` function that accepts a list of
    messages and returns a string.  This lets ``BeliefAgent`` work with
    *any* LLM provider (OpenAI, Anthropic, DeepSeek, local models, …).
    """

    def __init__(
        self,
        llm_call: Callable[[list[Message]], str],
        system_prompt: str | None = None,
        name: str = "agent",
        max_history: int = 100,
    ) -> None:
        self.llm_call = llm_call
        self.name = name
        self.system_prompt = system_prompt
        self.beliefs: dict[str, BeliefState] = {}
        self.history: list[Message] = []
        self.max_history = max_history

    # ---- core interaction ----

    def __call__(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})
        self._trim_history()
        reply = self._generate()
        self.history.append({"role": "assistant", "content": reply})
        self._update_beliefs_from(reply)
        return reply

    def _generate(self) -> str:
        messages = self._build_messages()
        return self.llm_call(messages)

    def _build_messages(self) -> list[Message]:
        msgs: list[Message] = []
        if self.system_prompt:
            msgs.append({"role": "system", "content": self.system_prompt})
        # optionally inject belief context
        if self.beliefs:
            ctx = self._belief_context()
            if ctx:
                msgs.append({"role": "system", "content": ctx})
        msgs.extend(self.history)
        return msgs

    # ---- belief injection ----

    def _belief_context(self) -> str:
        if not self.beliefs:
            return ""
        lines = ["<beliefs>"]
        for b in self.beliefs.values():
            status = "confident" if b.is_confident() else "uncertain"
            if b.is_contradicted():
                status = "contradicted"
            lines.append(
                f'  - "{b.proposition}" confidence={b.confidence:.2f} [{status}]'
            )
        lines.append("</beliefs>")
        return "\n".join(lines)

    # ---- belief management ----

    def adopt(self, belief: BeliefState) -> None:
        key = belief.proposition
        if key in self.beliefs:
            self.beliefs[key] = self.beliefs[key].merge(belief)
        else:
            self.beliefs[key] = belief

    def update_belief(self, proposition: str, **kwargs: Any) -> BeliefState | None:
        if proposition not in self.beliefs:
            return None
        b = self.beliefs[proposition]
        updated = BeliefState(
            proposition=b.proposition,
            confidence=kwargs.get("confidence", b.confidence),
            contradictions=kwargs.get("contradictions", b.contradictions),
            evidence=kwargs.get("evidence", b.evidence),
            source=kwargs.get("source", b.source),
            metadata=kwargs.get("metadata", b.metadata),
        )
        self.beliefs[proposition] = updated
        return updated

    def get_belief(self, proposition: str) -> BeliefState | None:
        return self.beliefs.get(proposition)

    def remove_belief(self, proposition: str) -> bool:
        return self.beliefs.pop(proposition, None) is not None

    def list_beliefs(
        self, min_confidence: float = 0.0, only_contradicted: bool = False
    ) -> list[BeliefState]:
        result = list(self.beliefs.values())
        if only_contradicted:
            result = [b for b in result if b.is_contradicted()]
        if min_confidence > 0.0:
            result = [b for b in result if b.confidence >= min_confidence]
        return result

    # ---- automatic belief extraction ----

    def _update_beliefs_from(self, reply: str) -> None:
        """Parse structured belief annotations from the LLM reply."""
        try:
            data = json.loads(reply)
            if not isinstance(data, list):
                data = [data]
            for item in data:
                if "proposition" in item:
                    self.adopt(BeliefState.from_dict(item))
        except (json.JSONDecodeError, KeyError):
            pass

    # ---- reflection hook ----

    def reflect(self) -> str:
        """Ask the agent to reflect on its own beliefs."""
        msg = (
            "Reflect on your current beliefs. For each belief, state whether "
            "you still hold it, whether you have found contradictions, and "
            "what your updated confidence level is. Return as JSON: "
            '[{"proposition":"...","confidence":0.X,"contradictions":[...],"evidence":[...]}]'
        )
        self.history.append({"role": "user", "content": msg})
        reply = self._generate()
        self.history.append({"role": "assistant", "content": reply})
        self._update_beliefs_from(reply)
        return reply

    # ---- negotiation hook ----

    def negotiate(self, other_agent: BeliefAgent, issue: str) -> str:
        """Two-agent negotiation over a shared issue."""
        prompt = (
            f"You are negotiating with {other_agent.name} about: {issue}. "
            "State your position, your underlying goal, and a possible compromise. "
            f"Your current beliefs: {self._belief_context()}"
        )
        self.history.append({"role": "user", "content": prompt})
        reply = self._generate()
        self.history.append({"role": "assistant", "content": reply})
        self._update_beliefs_from(reply)
        return reply

    # ---- history ----

    def _trim_history(self) -> None:
        while len(self.history) > self.max_history:
            self.history.pop(0)

    def reset_history(self) -> None:
        self.history.clear()

    # ---- serialization ----

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "system_prompt": self.system_prompt,
            "beliefs": {k: v.to_dict() for k, v in self.beliefs.items()},
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)
