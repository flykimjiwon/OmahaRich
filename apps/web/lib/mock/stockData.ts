import type { RealtimePricesResponse, StockPrice, MarketIndex } from "@/types/stock";

function randomDelta(base: number, pct: number): number {
  return base * (1 + (Math.random() - 0.5) * 2 * pct);
}

function makeKorean(
  symbol: string,
  name: string,
  basePrice: number,
  per: number | null,
  pbr: number | null,
  marketCapEok: number,
): StockPrice {
  const price = Math.round(randomDelta(basePrice, 0.02));
  const prevClose = Math.round(randomDelta(basePrice, 0.01));
  const change = price - prevClose;
  const changeRate = (change / prevClose) * 100;
  const volume = Math.floor(randomDelta(500_000, 0.4));
  return {
    symbol,
    name,
    market: "KRX",
    price,
    prevClose,
    change,
    changeRate,
    volume,
    marketCap: Math.round(randomDelta(marketCapEok, 0.01)),
    per,
    pbr,
    updatedAt: new Date().toISOString(),
  };
}

function makeUS(
  symbol: string,
  name: string,
  basePrice: number,
  per: number | null,
  pbr: number | null,
  marketCapM: number,
): StockPrice {
  const price = parseFloat(randomDelta(basePrice, 0.015).toFixed(2));
  const prevClose = parseFloat(randomDelta(basePrice, 0.008).toFixed(2));
  const change = parseFloat((price - prevClose).toFixed(2));
  const changeRate = parseFloat(((change / prevClose) * 100).toFixed(2));
  const volume = Math.floor(randomDelta(3_000_000, 0.5));
  return {
    symbol,
    name,
    market: symbol === "AAPL" || symbol === "MSFT" || symbol === "BRK.B" ? "NASDAQ" : "NYSE",
    price,
    prevClose,
    change,
    changeRate,
    volume,
    marketCap: Math.round(randomDelta(marketCapM, 0.01)),
    per,
    pbr,
    updatedAt: new Date().toISOString(),
  };
}

function makeIndex(
  name: string,
  base: number,
): MarketIndex {
  const value = parseFloat(randomDelta(base, 0.008).toFixed(2));
  const prevClose = parseFloat(randomDelta(base, 0.003).toFixed(2));
  const change = parseFloat((value - prevClose).toFixed(2));
  const changeRate = parseFloat(((change / prevClose) * 100).toFixed(2));
  return { name, value, change, changeRate };
}

export function getMockRealtimePrices(): RealtimePricesResponse {
  return {
    korean: [
      makeKorean("005930", "삼성전자", 71_500, 14.2, 1.1, 4_270_000),
      makeKorean("000660", "SK하이닉스", 182_000, 8.4, 1.6, 1_320_000),
      makeKorean("035420", "NAVER", 195_000, 28.1, 2.3, 320_000),
      makeKorean("051910", "LG화학", 312_000, 18.7, 0.9, 220_000),
      makeKorean("005380", "현대차", 218_000, 6.1, 0.6, 465_000),
      makeKorean("068270", "셀트리온", 148_500, 32.4, 3.2, 210_000),
    ],
    us: [
      makeUS("AAPL", "Apple", 189.5, 28.4, 45.2, 2_950_000),
      makeUS("MSFT", "Microsoft", 415.2, 35.1, 12.8, 3_080_000),
      makeUS("BRK.B", "Berkshire Hathaway", 358.0, 21.3, 1.4, 780_000),
      makeUS("KO", "Coca-Cola", 61.4, 22.6, 10.1, 265_000),
      makeUS("JNJ", "Johnson & Johnson", 152.3, 15.8, 4.2, 366_000),
      makeUS("WMT", "Walmart", 68.2, 29.4, 6.3, 548_000),
    ],
    indices: [
      makeIndex("KOSPI", 2_580),
      makeIndex("KOSDAQ", 740),
      makeIndex("S&P 500", 5_200),
      makeIndex("NASDAQ", 16_300),
    ],
    updatedAt: new Date().toISOString(),
  };
}
