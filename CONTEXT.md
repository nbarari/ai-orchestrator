# Session Context

This file provides handoff context for new Claude sessions working on this repo.
It is not part of the framework — it is a working document for the project itself.

---

## What This Repo Is

The ai-orchestrator-framework is an SDLC framework for non-coding architects
who direct AI-assisted development. It is built around problem class definitions,
gate-based phase progression, and IDE integration via Cursor rules and CLAUDE.md.

The framework is designed for people who do not write code but need to specify
systems precisely enough that AI can safely build them.

---

## Current State

Version: v0.1 — complete
Active milestone: v0.2 — Worked Example

All framework documents, templates, IDE rules, GitHub integration, and appendix
files are committed and validated. See the GitHub issues list for v0.2 scope.

---

## What Needs to Be Done Next

The immediate work is the worked example for a document classification agent:

```
examples/document-classification-agent/
├── gate-0.md          ← start here
├── gate-1.md
├── gate-2.md
├── contracts/
│   ├── class-interface-contract.md
│   └── prompt-contract-classification.md
├── adr/
│   └── ADR-001-model-selection.md
└── notes.md           ← already exists, captures validation gaps
```

Use `templates/gate-0-concept.md` as the base for gate-0.md.
Use `templates/gate-1-feasibility.md` as the base for gate-1.md.
Use `templates/gate-2-design.md` as the base for gate-2.md.
Use `templates/prompt-contract.md` as the base for the prompt contract.
Use `templates/adr-template.md` as the base for the ADR.

---

## The System Being Documented

A document classification agent that:
- Accepts incoming documents (text content)
- Classifies them into a predefined taxonomy
- Routes classified documents to the appropriate downstream workflow

This is a Runtime AI system — an LLM executes the classification in production.
AI Deployment Mode: Both (AI assists in build, LLM executes at runtime).

---

## Key Decisions Already Made

- AI Deployment Mode for the example: Both
- Model: claude-sonnet-4-6 (to be documented formally in ADR-001)
- The worked example is the reference implementation for the templates directory
- The example should be realistic enough to exercise all Runtime AI gate criteria

---

## Known Issues

Cursor intercept rules do not reliably halt direct imperative prompts such as
"Write an ADR for..." or "Create a schema for...". Use indirect phrasing instead:
- "I need to document the decision to..."
- "Help me think through the contract for..."
- "I need to define the shape of..."

See examples/notes.md for full detail and workaround.

---

## How to Work on This Repo

Read CLAUDE.md first. It defines the gate criteria, Task-Level Gate questions,
and file paths that apply to all work in this repo.

The .ai-orchestrator config file declares the current phase and deployment mode.

Do not begin implementation of any gate artifact until the prior gate worksheet
is complete. Gate 0 must exist before Gate 1, Gate 1 before Gate 2, and so on.