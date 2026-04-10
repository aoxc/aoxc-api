from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(default="ok")
    service: str
    version: str
    environment: str
    experimental: bool


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
