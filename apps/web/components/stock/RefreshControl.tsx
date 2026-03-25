"use client";

import type { RefreshInterval } from "@/types/stock";

const INTERVALS: RefreshInterval[] = [10, 30, 60];

interface RefreshControlProps {
  interval: RefreshInterval;
  onIntervalChange: (v: RefreshInterval) => void;
  nextUpdateIn: number;
  onRefresh: () => void;
  isLoading: boolean;
}

export function RefreshControl({
  interval,
  onIntervalChange,
  nextUpdateIn,
  onRefresh,
  isLoading,
}: RefreshControlProps) {
  const progress = Math.max(0, (nextUpdateIn / interval) * 100);

  return (
    <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
      {/* Interval selector */}
      <div className="flex items-center gap-1">
        <span
          className="text-xs mr-2"
          style={{ color: "var(--color-text-muted)" }}
        >
          갱신 간격
        </span>
        {INTERVALS.map((s) => (
          <button
            key={s}
            onClick={() => onIntervalChange(s)}
            className="text-xs px-2.5 py-1 rounded transition-colors"
            style={{
              backgroundColor:
                interval === s
                  ? "rgba(212,168,67,0.18)"
                  : "var(--color-bg-tertiary)",
              color:
                interval === s
                  ? "var(--color-gold)"
                  : "var(--color-text-secondary)",
              border: `1px solid ${
                interval === s
                  ? "var(--color-border-gold)"
                  : "var(--color-border)"
              }`,
            }}
          >
            {s}초
          </button>
        ))}
      </div>

      {/* Countdown + progress */}
      <div className="flex items-center gap-2 flex-1 min-w-0">
        <div
          className="relative flex-1 h-1.5 rounded-full overflow-hidden"
          style={{ backgroundColor: "var(--color-bg-tertiary)", minWidth: 80 }}
        >
          <div
            className="h-full rounded-full transition-all duration-1000"
            style={{
              width: `${progress}%`,
              backgroundColor: "var(--color-gold)",
              opacity: 0.7,
            }}
          />
        </div>
        <span
          className="text-xs tabular-nums shrink-0"
          style={{ color: "var(--color-text-muted)" }}
        >
          {nextUpdateIn}초 후 갱신
        </span>
      </div>

      {/* Manual refresh */}
      <button
        onClick={onRefresh}
        disabled={isLoading}
        className="text-xs px-3 py-1.5 rounded flex items-center gap-1.5 transition-opacity"
        style={{
          backgroundColor: "var(--color-bg-tertiary)",
          color: "var(--color-gold)",
          border: "1px solid var(--color-border-gold)",
          opacity: isLoading ? 0.5 : 1,
          cursor: isLoading ? "not-allowed" : "pointer",
        }}
      >
        <span
          style={{
            display: "inline-block",
            animation: isLoading ? "spin 1s linear infinite" : "none",
          }}
        >
          ↻
        </span>
        새로고침
      </button>
    </div>
  );
}
