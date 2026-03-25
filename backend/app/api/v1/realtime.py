from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from app.schemas.realtime import (
    AddWatchlistRequest,
    RealtimePrice,
    WatchlistResponse,
    WatchlistState,
)
from app.services import watchlist as watchlist_service
from app.services.realtime import get_cache_ttl_remaining, get_realtime_prices

router = APIRouter()


def _iso_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


@router.get(
    "/prices",
    response_model=WatchlistResponse,
    summary="워치리스트 전체 시세 조회",
    description="한국·미국 워치리스트 종목의 현재 시세를 반환합니다. 10초 캐시 적용.",
)
async def get_watchlist_prices() -> WatchlistResponse:
    korean_symbols = await watchlist_service.get_korean_symbols()
    us_symbols = await watchlist_service.get_us_symbols()

    korean_prices, us_prices = await _fetch_all(korean_symbols, us_symbols)

    # 다음 업데이트까지 남은 시간은 더 짧은 쪽 기준
    kr_ttl = get_cache_ttl_remaining(korean_symbols, "KRX")
    us_ttl = get_cache_ttl_remaining(us_symbols, "US")
    next_update_in = min(kr_ttl, us_ttl) if (kr_ttl and us_ttl) else max(kr_ttl, us_ttl)

    return WatchlistResponse(
        korean=korean_prices,
        us=us_prices,
        updated_at=_iso_now(),
        next_update_in=next_update_in,
    )


@router.get(
    "/prices/{symbol}",
    response_model=RealtimePrice,
    summary="단일 종목 시세 조회",
    description="종목코드로 단일 종목 현재 시세를 조회합니다. market 쿼리 파라미터로 시장을 지정합니다.",
)
async def get_single_price(
    symbol: str,
    market: str = "KRX",
) -> RealtimePrice:
    upper_market = market.upper()
    if upper_market not in ("KRX", "NASDAQ", "NYSE", "US"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="market은 KRX / NASDAQ / NYSE / US 중 하나여야 합니다.",
        )

    # NASDAQ / NYSE → US 그룹으로 조회
    fetch_market = "KRX" if upper_market == "KRX" else "US"
    prices = await get_realtime_prices([symbol], fetch_market)

    if not prices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"시세 데이터를 가져올 수 없습니다: {symbol}",
        )

    return prices[0]


@router.get(
    "/watchlist",
    response_model=WatchlistState,
    summary="워치리스트 조회",
    description="현재 워치리스트에 등록된 종목코드 목록을 반환합니다.",
)
async def get_watchlist() -> WatchlistState:
    return WatchlistState(
        korean=await watchlist_service.get_korean_symbols(),
        us=await watchlist_service.get_us_symbols(),
    )


@router.post(
    "/watchlist",
    response_model=WatchlistState,
    status_code=status.HTTP_201_CREATED,
    summary="워치리스트 종목 추가",
    description="워치리스트에 새 종목을 추가합니다. 이미 존재하면 409를 반환합니다.",
)
async def add_to_watchlist(body: AddWatchlistRequest) -> WatchlistState:
    added = await watchlist_service.add_symbol(body.symbol, body.market)
    if not added:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"이미 워치리스트에 존재하는 종목입니다: {body.symbol}",
        )
    return WatchlistState(
        korean=await watchlist_service.get_korean_symbols(),
        us=await watchlist_service.get_us_symbols(),
    )


@router.delete(
    "/watchlist/{symbol}",
    response_model=WatchlistState,
    summary="워치리스트 종목 제거",
    description="워치리스트에서 종목을 제거합니다. 존재하지 않으면 404를 반환합니다.",
)
async def remove_from_watchlist(symbol: str) -> WatchlistState:
    removed = await watchlist_service.remove_symbol(symbol)
    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"워치리스트에 없는 종목입니다: {symbol}",
        )
    return WatchlistState(
        korean=await watchlist_service.get_korean_symbols(),
        us=await watchlist_service.get_us_symbols(),
    )


# ── 내부 헬퍼 ─────────────────────────────────────────────────────

async def _fetch_all(
    korean_symbols: list[str],
    us_symbols: list[str],
) -> tuple[list[RealtimePrice], list[RealtimePrice]]:
    """한국·미국 시세를 동시에 조회"""
    import asyncio

    results = await asyncio.gather(
        get_realtime_prices(korean_symbols, "KRX"),
        get_realtime_prices(us_symbols, "US"),
        return_exceptions=True,
    )

    korean_prices: list[RealtimePrice] = (
        results[0] if not isinstance(results[0], BaseException) else []
    )
    us_prices: list[RealtimePrice] = (
        results[1] if not isinstance(results[1], BaseException) else []
    )

    return korean_prices, us_prices
