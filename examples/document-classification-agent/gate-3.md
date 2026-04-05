# Gate 3: Technical Verification

**Project:** Document Classification Agent (Worked Example)
**Date:** 2026-04-05
**Author:** ai-orchestrator-framework contributors
**Status:** Accepted

**Gate 0 reference:** `examples/document-classification-agent/gate-0.md`
**Gate 2 reference:** `examples/document-classification-agent/gate-2.md`

Reference: `manual.md` Phase 5.

**Test run:** 23 passed, 0 failed, 0.93 seconds
**Test suite:** `examples/document-classification-agent/src/test_classifier.py`
**Platform:** Python 3.14.3, pytest 9.0.2, macOS arm64

**Stop Criteria:** Halt if core functional requirements fail, if the system cannot reach the Breaking Point identified in Phase 3, or if class boundary behavior produces undefined outcomes.

---

## Verification

### Class Coverage

Does the test suite cover the full breadth of the defined problem class?

**In-class cases tested:**

```
- Invoice document classified successfully with confidence ≥ 0.65
  (TestSuccessfulClassification::test_invoice_document_returns_success)

- Contract document classified successfully with confidence ≥ 0.65
  (TestSuccessfulClassification::test_contract_document_returns_success)

- Result contains all required contract fields on success
  (TestSuccessfulClassification::test_result_contains_required_fields)
```

**Boundary cases tested:**

```
- Empty document text → fallback_human with EMPTY_DOCUMENT reason code
  (TestInputValidation::test_empty_document_text_returns_fallback_human)

- Whitespace-only document text → fallback_human with EMPTY_DOCUMENT
  (TestInputValidation::test_whitespace_only_document_returns_fallback_human)

- Document text below minimum character threshold → fallback_human
  (TestInputValidation::test_below_minimum_length_returns_fallback_human)

- LLM returns label not in taxonomy → retries 3 times, then fallback_human
  (TestClassBoundaryBehavior::test_invalid_label_in_llm_response_retries_then_falls_back)

- LLM returns non-JSON → retries 3 times, then fallback_human
  (TestClassBoundaryBehavior::test_invalid_json_response_retries_then_falls_back)

- Confidence below 0.65 threshold → fallback_human with LOW_CONFIDENCE;
  proposed label is preserved in result for human reviewer context
  (TestClassBoundaryBehavior::test_low_confidence_routes_to_fallback_human)

- Label with requires_human_review = true → fallback_human with
  REQUIRES_HUMAN_REVIEW regardless of confidence value
  (TestClassBoundaryBehavior::test_requires_human_review_label_routes_to_fallback)
```

**Gaps identified:**

```
- Oversize document truncation behavior is implemented in llm_client.py
  (truncate to MAX_DOCUMENT_CHARS = 12,000 characters) but not covered
  by a dedicated test case. A test sending a document exceeding
  MAX_DOCUMENT_CHARS and verifying it is truncated rather than rejected
  should be added before production deployment.

- Language hint behavior (adjacent-to-class input with unsupported language)
  is specified in the Class Interface Contract but not tested. Test should
  verify that an unsupported languageHint results in fallback_human rather
  than a confident automated label.

- Idempotency key behavior is not exercised in the test suite. The
  idempotencyKey field exists in the contract but the worked example
  does not implement idempotency logic in the service layer. This is
  acceptable for Minimum Viable Coverage but must be addressed before
  production deployment handles retries with downstream side effects.

These gaps are documented as known limitations of the worked example,
not as gate blockers. A production deployment must address all three
before Gate 3 can be approved against real system behavior.
```

---

### Contract Verification

Does the system adhere to the Class Interface Contracts defined in Phase 3?

**Link to Class Interface Contract:** `examples/document-classification-agent/contracts/class-interface-contract.md`

| Contract requirement | Verified | Method | Notes |
|---|---|---|---|
| Input schema validation rejects invalid inputs | Yes | Unit tests — TestInputValidation (7 tests) | Wrong contractVersion, wrong modelId, unknown taxonomyVersion, empty/short documentText all reject correctly |
| Output schema matches contract on success | Yes | Unit tests — TestOutputContract (5 tests) | contractVersion, requestId, taxonomyVersion, modelId, outcome all present; to_dict() verified against required fields |
| Contract version enforced | Yes | test_wrong_contract_version_returns_error_no_route | Rejects any value other than "1.0.0" |
| Rejection criteria produce documented behavior | Yes | Unit tests across TestInputValidation and TestClassBoundaryBehavior | Each rejection criterion maps to a specific outcome and reason code |

**Prompt Contract verification (Runtime AI):**

| LLM call | Contract file | Output matches contract | Violation handling verified |
|---|---|---|---|
| Primary taxonomy classification | `contracts/prompt-contract-classification.md` | Yes — mocked responses exercise valid and invalid output shapes | Yes — invalid JSON and invalid label ID both trigger retry then fallback |

---

### Signal Verification

Do health signals and alerts fire correctly under failure conditions?

| Signal | Condition that triggers it | Verified | Notes |
|---|---|---|---|
| INVALID_LLM_OUTPUT reason code | LLM returns non-contract output after 3 attempts | Yes | test_invalid_label_in_llm_response and test_invalid_json_response both verify reason code present |
| PROVIDER_TIMEOUT reason code | APITimeoutError raised by client | Yes | test_timeout_returns_fallback_human |
| PROVIDER_UNAVAILABLE reason code | APIConnectionError raised by client | Yes | test_connection_error_returns_fallback_human |
| RATE_LIMITED reason code | RateLimitError raised by client | Yes | test_rate_limit_returns_fallback_human |
| LOW_CONFIDENCE reason code | Confidence below 0.65 threshold | Yes | test_low_confidence_routes_to_fallback_human |
| REQUIRES_HUMAN_REVIEW reason code | Label has requires_human_review = true in taxonomy | Yes | test_requires_human_review_label_routes_to_fallback |
| EMPTY_DOCUMENT reason code | documentText empty or below minimum length | Yes | Three test cases covering empty, whitespace, and short text |

**Gaps:**

```
- Production alerting (operator-visible queue depth alerts, latency SLO
  breach notifications) is not implemented in the worked example. The
  llm_client.py logs structured events at each decision point, but no
  metrics emission or alerting integration exists. This is acceptable for
  Minimum Viable Coverage; production deployment requires a monitoring
  layer per Gate 2 BOM (observability infrastructure).

- Health check endpoint is not implemented. The worked example is a
  Python module, not a running service; no HTTP health signal exists.
  Production deployment requires a liveness/readiness probe.
```

---

### Stress Test

Has the system been pushed to the Breaking Point identified in Gate 2?

**Breaking Point identified in Gate 2:**

```
First failure under growth is LLM provider throughput or org-level rate
limits (queue backlog grows, latency SLO slips). Breaking Point metric:
queue age p95 exceeds 15 minutes during steady load. The design fails
safe: overload surfaces as delay and human routing, not as random labels.
```

**Stress test results:**

| Load level | Observed behavior | Breaking Point reached? |
|---|---|---|
| Steady state (mocked) | 23 tests complete in 0.93s; all pass | N/A — no real provider calls |
| Peak (Gate 1 estimate: 2-5x steady) | Not tested against real provider | No |
| Breaking Point threshold (p95 queue age > 15min) | Not tested — no queue infrastructure in worked example | No |

**First component to fail under load:**

```
Not measured in the worked example. The implementation has no queue,
no metrics, and no load testing harness. Per Gate 2, the expected first
failure is LLM provider rate limiting, followed by downstream workflow
consumer backlog.

For a production deployment, stress testing against the real Anthropic
API at expected peak volume (Gate 1 estimate) is required before Gate 3
can be approved. The worked example acknowledges this as a known gap in
Minimum Viable Coverage.
```

---

### Behavioral Evals (Runtime AI)

Does the verification suite include behavioral evals that test class-level correctness?

**Eval criteria from Gate 2:**

```
Correctness criteria:
- Top-1 primary-label accuracy ≥ 90% on held-out evaluation set
- Safety-critical / always-review labels: 100% routed to human review
- Invalid LLM output never produces a silent production route
- Provider failure never produces a confident automated route

Class boundary eval criteria:
- Adjacent inputs follow Class Boundary Behavior without fabricating confidence
- Idempotent retries do not duplicate downstream commits

Runtime AI eval criteria:
- Outputs conform to Prompt Contract JSON/schema; violations caught in tests
- Nondeterminism allowed; contract violations are not allowed
- Golden-set behavioral tests per claude-sonnet-4-6 and pinned taxonomy
```

**Coverage of criteria:**

| Eval criterion | Covered | Method | Pass rate or result |
|---|---|---|---|
| Top-1 accuracy ≥ 90% on evaluation set | No — mocked only | Real API calls with labeled set required | Not measured; requires real evaluation set and API calls |
| Always-review labels route to human 100% | Yes | test_requires_human_review_label_routes_to_fallback | Pass — "regulated" label correctly routes to fallback_human regardless of confidence |
| Invalid LLM output never silent routes | Yes | test_invalid_label_in_llm_response, test_invalid_json_response | Pass — both route to fallback_human after 3 attempts |
| Provider failure never routes autonomously | Yes | TestProviderFailure (4 tests) | Pass — timeout, connection, rate limit all produce fallback_human; test_no_success_outcome_on_provider_failure confirms |
| Adjacent inputs follow class boundary behavior | Yes | TestInputValidation (7 tests) + TestClassBoundaryBehavior (4 tests) | Pass — empty, short, low-confidence, invalid output all handled per contract |
| Idempotent retries do not duplicate downstream | No — not implemented | Would require queue and downstream stub | Gap noted above |
| Prompt Contract output schema compliance | Yes | TestOutputContract (5 tests) + contract violation tests | Pass — valid outputs match schema; violations trigger retry then fallback |
| Nondeterminism: violations not allowed | Yes | All contract violation tests | Pass — any output not matching contract triggers retry, not silent acceptance |

**Note on nondeterminism:** All behavioral evals in the test suite use mocked LLM responses. The mocks exercise the contract violation handling path (invalid label, invalid JSON) but do not exercise nondeterministic variation in valid outputs. Production behavioral evals against the real API should include multiple runs of the same input to verify output distribution stays within contract bounds.

**Gaps:**

```
- Top-1 accuracy against a real labeled evaluation set is not measured.
  This is the primary correctness criterion from Gate 2 and the only
  criterion not covered by the worked example test suite. A production
  Gate 3 requires this measurement.

- Golden-set tests against the real claude-sonnet-4-6 model are not
  included. All tests use mocked responses. Adding at least a small
  golden set (10-20 labeled documents) tested against the real API
  would validate that the prompt structure produces the expected label
  distribution before production deployment.
```

---

## Diagnostic Audit

### Self-Service Diagnosis

Can a qualified person diagnose a failure without access to the original builder?

- [x] Yes — structured logging at every decision point in llm_client.py and classifier.py; README documents all outcome/reason code combinations
- [ ] No — document what is missing before this gate is approved

**Evidence:**

```
The implementation logs structured events at each decision point:
- classify_document called (request metadata, no document content)
- Validation rejection (reason code, outcome)
- LLM call started (request_id, document_id, document text hash and length,
  taxonomy version, model id — no raw document content per Data Boundary)
- LLM call completed (latency_ms, input_tokens, output_tokens, model_id)
- LLM output violated contract (attempt number)
- Confidence below commit threshold (confidence value, threshold)
- Label requires human review (label id)
- Classification fell back to human queue (attempts, reason code)
- Classification succeeded (label id, confidence, attempts)

The README at examples/document-classification-agent/README.md documents
all outcome and reason code combinations. A qualified engineer can trace
any classification result back to its cause using request_id as the
correlation key.

Gap for production: logs are structured Python logging output. A production
deployment requires log aggregation (e.g., CloudWatch, Datadog, Splunk) and
a runbook tested by someone other than the author. The worked example
does not include a formal runbook.
```

---

### Traceability

Are logs, traces, and metrics sufficient to reconstruct a failure after the fact?

| What must be traceable | Logged? | Location | Notes |
|---|---|---|---|
| Request identifier | Yes | All log events include request_id | Used as correlation key |
| Input received | Partial | document text hash and length logged; raw text not logged | Compliant with Data Boundary — hash sufficient to verify document identity |
| Model version used | Yes | Logged at LLM call start and in result | Required for audit per contract |
| Output produced | Yes | Structured outcome and reason codes logged | Rationale logged as internal; raw LLM text not retained by default |
| Latency | Yes | latency_ms logged per attempt | Sufficient for SLO monitoring |
| Outcome (success / fallback / error) | Yes | Logged at classification start and end | All three outcome values logged explicitly |
| Fallback reason | Yes | reason_codes logged for all non-success outcomes | Maps directly to contract ReasonCode enum |

**Data Boundary compliance (Runtime AI):**
Is the logging approach compliant with the Data Boundary Declaration from Gate 2?

- [x] Yes — logging reviewed against Data Boundary Declaration

Document text is hashed (SHA-256, first 16 hex characters) before logging. Raw document content is not written to logs. Token counts are logged for cost monitoring. Structured output fields (primary label, confidence, reason codes) are logged; the LLM's shortRationale is treated as internal and not retained in the default logging path.

**Note:** Logging what should not be logged is a compliance failure equivalent to not logging what should be.

---

## Gate Approval

- [x] Class coverage verified including boundary cases
- [x] All Class Interface Contract requirements verified
- [x] Prompt Contract outputs verified for all LLM calls (Runtime AI)
- [x] All health signals verified under failure conditions
- [ ] Stress test completed to Breaking Point — **not completed; known gap in worked example**
- [x] Behavioral evals cover all criteria from Gate 2 (Runtime AI) — **with documented gaps: accuracy on real eval set and golden-set tests not included**
- [ ] Self-service diagnosis confirmed by non-author — **runbook not yet written; logging is sufficient for diagnosis**
- [x] Traceability verified for all required fields
- [x] Logging is compliant with Data Boundary Declaration (Runtime AI)

**Approved by:** ai-orchestrator-framework contributors (worked example)
**Date:** 2026-04-05

**Notes:**

This Gate 3 documents verification against a **mocked test suite** (23 tests, 0 failures). Two checklist items are not fully satisfied for the worked example and are documented as known gaps rather than blockers:

1. **Stress test not completed.** The worked example has no queue infrastructure, no load testing harness, and no real provider calls. The breaking point identified in Gate 2 (queue age p95 > 15 minutes) cannot be measured without a deployed service. A production Gate 3 requires stress testing at the Gate 1 volume estimate against the real Anthropic API.

2. **Top-1 accuracy on real evaluation set not measured.** All LLM responses are mocked. The primary correctness criterion from Gate 2 (≥ 90% accuracy) cannot be verified without a labeled evaluation set and real API calls. This is the most significant gap in the worked example.

For a production deployment, both gaps are blocking. The worked example proceeds to Gate 4 with these gaps documented to demonstrate the framework's structure; real deployments must resolve them before Gate 3 approval.

See `examples/notes.md` for framework observations surfaced during this gate.
