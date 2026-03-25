from __future__ import annotations

from app.schemas.stock import StockCandle, StockHistory, StockPrice
from app.services.kis.client import KISClient


class KISDomesticService:
    """국내 주식 시세 서비스 (KIS Open API)"""

    # ── 엔드포인트 ───────────────────────────────────────────────
    _PRICE_PATH = "/uapi/domestic-stock/v1/quotations/inquire-price"
    _DAILY_PRICE_PATH = "/uapi/domestic-stock/v1/quotations/inquire-daily-price"

    # ── TR ID ─────────────────────────────────────────────────────
    # 실전: FHKST01010100  모의: VTTC8801R (주의: 모의는 일부 TR 미지원)
    _TR_PRICE_REAL = "FHKST01010100"
    _TR_DAILY_PRICE = "FHKST01010400"

    def __init__(self) -> None:
        self._client = KISClient()

    @property
    def _tr_price(self) -> str:
        settings = self._client._settings
        return "FHKST01010100" if not settings.kis_is_virtual else "FHKST01010100"

    async def get_stock_price(self, symbol: str) -> StockPrice:
        """주식 현재가 시세 조회 (TR: FHKST01010100)

        Args:
            symbol: 종목코드 6자리 (예: "005930")

        Returns:
            StockPrice 스키마

        Raises:
            ValueError: 종목 미존재
            RuntimeError: KIS API 오류
        """
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",  # J=KRX
            "FID_INPUT_ISCD": symbol,
        }

        data = await self._client.get(
            self._PRICE_PATH,
            tr_id=self._tr_price,
            params=params,
        )

        rt_cd = data.get("rt_cd", "")
        if rt_cd != "0":
            msg = data.get("msg1", "알 수 없는 오류")
            if "종목" in msg or "코드" in msg:
                raise ValueError(f"종목을 찾을 수 없습니다: {symbol}")
            raise RuntimeError(msg)

        output = data.get("output", {})

        current_price = int(output.get("stck_prpr", 0))
        prev_close = int(output.get("stck_sdpr", 0))
        change = int(output.get("prdy_vrss", 0))
        change_rate = float(output.get("prdy_ctrt", 0.0))

        return StockPrice(
            symbol=symbol,
            name=output.get("hts_kor_isnm", symbol),
            current_price=current_price,
            change=change,
            change_rate=change_rate,
            volume=int(output.get("acml_vol", 0)),
            market_cap=int(output.get("hts_avls", 0)) * 100_000_000 or None,
            high_price=int(output.get("stck_hgpr", 0)),
            low_price=int(output.get("stck_lwpr", 0)),
            open_price=int(output.get("stck_oprc", 0)),
            prev_close=prev_close,
        )

    async def get_stock_history(
        self,
        symbol: str,
        period: str = "D",
        count: int = 60,
    ) -> StockHistory:
        """기간별 OHLCV 시세 조회 (TR: FHKST01010400)

        Args:
            symbol: 종목코드 6자리
            period: D(일) / W(주) / M(월) / Y(년)
            count: 조회 봉 수 (최대 500)

        Returns:
            StockHistory 스키마
        """
        period_map = {"D": "D", "W": "W", "M": "M", "Y": "Y"}
        fid_period = period_map.get(period, "D")

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
            "FID_PERIOD_DIV_CODE": fid_period,
            "FID_ORG_ADJ_PRC": "0",  # 0=수정주가
        }

        data = await self._client.get(
            self._DAILY_PRICE_PATH,
            tr_id=self._TR_DAILY_PRICE,
            params=params,
        )

        rt_cd = data.get("rt_cd", "")
        if rt_cd != "0":
            msg = data.get("msg1", "알 수 없는 오류")
            raise RuntimeError(msg)

        output2 = data.get("output2", []) or []
        candles: list[StockCandle] = []

        for row in output2[:count]:
            candles.append(
                StockCandle(
                    date=row.get("stck_bsop_date", ""),
                    open_price=int(row.get("stck_oprc", 0)),
                    high_price=int(row.get("stck_hgpr", 0)),
                    low_price=int(row.get("stck_lwpr", 0)),
                    close_price=int(row.get("stck_clpr", 0)),
                    volume=int(row.get("acml_vol", 0)),
                    change_rate=float(row.get("prdy_ctrt", 0.0)),
                )
            )

        output1 = data.get("output1", {}) or {}
        name = output1.get("hts_kor_isnm", symbol)

        return StockHistory(
            symbol=symbol,
            name=name,
            period=period,
            candles=candles,
        )
