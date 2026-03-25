export const metadata = {
  title: "포트폴리오 — 오마하부자",
  description: "보유 종목 관리 및 수익률 추적",
};

export default function PortfolioPage() {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Page header */}
      <div>
        <p
          className="text-xs font-medium uppercase tracking-widest mb-1"
          style={{ color: "var(--color-gold)" }}
        >
          내 투자
        </p>
        <h1
          className="text-2xl font-bold"
          style={{ color: "var(--color-text-primary)" }}
        >
          포트폴리오
        </h1>
        <p
          className="text-sm mt-1"
          style={{ color: "var(--color-text-secondary)" }}
        >
          보유 종목을 관리하고 수익률 및 리스크를 추적합니다.
        </p>
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
          ◆
        </div>
        <h2
          className="text-base font-semibold mb-2"
          style={{ color: "var(--color-text-primary)" }}
        >
          포트폴리오가 비어 있습니다
        </h2>
        <p
          className="text-sm mb-6"
          style={{ color: "var(--color-text-muted)" }}
        >
          종목 분석 후 포트폴리오에 추가할 수 있습니다.
        </p>
        <span
          className="inline-block text-xs px-3 py-1.5 rounded-full border"
          style={{
            color: "var(--color-text-muted)",
            borderColor: "var(--color-border)",
          }}
        >
          연동 기능 준비 중
        </span>
      </div>

      {/* Feature preview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          {
            title: "수익률 추적",
            description: "보유 종목별 평가손익 및 수익률을 실시간으로 표시합니다.",
          },
          {
            title: "섹터 분산",
            description: "섹터별 비중을 차트로 시각화해 리스크 분산 현황을 확인합니다.",
          },
          {
            title: "목표 비중 관리",
            description: "목표 비중을 설정하고 리밸런싱 필요 종목을 알려드립니다.",
          },
        ].map((item) => (
          <div
            key={item.title}
            className="rounded-xl border p-5"
            style={{
              backgroundColor: "var(--color-bg-card)",
              borderColor: "var(--color-border)",
              opacity: 0.5,
            }}
          >
            <h3
              className="text-sm font-semibold mb-1"
              style={{ color: "var(--color-text-primary)" }}
            >
              {item.title}
            </h3>
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
