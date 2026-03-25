from __future__ import annotations

import math
from typing import Optional

from app.config import get_settings
from app.schemas.analysis import (
    IntrinsicValue,
    MoatAssessment,
    ProfitabilityMetrics,
    SafetyMetrics,
    ValuationMetrics,
    ValueAnalysis,
)


def calculate_intrinsic_value(
    eps: float,
    current_price: int,
    growth_rate: float,
    discount_rate: float,
    terminal_growth: float,
    years: int,
) -> IntrinsicValue:
    """간략 DCF 내재가치 계산 (버핏식 2단계 DCF)

    1단계: `years`년간 EPS를 `growth_rate`로 성장
    2단계: 영구 성장 `terminal_growth` 적용

    Args:
        eps: 주당순이익
        current_price: 현재 주가
        growth_rate: 성장 기간 성장률 (소수, 예 0.10)
        discount_rate: 할인율 (소수, 예 0.10)
        terminal_growth: 영구 성장률 (소수, 예 0.03)
        years: 성장 기간 (년)

    Returns:
        IntrinsicValue
    """
    if discount_rate <= terminal_growth:
        raise ValueError("할인율은 영구 성장률보다 커야 합니다.")

    # 1단계: 성장기 현금흐름의 현재가치
    pv_growth = sum(
        eps * (1 + growth_rate) ** t / (1 + discount_rate) ** t
        for t in range(1, years + 1)
    )

    # 2단계: 터미널 가치 (고든 성장 모델)
    terminal_eps = eps * (1 + growth_rate) ** years
    terminal_value = terminal_eps * (1 + terminal_growth) / (discount_rate - terminal_growth)
    pv_terminal = terminal_value / (1 + discount_rate) ** years

    intrinsic = pv_growth + pv_terminal

    margin_of_safety = (
        round((intrinsic - current_price) / intrinsic * 100, 2)
        if intrinsic > 0
        else -100.0
    )

    return IntrinsicValue(
        current_price=current_price,
        intrinsic_value=round(intrinsic, 2),
        margin_of_safety=margin_of_safety,
        is_undervalued=margin_of_safety >= 25.0,  # 버핏: 최소 25% 안전마진
        eps=eps,
        growth_rate=growth_rate,
        discount_rate=discount_rate,
    )


def check_moat(
    roe_history: list[float],
    margin_history: list[float],
    debt_to_equity: Optional[float] = None,
    brand_power: bool = False,
    switching_cost: bool = False,
) -> MoatAssessment:
    """경제적 해자 평가

    Args:
        roe_history: 최근 5년 ROE 목록 (%)
        margin_history: 최근 5년 순이익률 목록 (%)
        debt_to_equity: 부채비율
        brand_power: 브랜드 파워 여부
        switching_cost: 전환 비용 여부

    Returns:
        MoatAssessment
    """
    # ROE 일관성: 5년 평균 15% 이상
    avg_roe = sum(roe_history) / len(roe_history) if roe_history else 0.0
    roe_consistent = avg_roe >= 15.0 and all(r >= 10.0 for r in roe_history)

    # 마진 추세
    if len(margin_history) >= 2:
        recent_avg = sum(margin_history[-2:]) / 2
        past_avg = sum(margin_history[:-2]) / max(len(margin_history) - 2, 1)
        if recent_avg > past_avg * 1.05:
            margin_trend = "IMPROVING"
        elif recent_avg < past_avg * 0.95:
            margin_trend = "DECLINING"
        else:
            margin_trend = "STABLE"
    else:
        margin_trend = "STABLE"

    # 경쟁 우위 요소
    advantages: list[str] = []
    risks: list[str] = []

    if roe_consistent:
        advantages.append("ROE 일관성 (5년 평균 15% 이상)")
    if brand_power:
        advantages.append("브랜드 파워")
    if switching_cost:
        advantages.append("높은 전환 비용")
    if margin_trend == "IMPROVING":
        advantages.append("이익률 개선 추세")
    if debt_to_equity is not None and debt_to_equity < 0.5:
        advantages.append("낮은 부채비율")

    if not roe_consistent:
        risks.append("ROE 불안정 또는 저조")
    if margin_trend == "DECLINING":
        risks.append("이익률 하락 추세")
    if debt_to_equity is not None and debt_to_equity > 2.0:
        risks.append("높은 부채비율 (재무 리스크)")

    # 해자 강도 결정
    score = sum([
        roe_consistent,
        brand_power,
        switching_cost,
        margin_trend == "IMPROVING",
        debt_to_equity is not None and debt_to_equity < 0.5,
    ])

    if score >= 4:
        moat_strength = "WIDE"
        has_moat = True
    elif score >= 2:
        moat_strength = "NARROW"
        has_moat = True
    else:
        moat_strength = "NONE"
        has_moat = False

    return MoatAssessment(
        has_moat=has_moat,
        moat_strength=moat_strength,
        roe_consistency=roe_consistent,
        margin_trend=margin_trend,
        competitive_advantages=advantages,
        risks=risks,
    )


def _calculate_overall_score(
    valuation: ValuationMetrics,
    profitability: ProfitabilityMetrics,
    safety: SafetyMetrics,
    moat: MoatAssessment,
    intrinsic: IntrinsicValue,
) -> float:
    """0~100점 종합 투자 점수 산출"""
    score = 0.0

    # 밸류에이션 (30점)
    if valuation.per is not None:
        if valuation.per < 10:
            score += 30
        elif valuation.per < 15:
            score += 20
        elif valuation.per < 25:
            score += 10

    # 수익성 (30점)
    if profitability.roe is not None:
        if profitability.roe >= 20:
            score += 15
        elif profitability.roe >= 15:
            score += 10
    if profitability.operating_margin is not None:
        if profitability.operating_margin >= 20:
            score += 15
        elif profitability.operating_margin >= 10:
            score += 8

    # 안전성 (20점)
    if safety.debt_to_equity is not None:
        if safety.debt_to_equity < 0.5:
            score += 20
        elif safety.debt_to_equity < 1.0:
            score += 12
        elif safety.debt_to_equity < 2.0:
            score += 6

    # 해자 (10점)
    if moat.moat_strength == "WIDE":
        score += 10
    elif moat.moat_strength == "NARROW":
        score += 5

    # 안전마진 (10점)
    if intrinsic.margin_of_safety >= 40:
        score += 10
    elif intrinsic.margin_of_safety >= 25:
        score += 7
    elif intrinsic.margin_of_safety >= 10:
        score += 3

    return min(round(score, 1), 100.0)


def _score_to_verdict(score: float) -> str:
    if score >= 80:
        return "STRONG_BUY"
    if score >= 65:
        return "BUY"
    if score >= 45:
        return "HOLD"
    if score >= 30:
        return "SELL"
    return "STRONG_SELL"


class ValueAnalysisService:
    """버핏식 가치투자 분석 서비스"""

    def __init__(self) -> None:
        self._settings = get_settings()

    async def analyze_value(
        self, symbol: str, include_ai: bool = False
    ) -> ValueAnalysis:
        """가치투자 종합 분석

        현재는 Mock 데이터 기반. Stage 2에서 DART/KIS 실데이터 연동.
        """
        # TODO: DART/KIS에서 실제 재무 데이터 조회 (Stage 2)
        mock_valuation = ValuationMetrics(
            per=12.5,
            pbr=1.8,
            psr=1.2,
            ev_ebitda=8.3,
            dividend_yield=2.1,
        )
        mock_profitability = ProfitabilityMetrics(
            roe=18.5,
            roa=9.2,
            gross_margin=45.0,
            operating_margin=22.0,
            net_margin=15.5,
        )
        mock_safety = SafetyMetrics(
            debt_to_equity=0.4,
            current_ratio=2.1,
            quick_ratio=1.8,
            interest_coverage=15.0,
        )

        moat = check_moat(
            roe_history=[17.0, 18.0, 19.5, 18.5, 18.5],
            margin_history=[14.0, 14.5, 15.0, 15.5, 15.5],
            debt_to_equity=mock_safety.debt_to_equity,
        )

        intrinsic = calculate_intrinsic_value(
            eps=5000.0,
            current_price=62500,
            growth_rate=0.10,
            discount_rate=self._settings.dcf_discount_rate,
            terminal_growth=self._settings.dcf_terminal_growth,
            years=self._settings.dcf_growth_years,
        )

        overall_score = _calculate_overall_score(
            mock_valuation, mock_profitability, mock_safety, moat, intrinsic
        )

        ai_commentary: Optional[str] = None
        if include_ai:
            from app.services.ai.analyzer import AIAnalyzer
            analyzer = AIAnalyzer()
            ai_commentary = await analyzer.generate_buffett_commentary(
                symbol=symbol,
                valuation=mock_valuation,
                profitability=mock_profitability,
                moat=moat,
                intrinsic=intrinsic,
            )

        return ValueAnalysis(
            symbol=symbol,
            name=f"종목 {symbol}",
            valuation=mock_valuation,
            profitability=mock_profitability,
            safety=mock_safety,
            moat=moat,
            intrinsic_value=intrinsic,
            overall_score=overall_score,
            verdict=_score_to_verdict(overall_score),
            ai_commentary=ai_commentary,
        )

    async def get_intrinsic_value(
        self, symbol: str, growth_rate: Optional[float] = None
    ) -> IntrinsicValue:
        """내재가치 단독 계산"""
        # TODO: 실제 EPS 조회 (Stage 2)
        eps = 5000.0
        current_price = 62500
        rate = growth_rate if growth_rate is not None else 0.10

        return calculate_intrinsic_value(
            eps=eps,
            current_price=current_price,
            growth_rate=rate,
            discount_rate=self._settings.dcf_discount_rate,
            terminal_growth=self._settings.dcf_terminal_growth,
            years=self._settings.dcf_growth_years,
        )

    async def check_moat(self, symbol: str) -> MoatAssessment:
        """해자 분석 단독 실행"""
        # TODO: 실제 재무 데이터 조회 (Stage 2)
        return check_moat(
            roe_history=[17.0, 18.0, 19.5, 18.5, 18.5],
            margin_history=[14.0, 14.5, 15.0, 15.5, 15.5],
            debt_to_equity=0.4,
        )
