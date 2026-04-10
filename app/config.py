from __future__ import annotations

import os
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class Settings:
    _BOOL_TRUE_VALUES: ClassVar[set[str]] = {"1", "true", "yes", "on"}

    app_name: str = os.getenv("APP_NAME", "AOXC API")
    app_version: str = os.getenv("APP_VERSION", "0.2.0")
    app_env: str = os.getenv("APP_ENV", "dev")
    allowed_origins: tuple[str, ...] = tuple(
        origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",") if origin.strip()
    )
    require_api_key: bool = os.getenv("REQUIRE_API_KEY", "false").strip().lower() in _BOOL_TRUE_VALUES
    api_key: str = os.getenv("API_KEY", "")
    requests_per_minute: int = int(os.getenv("REQUESTS_PER_MINUTE", "120"))
    enforce_https: bool = os.getenv("ENFORCE_HTTPS", "true").strip().lower() in _BOOL_TRUE_VALUES


settings = Settings()
