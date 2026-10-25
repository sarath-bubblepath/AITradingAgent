import pytest
from pydantic import ValidationError

from trading_agent.schemas import ResearchReport


def test_research_report_defaults_to_neutral_no_action():
    report = ResearchReport(
        ticker="AAPL",
        as_of="2025-01-01T00:00:00Z",
        thesis="Insufficient evidence for a directional thesis.",
    )
    assert report.stance == "neutral"
    assert report.action == "no_action"
    assert report.confidence == "low"


def test_research_report_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        ResearchReport(
            ticker="AAPL",
            as_of="2025-01-01T00:00:00Z",
            thesis="Example",
            made_up_field="not allowed",
        )
