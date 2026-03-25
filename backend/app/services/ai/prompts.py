from __future__ import annotations

"""워렌 버핏 스타일 AI 분석 프롬프트 템플릿."""

from app.schemas.analysis import (
    IntrinsicValue,
    MoatAssessment,
    ProfitabilityMetrics,
    ValuationMetrics,
)

BUFFETT_SYSTEM_PROMPT = """당신은 워렌 버핏의 투자 철학을 깊이 이해하는 가치투자 분석가입니다.

핵심 원칙:
1. 사업을 이해할 수 있는가? (Circle of Competence)
2. 경제적 해자(Economic Moat)가 있는가?
3. 믿을 수 있는 경영진인가?
4. 합리적인 가격에 살 수 있는가? (Margin of Safety ≥ 25%)

분석 스타일:
- 장기(5~10년) 관점으로 분석
- 단기 주가 변동보다 사업의 본질에 집중
- 복잡한 금융 용어보다 쉬운 언어로 설명
- 투자 의견에 근거를 명확히 제시
- 리스크를 솔직하게 언급

금지 사항:
- 단정적 예측 ("반드시", "확실히") 사용 금지
- 단기 시세 예측 금지
- 근거 없는 낙관론 금지"""


def build_value_analysis_prompt(
    symbol: str,
    company_name: str,
    valuation: ValuationMetrics,
    profitability: ProfitabilityMetrics,
    moat: MoatAssessment,
    intrinsic: IntrinsicValue,
) -> str:
    """가치투자 종합 분석 프롬프트 생성"""
    margin_pct = f"{intrinsic.margin_of_safety:.1f}%"
    verdict_kor = {
        "WIDE": "넓은 해자",
        "NARROW": "좁은 해자",
        "NONE": "해자 없음",
    }.get(moat.moat_strength, moat.moat_strength)

    advantages_str = (
        "\n".join(f"  - {a}" for a in moat.competitive_advantages)
        if moat.competitive_advantages
        else "  - 확인된 경쟁 우위 없음"
    )
    risks_str = (
        "\n".join(f"  - {r}" for r in moat.risks)
        if moat.risks
        else "  - 특별한 리스크 없음"
    )

    return f"""다음 재무 데이터를 바탕으로 {company_name} ({symbol})에 대한 버핏 스타일 가치투자 분석을 해주세요.

## 밸류에이션 지표
- PER: {valuation.per or 'N/A'}
- PBR: {valuation.pbr or 'N/A'}
- EV/EBITDA: {valuation.ev_ebitda or 'N/A'}
- 배당수익률: {valuation.dividend_yield or 'N/A'}%

## 수익성 지표
- ROE: {profitability.roe or 'N/A'}%
- 영업이익률: {profitability.operating_margin or 'N/A'}%
- 순이익률: {profitability.net_margin or 'N/A'}%

## 경제적 해자
- 해자 강도: {verdict_kor}
- ROE 일관성: {'5년 평균 15% 이상 유지' if moat.roe_consistency else '불안정'}
- 이익률 추세: {moat.margin_trend}
- 경쟁 우위:
{advantages_str}
- 리스크:
{risks_str}

## 내재가치
- 현재 주가: {intrinsic.current_price:,}원
- DCF 내재가치: {intrinsic.intrinsic_value:,.0f}원
- 안전마진: {margin_pct}
- 저평가 여부: {'저평가' if intrinsic.is_undervalued else '고평가 또는 적정'}

위 데이터를 분석하여 다음을 포함한 300자 내외의 투자 코멘트를 작성해 주세요:
1. 이 기업의 핵심 투자 매력 (또는 우려)
2. 현재 가격 수준에 대한 평가
3. 버핏이라면 어떻게 접근할지

한국어로 작성하고, 성향 언어를 사용하세요 (단정적 표현 금지)."""


def build_moat_analysis_prompt(
    symbol: str,
    company_name: str,
    industry: str,
    moat: MoatAssessment,
    profitability: ProfitabilityMetrics,
) -> str:
    """경제적 해자 심층 분석 프롬프트"""
    return f"""워렌 버핏의 경제적 해자 프레임워크로 {company_name} ({symbol}, {industry} 섹터)를 분석해 주세요.

## 현재 해자 평가
- 해자 강도: {moat.moat_strength}
- ROE 일관성: {moat.roe_consistency}
- 이익률 추세: {moat.margin_trend}
- ROE: {profitability.roe or 'N/A'}%
- 영업이익률: {profitability.operating_margin or 'N/A'}%

다음 해자 유형 중 해당되는 것을 분석해 주세요:
1. 브랜드 파워 (pricing power)
2. 네트워크 효과
3. 전환 비용 (switching costs)
4. 비용 우위 (cost advantage)
5. 효율적 규모 (efficient scale)
6. 무형자산 (특허, 라이선스)

200자 내외로 핵심만 설명해 주세요."""


def build_news_sentiment_prompt(news_items: list[str]) -> str:
    """뉴스 센티먼트 분석 프롬프트"""
    news_text = "\n".join(f"{i+1}. {item}" for i, item in enumerate(news_items))
    return f"""다음 뉴스 헤드라인들을 분석하여 장기 가치투자 관점에서 센티먼트를 평가해 주세요.

뉴스 목록:
{news_text}

다음 JSON 형식으로만 응답해 주세요:
{{
  "overall_sentiment": "POSITIVE|NEUTRAL|NEGATIVE",
  "sentiment_score": 0.0에서 1.0 사이 숫자,
  "key_themes": ["테마1", "테마2"],
  "investment_implication": "투자 관점에서 함의 (100자 이내)",
  "long_term_impact": "HIGH|MEDIUM|LOW"
}}"""
