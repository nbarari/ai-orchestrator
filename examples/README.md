# Examples

End-to-end walkthroughs of the AI Orchestrator framework applied to real, bounded systems.

Each example runs a complete project through all seven phases, producing real artifacts at each gate. The artifacts produced become the reference implementation for the templates in `../templates/`.

---

## Planned Examples

### Example 01: Document Classification Agent (Runtime AI)

A system that classifies incoming documents into a predefined taxonomy and routes them to the appropriate workflow. Small enough to complete in a single example, complex enough to exercise all Runtime AI gate criteria including Prompt Contracts, Data Boundary Declaration, and Human Oversight Model.

Status: In progress.

---

## How to Read an Example

Each example follows the same structure:

```
examples/[name]/
├── README.md               # Summary and what the example demonstrates
├── gate-0.md               # Completed Gate 0 worksheet
├── gate-1.md               # Completed Gate 1 worksheet
├── gate-2.md               # Completed Gate 2 worksheet
├── contracts/
│   ├── class-interface-contract.md
│   └── prompt-contract-[name].md
├── adr/
│   ├── 001-[decision].md
│   └── 002-[decision].md
└── notes.md                # What the example revealed about the framework
```

The `notes.md` file in each example is where the framework is evaluated against the reality of applying it. Gaps, friction points, and decisions that the framework did not anticipate well are documented there. These notes feed back into the framework's own iteration.

---

## Contributing an Example

If you have applied this framework to a real project and can share the artifacts in a sanitized form, a contributed example is the most useful thing you can add to this repository. See `CONTRIBUTING.md` for guidelines.
