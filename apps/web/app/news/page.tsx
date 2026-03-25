export const metadata = {
  title: "뉴스 & 공시 — 오마하부자",
  description: "보유 종목 관련 최신 뉴스와 공시를 AI 요약으로 확인합니다.",
};

export default function NewsPage() {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Page header */}
      <div>
        <p
          className="text-xs font-medium uppercase tracking-widest mb-1"
          style={{ color: "var(--color-gold)" }}
        >
          마켓 인텔리전스
        </p>
        <h1
          className="text-2xl font-bold"
          style={{ color: "var(--color-text-primary)" }}
        >
          뉴스 & 공시
        </h1>
        <p
          className="text-sm mt-1"
          style={{ color: "var(--color-text-secondary)" }}
        >
          보유 종목 관련 최신 뉴스와 공시를 AI가 투자 관점으로 요약합니다.
        </p>
      </div>

      {/* Filter bar placeholder */}
      <div
        className="rounded-xl border p-4 flex items-center gap-3"
        style={{
          backgroundColor: "var(--color-bg-card)",
          borderColor: "var(--color-border)",
        }}
      >
        <input
          type="text"
          placeholder="종목 또는 키워드 검색..."
          className="flex-1 bg-transparent text-sm outline-none"
          style={{ color: "var(--color-text-secondary)" }}
          disabled
        />
        <div className="flex gap-2">
          {["전체", "뉴스", "공시", "실적"].map((filter) => (
            <button
              key={filter}
              className="text-xs px-3 py-1 rounded-full border transition-colors cursor-not-allowed"
              style={{
                borderColor: filter === "전체" ? "var(--color-gold)" : "var(--color-border)",
                color: filter === "전체" ? "var(--color-gold)" : "var(--color-text-muted)",
                backgroundColor:
                  filter === "전체" ? "rgba(212,168,67,0.08)" : "transparent",
              }}
              disabled
            >
              {filter}
            </button>
          ))}
        </div>
      </div>

      {/* Empty state */}
      <div
        className="rounded-xl border p-12 text-center"
        style={{
          backgroundColor: "var(--color-bg-card)",
          borderColor: "var(--color-border)",
        }}
      >
        <div
          className="text-4xl mb-4"
          style={{ color: "var(--color-text-muted)" }}
        >
          ◈
        </div>
        <h2
          className="text-base font-semibold mb-2"
          style={{ color: "var(--color-text-primary)" }}
        >
          뉴스 피드 준비 중
        </h2>
        <p
          className="text-sm"
          style={{ color: "var(--color-text-muted)" }}
        >
          Alpha Vantage, Yahoo Finance 연동 후 실시간 뉴스를 제공합니다.
        </p>
      </div>

      {/* Feature preview cards */}
      <div className="space-y-3">
        <h3
          className="text-xs font-semibold uppercase tracking-widest"
          style={{ color: "var(--color-text-muted)" }}
        >
          제공 예정 기능
        </h3>
        {[
          {
            badge: "AI 요약",
            title: "실시간 뉴스 AI 요약",
            description:
              "수백 개의 뉴스를 AI가 투자 관점에서 3줄로 압축합니다. 긍정/부정 센티먼트 분석 포함.",
          },
          {
            badge: "공시",
            title: "DART 공시 자동 알림",
            description:
              "보유 종목의 실적 발표, 대규모 내부거래, 주요 계약 공시를 즉시 알려드립니다.",
          },
          {
            badge: "스크리닝",
            title: "이벤트 기반 투자 기회",
            description:
              "어닝 서프라이즈, 배당 발표, CEO 변경 등 주가에 영향을 미칠 이벤트를 포착합니다.",
          },
        ].map((item) => (
          <div
            key={item.title}
            className="rounded-xl border p-5"
            style={{
              backgroundColor: "var(--color-bg-card)",
              borderColor: "var(--color-border)",
              opacity: 0.55,
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
                {item.badge}
              </span>
              <h4
                className="text-sm font-semibold"
                style={{ color: "var(--color-text-primary)" }}
              >
                {item.title}
              </h4>
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
    </div>
  );
}
