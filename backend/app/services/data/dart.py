from __future__ import annotations

"""DART (전자공시시스템) 연동 모듈.

OpenDartReader 라이브러리 또는 직접 HTTP 요청으로
재무제표, 공시 데이터를 조회합니다.
"""

from typing import Any, Optional

import httpx

from app.config import get_settings


class DARTClient:
    """DART Open API 클라이언트"""

    _BASE_URL = "https://opendart.fss.or.kr/api"

    def __init__(self) -> None:
        self._settings = get_settings()

    @property
    def _api_key(self) -> str:
        return self._settings.dart_api_key

    async def get_company_info(self, corp_code: str) -> dict[str, Any]:
        """기업 기본 정보 조회

        Args:
            corp_code: DART 고유번호 (8자리)

        Returns:
            기업 기본 정보 딕셔너리
        """
        params = {
            "crtfc_key": self._api_key,
            "corp_code": corp_code,
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                f"{self._BASE_URL}/company.json", params=params
            )

        if response.status_code != 200:
            raise RuntimeError(
                f"DART API 오류: HTTP {response.status_code}"
            )

        data: dict[str, Any] = response.json()
        if data.get("status") != "000":
            raise RuntimeError(f"DART 오류: {data.get('message', '알 수 없는 오류')}")

        return data

    async def get_financial_statements(
        self,
        corp_code: str,
        year: str,
        report_code: str = "11011",  # 11011=사업보고서
        fs_div: str = "CFS",         # CFS=연결, OFS=별도
    ) -> list[dict[str, Any]]:
        """재무제표 조회 (단일회사 주요계정)

        Args:
            corp_code: DART 고유번호
            year: 사업연도 (예: "2023")
            report_code: 보고서 코드 (11011=사업보고서)
            fs_div: 재무제표 구분 (CFS=연결, OFS=별도)

        Returns:
            재무제표 항목 목록
        """
        params = {
            "crtfc_key": self._api_key,
            "corp_code": corp_code,
            "bsns_year": year,
            "reprt_code": report_code,
            "fs_div": fs_div,
        }
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                f"{self._BASE_URL}/fnlttSinglAcntAll.json", params=params
            )

        if response.status_code != 200:
            raise RuntimeError(
                f"DART 재무제표 API 오류: HTTP {response.status_code}"
            )

        data: dict[str, Any] = response.json()
        if data.get("status") != "000":
            raise RuntimeError(
                f"DART 재무제표 오류: {data.get('message', '알 수 없는 오류')}"
            )

        return data.get("list", [])

    async def get_disclosures(
        self,
        corp_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page_no: int = 1,
        page_count: int = 10,
    ) -> dict[str, Any]:
        """공시 목록 조회

        Args:
            corp_code: DART 고유번호 (없으면 전체)
            start_date: 시작일 YYYYMMDD
            end_date: 종료일 YYYYMMDD
            page_no: 페이지 번호
            page_count: 페이지당 건수

        Returns:
            공시 목록 응답 딕셔너리
        """
        params: dict[str, str | int] = {
            "crtfc_key": self._api_key,
            "page_no": page_no,
            "page_count": page_count,
        }
        if corp_code:
            params["corp_code"] = corp_code
        if start_date:
            params["bgn_de"] = start_date
        if end_date:
            params["end_de"] = end_date

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                f"{self._BASE_URL}/list.json", params=params
            )

        if response.status_code != 200:
            raise RuntimeError(
                f"DART 공시 API 오류: HTTP {response.status_code}"
            )

        return response.json()
