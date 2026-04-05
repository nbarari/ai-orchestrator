# Gate 5: Post-Deploy Validation

**Project:** Document Classification Agent (Worked Example)
**Date:** 2026-04-05
**Author:** ai-orchestrator-framework contributors
**Status:** Accepted

**Gate 0 reference:** `examples/document-classification-agent/gate-0.md`
**Gate 4 reference:** `examples/document-classification-agent/gate-4.md`

Reference: `manual.md` Phase 7.

---

## Validation Loop

### Success Predicate Audit

Did the Success Predicate from Gate 0 evaluate to true under real operating conditions?

**Success Predicate (from Gate 0):**

```
For documents whose gold label is agreed under the approved taxonomy
(per evaluation set or adjudicated queue):

1. Routing accuracy: the predicted primary label matches the gold label
   at or above the agreed threshold on a held-out evaluation set, with
   bounded error on safety-critical categories if defined in Gate 2.

2. Operational safety: when the model output is invalid, incomplete, or
   confidence is below threshold, the system does not silently pick a
   workflow; it follows the documented fallback (e.g., default route,
   human queue) without unhandled failures.

3. Traceability: each classification decision is attributable to logged
   inputs (per data boundary), model version, and output, for audit
   and replay.

The composite predicate holds when (1)-(3) are all satisfied over the
evaluation window defined in Phase 7.
```

**Evaluation results:**

| Predicate condition | Result | Evidence | Notes |
|---|---|---|---|
| Routing accuracy ≥ 90% on held-out evaluation set | Not met — not measured | No real API calls or labeled evaluation set in worked example | Primary gap; requires real deployment and labeled data |
| Operational safety: no silent wrong routes | Met (mocked) | 23 tests passing; all failure paths produce explicit fallback_human or error_no_route outcomes | Verified against mocked provider; not yet verified against real provider at volume |
| Traceability: decisions attributable to logged inputs and model version | Met | Structured logging in llm_client.py; all decision points log request_id, model_id, outcome, reason codes; document text hashed per Data Boundary | Verified in implementation; not yet verified in a deployed observability stack |

**Composite predicate evaluation:**

- [ ] All conditions met — Success Predicate is satisfied
- [x] One or more conditions not met — document gap and decision below

**If not fully satisfied:**

```
Condition 1 (routing accuracy) cannot be evaluated without:
- A deployed instance of the classifier making real API calls
- A labeled evaluation set of documents with agreed gold labels
- A measurement run using the pinned taxonomy version and model

This is not a design failure — it is the expected state for a worked
example that demonstrates framework structure without a production system.

For a real deployment: measure top-1 accuracy on the held-out set
within the first operational week. If accuracy is below 90%, return
to Gate 2 to revise accuracy thresholds, prompt structure, or taxonomy
definitions before expanding to full volume.

Conditions 2 and 3 are satisfied at the implementation level. Full
verification requires a deployed observability stack with a production
traffic sample.
```

---

### Adoption

After sufficient usage, do operators and consumers trust the system enough to rely on it?

**Usage period evaluated:** Not applicable — no production deployment

**Signals of adoption:**

```
No real usage to evaluate. For a production deployment, adoption signals
would include:

- Reduction in documents routed manually relative to pre-deployment baseline
- Operator override rate declining over time (operators accepting automated
  classifications rather than correcting them)
- Downstream workflow teams reporting fewer mis-route corrections
- Human review queue handling only genuinely ambiguous documents rather
  than all documents
```

**Signals of non-adoption or distrust:**

```
No real usage to evaluate. Non-adoption signals to watch for in production:

- Operators systematically overriding automated classifications
- Teams bypassing the classifier and routing manually
- Fallback_human rate remaining at or above pre-deployment baseline
  (system provides no net automation)
- Complaints about classification correctness from downstream workflow owners
```

---

## Routine Health and Review

### Class Drift Audit

Is the system still handling the problem class it was designed for?

**Problem Class (from Gate 0):**

```
In scope: Given authoritative text content for a single inbound document
and a known taxonomy, decide which taxonomy label(s) apply for routing
purposes, under volume and latency expectations typical of operational
mailrooms and intake queues. Includes mixed-quality OCR text, short memos,
long attachments, and ambiguous but decidable documents.

Out of scope: Defining or evolving the taxonomy; extracting structured
fields beyond routing needs; guaranteeing legal or regulatory correctness;
classifying non-text modalities; end-to-end workflow execution.
```

**Observed operational behavior:**

```
Not applicable — no production deployment. For a first Gate 5 review,
this section would document whether the intake document types in production
match what Gate 0 described, or whether new document types have appeared
that are adjacent to the class but outside it.

Common drift patterns to watch for:
- Intake begins receiving document types not covered by the taxonomy
  (e.g., multimedia attachments, structured data files)
- Taxonomy evolves without a corresponding re-validation of the classifier
- Volume profile shifts significantly from Gate 1 estimates, changing
  cost and latency assumptions
- New downstream workflows require finer-grained routing than the
  current taxonomy supports
```

**Drift finding:**

- [x] No drift — system handles the documented class (no production data to contradict)
- [ ] Drift identified

```
No drift can be confirmed or denied without production usage. This section
should be completed at the first real operational review, approximately
30 days after production deployment.
```

**Runtime AI — Model version drift:**

Has the underlying model version changed since Gate 2?

- [x] No change — claude-sonnet-4-6 is still the pinned version as of this worked example date

**Model version at Gate 2:** claude-sonnet-4-6
**Current model version:** claude-sonnet-4-6

**Re-validation result:** Not applicable — no version change.

---

### Knowledge Persistence

Have all design artifacts been preserved and updated to reflect current reality?

| Artifact | Current? | Last reviewed | Review trigger met? |
|---|---|---|---|
| Gate 0 — Problem Class Definition | Yes | 2026-04-05 | No trigger events since creation |
| Gate 2 — Class Interface Contract | Yes | 2026-04-05 | No trigger events since creation |
| Gate 2 — Prompt Contracts (Runtime AI) | Yes | 2026-04-05 | No trigger events since creation |
| Gate 2 — Data Boundary Declaration (Runtime AI) | Yes | 2026-04-05 | No trigger events since creation |
| Gate 2 — Human Oversight Model (Runtime AI) | Yes | 2026-04-05 | No trigger events since creation |
| ADRs | Yes | 2026-04-05 | No trigger events since creation |

All artifacts are current as of the worked example date. No trigger events
have occurred that would require revision (no model version change, no
taxonomy change, no volume change, no class-adjacent production findings).

---

### Living Document Protocol

Review is triggered by events, not only by calendar schedule.

**Events that have occurred since the last review:**

- [ ] Model version change
- [ ] Significant volume change
- [ ] New class-adjacent use case discovered in production
- [ ] Team ownership change
- [ ] Class Drift finding
- [ ] Provider behavior change (Runtime AI)
- [ ] Taxonomy change
- [x] None of the above

**Review actions taken:**

```
No trigger events have occurred. No artifact reviews required at this time.

For a production deployment operating over time, the first expected
trigger is model version deprecation by Anthropic. When claude-sonnet-4-6
is deprecated:

1. Open a new ADR selecting a replacement pinned version
2. Re-run behavioral evals against the new version
3. Update Prompt Contract with the new model version
4. Update Class Interface Contract if output behavior changes
5. Complete a Class Drift Audit comparing outputs before and after
6. Update .ai-orchestrator with new gate-5 review date
```

---

## Decommission Gate

The system is not being considered for decommission. This section is not applicable to this worked example review.

**Decision:**

- [x] Continue operating — maintenance cost justified (framework demonstration value)
- [ ] Decommission

---

## Gate Approval

- [ ] Success Predicate evaluated against real operating data — **gap: no production deployment**
- [ ] Adoption signals reviewed — **gap: no production usage**
- [x] Class Drift Audit completed — **no drift detectable without production data; documented**
- [x] Model version drift checked and re-validated if applicable — **no version change**
- [x] All design artifacts confirmed current
- [x] Living Document Protocol events reviewed and acted on — **no trigger events**
- [x] Decommission decision made explicitly — **continue operating**

**Approved by:** ai-orchestrator-framework contributors (worked example)
**Date:** 2026-04-05

**Notes:**

This Gate 5 is a **worked example**. Two checklist items are not satisfied
because they require real production usage data:

1. Success Predicate evaluation against real operating data — cannot be
   completed without a deployed system, real API calls, and a labeled
   evaluation set. Condition 1 (routing accuracy) is the primary gap.
   Conditions 2 and 3 are verified at the implementation level.

2. Adoption signals — cannot be evaluated without real operators and
   consumers using the system over time.

These are the expected gaps for a worked example. A production Gate 5
is conducted 30-60 days after deployment with real usage data.

The framework observation from this gate: Gate 5 is the gate that proves
whether Gates 0-4 produced a system worth operating. Without real usage
data it can only confirm that the artifacts are current and the design
intent is intact. The most important section — the Success Predicate
Audit — requires the numbers that the worked example cannot provide.
This is correct: a framework that can be fully validated without a real
system would not be testing the right things.

The worked example demonstrates what Gate 5 asks, how it is structured,
and what evidence a real deployment must produce. That is its purpose.

See `examples/notes.md` for observations on Gate 5 friction points.
