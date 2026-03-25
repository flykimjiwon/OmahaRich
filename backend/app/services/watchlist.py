from __future__ import annotations

"""워치리스트 서비스 — SQLite CRUD 기반.

이전 인메모리 dict 방식에서 SQLAlchemy async로 전환.
공개 인터페이스(get_korean_symbols, get_us_symbols, add_symbol, remove_symbol)는
기존 호출 코드(api/v1/realtime.py)와 완전히 호환된다.
"""

import logging
from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError

from app.database import get_session_factory
from app.models.db import WatchlistItem

logger = logging.getLogger(__name__)

# ── 기본 종목 (첫 실행 시 자동 삽입) ─────────────────────────────

_DEFAULT_ITEMS: list[tuple[str, str, str]] = [
    # (symbol, name, market)
    ("005930", "삼성전자", "KRX"),
    ("000660", "SK하이닉스", "KRX"),
    ("373220", "LG에너지솔루션", "KRX"),
    ("AAPL", "Apple Inc.", "NASDAQ"),
    ("MSFT", "Microsoft Corp.", "NASDAQ"),
    ("NVDA", "NVIDIA Corp.", "NASDAQ"),
    ("TSLA", "Tesla Inc.", "NASDAQ"),
]


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


# ── 초기화 ────────────────────────────────────────────────────────

async def seed_default_watchlist() -> None:
    """기본 종목이 없을 때만 삽입 (멱등)."""
    factory = get_session_factory()
    async with factory() as session:
        result = await session.execute(select(WatchlistItem).limit(1))
        if result.scalars().first() is not None:
            return  # 이미 데이터 있음

        for symbol, name, market in _DEFAULT_ITEMS:
            session.add(
                WatchlistItem(
                    symbol=symbol,
                    name=name,
                    market=market,
                    added_at=_utcnow(),
                )
            )
        await session.commit()
        logger.info("기본 워치리스트 %d개 종목 삽입 완료", len(_DEFAULT_ITEMS))


# ── 조회 ──────────────────────────────────────────────────────────

async def get_korean_symbols() -> list[str]:
    """KRX 워치리스트 종목코드 목록 반환."""
    factory = get_session_factory()
    async with factory() as session:
        result = await session.execute(
            select(WatchlistItem.symbol)
            .where(WatchlistItem.market == "KRX")
            .order_by(WatchlistItem.added_at)
        )
        return list(result.scalars().all())


async def get_us_symbols() -> list[str]:
    """NASDAQ / NYSE 워치리스트 종목코드 목록 반환."""
    factory = get_session_factory()
    async with factory() as session:
        result = await session.execute(
            select(WatchlistItem.symbol)
            .where(WatchlistItem.market.in_(["NASDAQ", "NYSE"]))
            .order_by(WatchlistItem.added_at)
        )
        return list(result.scalars().all())


async def get_all_items() -> list[WatchlistItem]:
    """전체 워치리스트 아이템 반환."""
    factory = get_session_factory()
    async with factory() as session:
        result = await session.execute(
            select(WatchlistItem).order_by(WatchlistItem.added_at)
        )
        return list(result.scalars().all())


# ── 추가 ──────────────────────────────────────────────────────────

async def add_symbol(symbol: str, market: str, name: str = "") -> bool:
    """워치리스트에 종목 추가.

    Args:
        symbol: 종목코드
        market: 시장 구분 (KRX / NASDAQ / NYSE)
        name: 종목명 (선택)

    Returns:
        True=추가됨, False=이미 존재
    """
    upper_market = market.upper()

    # NASDAQ / NYSE 모두 대문자 심볼로 정규화
    normalized_symbol = symbol if upper_market == "KRX" else symbol.upper()
    # market 정규화: NASDAQ/NYSE 외에는 KRX
    normalized_market = upper_market if upper_market in ("KRX", "NASDAQ", "NYSE") else "KRX"

    factory = get_session_factory()
    async with factory() as session:
        try:
            session.add(
                WatchlistItem(
                    symbol=normalized_symbol,
                    name=name,
                    market=normalized_market,
                    added_at=_utcnow(),
                )
            )
            await session.commit()
            return True
        except IntegrityError:
            await session.rollback()
            return False


# ── 제거 ──────────────────────────────────────────────────────────

async def remove_symbol(symbol: str) -> bool:
    """워치리스트에서 종목 제거.

    Args:
        symbol: 종목코드 (대소문자 무관)

    Returns:
        True=제거됨, False=존재하지 않음
    """
    factory = get_session_factory()
    async with factory() as session:
        # 한국 심볼 그대로, 미국 심볼은 대문자로도 시도
        candidates = {symbol, symbol.upper()}
        result = await session.execute(
            delete(WatchlistItem).where(WatchlistItem.symbol.in_(candidates))
        )
        await session.commit()
        return (result.rowcount or 0) > 0
