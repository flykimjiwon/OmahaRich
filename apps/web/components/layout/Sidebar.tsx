"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

interface NavItem {
  label: string;
  href: string;
  icon: string;
  description: string;
}

const navItems: NavItem[] = [
  {
    label: "대시보드",
    href: "/",
    icon: "◈",
    description: "홈 & 요약",
  },
  {
    label: "종목 분석",
    href: "/analysis",
    icon: "◉",
    description: "AI 가치평가",
  },
  {
    label: "포트폴리오",
    href: "/portfolio",
    icon: "◆",
    description: "내 보유 종목",
  },
  {
    label: "뉴스 & 공시",
    href: "/news",
    icon: "◈",
    description: "최신 정보",
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside
      className="hidden md:flex flex-col w-60 border-r shrink-0"
      style={{
        backgroundColor: "var(--color-bg-secondary)",
        borderColor: "var(--color-border)",
      }}
    >
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-150"
              style={{
                backgroundColor: isActive
                  ? "rgba(212, 168, 67, 0.12)"
                  : "transparent",
                borderLeft: isActive
                  ? "2px solid var(--color-gold)"
                  : "2px solid transparent",
                color: isActive
                  ? "var(--color-gold)"
                  : "var(--color-text-secondary)",
              }}
            >
              <span className="text-base w-5 text-center">{item.icon}</span>
              <div className="flex flex-col leading-tight">
                <span
                  className="text-sm font-medium"
                  style={{
                    color: isActive
                      ? "var(--color-gold)"
                      : "var(--color-text-primary)",
                  }}
                >
                  {item.label}
                </span>
                <span
                  className="text-xs"
                  style={{ color: "var(--color-text-muted)" }}
                >
                  {item.description}
                </span>
              </div>
            </Link>
          );
        })}
      </nav>

      {/* Bottom quote */}
      <div
        className="p-4 m-3 rounded-lg border"
        style={{
          backgroundColor: "rgba(212, 168, 67, 0.05)",
          borderColor: "var(--color-border-gold)",
        }}
      >
        <p
          className="text-xs italic leading-relaxed"
          style={{ color: "var(--color-text-muted)" }}
        >
          "가격은 당신이 지불하는 것이고, 가치는 당신이 얻는 것이다."
        </p>
        <p
          className="text-xs mt-2 font-medium"
          style={{ color: "var(--color-gold)" }}
        >
          — 워렌 버핏
        </p>
      </div>
    </aside>
  );
}
