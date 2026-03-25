from __future__ import annotations

"""뉴스 센티먼트 분석 서비스.

현재는 구조만 구성. Stage 2에서 뉴스 API (Naver, Google News, Yahoo Finance)
연동 후 실데이터로 교체 예정.
"""

from typing import Any, Optional

from app.services.ai.analyzer import AIAnalyzer
from app.services.ai.prompts import build_news_sentiment_prompt


class NewsSentimentService:
    """뉴스 수집 및 센티먼트 분석 서비스"""

    def __init__(self) -> None:
        self._ai = AIAnalyzer()

    async def get_news_with_sentiment(
        self, symbol: str, limit: int = 10
    ) -> dict[str, Any]:
        """종목 관련 뉴스 + 센티먼트 분석

        Args:
            symbol: 종목코드
            limit: 뉴스 개수

        Returns:
            뉴스 목록과 센티먼트 분석 결과
        """
        # TODO: 실제 뉴스 API 연동 (Stage 2)
        # 현재는 Mock 응답
        mock_news = [
            {
                "title": f"{symbol} 관련 뉴스 (Mock)",
                "summary": "실제 뉴스 API 연동 후 표시됩니다.",
                "published_at": "2026-03-25T09:00:00+09:00",
                "source": "Mock",
                "url": "",
            }
        ]

        return {
            "symbol": symbol,
            "news": mock_news[:limit],
            "sentiment": {
                "overall": "NEUTRAL",
                "score": 0.5,
                "note": "뉴스 API 연동 전 Mock 데이터입니다.",
            },
        }

    async def analyze_sentiment(self, headlines: list[str]) -> dict[str, Any]:
        """뉴스 헤드라인 목록의 센티먼트 AI 분석

        Args:
            headlines: 뉴스 헤드라인 목록

        Returns:
            센티먼트 분석 결과 딕셔너리
        """
        if not headlines:
            return {
                "overall_sentiment": "NEUTRAL",
                "sentiment_score": 0.5,
                "key_themes": [],
                "investment_implication": "분석할 뉴스가 없습니다.",
                "long_term_impact": "LOW",
            }

        prompt = build_news_sentiment_prompt(headlines)
        raw_response = await self._ai._call_openai(prompt) if self._ai._settings.openai_api_key else ""

        if not raw_response:
            return {
                "overall_sentiment": "NEUTRAL",
                "sentiment_score": 0.5,
                "key_themes": [],
                "investment_implication": "AI 키가 설정되지 않아 분석 불가.",
                "long_term_impact": "LOW",
            }

        return await self._ai.parse_json_response(raw_response)

    async def get_market_summary(self, market: str = "KR") -> dict[str, Any]:
        """시장 전반 뉴스 요약

        Args:
            market: 시장 구분 (KR/US)

        Returns:
            시장 뉴스 요약
        """
        # TODO: 실제 시장 뉴스 수집 (Stage 2)
        return {
            "market": market,
            "summary": "시장 뉴스 API 연동 후 제공됩니다.",
            "overall_sentiment": "NEUTRAL",
            "top_movers": [],
            "key_events": [],
        }
