from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PortfolioItem(BaseModel):
    """포트폴리오 종목"""

    symbol: str = Field(..., description="종목코드")
    name: str = Field(..., description="종목명")
    quantity: int = Field(..., description="보유 수량")
    avg_cost: float = Field(..., description="평균 매입단가")
    current_price: float = Field(..., description="현재가")
    market_value: float = Field(..., description="평가금액")
    unrealized_pnl: float = Field(..., description="평가손익")
    unrealized_pnl_rate: float = Field(..., description="수익률 (%)")
    weight: float = Field(..., description="포트폴리오 비중 (%)")


class PortfolioSummary(BaseModel):
    """포트폴리오 요약"""

    total_invested: float = Field(..., description="총 투자금액")
    total_market_value: float = Field(..., description="총 평가금액")
    total_unrealized_pnl: float = Field(..., description="총 평가손익")
    total_unrealized_pnl_rate: float = Field(..., description="총 수익률 (%)")
    items: list[PortfolioItem]
    updated_at: datetime = Field(default_factory=datetime.now)


class PortfolioAddRequest(BaseModel):
    """포트폴리오 종목 추가 요청"""

    symbol: str
    quantity: int = Field(..., gt=0)
    avg_cost: float = Field(..., gt=0)


class DiversificationAnalysis(BaseModel):
    """분산투자 분석"""

    sector_weights: dict[str, float] = Field(
        ..., description="섹터별 비중 (%)"
    )
    top_holdings_weight: float = Field(..., description="상위 5종목 비중 (%)")
    herfindahl_index: float = Field(..., description="집중도 지수 (낮을수록 분산)")
    recommendation: Optional[str] = Field(None, description="분산투자 개선 제안")
