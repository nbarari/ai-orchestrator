# Prompt Contract: Primary taxonomy classification

A Prompt Contract defines the interface for a single LLM call. It is a component of the Class Interface Contract for Runtime AI systems.

**System:** Document Classification Agent (Worked Example)
**LLM call name / identifier:** `primary_taxonomy_classification`
**Model version validated against:** `claude-sonnet-4-6`
**Date:** 2026-04-05
**Author:** ai-orchestrator-framework contributors
**Status:** Draft

**Related:** `class-interface-contract.md`, `../gate-2.md`, `../adr/ADR-001-model-selection.md`

---

## Purpose

What problem-class operation does this LLM call perform? State this in terms of the Problem Class Definition from Gate 0, not in terms of the model or prompt.

```
Given authoritative text for a single inbound document and a pinned, versioned taxonomy (labels and descriptions), select the single primary taxonomy label that best determines downstream routing for that document, and emit a structured response that can be validated against this contract. This call does not define or modify the taxonomy, extract unrelated structured fields, or execute downstream workflows.
```

---

## Input Contract

### Required inputs

| Field | Type | Description | Constraints |
|---|---|---|---|
| `taxonomyVersion` | string | Pinned taxonomy artifact version | Must match request; labels/descriptions loaded from artifact, not free-form user text. |
| `labels` | array of objects | Allowed primary labels for this request | Each item: `id` (string), `title` (string), `description` (string); subset of taxonomy per tenant config. |
| `documentText` | string | Authoritative document body | Must comply with class-interface input validation; truncated/chunked only per oversize policy with explicit markers. |
| `outputSchemaHint` | string or object | Instructions to emit parseable structured output | Fixed template in implementation; constrains model to JSON or equivalent. |

### Optional inputs

| Field | Type | Description | Default |
|---|---|---|---|
| `languageHint` | string | Hint for language | Omitted if unknown |
| `priorLabel` | string | Previously assigned label for relabel flows | Omitted |

### Input validation

What makes an input invalid for this call? What does the system do with an invalid input before it reaches the LLM?

```
- Missing or empty `documentText` after trimming: do not call the LLM; return class-interface `error_no_route` or `fallback_human` per gate-2.
- Empty `labels` list: invalid; fail closed.
- Oversize `documentText` relative to token budget: apply oversize strategy from class-interface request (`oversizeHandling`); never silently pass full text that exceeds declared policy.
- Disallowed content patterns (e.g., secret material): strip/block per Data Boundary; if document unusable, no LLM call.
```

### Data Boundary Compliance

Confirm that all input fields are permitted to cross into this LLM call per the Data Boundary Declaration in Gate 2.

| Field | Permitted | Policy basis |
|---|---|---|
| `labels` / taxonomy text | Yes | Internal product definitions; required for classification. |
| `documentText` | Yes*, conditional on org policy | Required for routing; *regulated/PII content only if org governance approves provider processing; otherwise pre-redact. |
| `languageHint` | Yes | Low sensitivity. |
| `priorLabel` | Yes | Internal routing metadata. |

---

## Output Contract

### Expected output structure

| Field | Type | Description | Required |
|---|---|---|---|
| `primaryLabelId` | string | Must match one of the supplied label `id` values | Yes |
| `confidence` | number | 0–1 calibrated or model-reported | Yes if model supports; else omit and rely on validation path |
| `shortRationale` | string | One to three sentences, non-binding | No |
| `alternates` | array | Optional secondary candidates with scores | No |

### Output constraints

What properties must the output satisfy to be considered valid?

```
- Parseable JSON (or equivalent fixed format) matching the implementation schema.
- `primaryLabelId` MUST be exactly one of the input label ids.
- `confidence` in [0, 1] when present.
- No additional fields that bypass validation (`additionalProperties` false at application layer).
```

### Class-level correctness criteria

What does a correct output look like at the problem-class level? These become the behavioral eval criteria for this call.

```
- The chosen primary label matches the gold label on the evaluation set at or above the Gate 2 accuracy target, given the pinned taxonomy and model version.
- For ambiguous but decidable cases, label choice aligns with taxonomy definitions rather than arbitrary wording.
- When the model cannot decide safely, the implementation must detect low confidence or invalid structure and move to fallback per gate-2—not treat a guess as success.
```

---

## Contract Violation Handling

### Invalid output

What does the system do when the LLM returns output that violates this contract?

- [x] Retry with the same input (maximum **2** retries)
- [ ] Retry with a modified input
- [x] Fall back to: **`fallback_human`** (no automated route commit)
- [ ] Reject and surface error to caller
- [ ] Other:

```
Parse/validate failure → retry up to 2 times (3 total attempts) with identical validated prompt inputs and idempotency key. If still invalid, emit class-interface outcome `fallback_human` with reason code `INVALID_LLM_OUTPUT`. No invented labels.
```

### Provider unavailability

What does the system do when the LLM provider cannot be reached?

```
Do not emit `success`. Return `fallback_human` or `error_no_route` per API mapping; enqueue retry with exponential backoff; operator-visible alert when backlog thresholds exceeded. Align with gate-2 Failure Mode Registry.
```

### Rate limiting

What does the system do when the call is rate-limited?

```
Client-side backoff and queue; shed load per policy; escalate if queue depth breaches SLO; never substitute a cached label from a different document.
```

---

## Observability

### Logged fields

| Field | Logged | Privacy classification |
|---|---|---|
| Input | Partial | Log **hashes** of documentText and full length; full text only if Data Boundary permits and retention policy allows |
| Output | Yes (structured) | Treat rationale as internal; same redaction rules as input for free text |
| Latency | Yes | Operational |
| Token count | Yes | Operational / cost |
| Model version | Yes | Required for audit |

**Logging complies with Data Boundary Declaration:**

- [x] Confirmed (worked example: structured logs + redaction defaults; production must match governance)

---

## Human Oversight

What oversight level applies to any actions taken based on this call's output?

- [ ] Autonomous: system acts on output without human review
- [x] Supervised: human reviews output before action is taken
- [ ] Advisory: human makes the decision; this call informs it

**Rationale:**

```
Initial deployment uses **supervised** oversight for committing irreversible or high–blast-radius downstream routes: the structured classification may be stored autonomously for audit, but workflow commits require human or approved batch release per gate-2 Human Oversight Model. Low-confidence and invalid outputs route to human review without autonomous commit.
```

---

## Model Version

**Validated against:** `claude-sonnet-4-6`

**Pinning strategy:**

```
Configure the Anthropic API client with an explicit model string `claude-sonnet-4-6` in versioned configuration (IaC or service config); reject undeclared model aliases in production. CI checks that prompts and contracts reference the same identifier.
```

**Pinning expiry plan:**

What happens when this version is deprecated?

```
Open a new ADR selecting a replacement pinned version; re-run behavioral evals and update Prompt Contract and Class Interface Contract; complete Phase 7 Class Drift Audit; maintain provider failure fallbacks throughout migration.
```

---

## Review Trigger

What event requires this Prompt Contract to be revisited?

Minimum triggers: model version change, output quality degradation detected in Phase 7 audit, change to the Class Interface Contract, Data Boundary Declaration update.

```
- Taxonomy version change affecting label ids or descriptions.
- Change to oversize or language policy.
- Shift from supervised to partial autonomous routing (requires new ADR and Gate 4 evidence).
```
