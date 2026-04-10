# AOXC API Usage Guide (Experimental)

## 1. Operational Positioning

AOXC API should be evaluated as an experimental integration layer, not a final production security platform.

Recommended usage pattern:

- Start in isolated non-production environments.
- Integrate centralized secret management.
- Add observability, SIEM pipelines, and external WAF/API gateway controls.
- Run security testing (SAST/DAST/dependency scans/penetration tests).

## 2. Environment Configuration

Use `.env.example` as baseline and override with deployment-specific secrets.

Key controls:

- `REQUIRE_API_KEY`: Enforces API key auth for protected resources.
- `REQUIRE_SIGNED_REQUESTS`: Enforces request signatures.
- `REQUEST_SIGNING_SECRET`: Secret key used for HMAC signature verification.
- `REQUEST_MAX_AGE_SECONDS`: Rejects stale signed requests.
- `NONCE_CACHE_TTL_SECONDS`: Nonce replay cache retention period.
- `REQUESTS_PER_MINUTE`: Per-IP rate limiter threshold.

## 3. Signature Protocol

Expected headers:

- `x-sign-ts`: Unix timestamp (seconds)
- `x-sign-nonce`: Unique nonce per request
- `x-signature`: HMAC-SHA256 hex digest over payload

Payload format:

`{METHOD}|{PATH}|{TIMESTAMP}|{NONCE}`

Example payload:

`GET|/api/v1/developer/compatibility|1710000000|f6a8...`

## 4. API Credential Protocol

Expected headers for protected developer endpoints:

- `x-key-id`: key identifier
- `x-api-key`: secret value bound to key id

Authorization path:

1. Validate key id exists.
2. Compare secret using constant-time comparison.
3. Resolve principal scopes.
4. Enforce required scope (e.g., `developer:read`).

## 5. Security Caveats

- HMAC-SHA256 is practical today but not post-quantum resistant.
- In-memory nonce cache is single-instance scoped (not distributed).
- In-memory rate limiting is not globally consistent across replicas.

For production, move these controls to shared infrastructure (Redis, API gateway, service mesh policy).

## 6. Suggested Production Hardening Roadmap

1. Replace static key map with KMS-backed key registry.
2. Replace local nonce cache/rate limiter with Redis.
3. Add mTLS between trusted services.
4. Add formal audit logs and immutable event storage.
5. Add OpenTelemetry traces and security alerting.
6. Integrate key rotation and break-glass controls.
