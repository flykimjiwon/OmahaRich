import type { Metadata } from "next";
import "./globals.css";
import { Header } from "@/components/layout/Header";
import { Sidebar } from "@/components/layout/Sidebar";

export const metadata: Metadata = {
  title: "오마하부자 — AI 주식투자 플랫폼",
  description: "워렌 버핏의 가치투자 철학 + AI 분석으로 현명한 투자 결정을 내리세요.",
  keywords: ["주식", "투자", "가치투자", "AI", "워렌 버핏", "오마하"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko" className="dark">
      <body className="min-h-screen" style={{ backgroundColor: "var(--color-bg-primary)" }} suppressHydrationWarning>
        <div className="flex flex-col min-h-screen">
          <Header />
          <div className="flex flex-1 overflow-hidden">
            <Sidebar />
            <main className="flex-1 overflow-y-auto p-6 lg:p-8">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
