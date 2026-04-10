import hashlib
import hmac
import time
import uuid

from fastapi.testclient import TestClient

from app.config import settings
from app.main import app

client = TestClient(app)


def _signed_headers(path: str, method: str = "GET") -> dict[str, str]:
    ts = int(time.time())
    nonce = uuid.uuid4().hex
    payload = f"{method}|{path}|{ts}|{nonce}"
    signature = hmac.new(
        settings.request_signing_secret.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return {
        "x-sign-ts": str(ts),
        "x-sign-nonce": nonce,
        "x-signature": signature,
        "x-key-id": "dev-root",
        "x-api-key": settings.api_key,
    }


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "aoxc-api"
    assert "environment" in data
    assert data["experimental"] is True


def test_user_roadmap() -> None:
    response = client.get("/api/v1/user/roadmap")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 4
    assert data[0]["year"] == "2025"


def test_developer_compatibility() -> None:
    response = client.get("/api/v1/developer/compatibility", headers=_signed_headers("/api/v1/developer/compatibility"))
    assert response.status_code == 200
    data = response.json()
    assert data["network"] == "AOXChain"
    assert data["compatible"] is True


def test_security_headers_exist() -> None:
    response = client.get("/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["x-experimental-mode"] in {"true", "false"}


def test_profiles_require_signature() -> None:
    response = client.get("/api/v1/user/profiles")
    assert response.status_code == 401
