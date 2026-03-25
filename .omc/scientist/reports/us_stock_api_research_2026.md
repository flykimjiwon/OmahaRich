# 미국 주식 투자를 위한 API & 데이터 소스 종합 조사 보고서

> 작성일: 2026-03-25  
> 대상: 한국에서 미국 주식 투자 및 자동매매를 위한 API/데이터 소스  
> 출처: 웹 검색 기반 (2025–2026년 최신 정보)

---

## 1. 미국 주식 데이터 API (시세 / 히스토리컬)

### 1-1. yfinance (Yahoo Finance 비공식 라이브러리)

| 항목 | 내용 |
|------|------|
| 비용 | 완전 무료 (오픈소스) |
| 데이터 지연 | 무료 15분 지연 / EOD 무료 |
| 실시간 여부 | 실시간 불가 (스크래핑 기반) |
| Python 지원 | `pip install yfinance` — pandas DataFrame 직접 반환 |
| API 키 필요 | 불필요 |
| 주요 특징 | - 가장 빠른 프로토타이핑 도구<br>- 주가·재무제표·배당·분할 정보 포함<br>- Yahoo Finance 백엔드 구조 변경 시 장애 위험<br>- 공식 API 아님 (비상업적 연구/교육 목적)<br>- 2025년 기준 가장 널리 쓰이는 무료 주가 데이터 도구 |
| 한계 | 서비스 안정성 불보장, 고빈도 요청 시 차단 가능 |

```python
import yfinance as yf
df = yf.download("AAPL", start="2024-01-01", end="2025-01-01")
print(df.head())
```

---

### 1-2. Alpha Vantage

| 항목 | 내용 |
|------|------|
| 비용 | 무료 티어 있음 / 유료 $50/월~ |
| 무료 티어 | 25 요청/일 (2025년 기준, 이전 500/일에서 대폭 축소됨) |
| 데이터 지연 | 무료: 15~20분 지연 / 유료: 실시간 |
| 실시간 여부 | 유료 플랜만 실시간 |
| Python 지원 | `pip install alpha_vantage` — 공식 라이브러리 제공 |
| API 키 필요 | 필요 (무료 등록) |
| 주요 특징 | - Nasdaq 공식 데이터 벤더<br>- 주식·외환·암호화폐·기술지표(50+ 종) 지원<br>- AI 기반 뉴스 센티먼트 점수 포함<br>- 무료 티어가 2025년에 25 req/일로 대폭 제한됨 (주의) |

---

### 1-3. Polygon.io (현재 "Massive"로 리브랜딩)

| 항목 | 내용 |
|------|------|
| 비용 | 무료 티어 있음 / 유료 $29~$199/월 |
| 무료 티어 | 5 요청/분, EOD 데이터, 2년 히스토리 |
| 데이터 지연 | 무료: 15분 지연 / 유료($79+): 실시간 |
| 실시간 여부 | 유료 Developer 플랜($79/월)부터 실시간 |
| WebSocket | 유료 Advanced 플랜($199/월)부터 스트리밍 |
| Python 지원 | 공식 Python SDK 제공 (`polygon-api-client`) |
| 주요 특징 | - 미국 주식 데이터 전문, 가장 높은 데이터 품질<br>- 틱(Tick) 단위 데이터, 옵션 체인 포함<br>- WebSocket 실시간 스트리밍 (고급 플랜)<br>- Alpaca 데이터 소스로도 사용됨<br>- 2025년 "Massive"로 리브랜딩 |

---

### 1-4. Finnhub

| 항목 | 내용 |
|------|------|
| 비용 | 무료 티어 있음 / 유료 $49~$299/월 |
| 무료 티어 | 60 요청/분 (비교적 넉넉함) |
| 데이터 지연 | 무료: 15분 지연 / 유료: 실시간 |
| 실시간 여부 | 유료만 실시간 |
| Python 지원 | 공식 Python SDK (`finnhub-python`) |
| 주요 특징 | - 주가·뉴스·센티먼트·수익 캘린더 통합<br>- 내부자 거래, 애널리스트 평점 포함<br>- 무료 티어가 다른 API 대비 관대한 편<br>- 뉴스+센티먼트 동시 제공이 강점 |

---

### 1-5. Tiingo

| 항목 | 내용 |
|------|------|
| 비용 | 무료 티어 있음 / 유료 $10~$30/월 |
| 무료 티어 | 50 심볼/시간, EOD 데이터 |
| 데이터 지연 | EOD 무료 / 실시간은 유료 |
| 실시간 여부 | 유료 플랜 필요 |
| Python 지원 | `pip install tiingo` 공식 라이브러리 |
| 주요 특징 | - 합리적인 가격의 고품질 EOD 데이터<br>- 뉴스 API 포함<br>- pandas_datareader 통합 지원<br>- 소규모 퀀트 프로젝트에 적합 |

---

### 1-6. Nasdaq Data Link (구 Quandl)

| 항목 | 내용 |
|------|------|
| 비용 | 일부 무료 / 대부분 유료 (데이터셋별 상이) |
| 무료 티어 | 공개 데이터셋 무료 / 프리미엄 데이터셋 유료 |
| 데이터 지연 | 대부분 EOD / 일부 실시간 |
| Python 지원 | `pip install nasdaq-data-link` 공식 라이브러리 |
| 주요 특징 | - 400개+ 데이터 소스, 수백만 시계열 데이터셋<br>- Quandl을 2018년 Nasdaq이 인수, 2021년 통합<br>- 거시경제·대체 데이터·선물 포함<br>- Excel Add-in 지원<br>- 퀀트 리서치에 특화 |

---

### 1-7. Financial Modeling Prep (FMP)

| 항목 | 내용 |
|------|------|
| 비용 | 무료 티어 있음 / 유료 $19/월 (플랫 가격) |
| 무료 티어 | 제한적 (일부 기본 엔드포인트) |
| 데이터 지연 | 유료 $19/월: 실시간 무제한 (REST+WebSocket) |
| 실시간 여부 | 유료 플랜: 실시간 |
| Python 지원 | REST API (Python requests 사용) |
| 주요 특징 | - 30년 이상 히스토리컬 데이터<br>- SEC EDGAR 재무제표 통합<br>- 투명한 플랫 가격 정책 ($19/월, 요청 무제한)<br>- 기본적 분석 데이터 강점 |

---

### 1-8. IEX Cloud (서비스 종료 — 주의!)

> **IEX Cloud는 2024년 8월 31일자로 서비스를 완전 종료했습니다.**  
> 기존 사용자는 Alpha Vantage, Polygon.io 등으로 마이그레이션 필요.

---

## 2. 미국 자동매매 API (브로커 API)

### 2-1. Alpaca Markets

| 항목 | 내용 |
|------|------|
| 비용 | 무료 (페이퍼 트레이딩 완전 무료) / 라이브 트레이딩 무수수료 |
| 실시간 여부 | 실시간 주문 실행 |
| Python 지원 | `pip install alpaca-py` 공식 라이브러리 |
| 한국 사용 가능? | 페이퍼 트레이딩: 전 세계 가능 / 라이브: 비미국 거주자는 초대제(invite-only) 또는 제한적 |
| 주요 특징 | - 개발자 친화적 API 1순위<br>- RESTful + WebSocket 스트리밍<br>- 페이퍼(모의) 트레이딩 환경 무료 제공<br>- 24/5 거래 지원 (Broker API)<br>- Polygon.io 데이터 통합 옵션<br>- 알고트레이딩 백테스팅 적합<br>- 한국 거주자 라이브 계좌: 현재 초대 대기 필요 |

```python
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

client = TradingClient("API_KEY", "SECRET_KEY", paper=True)
order = client.submit_order(MarketOrderRequest(
    symbol="AAPL", qty=1,
    side=OrderSide.BUY, time_in_force=TimeInForce.DAY
))
```

---

### 2-2. Interactive Brokers (IBKR)

| 항목 | 내용 |
|------|------|
| 비용 | 거래 수수료: $0.005/주 (최소 $1) / API 자체는 무료 |
| 실시간 여부 | 실시간 주문·데이터 |
| Python 지원 | 공식 TWS API (`ibapi`) + `ib_insync` (커뮤니티 래퍼, 더 편리) |
| 한국 사용 가능? | 가능 — 한국 거주자 계좌 개설 지원 |
| 주요 특징 | - 전문가급 브로커 API 표준<br>- TWS(Trader Workstation) 또는 IB Gateway 실행 필요<br>- 전 세계 135개 시장 접근<br>- 초저 수수료 (월 $10 최소 수수료 있었으나 2021년 폐지)<br>- 복잡한 설정이 단점 (학습 곡선 높음)<br>- 한국 거주자도 미국 주식 자동매매 가능 |

```python
from ib_insync import IB, Stock, MarketOrder
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)  # TWS 실행 필요
contract = Stock('AAPL', 'SMART', 'USD')
order = MarketOrder('BUY', 10)
trade = ib.placeOrder(contract, order)
```

---

### 2-3. TD Ameritrade / Schwab API

| 항목 | 내용 |
|------|------|
| 현황 | TD Ameritrade가 Charles Schwab에 합병 완료 (2024년) |
| API | Schwab Developer API로 전환 (schwabdev 라이브러리) |
| 한국 사용 가능? | 미국 거주자/시민권자 위주 — 한국 거주자 계좌 개설 어려움 |
| 주요 특징 | 미국 내 개인 투자자 중심, 한국에서는 사실상 사용 불가 |

---

## 3. SEC 공시 데이터 (EDGAR)

### 3-1. SEC EDGAR 공식 API (data.sec.gov)

| 항목 | 내용 |
|------|------|
| 비용 | 완전 무료 |
| API 키 | 불필요 |
| Python 지원 | `requests` 라이브러리로 직접 사용 |
| 주요 특징 | - SEC 공식 RESTful API (JSON 반환)<br>- 10-K, 10-Q, 8-K, Form 4, 13-F 등 150+ 공시 유형<br>- XBRL 재무 데이터 (companyfacts.zip 벌크 다운로드)<br>- 1993년~현재 1,800만+ 공시 |

```python
import requests
# 애플 재무제표 가져오기
url = "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json"
data = requests.get(url, headers={"User-Agent": "yourname@email.com"}).json()
```

---

### 3-2. EdgarTools (오픈소스 Python 라이브러리)

| 항목 | 내용 |
|------|------|
| 비용 | 완전 무료 (MIT 라이선스) |
| API 키 | 불필요 |
| Python 지원 | `pip install edgartools` |
| 주요 특징 | - SEC EDGAR 직접 파싱, 구조화된 데이터 반환<br>- 10-K·10-Q·8-K·내부자 거래·펀드 보유 파싱<br>- 속도 제한 없음 (공식 SEC 서버 직접 접근)<br>- 가장 사용하기 쉬운 EDGAR Python 인터페이스 |

```python
from edgartools import Company
apple = Company("AAPL")
filings = apple.get_filings(form="10-K")
```

---

### 3-3. sec-api.io (유료 래퍼)

| 항목 | 내용 |
|------|------|
| 비용 | 무료 API 키 제공 (제한적) / 유료 플랜 있음 |
| 주요 특징 | - 전문 파싱, 실시간 스트리밍 공시<br>- XBRL-to-JSON 변환 자동화<br>- 풀텍스트 검색 지원 |

---

## 4. 뉴스 & 센티먼트 API

### 4-1. Finnhub (뉴스+센티먼트 통합)

| 항목 | 내용 |
|------|------|
| 비용 | 무료 티어 60 req/분 |
| 주요 특징 | - 종목별 뉴스·시장 뉴스·내부자 센티먼트<br>- 애널리스트 평점 포함<br>- 단일 API로 데이터+뉴스 동시 수집 가능 |

---

### 4-2. Alpha Vantage News & Sentiment

| 항목 | 내용 |
|------|------|
| 비용 | 무료 티어 포함 (25 req/일) |
| 주요 특징 | - AI/ML 기반 센티먼트 점수<br>- 뉴스 소스: Reuters, Bloomberg, CNBC 등 |

---

### 4-3. Benzinga API

| 항목 | 내용 |
|------|------|
| 비용 | 무료 기본 티어 / 유료 플랜 (AWS Marketplace 통해 구독) |
| Python 지원 | 공식 Python 라이브러리 + TCP 스트리밍 |
| 주요 특징 | - 전문 금융 뉴스 전문 API<br>- 실시간 헤드라인·뉴스 본문<br>- 센티먼트 기반 가격 예측 모델 구축 가능<br>- 무료 티어: 헤드라인+요약+링크 제공 |

---

### 4-4. Stock News API

| 항목 | 내용 |
|------|------|
| 비용 | 무료 티어 있음 |
| 주요 특징 | - CNBC·Bloomberg·Seeking Alpha·Zacks 등 30+ 소스<br>- 각 기사별 positive/negative/neutral 센티먼트 점수<br>- 종목별 필터링 지원 |

---

### 4-5. NewsAPI

| 항목 | 내용 |
|------|------|
| 비용 | 무료 개발자 플랜 / 유료 $449/월~ |
| 주요 특징 | - 금융 특화 아님, 범용 뉴스 API<br>- 무료 티어: 100 req/일, 최근 1개월 기사만<br>- 금융 전용 API 대비 센티먼트 분석 기능 부족 |

---

## 5. 한국 증권사 해외주식 API

### 5-1. 한국투자증권 KIS Developers (가장 활성화)

| 항목 | 내용 |
|------|------|
| 비용 | 무료 (계좌 보유 조건) |
| 실시간 여부 | 실시간 시세 + WebSocket 지원 |
| Python 지원 | `pip install python-kis` (비공식 but 활발한 커뮤니티 라이브러리)<br>공식 GitHub 샘플 코드 제공 |
| API 키 | KIS Developers 포탈에서 App Key / App Secret 발급 |
| 주요 특징 | - 국내 증권사 최초 오픈 API (2022년 4월 출시)<br>- 국내주식 + **해외주식** + 선물/옵션 통합<br>- OAuth 2.0 인증 (액세스 토큰 발급)<br>- RESTful API + WebSocket 실시간 소켓<br>- 모의투자 환경 지원<br>- Claude·ChatGPT LLM 연동 샘플 코드 제공<br>- WikiDocs 한국어 튜토리얼 풍부 |
| 해외주식 지원 | 미국(NYSE·NASDAQ·AMEX)·홍콩·일본·중국·베트남 |
| 공식 포탈 | https://apiportal.koreainvestment.com |
| GitHub | https://github.com/koreainvestment/open-trading-api |

```python
import kis_api  # python-kis 패키지

# 미국 주식 현재가 조회
# (실제 코드는 공식 GitHub 샘플 참고)
```

---

### 5-2. 키움증권 Open API+

| 항목 | 내용 |
|------|------|
| 비용 | 무료 (계좌 보유 조건) |
| 실시간 여부 | 실시간 (국내주식 중심) |
| Python 지원 | PyQt5 기반 COM 방식 (Windows 전용) — 해외주식 API는 제한적 |
| 주요 특징 | - 국내 주식 자동매매 1위 점유율<br>- **해외주식 API는 제한적**: 주로 국내주식 중심<br>- Windows COM 방식이라 Linux/Mac 사용 불가<br>- 해외주식 자동매매는 한국투자증권 KIS 대비 기능 부족 |
| 한계 | 미국 주식 자동매매 목적이라면 KIS Developers 권장 |

---

### 5-3. 기타 증권사 현황

| 증권사 | 해외주식 API | 비고 |
|--------|-------------|------|
| 미래에셋증권 | OpenAPI 제공 (제한적) | 주로 국내주식 |
| 신한투자증권 | API 없음 (2025 기준) | — |
| NH투자증권 | API 없음 (2025 기준) | — |
| 삼성증권 | 내부 API만 | 공개 미제공 |

> 한국에서 미국 주식 자동매매 시 **한국투자증권 KIS Developers**가 사실상 유일한 한국 증권사 공개 API 옵션.

---

## 6. 종합 추천 조합

### 시나리오별 추천

| 목적 | 추천 조합 |
|------|----------|
| 빠른 프로토타이핑 / 학습 | `yfinance` + `EdgarTools` (둘 다 무료, 설정 불필요) |
| 퀀트 백테스팅 | `Polygon.io` (무료 EOD) + `Nasdaq Data Link` |
| 실시간 알고트레이딩 (국내 증권사) | **KIS Developers** (한국투자증권) — 한국 거주자 최적 |
| 실시간 알고트레이딩 (해외 브로커) | **IBKR** (`ib_insync`) — 전문가급, 한국 계좌 개설 가능 |
| 모의 트레이딩 개발 연습 | **Alpaca** 페이퍼 트레이딩 (전 세계 무료) |
| 뉴스 + 센티먼트 분석 | `Finnhub` (무료 60 req/분) 또는 `Alpha Vantage` |
| SEC 공시 분석 | `EdgarTools` (무료) 또는 `data.sec.gov` 직접 호출 |
| 가격 대비 최고 기본 분석 | `Financial Modeling Prep` ($19/월, 실시간 무제한) |

---

## 7. 중요 주의사항

1. **IEX Cloud 종료**: 2024년 8월 31일 완전 폐쇄. 대체재로 Polygon.io, Alpha Vantage 권장.
2. **Alpha Vantage 무료 축소**: 2025년 기준 무료 티어가 25 req/일로 대폭 축소 (이전 500 req/일 대비).
3. **Alpaca 라이브 트레이딩**: 한국 거주자는 현재 초대제(invite-only). 페이퍼 트레이딩은 전 세계 무료.
4. **yfinance 안정성**: 공식 API가 아니므로 프로덕션 사용 비권장. 연구/학습 목적으로만 사용.
5. **Polygon.io 리브랜딩**: "Massive"로 리브랜딩 진행 중 (2025년). URL은 polygon.io 유지.
6. **키움증권**: Windows COM 방식으로 미국 주식 자동매매에는 비적합. KIS 권장.

---

## 참고 자료

- [KIS Developers 공식 포탈](https://apiportal.koreainvestment.com/intro)
- [KIS Open API GitHub](https://github.com/koreainvestment/open-trading-api)
- [python-kis PyPI](https://pypi.org/project/python-kis/)
- [Alpaca Markets API Docs](https://docs.alpaca.markets/)
- [IBKR Python API 가이드](https://www.interactivebrokers.com/campus/ibkr-quant-news/interactive-brokers-python-api-native-a-step-by-step-guide/)
- [SEC EDGAR Developer Resources](https://www.sec.gov/about/developer-resources)
- [EdgarTools 공식 문서](https://edgartools.readthedocs.io/)
- [Polygon.io 가격 정책](https://polygon.io/pricing)
- [Finnhub API](https://finnhub.io/)
- [Tiingo API](https://www.tiingo.com/)
- [Nasdaq Data Link](https://data.nasdaq.com/)
- [Alpha Vantage](https://www.alphavantage.co/)
- [IEX Cloud 종료 공지](https://iexcloud.org/)
- [yfinance PyPI](https://pypi.org/project/yfinance/)
