# Examples

End-to-end walkthroughs of the AI Orchestrator framework applied to real, bounded systems.

Each example runs a complete project through all seven phases, producing real artifacts at each gate. The artifacts produced become the reference implementation for the templates in `../templates/`.

---

## Worked Examples

### document-classification-agent

A system that classifies incoming documents into a predefined taxonomy and routes them to the appropriate downstream workflow. Uses an LLM at runtime (Runtime AI deployment mode — Both).

**Gate artifacts:**

| Artifact | Status |
|---|---|
| `gate-0.md` — Concept Validation | Complete |
| `gate-1.md` — Feasibility Analysis | Complete |
| `gate-2.md` — Architecture and Design | Complete |
| `contracts/class-interface-contract.md` | Complete |
| `contracts/prompt-contract-classification.md` | Complete |
| `adr/ADR-001-model-selection.md` | Complete |
| `gate-3.md` — Technical Verification | In progress |
| `gate-4.md` — Operational Readiness | Planned |
| `gate-5.md` — Post-Deploy Validation | Planned |

**Implementation:**

```
document-classification-agent/
├── README.md
├── requirements.txt
└── src/
    ├── taxonomy.py        # Versioned taxonomy loader and label definitions
    ├── models.py          # Request and result dataclasses per contract schemas
    ├── validation.py      # Input validation before any LLM call
    ├── llm_client.py      # Anthropic API call with retry and fallback logic
    ├── classifier.py      # Main entry point
    └── test_classifier.py # Test suite covering Gate 3 verification requirements
```

---

## How to Read an Example

Each example follows the same structure:

```
examples/[name]/
├── README.md               # Summary and what the example demonstrates
├── gate-0.md               # Completed Gate 0 worksheet
├── gate-1.md               # Completed Gate 1 worksheet
├── gate-2.md               # Completed Gate 2 worksheet
├── gate-3.md               # Completed Gate 3 worksheet
├── gate-4.md               # Completed Gate 4 worksheet
├── gate-5.md               # Completed Gate 5 worksheet
├── contracts/
│   ├── class-interface-contract.md
│   └── prompt-contract-[name].md
├── adr/
│   └── ADR-001-[decision].md
├── src/                    # Implementation built against the contracts
└── notes.md                # What the example revealed about the framework
```

The `notes.md` file is where the framework is evaluated against the reality of applying it. Gaps, friction points, and decisions the framework did not anticipate well are documented there. These notes feed back into framework iteration.

---

## Contributing an Example

If you have applied this framework to a real project and can share the artifacts in sanitized form, a contributed example is the most useful thing you can add to this repository. See `../CONTRIBUTING.md` for guidelines.

The gate artifacts are more valuable than the implementation. A complete set of gate worksheets and contracts for a real system — even without code — demonstrates the framework in a way that synthetic examples cannot.
