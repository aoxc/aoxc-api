from fastapi import APIRouter, Request

from app.auth import authenticate_api_key, require_scope
from app.data import COMPATIBILITY, DEVELOPER_TOOLS
from app.schemas import CompatibilityReport, DeveloperTool
from app.security import enforce_rate_limit, enforce_signed_request

router = APIRouter(prefix="/developer", tags=["developer"])


@router.get("/tools", response_model=list[DeveloperTool])
def list_tools(request: Request) -> list[DeveloperTool]:
    enforce_rate_limit(request)
    enforce_signed_request(request)
    principal = authenticate_api_key(request)
    require_scope(principal, "developer:read")
    return DEVELOPER_TOOLS


@router.get("/compatibility", response_model=CompatibilityReport)
def compatibility(request: Request) -> CompatibilityReport:
    enforce_rate_limit(request)
    enforce_signed_request(request)
    principal = authenticate_api_key(request)
    require_scope(principal, "developer:read")
    return COMPATIBILITY
