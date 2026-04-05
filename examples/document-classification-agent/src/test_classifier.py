"""
test_classifier.py

Test suite for the Document Classification Agent.

Covers the Gate 3 verification requirements:
- Class coverage: in-class and boundary cases
- Contract verification: input and output schema
- Behavioral eval criteria from Gate 2

Run with:
    pip install pytest anthropic
    pytest test_classifier.py -v
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from classifier import classify_document
from models import (
    CONTRACT_VERSION,
    PINNED_MODEL_ID,
    ClassificationRequest,
    Outcome,
    OversizeHandling,
    ReasonCode,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_request(**overrides) -> ClassificationRequest:
    defaults = dict(
        contract_version=CONTRACT_VERSION,
        request_id="req-test-001",
        tenant_id="tenant-test",
        document_id="doc-test-001",
        taxonomy_version="1.0.0",
        model_id=PINNED_MODEL_ID,
        document_text="Please find attached our invoice #1234 for services rendered in March.",
    )
    defaults.update(overrides)
    return ClassificationRequest(**defaults)


def mock_llm_response(primary_label_id: str, confidence: float = 0.9) -> MagicMock:
    """Return a mock Anthropic client that produces a valid contract response."""
    content = json.dumps({
        "primaryLabelId": primary_label_id,
        "confidence": confidence,
        "shortRationale": "Test rationale.",
    })
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text=content)]
    mock_message.usage = MagicMock(input_tokens=100, output_tokens=50)

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_message
    return mock_client


# ---------------------------------------------------------------------------
# Input validation — contract rejection criteria
# ---------------------------------------------------------------------------

class TestInputValidation:

    def test_wrong_contract_version_returns_error_no_route(self):
        result = classify_document(make_request(contract_version="0.9.0"))
        assert result.outcome == Outcome.ERROR_NO_ROUTE
        assert ReasonCode.INVALID_CONTRACT_VERSION in result.reason_codes

    def test_wrong_model_id_returns_error_no_route(self):
        result = classify_document(make_request(model_id="some-other-model"))
        assert result.outcome == Outcome.ERROR_NO_ROUTE
        assert ReasonCode.INVALID_MODEL_ID in result.reason_codes

    def test_unknown_taxonomy_version_returns_error_no_route(self):
        result = classify_document(make_request(taxonomy_version="99.0.0"))
        assert result.outcome == Outcome.ERROR_NO_ROUTE
        assert ReasonCode.UNKNOWN_TAXONOMY_VERSION in result.reason_codes

    def test_empty_document_text_returns_fallback_human(self):
        result = classify_document(make_request(document_text=""))
        assert result.outcome == Outcome.FALLBACK_HUMAN
        assert ReasonCode.EMPTY_DOCUMENT in result.reason_codes

    def test_whitespace_only_document_returns_fallback_human(self):
        result = classify_document(make_request(document_text="   \n  \t  "))
        assert result.outcome == Outcome.FALLBACK_HUMAN
        assert ReasonCode.EMPTY_DOCUMENT in result.reason_codes

    def test_below_minimum_length_returns_fallback_human(self):
        result = classify_document(make_request(document_text="hi"))
        assert result.outcome == Outcome.FALLBACK_HUMAN
        assert ReasonCode.EMPTY_DOCUMENT in result.reason_codes

    def test_no_llm_call_on_validation_failure(self):
        """Validation failures must not call the LLM."""
        with patch("classifier.classify") as mock_classify:
            classify_document(make_request(contract_version="0.9.0"))
            mock_classify.assert_not_called()


# ---------------------------------------------------------------------------
# Successful classification — in-class cases
# ---------------------------------------------------------------------------

class TestSuccessfulClassification:

    def test_invoice_document_returns_success(self):
        client = mock_llm_response("invoice", confidence=0.95)
        result = classify_document(make_request(), client=client)
        assert result.outcome == Outcome.SUCCESS
        assert result.primary_label == "invoice"
        assert result.confidence == 0.95

    def test_contract_document_returns_success(self):
        client = mock_llm_response("contract", confidence=0.88)
        result = classify_document(
            make_request(
                document_text="This service agreement is entered into between Party A and Party B."
            ),
            client=client,
        )
        assert result.outcome == Outcome.SUCCESS
        assert result.primary_label == "contract"

    def test_result_contains_required_fields(self):
        client = mock_llm_response("report", confidence=0.91)
        result = classify_document(make_request(), client=client)
        d = result.to_dict()
        assert d["contractVersion"] == CONTRACT_VERSION
        assert "requestId" in d
        assert "taxonomyVersion" in d
        assert "modelId" in d
        assert "outcome" in d


# ---------------------------------------------------------------------------
# Boundary cases — class boundary behavior per Gate 2
# ---------------------------------------------------------------------------

class TestClassBoundaryBehavior:

    def test_low_confidence_routes_to_fallback_human(self):
        """Confidence below 0.65 must not produce an automated commit."""
        client = mock_llm_response("invoice", confidence=0.50)
        result = classify_document(make_request(), client=client)
        assert result.outcome == Outcome.FALLBACK_HUMAN
        assert ReasonCode.LOW_CONFIDENCE in result.reason_codes
        # Label is present for human review context but no automated route
        assert result.primary_label == "invoice"

    def test_requires_human_review_label_routes_to_fallback(self):
        """Labels marked requires_human_review in taxonomy must route to human."""
        client = mock_llm_response("regulated", confidence=0.99)
        result = classify_document(make_request(), client=client)
        assert result.outcome == Outcome.FALLBACK_HUMAN
        assert result.requires_human_review is True
        assert ReasonCode.REQUIRES_HUMAN_REVIEW in result.reason_codes

    def test_invalid_label_in_llm_response_retries_then_falls_back(self):
        """LLM returning a label not in the taxonomy triggers retry then fallback."""
        content = json.dumps({
            "primaryLabelId": "not-a-real-label",
            "confidence": 0.9,
        })
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text=content)]
        mock_message.usage = MagicMock(input_tokens=100, output_tokens=20)

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_message

        result = classify_document(make_request(), client=mock_client)
        assert result.outcome == Outcome.FALLBACK_HUMAN
        assert ReasonCode.INVALID_LLM_OUTPUT in result.reason_codes
        # Should have retried MAX_LLM_RETRIES + 1 = 3 total attempts
        assert mock_client.messages.create.call_count == 3

    def test_invalid_json_response_retries_then_falls_back(self):
        """LLM returning non-JSON triggers retry then fallback."""
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="I cannot classify this document.")]
        mock_message.usage = MagicMock(input_tokens=100, output_tokens=10)

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_message

        result = classify_document(make_request(), client=mock_client)
        assert result.outcome == Outcome.FALLBACK_HUMAN
        assert ReasonCode.INVALID_LLM_OUTPUT in result.reason_codes


# ---------------------------------------------------------------------------
# Provider failure — per Prompt Contract and Gate 2 Failure Mode Registry
# ---------------------------------------------------------------------------

class TestProviderFailure:

    def test_timeout_returns_fallback_human(self):
        import anthropic as ant
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = ant.APITimeoutError(request=MagicMock())
        result = classify_document(make_request(), client=mock_client)
        assert result.outcome == Outcome.FALLBACK_HUMAN
        assert ReasonCode.PROVIDER_TIMEOUT in result.reason_codes

    def test_connection_error_returns_fallback_human(self):
        import anthropic as ant
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = ant.APIConnectionError(request=MagicMock())
        result = classify_document(make_request(), client=mock_client)
        assert result.outcome == Outcome.FALLBACK_HUMAN
        assert ReasonCode.PROVIDER_UNAVAILABLE in result.reason_codes

    def test_rate_limit_returns_fallback_human(self):
        import anthropic as ant
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = ant.RateLimitError(
            message="rate limited",
            response=MagicMock(status_code=429, headers={}),
            body={},
        )
        result = classify_document(make_request(), client=mock_client)
        assert result.outcome == Outcome.FALLBACK_HUMAN
        assert ReasonCode.RATE_LIMITED in result.reason_codes

    def test_no_success_outcome_on_provider_failure(self):
        """Provider failure must never produce a success outcome."""
        import anthropic as ant
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = ant.APIConnectionError(request=MagicMock())
        result = classify_document(make_request(), client=mock_client)
        assert result.outcome != Outcome.SUCCESS


# ---------------------------------------------------------------------------
# Contract output verification
# ---------------------------------------------------------------------------

class TestOutputContract:

    def test_output_contains_contract_version(self):
        client = mock_llm_response("invoice")
        result = classify_document(make_request(), client=client)
        assert result.contract_version == CONTRACT_VERSION

    def test_output_model_id_matches_pinned(self):
        client = mock_llm_response("invoice")
        result = classify_document(make_request(), client=client)
        assert result.model_id == PINNED_MODEL_ID

    def test_output_taxonomy_version_matches_request(self):
        client = mock_llm_response("invoice")
        result = classify_document(make_request(taxonomy_version="1.0.0"), client=client)
        assert result.taxonomy_version == "1.0.0"

    def test_success_outcome_has_primary_label(self):
        client = mock_llm_response("invoice")
        result = classify_document(make_request(), client=client)
        if result.outcome == Outcome.SUCCESS:
            assert result.primary_label is not None

    def test_to_dict_matches_contract_schema(self):
        client = mock_llm_response("invoice", confidence=0.92)
        result = classify_document(make_request(), client=client)
        d = result.to_dict()
        # Required fields per contract
        for field in ["contractVersion", "requestId", "taxonomyVersion", "modelId", "outcome"]:
            assert field in d, f"Missing required field: {field}"
        # outcome must be one of the contract enum values
        assert d["outcome"] in ["success", "fallback_human", "error_no_route"]
