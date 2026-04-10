from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.middleware import RequestContextMiddleware, SecurityHeadersMiddleware
from app.routers import developer, user
from app.schemas import HealthResponse

is_prod = settings.app_env.lower() == "prod"

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AOXChain uyumlu kullanici ve gelistirici API servisi",
    docs_url=None if is_prod else "/docs",
    redoc_url=None if is_prod else "/redoc",
)

app.add_middleware(RequestContextMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api/v1")
app.include_router(developer.router, prefix="/api/v1")


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(
        service="aoxc-api",
        version=app.version,
        environment=settings.app_env,
    )
