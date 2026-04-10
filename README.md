# AOXC API

A FastAPI-based integration service designed for AOXChain ecosystem clients and developer tooling.

> ⚠️ **Experimental Build Notice**  
> This project is currently under active construction and should be treated as **experimental software**. Do not classify this codebase as production-grade without completing the hardening, validation, and governance controls listed in the documentation.

## 1) Product Scope

AOXC API provides two access surfaces:

- **User APIs** for roadmap visibility and ecosystem-facing data consumption.
- **Developer APIs** for compatibility and toolchain metadata (optionally protected via API key).

The service is intentionally lightweight and intended to be a foundation layer for enterprise deployments.

## 2) Core Capabilities

- FastAPI application lifecycle with OpenAPI schema generation.
- Structured response contracts through Pydantic models.
- Basic HTTP security header middleware (including optional HSTS).
- In-memory per-IP rate limiting.
- Optional API key protection for developer endpoints.
- Wallet challenge/verify authentication scaffold for application sessions.
- Transaction policy-check endpoint scaffold for chain-operation guardrails.
- Docker-based reproducible runtime.

## 3) Architecture Map

- `app/main.py` — FastAPI initialization, middleware registration, router composition.
- `app/config.py` — runtime configuration contract sourced from environment variables.
- `app/middleware.py` — baseline transport-level security headers + experimental status header.
- `app/security.py` — request throttling and developer endpoint API key checks.
- `app/routers/user.py` — user-facing endpoints.
- `app/routers/developer.py` — developer-facing endpoints.
- `app/data.py` — static AOXChain roadmap and sample payload data.
- `docs/USAGE.md` — enterprise usage and operational controls.

## 4) Quick Start

### Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
make run
```

### Docker (recommended)

```bash
docker compose up --build
```

## 5) API Endpoints

- `GET /health`
- `GET /api/v1/user/roadmap`
- `GET /api/v1/user/features`
- `GET /api/v1/user/profiles`
- `GET /api/v1/developer/tools`
- `GET /api/v1/developer/compatibility`
- `POST /api/v1/auth/challenge`
- `POST /api/v1/auth/verify`
- `GET /api/v1/chain/status`
- `POST /api/v1/chain/tx/policy-check`

## 6) Configuration

Use environment variables for deployment configuration:

- `APP_NAME`
- `APP_VERSION`
- `APP_ENV`
- `ALLOWED_ORIGINS`
- `REQUIRE_API_KEY`
- `API_KEY`
- `REQUESTS_PER_MINUTE`
- `ENFORCE_HTTPS`

## 7) Experimental & Quantum Security Warning

This implementation does **not** provide post-quantum cryptographic guarantees. While AOXChain strategy may evolve toward quantum-resilient controls, this repository currently includes only conventional transport and access controls.

Before enterprise launch, establish:

1. Centralized key and secret lifecycle management.
2. Distributed replay/rate-control infrastructure.
3. Cryptographic agility roadmap including post-quantum migration planning.
4. Full observability, auditability, and incident response operations.

## 8) Validation

```bash
make test
```

## 9) License

This project is distributed under the MIT License (`LICENSE`).
