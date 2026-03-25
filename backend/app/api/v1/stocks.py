from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas.stock import StockHistory, StockPrice, StockSearchResult
from app.services.kis.domestic import KISDomesticService

router = APIRouter()


def get_kis_domestic() -> KISDomesticService:
    return KISDomesticService()


@router.get(
    "/{symbol}/price",
    response_model=StockPrice,
    summary="주식 현재가 조회",
    description="종목코드로 현재가 시세를 조회합니다.",
)
async def get_stock_price(
    symbol: str,
    service: Annotated[KISDomesticService, Depends(get_kis_domestic)],
) -> StockPrice:
    try:
        return await service.get_stock_price(symbol)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"KIS API 오류: {exc}",
        ) from exc


@router.get(
    "/{symbol}/history",
    response_model=StockHistory,
    summary="기간별 시세 조회",
    description="종목의 일/주/월/년 OHLCV 캔들 데이터를 조회합니다.",
)
async def get_stock_history(
    symbol: str,
    service: Annotated[KISDomesticService, Depends(get_kis_domestic)],
    period: Annotated[str, Query(description="기간 구분 (D/W/M/Y)", pattern="^[DWMY]$")] = "D",
    count: Annotated[int, Query(description="조회 봉 수", ge=1, le=500)] = 60,
) -> StockHistory:
    try:
        return await service.get_stock_history(symbol, period=period, count=count)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"KIS API 오류: {exc}",
        ) from exc


@router.get(
    "/search",
    response_model=list[StockSearchResult],
    summary="종목 검색",
    description="종목명 또는 종목코드로 검색합니다.",
)
async def search_stocks(
    q: Annotated[str, Query(description="검색어", min_length=1)],
) -> list[StockSearchResult]:
    # TODO: pykrx 또는 KIS 종목 검색 API 연동 (Stage 2)
    return []
