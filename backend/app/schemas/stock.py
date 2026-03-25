from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StockPrice(BaseModel):
    """주식 현재가 응답 스키마"""

    symbol: str = Field(..., description="종목코드 (예: 005930)")
    name: str = Field(..., description="종목명")
    current_price: int = Field(..., description="현재가 (원)")
    change: int = Field(..., description="전일 대비 변동액")
    change_rate: float = Field(..., description="전일 대비 변동률 (%)")
    volume: int = Field(..., description="거래량")
    market_cap: Optional[int] = Field(None, description="시가총액 (원)")
    high_price: int = Field(..., description="당일 고가")
    low_price: int = Field(..., description="당일 저가")
    open_price: int = Field(..., description="당일 시가")
    prev_close: int = Field(..., description="전일 종가")
    timestamp: datetime = Field(default_factory=datetime.now, description="조회 시각")


class StockCandle(BaseModel):
    """OHLCV 캔들 데이터"""

    date: str = Field(..., description="일자 (YYYYMMDD)")
    open_price: int = Field(..., description="시가")
    high_price: int = Field(..., description="고가")
    low_price: int = Field(..., description="저가")
    close_price: int = Field(..., description="종가")
    volume: int = Field(..., description="거래량")
    change_rate: float = Field(..., description="등락률 (%)")


class StockHistory(BaseModel):
    """기간별 시세 응답 스키마"""

    symbol: str
    name: str
    period: str = Field(..., description="조회 기간 (D/W/M/Y)")
    candles: list[StockCandle]


class StockSearchResult(BaseModel):
    """종목 검색 결과"""

    symbol: str
    name: str
    market: str = Field(..., description="시장 구분 (KOSPI/KOSDAQ/NASDAQ 등)")
