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

Version: v0.2 — Worked Example (in progress)
Previous: v0.1 — complete

Completed in v0.1:
- Framework documents: manual.md, curriculum.md, README.md
- All gate worksheet templates (Gates 0-5), ADR template, prompt contract template
- IDE integration: Cursor rules, CLAUDE.md, GitHub Copilot instructions
- GitHub integration: issue templates, PR template
- Appendix: glossary, rigor-by-risk, deployment mode reference

Completed in v0.2 so far:
- examples/document-classification-agent/gate-0.md
- examples/document-classification-agent/gate-1.md
- examples/document-classification-agent/gate-2.md
- examples/document-classification-agent/contracts/class-interface-contract.md
- examples/document-classification-agent/contracts/prompt-contract-classification.md
- examples/document-classification-agent/adr/ADR-001-model-selection.md
- examples/document-classification-agent/src/ (Python implementation, 5 modules)
- examples/document-classification-agent/src/test_classifier.py (23 tests, all passing)
- examples/document-classification-agent/gate-3.md
- examples/notes.md (framework gaps discovered during worked example)

Remaining for v0.2:
- examples/document-classification-agent/gate-4.md
- examples/document-classification-agent/gate-5.md

---

## Roadmap

| Version | Focus | Status |
|---|---|---|
| v0.1 | Foundation — documents, templates, IDE integration | Complete |
| v0.2 | Worked Example — document classification agent end-to-end | In progress |
| v0.3 | Gate Interview Agent — conversational gate facilitation via Anthropic API | Planned |
| v0.4 | CLI and Validation — gate enforcement tooling | Planned |
| v1.0 | MCP Server — framework as queryable tools for Cursor and Claude | Planned |

---

## v0.3 Agent Architecture

The Gate Interview Agent is the most important planned feature. It solves the
primary adoption barrier: completing gate worksheets requires understanding the
framework, knowing the right questions, and having the discipline to write
before building. The agent removes all three.

How it works:
1. Takes a gate number and project path as input
2. Loads the corresponding gate template and any prior gate artifacts for context
3. Runs a conversation loop using the Anthropic API — asks each section's
   questions, waits for answers, validates completeness
4. Produces a completed gate worksheet and writes it to the correct path
5. Updates .ai-orchestrator to reflect gate status

The system prompt is the manual. The user turn is the conversation.
The output is the artifact.

The agent creates the artifacts that the v0.4 CLI validates. Agent before CLI
is the correct build order.

---

## What Needs to Be Done Next

Complete v0.2 by building Gate 4 and Gate 5 for the document classification agent.

Both gates have known gaps (no deployed system, no real operational data) that
are documented explicitly following the same pattern as Gate 3. The gaps are
framework findings, not failures.

Gate 4 template: templates/gate-4-operational.md
Gate 5 template: templates/gate-5-postdeploy.md
Prior gate for context: examples/document-classification-agent/gate-3.md

After Gate 4 and Gate 5 are committed, v0.2 is complete. Update GitHub
milestones and open v0.3 issues for the Gate Interview Agent.

---

## The Document Classification Agent

A Runtime AI system that:
- Accepts incoming documents (text content)
- Classifies them into a predefined taxonomy
- Routes classified documents to the appropriate downstream workflow

AI Deployment Mode: Both (AI assists in build, LLM executes at runtime)
Model: claude-sonnet-4-6 (documented in ADR-001)
Human oversight: Supervised for initial deployment

Implementation location: examples/document-classification-agent/src/
- taxonomy.py — versioned taxonomy loader
- models.py — request/result dataclasses matching contract schemas
- validation.py — input validation before any LLM call
- llm_client.py — Anthropic API call with retry and fallback logic
- classifier.py — main entry point
- test_classifier.py — 23 tests, all passing

Test results (Gate 3 input):
- 23 passed, 0 failed, 0.93 seconds
- Python 3.14.3, pytest 9.0.2, macOS arm64
- All LLM calls mocked; real API accuracy not yet measured

---

## Key Decisions Already Made

- AI Deployment Mode for the example: Both
- Model: claude-sonnet-4-6 (ADR-001)
- Human oversight: Supervised for initial deployment
- Confidence threshold: 0.65 (below this routes to fallback_human)
- Max LLM retries: 2 (3 total attempts before fallback_human)
- Per-attempt timeout: 30 seconds

---

## Known Issues

Cursor intercept rules do not reliably halt direct imperative prompts such as
"Write an ADR for..." or "Create a schema for...". Use indirect phrasing instead:
- "I need to document the decision to..."
- "Help me think through the contract for..."
- "I need to define the shape of..."

See examples/notes.md for full detail, workaround, and all other framework
gaps discovered during validation and the worked example.

---

## How to Work on This Repo

Read CLAUDE.md first. It defines the gate criteria, Task-Level Gate questions,
and file paths that apply to all work in this repo.

The .ai-orchestrator config file declares the current phase and deployment mode.

Do not begin implementation of any gate artifact until the prior gate worksheet
is complete. Gate 0 must exist before Gate 1, Gate 1 before Gate 2, and so on.

When starting a new session on the worked example, include the immediately
prior gate artifact and gate-0.md in the file references. Do not load the
full gate chain — load gate-0 and gate-N-1 only.
