from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "aoxc-api"
    assert "environment" in data


def test_user_roadmap() -> None:
    response = client.get("/api/v1/user/roadmap")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 4
    assert data[0]["year"] == "2025"


def test_developer_compatibility() -> None:
    response = client.get("/api/v1/developer/compatibility")
    assert response.status_code == 200
    data = response.json()
    assert data["network"] == "AOXChain"
    assert data["compatible"] is True


def test_security_headers_exist() -> None:
    response = client.get("/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
