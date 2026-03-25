# CLAUDE.md — 오마하부자 프로젝트 컨텍스트

> 워렌 버핏 가치투자 철학 기반 AI 주식투자 종합 플랫폼

---

## 프로젝트 개요

**오마하부자 (OmahaRich)** — 한국투자증권 KIS API + AI 분석을 결합한 가치투자 플랫폼.
한국(KRX) + 미국(NYSE/NASDAQ) 양쪽 시장 지원. 버핏식 가치투자 분석 자동화.

---

## 아키텍처

```
apps/web (Next.js 16)  ←→  backend (FastAPI)  ←→  KIS API / DART / SEC
     :3101                     :8101                 외부 데이터 소스
```

| 레이어 | 기술 | 역할 |
|--------|------|------|
| **프론트엔드** | Next.js 16 (App Router) + Tailwind v4 | 대시보드 UI |
| **백엔드** | FastAPI (Python) | API 서버, 분석 엔진 |
| **브로커** | 한국투자증권 KIS API | 시세 조회, 주문 실행 |
| **데이터** | DART, SEC EDGAR, pykrx, yfinance | 재무제표, 공시, 시장 데이터 |
| **AI** | OpenAI GPT / Claude API | 가치투자 분석, 뉴스 센티먼트 |
| **DB** | Supabase (예정) | 포트폴리오, 사용자 데이터 |

---

## 디렉토리 구조

```
오마하부자/
├── apps/web/                    # Next.js 프론트엔드
│   ├── app/                     #   App Router 페이지
│   │   ├── page.tsx             #     대시보드
│   │   ├── analysis/            #     종목 분석
│   │   ├── portfolio/           #     포트폴리오
│   │   └── news/                #     뉴스/공시
│   └── components/layout/       #   Header, Sidebar
├── backend/                     # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py              #   FastAPI 진입점
│   │   ├── config.py            #   환경변수 설정
│   │   ├── api/v1/              #   API 라우트 (stocks, analysis, portfolio, news)
│   │   ├── services/
│   │   │   ├── kis/             #   KIS API 연동 (auth, client, domestic, overseas)
│   │   │   ├── analysis/        #   가치투자 분석 (value, financial, technical)
│   │   │   ├── data/            #   데이터 소스 (dart, edgar, market)
│   │   │   ├── ai/              #   AI 분석기 (prompts, analyzer)
│   │   │   └── news/            #   뉴스 센티먼트
│   │   ├── models/              #   DB 모델
│   │   └── schemas/             #   Pydantic 스키마
│   ├── requirements.txt
│   └── tests/
├── packages/shared/             # 공유 타입 (TypeScript)
├── CLAUDE.md                    # (이 파일)
├── RESEARCH.md                  # API & 인프라 조사 보고서
├── turbo.json                   # Turborepo 설정
└── package.json                 # 모노레포 루트
```

---

## 개발 명령어

### 프론트엔드
```bash
npm run dev:web          # Next.js 개발 서버 (localhost:3101)
npm run build            # 전체 빌드
npm run type-check       # TypeScript 검사
```

### 백엔드
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000   # API 서버 (localhost:8101)
pytest tests/                                # 테스트
```

### API 문서
- FastAPI Swagger: http://localhost:8101/docs
- FastAPI ReDoc: http://localhost:8101/redoc

---

## 환경변수

`backend/.env` (`.env.example` 참고):

```
# KIS API (한국투자증권)
KIS_APP_KEY=
KIS_APP_SECRET=
KIS_ACCOUNT_NO=           # 계좌번호 (8자리-2자리)
KIS_IS_VIRTUAL=true       # true=모의투자, false=실전

# AI
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# 데이터
DART_API_KEY=             # https://opendart.fss.or.kr/

# MCP (Claude Code 자동 등록됨)
# Alpha Vantage, Yahoo Finance, Finnhub
```

---

## 핵심 API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/v1/stocks/{symbol}/price` | 주식 현재가 |
| GET | `/api/v1/stocks/{symbol}/history` | 기간별 시세 |
| GET | `/api/v1/analysis/{symbol}/value` | 가치투자 분석 |
| GET | `/api/v1/analysis/{symbol}/intrinsic-value` | 내재가치 계산 |
| GET | `/api/v1/analysis/{symbol}/moat` | 경제적 해자 분석 |
| GET | `/api/v1/portfolio` | 포트폴리오 조회 |
| POST | `/api/v1/portfolio` | 종목 추가 |
| GET | `/api/v1/news/{symbol}` | 종목 뉴스 |

---

## 코딩 규칙

### 공통
- `as any`, `@ts-ignore`, `@ts-expect-error`, `type: ignore` **절대 금지**
- 빈 catch 블록 금지
- 모든 함수에 타입 힌트/타입 어노테이션 필수

### TypeScript (프론트엔드)
- strict 모드
- 컴포넌트: PascalCase, 유틸: camelCase
- 새 공유 타입은 `packages/shared/src/types/`에 추가

### Python (백엔드)
- async 우선 (FastAPI 비동기)
- Pydantic v2 스키마
- `from __future__ import annotations` 전 파일
- 서비스 레이어 패턴: API Route → Service → External API

---

## KIS API 핵심 정보

- **실전**: `https://openapi.koreainvestment.com:9443`
- **모의**: `https://openapivts.koreainvestment.com:29443`
- **인증**: OAuth 2.0 (appkey + appsecret → access_token, 유효기간 1일)
- **유량 제한**: 초당 20건 (기본), 신규 3일간 초당 3건
- **주요 TR**: 국내시세 `FHKST01010100`, 국내일별 `FHKST01010400`, 해외시세 `HHDFS76200200`

---

## 설치된 MCP 서버

| MCP | 용도 | API 키 |
|-----|------|--------|
| Alpha Vantage | 글로벌 금융 데이터 100+ 도구 | 필요 (무료 발급) |
| Yahoo Finance | 주가, 재무제표 (무료) | 불필요 |
| Finnhub | 뉴스, 센티먼트, 기업 프로필 | 필요 (무료 발급) |
| Firecrawl | 웹 스크래핑 | 기존 설치 |
| Tavily | AI 검색 | 기존 설치 |
| Playwright | 브라우저 자동화 | 기존 설치 |

---

## 디자인 컨셉

- **테마**: 워렌 버핏 / 오마하 — 고급 다크 + 골드
- **Primary (Gold)**: #D4A843
- **Background (Dark)**: #0F1419, #1A1F2E
- **Text (Warm White)**: #F5F0E8
- **Success**: #4ADE80, **Danger**: #F87171

---

## 로드맵

### Stage 1 (현재) — 기초 인프라
- [x] 모노레포 스캐폴딩 (Next.js + FastAPI)
- [x] KIS API 연동 모듈
- [x] 가치투자 분석 엔진
- [x] MCP 서버 설치
- [ ] 프론트엔드-백엔드 연동
- [ ] KIS 모의투자 실제 테스트

### Stage 2 — 데이터 & AI
- [ ] DART/SEC 실데이터 연동
- [ ] AI 분석 리포트 생성
- [ ] 뉴스 센티먼트 실시간 수집
- [ ] Supabase DB 연동

### Stage 3 — 수익화
- [ ] 실전 자동매매
- [ ] 포트폴리오 리밸런싱
- [ ] Telegram 알림
- [ ] 사용자 인증 & 결제

---

## 주의사항

- KIS API 키(appkey, appsecret, access_token) **외부 노출 절대 금지**
- 실전 매매 전 반드시 모의투자(`KIS_IS_VIRTUAL=true`)로 충분히 테스트
- AI 분석 결과는 **투자 참고용**이며 투자 판단의 최종 책임은 사용자에게 있음
- 한글 경로 이슈: Next.js Turbopack이 멀티바이트 경로에서 패닉 → `--webpack` / `--no-turbopack` 사용
