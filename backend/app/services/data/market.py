from __future__ import annotations

"""시장 데이터 서비스.

pykrx(국내), yfinance(해외) 기반 시장 데이터 조회.
동기 라이브러리를 asyncio.to_thread로 비동기 래핑.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, Optional


async def get_krx_ohlcv(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> list[dict[str, Any]]:
    """pykrx로 국내 주식 OHLCV 조회

    Args:
        symbol: 종목코드 (예: "005930")
        start_date: 시작일 YYYYMMDD (없으면 90일 전)
        end_date: 종료일 YYYYMMDD (없으면 오늘)

    Returns:
        OHLCV 레코드 목록
    """
    try:
        from pykrx import stock as pykrx_stock
    except ImportError as exc:
        raise RuntimeError("pykrx가 설치되어 있지 않습니다: pip install pykrx") from exc

    if end_date is None:
        end_date = datetime.now().strftime("%Y%m%d")
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")

    def _fetch() -> list[dict[str, Any]]:
        df = pykrx_stock.get_market_ohlcv_by_date(start_date, end_date, symbol)
        records = []
        for date_idx, row in df.iterrows():
            records.append({
                "date": str(date_idx).replace("-", ""),
                "open": int(row.get("시가", 0)),
                "high": int(row.get("고가", 0)),
                "low": int(row.get("저가", 0)),
                "close": int(row.get("종가", 0)),
                "volume": int(row.get("거래량", 0)),
            })
        return records

    return await asyncio.to_thread(_fetch)


async def get_yfinance_ohlcv(
    ticker: str,
    period: str = "3mo",
    interval: str = "1d",
) -> list[dict[str, Any]]:
    """yfinance로 해외 주식 OHLCV 조회

    Args:
        ticker: Yahoo Finance 티커 (예: "AAPL", "005930.KS")
        period: 기간 (1d/5d/1mo/3mo/6mo/1y/2y/5y/10y/ytd/max)
        interval: 간격 (1m/2m/5m/15m/30m/60m/90m/1h/1d/5d/1wk/1mo/3mo)

    Returns:
        OHLCV 레코드 목록
    """
    try:
        import yfinance as yf
    except ImportError as exc:
        raise RuntimeError("yfinance가 설치되어 있지 않습니다: pip install yfinance") from exc

    def _fetch() -> list[dict[str, Any]]:
        hist = yf.Ticker(ticker).history(period=period, interval=interval)
        records = []
        for date_idx, row in hist.iterrows():
            records.append({
                "date": str(date_idx)[:10].replace("-", ""),
                "open": round(float(row["Open"]), 4),
                "high": round(float(row["High"]), 4),
                "low": round(float(row["Low"]), 4),
                "close": round(float(row["Close"]), 4),
                "volume": int(row["Volume"]),
            })
        return records

    return await asyncio.to_thread(_fetch)


async def get_market_index(index_code: str = "KOSPI") -> dict[str, Any]:
    """주요 지수 현재값 조회

    Args:
        index_code: 지수명 (KOSPI/KOSDAQ/NASDAQ/SNP500)

    Returns:
        지수 정보 딕셔너리
    """
    yf_map = {
        "KOSPI": "^KS11",
        "KOSDAQ": "^KQ11",
        "NASDAQ": "^IXIC",
        "SNP500": "^GSPC",
        "DOW": "^DJI",
    }
    ticker = yf_map.get(index_code.upper())
    if ticker is None:
        raise ValueError(f"지원하지 않는 지수: {index_code}")

    try:
        import yfinance as yf
    except ImportError as exc:
        raise RuntimeError("yfinance가 설치되어 있지 않습니다.") from exc

    def _fetch() -> dict[str, Any]:
        info = yf.Ticker(ticker).fast_info
        return {
            "index": index_code,
            "last_price": round(float(info.last_price), 2),
            "previous_close": round(float(info.previous_close), 2),
            "change": round(float(info.last_price - info.previous_close), 2),
            "change_rate": round(
                (info.last_price - info.previous_close) / info.previous_close * 100, 2
            ),
        }

    return await asyncio.to_thread(_fetch)
