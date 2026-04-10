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
    assert data["warning"] == "Experimental build: not production-ready."


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


def test_developer_full_compatibility() -> None:
    response = client.get("/api/v1/developer/compatibility/full")
    assert response.status_code == 200
    data = response.json()
    assert data["network"] == "AOXChain"
    assert data["runtime"]["chain_id"] == "aoxc-1"
    assert "eth_chainId" in data["sample_rpc_methods"]
    assert len(data["capabilities"]) >= 4


def test_security_headers_exist() -> None:
    response = client.get("/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["x-aoxc-status"] == "experimental"


def test_cors_preflight_supports_post_routes() -> None:
    response = client.options(
        "/api/v1/auth/challenge",
        headers={
            "Origin": "http://localhost",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.status_code == 200
    assert "POST" in response.headers.get("access-control-allow-methods", "")


def test_hsts_header_present_by_default() -> None:
    response = client.get("/health")
    assert "strict-transport-security" in response.headers
