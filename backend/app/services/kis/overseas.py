from __future__ import annotations

from app.schemas.stock import StockPrice
from app.services.kis.client import KISClient


# 해외 거래소 코드 매핑
EXCHANGE_CODE_MAP: dict[str, str] = {
    "NASDAQ": "NAS",
    "NYSE": "NYS",
    "AMEX": "AMS",
    "TOKYO": "TSE",
    "SHANGHAI": "SHS",
    "HONGKONG": "HKS",
}


class KISOverseasService:
    """해외 주식 시세 서비스 (KIS Open API)"""

    _PRICE_PATH = "/uapi/overseas-price/v1/quotations/price"
    _DAILY_PRICE_PATH = "/uapi/overseas-price/v1/quotations/dailyprice"

    # 실전 TR
    _TR_PRICE = "HHDFS76200200"
    _TR_DAILY = "HHDFS76240000"

    def __init__(self) -> None:
        self._client = KISClient()

    async def get_stock_price(
        self, symbol: str, exchange: str = "NASDAQ"
    ) -> StockPrice:
        """해외 주식 현재가 조회

        Args:
            symbol: 해외 종목코드 (예: "AAPL")
            exchange: 거래소 코드 (NASDAQ/NYSE/AMEX 등)

        Returns:
            StockPrice 스키마
        """
        excd = EXCHANGE_CODE_MAP.get(exchange.upper(), exchange)

        params = {
            "AUTH": "",
            "EXCD": excd,
            "SYMB": symbol,
        }

        data = await self._client.get(
            self._PRICE_PATH,
            tr_id=self._TR_PRICE,
            params=params,
        )

        rt_cd = data.get("rt_cd", "")
        if rt_cd != "0":
            msg = data.get("msg1", "알 수 없는 오류")
            raise RuntimeError(msg)

        output = data.get("output", {})
        current_price_str = output.get("last", "0")
        current_price = int(float(current_price_str))
        prev_close_str = output.get("base", "0")
        prev_close = int(float(prev_close_str))
        change = current_price - prev_close
        change_rate = (
            round(change / prev_close * 100, 2) if prev_close != 0 else 0.0
        )

        return StockPrice(
            symbol=symbol,
            name=output.get("rsym", symbol),
            current_price=current_price,
            change=change,
            change_rate=change_rate,
            volume=int(output.get("tvol", 0)),
            market_cap=None,
            high_price=int(float(output.get("high", 0))),
            low_price=int(float(output.get("low", 0))),
            open_price=int(float(output.get("open", 0))),
            prev_close=prev_close,
        )
