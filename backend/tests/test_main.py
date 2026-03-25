from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestHealthCheck:
    def test_health_returns_ok(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data
        assert "environment" in data

    def test_root_returns_message(self, client: TestClient) -> None:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data


class TestAPIRoutes:
    def test_docs_accessible(self, client: TestClient) -> None:
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_schema(self, client: TestClient) -> None:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "paths" in schema
        assert "/api/v1/stocks/{symbol}/price" in schema["paths"]
        assert "/api/v1/analysis/{symbol}/value" in schema["paths"]
        assert "/api/v1/portfolio/" in schema["paths"]

    def test_portfolio_get_empty(self, client: TestClient) -> None:
        response = client.get("/api/v1/portfolio/")
        assert response.status_code == 200
        data = response.json()
        assert data["total_invested"] == 0.0
        assert data["items"] == []

    def test_portfolio_add_item(self, client: TestClient) -> None:
        payload = {"symbol": "005930", "quantity": 10, "avg_cost": 62000.0}
        response = client.post("/api/v1/portfolio/", json=payload)
        assert response.status_code == 201
        assert "추가 완료" in response.json()["message"]

    def test_portfolio_remove_nonexistent(self, client: TestClient) -> None:
        response = client.delete("/api/v1/portfolio/INVALID")
        assert response.status_code == 404

    def test_stock_search_empty(self, client: TestClient) -> None:
        response = client.get("/api/v1/stocks/search", params={"q": "삼성"})
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_market_news_summary(self, client: TestClient) -> None:
        response = client.get("/api/v1/news/market/summary", params={"market": "KR"})
        assert response.status_code == 200
        data = response.json()
        assert "market" in data
