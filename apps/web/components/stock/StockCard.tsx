"use client";

import type { StockPrice } from "@/types/stock";
import { getChangeDirection } from "@/types/stock";

interface StockCardProps {
  stock: StockPrice;
  isStale: boolean;
}

function formatPrice(price: number, market: StockPrice["market"]): string {
  if (market === "KRX") {
    return price.toLocaleString("ko-KR") + "원";
  }
  return "$" + price.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function formatChange(change: number, market: StockPrice["market"]): string {
  const prefix = change >= 0 ? "+" : "";
  if (market === "KRX") {
    return prefix + change.toLocaleString("ko-KR") + "원";
  }
  return prefix + "$" + Math.abs(change).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function formatVolume(volume: number): string {
  if (volume >= 1_000_000) return (volume / 1_000_000).toFixed(1) + "M";
  if (volume >= 1_000) return (volume / 1_000).toFixed(0) + "K";
  return volume.toLocaleString();
}

function formatMarketCap(cap: number, market: StockPrice["market"]): string {
  if (market === "KRX") {
    if (cap >= 10_000) return (cap / 10_000).toFixed(1) + "조";
    return cap.toLocaleString() + "억";
  }
  if (cap >= 1_000_000) return "$" + (cap / 1_000_000).toFixed(2) + "T";
  if (cap >= 1_000) return "$" + (cap / 1_000).toFixed(0) + "B";
  return "$" + cap + "M";
}

function formatTime(isoStr: string): string {
  const d = new Date(isoStr);
  return d.toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

const CHANGE_COLORS = {
  up: "#EF4444",
  down: "#3B82F6",
  flat: "#6B7280",
} as const;

export function StockCard({ stock, isStale }: StockCardProps) {
  const dir = getChangeDirection(stock.change);
  const changeColor = CHANGE_COLORS[dir];

  return (
    <div
      className="stock-card rounded-xl border p-4 flex flex-col gap-3"
      style={{
        backgroundColor: "var(--color-bg-card)",
        borderColor: isStale ? "var(--color-border)" : "var(--color-border)",
        opacity: isStale ? 0.6 : 1,
        transition: "opacity 0.3s ease",
      }}
    >
      {/* Header: name + stale badge */}
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <p
            className="text-sm font-semibold truncate"
            style={{ color: "var(--color-text-primary)" }}
          >
            {stock.name}
          </p>
          <p className="text-xs mt-0.5" style={{ color: "var(--color-text-muted)" }}>
            {stock.symbol} · {stock.market}
          </p>
        </div>
        {isStale && (
          <span
            className="text-xs px-1.5 py-0.5 rounded shrink-0"
            style={{
              backgroundColor: "rgba(239,68,68,0.12)",
              color: "#EF4444",
              border: "1px solid rgba(239,68,68,0.25)",
            }}
          >
            데이터 지연
          </span>
        )}
      </div>

      {/* Price */}
      <div>
        <p
          className="text-xl font-bold tabular-nums"
          style={{ color: "var(--color-text-primary)" }}
        >
          {formatPrice(stock.price, stock.market)}
        </p>
        <div className="flex items-center gap-2 mt-0.5">
          <span
            className="text-sm font-medium tabular-nums"
            style={{ color: changeColor }}
          >
            {dir === "up" ? "▲" : dir === "down" ? "▼" : "■"}{" "}
            {formatChange(stock.change, stock.market)}
          </span>
          <span
            className="text-sm font-medium tabular-nums"
            style={{ color: changeColor }}
          >
            ({stock.changeRate >= 0 ? "+" : ""}
            {stock.changeRate.toFixed(2)}%)
          </span>
        </div>
      </div>

      {/* Value investor metrics */}
      <div
        className="grid grid-cols-2 gap-2 rounded-lg p-2.5"
        style={{ backgroundColor: "var(--color-bg-secondary)" }}
      >
        <div>
          <p className="text-xs" style={{ color: "var(--color-text-muted)" }}>PER</p>
          <p className="text-sm font-semibold tabular-nums" style={{ color: "var(--color-text-primary)" }}>
            {stock.per !== null ? stock.per.toFixed(1) + "x" : "—"}
          </p>
        </div>
        <div>
          <p className="text-xs" style={{ color: "var(--color-text-muted)" }}>PBR</p>
          <p className="text-sm font-semibold tabular-nums" style={{ color: "var(--color-text-primary)" }}>
            {stock.pbr !== null ? stock.pbr.toFixed(2) + "x" : "—"}
          </p>
        </div>
        <div>
          <p className="text-xs" style={{ color: "var(--color-text-muted)" }}>거래량</p>
          <p className="text-sm font-semibold tabular-nums" style={{ color: "var(--color-text-primary)" }}>
            {formatVolume(stock.volume)}
          </p>
        </div>
        <div>
          <p className="text-xs" style={{ color: "var(--color-text-muted)" }}>시가총액</p>
          <p className="text-sm font-semibold tabular-nums" style={{ color: "var(--color-text-primary)" }}>
            {formatMarketCap(stock.marketCap, stock.market)}
          </p>
        </div>
      </div>

      {/* Footer: update time */}
      <p className="text-xs" style={{ color: "var(--color-text-muted)" }}>
        갱신: {formatTime(stock.updatedAt)}
      </p>
    </div>
  );
}
