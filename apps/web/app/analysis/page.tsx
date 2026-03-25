"use client";

import { useState } from "react";

interface AnalysisResult {
  symbol: string;
  name: string;
  market: string;
  per: number | null;
  pbr: number | null;
  grahamScore: number | null;
  intrinsicValue: number | null;
  currentPrice: number | null;
  upside: number | null;
  summary: string;
}

const BACKEND_URL = "http://localhost:8101";

export default function AnalysisPage() {
  const [ticker, setTicker] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  async function handleAnalyze() {
    const trimmed = ticker.trim().toUpperCase();
    if (!trimmed) {
      setError("종목코드를 입력하세요.");
      return;
    }
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch(`${BACKEND_URL}/api/v1/analysis/${trimmed}`, {
        signal: AbortSignal.timeout(30_000),
      });
      if (!res.ok) {
        throw new Error(`서버 응답 오류 (${res.status}). 백엔드가 실행 중인지 확인하세요.`);
      }
      const data: AnalysisResult = await res.json();
      setResult(data);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "알 수 없는 오류";
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") handleAnalyze();
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Page header */}
      <div>
        <p
          className="text-xs font-medium uppercase tracking-widest mb-1"
          style={{ color: "var(--color-gold)" }}
        >
          AI 분석
        </p>
        <h1
          className="text-2xl font-bold"
          style={{ color: "var(--color-text-primary)" }}
        >
          종목 분석
        </h1>
        <p className="text-sm mt-1" style={{ color: "var(--color-text-secondary)" }}>
          티커 또는 종목코드를 입력하면 워렌 버핏 방식의 가치평가를 수행합니다.
        </p>
      </div>

      {/* Search form */}
      <div
        className="rounded-xl border p-6"
        style={{
          backgroundColor: "var(--color-bg-card)",
          borderColor: "var(--color-border)",
        }}
      >
        <label
          className="block text-sm font-medium mb-2"
          style={{ color: "var(--color-text-primary)" }}
          htmlFor="ticker-input"
        >
          종목 검색
        </label>
        <div className="flex gap-3">
          <input
            id="ticker-input"
            type="text"
            value={ticker}
            onChange={(e) => {
              setTicker(e.target.value);
              setError(null);
            }}
            onKeyDown={handleKeyDown}
            placeholder="예: 005930 (삼성전자), AAPL, MSFT"
            className="flex-1 px-4 py-3 rounded-lg text-sm outline-none transition-colors"
            style={{
              backgroundColor: "var(--color-bg-secondary)",
              border: `1px solid ${error ? "#EF4444" : "var(--color-border)"}`,
              color: "var(--color-text-primary)",
            }}
            disabled={isLoading}
          />
          <button
            onClick={handleAnalyze}
            disabled={isLoading || !ticker.trim()}
            className="px-6 py-3 rounded-lg text-sm font-semibold transition-opacity"
            style={{
              backgroundColor: "var(--color-gold)",
              color: "#0F1419",
              opacity: isLoading || !ticker.trim() ? 0.6 : 1,
              cursor: isLoading || !ticker.trim() ? "not-allowed" : "pointer",
            }}
          >
            {isLoading ? "분석 중..." : "분석 시작"}
          </button>
        </div>
        {error && (
          <p className="text-xs mt-2" style={{ color: "#EF4444" }}>
            {error}
          </p>
        )}
        <p className="text-xs mt-2" style={{ color: "var(--color-text-muted)" }}>
          KRX (한국), NASDAQ, NYSE 종목 지원 · 백엔드 연결 필요
        </p>
      </div>

      {/* Loading state */}
      {isLoading && (
        <div
          className="rounded-xl border p-8 text-center"
          style={{
            backgroundColor: "var(--color-bg-card)",
            borderColor: "var(--color-border)",
          }}
        >
          <div
            className="text-3xl mb-3 animate-pulse"
            style={{ color: "var(--color-gold)" }}
          >
            ◉
          </div>
          <p className="text-sm" style={{ color: "var(--color-text-secondary)" }}>
            {ticker.toUpperCase()} 분석 중... AI가 재무제표를 검토하고 있습니다.
          </p>
        </div>
      )}

      {/* Analysis result */}
      {result && (
        <div className="space-y-4">
          {/* Header */}
          <div
            className="rounded-xl border p-5"
            style={{
              backgroundColor: "var(--color-bg-card)",
              borderColor: "var(--color-border-gold)",
            }}
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <p
                  className="text-xs uppercase tracking-widest font-medium mb-1"
                  style={{ color: "var(--color-gold)" }}
                >
                  {result.market}
                </p>
                <h2
                  className="text-xl font-bold"
                  style={{ color: "var(--color-text-primary)" }}
                >
                  {result.name}
                  <span
                    className="text-sm font-normal ml-2"
                    style={{ color: "var(--color-text-muted)" }}
                  >
                    {result.symbol}
                  </span>
                </h2>
              </div>
              {result.grahamScore !== null && (
                <div className="text-right">
                  <p
                    className="text-xs mb-0.5"
                    style={{ color: "var(--color-text-muted)" }}
                  >
                    Graham Score
                  </p>
                  <p
                    className="text-2xl font-bold"
                    style={{
                      color:
                        result.grahamScore >= 70
                          ? "#4CAF7D"
                          : result.grahamScore >= 40
                          ? "var(--color-gold)"
                          : "#EF4444",
                    }}
                  >
                    {result.grahamScore}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Metrics grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "현재가", value: result.currentPrice !== null ? result.currentPrice.toLocaleString() : "—" },
              { label: "내재가치", value: result.intrinsicValue !== null ? result.intrinsicValue.toLocaleString() : "—" },
              { label: "PER", value: result.per !== null ? result.per.toFixed(1) + "x" : "—" },
              { label: "PBR", value: result.pbr !== null ? result.pbr.toFixed(2) + "x" : "—" },
            ].map((m) => (
              <div
                key={m.label}
                className="rounded-xl border p-4"
                style={{
                  backgroundColor: "var(--color-bg-card)",
                  borderColor: "var(--color-border)",
                }}
              >
                <p
                  className="text-xs mb-1"
                  style={{ color: "var(--color-text-muted)" }}
                >
                  {m.label}
                </p>
                <p
                  className="text-lg font-bold tabular-nums"
                  style={{ color: "var(--color-text-primary)" }}
                >
                  {m.value}
                </p>
              </div>
            ))}
          </div>

          {/* Upside */}
          {result.upside !== null && (
            <div
              className="rounded-xl border p-4 flex items-center gap-3"
              style={{
                backgroundColor: "var(--color-bg-card)",
                borderColor:
                  result.upside > 0
                    ? "rgba(76,175,125,0.3)"
                    : "rgba(239,68,68,0.3)",
              }}
            >
              <span
                className="text-xl"
                style={{ color: result.upside > 0 ? "#4CAF7D" : "#EF4444" }}
              >
                {result.upside > 0 ? "▲" : "▼"}
              </span>
              <div>
                <p
                  className="text-sm font-semibold"
                  style={{ color: "var(--color-text-primary)" }}
                >
                  내재가치 대비{" "}
                  <span
                    style={{
                      color: result.upside > 0 ? "#4CAF7D" : "#EF4444",
                    }}
                  >
                    {result.upside > 0 ? "+" : ""}
                    {result.upside.toFixed(1)}% 여력
                  </span>
                </p>
                <p
                  className="text-xs mt-0.5"
                  style={{ color: "var(--color-text-muted)" }}
                >
                  {result.upside > 30
                    ? "안전마진 충분 — 매수 검토 가능"
                    : result.upside > 0
                    ? "적정 가격 근처"
                    : "현재가가 내재가치를 초과"}
                </p>
              </div>
            </div>
          )}

          {/* AI summary */}
          {result.summary && (
            <div
              className="rounded-xl border p-5"
              style={{
                backgroundColor: "var(--color-bg-card)",
                borderColor: "var(--color-border)",
              }}
            >
              <p
                className="text-xs uppercase tracking-widest font-medium mb-3"
                style={{ color: "var(--color-gold)" }}
              >
                AI 투자 의견
              </p>
              <p
                className="text-sm leading-relaxed"
                style={{ color: "var(--color-text-secondary)" }}
              >
                {result.summary}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Feature cards — shown when no result */}
      {!result && !isLoading && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            {
              title: "Graham Score",
              description:
                "벤저민 그레이엄의 7가지 기준으로 종목을 평가합니다.",
            },
            {
              title: "내재가치 계산",
              description:
                "DCF 모델과 Graham Number로 내재가치를 산출합니다.",
            },
            {
              title: "재무제표 분석",
              description:
                "최근 5년 손익계산서, 대차대조표, 현금흐름표를 시각화합니다.",
            },
            {
              title: "투자 리포트",
              description:
                "AI가 투자 의견과 리스크 요인을 자동으로 작성합니다.",
            },
          ].map((item) => (
            <div
              key={item.title}
              className="rounded-xl border p-5"
              style={{
                backgroundColor: "var(--color-bg-card)",
                borderColor: "var(--color-border)",
                opacity: 0.65,
              }}
            >
              <div className="flex items-center gap-2 mb-2">
                <span
                  className="text-xs px-2 py-0.5 rounded-full"
                  style={{
                    backgroundColor: "rgba(212,168,67,0.1)",
                    color: "var(--color-gold)",
                  }}
                >
                  준비 중
                </span>
                <h3
                  className="text-sm font-semibold"
                  style={{ color: "var(--color-text-primary)" }}
                >
                  {item.title}
                </h3>
              </div>
              <p
                className="text-xs leading-relaxed"
                style={{ color: "var(--color-text-muted)" }}
              >
                {item.description}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
