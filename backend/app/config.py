from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── 앱 기본 설정 ──────────────────────────────────────────────
    app_name: str = "오마하부자 API"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: Literal["development", "production", "test"] = "development"

    # ── CORS ──────────────────────────────────────────────────────
    allowed_origins: list[str] = [
        "http://localhost:3101",
    ]

    # ── KIS (한국투자증권) API ────────────────────────────────────
    kis_app_key: str = ""
    kis_app_secret: str = ""
    kis_account_no: str = ""          # 계좌번호 (8자리-2자리)
    kis_is_virtual: bool = True       # True=모의, False=실전

    @property
    def kis_base_url(self) -> str:
        if self.kis_is_virtual:
            return "https://openapivts.koreainvestment.com:29443"
        return "https://openapi.koreainvestment.com:9443"

    # ── OpenAI ───────────────────────────────────────────────────
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # ── Anthropic (Claude) ────────────────────────────────────────
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20241022"

    # ── DART (전자공시) ───────────────────────────────────────────
    dart_api_key: str = ""

    # ── Supabase (Stage 2) ────────────────────────────────────────
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""

    # ── Redis (캐시, 선택) ────────────────────────────────────────
    redis_url: str = "redis://localhost:6379"

    # ── 분석 파라미터 기본값 ──────────────────────────────────────
    dcf_discount_rate: float = 0.10    # DCF 할인율 10%
    dcf_growth_years: int = 10         # 성장기간 10년
    dcf_terminal_growth: float = 0.03  # 영구성장률 3%


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
