"""
validation.py

Input validation against the Class Interface Contract v1.0.0.
All validation runs before any LLM call is made.

Contract reference:
  examples/document-classification-agent/contracts/class-interface-contract.md
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

from models import (
    CONTRACT_VERSION,
    MIN_DOCUMENT_TEXT_LENGTH,
    PINNED_MODEL_ID,
    ClassificationRequest,
    ClassificationResult,
    Outcome,
    ReasonCode,
)
from taxonomy import label_ids, load_taxonomy

logger = logging.getLogger(__name__)


@dataclass
class ValidationError:
    reason_code: ReasonCode
    message: str


def validate_request(
    request: ClassificationRequest,
) -> Optional[ValidationError]:
    """
    Validate a ClassificationRequest against the Class Interface Contract.

    Returns None if valid.
    Returns a ValidationError describing the first blocking condition if invalid.

    Per the contract, validation failures do not call the LLM.
    """

    # contractVersion must be pinned value
    if request.contract_version != CONTRACT_VERSION:
        return ValidationError(
            reason_code=ReasonCode.INVALID_CONTRACT_VERSION,
            message=(
                f"contractVersion must be '{CONTRACT_VERSION}', "
                f"got '{request.contract_version}'."
            ),
        )

    # modelId must be pinned value per ADR-001
    if request.model_id != PINNED_MODEL_ID:
        return ValidationError(
            reason_code=ReasonCode.INVALID_MODEL_ID,
            message=(
                f"modelId must be '{PINNED_MODEL_ID}', "
                f"got '{request.model_id}'. "
                "Only the pinned model may be used per ADR-001."
            ),
        )

    # taxonomyVersion must be known
    try:
        load_taxonomy(request.taxonomy_version)
    except ValueError as exc:
        logger.warning(
            "Unknown taxonomy version",
            extra={
                "request_id": request.request_id,
                "taxonomy_version": request.taxonomy_version,
            },
        )
        return ValidationError(
            reason_code=ReasonCode.UNKNOWN_TAXONOMY_VERSION,
            message=str(exc),
        )

    # documentText must be present and meet minimum length
    stripped = request.document_text.strip() if request.document_text else ""
    if len(stripped) < MIN_DOCUMENT_TEXT_LENGTH:
        logger.info(
            "Document text below minimum length threshold",
            extra={
                "request_id": request.request_id,
                "text_length": len(stripped),
                "minimum": MIN_DOCUMENT_TEXT_LENGTH,
            },
        )
        return ValidationError(
            reason_code=ReasonCode.EMPTY_DOCUMENT,
            message=(
                f"documentText must be at least {MIN_DOCUMENT_TEXT_LENGTH} "
                f"characters after stripping whitespace. "
                f"Got {len(stripped)} characters."
            ),
        )

    return None


def build_rejection_result(
    request: ClassificationRequest,
    error: ValidationError,
    outcome: Outcome = Outcome.ERROR_NO_ROUTE,
) -> ClassificationResult:
    """
    Build a ClassificationResult for a rejected request.

    Boundary behavior per Gate 2:
    - Empty/near-empty document: fallback_human or error_no_route
    - Unknown taxonomy version: error_no_route (fail closed)
    - Invalid modelId or contractVersion: error_no_route
    """
    logger.info(
        "Request rejected at validation",
        extra={
            "request_id": request.request_id,
            "document_id": request.document_id,
            "reason_code": error.reason_code.value,
            "outcome": outcome.value,
        },
    )
    return ClassificationResult(
        contract_version=CONTRACT_VERSION,
        request_id=request.request_id,
        taxonomy_version=request.taxonomy_version,
        model_id=request.model_id,
        outcome=outcome,
        reason_codes=[error.reason_code],
    )
