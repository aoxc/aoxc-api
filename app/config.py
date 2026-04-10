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

    require_request_signature: bool = (
        os.getenv("REQUIRE_REQUEST_SIGNATURE", "false").strip().lower() in _BOOL_TRUE_VALUES
    )
    request_signing_key: str = os.getenv("REQUEST_SIGNING_KEY", "")
    signature_max_skew_seconds: int = int(os.getenv("SIGNATURE_MAX_SKEW_SECONDS", "300"))
    signature_nonce_ttl_seconds: int = int(os.getenv("SIGNATURE_NONCE_TTL_SECONDS", "600"))

    aoxc_rpc_url: str = os.getenv("AOXC_RPC_URL", "")
    aoxc_chain_id: str = os.getenv("AOXC_CHAIN_ID", "aoxc-mainnet")
    aoxc_supported_assets: tuple[str, ...] = tuple(
        asset.strip().upper()
        for asset in os.getenv("AOXC_SUPPORTED_ASSETS", "AOXC").split(",")
        if asset.strip()
    )
    aoxc_max_tx_amount: float = float(os.getenv("AOXC_MAX_TX_AMOUNT", "100000"))
    aoxc_allowed_rpc_methods: tuple[str, ...] = tuple(
        method.strip()
        for method in os.getenv(
            "AOXC_ALLOWED_RPC_METHODS",
            "eth_chainId,eth_blockNumber,eth_getBalance,eth_getTransactionByHash,eth_getTransactionReceipt,eth_call,net_version",
        ).split(",")
        if method.strip()
    )


settings = Settings()
