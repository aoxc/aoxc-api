from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(default="ok")
    service: str
    version: str
    environment: str
    warning: str = Field(default="Experimental build: not production-ready.")


class UserProfile(BaseModel):
    wallet_address: str
    reputation_score: float = Field(ge=0)
    country: str
    joined_year: int


class RoadmapMilestone(BaseModel):
    year: str
    focus: str
    targets: list[str]


class FeatureFlag(BaseModel):
    key: str
    enabled: bool
    rollout_stage: str
    description: str


class DeveloperTool(BaseModel):
    name: str
    status: str
    description: str


class CompatibilityReport(BaseModel):
    network: str
    compatible: bool
    supported_standards: list[str]
    notes: str


class CompatibilityCapability(BaseModel):
    key: str
    status: str
    description: str


class CompatibilityRuntime(BaseModel):
    api_version: str
    compatibility_version: str
    chain_id: str
    rpc_transport: str
    signature_modes: list[str]


class FullCompatibilityReport(BaseModel):
    network: str
    compatible: bool
    runtime: CompatibilityRuntime
    standards: list[str]
    capabilities: list[CompatibilityCapability]
    required_headers: list[str]
    sample_rpc_methods: list[str]
    notes: str


ADDRESS_PATTERN = r"^0x[a-fA-F0-9]{4,128}$"


class WalletChallengeRequest(BaseModel):
    wallet_address: str = Field(min_length=6, max_length=130, pattern=ADDRESS_PATTERN)


class WalletChallengeResponse(BaseModel):
    wallet_address: str
    nonce: str
    message: str
    expires_in_seconds: int


class WalletVerifyRequest(BaseModel):
    wallet_address: str = Field(min_length=6, max_length=130, pattern=ADDRESS_PATTERN)
    signature: str = Field(min_length=1)


class SessionTokenResponse(BaseModel):
    access_token: str
    token_type: str = Field(default="Bearer")
    expires_in_seconds: int
    wallet_address: str


class ChainStatusResponse(BaseModel):
    network: str
    chain_id: str
    rpc_status: str
    finality_target_blocks: int
    policy_mode: str


class TxPolicyCheckRequest(BaseModel):
    from_address: str = Field(min_length=6, max_length=130, pattern=ADDRESS_PATTERN)
    to_address: str = Field(min_length=6, max_length=130, pattern=ADDRESS_PATTERN)
    amount: float = Field(gt=0)
    asset: str = Field(default="AOXC")


class TxPolicyCheckResponse(BaseModel):
    allowed: bool
    risk_level: str
    reasons: list[str]
    required_controls: list[str]
    policy_version: str


class RpcProxyRequest(BaseModel):
    method: str = Field(min_length=3, max_length=128)
    params: list[Any] = Field(default_factory=list)


class RpcProxyResponse(BaseModel):
    method: str
    result: Any
    chain_id: str
