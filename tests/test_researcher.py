import pytest
from pydantic import ValidationError

from trading_agent.analysis.researcher import ResearchDraft


def test_research_draft_accepts_valid_response():
    draft = ResearchDraft.model_validate({
        "horizon": "1–4 weeks",
        "stance": "neutral",
        "thesis": "The supplied indicators are mixed.",
        "supporting_evidence": [
            "Close is above the 20-day SMA."
        ],
        "counter_evidence": [
            "The 20-session return is negative."
        ],
        "risks": ["Historical volatility is elevated."],
        "invalidation_conditions": [],
        "confidence": "low",
        "missing_information": ["Recent company news"],
        "action": "no_action",
    })

    assert draft.stance == "neutral"
    assert draft.action == "no_action"


def test_research_draft_rejects_invalid_stance():
    with pytest.raises(ValidationError):
        ResearchDraft.model_validate({
            "horizon": "1–4 weeks",
            "stance": "guaranteed_profit",
            "thesis": "Test",
            "confidence": "low",
            "action": "no_action",
        })
