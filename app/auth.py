from __future__ import annotations

import secrets
import time
from dataclasses import dataclass

from fastapi import HTTPException, status

CHALLENGE_TTL_SECONDS = 300
SESSION_TTL_SECONDS = 3600


@dataclass
class WalletChallenge:
    wallet_address: str
    nonce: str
    expires_at: float


@dataclass
class SessionToken:
    wallet_address: str
    token: str
    expires_at: float


_challenges: dict[str, WalletChallenge] = {}
_sessions: dict[str, SessionToken] = {}


def create_wallet_challenge(wallet_address: str) -> WalletChallenge:
    nonce = secrets.token_urlsafe(24)
    challenge = WalletChallenge(
        wallet_address=wallet_address,
        nonce=nonce,
        expires_at=time.time() + CHALLENGE_TTL_SECONDS,
    )
    _challenges[wallet_address] = challenge
    return challenge


def verify_wallet_challenge(wallet_address: str, signature: str) -> SessionToken:
    challenge = _challenges.get(wallet_address)
    if challenge is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active challenge for wallet.")

    if time.time() > challenge.expires_at:
        _challenges.pop(wallet_address, None)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Challenge has expired.")

    # Scaffold behavior: signature parsing/validation will be replaced by chain-native verification.
    if not signature.strip():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature payload.")

    _challenges.pop(wallet_address, None)
    token = secrets.token_urlsafe(32)
    session = SessionToken(
        wallet_address=wallet_address,
        token=token,
        expires_at=time.time() + SESSION_TTL_SECONDS,
    )
    _sessions[token] = session
    return session


def enforce_session_token(authorization: str | None) -> SessionToken:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token.")

    token = authorization.removeprefix("Bearer ").strip()
    session = _sessions.get(token)
    if session is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")

    if time.time() > session.expires_at:
        _sessions.pop(token, None)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")

    return session
