from __future__ import annotations

"""SQLAlchemy 2.0 async 데이터베이스 설정.

DB 파일 경로: backend/data/omaha.db
드라이버: aiosqlite (async SQLite)
"""

import logging
from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger(__name__)

# ── 경로 설정 ──────────────────────────────────────────────────────
# 이 파일 기준: backend/app/database.py → backend/ = parent.parent
_BACKEND_DIR = Path(__file__).resolve().parent.parent
_DATA_DIR = _BACKEND_DIR / "data"
_DB_PATH = _DATA_DIR / "omaha.db"


def _get_database_url() -> str:
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    return f"sqlite+aiosqlite:///{_DB_PATH}"


# ── ORM Base ──────────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


# ── 엔진 & 세션 팩토리 ────────────────────────────────────────────

_engine: AsyncEngine | None = None
_async_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            _get_database_url(),
            echo=False,
            connect_args={"check_same_thread": False},
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    global _async_session_factory
    if _async_session_factory is None:
        _async_session_factory = async_sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )
    return _async_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI Depends 용 DB 세션 제공자."""
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    """앱 시작 시 모든 테이블 생성 (없으면 생성, 있으면 스킵)."""
    # 모든 모델을 임포트하여 Base.metadata에 등록
    from app.models import db as _  # noqa: F401

    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("DB 초기화 완료: %s", _DB_PATH)
