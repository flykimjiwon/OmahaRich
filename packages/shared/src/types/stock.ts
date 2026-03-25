// 주식 관련 공유 타입 정의

export interface Stock {
  ticker: string;
  name: string;
  exchange: "KRX" | "NASDAQ" | "NYSE" | "KOSPI" | "KOSDAQ";
  sector: string;
  industry: string;
  marketCap: number;
  currency: "KRW" | "USD";
}

export interface StockPrice {
  ticker: string;
  date: string; // YYYY-MM-DD
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  adjustedClose: number;
}

export interface FinancialStatement {
  ticker: string;
  fiscalYear: number;
  fiscalQuarter: 1 | 2 | 3 | 4 | null; // null = annual
  statementType: "income" | "balance_sheet" | "cash_flow";
  currency: "KRW" | "USD";
  items: FinancialItem[];
  reportedAt: string; // ISO 8601
}

export interface FinancialItem {
  label: string;
  value: number;
  unit: "원" | "USD" | "%";
}

export interface ValuationMetrics {
  ticker: string;
  date: string;
  per: number | null;      // Price-to-Earnings Ratio
  pbr: number | null;      // Price-to-Book Ratio
  psr: number | null;      // Price-to-Sales Ratio
  pcr: number | null;      // Price-to-Cash-flow Ratio
  evEbitda: number | null; // EV/EBITDA
  dividendYield: number | null;
  roe: number | null;      // Return on Equity
  roa: number | null;      // Return on Assets
  debtToEquity: number | null;
}

export interface GrahamScore {
  ticker: string;
  analyzedAt: string;
  intrinsicValue: number;
  currentPrice: number;
  marginOfSafety: number; // percentage
  recommendation: "strong_buy" | "buy" | "hold" | "sell" | "avoid";
  reasoning: string;
  criteria: GrahamCriteria;
}

export interface GrahamCriteria {
  adequateSize: boolean;
  strongFinancialCondition: boolean;
  earningsStability: boolean;
  dividendRecord: boolean;
  earningsGrowth: boolean;
  moderatePE: boolean;
  moderatePB: boolean;
}

export interface NewsItem {
  id: string;
  title: string;
  summary: string;
  source: string;
  publishedAt: string; // ISO 8601
  url: string;
  tickers: string[];
  sentiment: "positive" | "negative" | "neutral" | null;
}

export interface PortfolioHolding {
  ticker: string;
  stock: Stock;
  quantity: number;
  averageCost: number;
  currentPrice: number;
  currency: "KRW" | "USD";
}

export interface Portfolio {
  id: string;
  name: string;
  createdAt: string;
  holdings: PortfolioHolding[];
  cashKrw: number;
  cashUsd: number;
}

export interface AnalysisRequest {
  ticker: string;
  analysisType: "value" | "growth" | "dividend" | "comprehensive";
}

export interface AnalysisResult {
  ticker: string;
  stock: Stock;
  analyzedAt: string;
  valuation: ValuationMetrics;
  grahamScore: GrahamScore;
  summary: string;
  risks: string[];
  opportunities: string[];
}
