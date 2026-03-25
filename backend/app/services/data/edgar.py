from __future__ import annotations

"""SEC EDGAR 연동 모듈.

미국 주식 재무 데이터를 SEC EDGAR API(무료)로 조회합니다.
별도 API 키 불필요. User-Agent 헤더 필수.
"""

from typing import Any

import httpx

_EDGAR_BASE = "https://data.sec.gov"
_COMPANY_FACTS_URL = f"{_EDGAR_BASE}/api/xbrl/companyfacts/CIK{{cik}}.json"
_COMPANY_TICKERS_URL = f"{_EDGAR_BASE}/submissions/CIK{{cik}}.json"

# SEC 요구사항: User-Agent에 연락처 명시
_USER_AGENT = "OmahaRich/0.1 contact@omaharich.com"


async def _get(url: str) -> dict[str, Any]:
    headers = {"User-Agent": _USER_AGENT, "Accept": "application/json"}
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(url, headers=headers)

    if response.status_code == 404:
        raise ValueError(f"EDGAR: 데이터를 찾을 수 없습니다 — {url}")
    if response.status_code != 200:
        raise RuntimeError(
            f"EDGAR API 오류: HTTP {response.status_code}"
        )
    return response.json()


def _pad_cik(cik: str | int) -> str:
    """CIK를 10자리 zero-padding 형식으로 변환"""
    return str(cik).zfill(10)


async def get_company_facts(cik: str | int) -> dict[str, Any]:
    """SEC EDGAR에서 기업의 전체 XBRL 재무 팩트 조회

    Args:
        cik: SEC CIK 번호 (예: 789019 = Microsoft)

    Returns:
        XBRL 팩트 딕셔너리 (us-gaap, dei 등)
    """
    url = _COMPANY_FACTS_URL.format(cik=_pad_cik(cik))
    return await _get(url)


async def get_eps_history(cik: str | int) -> list[dict[str, Any]]:
    """연간 EPS(희석) 이력 조회

    Args:
        cik: SEC CIK 번호

    Returns:
        EPS 이력 목록 [{end, val, form, filed}, ...]
    """
    facts = await get_company_facts(cik)
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    eps_data = us_gaap.get("EarningsPerShareDiluted", {})
    units = eps_data.get("units", {})
    usd_eps = units.get("USD/shares", [])

    # 연간 보고서(10-K)만 필터링
    annual = [
        item for item in usd_eps
        if item.get("form") in {"10-K", "20-F"}
    ]
    # 최신 순 정렬
    annual.sort(key=lambda x: x.get("end", ""), reverse=True)
    return annual


async def get_revenue_history(cik: str | int) -> list[dict[str, Any]]:
    """연간 매출 이력 조회

    Returns:
        매출 이력 목록 (단위: USD)
    """
    facts = await get_company_facts(cik)
    us_gaap = facts.get("facts", {}).get("us-gaap", {})

    # 매출 계정명은 기업마다 다를 수 있음
    for key in ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"):
        revenue_data = us_gaap.get(key, {})
        units = revenue_data.get("units", {})
        usd_rev = units.get("USD", [])
        if usd_rev:
            annual = [
                item for item in usd_rev
                if item.get("form") in {"10-K", "20-F"}
            ]
            annual.sort(key=lambda x: x.get("end", ""), reverse=True)
            return annual

    return []


async def search_cik_by_ticker(ticker: str) -> str | None:
    """티커로 CIK 검색

    Args:
        ticker: 주식 티커 (예: "AAPL")

    Returns:
        CIK 문자열 또는 None
    """
    url = "https://efts.sec.gov/LATEST/search-index?q=%22" + ticker + "%22&dateRange=custom&startdt=2020-01-01&forms=10-K"
    # 간단하게 tickers.json 사용
    tickers_url = "https://www.sec.gov/files/company_tickers.json"
    headers = {"User-Agent": _USER_AGENT}

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(tickers_url, headers=headers)

    if response.status_code != 200:
        return None

    data: dict[str, dict[str, str | int]] = response.json()
    ticker_upper = ticker.upper()

    for entry in data.values():
        if str(entry.get("ticker", "")).upper() == ticker_upper:
            return _pad_cik(entry["cik_str"])

    return None
