from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from app.config import get_settings
from app.schemas.realtime import RealtimePrice

logger = logging.getLogger(__name__)

# ── 캐시 (10초 TTL) ────────────────────────────────────────────────
_CACHE_TTL_SECONDS = 10

# 캐시 구조: { cache_key: (timestamp_utc, list[RealtimePrice]) }
_price_cache: dict[str, tuple[float, list[RealtimePrice]]] = {}

# stale 캐시 (마지막 성공 데이터): { cache_key: list[RealtimePrice] }
_stale_cache: dict[str, list[RealtimePrice]] = {}

# KIS 종목명 맵 (한국 기본 종목)
_KRX_NAMES: dict[str, str] = {
    "005930": "삼성전자",
    "000660": "SK하이닉스",
    "373220": "LG에너지솔루션",
}

# 미국 기본 종목명 맵
_US_NAMES: dict[str, str] = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "NVDA": "NVIDIA Corp.",
    "TSLA": "Tesla Inc.",
}

# price_history 보관 기간 (기본 1일)
_PRICE_HISTORY_RETENTION_DAYS: int = 1


def _now_utc() -> float:
    return datetime.now(tz=timezone.utc).timestamp()


def _iso_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _cache_key(symbols: list[str], market: str) -> str:
    return f"{market}:{','.join(sorted(symbols))}"


def _is_cache_fresh(key: str) -> bool:
    if key not in _price_cache:
        return False
    cached_at, _ = _price_cache[key]
    return (_now_utc() - cached_at) < _CACHE_TTL_SECONDS


def _seconds_until_refresh(key: str) -> int:
    if key not in _price_cache:
        return 0
    cached_at, _ = _price_cache[key]
    remaining = _CACHE_TTL_SECONDS - (_now_utc() - cached_at)
    return max(0, int(remaining))


# ── KIS 사용 가능 여부 ─────────────────────────────────────────────

def _kis_available() -> bool:
    settings = get_settings()
    return bool(settings.kis_app_key and settings.kis_app_secret)


# ── yfinance 폴백 (미국) ───────────────────────────────────────────

async def _fetch_us_yfinance(symbols: list[str]) -> list[RealtimePrice]:
    """yfinance로 미국 주식 시세 조회 (동기 → asyncio.to_thread 래핑)"""

    def _sync_fetch(symbol: str) -> RealtimePrice:
        import yfinance as yf  # 지연 임포트 (선택적 의존성)

        ticker = yf.Ticker(symbol)
        info: dict[str, Any] = ticker.fast_info or {}
        full_info: dict[str, Any] = {}

        current_price = float(info.get("last_price") or info.get("regularMarketPrice") or 0.0)
        prev_close = float(info.get("previous_close") or info.get("regularMarketPreviousClose") or 0.0)
        change = round(current_price - prev_close, 4)
        change_percent = round((change / prev_close * 100), 2) if prev_close else 0.0

        # PER, PBR, market_cap은 full info에서 (느리지만 캐시됨)
        try:
            full_info = ticker.info or {}
        except Exception as exc:
            logger.debug("yfinance full info 조회 실패 [%s]: %s", symbol, exc)

        market_cap = float(full_info.get("marketCap") or info.get("market_cap") or 0.0) or None
        per = float(full_info.get("trailingPE") or 0.0) or None
        pbr = float(full_info.get("priceToBook") or 0.0) or None

        # 거래소 판별
        exchange = str(full_info.get("exchange") or "NASDAQ").upper()
        market = "NYSE" if exchange in ("NYQ", "NYSE") else "NASDAQ"

        name = str(full_info.get("shortName") or full_info.get("longName") or _US_NAMES.get(symbol, symbol))

        return RealtimePrice(
            symbol=symbol,
            name=name,
            market=market,
            current_price=current_price,
            change=change,
            change_percent=change_percent,
            volume=int(info.get("three_month_average_volume") or full_info.get("volume") or 0),
            high=float(info.get("day_high") or full_info.get("dayHigh") or current_price),
            low=float(info.get("day_low") or full_info.get("dayLow") or current_price),
            open_price=float(info.get("open") or full_info.get("open") or prev_close),
            prev_close=prev_close,
            market_cap=market_cap,
            per=per,
            pbr=pbr,
            updated_at=_iso_now(),
            is_stale=False,
        )

    results: list[RealtimePrice] = []
    tasks = [asyncio.to_thread(_sync_fetch, sym) for sym in symbols]
    raw = await asyncio.gather(*tasks, return_exceptions=True)

    for sym, result in zip(symbols, raw):
        if isinstance(result, BaseException):
            logger.warning("yfinance 조회 실패 [%s]: %s", sym, result)
            # stale 데이터가 있으면 반환
            stale_key = _cache_key([sym], "US")
            if stale_key in _stale_cache and _stale_cache[stale_key]:
                stale = _stale_cache[stale_key][0]
                results.append(stale.model_copy(update={"is_stale": True}))
        else:
            results.append(result)  # type: ignore[arg-type]

    return results


# ── pykrx 폴백 (한국) ─────────────────────────────────────────────

async def _fetch_krx_pykrx(symbols: list[str]) -> list[RealtimePrice]:
    """pykrx로 한국 주식 시세 조회 (동기 → asyncio.to_thread 래핑)"""

    def _sync_fetch_all(syms: list[str]) -> list[RealtimePrice]:
        from pykrx import stock as pykrx_stock  # 지연 임포트

        today = datetime.now(tz=timezone.utc).strftime("%Y%m%d")
        results_inner: list[RealtimePrice] = []

        for sym in syms:
            try:
                # 당일 OHLCV
                df = pykrx_stock.get_market_ohlcv_by_date(today, today, sym)
                if df.empty:
                    raise ValueError(f"데이터 없음: {sym}")

                row = df.iloc[-1]
                open_p = float(row.get("시가", 0))
                high_p = float(row.get("고가", 0))
                low_p = float(row.get("저가", 0))
                close_p = float(row.get("종가", 0))
                volume = int(row.get("거래량", 0))

                # 전일 종가
                prev_df = pykrx_stock.get_market_ohlcv_by_date(
                    (datetime.now(tz=timezone.utc).replace(day=max(1, datetime.now(tz=timezone.utc).day - 5))).strftime("%Y%m%d"),
                    today,
                    sym,
                )
                if len(prev_df) >= 2:
                    prev_close = float(prev_df.iloc[-2]["종가"])
                else:
                    prev_close = close_p

                change = round(close_p - prev_close, 2)
                change_percent = round((change / prev_close * 100), 2) if prev_close else 0.0

                # 시가총액
                market_cap_df = pykrx_stock.get_market_cap_by_date(today, today, sym)
                market_cap: float | None = None
                if not market_cap_df.empty:
                    market_cap = float(market_cap_df.iloc[-1].get("시가총액", 0)) or None

                name = _KRX_NAMES.get(sym, sym)
                try:
                    name = pykrx_stock.get_market_ticker_name(sym) or name
                except Exception:
                    pass

                results_inner.append(
                    RealtimePrice(
                        symbol=sym,
                        name=name,
                        market="KRX",
                        current_price=close_p,
                        change=change,
                        change_percent=change_percent,
                        volume=volume,
                        high=high_p,
                        low=low_p,
                        open_price=open_p,
                        prev_close=prev_close,
                        market_cap=market_cap,
                        per=None,
                        pbr=None,
                        updated_at=_iso_now(),
                        is_stale=False,
                    )
                )
            except Exception as exc:
                logger.warning("pykrx 조회 실패 [%s]: %s", sym, exc)
                stale_key = _cache_key([sym], "KRX")
                if stale_key in _stale_cache and _stale_cache[stale_key]:
                    stale = _stale_cache[stale_key][0]
                    results_inner.append(stale.model_copy(update={"is_stale": True}))

        return results_inner

    return await asyncio.to_thread(_sync_fetch_all, symbols)


# ── KIS 경로 (설정 시) ────────────────────────────────────────────

async def _fetch_krx_kis(symbols: list[str]) -> list[RealtimePrice]:
    """KIS API로 국내 주식 시세 일괄 조회"""
    from app.services.kis.domestic import KISDomesticService

    service = KISDomesticService()
    results: list[RealtimePrice] = []

    fetch_tasks = [service.get_stock_price(sym) for sym in symbols]
    raw = await asyncio.gather(*fetch_tasks, return_exceptions=True)

    for sym, result in zip(symbols, raw):
        if isinstance(result, BaseException):
            logger.warning("KIS 국내 조회 실패 [%s]: %s", sym, result)
            stale_key = _cache_key([sym], "KRX")
            if stale_key in _stale_cache and _stale_cache[stale_key]:
                stale = _stale_cache[stale_key][0]
                results.append(stale.model_copy(update={"is_stale": True}))
            continue

        sp = result  # StockPrice
        results.append(
            RealtimePrice(
                symbol=sp.symbol,
                name=sp.name,
                market="KRX",
                current_price=float(sp.current_price),
                change=float(sp.change),
                change_percent=float(sp.change_rate),
                volume=sp.volume,
                high=float(sp.high_price),
                low=float(sp.low_price),
                open_price=float(sp.open_price),
                prev_close=float(sp.prev_close),
                market_cap=float(sp.market_cap) if sp.market_cap else None,
                per=None,
                pbr=None,
                updated_at=_iso_now(),
                is_stale=False,
            )
        )

    return results


async def _fetch_us_kis(symbols: list[str]) -> list[RealtimePrice]:
    """KIS API로 해외 주식 시세 일괄 조회"""
    from app.services.kis.overseas import KISOverseasService

    service = KISOverseasService()
    results: list[RealtimePrice] = []

    fetch_tasks = [service.get_stock_price(sym) for sym in symbols]
    raw = await asyncio.gather(*fetch_tasks, return_exceptions=True)

    for sym, result in zip(symbols, raw):
        if isinstance(result, BaseException):
            logger.warning("KIS 해외 조회 실패 [%s]: %s", sym, result)
            stale_key = _cache_key([sym], "US")
            if stale_key in _stale_cache and _stale_cache[stale_key]:
                stale = _stale_cache[stale_key][0]
                results.append(stale.model_copy(update={"is_stale": True}))
            continue

        sp = result
        results.append(
            RealtimePrice(
                symbol=sp.symbol,
                name=sp.name,
                market="NASDAQ",
                current_price=float(sp.current_price),
                change=float(sp.change),
                change_percent=float(sp.change_rate),
                volume=sp.volume,
                high=float(sp.high_price),
                low=float(sp.low_price),
                open_price=float(sp.open_price),
                prev_close=float(sp.prev_close),
                market_cap=None,
                per=None,
                pbr=None,
                updated_at=_iso_now(),
                is_stale=False,
            )
        )

    return results


# ── price_history 저장 ────────────────────────────────────────────

async def _save_price_history(prices: list[RealtimePrice]) -> None:
    """시세 데이터를 price_history 테이블에 저장 (stale 데이터 제외)."""
    fresh = [p for p in prices if not p.is_stale]
    if not fresh:
        return

    try:
        from app.database import get_session_factory
        from app.models.db import PriceHistory

        now = datetime.now(tz=timezone.utc)
        factory = get_session_factory()
        async with factory() as session:
            for p in fresh:
                session.add(
                    PriceHistory(
                        symbol=p.symbol,
                        price=p.current_price,
                        change=p.change,
                        change_percent=p.change_percent,
                        volume=p.volume,
                        per=p.per,
                        pbr=p.pbr,
                        market_cap=p.market_cap,
                        recorded_at=now,
                    )
                )
            await session.commit()
    except Exception as exc:
        logger.warning("price_history 저장 실패: %s", exc)


async def _cleanup_old_price_history() -> None:
    """보관 기간 초과 price_history 레코드 삭제."""
    try:
        from sqlalchemy import delete as sa_delete

        from app.database import get_session_factory
        from app.models.db import PriceHistory

        cutoff = datetime.now(tz=timezone.utc) - timedelta(days=_PRICE_HISTORY_RETENTION_DAYS)
        factory = get_session_factory()
        async with factory() as session:
            result = await session.execute(
                sa_delete(PriceHistory).where(PriceHistory.recorded_at < cutoff)
            )
            await session.commit()
            if result.rowcount:
                logger.debug("오래된 price_history %d건 삭제", result.rowcount)
    except Exception as exc:
        logger.warning("price_history 정리 실패: %s", exc)


# ── 공개 인터페이스 ──────────────────────────────────────────────────

async def get_realtime_prices(symbols: list[str], market: str) -> list[RealtimePrice]:
    """여러 종목 시세 한번에 조회.

    - KIS 설정 시 KIS 우선, 없으면 yfinance(미국) / pykrx(한국) 폴백
    - 10초 TTL 캐시 적용
    - 에러 시 마지막 성공 데이터(stale) 반환
    - 성공 시 price_history 테이블에 자동 저장

    Args:
        symbols: 종목코드 목록
        market: "KRX" | "US"

    Returns:
        RealtimePrice 목록
    """
    if not symbols:
        return []

    key = _cache_key(symbols, market)

    if _is_cache_fresh(key):
        _, cached = _price_cache[key]
        return cached

    try:
        upper_market = market.upper()
        if upper_market == "KRX":
            if _kis_available():
                prices = await _fetch_krx_kis(symbols)
            else:
                prices = await _fetch_krx_pykrx(symbols)
        else:
            if _kis_available():
                prices = await _fetch_us_kis(symbols)
            else:
                prices = await _fetch_us_yfinance(symbols)

        if prices:
            _price_cache[key] = (_now_utc(), prices)
            _stale_cache[key] = prices
            # DB에 비동기 저장 (실패해도 응답에 영향 없음)
            asyncio.create_task(_save_price_history(prices))
            asyncio.create_task(_cleanup_old_price_history())

        return prices

    except Exception as exc:
        logger.error("시세 조회 전체 실패 [%s/%s]: %s", market, symbols, exc)
        if key in _stale_cache:
            stale = _stale_cache[key]
            return [p.model_copy(update={"is_stale": True}) for p in stale]
        return []


def get_cache_ttl_remaining(symbols: list[str], market: str) -> int:
    """캐시 TTL 잔여 시간(초) 반환"""
    key = _cache_key(symbols, market)
    return _seconds_until_refresh(key)
