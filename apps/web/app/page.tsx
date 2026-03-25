"use client";

import { useState } from "react";
import Link from "next/link";
import { useRealtimePrices } from "@/lib/hooks/useRealtimePrices";
import { StockCard } from "@/components/stock/StockCard";
import { IndexBar } from "@/components/stock/IndexBar";
import { RefreshControl } from "@/components/stock/RefreshControl";
import { WatchlistManager } from "@/components/stock/WatchlistManager";
import type { RefreshInterval, WatchlistItem } from "@/types/stock";

const DEFAULT_WATCHLIST: WatchlistItem[] = [
  { symbol: "005930", market: "KRX" },
  { symbol: "000660", market: "KRX" },
  { symbol: "AAPL", market: "NASDAQ" },
  { symbol: "BRK.B", market: "NASDAQ" },
];

export default function DashboardPage() {
  const [interval, setInterval] = useState<RefreshInterval>(30);
  const [showWatchlist, setShowWatchlist] = useState(false);
  const [watchlist, setWatchlist] = useState<WatchlistItem[]>(DEFAULT_WATCHLIST);

  const { data, isLoading, error, nextUpdateIn, refetch, isStale } =
    useRealtimePrices(interval);

  function handleAddWatchlist(item: WatchlistItem) {
    setWatchlist((prev) => [...prev, item]);
  }

  function handleRemoveWatchlist(symbol: string) {
    setWatchlist((prev) => prev.filter((w) => w.symbol !== symbol));
  }

  const korean = data?.korean ?? [];
  const us = data?.us ?? [];
  const indices = data?.indices ?? [];

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Hero */}
      <section className="pt-2">
        <div
          className="rounded-2xl p-6 border"
          style={{
            background:
              "linear-gradient(135deg, rgba(212,168,67,0.08) 0%, rgba(26,31,46,0.6) 100%)",
            borderColor: "var(--color-border-gold)",
          }}
        >
          <div className="flex items-start justify-between gap-4">
            <div>
              <p
                className="text-xs font-medium mb-1.5 tracking-widest uppercase"
                style={{ color: "var(--color-gold)" }}
              >
                오마하부자 AI 투자 플랫폼
              </p>
              <h1
                className="text-2xl lg:text-3xl font-bold mb-2"
                style={{ color: "var(--color-text-primary)" }}
              >
                실시간 시세{" "}
                <span style={{ color: "var(--color-gold)" }}>대시보드</span>
              </h1>
              <p
                className="text-sm max-w-lg leading-relaxed"
                style={{ color: "var(--color-text-secondary)" }}
              >
                한국 · 미국 주요 종목을 가치투자 지표와 함께 실시간으로
                모니터링하세요.
              </p>
            </div>
            <div className="flex items-center gap-2 shrink-0">
              <button
                onClick={() => setShowWatchlist(true)}
                className="text-xs px-3 py-1.5 rounded-lg transition-colors"
                style={{
                  backgroundColor: "rgba(212,168,67,0.12)",
                  color: "var(--color-gold)",
                  border: "1px solid var(--color-border-gold)",
                }}
              >
                ☆ 워치리스트
              </button>
              <Link
                href="/analysis"
                className="text-xs px-3 py-1.5 rounded-lg"
                style={{
                  backgroundColor: "var(--color-gold)",
                  color: "#0F1419",
                  fontWeight: 600,
                }}
              >
                종목 분석 →
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Refresh control */}
      <section>
        <RefreshControl
          interval={interval}
          onIntervalChange={setInterval}
          nextUpdateIn={nextUpdateIn}
          onRefresh={refetch}
          isLoading={isLoading}
        />
        {error && (
          <div
            className="mt-2 px-3 py-2 rounded-lg text-xs flex items-center gap-2"
            style={{
              backgroundColor: "rgba(212,168,67,0.08)",
              border: "1px solid var(--color-border-gold)",
              color: "var(--color-gold)",
            }}
          >
            <span>⚠</span>
            <span>{error}</span>
          </div>
        )}
      </section>

      {/* Index bar */}
      {indices.length > 0 && (
        <section>
          <p
            className="text-xs font-semibold uppercase tracking-widest mb-3"
            style={{ color: "var(--color-text-muted)" }}
          >
            주요 지수
          </p>
          <IndexBar indices={indices} />
        </section>
      )}

      {/* Loading skeleton */}
      {isLoading && !data && (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div
              key={i}
              className="rounded-xl border p-4 h-48 animate-pulse"
              style={{
                backgroundColor: "var(--color-bg-card)",
                borderColor: "var(--color-border)",
              }}
            />
          ))}
        </div>
      )}

      {/* Korean stocks */}
      {korean.length > 0 && (
        <section>
          <div className="flex items-center justify-between mb-3">
            <p
              className="text-xs font-semibold uppercase tracking-widest"
              style={{ color: "var(--color-text-muted)" }}
            >
              🇰🇷 한국 주식 (KRX)
            </p>
            <span
              className="text-xs px-2 py-0.5 rounded-full"
              style={{
                backgroundColor: "rgba(212,168,67,0.1)",
                color: "var(--color-gold)",
              }}
            >
              {korean.length}종목
            </span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {korean.map((stock) => (
              <StockCard key={stock.symbol} stock={stock} isStale={isStale} />
            ))}
          </div>
        </section>
      )}

      {/* US stocks */}
      {us.length > 0 && (
        <section>
          <div className="flex items-center justify-between mb-3">
            <p
              className="text-xs font-semibold uppercase tracking-widest"
              style={{ color: "var(--color-text-muted)" }}
            >
              🇺🇸 미국 주식 (NASDAQ · NYSE)
            </p>
            <span
              className="text-xs px-2 py-0.5 rounded-full"
              style={{
                backgroundColor: "rgba(212,168,67,0.1)",
                color: "var(--color-gold)",
              }}
            >
              {us.length}종목
            </span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {us.map((stock) => (
              <StockCard key={stock.symbol} stock={stock} isStale={isStale} />
            ))}
          </div>
        </section>
      )}

      {/* Philosophy quote */}
      <section>
        <blockquote
          className="rounded-xl px-6 py-5"
          style={{
            borderLeft: "4px solid var(--color-gold)",
            border: "1px solid var(--color-border)",
            borderLeftWidth: "4px",
            borderLeftColor: "var(--color-gold)",
            backgroundColor: "var(--color-bg-card)",
          }}
        >
          <p
            className="text-sm italic leading-relaxed mb-2"
            style={{ color: "var(--color-text-secondary)" }}
          >
            "훌륭한 기업을 공정한 가격에 사는 것이 공정한 기업을 훌륭한
            가격에 사는 것보다 훨씬 낫다."
          </p>
          <footer
            className="text-xs font-semibold"
            style={{ color: "var(--color-gold)" }}
          >
            — 워렌 버핏, 오마하의 현인
          </footer>
        </blockquote>
      </section>

      {/* Watchlist modal */}
      {showWatchlist && (
        <WatchlistManager
          watchlist={watchlist}
          onAdd={handleAddWatchlist}
          onRemove={handleRemoveWatchlist}
          onClose={() => setShowWatchlist(false)}
        />
      )}
    </div>
  );
}
