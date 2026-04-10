# AOXC API Enterprise Usage Guide

## ⚠️ Experimental Program Status

AOXC API is currently in an active build phase and should be categorized as an **experimental integration platform**.

Do not onboard this service into high-risk production domains (regulated financial workflows, critical infrastructure controls, or irreversible transaction automation) until all production hardening controls are complete.

---

## 1. Operating Model

Use AOXC API as a controlled gateway layer between AOXChain-aligned services and client applications.

Recommended lifecycle:

1. Validate in isolated development and staging environments.
2. Add identity, policy, and secrets controls using enterprise infrastructure.
3. Introduce complete telemetry and security monitoring.
4. Complete architecture and penetration reviews before production authorization.

---

## 2. Environment Configuration Baseline

Use environment variables as the single source of runtime behavior.

| Variable | Purpose | Recommended Enterprise Practice |
|---|---|---|
| `APP_ENV` | Environment label (`dev`, `staging`, `prod`) | Bind to deployment profile and change control workflows |
| `ALLOWED_ORIGINS` | CORS allow-list | Restrict to approved domains only |
| `REQUIRE_API_KEY` | Enables API key auth on developer endpoints | Set `true` outside local-only development |
| `API_KEY` | Shared key for protected developer routes | Store in secret manager; rotate periodically |
| `REQUESTS_PER_MINUTE` | In-memory per-IP throttling threshold | Treat as temporary control; replace with distributed limiter |
| `ENFORCE_HTTPS` | Enables Strict-Transport-Security header | Keep `true` in environments served over TLS |

---

## 3. Endpoint Access Surfaces

### Public system surface

- `GET /health`

### User surface

- `GET /api/v1/user/roadmap`
- `GET /api/v1/user/features`
- `GET /api/v1/user/profiles`

### Developer surface

- `GET /api/v1/developer/tools`
- `GET /api/v1/developer/compatibility`

### Auth & chain security scaffold

- `POST /api/v1/auth/challenge`
- `POST /api/v1/auth/verify`
- `GET /api/v1/chain/status`
- `POST /api/v1/chain/tx/policy-check`

When `REQUIRE_API_KEY=true`, developer routes require:

- `x-api-key: <configured-secret>`

When submitting transaction policy checks, send:

- `Authorization: Bearer <session-token>`

---

## 4. Security Control Summary

Current controls:

- Security response headers (CSP, frame protection, content-type protections).
- In-memory rate limiting by client IP.
- Optional API key enforcement for developer endpoints.
- Explicit experimental warning response header (`X-AOXC-Status: experimental`).

Current limitations:

- Local process memory is used for throttling state.
- Not horizontally consistent across replicas.
- No built-in KMS-backed secret lifecycle.
- No post-quantum cryptographic implementation.

---

## 5. Quantum-Readiness Statement

AOXC API currently uses conventional web/API security controls and should be considered **quantum-transition unready**.

To align with quantum-resilient strategy, plan these tracks:

1. Cryptographic inventory and algorithm agility framework.
2. Controlled migration design for post-quantum signatures/KEMs.
3. Hybrid mode validation during transition periods.
4. Governance sign-off based on formal security assurance.

---

## 6. Production Hardening Roadmap

1. Replace in-memory controls with shared infrastructure (Redis, gateway policy engine).
2. Externalize authentication and authorization via centralized identity platform.
3. Add OpenTelemetry traces + immutable security audit logs.
4. Enforce key rotation, revocation, and incident break-glass procedures.
5. Add CI/CD quality gates: SAST, DAST, dependency, container, and IaC scanning.
6. Implement formal release governance with rollback playbooks.

---

## 7. Validation Commands

```bash
make test
```

```bash
docker compose up --build
```
