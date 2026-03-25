import Link from "next/link";

export function Header() {
  return (
    <header
      className="sticky top-0 z-50 border-b"
      style={{
        backgroundColor: "var(--color-bg-secondary)",
        borderColor: "var(--color-border)",
      }}
    >
      <div className="flex items-center justify-between px-6 h-16">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-3 group">
          <div
            className="w-9 h-9 rounded-lg flex items-center justify-center text-sm font-bold gradient-gold"
            style={{ color: "#0F1419" }}
          >
            O
          </div>
          <div className="flex flex-col leading-tight">
            <span
              className="text-lg font-bold tracking-tight"
              style={{ color: "var(--color-gold)" }}
            >
              오마하부자
            </span>
            <span
              className="text-xs"
              style={{ color: "var(--color-text-muted)" }}
            >
              AI 가치투자 플랫폼
            </span>
          </div>
        </Link>

        {/* Right side actions */}
        <div className="flex items-center gap-4">
          <span
            className="text-xs px-2 py-1 rounded-full border"
            style={{
              color: "var(--color-gold)",
              borderColor: "var(--color-border-gold)",
              backgroundColor: "rgba(212, 168, 67, 0.08)",
            }}
          >
            Beta
          </span>
          <div
            className="text-sm"
            style={{ color: "var(--color-text-secondary)" }}
          >
            <span className="font-medium" style={{ color: "var(--color-text-primary)" }}>
              KOSPI
            </span>{" "}
            <span style={{ color: "var(--color-success)" }}>+0.00%</span>
          </div>
        </div>
      </div>
    </header>
  );
}
