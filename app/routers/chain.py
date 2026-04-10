from __future__ import annotations

from fastapi import APIRouter, Header, Request

from app.auth import enforce_session_token
from app.chain_client import rpc_call
from app.config import settings
from app.data import COMPATIBILITY
from app.schemas import (
    ChainStatusResponse,
    RpcProxyRequest,
    RpcProxyResponse,
    TxPolicyCheckRequest,
    TxPolicyCheckResponse,
)
from app.security import enforce_rate_limit, enforce_tx_request_signature

router = APIRouter(prefix="/chain", tags=["chain"])


@router.get("/status", response_model=ChainStatusResponse)
def chain_status(request: Request) -> ChainStatusResponse:
    enforce_rate_limit(request)

    rpc_status = "disconnected"
    if settings.aoxc_rpc_url:
        try:
            _ = rpc_call("eth_chainId", [])
            rpc_status = "connected"
        except Exception:
            rpc_status = "degraded"

    return ChainStatusResponse(
        network=COMPATIBILITY.network,
        chain_id=settings.aoxc_chain_id,
        rpc_status=rpc_status,
        finality_target_blocks=12,
        policy_mode="strict",
    )


@router.post("/rpc", response_model=RpcProxyResponse)
def chain_rpc_proxy(
    payload: RpcProxyRequest,
    request: Request,
    authorization: str | None = Header(default=None),
) -> RpcProxyResponse:
    enforce_rate_limit(request)
    enforce_session_token(authorization)

    result = rpc_call(payload.method, payload.params)
    return RpcProxyResponse(method=payload.method, result=result, chain_id=settings.aoxc_chain_id)


@router.post("/tx/policy-check", response_model=TxPolicyCheckResponse)
def tx_policy_check(
    payload: TxPolicyCheckRequest,
    request: Request,
    authorization: str | None = Header(default=None),
    x_aoxc_timestamp: str | None = Header(default=None),
    x_aoxc_nonce: str | None = Header(default=None),
    x_aoxc_signature: str | None = Header(default=None),
) -> TxPolicyCheckResponse:
    enforce_rate_limit(request)
    session = enforce_session_token(authorization)
    enforce_tx_request_signature(
        from_address=payload.from_address,
        to_address=payload.to_address,
        amount=payload.amount,
        asset=payload.asset,
        timestamp_header=x_aoxc_timestamp,
        nonce_header=x_aoxc_nonce,
        signature_header=x_aoxc_signature,
    )

    reasons: list[str] = []
    controls: list[str] = ["transaction_signing", "nonce_validation", "post-submit_monitoring"]
    risk = "low"
    allowed = True

    if session.wallet_address.lower() != payload.from_address.lower():
        allowed = False
        risk = "high"
        reasons.append("Session wallet and from_address mismatch.")
        controls.append("manual_review")

    asset = payload.asset.upper()
    if asset not in settings.aoxc_supported_assets:
        allowed = False
        risk = "high"
        reasons.append(f"Asset '{asset}' is not supported on this AOXC policy profile.")

    if payload.amount > settings.aoxc_max_tx_amount:
        allowed = False
        risk = "high"
        reasons.append("Transfer amount exceeds policy limit.")

    elif payload.amount > 10_000 and risk != "high":
        risk = "medium"
        reasons.append("High value transfer requires stepped-up verification.")
        controls.append("step_up_auth")

    if payload.to_address.lower() == payload.from_address.lower() and risk != "high":
        risk = "medium"
        reasons.append("Self-transfer pattern flagged for behavioral monitoring.")
        controls.append("behavioral_monitoring")

    return TxPolicyCheckResponse(
        allowed=allowed,
        risk_level=risk,
        reasons=reasons or ["No blocking policy triggered."],
        required_controls=controls,
        policy_version="aoxc-policy-v2",
    )
