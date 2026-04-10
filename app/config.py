from __future__ import annotations

import os
from dataclasses import dataclass


def _env_bool(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "AOXC API")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    app_env: str = os.getenv("APP_ENV", "dev")
    allowed_origins: tuple[str, ...] = tuple(
        origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",") if origin.strip()
    )

    # API security
    require_api_key: bool = _env_bool("REQUIRE_API_KEY", "true")
    api_key: str = os.getenv("API_KEY", "local-dev-key")
    requests_per_minute: int = int(os.getenv("REQUESTS_PER_MINUTE", "120"))

    # Signed request security (anti-replay + integrity)
    require_signed_requests: bool = _env_bool("REQUIRE_SIGNED_REQUESTS", "true")
    request_signing_secret: str = os.getenv("REQUEST_SIGNING_SECRET", "local-signing-secret")
    request_max_age_seconds: int = int(os.getenv("REQUEST_MAX_AGE_SECONDS", "120"))
    nonce_cache_ttl_seconds: int = int(os.getenv("NONCE_CACHE_TTL_SECONDS", "300"))


settings = Settings()
