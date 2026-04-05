"""
taxonomy.py

Versioned taxonomy artifact loader and label definitions.
In production this loads from a config store or versioned blob.
For the worked example, a hardcoded v1.0.0 taxonomy is provided.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TaxonomyLabel:
    id: str
    title: str
    description: str
    requires_human_review: bool = False


# Worked example taxonomy v1.0.0
# In production: load from a versioned artifact store keyed by taxonomyVersion.
_TAXONOMY_V1: dict[str, TaxonomyLabel] = {
    "invoice": TaxonomyLabel(
        id="invoice",
        title="Invoice",
        description=(
            "A document requesting payment for goods or services rendered. "
            "Includes bills, purchase invoices, and vendor payment requests."
        ),
    ),
    "contract": TaxonomyLabel(
        id="contract",
        title="Contract",
        description=(
            "A legally binding agreement between two or more parties. "
            "Includes service agreements, NDAs, and vendor contracts."
        ),
    ),
    "report": TaxonomyLabel(
        id="report",
        title="Report",
        description=(
            "A structured document presenting findings, analysis, or status. "
            "Includes financial reports, audit reports, and status updates."
        ),
    ),
    "correspondence": TaxonomyLabel(
        id="correspondence",
        title="Correspondence",
        description=(
            "General written communication between parties. "
            "Includes emails, letters, memos, and notices."
        ),
    ),
    "regulated": TaxonomyLabel(
        id="regulated",
        title="Regulated Document",
        description=(
            "A document subject to regulatory or compliance requirements. "
            "Always requires human review before routing."
        ),
        requires_human_review=True,
    ),
}

SUPPORTED_VERSIONS: set[str] = {"1.0.0"}


def load_taxonomy(version: str) -> dict[str, TaxonomyLabel]:
    """
    Load a versioned taxonomy artifact.

    Raises ValueError if the version is not supported.
    In production: fetch from versioned config store.
    """
    if version not in SUPPORTED_VERSIONS:
        raise ValueError(
            f"Taxonomy version '{version}' is not supported. "
            f"Supported versions: {sorted(SUPPORTED_VERSIONS)}"
        )
    return _TAXONOMY_V1


def get_labels(version: str) -> list[TaxonomyLabel]:
    """Return ordered list of labels for a taxonomy version."""
    taxonomy = load_taxonomy(version)
    return list(taxonomy.values())


def label_ids(version: str) -> set[str]:
    """Return the set of valid label ids for a taxonomy version."""
    return set(load_taxonomy(version).keys())
