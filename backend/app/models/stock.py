from __future__ import annotations

"""데이터베이스 모델 (Stage 2: Supabase/SQLAlchemy 연동 예정).

현재는 Pydantic 기반 도메인 모델로만 사용.
Supabase 연동 시 SQLAlchemy 2.0 mapped_column 방식으로 전환.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StockRecord(BaseModel):
    """주식 시세 기록 (DB 저장용)"""

    id: Optional[int] = None
    symbol: str
    name: str
    market: str  # KOSPI / KOSDAQ / NASDAQ / NYSE
    current_price: int
    change: int
    change_rate: float
    volume: int
    recorded_at: datetime = Field(default_factory=datetime.now)


class AnalysisRecord(BaseModel):
    """가치투자 분석 기록 (DB 저장용)"""

    id: Optional[int] = None
    symbol: str
    overall_score: float
    verdict: str
    intrinsic_value: float
    margin_of_safety: float
    moat_strength: str
    ai_commentary: Optional[str] = None
    analyzed_at: datetime = Field(default_factory=datetime.now)


class WatchlistItem(BaseModel):
    """관심 종목"""

    id: Optional[int] = None
    user_id: str  # Supabase auth.uid()
    symbol: str
    name: str
    target_price: Optional[float] = None
    note: Optional[str] = None
    added_at: datetime = Field(default_factory=datetime.now)
