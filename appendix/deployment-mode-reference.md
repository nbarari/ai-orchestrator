# AI Deployment Mode Reference

Declared at Gate 0. Determines which gate criteria are active throughout the SDLC.

---

## Mode Definitions

**Build-Time AI**
AI assists in writing, testing, or documenting the system during development. No LLM executes when the system runs in production.

**Runtime AI**
An LLM executes as part of the live system, processing inputs, generating outputs, or taking actions on behalf of users or other systems.

**Both**
AI is present in both the build process and the live system. All criteria from both modes apply.

---

## Gate Criteria by Mode

| Criterion | Build-Time AI | Runtime AI |
|---|---|---|
| **Phase 1** | | |
| Problem Class Definition | Required | Required |
| Success Predicate | Required | Required |
| AI Deployment Mode declaration | Required | Required |
| **Phase 2** | | |
| Environmental mapping | Required | Required |
| Class Volume Analysis | Required | Required |
| Capability assessment | Required | Required |
| Operational Cost Model | Not applicable | Required |
| LLM provider failure fallback | Not applicable | Required |
| **Phase 3** | | |
| C4 diagrams | Required (High risk) | Required (High risk) |
| Bill of Materials | Required (High risk) | Required (High risk) |
| Class Interface Contract | Required | Required |
| Prompt Contracts | Not applicable | Required (one per LLM call) |
| Data Boundary Declaration | Not applicable | Required |
| Class boundary behavior definition | Required | Required |
| Failure mode registry | Required | Required |
| Human Oversight Model | Not applicable | Required |
| ADRs | Required for major decisions | Required; must include model version rationale, oversight decisions, data boundary decisions |
| Behavioral eval criteria | Required | Required |
| **Phase 4** | | |
| Task-Level Gate | Required | Required |
| Data Boundary check (per task) | Not applicable | Required |
| **Phase 5** | | |
| Contract verification | Required | Required |
| Stress test | Required | Required |
| Behavioral evals | Not applicable | Required |
| Prompt and response log compliance audit | Not applicable | Required |
| **Phase 6** | | |
| Runbooks tested by non-author | Required | Required |
| Kill switch / cost circuit-breaker | Not applicable | Required |
| Privilege scope enforcement at infrastructure level | Not applicable | Required |
| **Phase 7** | | |
| Success Predicate audit | Required | Required |
| Class Drift Audit | Required | Required |
| Model version drift check | Not applicable | Required |
| Living Document Protocol | Required | Required |
| Decommission: credential and key revocation | Not applicable | Required |
| Decommission: prompt/response log retention handling | Not applicable | Required |

---

## Runtime AI: Additional Considerations

### Model Version Pinning

Pin to a specific model version, not a floating alias. Pinning reduces drift but does not prevent it. Providers deprecate model versions on their own schedules, typically with 30 to 90 days notice. The Phase 7 Class Drift Audit should include a check of whether any pinned versions are within the deprecation window.

### Cost Circuit-Breaker

An automated limit that halts LLM calls when spend reaches a defined threshold within a billing period. Must be active before Gate 4 approval. The threshold is set based on the Operational Cost Model from Phase 2.

### Observability Requirement

Every LLM call must produce structured logs of inputs and outputs sufficient to reconstruct a failure without access to the original builder. Logging must comply with the Data Boundary Declaration. Logging what should not be logged is a compliance failure equivalent to not logging what should be.

### Human Oversight Escalation

If a Runtime AI system's blast radius or action reversibility changes after Gate 2 approval, the Human Oversight Model must be revisited before deployment. An autonomous classification that was appropriate at Gate 2 may not be appropriate after a scope change in Phase 4.
