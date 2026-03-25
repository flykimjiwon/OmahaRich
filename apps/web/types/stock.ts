export type Market = "KRX" | "NASDAQ" | "NYSE";

export interface StockPrice {
  symbol: string;
  name: string;
  market: Market;
  price: number;
  prevClose: number;
  change: number;       // 전일 대비 금액
  changeRate: number;   // 전일 대비 %
  volume: number;
  marketCap: number;    // 시가총액 (억원 or million USD)
  per: number | null;
  pbr: number | null;
  updatedAt: string;    // ISO string
}

export interface MarketIndex {
  name: string;
  value: number;
  change: number;
  changeRate: number;
}

export interface RealtimePricesResponse {
  korean: StockPrice[];
  us: StockPrice[];
  indices: MarketIndex[];
  updatedAt: string;
}

export type ChangeDirection = "up" | "down" | "flat";

export function getChangeDirection(change: number): ChangeDirection {
  if (change > 0) return "up";
  if (change < 0) return "down";
  return "flat";
}

export interface WatchlistItem {
  symbol: string;
  market: Market;
}

export type RefreshInterval = 10 | 30 | 60;
