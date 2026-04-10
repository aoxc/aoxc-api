# AOXC API (Experimental)

AOXC API is an **experimental**, security-focused FastAPI service intended for AOXChain/XChain-compatible integrations.

## Important Notice

This repository is a **pre-production experimental reference implementation**. It is not intended to be used as-is for high-value or regulated production environments without additional controls, external audits, and operational hardening.

- **Do not assume enterprise-grade guarantees** from this codebase alone.
- **Do not rely on this service as a sole security boundary**.
- **Treat all cryptographic and auth configurations as environment-specific responsibilities**.

## Purpose

The project provides:

1. A versioned REST API surface for **user** and **developer** domains.
2. A hardened baseline for API security (signed requests, API keys, scope checks, anti-replay, rate limiting, security headers).
3. A containerized developer experience for reproducible local deployment.
4. An AOXChain-oriented roadmap data contract for prototyping integrations.

## Scope and Non-Goals

### In Scope
- REST endpoints for roadmap, features, sample profiles, developer tools, and compatibility status.
- Request integrity controls (signature validation, timestamp freshness, nonce replay protection).
- API key + scope authorization model.
- Operational defaults through environment-driven settings.

### Explicit Non-Goals
- Formal post-quantum cryptographic assurances.
- Turnkey zero-trust platform implementation.
- Compliance certifications (SOC 2, ISO 27001, PCI DSS, etc.).

## Architecture Overview

- `app/main.py`: application assembly, middleware, routing, health endpoint.
- `app/config.py`: runtime settings and feature toggles via environment variables.
- `app/security.py`: rate limiting, anti-replay, request signature enforcement.
- `app/auth.py`: API key authentication and RBAC-style scope enforcement.
- `app/crypto.py`: signature verification abstraction (currently HMAC-SHA256).
- `app/routers/`: user and developer endpoint modules.
- `app/data.py`: AOXChain-compatible sample payloads and roadmap milestones.

For full architecture and operational guidance, see `docs/USAGE.md`.

## Security Model (Baseline)

- HTTP hardening headers (CSP, HSTS, X-Frame-Options, etc.).
- Signed requests with timestamp and nonce.
- Replay detection via nonce cache.
- API key identity + scope checks.
- Per-IP rate limiting.

## Quick Start

### Local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
make run
```

### Docker

```bash
docker compose up --build
```

## Endpoints

- `GET /health`
- `GET /api/v1/user/roadmap`
- `GET /api/v1/user/features`
- `GET /api/v1/user/profiles` *(requires signed request)*
- `GET /api/v1/developer/tools` *(requires signed request + API credentials + scope)*
- `GET /api/v1/developer/compatibility` *(requires signed request + API credentials + scope)*

## Testing

```bash
make test
```

## License

See `LICENSE`.
