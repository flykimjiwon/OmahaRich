from __future__ import annotations

from typing import Optional

import pandas as pd


def parse_income_statement(raw: dict[str, object]) -> dict[str, float]:
    """DART 손익계산서 파싱 → 핵심 지표 추출

    Args:
        raw: DART API 응답 딕셔너리

    Returns:
        표준화된 재무 지표 딕셔너리
    """
    def safe_float(val: object) -> float:
        try:
            return float(str(val).replace(",", ""))
        except (ValueError, TypeError):
            return 0.0

    revenue = safe_float(raw.get("revenue", 0))
    gross_profit = safe_float(raw.get("gross_profit", 0))
    operating_income = safe_float(raw.get("operating_income", 0))
    net_income = safe_float(raw.get("net_income", 0))

    return {
        "revenue": revenue,
        "gross_profit": gross_profit,
        "operating_income": operating_income,
        "net_income": net_income,
        "gross_margin": round(gross_profit / revenue * 100, 2) if revenue else 0.0,
        "operating_margin": round(operating_income / revenue * 100, 2) if revenue else 0.0,
        "net_margin": round(net_income / revenue * 100, 2) if revenue else 0.0,
    }


def calculate_roe(net_income: float, equity: float) -> Optional[float]:
    """ROE = 순이익 / 자기자본 × 100"""
    if equity <= 0:
        return None
    return round(net_income / equity * 100, 2)


def calculate_roa(net_income: float, total_assets: float) -> Optional[float]:
    """ROA = 순이익 / 총자산 × 100"""
    if total_assets <= 0:
        return None
    return round(net_income / total_assets * 100, 2)


def calculate_roic(
    operating_income: float,
    tax_rate: float,
    invested_capital: float,
) -> Optional[float]:
    """ROIC = NOPAT / 투하자본 × 100

    NOPAT = 영업이익 × (1 - 세율)
    """
    if invested_capital <= 0:
        return None
    nopat = operating_income * (1 - tax_rate)
    return round(nopat / invested_capital * 100, 2)


def compute_cagr(values: list[float], years: int) -> Optional[float]:
    """연평균 성장률 (CAGR) 계산

    Args:
        values: 시계열 값 목록 (오래된 순)
        years: 기간 (년)

    Returns:
        CAGR (%) 또는 None
    """
    if len(values) < 2 or years <= 0:
        return None
    start, end = values[0], values[-1]
    if start <= 0:
        return None
    cagr = (end / start) ** (1 / years) - 1
    return round(cagr * 100, 2)


def altman_z_score(
    working_capital: float,
    retained_earnings: float,
    ebit: float,
    market_cap: float,
    total_liabilities: float,
    revenue: float,
    total_assets: float,
) -> float:
    """Altman Z-Score (파산 예측 모델)

    Z > 2.99: 안전  1.81 ~ 2.99: 회색지대  Z < 1.81: 위험

    Returns:
        Z-Score 값
    """
    if total_assets == 0:
        return 0.0

    x1 = working_capital / total_assets
    x2 = retained_earnings / total_assets
    x3 = ebit / total_assets
    x4 = market_cap / total_liabilities if total_liabilities > 0 else 0.0
    x5 = revenue / total_assets

    return round(1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + x5, 3)
