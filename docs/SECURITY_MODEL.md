# AOXC API Security Model

## 1. Security Scope

This model describes:

- Threat assumptions.
- Control families and expected outcomes.
- Operational runbook minimums.
- Gaps between current code and target-state controls.

---

## 2. Threat Assumptions

1. Adversaries can fully observe public network traffic metadata.
2. Credential theft and token replay attempts are expected.
3. API abuse (automation, scraping, flooding) is continuous.
4. Insider misuse is possible.
5. Third-party dependency compromise is possible.
6. Future cryptanalytic advances may weaken legacy algorithms.

---

## 3. Security Control Families

## 3.1 Identity & Access Controls

- Unique identities for users, services, and workloads.
- Least privilege + separation of duties.
- Short-lived credentials and token audience restrictions.
- Conditional and risk-adaptive authentication.

## 3.2 Request Integrity Controls

- Request signing for sensitive transaction policy endpoints.
- Timestamp skew bounds.
- Nonce uniqueness with TTL.
- Canonical payload serialization.

## 3.3 API Abuse Controls

- Per-client rate limiting and quotas.
- IP reputation and bot/anomaly heuristics.
- Dynamic throttling based on risk score.

## 3.4 Data Protection Controls

- Data classification and handling policies.
- Encryption in transit and at rest.
- Tokenization/redaction for regulated fields.
- Deterministic key rotation and revocation workflow.

## 3.5 Supply Chain Controls

- Dependency governance policy.
- Artifact signing and verification.
- Provenance attestation before deployment.
- Continuous vulnerability triage SLA.

## 3.6 Detection & Response Controls

- Centralized logs and correlation.
- Immutable security event retention.
- Alert tuning and response automation.
- Post-incident corrective action tracking.

---

## 4. Trust Model

### Trust assumptions

- No client input is trusted without validation and policy checks.
- No internal service is trusted without identity proof.
- No critical action is trusted without auditable evidence.

### Trust decisions

Every sensitive request should include:

- Identity signal.
- Device/workload signal.
- Context signal (time, geo, behavior).
- Policy evaluation result.
- Integrity verification result.

---

## 5. Current Baseline vs Target State

| Domain | Current Baseline in Repo | Target State |
|---|---|---|
| Security Headers | Implemented | Hardened per endpoint risk profile |
| API Key Protection | Optional for developer routes | Centralized IAM with scoped tokens |
| Rate Limiting | In-memory per-IP | Distributed, identity-aware global controls |
| Tx Request Signing | HMAC + nonce + skew for policy-check endpoint | Hardware-backed keys and algorithm agility |
| Observability | Minimal app-level logs | Full SIEM + tamper-evident audit plane |
| Supply Chain | Basic project setup | Signed artifacts, SBOM, policy gates |
| Quantum Readiness | Conceptual only | Hybrid PQC rollout with cutover strategy |

---

## 6. Security Operations Minimums

1. **Key management**
   - Secret manager or KMS mandatory in non-dev environments.
   - Rotation intervals defined and tested.
2. **Monitoring**
   - 24/7 alerting for auth failures, replay spikes, rate-limit evasion attempts.
3. **Incident response**
   - Clear severity matrix and on-call runbooks.
   - Tabletop exercises at least quarterly.
4. **Change control**
   - Security-impacting config changes require peer review and audit record.

---

## 7. Chain Transaction Safety Pattern

For chain-bound operations:

1. Authenticate caller.
2. Authorize action against policy.
3. Validate schema + business constraints.
4. Verify request signature and anti-replay controls.
5. Produce immutable audit event.
6. Submit to chain worker queue.
7. Return signed receipt with trace correlation id.

---

## 8. Quantum Transition Guidance

- Maintain crypto inventory.
- Avoid hardcoding cryptographic primitives in business logic.
- Introduce algorithm negotiation and version tags.
- Pilot hybrid verification where protocol permits.
- Define deprecation dates for legacy algorithms.

---

## 9. Acceptance Criteria for “High-Assurance Ready”

The platform can be considered high-assurance ready only when:

- Distributed and identity-aware abuse controls are active.
- Centralized IAM and policy plane enforce least privilege.
- Key lifecycle is externally managed and auditable.
- Immutable evidence logging is operational.
- Supply-chain attestations block untrusted artifacts.
- Incident response SLAs are tested and measurable.
- Crypto-agility framework supports staged PQC migration.

