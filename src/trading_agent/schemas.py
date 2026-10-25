from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MarketSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticker: str = Field(min_length=1, max_length=15)
    requested_start: str
    requested_end: str
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    observations: int = Field(ge=1)
    first_bar_date: str
    last_bar_date: str
    latest_close: float = Field(gt=0)
    sma20: float | None = Field(default=None, gt=0)
    sma50: float | None = Field(default=None, gt=0)
    return_20d: float | None = None
    volatility_20d_annualized: float | None = Field(default=None, ge=0)
    trend_vs_sma20: str

    @field_validator("ticker")
    @classmethod
    def uppercase_ticker(cls, value: str) -> str:
        return value.strip().upper()


class EvidenceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_id: str
    claim: str
    source_name: str
    source_url: str | None = None
    published_at: datetime | None = None
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    excerpt: str | None = None
    numeric_value: float | None = None


class ResearchReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticker: str
    as_of: datetime
    horizon: str = "1–4 weeks"
    stance: Literal["bullish", "bearish", "neutral"] = "neutral"
    thesis: str
    supporting_evidence: list[str] = Field(default_factory=list)
    counter_evidence: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    invalidation_conditions: list[str] = Field(default_factory=list)
    confidence: Literal["low", "medium", "high"] = "low"
    missing_information: list[str] = Field(default_factory=list)
    action: Literal["watch", "investigate_further", "no_action"] = "no_action"
