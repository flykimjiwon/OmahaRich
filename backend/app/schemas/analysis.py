from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ValuationMetrics(BaseModel):
    """밸류에이션 지표"""

    per: Optional[float] = Field(None, description="주가수익비율 (Price/EPS)")
    pbr: Optional[float] = Field(None, description="주가순자산비율 (Price/BPS)")
    psr: Optional[float] = Field(None, description="주가매출비율 (Price/SPS)")
    pcr: Optional[float] = Field(None, description="주가현금흐름비율")
    ev_ebitda: Optional[float] = Field(None, description="EV/EBITDA")
    dividend_yield: Optional[float] = Field(None, description="배당수익률 (%)")


class ProfitabilityMetrics(BaseModel):
    """수익성 지표"""

    roe: Optional[float] = Field(None, description="자기자본이익률 (%)")
    roa: Optional[float] = Field(None, description="총자산이익률 (%)")
    roic: Optional[float] = Field(None, description="투하자본이익률 (%)")
    gross_margin: Optional[float] = Field(None, description="매출총이익률 (%)")
    operating_margin: Optional[float] = Field(None, description="영업이익률 (%)")
    net_margin: Optional[float] = Field(None, description="순이익률 (%)")


class SafetyMetrics(BaseModel):
    """안전성 지표"""

    debt_to_equity: Optional[float] = Field(None, description="부채비율")
    current_ratio: Optional[float] = Field(None, description="유동비율")
    quick_ratio: Optional[float] = Field(None, description="당좌비율")
    interest_coverage: Optional[float] = Field(None, description="이자보상배율")


class MoatAssessment(BaseModel):
    """경제적 해자 평가"""

    has_moat: bool = Field(..., description="해자 보유 여부")
    moat_strength: str = Field(..., description="해자 강도 (WIDE/NARROW/NONE)")
    roe_consistency: bool = Field(..., description="ROE 일관성 (5년 평균 15% 이상)")
    margin_trend: str = Field(..., description="이익률 추세 (IMPROVING/STABLE/DECLINING)")
    competitive_advantages: list[str] = Field(
        default_factory=list, description="경쟁 우위 요소"
    )
    risks: list[str] = Field(default_factory=list, description="리스크 요소")


class IntrinsicValue(BaseModel):
    """내재가치 계산 결과"""

    current_price: int = Field(..., description="현재 주가")
    intrinsic_value: float = Field(..., description="DCF 내재가치")
    margin_of_safety: float = Field(..., description="안전마진 (%)")
    is_undervalued: bool = Field(..., description="저평가 여부")
    eps: float = Field(..., description="주당순이익")
    growth_rate: float = Field(..., description="사용된 성장률")
    discount_rate: float = Field(..., description="사용된 할인율")


class ValueAnalysis(BaseModel):
    """가치투자 종합 분석 결과"""

    symbol: str
    name: str
    valuation: ValuationMetrics
    profitability: ProfitabilityMetrics
    safety: SafetyMetrics
    moat: MoatAssessment
    intrinsic_value: IntrinsicValue
    overall_score: float = Field(..., description="종합 투자 점수 (0~100)")
    verdict: str = Field(
        ..., description="투자 의견 (STRONG_BUY/BUY/HOLD/SELL/STRONG_SELL)"
    )
    ai_commentary: Optional[str] = Field(None, description="AI 버핏 스타일 코멘트")
