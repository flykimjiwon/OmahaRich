from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional

import httpx

from app.config import get_settings


@dataclass
class TokenInfo:
    access_token: str
    token_type: str
    expires_in: int
    issued_at: float = field(default_factory=time.time)

    @property
    def is_expired(self) -> bool:
        # 만료 60초 전에 갱신 트리거
        return time.time() >= self.issued_at + self.expires_in - 60


class KISAuthManager:
    """KIS OAuth 토큰 발급 및 자동 갱신 관리자"""

    _TOKEN_PATH = "/oauth2/tokenP"

    def __init__(self) -> None:
        self._settings = get_settings()
        self._token_info: Optional[TokenInfo] = None

    async def get_access_token(self) -> str:
        """유효한 액세스 토큰 반환. 만료 시 자동 갱신."""
        if self._token_info is None or self._token_info.is_expired:
            await self._issue_token()
        assert self._token_info is not None
        return self._token_info.access_token

    async def _issue_token(self) -> None:
        """KIS OAuth 토큰 발급 요청"""
        url = f"{self._settings.kis_base_url}{self._TOKEN_PATH}"
        payload = {
            "grant_type": "client_credentials",
            "appkey": self._settings.kis_app_key,
            "appsecret": self._settings.kis_app_secret,
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload)

        if response.status_code != 200:
            raise RuntimeError(
                f"KIS 토큰 발급 실패: HTTP {response.status_code} — {response.text}"
            )

        data = response.json()

        if "access_token" not in data:
            raise RuntimeError(f"KIS 토큰 응답에 access_token 없음: {data}")

        self._token_info = TokenInfo(
            access_token=data["access_token"],
            token_type=data.get("token_type", "Bearer"),
            expires_in=int(data.get("expires_in", 86400)),
        )

    def invalidate(self) -> None:
        """토큰 강제 무효화 (재발급 강제)"""
        self._token_info = None
