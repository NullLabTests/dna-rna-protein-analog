from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any

import pydantic


class BeliefStateModel(pydantic.BaseModel):
    proposition: str
    confidence: float = 0.0
    contradictions: list[str] = pydantic.Field(default_factory=list)
    evidence: list[str] = pydantic.Field(default_factory=list)
    source: str | None = None
    metadata: dict[str, Any] = pydantic.Field(default_factory=dict)


@dataclass
class BeliefState:
    proposition: str
    confidence: float = 0.0
    contradictions: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    source: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    # ---- validation ----

    def __post_init__(self):
        self.confidence = max(0.0, min(1.0, self.confidence))

    # ---- merge ----

    def merge(self, other: BeliefState) -> BeliefState:
        if self.proposition != other.proposition:
            raise ValueError(
                f"Cannot merge beliefs with different propositions: "
                f"{self.proposition!r} vs {other.proposition!r}"
            )
        contradictions = self.contradictions.copy()
        for c in other.contradictions:
            if c not in contradictions:
                contradictions.append(c)
        evidence = self.evidence.copy()
        for e in other.evidence:
            if e not in evidence:
                evidence.append(e)
        return BeliefState(
            proposition=self.proposition,
            confidence=round((self.confidence + other.confidence) / 2.0, 10),
            contradictions=contradictions,
            evidence=evidence,
            source=self.source or other.source,
            metadata={**self.metadata, **other.metadata},
        )

    def contradict(self, statement: str) -> BeliefState:
        cs = self.contradictions.copy()
        if statement not in cs:
            cs.append(statement)
        return BeliefState(
            proposition=self.proposition,
            confidence=self.confidence * 0.5,
            contradictions=cs,
            evidence=self.evidence.copy(),
            source=self.source,
            metadata=self.metadata.copy(),
        )

    def support(self, evidence_item: str, delta: float = 0.1) -> BeliefState:
        ev = self.evidence.copy()
        if evidence_item not in ev:
            ev.append(evidence_item)
        return BeliefState(
            proposition=self.proposition,
            confidence=min(1.0, self.confidence + delta),
            contradictions=self.contradictions.copy(),
            evidence=ev,
            source=self.source,
            metadata=self.metadata.copy(),
        )

    # ---- serialization ----

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposition": self.proposition,
            "confidence": self.confidence,
            "contradictions": self.contradictions.copy(),
            "evidence": self.evidence.copy(),
            "source": self.source,
            "metadata": self.metadata.copy(),
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BeliefState:
        return cls(
            proposition=data["proposition"],
            confidence=data.get("confidence", 0.0),
            contradictions=data.get("contradictions", []),
            evidence=data.get("evidence", []),
            source=data.get("source"),
            metadata=data.get("metadata", {}),
        )

    @classmethod
    def from_json(cls, raw: str) -> BeliefState:
        return cls.from_dict(json.loads(raw))

    def to_pydantic(self) -> BeliefStateModel:
        return BeliefStateModel(**self.to_dict())

    @classmethod
    def from_pydantic(cls, model: BeliefStateModel) -> BeliefState:
        return cls.from_dict(model.model_dump())

    # ---- helpers ----

    def is_confident(self, threshold: float = 0.7) -> bool:
        return self.confidence >= threshold

    def is_contradicted(self) -> bool:
        return len(self.contradictions) > 0

    def __repr__(self) -> str:
        return (
            f"BeliefState(proposition={self.proposition!r}, "
            f"confidence={self.confidence:.2f}, "
            f"evidence={len(self.evidence)}, "
            f"contradictions={len(self.contradictions)})"
        )
