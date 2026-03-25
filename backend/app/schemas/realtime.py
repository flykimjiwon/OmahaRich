from __future__ import annotations

from pydantic import BaseModel, Field


class RealtimePrice(BaseModel):
    """실시간 시세 응답 스키마"""

    symbol: str = Field(..., description="종목코드 (예: 005930, AAPL)")
    name: str = Field(..., description="종목명")
    market: str = Field(..., description="시장 구분 (KRX / NASDAQ / NYSE)")
    current_price: float = Field(..., description="현재가")
    change: float = Field(..., description="전일대비 변동액")
    change_percent: float = Field(..., description="등락률 (%)")
    volume: int = Field(..., description="거래량")
    high: float = Field(..., description="당일 고가")
    low: float = Field(..., description="당일 저가")
    open_price: float = Field(..., description="당일 시가")
    prev_close: float = Field(..., description="전일 종가")
    market_cap: float | None = Field(None, description="시가총액")
    per: float | None = Field(None, description="PER (주가수익비율)")
    pbr: float | None = Field(None, description="PBR (주가순자산비율)")
    updated_at: str = Field(..., description="업데이트 시각 (ISO 8601)")
    is_stale: bool = Field(False, description="캐시된 stale 데이터 여부")


class WatchlistResponse(BaseModel):
    """워치리스트 전체 시세 응답"""

    korean: list[RealtimePrice] = Field(..., description="한국 주식 시세")
    us: list[RealtimePrice] = Field(..., description="미국 주식 시세")
    updated_at: str = Field(..., description="조회 시각 (ISO 8601)")
    next_update_in: int = Field(..., description="다음 업데이트까지 남은 초")


class WatchlistItem(BaseModel):
    """워치리스트 단일 항목"""

    symbol: str = Field(..., description="종목코드")
    market: str = Field(..., description="시장 구분 (KRX / NASDAQ / NYSE)")


class WatchlistState(BaseModel):
    """워치리스트 현재 상태"""

    korean: list[str] = Field(..., description="한국 종목코드 목록")
    us: list[str] = Field(..., description="미국 종목코드 목록")


class AddWatchlistRequest(BaseModel):
    """워치리스트 종목 추가 요청"""

    symbol: str = Field(..., description="종목코드")
    market: str = Field(..., description="시장 구분 (KRX / NASDAQ / NYSE)")
