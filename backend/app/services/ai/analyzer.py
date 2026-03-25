from __future__ import annotations

"""AI 분석기 모듈.

OpenAI GPT 또는 Anthropic Claude를 사용하여
버핏 스타일 투자 코멘트를 생성합니다.
"""

import json
from typing import Any, Optional

from app.config import get_settings
from app.schemas.analysis import (
    IntrinsicValue,
    MoatAssessment,
    ProfitabilityMetrics,
    ValuationMetrics,
)
from app.services.ai.prompts import (
    BUFFETT_SYSTEM_PROMPT,
    build_value_analysis_prompt,
)


class AIAnalyzer:
    """LLM 기반 투자 분석기"""

    def __init__(self) -> None:
        self._settings = get_settings()

    async def generate_buffett_commentary(
        self,
        symbol: str,
        valuation: ValuationMetrics,
        profitability: ProfitabilityMetrics,
        moat: MoatAssessment,
        intrinsic: IntrinsicValue,
        company_name: str = "",
    ) -> str:
        """버핏 스타일 투자 코멘트 생성

        Args:
            symbol: 종목코드
            valuation: 밸류에이션 지표
            profitability: 수익성 지표
            moat: 경제적 해자 평가
            intrinsic: 내재가치 계산 결과
            company_name: 기업명

        Returns:
            AI 생성 코멘트 문자열
        """
        user_prompt = build_value_analysis_prompt(
            symbol=symbol,
            company_name=company_name or symbol,
            valuation=valuation,
            profitability=profitability,
            moat=moat,
            intrinsic=intrinsic,
        )

        if self._settings.openai_api_key:
            return await self._call_openai(user_prompt)

        if self._settings.anthropic_api_key:
            return await self._call_claude(user_prompt)

        return "AI 분석을 위해 OPENAI_API_KEY 또는 ANTHROPIC_API_KEY를 설정해 주세요."

    async def _call_openai(self, user_prompt: str) -> str:
        """OpenAI Chat Completions API 호출"""
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:
            raise RuntimeError("openai 패키지가 필요합니다: pip install openai") from exc

        client = AsyncOpenAI(api_key=self._settings.openai_api_key)
        response = await client.chat.completions.create(
            model=self._settings.openai_model,
            messages=[
                {"role": "system", "content": BUFFETT_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=600,
            temperature=0.7,
        )
        content = response.choices[0].message.content
        return content if content is not None else ""

    async def _call_claude(self, user_prompt: str) -> str:
        """Anthropic Claude API 호출"""
        try:
            import anthropic
        except ImportError as exc:
            raise RuntimeError("anthropic 패키지가 필요합니다: pip install anthropic") from exc

        client = anthropic.AsyncAnthropic(api_key=self._settings.anthropic_api_key)
        message = await client.messages.create(
            model=self._settings.anthropic_model,
            max_tokens=600,
            system=BUFFETT_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        block = message.content[0]
        if hasattr(block, "text"):
            return block.text
        return ""

    async def parse_json_response(self, raw: str) -> dict[str, Any]:
        """LLM 응답에서 JSON 블록 추출 및 파싱"""
        raw = raw.strip()
        # ```json ... ``` 블록 제거
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(
                line for line in lines if not line.startswith("```")
            ).strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"AI 응답 JSON 파싱 실패: {exc}\n원문: {raw}") from exc
