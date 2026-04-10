from __future__ import annotations

from fastapi import APIRouter, Header, Request

from app.auth import enforce_session_token
from app.data import COMPATIBILITY
from app.schemas import ChainStatusResponse, TxPolicyCheckRequest, TxPolicyCheckResponse
from app.security import enforce_rate_limit

router = APIRouter(prefix="/chain", tags=["chain"])


@router.get("/status", response_model=ChainStatusResponse)
def chain_status(request: Request) -> ChainStatusResponse:
    enforce_rate_limit(request)
    return ChainStatusResponse(
        network=COMPATIBILITY.network,
        rpc_status="connected",
        finality_target_blocks=12,
        policy_mode="strict",
    )


@router.post("/tx/policy-check", response_model=TxPolicyCheckResponse)
def tx_policy_check(
    payload: TxPolicyCheckRequest,
    request: Request,
    authorization: str | None = Header(default=None),
) -> TxPolicyCheckResponse:
    enforce_rate_limit(request)
    enforce_session_token(authorization)

    reasons: list[str] = []
    controls: list[str] = ["transaction_signing", "nonce_validation", "post-submit_monitoring"]
    risk = "low"

    if payload.amount > 10_000:
        risk = "medium"
        reasons.append("High value transfer requires stepped-up verification.")
        controls.append("step_up_auth")

    if payload.to_address.lower() == payload.from_address.lower():
        risk = "high"
        reasons.append("Self-transfer pattern flagged for review.")
        controls.append("manual_review")

    return TxPolicyCheckResponse(
        allowed=risk != "high",
        risk_level=risk,
        reasons=reasons or ["No blocking policy triggered."],
        required_controls=controls,
    )
