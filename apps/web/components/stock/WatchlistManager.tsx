"use client";

import { useState } from "react";
import type { WatchlistItem, Market } from "@/types/stock";

interface WatchlistManagerProps {
  watchlist: WatchlistItem[];
  onAdd: (item: WatchlistItem) => void;
  onRemove: (symbol: string) => void;
  onClose: () => void;
}

const MARKETS: Market[] = ["KRX", "NASDAQ", "NYSE"];

export function WatchlistManager({
  watchlist,
  onAdd,
  onRemove,
  onClose,
}: WatchlistManagerProps) {
  const [symbol, setSymbol] = useState("");
  const [market, setMarket] = useState<Market>("KRX");
  const [inputError, setInputError] = useState("");

  function handleAdd() {
    const trimmed = symbol.trim().toUpperCase();
    if (!trimmed) {
      setInputError("종목코드를 입력하세요.");
      return;
    }
    if (watchlist.some((w) => w.symbol === trimmed)) {
      setInputError("이미 추가된 종목입니다.");
      return;
    }
    onAdd({ symbol: trimmed, market });
    setSymbol("");
    setInputError("");
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") handleAdd();
  }

  return (
    /* Backdrop */
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ backgroundColor: "rgba(0,0,0,0.6)" }}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        className="w-full max-w-md rounded-2xl border p-6 flex flex-col gap-5"
        style={{
          backgroundColor: "var(--color-bg-secondary)",
          borderColor: "var(--color-border-gold)",
        }}
      >
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <p
              className="text-xs uppercase tracking-widest font-medium mb-0.5"
              style={{ color: "var(--color-gold)" }}
            >
              워치리스트
            </p>
            <h2
              className="text-base font-bold"
              style={{ color: "var(--color-text-primary)" }}
            >
              관심 종목 관리
            </h2>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 flex items-center justify-center rounded-lg text-lg transition-colors"
            style={{
              color: "var(--color-text-muted)",
              backgroundColor: "var(--color-bg-tertiary)",
            }}
          >
            ×
          </button>
        </div>

        {/* Add form */}
        <div
          className="rounded-xl border p-4 flex flex-col gap-3"
          style={{
            backgroundColor: "var(--color-bg-card)",
            borderColor: "var(--color-border)",
          }}
        >
          <p
            className="text-sm font-medium"
            style={{ color: "var(--color-text-primary)" }}
          >
            종목 추가
          </p>
          <div className="flex gap-2">
            <input
              type="text"
              value={symbol}
              onChange={(e) => {
                setSymbol(e.target.value);
                setInputError("");
              }}
              onKeyDown={handleKeyDown}
              placeholder="예: 005930, AAPL"
              className="flex-1 px-3 py-2 rounded-lg text-sm outline-none"
              style={{
                backgroundColor: "var(--color-bg-secondary)",
                border: "1px solid var(--color-border)",
                color: "var(--color-text-primary)",
              }}
            />
            <select
              value={market}
              onChange={(e) => setMarket(e.target.value as Market)}
              className="px-2 py-2 rounded-lg text-xs outline-none"
              style={{
                backgroundColor: "var(--color-bg-secondary)",
                border: "1px solid var(--color-border)",
                color: "var(--color-text-secondary)",
              }}
            >
              {MARKETS.map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
          </div>
          {inputError && (
            <p className="text-xs" style={{ color: "#EF4444" }}>
              {inputError}
            </p>
          )}
          <button
            onClick={handleAdd}
            className="w-full py-2 rounded-lg text-sm font-semibold transition-opacity"
            style={{
              backgroundColor: "var(--color-gold)",
              color: "#0F1419",
            }}
          >
            추가
          </button>
        </div>

        {/* Watchlist */}
        <div className="flex flex-col gap-2 max-h-64 overflow-y-auto">
          {watchlist.length === 0 ? (
            <p
              className="text-sm text-center py-6"
              style={{ color: "var(--color-text-muted)" }}
            >
              추가된 종목이 없습니다.
            </p>
          ) : (
            watchlist.map((item) => (
              <div
                key={item.symbol}
                className="flex items-center justify-between px-3 py-2 rounded-lg"
                style={{
                  backgroundColor: "var(--color-bg-card)",
                  border: "1px solid var(--color-border)",
                }}
              >
                <div>
                  <span
                    className="text-sm font-medium"
                    style={{ color: "var(--color-text-primary)" }}
                  >
                    {item.symbol}
                  </span>
                  <span
                    className="text-xs ml-2"
                    style={{ color: "var(--color-text-muted)" }}
                  >
                    {item.market}
                  </span>
                </div>
                <button
                  onClick={() => onRemove(item.symbol)}
                  className="text-xs px-2 py-1 rounded transition-colors"
                  style={{
                    color: "#EF4444",
                    backgroundColor: "rgba(239,68,68,0.1)",
                    border: "1px solid rgba(239,68,68,0.2)",
                  }}
                >
                  삭제
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
