"use client";

import type { MarketIndex } from "@/types/stock";
import { getChangeDirection } from "@/types/stock";

interface IndexBarProps {
  indices: MarketIndex[];
}

const CHANGE_COLORS = {
  up: "#EF4444",
  down: "#3B82F6",
  flat: "#6B7280",
} as const;

export function IndexBar({ indices }: IndexBarProps) {
  return (
    <div
      className="rounded-xl border p-4"
      style={{
        backgroundColor: "var(--color-bg-card)",
        borderColor: "var(--color-border)",
      }}
    >
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {indices.map((idx) => {
          const dir = getChangeDirection(idx.change);
          const color = CHANGE_COLORS[dir];
          return (
            <div key={idx.name} className="flex flex-col gap-1">
              <p
                className="text-xs font-medium uppercase tracking-wider"
                style={{ color: "var(--color-text-muted)" }}
              >
                {idx.name}
              </p>
              <p
                className="text-lg font-bold tabular-nums"
                style={{ color: "var(--color-text-primary)" }}
              >
                {idx.value.toLocaleString("ko-KR", { maximumFractionDigits: 2 })}
              </p>
              <p className="text-xs font-medium tabular-nums" style={{ color }}>
                {dir === "up" ? "▲" : dir === "down" ? "▼" : "■"}{" "}
                {idx.changeRate >= 0 ? "+" : ""}
                {idx.changeRate.toFixed(2)}%
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
