from belief_agent.state import BeliefState


class TestBeliefState:
    def test_default_confidence(self):
        b = BeliefState(proposition="The sky is blue")
        assert b.proposition == "The sky is blue"
        assert b.confidence == 0.0
        assert b.contradictions == []
        assert b.evidence == []

    def test_confidence_clamped(self):
        b = BeliefState(proposition="p", confidence=1.5)
        assert b.confidence == 1.0
        b = BeliefState(proposition="p", confidence=-0.5)
        assert b.confidence == 0.0

    def test_merge_same_proposition(self):
        a = BeliefState("p", confidence=0.8, evidence=["e1"])
        b = BeliefState("p", confidence=0.4, contradictions=["c1"])
        merged = a.merge(b)
        assert merged.proposition == "p"
        assert merged.confidence == 0.6
        assert "e1" in merged.evidence
        assert "c1" in merged.contradictions

    def test_merge_different_proposition_raises(self):
        import pytest

        a = BeliefState("p")
        b = BeliefState("q")
        with pytest.raises(ValueError, match="different propositions"):
            a.merge(b)

    def test_contradict_lowers_confidence(self):
        b = BeliefState("p", confidence=0.8)
        b2 = b.contradict("q")
        assert b2.confidence == 0.4

    def test_support_raises_confidence(self):
        b = BeliefState("p", confidence=0.5)
        b2 = b.support("new evidence")
        assert b2.confidence == 0.6

    def test_support_caps_at_one(self):
        b = BeliefState("p", confidence=0.95)
        b2 = b.support("more evidence")
        assert b2.confidence == 1.0

    def test_to_dict_roundtrip(self):
        b = BeliefState(
            proposition="p",
            confidence=0.7,
            evidence=["e1"],
            contradictions=["c1"],
            source="test",
            metadata={"k": "v"},
        )
        d = b.to_dict()
        b2 = BeliefState.from_dict(d)
        assert b2.proposition == "p"
        assert b2.confidence == 0.7
        assert b2.evidence == ["e1"]
        assert b2.contradictions == ["c1"]
        assert b2.source == "test"
        assert b2.metadata == {"k": "v"}

    def test_to_json_roundtrip(self):
        b = BeliefState("p", confidence=0.5)
        raw = b.to_json()
        b2 = BeliefState.from_json(raw)
        assert b2.proposition == "p"
        assert b2.confidence == 0.5

    def test_is_confident(self):
        assert BeliefState("p", confidence=0.8).is_confident()
        assert not BeliefState("p", confidence=0.5).is_confident()

    def test_is_contradicted(self):
        assert BeliefState("p", contradictions=["c"]).is_contradicted()
        assert not BeliefState("p").is_contradicted()

    def test_repr(self):
        b = BeliefState("p", confidence=0.5, evidence=["a"], contradictions=["b"])
        r = repr(b)
        assert "p" in r
        assert "0.50" in r
