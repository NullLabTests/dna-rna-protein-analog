import json

from belief_agent.agent import BeliefAgent
from belief_agent.state import BeliefState


def dummy_llm(messages):
    return json.dumps({"proposition": "test belief", "confidence": 0.8})


class TestBeliefAgent:
    def test_init(self):
        agent = BeliefAgent(llm_call=dummy_llm, name="test-agent")
        assert agent.name == "test-agent"
        assert agent.beliefs == {}

    def test_adopt_and_get_belief(self):
        agent = BeliefAgent(llm_call=dummy_llm)
        b = BeliefState("p", confidence=0.5)
        agent.adopt(b)
        assert agent.get_belief("p") is b

    def test_adopt_merge(self):
        agent = BeliefAgent(llm_call=dummy_llm)
        agent.adopt(BeliefState("p", confidence=0.6, evidence=["e1"]))
        agent.adopt(BeliefState("p", confidence=0.4, evidence=["e2"]))
        merged = agent.get_belief("p")
        assert merged.confidence == 0.5
        assert len(merged.evidence) == 2

    def test_update_belief(self):
        agent = BeliefAgent(llm_call=dummy_llm)
        agent.adopt(BeliefState("p", confidence=0.5))
        agent.update_belief("p", confidence=0.9)
        assert agent.get_belief("p").confidence == 0.9

    def test_update_belief_nonexistent(self):
        agent = BeliefAgent(llm_call=dummy_llm)
        assert agent.update_belief("nope") is None

    def test_remove_belief(self):
        agent = BeliefAgent(llm_call=dummy_llm)
        agent.adopt(BeliefState("p"))
        assert agent.remove_belief("p") is True
        assert agent.get_belief("p") is None
        assert agent.remove_belief("p") is False

    def test_list_beliefs_filter(self):
        agent = BeliefAgent(llm_call=dummy_llm)
        agent.adopt(BeliefState("a", confidence=0.9))
        agent.adopt(BeliefState("b", confidence=0.3))
        agent.adopt(BeliefState("c", confidence=0.6, contradictions=["x"]))
        assert len(agent.list_beliefs(min_confidence=0.5)) == 2
        assert len(agent.list_beliefs(only_contradicted=True)) == 1
        assert len(agent.list_beliefs(min_confidence=0.5, only_contradicted=True)) == 1

    def test_call_extracts_belief(self):
        agent = BeliefAgent(llm_call=dummy_llm)
        reply = agent("hello")
        data = json.loads(reply)
        assert agent.get_belief(data["proposition"]) is not None

    def test_belief_context(self):
        agent = BeliefAgent(llm_call=dummy_llm)
        agent.adopt(BeliefState("p", confidence=0.9))
        ctx = agent._belief_context()
        assert "confident" in ctx
        assert "p" in ctx
        agent.adopt(BeliefState("q", confidence=0.2, contradictions=["c"]))
        ctx = agent._belief_context()
        assert "contradicted" in ctx

    def test_serialization(self):
        agent = BeliefAgent(llm_call=dummy_llm, name="ser")
        agent.adopt(BeliefState("p", confidence=0.7))
        d = agent.to_dict()
        assert d["name"] == "ser"
        assert "p" in d["beliefs"]

    def test_reset_history(self):
        agent = BeliefAgent(llm_call=dummy_llm)
        agent("hi")
        assert len(agent.history) > 0
        agent.reset_history()
        assert agent.history == []

    def test_max_history(self):
        agent = BeliefAgent(llm_call=dummy_llm, max_history=2)
        agent("msg1")
        agent("msg2")
        agent("msg3")
        assert len(agent.history) <= 4  # 2 user + 2 assistant
