# 대한민국 주식 자동매매 API 완전 조사 보고서

> 작성일: 2026-03-25
> 조사 범위: 증권사 오픈API, 핀테크 API, 데이터 API, 오픈소스 라이브러리

---

## 1. 증권사 오픈 API

### 1-1. 한국투자증권 (KIS) Open API

| 항목 | 내용 |
|------|------|
| **서비스명** | KIS Developers / eFriend Expert Open API |
| **API 종류** | REST API + WebSocket |
| **주요 기능** | 시세 조회, 주식 주문(매수/매도/정정/취소), 잔고 조회, 실시간 체결, 현재가, 호가, 차트 데이터 |
| **한국 주식** | 지원 |
| **미국 주식** | 지원 (해외주식 포함) |
| **무료/유료** | 무료 |
| **개인 개발자** | 가능 (계좌 개설 후 신청) |
| **공식 문서** | https://apiportal.koreainvestment.com/intro |
| **Python SDK** | 공식 GitHub 예제 제공 (https://github.com/koreainvestment/open-trading-api) |
| **특이사항** | 국내 최초 순수 REST API 방식 증권사 API (2022년 4월 출시). Linux/Mac 환경에서도 개발 가능. ChatGPT·Claude 등 LLM 연동 사례 多 |

---

### 1-2. 키움증권 OpenAPI+

| 항목 | 내용 |
|------|------|
| **서비스명** | 키움증권 OpenAPI+ |
| **API 종류** | COM/OCX (Windows 전용 ActiveX) |
| **주요 기능** | 시세 조회, 주식/선물/옵션 주문, 잔고 조회, 실시간 체결, 조건 검색 |
| **한국 주식** | 지원 |
| **미국 주식** | 미지원 (국내 전용) |
| **무료/유료** | 무료 |
| **개인 개발자** | 가능 (계좌 개설 후 신청, Windows 필수) |
| **공식 문서** | https://www.kiwoom.com/h/customer/download/VOpenApiInfoView |
| **Python SDK** | 직접 지원 없음. 커뮤니티 래퍼 다수 존재 (KOAPY, kiwoom 등) |
| **특이사항** | 국내 자동매매 커뮤니티에서 가장 널리 사용. 1초 5회 / 1시간 1000회 요청 제한. Windows 32비트 환경 필수로 개발 난이도 높음. 보안 강함(비밀번호 코드 노출 없음) |

---

### 1-3. LS증권 (구 이베스트투자증권) xingAPI / Open API

| 항목 | 내용 |
|------|------|
| **서비스명** | xingAPI (DLL/COM 방식) + LS Open API (REST 방식) |
| **API 종류** | COM/DLL (레거시) + REST API (신규) |
| **주요 기능** | 시세 조회, 주식 주문, 잔고 조회, 실시간 데이터, 차트, 선물/옵션 |
| **한국 주식** | 지원 |
| **미국 주식** | 일부 지원 |
| **무료/유료** | 무료 |
| **개인 개발자** | 가능 |
| **공식 문서** | https://openapi.ls-sec.co.kr/intro |
| **Python SDK** | 커뮤니티 래퍼 존재 (Go 래퍼: github.com/gobenpark/lssec-go) |
| **특이사항** | xingAPI는 COM/DLL 방식으로 Windows 필수였으나 신규 Open API는 REST 지원. 수수료 저렴하여 알고트레이더들에게 인기. API Signature가 직관적이지 않다는 평가 있음 |

---

### 1-4. 대신증권 CYBOS Plus / 크레온 API

| 항목 | 내용 |
|------|------|
| **서비스명** | CYBOS Plus (사이보스플러스) / Creon Plus |
| **API 종류** | COM Object (Windows 전용) |
| **주요 기능** | 시세 조회, 주식/선물/옵션/야간선물 주문, 잔고 조회, 실시간 체결, 조건 검색 |
| **한국 주식** | 지원 |
| **미국 주식** | 미지원 |
| **무료/유료** | 무료 |
| **개인 개발자** | 가능 |
| **공식 문서** | https://money2.daishin.com/E5/WTS/Customer/GuideTrading/DW_CybosPlus_Page.aspx |
| **Python SDK** | VB, C#, Python 등 COM 지원 언어 모두 가능. 비공식 도움말: https://cybosplus.github.io/ |
| **특이사항** | 문서화 우수, API 설계 직관적, 요청 결과를 동기적으로 수신 가능. 15초에 60건(시세)/20건(주문) 제한. 역사가 오래되어 학습 자료 풍부 |

---

### 1-5. NH투자증권 QV Open API

| 항목 | 내용 |
|------|------|
| **서비스명** | QV Open API (나무증권) |
| **API 종류** | DLL/COM (Windows 전용) |
| **주요 기능** | 시세 조회, 주문 (조건부 자동매매), 잔고 조회, 실시간 데이터 |
| **한국 주식** | 지원 |
| **미국 주식** | 일부 지원 |
| **무료/유료** | 무료 |
| **개인 개발자** | 가능 |
| **공식 문서** | https://www.nhqv.com/WMDoc.action?viewPage=/guestGuide/trading/openAPI.jsp |
| **Python SDK** | 미공식. Rust 래퍼 존재 (github.com/bekker/qvopenapi-rs) |
| **특이사항** | QV Auto Trade 기능으로 조건부 자동 분할매수/분할매도 지원. 나무증권(모바일) 브랜드로 서비스 |

---

### 1-6. 삼성증권

| 항목 | 내용 |
|------|------|
| **서비스명** | POP HTS / POP DTS |
| **API 종류** | HTS 플러그인 기반 (제한적) |
| **주요 기능** | 제한적 자동화 (HTS 매크로 수준) |
| **한국 주식** | 지원 |
| **미국 주식** | 지원 (HTS 내) |
| **무료/유료** | 무료 |
| **개인 개발자** | 공개 오픈API 미제공 |
| **공식 문서** | https://www.samsungpop.com (다운로드 센터) |
| **Python SDK** | 미지원 |
| **특이사항** | 공개 오픈API 미제공. HTS 기반 제한적 자동화만 가능. 개인 알고트레이딩 용도로는 부적합 |

---

### 1-7. 미래에셋증권

| 항목 | 내용 |
|------|------|
| **서비스명** | AnyLink (플러그인, 서비스 종료) |
| **API 종류** | 플러그인 방식 (신규 신청 2017년 7월 중단) |
| **주요 기능** | 제한적 (서비스 종료) |
| **한국 주식** | 지원 |
| **미국 주식** | 지원 |
| **무료/유료** | 해당 없음 |
| **개인 개발자** | 신규 신청 불가 |
| **공식 문서** | https://securities.miraeasset.com/imf/200/imf401.do |
| **Python SDK** | 미지원 |
| **특이사항** | 오픈API 미제공. 자동매매 조건 미지원. 알고트레이딩 불가 |

---

## 2. 핀테크/스타트업 API

### 2-1. 토스증권

| 항목 | 내용 |
|------|------|
| **서비스명** | 토스증권 (Toss Securities) |
| **API 종류** | 내부 REST API (외부 개방 없음) |
| **주요 기능** | 모바일 주식 거래, 소수점 매매 |
| **한국 주식** | 지원 |
| **미국 주식** | 지원 |
| **무료/유료** | 해당 없음 |
| **개인 개발자** | 외부 오픈API 미제공 |
| **공식 문서** | 없음 (외부 API 미공개) |
| **Python SDK** | 미지원 |
| **특이사항** | 원장 시스템/시세 정보를 외부 오픈API로 연계하는 방식으로 MTS를 구현했으나, 자동매매용 외부 API 미제공 |

---

### 2-2. 카카오페이증권

| 항목 | 내용 |
|------|------|
| **서비스명** | 카카오페이증권 |
| **API 종류** | 내부 REST API (외부 개방 없음) |
| **주요 기능** | 모바일 주식/펀드 거래 |
| **한국 주식** | 지원 |
| **미국 주식** | 지원 |
| **무료/유료** | 해당 없음 |
| **개인 개발자** | 외부 오픈API 미제공 |
| **공식 문서** | 없음 |
| **Python SDK** | 미지원 |
| **특이사항** | 카카오 생태계 연동 MTS 서비스. 자동매매용 외부 API 미제공 |

---

### 2-3. CODEF API (핀테크 스크래핑 API)

| 항목 | 내용 |
|------|------|
| **서비스명** | CODEF (코드에프) |
| **API 종류** | REST API |
| **주요 기능** | 다중 증권사 계좌 잔고 조회, 거래 내역 조회 (스크래핑 방식). 주문 기능 없음 |
| **한국 주식** | 잔고/거래내역 조회만 지원 |
| **미국 주식** | 일부 증권사 해외 잔고 조회 |
| **무료/유료** | 일부 무료 (Free Tier) + 유료 |
| **개인 개발자** | 가능 (Sandbox 환경 제공) |
| **공식 문서** | https://developer.codef.io/products/stock/overview |
| **Python SDK** | 공식 Python 바인딩: https://github.com/codef-io/codef-python |
| **특이사항** | 직접 API가 아닌 스크래핑 방식으로 여러 금융기관 데이터 통합 조회. 주문 불가, 데이터 조회 전용 |

---

## 3. 데이터 제공 API

### 3-1. 한국거래소 KRX Open API

| 항목 | 내용 |
|------|------|
| **서비스명** | KRX Open API / KRX Data Marketplace |
| **API 종류** | REST API |
| **주요 기능** | 주식/채권/파생상품 시세, 종목 정보, 지수, 공매도 정보, 투자 분석 정보 |
| **한국 주식** | 지원 (KRX 상장 전 종목) |
| **미국 주식** | 미지원 |
| **무료/유료** | 무료 (일부 고급 데이터 유료) |
| **개인 개발자** | 가능 (회원가입 후 키 발급) |
| **공식 문서** | https://openapi.krx.co.kr / https://data.krx.co.kr |
| **Python SDK** | 미공식. pykrx 라이브러리가 KRX 데이터 활용 |
| **특이사항** | 실시간 데이터 미지원 (일별 데이터 중심). 종목 코드, 상장 현황, 지수 구성 등 기초 데이터에 강점 |

---

### 3-2. DART 전자공시 Open API (OpenDart)

| 항목 | 내용 |
|------|------|
| **서비스명** | OpenDART (금융감독원 전자공시 시스템) |
| **API 종류** | REST API |
| **주요 기능** | 재무제표, 사업보고서, 주요사항보고, 지분공시, 분기별 재무데이터, 공시 검색 |
| **한국 주식** | 지원 (국내 상장/비상장 기업 공시) |
| **미국 주식** | 미지원 |
| **무료/유료** | 무료 |
| **개인 개발자** | 가능 (API Key 발급 후 이용) |
| **공식 문서** | https://opendart.fss.or.kr/intro/main.do |
| **Python SDK** | OpenDartReader 라이브러리 (pip install opendartreader) |
| **특이사항** | 2020년 1월 서비스 시작. 퀀트 투자 재무 분석의 핵심 데이터 소스. 분기/반기/연간 재무제표 자동 수집 가능 |

---

### 3-3. 네이버 금융 (비공식)

| 항목 | 내용 |
|------|------|
| **서비스명** | 네이버 금융 (finance.naver.com) |
| **API 종류** | 비공식 스크래핑 (공식 API 없음) |
| **주요 기능** | 주가 데이터, 재무 정보, 종목 정보 (스크래핑) |
| **한국 주식** | 지원 |
| **미국 주식** | 일부 |
| **무료/유료** | 무료 (비공식) |
| **개인 개발자** | 가능 (단, 이용약관 주의) |
| **공식 문서** | 없음 (비공식) |
| **Python SDK** | pykrx, FinanceDataReader 등이 내부적으로 활용 |
| **특이사항** | 공식 API 없음. pykrx가 네이버 금융 데이터를 스크래핑하여 제공. 서비스 변경 시 동작 불안정 가능 |

---

### 3-4. 공공데이터포털 금융 API

| 항목 | 내용 |
|------|------|
| **서비스명** | 공공데이터포털 (data.go.kr) 금융 API |
| **API 종류** | REST API |
| **주요 기능** | 한국예탁결제원 주식정보, 종목 코드, 기업 정보 |
| **한국 주식** | 지원 |
| **미국 주식** | 미지원 |
| **무료/유료** | 무료 |
| **개인 개발자** | 가능 |
| **공식 문서** | https://www.data.go.kr/data/15001145/openapi.do |
| **Python SDK** | 미공식 |
| **특이사항** | 실시간 데이터 없음. 기초 종목 정보 수집용 |

---

## 4. 오픈소스/커뮤니티 라이브러리

### 4-1. pykrx

| 항목 | 내용 |
|------|------|
| **서비스명** | pykrx |
| **API 종류** | Python 라이브러리 (KRX/네이버 스크래핑) |
| **주요 기능** | KOSPI/KOSDAQ/KONEX 종목 시세, 지수, ETF, PER/PBR/배당수익률, 공매도, 외국인/기관 수급 데이터 |
| **한국 주식** | 지원 |
| **미국 주식** | 미지원 |
| **무료/유료** | 무료 (오픈소스) |
| **개인 개발자** | 가능 |
| **GitHub** | https://github.com/sharebook-kr/pykrx |
| **Python SDK** | 자체가 Python 라이브러리 (`pip install pykrx`) |
| **특이사항** | 설치 후 API 키 없이 즉시 사용 가능. 실시간 데이터 미지원 (일별 데이터). KRX/네이버 페이지 구조 변경 시 동작 불안정 가능 |

---

### 4-2. FinanceDataReader

| 항목 | 내용 |
|------|------|
| **서비스명** | FinanceDataReader |
| **API 종류** | Python 라이브러리 (다중 소스 통합) |
| **주요 기능** | 한국/미국/글로벌 주가, KOSPI/KOSDAQ/S&P500/NASDAQ/NYSE 종목 리스트, 지수, 환율(USD/KRW 등), 암호화폐(BTC/KRW 등) |
| **한국 주식** | 지원 |
| **미국 주식** | 지원 (Yahoo Finance 활용) |
| **무료/유료** | 무료 (오픈소스) |
| **개인 개발자** | 가능 |
| **GitHub** | https://github.com/FinanceData/FinanceDataReader |
| **공식 문서** | https://financedata.github.io/posts/finance-data-reader-users-guide.html |
| **Python SDK** | 자체가 Python 라이브러리 (`pip install finance-datareader`) |
| **특이사항** | 데이터 소스: Yahoo Finance, FRED, KRX, 네이버 금융. 퀀트 분석에서 가장 많이 쓰이는 데이터 수집 라이브러리 중 하나 |

---

### 4-3. mojito (sharebook-kr)

| 항목 | 내용 |
|------|------|
| **서비스명** | mojito |
| **API 종류** | Python 라이브러리 (증권사 API 통합 래퍼) |
| **주요 기능** | 한국투자증권 KIS API 래퍼 (시세 조회, 매수/매도, 잔고 조회). 암호화폐 거래소(업비트, 바이낸스) 일부 지원 |
| **한국 주식** | 지원 (KIS API 기반) |
| **미국 주식** | 지원 (KIS API 해외주식 기능 활용) |
| **무료/유료** | 무료 (오픈소스) |
| **개인 개발자** | 가능 |
| **GitHub** | https://github.com/sharebook-kr/mojito |
| **Python SDK** | 자체가 Python 라이브러리 (`pip install mojito2`) |
| **특이사항** | "파이썬을 이용한 한국/미국 주식 자동매매 시스템" 책(WikiDocs)과 함께 사용. KIS API를 가장 간단하게 쓸 수 있는 래퍼 |

---

### 4-4. python-kis (Soju06)

| 항목 | 내용 |
|------|------|
| **서비스명** | python-kis (PyKis) |
| **API 종류** | Python 라이브러리 (한국투자증권 REST API 래퍼) |
| **주요 기능** | 시세 조회, 매수/매도 주문, 정정/취소, 잔고 조회, 실시간 WebSocket 연결 |
| **한국 주식** | 지원 |
| **미국 주식** | 지원 |
| **무료/유료** | 무료 (오픈소스) |
| **개인 개발자** | 가능 |
| **GitHub** | https://github.com/Soju06/python-kis |
| **Python SDK** | 자체가 Python 라이브러리 (`pip install python-kis`) |
| **특이사항** | 커뮤니티 기반 강력한 KIS API 래퍼. mojito보다 기능이 풍부하고 타입 힌트 완비. 실시간 주문 체결 지원 |

---

### 4-5. pykis (pjueon)

| 항목 | 내용 |
|------|------|
| **서비스명** | pykis |
| **API 종류** | Python 라이브러리 (한국투자증권 REST API 래퍼) |
| **주요 기능** | 한국투자증권 신규 Open Trade API 래핑. 시세, 주문, 잔고 조회 |
| **한국 주식** | 지원 |
| **미국 주식** | 지원 |
| **무료/유료** | 무료 (오픈소스) |
| **개인 개발자** | 가능 |
| **GitHub** | https://github.com/pjueon/pykis |
| **Python SDK** | 자체가 Python 라이브러리 |
| **특이사항** | python-kis와 별개의 독립 프로젝트. KIS 신규 API 기준으로 구현 |

---

### 4-6. KOAPY (키움증권 래퍼)

| 항목 | 내용 |
|------|------|
| **서비스명** | KOAPY (Korea Open API for Python) |
| **API 종류** | Python 라이브러리 (키움 OpenAPI+ COM 래퍼) |
| **주요 기능** | 키움 OpenAPI+ 전체 기능 래핑. CLI 도구 포함 (종목 리스트, 시세, 실시간 데이터, 저장) |
| **한국 주식** | 지원 |
| **미국 주식** | 미지원 |
| **무료/유료** | 무료 (오픈소스) |
| **개인 개발자** | 가능 (Windows 필수) |
| **GitHub** | https://github.com/elbakramer/koapy |
| **Python SDK** | 자체가 Python 라이브러리 (`pip install koapy`) |
| **특이사항** | PySide2 기본 사용 (PyQt5 전환 가능). gRPC 서버 모드로 비Windows 환경에서 Windows VM을 통해 우회 가능 |

---

### 4-7. kiwoom (breadum)

| 항목 | 내용 |
|------|------|
| **서비스명** | kiwoom |
| **API 종류** | Python 라이브러리 (키움 OpenAPI+ 심플 래퍼) |
| **주요 기능** | 키움 OpenAPI+ 기본 기능 (시세, 주문, 잔고). PyQt5 직접 사용자 대상 |
| **한국 주식** | 지원 |
| **미국 주식** | 미지원 |
| **무료/유료** | 무료 (오픈소스) |
| **개인 개발자** | 가능 (Windows 필수) |
| **GitHub** | https://github.com/breadum/kiwoom |
| **Python SDK** | 자체가 Python 라이브러리 |
| **특이사항** | KOAPY보다 경량. PyQt5 기반 직접 개발자에게 적합 |

---

### 4-8. OpenDartReader

| 항목 | 내용 |
|------|------|
| **서비스명** | OpenDartReader |
| **API 종류** | Python 라이브러리 (DART OpenAPI 래퍼) |
| **주요 기능** | 재무제표 수집, 공시 검색, 사업보고서, 지분 공시, 분기/반기/연간 재무 데이터 pandas DataFrame 반환 |
| **한국 주식** | 지원 (공시/재무 데이터) |
| **미국 주식** | 미지원 |
| **무료/유료** | 무료 (오픈소스) |
| **개인 개발자** | 가능 (DART API Key 필요) |
| **GitHub** | https://github.com/FinanceData/OpenDartReader |
| **Python SDK** | 자체가 Python 라이브러리 (`pip install opendartreader`) |
| **특이사항** | 퀀트 투자 재무 분석의 핵심 도구. 종목코드로 기업 유니크 번호 자동 변환. pandas DataFrame으로 바로 분석 가능 |

---

## 5. 종합 비교표

### 5-1. 증권사 API 비교

| 증권사 | API 방식 | 한국 | 미국 | 무료 | 개인 | 주문 | Linux/Mac |
|--------|---------|:----:|:----:|:----:|:----:|:----:|:--------:|
| 한국투자증권 | REST + WebSocket | O | O | O | O | O | **O** |
| 키움증권 | COM/OCX | O | X | O | O | O | X |
| LS증권 | COM/DLL + REST | O | 일부 | O | O | O | 신규만 |
| 대신증권(크레온) | COM | O | X | O | O | O | X |
| NH투자증권 | DLL/COM | O | 일부 | O | O | O | X |
| 삼성증권 | 오픈API 없음 | - | - | - | X | X | X |
| 미래에셋 | 서비스 종료 | - | - | - | X | X | X |

### 5-2. 데이터 라이브러리 비교

| 라이브러리 | 설치 | 한국 | 미국 | 실시간 | 주문 | API키 필요 |
|-----------|------|:----:|:----:|:------:|:----:|:---------:|
| pykrx | pip | O | X | X | X | X |
| FinanceDataReader | pip | O | O | X | X | X |
| OpenDartReader | pip | O (공시) | X | X | X | O (DART) |
| mojito | pip | O | O | X | O | O (KIS) |
| python-kis | pip | O | O | O | O | O (KIS) |
| pykis | pip | O | O | X | O | O (KIS) |
| KOAPY | pip | O | X | O | O | X (키움계정) |

---

## 6. 추천 조합 (용도별)

### 퀀트 데이터 분석 (주문 없음)
```
pykrx + FinanceDataReader + OpenDartReader
```
- 설치 즉시 사용, API 키 불필요 (DART 제외)
- 시가총액, 재무제표, 주가 히스토리 통합 분석 가능

### 한국/미국 주식 자동매매 (추천)
```
한국투자증권 KIS API + python-kis 또는 mojito
```
- REST API로 Linux/Mac 환경 모두 지원
- 실계좌/모의계좌 모두 지원
- ChatGPT/Claude LLM 연동 자동화 사례 증가 중

### 키움증권 기반 자동매매 (Windows 환경)
```
키움증권 OpenAPI+ + KOAPY
```
- 가장 넓은 커뮤니티와 레퍼런스
- Windows 필수, 32비트 환경 필요

### 대신증권 기반 자동매매 (Windows 환경)
```
CYBOS Plus + Python COM
```
- 문서화 우수, 동기적 요청-응답으로 개발 편의
- 비공식 도움말 (cybosplus.github.io) 활용

---

## 7. 참고 자료

- [위키백과: 대한민국 금융투자회사 수수료 및 API 목록](https://ko.wikipedia.org/wiki/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EA%B8%88%EC%9C%B5%ED%88%AC%EC%9E%90%ED%9A%8C%EC%82%AC_%EC%88%98%EC%88%98%EB%A3%8C_%EB%B0%8F_API_%EB%AA%A9%EB%A1%9D)
- [KIS Developers 공식 포털](https://apiportal.koreainvestment.com/intro)
- [LS증권 Open API 공식 포털](https://openapi.ls-sec.co.kr/intro)
- [KRX Open API](https://openapi.krx.co.kr/)
- [OpenDART](https://opendart.fss.or.kr/intro/main.do)
- [퀀티랩 블로그 - 증권사 API 장단점 비교](https://blog.quantylab.com/htsapi.html)
- [증권사별 Open API 차이 비교](https://mg.jnomy.com/whatis-diff-stock-open-api)
- [파이썬을 이용한 한국/미국 주식 자동매매 시스템 (WikiDocs)](https://wikidocs.net/book/7845)
- [koreainvestment/open-trading-api (GitHub)](https://github.com/koreainvestment/open-trading-api)
- [sharebook-kr/mojito (GitHub)](https://github.com/sharebook-kr/mojito)
- [Soju06/python-kis (GitHub)](https://github.com/Soju06/python-kis)
- [FinanceData/FinanceDataReader (GitHub)](https://github.com/FinanceData/FinanceDataReader)
- [sharebook-kr/pykrx (GitHub)](https://github.com/sharebook-kr/pykrx)
- [FinanceData/OpenDartReader (GitHub)](https://github.com/FinanceData/OpenDartReader)
- [elbakramer/koapy (GitHub)](https://github.com/elbakramer/koapy)
- [CODEF API 개발가이드](https://developer.codef.io/products/stock/overview)
