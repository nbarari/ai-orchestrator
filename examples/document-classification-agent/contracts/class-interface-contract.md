# Class Interface Contract: Document Classification Agent

**System:** Document Classification Agent (Worked Example)
**Date:** 2026-04-05
**Author:** ai-orchestrator-framework contributors
**Status:** Draft

**References:**

- Problem class: `examples/document-classification-agent/gate-0.md`
- Design gate: `examples/document-classification-agent/gate-2.md`
- Prompt Contract (primary LLM call): `prompt-contract-classification.md`
- Model ADR: `../adr/ADR-001-model-selection.md`

---

## Purpose

This contract defines the **valid input** and **valid output** for the classification service at the system boundary: one logical **classification request** yields one **classification result** suitable for routing and audit, independent of internal implementation.

Runtime AI is in scope: the primary label is produced by an LLM call governed by the Prompt Contract.

---

## contractVersion

| Field | Value |
|---|---|
| `contractVersion` | `1.0.0` |

Bump **minor** when adding optional fields backward-compatibly; **major** when removing or redefining required fields or semantics.

---

## Input: Classification Request

### Valid input (summary)

A request MUST include stable document identity, tenant scope, pinned taxonomy version, pinned model identifier, and authoritative document text (or an explicit chunk sequence for oversize handling). It MUST NOT rely on modalities outside Gate 0 (e.g., raw image bytes without text).

### JSON schema (normative shape)

Describe payloads using this shape; implementations may use equivalent structs. `additionalProperties` is **false** on each object unless a future minor version explicitly documents an extension.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ClassificationRequest",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "contractVersion",
    "requestId",
    "tenantId",
    "documentId",
    "taxonomyVersion",
    "modelId",
    "documentText"
  ],
  "properties": {
    "contractVersion": {
      "type": "string",
      "const": "1.0.0"
    },
    "requestId": {
      "type": "string",
      "description": "Correlation id for logs and idempotency grouping."
    },
    "idempotencyKey": {
      "type": "string",
      "description": "Stable key so retries do not double-commit downstream effects."
    },
    "tenantId": {
      "type": "string",
      "description": "Opaque tenant identifier; required for isolation and routing."
    },
    "documentId": {
      "type": "string",
      "description": "Opaque document identifier from intake."
    },
    "taxonomyVersion": {
      "type": "string",
      "description": "Pinned taxonomy artifact version (labels + descriptions + policy flags)."
    },
    "modelId": {
      "type": "string",
      "const": "claude-sonnet-4-6",
      "description": "Pinned model per ADR-001 and Prompt Contract."
    },
    "languageHint": {
      "type": "string",
      "description": "Optional BCP 47 or org allowlist token; if present and out of allowlist, apply Gate 2 class-boundary behavior."
    },
    "documentText": {
      "type": "string",
      "description": "Authoritative text content for classification."
    },
    "oversizeHandling": {
      "type": "string",
      "enum": ["reject", "truncate_head", "chunk_then_aggregate", "human_queue"],
      "description": "How to handle text exceeding model/context policy; must match implementation capability."
    }
  }
}
```

### Invalid input (rejection criteria)

| Condition | System behavior |
|---|---|
| Missing required fields or wrong `contractVersion` | Reject at API validation; do not call LLM. |
| `documentText` empty or below minimum length | Reject or `fallback_human` per gate-2 class boundary (no LLM for silent routing). |
| `taxonomyVersion` unknown | Fail closed; operator alert. |
| `modelId` not pinned value | Reject; prevents accidental uncontracted models. |

---

## Output: Classification Result

### Valid output (summary)

A result MUST state an explicit **outcome**, include versioning metadata, and when a primary label is present MUST tie it to the taxonomy version used. It MUST NOT expose raw unchecked LLM text as the only routable signal—structured fields per Prompt Contract.

### JSON schema (normative shape)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ClassificationResult",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "contractVersion",
    "requestId",
    "taxonomyVersion",
    "modelId",
    "outcome"
  ],
  "properties": {
    "contractVersion": {
      "type": "string",
      "const": "1.0.0"
    },
    "requestId": {
      "type": "string"
    },
    "taxonomyVersion": {
      "type": "string"
    },
    "modelId": {
      "type": "string"
    },
    "outcome": {
      "type": "string",
      "enum": ["success", "fallback_human", "error_no_route"]
    },
    "primaryLabel": {
      "type": "string",
      "description": "Taxonomy primary label when outcome is success and contract validated."
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "If present, used with Gate 2 thresholds; may be absent if model does not emit."
    },
    "requiresHumanReview": {
      "type": "boolean",
      "description": "True when taxonomy policy mandates review regardless of confidence."
    },
    "reasonCodes": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Stable machine codes, e.g. INVALID_LLM_OUTPUT, PROVIDER_TIMEOUT, LOW_CONFIDENCE."
    },
    "traceId": {
      "type": "string",
      "description": "Distributed trace id for observability."
    }
  }
}
```

### Outcome semantics

| `outcome` | Meaning |
|---|---|
| `success` | Valid structured result; primary label may be used per Human Oversight Model (supervised commit in initial deployment). |
| `fallback_human` | No safe automated routing; human queue per policy. |
| `error_no_route` | Validation or class-boundary block; no downstream automated route. |

---

## Prompt Contract linkage

| LLM call | Prompt Contract | Model |
|---|---|---|
| Primary classification | `prompt-contract-classification.md` | `claude-sonnet-4-6` |

---

## Alignment with Success Predicate (Gate 0)

- **Routing accuracy:** Evaluated against pinned taxonomy and thresholds in `gate-2.md`.
- **Operational safety:** Invalid outputs and low-confidence paths resolve to `fallback_human` or `error_no_route`, not silent wrong routes.
- **Traceability:** `requestId`, `traceId`, `taxonomyVersion`, and `modelId` enable replay and audit when combined with logging policy in the Prompt Contract and Data Boundary Declaration.
