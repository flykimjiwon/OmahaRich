from __future__ import annotations

from typing import Annotated, Optional

from fastapi import APIRouter, Query

from app.services.news.sentiment import NewsSentimentService

router = APIRouter()


def get_news_service() -> NewsSentimentService:
    return NewsSentimentService()


@router.get(
    "/{symbol}",
    summary="종목 관련 뉴스 조회",
    description="종목 관련 최신 뉴스와 센티먼트 분석 결과를 반환합니다.",
)
async def get_stock_news(
    symbol: str,
    limit: Annotated[int, Query(description="뉴스 개수", ge=1, le=50)] = 10,
) -> dict[str, object]:
    service = get_news_service()
    return await service.get_news_with_sentiment(symbol, limit=limit)


@router.get(
    "/market/summary",
    summary="시장 뉴스 요약",
    description="오늘의 주요 시장 뉴스와 전반적인 센티먼트를 요약합니다.",
)
async def get_market_news_summary(
    market: Annotated[
        Optional[str],
        Query(description="시장 구분 (KR/US)", pattern="^(KR|US)$"),
    ] = "KR",
) -> dict[str, object]:
    service = get_news_service()
    return await service.get_market_summary(market=market or "KR")
