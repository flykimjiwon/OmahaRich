# 오마하부자 - API & 인프라 조사 종합 보고서

> 조사일: 2026-03-25

---

## 1. 한국 증권사 자동투자 API

### 1-1. 실전 사용 가능 (Open API)

| 증권사 | API 방식 | 한국 | 미국 | 주문 | Linux/Mac | 특이사항 |
|--------|---------|:----:|:----:|:----:|:---------:|---------|
| **한국투자증권 KIS** | REST + WebSocket | O | O | O | **O** | **1순위 추천**. 국내 유일 순수 REST API. 모의투자 환경 제공. Python SDK 풍부 (mojito, python-kis, pykis) |
| **키움증권 OpenAPI+** | COM/OCX (Windows) | O | X | O | X | 커뮤니티 최대. 1초 5회 제한. Windows 전용 |
| **LS증권 (구 이베스트)** | COM/DLL + REST(신규) | O | 일부 | O | 신규만 | xingAPI(레거시) + Open API(REST 신규) 병행 |
| **대신증권 크레온** | COM (Windows) | O | X | O | X | 문서화 우수. 동기 응답 |
| **NH투자증권 QV** | DLL/COM (Windows) | O | 일부 | O | X | 조건부 자동 분할매매 내장 |

### 1-2. 사실상 불가

| 증권사 | 상태 |
|--------|------|
| 삼성증권 | 공개 오픈API 미제공 |
| 미래에셋증권 | AnyLink 2017년 서비스 종료 |
| 토스증권 | 내부 전용 (미공개) |
| 카카오페이증권 | 내부 전용 (미공개) |

### 1-3. 데이터 전용 API

| 서비스 | 방식 | 무료 | 용도 |
|--------|------|:----:|------|
| **OpenDART** | REST | O | 재무제표, 사업보고서, 공시 전문 |
| **KRX Open API** | REST | O | 종목/지수/공매도 (실시간 미지원) |
| **공공데이터포털** | REST | O | 한국예탁결제원 기초 종목 정보 |
| **CODEF** | REST | O | 스크래핑 방식 다중 증권사 잔고 조회 (주문 불가) |

---

## 2. 미국 주식 API

### 2-1. 데이터 API

| 서비스 | 무료 티어 | 실시간 | Python | 특징 |
|--------|----------|:------:|--------|------|
| **yfinance** | 완전 무료, 키 불필요 | X (EOD) | `pip install yfinance` | 프로토타이핑 최적. 비공식이라 불안정 위험 |
| **Alpha Vantage** | 25 req/일 | 유료만 | `pip install alpha_vantage` | 50+ 기술지표, AI 센티먼트 점수 |
| **Polygon.io (Massive)** | 5 req/분, EOD | $79/월~ | `polygon-api-client` | 틱 단위 최고 품질. Alpaca 데이터 소스 |
| **Finnhub** | 60 req/분 | 유료만 | `pip install finnhub-python` | 뉴스+센티먼트+내부자거래 통합 |
| **Tiingo** | 50 심볼/시간 | 유료 | `pip install tiingo` | 합리적 가격. 소규모 퀀트 적합 |
| **FMP** | 제한적 | $19/월 무제한 | 공식 SDK | 30년 히스토리, SEC 통합. 가성비 최고 |
| **Nasdaq Data Link** | 공개 데이터 무료 | - | `pip install nasdaq-data-link` | 400개+ 소스, 거시경제/대체 데이터 |
| **IEX Cloud** | **서비스 종료 (2024.08)** | - | - | 사용 불가 |

### 2-2. 자동매매 브로커 API

| 서비스 | 비용 | 한국 사용 | Python | 특징 |
|--------|------|:---------:|--------|------|
| **Alpaca** | 무료 (페이퍼) | 페이퍼만 가능 | `pip install alpaca-py` | 개발자 친화 1순위. 모의투자 최적 |
| **Interactive Brokers** | $0.005/주 | O (계좌 개설 가능) | `ib_insync` | 전문가급. 135개 시장. 설정 복잡 |
| **TD Ameritrade** | Schwab 합병 | X | - | 한국 거주자 불가. 제외 |

### 2-3. SEC 공시

| 서비스 | 비용 | 특징 |
|--------|------|------|
| **data.sec.gov** | 완전 무료 | 10-K, 10-Q, 8-K 등 1,800만+ 공시 |
| **EdgarTools** | 무료 (MIT) | `pip install edgartools` — SEC EDGAR 최고 파서 |
| **sec-api.io** | 무료 키(제한) | 실시간 스트리밍 공시 |

### 2-4. 뉴스/센티먼트

| 서비스 | 무료 | 특징 |
|--------|:----:|------|
| **Finnhub** | 60 req/분 | 뉴스+센티먼트+데이터 통합 |
| **Alpha Vantage** | 25 req/일 | AI 센티먼트 점수 |
| **Benzinga** | 기본 무료 | 전문 금융 뉴스 |
| **NewsAPI** | 100 req/일 | 범용 뉴스 (금융 특화 아님) |

### 2-5. 한국에서 미국 주식 자동매매

> **한국투자증권 KIS API가 유일한 현실적 선택지**
> - 미국(NYSE/NASDAQ/AMEX) + 홍콩/일본/중국/베트남 지원
> - REST + WebSocket, 모의투자 환경 제공
> - Python: `python-kis`, `mojito2`

---

## 3. Python 오픈소스 라이브러리

| 라이브러리 | 설치 | 한국 | 미국 | 실시간 | 주문 | API키 |
|-----------|------|:----:|:----:|:------:|:----:|:-----:|
| **pykrx** | `pip install pykrx` | O | X | X | X | 불필요 |
| **FinanceDataReader** | `pip install finance-datareader` | O | O | X | X | 불필요 |
| **mojito** | `pip install mojito2` | O | O | X | O | KIS |
| **python-kis** | `pip install python-kis` | O | O | O | O | KIS |
| **pykis** | `pip install pykis` | O | O | X | O | KIS |
| **KOAPY** | `pip install koapy` | O | X | O | O | 키움 |
| **OpenDartReader** | `pip install opendartreader` | O(공시) | X | X | X | DART |
| **EdgarTools** | `pip install edgartools` | X | O(공시) | X | X | 불필요 |

---

## 4. MCP 서버 (현재 설치 + 추가 권장)

### 4-1. 현재 이미 설치됨 (즉시 활용 가능)

| MCP 서버 | 금융 플랫폼 활용 |
|----------|----------------|
| **Firecrawl** | Yahoo Finance 스크래핑, 공시 크롤링 |
| **Playwright** | 증권사 웹사이트 자동화, 로그인 필요 데이터 |
| **Tavily** | 금융 뉴스 검색, 시장 동향 조사 |
| **Brave Search** | 금융 정보 검색 |
| **Apify** | Yahoo Finance Actor, 뉴스 크롤러 |
| **Notion** | 투자 일지, 포트폴리오 추적 |
| **Python REPL** | 백테스팅, 기술 분석, 시각화 |
| **Memory** | 종목 분석 히스토리, 투자 패턴 추적 |
| **Context7** | yfinance, backtrader 등 라이브러리 문서 |

### 4-2. 추가 설치 권장

| 우선순위 | MCP 서버 | 비용 | 용도 | 설치 |
|---------|----------|------|------|------|
| ★★★★★ | **Alpha Vantage MCP** | 무료 25회/일 | 100+ 금융 도구, 기술지표 50개 | `claude mcp add alphavantage "https://mcp.alphavantage.co/mcp?apikey=KEY"` |
| ★★★★★ | **Yahoo Finance MCP** | 완전 무료 | 실시간 주가, PER, 시총 (키 불필요) | git clone StockMCP |
| ★★★★★ | **Supabase MCP** | 무료 티어 | PostgreSQL + 인증 + 실시간 | `npx @supabase/mcp-server-supabase` |
| ★★★★★ | **Telegram MCP** | 무료 (Bot Token) | 주가 알림, 포트폴리오 알림 | `npx telegram-notification-mcp` |
| ★★★★☆ | **Finnhub MCP** | 무료 60req/분 | 뉴스, 감성분석, 내부자거래 | git clone stock-market-mcp-server |
| ★★★★☆ | **TradingView MCP** | 무료 | 캔들 패턴, 기술 분석 | git clone |
| ★★★★☆ | **Alpaca MCP** | 무료 (페이퍼) | 자연어 주문, 모의매매 | npm install |
| ★★★★☆ | **Slack MCP** | Bot Token | 채널 알림, 팀 협업 | 공식 제공 |

---

## 5. 오마하부자 추천 스택

### 핵심 API 조합

```
[한국 주식 시세+주문]  → 한국투자증권 KIS API (python-kis)
[한국 공시/재무제표]   → OpenDART API (opendartreader)
[한국 히스토리 데이터]  → pykrx + FinanceDataReader
[미국 주식 시세]       → yfinance (프로토타입) → FMP/Polygon (프로덕션)
[미국 공시]           → SEC EDGAR (edgartools)
[미국 자동매매]        → KIS API 해외주식 (한국 계좌) 또는 Alpaca (페이퍼)
[뉴스/센티먼트]        → Finnhub (무료 60req/분)
[DB]                 → Supabase (PostgreSQL)
[알림]               → Telegram Bot
```

### 갭 분석

```
Layer 1: 데이터 수집     [해결] KIS + pykrx + yfinance + DART
Layer 2: 검색/리서치     [해결] Tavily + Brave + Finnhub
Layer 3: 데이터 분석     [해결] Python + pandas + numpy
Layer 4: AI 분석        [해결] OpenAI GPT / Claude API
Layer 5: 저장/관리       [필요] Supabase MCP 설치 필요
Layer 6: 트레이딩 실행   [필요] KIS API 계정 + python-kis 연동
Layer 7: 알림/모니터링   [필요] Telegram MCP 설치 필요
```

---

## 6. 한국투자증권 KIS API 상세 (사용자 제공 참고)

### 주요 공지사항 (2026.03 기준)
- **신규 고객 초당 호출 제한**: 2026.04.03부터 신규 신청 시 3일간 초당 3건 제한 → 이후 기본 유량
- **보안 관리**: appkey, appsecret, access_token 외부 노출 절대 금지
- **WebSocket 무한 연결 차단**: 비정상 접속 패턴 IP/앱키 차단 예정

### 주식현재가 시세 API 예시
- **Endpoint**: `GET /uapi/domestic-stock/v1/quotations/inquire-price`
- **실전 Domain**: `https://openapi.koreainvestment.com:9443`
- **모의 Domain**: `https://openapivts.koreainvestment.com:29443`
- **TR ID**: `FHKST01010100`
- **주요 응답 필드**: 현재가(stck_prpr), 전일대비(prdy_vrss), PER, PBR, EPS, BPS, 52주 고저, 외국인 보유량, 시가총액 등

---

## 7. 참고 링크

### 한국
- [KIS Developers 포탈](https://apiportal.koreainvestment.com/intro)
- [KIS GitHub](https://github.com/koreainvestment/open-trading-api)
- [OpenDART](https://opendart.fss.or.kr/intro/main.do)
- [KRX Open API](https://openapi.krx.co.kr/)
- [pykrx GitHub](https://github.com/sharebook-kr/pykrx)
- [FinanceDataReader GitHub](https://github.com/FinanceData/FinanceDataReader)
- [python-kis GitHub](https://github.com/Soju06/python-kis)
- [mojito GitHub](https://github.com/sharebook-kr/mojito)

### 미국
- [Alpha Vantage](https://www.alphavantage.co/)
- [Polygon.io](https://polygon.io/)
- [Finnhub](https://finnhub.io/)
- [Alpaca Markets](https://alpaca.markets/)
- [SEC EDGAR](https://www.sec.gov/about/developer-resources)
- [EdgarTools](https://edgartools.readthedocs.io/)
- [FMP](https://financialmodelingprep.com/)
- [yfinance PyPI](https://pypi.org/project/yfinance/)
