from __future__ import annotations

"""SQLAlchemy ORM 테이블 모델.

테이블 목록:
- watchlist        : 관심 종목
- price_history    : 시세 히스토리 캐싱
- analysis_history : 가치투자 분석 이력
- portfolio        : 보유 종목 포트폴리오
- settings         : 사용자 설정 (key-value)
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


# ── watchlist ─────────────────────────────────────────────────────

class WatchlistItem(Base):
    __tablename__ = "watchlist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    market: Mapped[str] = mapped_column(String(10), nullable=False)  # KRX / NASDAQ / NYSE
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )


# ── price_history ─────────────────────────────────────────────────

class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    change: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    change_percent: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    volume: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    per: Mapped[float | None] = mapped_column(Float, nullable=True)
    pbr: Mapped[float | None] = mapped_column(Float, nullable=True)
    market_cap: Mapped[float | None] = mapped_column(Float, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, index=True
    )


# ── analysis_history ──────────────────────────────────────────────

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    market: Mapped[str] = mapped_column(String(10), nullable=False, default="")
    analysis_type: Mapped[str] = mapped_column(
        String(20), nullable=False, default="value"
    )  # value / moat / intrinsic
    result_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    recommendation: Mapped[str] = mapped_column(
        String(20), nullable=False, default="HOLD"
    )  # STRONG_BUY / BUY / HOLD / SELL / STRONG_SELL
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, index=True
    )


# ── portfolio ─────────────────────────────────────────────────────

class PortfolioItem(Base):
    __tablename__ = "portfolio"
    __table_args__ = (UniqueConstraint("symbol", "buy_date", name="uq_portfolio_symbol_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    market: Mapped[str] = mapped_column(String(10), nullable=False, default="")
    buy_price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    buy_date: Mapped[str] = mapped_column(String(10), nullable=False)  # YYYY-MM-DD
    memo: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow
    )


# ── settings ──────────────────────────────────────────────────────

class Setting(Base):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False, default="")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow
    )
