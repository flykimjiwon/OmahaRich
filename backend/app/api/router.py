from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import analysis, news, portfolio, realtime, stocks

api_router = APIRouter()

api_router.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(realtime.router, prefix="/realtime", tags=["realtime"])
