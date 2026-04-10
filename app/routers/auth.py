from __future__ import annotations

from fastapi import APIRouter

from app.auth import CHALLENGE_TTL_SECONDS, SESSION_TTL_SECONDS, create_wallet_challenge, verify_wallet_challenge
from app.schemas import (
    SessionTokenResponse,
    WalletChallengeRequest,
    WalletChallengeResponse,
    WalletVerifyRequest,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/challenge", response_model=WalletChallengeResponse)
def create_challenge(payload: WalletChallengeRequest) -> WalletChallengeResponse:
    challenge = create_wallet_challenge(payload.wallet_address)
    message = (
        "AOXC login challenge\n"
        f"wallet={challenge.wallet_address}\n"
        f"nonce={challenge.nonce}\n"
        "purpose=Sign to authenticate with AOXC API gateway"
    )
    return WalletChallengeResponse(
        wallet_address=challenge.wallet_address,
        nonce=challenge.nonce,
        message=message,
        expires_in_seconds=CHALLENGE_TTL_SECONDS,
    )


@router.post("/verify", response_model=SessionTokenResponse)
def verify_challenge(payload: WalletVerifyRequest) -> SessionTokenResponse:
    session = verify_wallet_challenge(payload.wallet_address, payload.signature)
    return SessionTokenResponse(
        access_token=session.token,
        expires_in_seconds=SESSION_TTL_SECONDS,
        wallet_address=session.wallet_address,
    )
