from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas.analysis import IntrinsicValue, MoatAssessment, ValueAnalysis
from app.services.analysis.value import ValueAnalysisService

logger = logging.getLogger(__name__)

router = APIRouter()


def get_value_service() -> ValueAnalysisService:
    return ValueAnalysisService()


# ── 분석 이력 저장 헬퍼 ───────────────────────────────────────────

async def _save_analysis_history(
    symbol: str,
    analysis_type: str,
    result: ValueAnalysis | MoatAssessment | IntrinsicValue,
    score: float,
    recommendation: str,
) -> None:
    """분석 결과를 analysis_history 테이블에 저장."""
    try:
        from app.database import get_session_factory
        from app.models.db import AnalysisHistory

        result_json = result.model_dump_json()
        factory = get_session_factory()
        async with factory() as session:
            session.add(
                AnalysisHistory(
                    symbol=symbol.upper(),
                    market="",
                    analysis_type=analysis_type,
                    result_json=result_json,
                    score=score,
                    recommendation=recommendation,
                    created_at=datetime.now(tz=timezone.utc),
                )
            )
            await session.commit()
    except Exception as exc:
        logger.warning("analysis_history 저장 실패 [%s/%s]: %s", symbol, analysis_type, exc)


def _history_row_to_dict(row: object) -> dict[str, object]:
    from app.models.db import AnalysisHistory

    r: AnalysisHistory = row  # type: ignore[assignment]
    return {
        "id": r.id,
        "symbol": r.symbol,
        "market": r.market,
        "analysis_type": r.analysis_type,
        "score": r.score,
        "recommendation": r.recommendation,
        "result": json.loads(r.result_json),
        "created_at": r.created_at.isoformat() if r.created_at else None,
    }


# ── 분석 이력 조회 (고정 경로 먼저 — /{symbol} 보다 앞에 위치해야 함) ──

@router.get(
    "/history",
    summary="전체 분석 이력 조회",
    description="최근 분석 이력 목록을 반환합니다 (최대 100건, 최신순).",
)
async def get_analysis_history(
    limit: Annotated[int, Query(description="최대 조회 수", ge=1, le=100)] = 50,
) -> list[dict[str, object]]:
    try:
        from sqlalchemy import select

        from app.database import get_session_factory
        from app.models.db import AnalysisHistory

        factory = get_session_factory()
        async with factory() as session:
            result = await session.execute(
                select(AnalysisHistory)
                .order_by(AnalysisHistory.created_at.desc())
                .limit(limit)
            )
            rows = result.scalars().all()
            return [_history_row_to_dict(r) for r in rows]
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"이력 조회 오류: {exc}",
        ) from exc


@router.get(
    "/history/{symbol}",
    summary="종목별 분석 이력 조회",
    description="특정 종목의 분석 이력을 최신순으로 반환합니다 (최대 50건).",
)
async def get_analysis_history_by_symbol(
    symbol: str,
    limit: Annotated[int, Query(description="최대 조회 수", ge=1, le=50)] = 20,
) -> list[dict[str, object]]:
    try:
        from sqlalchemy import select

        from app.database import get_session_factory
        from app.models.db import AnalysisHistory

        factory = get_session_factory()
        async with factory() as session:
            result = await session.execute(
                select(AnalysisHistory)
                .where(AnalysisHistory.symbol == symbol.upper())
                .order_by(AnalysisHistory.created_at.desc())
                .limit(limit)
            )
            rows = result.scalars().all()
            return [_history_row_to_dict(r) for r in rows]
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"이력 조회 오류: {exc}",
        ) from exc


# ── 분석 엔드포인트 (/{symbol}/... 경로) ─────────────────────────

@router.get(
    "/{symbol}/value",
    response_model=ValueAnalysis,
    summary="가치투자 종합 분석",
    description="버핏 스타일 가치투자 지표 (PER, PBR, ROE, 모트 등) 종합 분석.",
)
async def analyze_value(
    symbol: str,
    service: Annotated[ValueAnalysisService, Depends(get_value_service)],
    include_ai: Annotated[
        bool, Query(description="AI 코멘트 포함 여부")
    ] = False,
) -> ValueAnalysis:
    try:
        result = await service.analyze_value(symbol, include_ai=include_ai)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"분석 오류: {exc}",
        ) from exc

    import asyncio
    asyncio.create_task(
        _save_analysis_history(
            symbol=symbol,
            analysis_type="value",
            result=result,
            score=result.overall_score,
            recommendation=result.verdict,
        )
    )
    return result


@router.get(
    "/{symbol}/intrinsic-value",
    response_model=IntrinsicValue,
    summary="내재가치 (DCF) 계산",
    description="EPS와 성장률 기반 간략 DCF 내재가치 계산.",
)
async def get_intrinsic_value(
    symbol: str,
    service: Annotated[ValueAnalysisService, Depends(get_value_service)],
    growth_rate: Annotated[
        Optional[float],
        Query(description="커스텀 성장률 (없으면 자동 추정)", ge=0.0, le=1.0),
    ] = None,
) -> IntrinsicValue:
    try:
        result = await service.get_intrinsic_value(symbol, growth_rate=growth_rate)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    import asyncio
    asyncio.create_task(
        _save_analysis_history(
            symbol=symbol,
            analysis_type="intrinsic",
            result=result,
            score=result.margin_of_safety,
            recommendation="BUY" if result.is_undervalued else "HOLD",
        )
    )
    return result


@router.get(
    "/{symbol}/moat",
    response_model=MoatAssessment,
    summary="경제적 해자 분석",
    description="ROE 일관성, 마진 추세, 경쟁우위 등 경제적 해자 평가.",
)
async def get_moat_assessment(
    symbol: str,
    service: Annotated[ValueAnalysisService, Depends(get_value_service)],
) -> MoatAssessment:
    try:
        result = await service.check_moat(symbol)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    moat_score = {"WIDE": 80.0, "NARROW": 50.0, "NONE": 20.0}.get(result.moat_strength, 50.0)
    import asyncio
    asyncio.create_task(
        _save_analysis_history(
            symbol=symbol,
            analysis_type="moat",
            result=result,
            score=moat_score,
            recommendation="BUY" if result.has_moat else "HOLD",
        )
    )
    return result
