# Templates

Fillable worksheets for each gate in the AI Orchestrator SDLC.

Each template corresponds to a phase in `manual.md`. Complete the worksheet before requesting gate approval. The completed worksheet becomes the gate artifact.

| Template | Phase | Purpose |
|---|---|---|
| `gate-0-concept.md` | Phase 1 | Problem Class Definition, Success Predicate, AI Deployment Mode |
| `gate-1-feasibility.md` | Phase 2 | Environmental mapping, cost model, class coverage |
| `gate-2-design.md` | Phase 3 | Class Interface Contract, Data Boundary, Human Oversight Model |
| `adr-template.md` | Phase 3 (ongoing) | Architecture Decision Records |
| `prompt-contract.md` | Phase 3 (Runtime AI) | LLM call input/output contract |

## Usage

Copy the relevant template into your project's `docs/` directory and fill it out. Use the GitHub issue templates in `.github/ISSUE_TEMPLATE/` to open gate review issues that reference the completed worksheet.

Completed worksheets are living documents. The Living Document Protocol in Phase 7 defines the events that trigger a review and update of each artifact.
