"""
llm_client.py

LLM client implementing the Prompt Contract for primary taxonomy classification.

Contract reference:
  examples/document-classification-agent/contracts/prompt-contract-classification.md

Behavior per contract:
- Retry up to MAX_LLM_RETRIES times on invalid output (3 total attempts)
- Return fallback_human with INVALID_LLM_OUTPUT on exhausted retries
- Return fallback_human with PROVIDER_UNAVAILABLE on connection failure
- Return fallback_human with PROVIDER_TIMEOUT on timeout
- Never invent a label not in the input label set
- Log hashes of document text, not raw content (per Data Boundary)
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from typing import Optional

import anthropic

from models import (
    CONFIDENCE_COMMIT_THRESHOLD,
    MAX_LLM_RETRIES,
    PER_ATTEMPT_TIMEOUT_SECONDS,
    PINNED_MODEL_ID,
    ClassificationRequest,
    ClassificationResult,
    CONTRACT_VERSION,
    Outcome,
    ReasonCode,
)
from taxonomy import TaxonomyLabel, get_labels, label_ids

logger = logging.getLogger(__name__)

# Maximum characters to send per attempt.
# In production: derive from model context window and token budget.
MAX_DOCUMENT_CHARS = 12_000


def _hash_text(text: str) -> str:
    """SHA-256 hash of text for logging. Never log raw document content."""
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _build_prompt(
    document_text: str,
    labels: list[TaxonomyLabel],
    language_hint: Optional[str] = None,
) -> str:
    """
    Assemble the classification prompt per the Prompt Contract.

    The prompt instructs the model to emit structured JSON with
    primaryLabelId, confidence, and optional shortRationale.
    """
    label_block = "\n".join(
        f"- id: {lbl.id}\n  title: {lbl.title}\n  description: {lbl.description}"
        for lbl in labels
    )

    language_line = (
        f"\nThe document language hint is: {language_hint}.\n"
        if language_hint
        else ""
    )

    return f"""You are a document classification assistant. Your task is to assign a single primary taxonomy label to the document below.

Available labels:
{label_block}
{language_line}
Instructions:
- Select exactly one label id from the list above that best describes the document for routing purposes.
- Do not invent label ids not in the list.
- Respond with valid JSON only, no prose before or after.
- Use this exact structure:

{{
  "primaryLabelId": "<one of the label ids above>",
  "confidence": <number between 0 and 1>,
  "shortRationale": "<one to three sentences explaining your choice>"
}}

Document:
---
{document_text}
---

Respond with JSON only."""


def _parse_llm_response(
    raw: str,
    valid_label_ids: set[str],
) -> Optional[dict]:
    """
    Parse and validate the LLM response against the Prompt Contract output schema.

    Returns the parsed dict if valid, None if the response violates the contract.
    """
    try:
        parsed = json.loads(raw.strip())
    except json.JSONDecodeError:
        logger.warning("LLM response is not valid JSON", extra={"raw_length": len(raw)})
        return None

    primary_label_id = parsed.get("primaryLabelId")
    if not isinstance(primary_label_id, str) or primary_label_id not in valid_label_ids:
        logger.warning(
            "LLM returned invalid primaryLabelId",
            extra={"primary_label_id": primary_label_id},
        )
        return None

    confidence = parsed.get("confidence")
    if confidence is not None:
        if not isinstance(confidence, (int, float)) or not (0 <= confidence <= 1):
            logger.warning(
                "LLM returned invalid confidence value",
                extra={"confidence": confidence},
            )
            return None

    return parsed


def classify(
    request: ClassificationRequest,
    client: anthropic.Anthropic,
) -> ClassificationResult:
    """
    Execute the primary taxonomy classification LLM call per the Prompt Contract.

    Implements:
    - Up to MAX_LLM_RETRIES retries on contract violation
    - fallback_human on exhausted retries or provider failure
    - Structured logging per Data Boundary (hashes, not raw text)
    - Human review routing for requires_human_review taxonomy labels
    """
    labels = get_labels(request.taxonomy_version)
    valid_ids = label_ids(request.taxonomy_version)

    # Check requires_human_review before any LLM call
    # (taxonomy policy may mandate review regardless of model output)
    from taxonomy import load_taxonomy
    taxonomy = load_taxonomy(request.taxonomy_version)

    # Truncate document text per oversize policy
    document_text = request.document_text.strip()
    if len(document_text) > MAX_DOCUMENT_CHARS:
        logger.info(
            "Document text truncated for LLM call",
            extra={
                "request_id": request.request_id,
                "original_length": len(document_text),
                "truncated_length": MAX_DOCUMENT_CHARS,
            },
        )
        document_text = document_text[:MAX_DOCUMENT_CHARS]

    prompt = _build_prompt(document_text, labels, request.language_hint)

    doc_hash = _hash_text(document_text)
    logger.info(
        "Starting LLM classification",
        extra={
            "request_id": request.request_id,
            "document_id": request.document_id,
            "document_text_hash": doc_hash,
            "document_text_length": len(document_text),
            "taxonomy_version": request.taxonomy_version,
            "model_id": PINNED_MODEL_ID,
        },
    )

    last_reason_code = ReasonCode.INVALID_LLM_OUTPUT
    attempts = 0

    for attempt in range(MAX_LLM_RETRIES + 1):
        attempts += 1
        attempt_start = time.monotonic()

        try:
            response = client.messages.create(
                model=PINNED_MODEL_ID,
                max_tokens=512,
                timeout=PER_ATTEMPT_TIMEOUT_SECONDS,
                messages=[{"role": "user", "content": prompt}],
            )
            latency_ms = int((time.monotonic() - attempt_start) * 1000)

            raw_content = response.content[0].text if response.content else ""
            input_tokens = response.usage.input_tokens if response.usage else None
            output_tokens = response.usage.output_tokens if response.usage else None

            logger.info(
                "LLM call completed",
                extra={
                    "request_id": request.request_id,
                    "attempt": attempt + 1,
                    "latency_ms": latency_ms,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "model_id": PINNED_MODEL_ID,
                },
            )

            parsed = _parse_llm_response(raw_content, valid_ids)

            if parsed is None:
                logger.warning(
                    "LLM output violated contract",
                    extra={
                        "request_id": request.request_id,
                        "attempt": attempt + 1,
                    },
                )
                last_reason_code = ReasonCode.INVALID_LLM_OUTPUT
                continue

            primary_label_id = parsed["primaryLabelId"]
            confidence = parsed.get("confidence")

            # Check taxonomy policy for requires_human_review
            label_def = taxonomy.get(primary_label_id)
            requires_human = label_def.requires_human_review if label_def else False

            if requires_human:
                logger.info(
                    "Label requires human review per taxonomy policy",
                    extra={
                        "request_id": request.request_id,
                        "primary_label_id": primary_label_id,
                    },
                )
                return ClassificationResult(
                    contract_version=CONTRACT_VERSION,
                    request_id=request.request_id,
                    taxonomy_version=request.taxonomy_version,
                    model_id=PINNED_MODEL_ID,
                    outcome=Outcome.FALLBACK_HUMAN,
                    primary_label=primary_label_id,
                    confidence=confidence,
                    requires_human_review=True,
                    reason_codes=[ReasonCode.REQUIRES_HUMAN_REVIEW],
                )

            # Check confidence threshold per Gate 2
            if confidence is not None and confidence < CONFIDENCE_COMMIT_THRESHOLD:
                logger.info(
                    "Confidence below commit threshold",
                    extra={
                        "request_id": request.request_id,
                        "confidence": confidence,
                        "threshold": CONFIDENCE_COMMIT_THRESHOLD,
                    },
                )
                return ClassificationResult(
                    contract_version=CONTRACT_VERSION,
                    request_id=request.request_id,
                    taxonomy_version=request.taxonomy_version,
                    model_id=PINNED_MODEL_ID,
                    outcome=Outcome.FALLBACK_HUMAN,
                    primary_label=primary_label_id,
                    confidence=confidence,
                    reason_codes=[ReasonCode.LOW_CONFIDENCE],
                )

            # Success
            logger.info(
                "Classification succeeded",
                extra={
                    "request_id": request.request_id,
                    "primary_label_id": primary_label_id,
                    "confidence": confidence,
                    "attempts": attempts,
                },
            )
            return ClassificationResult(
                contract_version=CONTRACT_VERSION,
                request_id=request.request_id,
                taxonomy_version=request.taxonomy_version,
                model_id=PINNED_MODEL_ID,
                outcome=Outcome.SUCCESS,
                primary_label=primary_label_id,
                confidence=confidence,
            )

        except anthropic.APITimeoutError:
            latency_ms = int((time.monotonic() - attempt_start) * 1000)
            logger.warning(
                "LLM call timed out",
                extra={
                    "request_id": request.request_id,
                    "attempt": attempt + 1,
                    "latency_ms": latency_ms,
                    "timeout_seconds": PER_ATTEMPT_TIMEOUT_SECONDS,
                },
            )
            last_reason_code = ReasonCode.PROVIDER_TIMEOUT

        except anthropic.APIConnectionError:
            logger.warning(
                "LLM provider unavailable",
                extra={
                    "request_id": request.request_id,
                    "attempt": attempt + 1,
                },
            )
            last_reason_code = ReasonCode.PROVIDER_UNAVAILABLE
            # Do not retry on connection errors in this implementation
            break

        except anthropic.RateLimitError:
            logger.warning(
                "LLM rate limited",
                extra={
                    "request_id": request.request_id,
                    "attempt": attempt + 1,
                },
            )
            last_reason_code = ReasonCode.RATE_LIMITED
            break

    # All attempts exhausted or non-retryable failure
    logger.warning(
        "Classification falling back to human queue",
        extra={
            "request_id": request.request_id,
            "attempts": attempts,
            "reason_code": last_reason_code.value,
        },
    )
    return ClassificationResult(
        contract_version=CONTRACT_VERSION,
        request_id=request.request_id,
        taxonomy_version=request.taxonomy_version,
        model_id=PINNED_MODEL_ID,
        outcome=Outcome.FALLBACK_HUMAN,
        reason_codes=[last_reason_code],
    )
