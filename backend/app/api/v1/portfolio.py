from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.schemas.portfolio import (
    DiversificationAnalysis,
    PortfolioAddRequest,
    PortfolioSummary,
)

router = APIRouter()

# 인메모리 포트폴리오 저장소 (Stage 2에서 Supabase로 교체)
_portfolio_store: list[PortfolioAddRequest] = []


@router.get(
    "/",
    response_model=PortfolioSummary,
    summary="포트폴리오 조회",
    description="보유 종목 목록과 평가 손익을 조회합니다.",
)
async def get_portfolio() -> PortfolioSummary:
    # TODO: Supabase 연동 후 사용자별 포트폴리오 조회 (Stage 2)
    return PortfolioSummary(
        total_invested=0.0,
        total_market_value=0.0,
        total_unrealized_pnl=0.0,
        total_unrealized_pnl_rate=0.0,
        items=[],
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="종목 추가",
    description="포트폴리오에 종목을 추가합니다.",
)
async def add_to_portfolio(request: PortfolioAddRequest) -> dict[str, str]:
    _portfolio_store.append(request)
    return {"message": f"{request.symbol} 추가 완료"}


@router.delete(
    "/{symbol}",
    summary="종목 제거",
    description="포트폴리오에서 종목을 제거합니다.",
)
async def remove_from_portfolio(symbol: str) -> dict[str, str]:
    global _portfolio_store
    before = len(_portfolio_store)
    _portfolio_store = [item for item in _portfolio_store if item.symbol != symbol]
    if len(_portfolio_store) == before:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{symbol} 종목을 찾을 수 없습니다.",
        )
    return {"message": f"{symbol} 제거 완료"}


@router.get(
    "/diversification",
    response_model=DiversificationAnalysis,
    summary="분산투자 분석",
    description="포트폴리오의 섹터 분산도와 집중 리스크를 분석합니다.",
)
async def analyze_diversification() -> DiversificationAnalysis:
    return DiversificationAnalysis(
        sector_weights={},
        top_holdings_weight=0.0,
        herfindahl_index=0.0,
        recommendation="포트폴리오 데이터를 추가하면 분석이 가능합니다.",
    )
