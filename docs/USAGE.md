# AOXC API Enterprise Usage Guide

## ⚠️ Experimental Program Status

AOXC API is in an active build phase and should be categorized as an **experimental integration platform**.

Do not onboard this service into high-risk production domains (regulated financial workflows, critical infrastructure controls, or irreversible transaction automation) until hardening controls are complete.

For target architecture and control model details:

- `docs/ARCHITECTURE.md`
- `docs/SECURITY_MODEL.md`

---

## 1. Operating Model

Use AOXC API as a controlled gateway layer between AOXChain-aligned services and client applications.

Recommended lifecycle:

1. Validate in isolated development and staging environments.
2. Add identity, policy, and secrets controls using enterprise infrastructure.
3. Introduce complete telemetry and security monitoring.
4. Complete architecture, threat, and penetration reviews before production authorization.

---

## 2. Environment Configuration Baseline

Use environment variables as the single source of runtime behavior.

| Variable | Purpose | Recommended Enterprise Practice |
|---|---|---|
| `APP_ENV` | Environment label (`dev`, `staging`, `prod`) | Bind to deployment profile and change control workflows |
| `ALLOWED_ORIGINS` | CORS allow-list | Restrict to approved domains only |
| `REQUIRE_API_KEY` | Enables API key auth on developer endpoints | Set `true` outside local-only development |
| `API_KEY` | Shared key for protected developer routes | Store in secret manager; rotate periodically |
| `REQUESTS_PER_MINUTE` | In-memory per-IP throttling threshold | Temporary control only; replace with distributed limiter |
| `ENFORCE_HTTPS` | Enables Strict-Transport-Security header | Keep `true` where TLS termination is correctly configured |
| `REQUIRE_REQUEST_SIGNATURE` | Enforces signed tx policy-check requests | Set `true` in staging/prod for anti-tamper + anti-replay |
| `REQUEST_SIGNING_KEY` | Shared HMAC key for tx request signatures | Store in KMS/secret manager and rotate |
| `SIGNATURE_MAX_SKEW_SECONDS` | Max tolerated client/server clock drift | Keep low (e.g., 120-300s) and monitor rejects |
| `SIGNATURE_NONCE_TTL_SECONDS` | Replay cache lifetime for used nonces | Tune to request latency + retry window |

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

If `REQUIRE_REQUEST_SIGNATURE=true`, also send:

- `X-AOXC-Timestamp: <unix-seconds>`
- `X-AOXC-Nonce: <unique-nonce>`
- `X-AOXC-Signature: <hmac-sha256>` over canonical value:
  `from_address|to_address|amount(8dp)|asset|timestamp|nonce`

---

## 4. Deployment Recommendations

### Minimum staging profile

- Enable `REQUIRE_API_KEY=true`.
- Enable `REQUIRE_REQUEST_SIGNATURE=true`.
- Use secret manager-backed `API_KEY` and `REQUEST_SIGNING_KEY`.
- Route all logs to centralized monitoring.

### Minimum production profile

- Keep all staging controls enabled.
- Replace in-memory limiter with distributed limiter.
- Enable immutable security event retention.
- Use centrally managed identity and policy systems.
- Enforce change-control for security settings.

---

## 5. Validation and Operational Checks

Recommended checks before each release:

1. Endpoint and auth regression tests pass.
2. Signature verification checks pass with valid/invalid test vectors.
3. Rate-limiting behavior matches expected thresholds.
4. Secret rotation rehearsal completed in non-production.
5. Rollback runbook tested for latest deployment artifacts.

---

## 6. Quantum-Transition Positioning

Current runtime controls are not post-quantum complete. Treat the service as **quantum-transition preparatory**.

To progress:

1. Build cryptographic inventory.
2. Add cryptographic abstraction and algorithm policy config.
3. Pilot hybrid classical + PQC modes where integration allows.
4. Add staged cutover and rollback plans.

---

## 7. Production Hardening Roadmap

1. Replace local in-memory controls with shared infrastructure (e.g., Redis + gateway policy engine).
2. Externalize authentication/authorization via centralized identity platform.
3. Add OpenTelemetry traces + immutable security audit logs.
4. Enforce key rotation, revocation, and incident break-glass procedures.
5. Add CI/CD quality gates: SAST, DAST, dependency, container, and IaC scanning.
6. Implement formal release governance with pre-approved rollback playbooks.

---

## 8. Validation Commands

```bash
make test
```

```bash
docker compose up --build
```

