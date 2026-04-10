from fastapi import APIRouter, Request

from app.data import FEATURE_FLAGS, ROADMAP, SAMPLE_USERS
from app.schemas import FeatureFlag, RoadmapMilestone, UserProfile
from app.security import enforce_rate_limit

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/roadmap", response_model=list[RoadmapMilestone])
def get_roadmap(request: Request) -> list[RoadmapMilestone]:
    enforce_rate_limit(request)
    return ROADMAP


@router.get("/profiles", response_model=list[UserProfile])
def list_profiles(request: Request) -> list[UserProfile]:
    enforce_rate_limit(request)
    return SAMPLE_USERS


@router.get("/features", response_model=list[FeatureFlag])
def list_feature_flags(request: Request) -> list[FeatureFlag]:
    enforce_rate_limit(request)
    return FEATURE_FLAGS
