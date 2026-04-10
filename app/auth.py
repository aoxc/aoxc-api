from __future__ import annotations

import hmac
from dataclasses import dataclass

from fastapi import HTTPException, Request, status

from app.config import settings


@dataclass(frozen=True)
class ApiPrincipal:
    key_id: str
    scopes: frozenset[str]


# Production'da bu map secret manager / DB'den gelmelidir.
API_KEYS: dict[str, tuple[str, frozenset[str]]] = {
    "dev-root": (settings.api_key, frozenset({"developer:read", "developer:write", "user:read"})),
}


def _safe_compare(left: str, right: str) -> bool:
    return hmac.compare_digest(left.encode("utf-8"), right.encode("utf-8"))


def authenticate_api_key(request: Request) -> ApiPrincipal:
    if not settings.require_api_key:
        return ApiPrincipal(key_id="anonymous", scopes=frozenset({"developer:read", "user:read"}))

    key_id = request.headers.get("x-key-id", "")
    provided = request.headers.get("x-api-key", "")

    if not key_id or not provided or key_id not in API_KEYS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid API credentials")

    expected_secret, scopes = API_KEYS[key_id]
    if not _safe_compare(provided, expected_secret):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API credentials")

    return ApiPrincipal(key_id=key_id, scopes=scopes)


def require_scope(principal: ApiPrincipal, required_scope: str) -> None:
    if required_scope not in principal.scopes:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing required scope: {required_scope}")
