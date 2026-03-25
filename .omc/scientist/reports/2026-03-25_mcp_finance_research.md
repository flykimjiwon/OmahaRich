# AI 주식투자 플랫폼 MCP 서버 조사 리포트

> 작성일: 2026-03-25
> 조사 목적: AI 주식투자 플랫폼 구축에 활용 가능한 MCP 서버 및 Claude Code 스킬 전수 조사

---

## [OBJECTIVE]

AI 주식투자 플랫폼 구축을 위해 활용 가능한 MCP(Model Context Protocol) 서버 전체를 카테고리별로 조사하고, 현재 환경에 설치된 서버와 추가로 설치해야 할 서버를 분류하여 우선순위 설치 가이드를 제공한다.

---

## [DATA] 현재 활성 MCP 서버 (9개)

현재 Claude Code 환경에 설치되어 즉시 사용 가능한 MCP 서버 목록.

| 서버명 | 카테고리 | 주요 도구 | 금융 플랫폼 활용 용도 | 비용 |
|--------|----------|-----------|----------------------|------|
| **Firecrawl** | 웹 스크래핑/크롤링 | firecrawl_scrape, firecrawl_crawl, firecrawl_search, firecrawl_extract, firecrawl_browser_* | 금융 뉴스 스크래핑, 공시 데이터 수집, SEC 파일링 크롤링, Yahoo Finance 데이터 수집 | 무료 티어 |
| **Playwright** | 브라우저 자동화 | browser_navigate, browser_click, browser_snapshot, browser_screenshot | 증권사 웹사이트 자동화, 로그인 필요 데이터 수집, HTS 자동화 | 무료 |
| **Tavily** | AI 검색/리서치 | tavily_search, tavily_extract, tavily_crawl, tavily_research | 금융 뉴스 검색, 종목 리서치, 시장 동향 조사, 실시간 이슈 파악 | 1,000회/월 무료 |
| **Brave Search** | 웹 검색 | brave_web_search, brave_local_search | 금융 정보 검색, 뉴스 검색, 경쟁사 조사 | 2,000회/월 무료 |
| **Apify** | 웹 크롤링/자동화 | call-actor, fetch-actor-details, search-actors, get-actor-output | Yahoo Finance 스크래핑 Actor, 뉴스 크롤러, 소셜 미디어 감성 분석 | 무료 티어 |
| **Notion** | 문서/DB | notion-create-database, notion-create-pages, notion-search, notion-update-page | 투자 일지 관리, 종목 분석 노트, 포트폴리오 추적 | 무료 |
| **Context7 (c7)** | 개발 문서 | query-docs, resolve-library-id | 금융 Python 라이브러리 문서 조회 (pandas, yfinance, backtrader 등) | 무료 |
| **OMC Python REPL** | 데이터 분석 | python_repl | 주가 분석, 백테스팅, 시각화, 통계 분석, 포트폴리오 최적화 | 무료 |
| **Memory** | 지식 그래프 | create_entities, create_relations, search_nodes, read_graph | 종목 분석 히스토리 저장, 투자 아이디어 그래프, 패턴 추적 | 무료 |

---

## [FINDING] 카테고리별 추가 설치 권장 MCP 서버

### 1. 금융/주식 데이터 MCP (가장 중요)

현재 전용 금융 API MCP가 없는 것이 가장 큰 갭이다.

| 서버명 | GitHub | API 키 | 주요 기능 | 비용 | 우선순위 |
|--------|--------|--------|-----------|------|----------|
| **Alpha Vantage MCP** | alphavantage/alpha_vantage_mcp | alphavantage.co | 주가 실시간/역사, 기술적 지표 50+, 펀더멘털, 환율, 암호화폐, 원자재, 경제지표 (100+ 도구) | 무료 25회/일, $50/월~ | ★★★★★ |
| **Yahoo Finance MCP** | leogue/StockMCP | 없음 (무료) | 실시간 주가, 기업 메타데이터, 역사적 데이터, P/E, 시가총액 | 완전 무료 | ★★★★★ |
| **Finnhub MCP** | sverze/stock-market-mcp-server | finnhub.io | 실시간 뉴스, 감성 분석, 애널리스트 목표가, 내부자 거래, 어닝 캘린더 | 무료 60req/분 | ★★★★☆ |
| **Financial Datasets MCP** | financial-datasets/mcp-server | financialdatasets.ai | 재무제표 (손익/대차/현금흐름), 주가, 기업 뉴스, 암호화폐 | 유료 | ★★★★☆ |
| **TradingView MCP** | atilaahmettaner/tradingview-mcp | 없음 (무료) | 다중 타임프레임, 캔들 패턴 인식, Ichimoku, Fibonacci, 다중 거래소 | 무료 | ★★★★☆ |
| **Alpaca MCP** | alpacahq/alpaca-mcp-server | alpaca.markets | 자연어 주문, 포트폴리오 추적, P&L, 페이퍼/실제 트레이딩 | 무료 (페이퍼 트레이딩) | ★★★★☆ |
| **Polygon.io MCP** | 별도 설정 | polygon.io | 틱 단위 데이터, 옵션 체인/Greeks, WebSocket 스트리밍 | $29/월~ | ★★★☆☆ |

**Alpha Vantage MCP 한 줄 설치 (Claude Code):**
```bash
claude mcp add alphavantage "https://mcp.alphavantage.co/mcp?apikey=YOUR_API_KEY"
```

### 2. 데이터베이스 MCP

| 서버명 | 설치 명령 | 기능 | 비용 | 우선순위 |
|--------|-----------|------|------|----------|
| **Supabase MCP** | `npx @supabase/mcp-server-supabase` | PostgreSQL, 인증, 실시간 구독, 엣지 함수, 스토리지 전체 관리 | 무료 티어 | ★★★★★ |
| **PostgreSQL MCP** | `npx @modelcontextprotocol/server-postgres` | 직접 SQL 실행, 스키마 조회 | DB 연결 필요 | ★★★★☆ |

### 3. 알림/메시징 MCP

| 서버명 | 설치 명령 | 기능 | 비용 | 우선순위 |
|--------|-----------|------|------|----------|
| **Telegram Notification MCP** | `npx telegram-notification-mcp` | 주가 알림, 포트폴리오 알림, Claude Code 완료 알림, 모바일 실시간 | 무료 (Bot Token 필요) | ★★★★★ |
| **Slack MCP (공식)** | `npx @modelcontextprotocol/server-slack` | 채널 메시지, DM, 파일 공유, 팀 알림 | Slack Bot Token 필요 | ★★★★★ |
| **NotifyMe MCP** | `git clone + 설정` | Slack + Discord 웹훅 | 무료 | ★★★☆☆ |

---

## [FINDING] 플랫폼 레이어별 갭 분석

| 레이어 | 현재 가능 | 추가 필요 | 갭 심각도 |
|--------|-----------|-----------|-----------|
| Layer 1: 데이터 수집 | Firecrawl, Playwright, Apify (스크래핑) | Alpha Vantage, Yahoo Finance MCP (API) | 중간 — 스크래핑으로 대체 가능하나 불안정 |
| Layer 2: 검색/리서치 | Tavily, Brave Search | Finnhub MCP (전문 금융 뉴스) | 낮음 — 일반 검색으로 충분 |
| Layer 3: 데이터 분석 | OMC Python REPL | 없음 (충분) | 없음 |
| Layer 4: 저장/관리 | Notion, Memory | Supabase MCP (관계형 DB) | 중간 — Notion으로 임시 가능 |
| Layer 5: 트레이딩 실행 | 없음 | Alpaca MCP, TradingView MCP | 높음 — 자동매매 완전 공백 |
| Layer 6: 알림/모니터링 | 없음 | Telegram MCP, Slack MCP | 높음 — 알림 시스템 완전 공백 |

[STAT:n] 현재 활성 서버 9개, 추가 권장 서버 12개, 총 21개 서버 조사 완료

---

## [FINDING] Claude Code 스킬 활용 방안

현재 OMC(oh-my-claudecode)에서 금융 플랫폼 개발에 활용 가능한 스킬:

| 스킬 | 트리거 | 금융 플랫폼 활용 |
|------|--------|----------------|
| `scientist` | 직접 호출 | 주가 데이터 분석, 백테스팅, 통계 검증 |
| `autopilot` | "autopilot" | 멀티 에이전트로 전체 플랫폼 개발 자동화 |
| `executor` | 위임 | Next.js 주식 대시보드 컴포넌트 구현 |
| `document-specialist` | SDK 조회 | yfinance, alpaca-py, finnhub-python 문서 조회 |
| `tracer` | "trace" | 데이터 파이프라인 추적/디버깅 |
| `test-engineer` | TDD | 주식 분석 함수 테스트 자동 생성 |

---

## 설치 우선순위 TOP 5 (즉시 실행 가이드)

### 1위: Alpha Vantage MCP (★★★★★)
```bash
# 1. API 키 발급: https://www.alphavantage.co/support/#api-key (무료)
# 2. Claude Code에 한 줄로 추가
claude mcp add alphavantage "https://mcp.alphavantage.co/mcp?apikey=YOUR_API_KEY"
```
- 100+ 도구, 기술적 지표 50개+, 펀더멘털, 경제지표 전부 포함

### 2위: Yahoo Finance MCP (★★★★★)
```bash
# API 키 없음 — 완전 무료
git clone https://github.com/leogue/StockMCP.git
cd StockMCP
pip install -r requirements.txt
# claude_desktop_config.json에 추가
```

### 3위: Telegram Notification MCP (★★★★★)
```bash
# 1. @BotFather로 Telegram Bot 생성 → Token 획득
# 2. 설치
npm install -g telegram-notification-mcp
# 또는
npx telegram-notification-mcp --token YOUR_BOT_TOKEN --chatId YOUR_CHAT_ID
```

### 4위: Supabase MCP (★★★★★)
```bash
# 1. supabase.com 계정 생성 (무료)
# 2. 프로젝트 생성 → URL, anon key 획득
npx @supabase/mcp-server-supabase --supabase-url YOUR_URL --supabase-key YOUR_KEY
```

### 5위: Finnhub MCP (★★★★☆)
```bash
# 1. API 키 발급: https://finnhub.io (무료 60req/분)
git clone https://github.com/sverze/stock-market-mcp-server.git
cd stock-market-mcp-server
npm install
export FINNHUB_API_KEY=your_key
```

---

## [LIMITATION]

1. **API 요청 제한**: 무료 API 키(Alpha Vantage 25회/일, Finnhub 60req/분)는 실시간 모니터링에 부족할 수 있음. 유료 플랜 검토 필요.
2. **한국 주식 데이터**: Alpha Vantage, Finnhub 모두 KRX(한국거래소) 데이터 제한적. 한국투자증권 API(KIS Developers) 또는 FinanceDataReader 별도 연동 필요.
3. **MCP 버전 호환성**: 일부 커뮤니티 MCP 서버는 유지보수 상태가 불안정. GitHub 최근 커밋 날짜 확인 필요.
4. **실시간 WebSocket**: 대부분 MCP 서버는 REST API 기반. 틱 단위 실시간 스트리밍은 Polygon.io 유료 플랜 또는 별도 WebSocket 구현 필요.
5. **자동매매 법적 리스크**: Alpaca는 미국 주식 전용. 한국 자동매매는 증권사 API(삼성증권 ELW, 키움증권 OpenAPI) 별도 연동 필요.

---

## 참고 자료

- [GitHub: financial-datasets/mcp-server](https://github.com/financial-datasets/mcp-server)
- [Alpha Vantage MCP 공식](https://mcp.alphavantage.co/)
- [MCP Servers 디렉토리](https://mcpservers.org/)
- [Top 5 MCP Servers for Financial Data in 2026 — Medium](https://medium.com/predict/top-5-mcp-servers-for-financial-data-in-2026-5bf45c2c559d)
- [Best MCP Servers for Stock Market Data — Medium](https://medium.com/data-science-collective/best-mcp-servers-for-stock-market-data-and-algorithmic-trading-ca51e89cd0a1)
- [AI Trading Copilot MCP Servers — PickMyTrade](https://blog.pickmytrade.trade/ai-trading-copilot-mcp-servers-stock-analysis-2025/)
- [Official MCP Servers — modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
- [Firecrawl Blog: Best MCP Servers](https://www.firecrawl.dev/blog/best-mcp-servers-for-developers)
- [Telegram Notification MCP](https://github.com/kstonekuan/telegram-notification-mcp)
- [NotifyMe MCP (Slack/Discord)](https://github.com/thesammykins/notifyme_mcp)
