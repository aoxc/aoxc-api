# AOXC API

A FastAPI-based integration and security gateway service designed for AOXChain ecosystem clients and developer tooling.

> ⚠️ **Experimental Build Notice**
> This project is currently under active construction and should be treated as **experimental software**. Do not classify this codebase as production-grade without completing the hardening, validation, and governance controls listed in the documentation.

## 1) Product Scope

AOXC API provides two access surfaces:

- **User APIs** for roadmap visibility and ecosystem-facing data consumption.
- **Developer APIs** for compatibility and toolchain metadata (optionally protected via API key).

This service is intentionally lightweight and intended to be a composable foundation for enterprise deployments that need layered API security and policy enforcement.

## 2) Core Capabilities (Current Implementation)

- FastAPI application lifecycle with OpenAPI schema generation.
- Structured response contracts through Pydantic models.
- Basic HTTP security header middleware (including optional HSTS).
- In-memory per-IP rate limiting.
- Optional API key protection for developer endpoints.
- Wallet challenge/verify authentication scaffold for application sessions.
- Transaction policy-check endpoint scaffold for chain-operation guardrails.
- Docker-based reproducible runtime.

## 3) Architecture & Security Documentation

For full architecture, threat model, and roadmap, see:

- `docs/ARCHITECTURE.md` — target-state layered security architecture (Q-Zero Mesh).
- `docs/SECURITY_MODEL.md` — control matrix, trust boundaries, and security operations model.
- `docs/USAGE.md` — operational deployment and runtime guidance.

## 4) Current Code Map

- `app/main.py` — FastAPI initialization, middleware registration, router composition.
- `app/config.py` — runtime configuration contract sourced from environment variables.
- `app/middleware.py` — baseline transport-level security headers + experimental status header.
- `app/security.py` — request throttling and developer endpoint API key checks.
- `app/routers/user.py` — user-facing endpoints.
- `app/routers/developer.py` — developer-facing endpoints.
- `app/data.py` — static AOXChain roadmap and sample payload data.

## 5) Quick Start

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

## 6) API Endpoints

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
- `POST /api/v1/chain/rpc`

## 7) Configuration

Use environment variables for deployment configuration:

- `APP_NAME`
- `APP_VERSION`
- `APP_ENV`
- `ALLOWED_ORIGINS`
- `REQUIRE_API_KEY`
- `API_KEY`
- `REQUESTS_PER_MINUTE`
- `ENFORCE_HTTPS`
- `REQUIRE_REQUEST_SIGNATURE`
- `REQUEST_SIGNING_KEY`
- `SIGNATURE_MAX_SKEW_SECONDS`
- `SIGNATURE_NONCE_TTL_SECONDS`

For signed transaction policy requests (`REQUIRE_REQUEST_SIGNATURE=true`), clients must include:

- `X-AOXC-Timestamp`: Unix epoch seconds
- `X-AOXC-Nonce`: unique request nonce
- `X-AOXC-Signature`: HMAC-SHA256 over
  `from_address|to_address|amount(8dp)|asset|timestamp|nonce`

## 8) Important Security Positioning

- The current implementation is **not post-quantum secure**.
- The target model is **post-quantum transition ready** via cryptographic agility and hybrid modes.
- Current controls are useful as a baseline, but not sufficient alone for high-assurance production.

See `docs/ARCHITECTURE.md` and `docs/SECURITY_MODEL.md` for the complete migration and control strategy.

## 9) Validation

```bash
make test
```

## 10) License

This project is distributed under the MIT License (`LICENSE`).
