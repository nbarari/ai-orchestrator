"""Local document-type helpers (no network; no LLM in this module)."""

from __future__ import annotations

from enum import Enum
from typing import Final


class DocumentCategory(str, Enum):
    INVOICE = "invoice"
    CONTRACT = "contract"
    REPORT = "report"
    OTHER = "other"


# Phrases first — longer matches are scored the same as short ones; lists are curated to reduce noise.
_KEYWORDS: Final[dict[DocumentCategory, tuple[str, ...]]] = {
    DocumentCategory.INVOICE: (
        "invoice",
        "invoice number",
        "invoice #",
        "bill to",
        "ship to",
        "amount due",
        "total due",
        "balance due",
        "payment due",
        "remit to",
        "subtotal",
        "line item",
        "unit price",
        "po number",
        "purchase order",
        "tax id",
        "vat number",
    ),
    DocumentCategory.CONTRACT: (
        "this agreement",
        "the parties agree",
        "party of the first part",
        "whereas",
        "hereby agrees",
        "governing law",
        "termination for cause",
        "entire agreement",
        "counterparts",
        "effective date",
        "in witness whereof",
        "exhibit a",
        "schedule 1",
    ),
    DocumentCategory.REPORT: (
        "executive summary",
        "table of contents",
        "methodology",
        "findings",
        "recommendations",
        "appendix",
        "quarterly report",
        "annual report",
        "abstract",
        "figure ",
        "table ",
    ),
}

_ORDER: Final[tuple[DocumentCategory, ...]] = (
    DocumentCategory.INVOICE,
    DocumentCategory.CONTRACT,
    DocumentCategory.REPORT,
)


def _normalize(text: str) -> str:
    return " ".join(text.casefold().split())


def classify_document(document: str) -> DocumentCategory:
    """
    Classify plain-text document content into invoice, contract, report, or other.

    Uses deterministic keyword signals (no external services). Ambiguous or empty
    input yields ``other``. Tie scores break in order: invoice, contract, report.
    """
    if not document.strip():
        return DocumentCategory.OTHER

    normalized = _normalize(document)
    scores = {c: 0 for c in _ORDER}
    for category in _ORDER:
        for phrase in _KEYWORDS[category]:
            if phrase in normalized:
                scores[category] += 1

    best = max(scores.values())
    if best == 0:
        return DocumentCategory.OTHER

    for category in _ORDER:
        if scores[category] == best:
            return category

    return DocumentCategory.OTHER
