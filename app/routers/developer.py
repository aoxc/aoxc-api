from fastapi import APIRouter, Request

from app.data import COMPATIBILITY, DEVELOPER_TOOLS, FULL_COMPATIBILITY
from app.schemas import CompatibilityReport, DeveloperTool, FullCompatibilityReport
from app.security import enforce_developer_api_key, enforce_rate_limit

router = APIRouter(prefix="/developer", tags=["developer"])


@router.get("/tools", response_model=list[DeveloperTool])
def list_tools(request: Request) -> list[DeveloperTool]:
    enforce_rate_limit(request)
    enforce_developer_api_key(request)
    return DEVELOPER_TOOLS


@router.get("/compatibility", response_model=CompatibilityReport)
def compatibility(request: Request) -> CompatibilityReport:
    enforce_rate_limit(request)
    enforce_developer_api_key(request)
    return COMPATIBILITY


@router.get("/compatibility/full", response_model=FullCompatibilityReport)
def full_compatibility(request: Request) -> FullCompatibilityReport:
    enforce_rate_limit(request)
    enforce_developer_api_key(request)
    return FULL_COMPATIBILITY
