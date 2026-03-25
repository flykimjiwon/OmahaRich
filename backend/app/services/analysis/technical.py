from __future__ import annotations

"""기술적 분석 보조 모듈.

버핏식 가치투자에서는 기술적 분석을 보조 참고용으로만 사용.
진입 타이밍 최적화 목적으로 한정.
"""

from typing import Optional

import numpy as np
import pandas as pd


def calculate_sma(prices: list[float], window: int) -> list[Optional[float]]:
    """단순 이동평균 (SMA)

    Args:
        prices: 종가 목록 (오래된 순)
        window: 이동평균 기간

    Returns:
        SMA 값 목록 (window 미만 구간은 None)
    """
    result: list[Optional[float]] = []
    for i in range(len(prices)):
        if i < window - 1:
            result.append(None)
        else:
            avg = sum(prices[i - window + 1 : i + 1]) / window
            result.append(round(avg, 2))
    return result


def calculate_rsi(prices: list[float], period: int = 14) -> list[Optional[float]]:
    """RSI (상대강도지수)

    Args:
        prices: 종가 목록 (오래된 순)
        period: RSI 기간 (기본 14)

    Returns:
        RSI 값 목록 (0~100)
    """
    if len(prices) < period + 1:
        return [None] * len(prices)

    result: list[Optional[float]] = [None] * period

    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [max(d, 0.0) for d in deltas]
    losses = [abs(min(d, 0.0)) for d in deltas]

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        if avg_loss == 0:
            result.append(100.0)
        else:
            rs = avg_gain / avg_loss
            result.append(round(100 - 100 / (1 + rs), 2))

    return result


def calculate_bollinger_bands(
    prices: list[float], window: int = 20, num_std: float = 2.0
) -> dict[str, list[Optional[float]]]:
    """볼린저 밴드

    Returns:
        {"upper": [...], "middle": [...], "lower": [...]}
    """
    middle = calculate_sma(prices, window)
    upper: list[Optional[float]] = []
    lower: list[Optional[float]] = []

    for i, mid in enumerate(middle):
        if mid is None or i < window - 1:
            upper.append(None)
            lower.append(None)
        else:
            std = float(np.std(prices[i - window + 1 : i + 1]))
            upper.append(round(mid + num_std * std, 2))
            lower.append(round(mid - num_std * std, 2))

    return {"upper": upper, "middle": middle, "lower": lower}


def is_oversold(rsi_values: list[Optional[float]], threshold: float = 30.0) -> bool:
    """최근 RSI가 과매도 구간인지 확인"""
    recent = next((v for v in reversed(rsi_values) if v is not None), None)
    return recent is not None and recent <= threshold


def is_overbought(rsi_values: list[Optional[float]], threshold: float = 70.0) -> bool:
    """최근 RSI가 과매수 구간인지 확인"""
    recent = next((v for v in reversed(rsi_values) if v is not None), None)
    return recent is not None and recent >= threshold
