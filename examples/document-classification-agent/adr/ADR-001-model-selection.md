# ADR-001: Claude Sonnet model for document classification

**Status:** Proposed
**Date of decision:** 2026-04-04
**SDLC phase:** Design (model selection for Runtime AI)
**Author:** *(incomplete — assign owner)*

---

## Context

The project needs a pinned Anthropic model identifier for **LLM-based document classification** (mapping document content to categories or labels via an API call), so that implementations, Prompt Contracts, and audits refer to a single version rather than a floating alias.

At the time this ADR was recorded, `docs/gate-0.md` and `docs/gate-2.md` were not present in the repository. The Problem Class, Success Predicate, and Data Boundary Declaration should be aligned with this choice before any production Runtime AI path is activated.

---

## Decision

The project selects **`claude-sonnet-4-6`** as the pinned model for document classification performed via the Anthropic API.

All Prompt Contracts, logging configuration, and drift reviews for that workload must name this model version explicitly.

---

## Alternatives Considered

- No other models or providers have been formally documented as evaluated for this decision at the time of writing.

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
- The Data Boundary Declaration is introduced or updated in a way that affects what may be sent to the model.

---

## Runtime AI Fields

**Model version rationale:**

Intended direction (not a substitute for a recorded evaluation): use a **Sonnet**-class model where classification requires reliable instruction following and structured outputs, with cost and latency between smaller and larger tiers; confirm against benchmarks and SLOs.

**Human oversight level for affected actions:**

Examples for later resolution: **advisory** if humans always confirm routing; **supervised** if classification is shown before irreversible steps; **autonomous** only if scope and blast radius are explicitly accepted in gate documentation.

**Data boundary decision:**

**Blocked until `docs/gate-2.md` exists.** At decision time, no Data Boundary Declaration was present in the repository.

Before any implementation sends document text or identifiers to this model, the declaration must list exactly what may cross the boundary (e.g. raw text, redacted excerpts, filenames, metadata) and logging rules must match.

**Pinning expiry plan:**

- When **`claude-sonnet-4-6`** is deprecated or superseded, open a new ADR or supersede this one with a new pinned version.
- Re-run Prompt Contract validation and, per project process, include the change in the Phase 7 Class Drift Audit.
- Maintain a fallback path for provider unavailability, rate limits, and invalid model output (per Runtime AI requirements); unhandled exceptions are not an acceptable failure mode.

---

## Record completeness

| Item | State |
|------|--------|
| Decision maker / approver | Incomplete |
| Alternatives actually evaluated | Incomplete |
| Model rationale (vs. named alternatives) | Incomplete |
| Human oversight level for classification | Incomplete |
| Data boundary (gate-2) | Not present — blocking for production LLM calls |

Close this ADR’s incompletes and move **Status** to **Accepted** after the above are documented.
