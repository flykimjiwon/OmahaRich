from __future__ import annotations

from typing import Any

import httpx

from app.config import get_settings
from app.services.kis.auth import KISAuthManager

_auth_manager = KISAuthManager()


class KISClient:
    """KIS Open API httpx 비동기 클라이언트.

    - 실전/모의 도메인 자동 전환
    - 토큰 자동 갱신
    - 공통 헤더 주입
    """

    def __init__(self) -> None:
        self._settings = get_settings()
        self._auth = _auth_manager

    @property
    def base_url(self) -> str:
        return self._settings.kis_base_url

    async def _build_headers(
        self,
        tr_id: str,
        extra_headers: dict[str, str] | None = None,
    ) -> dict[str, str]:
        access_token = await self._auth.get_access_token()
        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {access_token}",
            "appkey": self._settings.kis_app_key,
            "appsecret": self._settings.kis_app_secret,
            "tr_id": tr_id,
            "custtype": "P",  # 개인
        }
        if extra_headers:
            headers.update(extra_headers)
        return headers

    async def get(
        self,
        path: str,
        tr_id: str,
        params: dict[str, str] | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """GET 요청. 토큰 만료 시 1회 재시도."""
        headers = await self._build_headers(tr_id, extra_headers)

        async with httpx.AsyncClient(
            base_url=self.base_url, timeout=15.0
        ) as client:
            response = await client.get(path, headers=headers, params=params)

        if response.status_code == 401:
            # 토큰 갱신 후 1회 재시도
            self._auth.invalidate()
            headers = await self._build_headers(tr_id, extra_headers)
            async with httpx.AsyncClient(
                base_url=self.base_url, timeout=15.0
            ) as client:
                response = await client.get(path, headers=headers, params=params)

        if response.status_code != 200:
            raise RuntimeError(
                f"KIS API 오류 [{tr_id}]: HTTP {response.status_code} — {response.text}"
            )

        return response.json()  # type: ignore[no-any-return]

    async def post(
        self,
        path: str,
        tr_id: str,
        body: dict[str, Any] | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """POST 요청."""
        headers = await self._build_headers(tr_id, extra_headers)

        async with httpx.AsyncClient(
            base_url=self.base_url, timeout=15.0
        ) as client:
            response = await client.post(
                path, headers=headers, json=body or {}
            )

        if response.status_code != 200:
            raise RuntimeError(
                f"KIS API 오류 [{tr_id}]: HTTP {response.status_code} — {response.text}"
            )

        return response.json()  # type: ignore[no-any-return]
