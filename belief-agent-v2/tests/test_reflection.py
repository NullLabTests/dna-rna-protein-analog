import json

from belief_agent.agent import BeliefAgent
from belief_agent.state import BeliefState
from belief_agent.reflection import reflect, auto_update, human_review, ReflectionResult


def _llm_accept(messages):
    return json.dumps({"critique": "Looks solid", "new_evidence": ["more data"], "new_contradictions": [], "updated_confidence": 0.9})


def _llm_reject(messages):
    return json.dumps({"critique": "Weak", "new_evidence": [], "new_contradictions": ["counterpoint"], "updated_confidence": 0.1})


def _llm_garbage(messages):
    return "not json"


def _llm_accept_decision(messages):
    return json.dumps({"accept": True})


def _llm_reject_decision(messages):
    return json.dumps({"accept": False})


class TestReflection:
    def test_reflect_updates_confidence(self):
        agent = BeliefAgent(llm_call=_llm_accept)
        agent.adopt(BeliefState("p", confidence=0.5, evidence=["e"]))
        results = reflect(agent, _llm_accept)
        assert len(results) == 1
        assert results[0].proposition == "p"
        assert results[0].original_confidence == 0.5
        assert results[0].accepted is True
        updated = agent.get_belief("p")
        assert updated.confidence == 0.9
        assert "more data" in updated.evidence

    def test_reflect_multiple_beliefs(self):
        agent = BeliefAgent(llm_call=_llm_accept)
        agent.adopt(BeliefState("a", confidence=0.5))
        agent.adopt(BeliefState("b", confidence=0.5))
        results = reflect(agent, _llm_accept)
        assert len(results) == 2

    def test_reflect_depth(self):
        agent = BeliefAgent(llm_call=_llm_accept)
        agent.adopt(BeliefState("p", confidence=0.5))
        results = reflect(agent, _llm_accept, depth=2)
        assert len(results) == 2  # 1 per depth

    def test_reflect_empty_agent(self):
        agent = BeliefAgent(llm_call=_llm_accept)
        results = reflect(agent, _llm_accept)
        assert results == []

    def test_reflect_depth_zero(self):
        agent = BeliefAgent(llm_call=_llm_accept)
        agent.adopt(BeliefState("p"))
        results = reflect(agent, _llm_accept, depth=0)
        assert results == []

    def test_garbage_llm_output(self):
        agent = BeliefAgent(llm_call=_llm_garbage)
        agent.adopt(BeliefState("p", confidence=0.5))
        results = reflect(agent, _llm_garbage)
        assert len(results) == 1
        assert results[0].accepted is False
        assert results[0].updated_confidence == 0.5

    def test_auto_update_low_confidence(self):
        agent = BeliefAgent(llm_call=_llm_accept)
        agent.adopt(BeliefState("high", confidence=0.9))
        agent.adopt(BeliefState("low", confidence=0.2))
        results = auto_update(agent, _llm_accept, threshold=0.3)
        assert len(results) == 1
        assert results[0].proposition == "low"

    def test_auto_update_no_low_confidence(self):
        agent = BeliefAgent(llm_call=_llm_accept)
        agent.adopt(BeliefState("p", confidence=0.9))
        results = auto_update(agent, _llm_accept, threshold=0.3)
        assert results == []

    def test_human_review(self):
        result = ReflectionResult(
            proposition="p",
            original_confidence=0.5,
            updated_confidence=0.8,
            critique="ok",
        )
        result = human_review(result, "Actually wrong", accepted=False)
        assert "Actually wrong" in result.critique
        assert result.accepted is False
