# ADR-001: Claude Sonnet model for document classification

**Status:** Accepted
**Date of decision:** 2026-04-04
**SDLC phase:** Design (model selection for Runtime AI)
**Author:** ai-orchestrator-framework contributors (worked example)

---

## Context

The project needs a pinned Anthropic model identifier for **LLM-based document classification** (mapping document content to categories or labels via an API call), so that implementations, Prompt Contracts, and audits refer to a single version rather than a floating alias.

The worked example’s Problem Class, Success Predicate, and design artifacts live under `examples/document-classification-agent/` (not `docs/`). **Gate 2** and the **Data Boundary Declaration** are recorded in `examples/document-classification-agent/gate-2.md` and reflected in `examples/document-classification-agent/contracts/`.

---

## Decision

The project selects **`claude-sonnet-4-6`** as the pinned model for document classification performed via the Anthropic API.

All Prompt Contracts, logging configuration, and drift reviews for that workload must name this model version explicitly.

---

## Alternatives Considered

- **Smaller / cheaper Anthropic or other-provider models:** Not formally benchmarked for this worked example; could reduce cost at the risk of instruction-following or structured-output quality. Revisit when cost or latency constraints dominate.
- **Larger / more capable models:** Higher cost and latency; reserved for future ADR if evals show insufficient accuracy on the pinned taxonomy.

*(For a production decision, list models actually evaluated and metrics.)*

---

## Consequences

**Easier:**

- A single stable identifier for contracts, tests, and operational runbooks.
- Clear trigger for re-validation when Anthropic deprecates or replaces this build.

**Harder:**

- Operational and cost characteristics are fixed to this version until the ADR is superseded.
- Classification quality and latency must be validated empirically against project requirements; pinning does not remove the need for evaluation.

---

## Review Trigger

Revisit this ADR when any of the following occurs:

- Anthropic deprecates, retires, or materially changes **`claude-sonnet-4-6`**.
- Document classification gains new categories, new data types in the prompt, or a new oversight level.
- The Data Boundary Declaration is updated in a way that affects what may be sent to the model (see `examples/document-classification-agent/gate-2.md`).

---

## Runtime AI Fields

**Model version rationale:**

Use a **Sonnet**-class model where classification requires reliable instruction following and structured outputs, with cost and latency between smaller and larger tiers. Confirm against benchmarks and SLOs in implementation; pinning does not replace measurement.

**Human oversight level for affected actions:**

**Supervised** for **initial deployment** for committing high–blast-radius downstream routes: classification proposals may be stored for audit, but irreversible workflow commits require human or approved release per `examples/document-classification-agent/gate-2.md` Human Oversight Model. Retries and validation-only paths remain bounded and autonomous as documented there.

**Data boundary decision:**

Document text, taxonomy label definitions, and minimal tenant/document identifiers may cross into the LLM **only as described** in the Data Boundary Declaration in **`examples/document-classification-agent/gate-2.md`** and field-level confirmation in **`examples/document-classification-agent/contracts/prompt-contract-classification.md`**.

Filenames and similar PII-adjacent metadata are **omitted from the default prompt** unless governance explicitly permits. Logging must follow the same declaration (structured outputs logged; raw document text logged only when policy allows).

**Pinning expiry plan:**

- When **`claude-sonnet-4-6`** is deprecated or superseded, open a new ADR or supersede this one with a new pinned version.
- Re-run Prompt Contract validation and, per project process, include the change in the Phase 7 Class Drift Audit.
- Maintain a fallback path for provider unavailability, rate limits, and invalid model output (per Runtime AI requirements); unhandled exceptions are not an acceptable failure mode.

---

## Record completeness

| Item | State |
|------|--------|
| Decision maker / approver | Worked example — use **named individual** in production (see `examples/notes.md`) |
| Alternatives actually evaluated | Partial — illustrative options only; production should record benchmarks |
| Model rationale (vs. named alternatives) | Documented at Sonnet-class intent; empirical comparison pending |
| Human oversight level for classification | **Supervised** for initial deployment (see Gate 2) |
| Data boundary (gate-2) | **Documented** in `examples/document-classification-agent/gate-2.md` and contracts |
