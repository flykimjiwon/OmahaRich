from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config import get_settings
from app.database import init_db
from app.services.watchlist import seed_default_watchlist


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # 앱 시작 시 초기화
    await init_db()
    await seed_default_watchlist()
    yield
    # 앱 종료 시 정리


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="워렌 버핏 스타일 가치투자 AI 분석 플랫폼 API",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # ── CORS ──────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── 라우터 마운트 ─────────────────────────────────────────────
    app.include_router(api_router, prefix="/api/v1")

    # ── 헬스 체크 ─────────────────────────────────────────────────
    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        return {
            "status": "ok",
            "version": settings.app_version,
            "environment": settings.environment,
        }

    @app.get("/", tags=["root"])
    async def root() -> dict[str, str]:
        return {"message": "오마하부자 API", "docs": "/docs"}

    return app


app = create_app()
