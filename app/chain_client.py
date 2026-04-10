from __future__ import annotations

from typing import Any
import json
import urllib.error
import urllib.request

from fastapi import HTTPException, status

from app.config import settings


def _ensure_rpc_configured() -> None:
    if not settings.aoxc_rpc_url:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AOXC RPC URL is not configured.",
        )


def rpc_call(method: str, params: list[Any] | None = None, request_id: int = 1) -> Any:
    _ensure_rpc_configured()

    if method not in settings.aoxc_allowed_rpc_methods:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"RPC method '{method}' is not allowed by policy.",
        )

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or [],
        "id": request_id,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        settings.aoxc_rpc_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AOXC RPC upstream returned HTTP {exc.code}.",
        ) from exc
    except urllib.error.URLError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AOXC RPC upstream is unreachable.",
        ) from exc

    decoded = json.loads(body)
    if "error" in decoded:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AOXC RPC error: {decoded['error']}",
        )

    return decoded.get("result")
