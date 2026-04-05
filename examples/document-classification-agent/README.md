# Document Classification Agent — Worked Example

A minimum viable implementation of the Document Classification Agent described in the gate worksheets and contracts under `examples/document-classification-agent/`.

This implementation builds directly against:
- `contracts/class-interface-contract.md` — input/output schema
- `contracts/prompt-contract-classification.md` — LLM call behavior
- `adr/ADR-001-model-selection.md` — model selection and pinning

---

## Structure

```
src/
├── taxonomy.py        # Versioned taxonomy artifact loader and label definitions
├── models.py          # Request and result dataclasses matching the contract schemas
├── validation.py      # Input validation (runs before any LLM call)
├── llm_client.py      # Anthropic API call with retry and fallback logic
├── classifier.py      # Main entry point composing validation and LLM call
└── test_classifier.py # Test suite covering Gate 3 verification requirements
requirements.txt
```

---

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
```

---

## Run the tests

```bash
cd src
pytest test_classifier.py -v
```

Tests run without a real API key — all LLM calls are mocked. The test suite covers:
- Input validation (contract rejection criteria)
- Successful classification (in-class cases)
- Class boundary behavior (low confidence, requires_human_review, invalid LLM output)
- Provider failure handling (timeout, connection error, rate limit)
- Output contract verification

---

## Run a classification

```python
from classifier import classify_document
from models import ClassificationRequest

result = classify_document(
    ClassificationRequest(
        contract_version="1.0.0",
        request_id="req-001",
        tenant_id="tenant-a",
        document_id="doc-001",
        taxonomy_version="1.0.0",
        model_id="claude-sonnet-4-6",
        document_text="Please find attached our invoice #1234 for March services.",
    )
)

print(result.to_dict())
```

---

## Key behaviors per the contracts

**Input validation (no LLM call on failure):**
- Wrong `contractVersion` → `error_no_route`
- Wrong `modelId` → `error_no_route`
- Unknown `taxonomyVersion` → `error_no_route`
- Empty or too-short `documentText` → `fallback_human`

**Classification outcomes:**
- Valid label, confidence ≥ 0.65, no human review policy → `success`
- Valid label, confidence < 0.65 → `fallback_human` with `LOW_CONFIDENCE`
- Label with `requires_human_review = true` → `fallback_human` regardless of confidence
- Invalid LLM output after 3 attempts → `fallback_human` with `INVALID_LLM_OUTPUT`
- Provider unavailable → `fallback_human` with `PROVIDER_UNAVAILABLE`
- Timeout → `fallback_human` with `PROVIDER_TIMEOUT`
- Rate limited → `fallback_human` with `RATE_LIMITED`

No silent routing. Every outcome is explicit.

---

## Gate 3 verification

The test suite is the Gate 3 behavioral eval implementation. Run it against real API calls by removing the mock and setting `ANTHROPIC_API_KEY`. The Gate 3 worksheet (`gate-3.md`) records the results.

---

## What this example demonstrates

1. **Build against contracts, not against a description.** Every behavior in the implementation is traceable to a specific field or requirement in the Class Interface Contract or Prompt Contract.

2. **All failure paths are explicit.** There is no path that produces a `success` outcome when inference did not complete correctly.

3. **Logging respects the Data Boundary.** Document text is hashed before logging; raw content is never written to logs by default.

4. **Tests cover the class boundary, not just the happy path.** The test suite exercises the conditions identified in Gate 2's class boundary behavior section.
