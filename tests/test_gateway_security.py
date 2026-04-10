from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_auth_challenge_and_verify_issue_session_token() -> None:
    challenge_response = client.post("/api/v1/auth/challenge", json={"wallet_address": "0xA0XC123"})
    assert challenge_response.status_code == 200
    challenge_data = challenge_response.json()
    assert challenge_data["wallet_address"] == "0xA0XC123"
    assert challenge_data["nonce"]

    verify_response = client.post(
        "/api/v1/auth/verify",
        json={"wallet_address": "0xA0XC123", "signature": "signed_payload"},
    )
    assert verify_response.status_code == 200
    verify_data = verify_response.json()
    assert verify_data["access_token"]
    assert verify_data["token_type"] == "Bearer"


def test_chain_policy_check_requires_session_token() -> None:
    response = client.post(
        "/api/v1/chain/tx/policy-check",
        json={
            "from_address": "0xFROM",
            "to_address": "0xTO",
            "amount": 3.5,
            "asset": "AOXC",
        },
    )
    assert response.status_code == 401


def test_chain_policy_check_accepts_valid_token() -> None:
    client.post("/api/v1/auth/challenge", json={"wallet_address": "0xA0XC777"})
    verify_response = client.post(
        "/api/v1/auth/verify",
        json={"wallet_address": "0xA0XC777", "signature": "ok"},
    )
    token = verify_response.json()["access_token"]

    response = client.post(
        "/api/v1/chain/tx/policy-check",
        json={
            "from_address": "0xA0XC777",
            "to_address": "0xA0XC888",
            "amount": 25.0,
            "asset": "AOXC",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["allowed"] is True
    assert data["risk_level"] in {"low", "medium", "high"}
