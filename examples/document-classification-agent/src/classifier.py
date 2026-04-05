"""
classifier.py

Main entry point for the Document Classification Agent.

Composes validation and LLM classification per the Class Interface Contract.
This module is the implementation of the service API layer described in Gate 2.

Usage:
    from classifier import classify_document
    from models import ClassificationRequest, OversizeHandling

    result = classify_document(
        request=ClassificationRequest(
            contract_version="1.0.0",
            request_id="req-001",
            tenant_id="tenant-a",
            document_id="doc-001",
            taxonomy_version="1.0.0",
            model_id="claude-sonnet-4-6",
            document_text="Please find attached our invoice for services rendered...",
        )
    )
    print(result.to_dict())
"""

from __future__ import annotations

import logging
import os
from typing import Optional

import anthropic

from llm_client import classify
from models import (
    ClassificationRequest,
    ClassificationResult,
    Outcome,
    ReasonCode,
)
from validation import build_rejection_result, validate_request

logger = logging.getLogger(__name__)


def _get_client() -> anthropic.Anthropic:
    """
    Return an Anthropic client.

    API key is read from ANTHROPIC_API_KEY environment variable.
    Never hardcode credentials.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY environment variable is not set. "
            "Set it before running the classifier."
        )
    return anthropic.Anthropic(api_key=api_key)


def classify_document(
    request: ClassificationRequest,
    client: Optional[anthropic.Anthropic] = None,
) -> ClassificationResult:
    """
    Classify a document per the Class Interface Contract v1.0.0.

    Steps:
    1. Validate input against the contract (no LLM call if invalid)
    2. Call the LLM per the Prompt Contract
    3. Return a ClassificationResult with explicit outcome

    All outcomes are explicit: success, fallback_human, or error_no_route.
    No silent routing.
    """
    logger.info(
        "classify_document called",
        extra={
            "request_id": request.request_id,
            "document_id": request.document_id,
            "tenant_id": request.tenant_id,
            "taxonomy_version": request.taxonomy_version,
            "model_id": request.model_id,
        },
    )

    # Step 1: Validate input
    validation_error = validate_request(request)
    if validation_error is not None:
        # Empty document routes to fallback_human per Gate 2 class boundary behavior
        outcome = (
            Outcome.FALLBACK_HUMAN
            if validation_error.reason_code == ReasonCode.EMPTY_DOCUMENT
            else Outcome.ERROR_NO_ROUTE
        )
        return build_rejection_result(request, validation_error, outcome)

    # Step 2: Classify via LLM
    if client is None:
        client = _get_client()

    return classify(request, client)
