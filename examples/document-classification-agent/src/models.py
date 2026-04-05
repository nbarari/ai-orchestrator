"""
models.py

Request and result dataclasses matching the Class Interface Contract v1.0.0.

Schemas are defined in:
  examples/document-classification-agent/contracts/class-interface-contract.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


CONTRACT_VERSION = "1.0.0"
PINNED_MODEL_ID = "claude-sonnet-4-6"

# Gate 2 thresholds
CONFIDENCE_COMMIT_THRESHOLD = 0.65
MAX_LLM_RETRIES = 2  # 3 total attempts
PER_ATTEMPT_TIMEOUT_SECONDS = 30
MIN_DOCUMENT_TEXT_LENGTH = 10  # characters after strip


class Outcome(str, Enum):
    SUCCESS = "success"
    FALLBACK_HUMAN = "fallback_human"
    ERROR_NO_ROUTE = "error_no_route"


class OversizeHandling(str, Enum):
    REJECT = "reject"
    TRUNCATE_HEAD = "truncate_head"
    CHUNK_THEN_AGGREGATE = "chunk_then_aggregate"
    HUMAN_QUEUE = "human_queue"


class ReasonCode(str, Enum):
    INVALID_LLM_OUTPUT = "INVALID_LLM_OUTPUT"
    PROVIDER_TIMEOUT = "PROVIDER_TIMEOUT"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    RATE_LIMITED = "RATE_LIMITED"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    EMPTY_DOCUMENT = "EMPTY_DOCUMENT"
    OVERSIZE_DOCUMENT = "OVERSIZE_DOCUMENT"
    UNKNOWN_TAXONOMY_VERSION = "UNKNOWN_TAXONOMY_VERSION"
    INVALID_MODEL_ID = "INVALID_MODEL_ID"
    REQUIRES_HUMAN_REVIEW = "REQUIRES_HUMAN_REVIEW"
    INVALID_CONTRACT_VERSION = "INVALID_CONTRACT_VERSION"


@dataclass
class ClassificationRequest:
    """
    Valid input per Class Interface Contract v1.0.0.

    Required fields: contractVersion, requestId, tenantId, documentId,
    taxonomyVersion, modelId, documentText.
    """
    contract_version: str
    request_id: str
    tenant_id: str
    document_id: str
    taxonomy_version: str
    model_id: str
    document_text: str
    idempotency_key: Optional[str] = None
    language_hint: Optional[str] = None
    oversize_handling: Optional[OversizeHandling] = None


@dataclass
class ClassificationResult:
    """
    Valid output per Class Interface Contract v1.0.0.

    Required fields: contractVersion, requestId, taxonomyVersion,
    modelId, outcome.
    """
    contract_version: str
    request_id: str
    taxonomy_version: str
    model_id: str
    outcome: Outcome
    primary_label: Optional[str] = None
    confidence: Optional[float] = None
    requires_human_review: bool = False
    reason_codes: list[ReasonCode] = field(default_factory=list)
    trace_id: Optional[str] = None

    def to_dict(self) -> dict:
        result = {
            "contractVersion": self.contract_version,
            "requestId": self.request_id,
            "taxonomyVersion": self.taxonomy_version,
            "modelId": self.model_id,
            "outcome": self.outcome.value,
        }
        if self.primary_label is not None:
            result["primaryLabel"] = self.primary_label
        if self.confidence is not None:
            result["confidence"] = self.confidence
        if self.requires_human_review:
            result["requiresHumanReview"] = self.requires_human_review
        if self.reason_codes:
            result["reasonCodes"] = [rc.value for rc in self.reason_codes]
        if self.trace_id is not None:
            result["traceId"] = self.trace_id
        return result
