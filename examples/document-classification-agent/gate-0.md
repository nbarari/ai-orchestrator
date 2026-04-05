# Gate 0: Concept Validation

**Project:** Document Classification Agent (Worked Example)
**Date:** 2026-04-05
**Author:** ai-orchestrator-framework contributors
**Status:** Approved

Reference: `manual.md` Phase 1.

---

## Problem Class Definition

### Problem Class

What is the bounded category of problems this system is designed to handle?

State this without referencing a solution. Be explicit about what falls outside the class. A useful test: can you describe a problem that is adjacent to the class but explicitly excluded?

**In scope:**

```
Organizations receive a steady stream of unstructured or semi-structured text documents that must be sorted against a fixed, versioned taxonomy so each item can be handed off to the correct downstream process (review, fulfillment, archival, escalation, etc.). The problem class is: given authoritative text content for a single inbound document and a known taxonomy, decide which taxonomy label(s) apply for routing purposes, under volume and latency expectations typical of operational mailrooms and intake queues.

Adjacent but in scope: mixed-quality OCR text, short memos, long attachments, and documents where the correct label is ambiguous but still plausibly decidable from the text plus the taxonomy definitions.
```

**Out of scope (Anti-Scope):**

```
- Defining or evolving the taxonomy itself (labels, hierarchy, business rules) as part of classification; that is governance and product scope, not this system’s problem class.
- Extracting structured fields (amounts, dates, parties) beyond what is required to choose a route; that is a different problem class (information extraction).
- Guaranteeing legal or regulatory correctness of a decision; human oversight and policy sit outside pure “pick a label.”
- Classifying non-text modalities (images, audio, video) without a prior text representation.
- End-to-end workflow execution after routing; downstream systems own those effects.
```

---

### Success Predicate

What logical condition determines whether the system is correctly handling its problem class?

The predicate may be composite. If it cannot be evaluated against observable system behavior, the class definition is not yet complete.

```
For documents whose gold label is agreed under the approved taxonomy (per evaluation set or adjudicated queue):

1. Routing accuracy: the predicted primary label matches the gold label at or above the agreed threshold on a held-out evaluation set, with bounded error on safety-critical categories if defined in Gate 2.
2. Operational safety: when the model output is invalid, incomplete, or confidence is below threshold, the system does not silently pick a workflow; it follows the documented fallback (e.g., default route, human queue) without unhandled failures.
3. Traceability: each classification decision is attributable to logged inputs (per data boundary), model version, and output, for audit and replay.

The composite predicate holds when (1)–(3) are all satisfied over the evaluation window defined in Phase 7.

Threshold deferral (explicit): Primary-label accuracy threshold, confidence and fallback thresholds, and definitions of safety-critical categories are set in Gate 2. Minimum acceptable accuracy is TBD based on downstream workflow risk. Until those values are fixed, condition (1) is not yet numerically evaluable; the predicate shape is complete, and full evaluation begins once Gate 2 pins the numbers.
```

**How will this predicate be evaluated in Phase 7?**

```
- Batch evaluation on a versioned labeled set (periodic re-run when taxonomy or model changes).
- Live monitoring: distribution of labels, confidence scores, fallback rate, and error budgets; incident review when thresholds breach.
- Spot checks or adjudication queue metrics where human review is the reference for ambiguous cases.
```

---

### Evidence

What observable signals confirm that this problem class exists and is not merely perceived?

Acceptable evidence: logs showing frequency, support tickets, measured time spent, error rates, incident reports. Not acceptable: anecdote or assumption.

```
The signal types below are representative of what a production Gate 0 would cite (logs, tickets, measured time, error rates). This worked example does not attach real system identifiers or datasets; see Gate Approval notes for how that affects the evidence checklist.

- Intake queue metrics: volume of documents awaiting manual triage, median and p95 time-to-route.
- Support or operations tickets citing mis-routed documents or rework after incorrect queue assignment.
- Error rates or rework rates from downstream workflows triggered by wrong routing.
- Measured staff time spent on manual classification where automation is intended to apply.
```

---

### Class Impact

What does an unaddressed instance of this problem class cost at the expected frequency of occurrence?

Quantify where possible: time per instance, error rate, capital cost, risk exposure.

```
Per misrouted or slow-routed document: additional handling time (e.g., tens of minutes of staff time), delayed processing for the recipient workflow, and risk of compliance or service-level breaches when the wrong path delays mandatory actions. At expected intake volume, even a small mis-route rate compounds into full-time equivalent cost and customer-visible latency.
```

---

### Inertia Test

What does the problem class cost if left unaddressed at scale over the mid-to-long term?

```
Manual triage does not scale linearly with volume: backlog grows, SLAs slip, and exception handling becomes the norm. Taxonomy and process drift increase inconsistency. Without a bounded automated classifier, the organization either caps intake or accepts growing operational load and quality variance—undermining the predictability that a fixed taxonomy is meant to provide.
```

---

## AI Deployment Mode

Select one and document the reasoning.

- [ ] **Build-Time Only.** AI assists in writing, testing, or documenting the system. No LLM executes in production.
- [ ] **Runtime.** An LLM executes as part of the live system.
- [x] **Both.** AI is present in both the build process and the live system.

**Reasoning:**

```
The worked example is built with AI-assisted authoring (build-time) while the production path uses an LLM to assign taxonomy labels from text at runtime. This matches how many teams adopt orchestration: accelerated implementation plus live inference. Gate criteria for both build-time quality and runtime operations therefore apply.
```

**Gate criteria activated by this mode:**

For Build-Time Only: verification, structural integrity, documentation discipline.

For Runtime (add to Build-Time): operational cost model, data boundary declaration, provider reliability and fallback, behavioral evals, LLM observability, human oversight model, model version pinning, cost circuit-breaker.

---

## Timing, Origin, and Solution Space

### Root Cause

Why does this problem class exist? Is the gap process-based, technical, organizational, or a knowledge deficit?

```
Volume and variety of inbound documents exceed what static rules and keyword routing can cover without constant maintenance. The gap is primarily technical and process: mapping free-form text to a stable taxonomy at scale requires judgment that traditional rules encode poorly, while purely manual triage does not scale.
```

### Catalyst

What changed recently that makes this class addressable now?

```
LLM-based classification can use taxonomy definitions and document text together in a single inference step, reducing bespoke rule sprawl. Mature APIs, observability patterns, and this framework’s contracts make it practical to deploy with explicit boundaries, fallbacks, and oversight—addressing risks that previously blocked production use.
```

### Solution Space

What tools or systems already handle adjacent problem classes, and why are they insufficient for this one?

| Tool / System | What it handles | Why insufficient |
|---|---|---|
| Rules engines / regex routes | High-precision patterns for stable formats | Brittle when language, layout, or content varies; high maintenance as taxonomy evolves |
| Traditional ML classifiers | Text classification with labeled training data | Require feature engineering and retraining pipelines; weaker zero-shot adaptation to taxonomy wording changes vs. LLM-with-prompt |
| Manual triage queues | Any document | Does not scale; inconsistent under load |
| Full RAG / knowledge systems | Answering questions from corpora | Solves retrieval QA, not authoritative single-label routing against a fixed taxonomy contract |

---

## Gate Approval

- [x] Problem Class is bounded with explicit inclusions and exclusions
- [x] Success Predicate is stated and can be evaluated
- [x] Evidence is observable, not assumed
- [x] AI Deployment Mode is declared with reasoning
- [x] Solution space has been reviewed

**Approved by:** ai-orchestrator-framework contributors (worked example)
**Date:** 2026-04-05

**Notes:**

This worksheet is a **worked example** for the framework. The Evidence section lists **types** of observable signals appropriate to a real deployment; it does not cite production logs, ticket IDs, or measured figures. For a live system, replace those placeholders with concrete references (systems, time ranges, metrics) so the evidence checklist is satisfied by verifiable data. The checklist item “Evidence is observable, not assumed” is checked here on the basis that the **categories** of evidence are operational and non-anecdotal—not on the basis of attached real telemetry in this repository artifact.
