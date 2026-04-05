# Gate 4: Operational Readiness

**Project:** Document Classification Agent (Worked Example)
**Date:** 2026-04-05
**Author:** ai-orchestrator-framework contributors
**Status:** Accepted

**Gate 0 reference:** `examples/document-classification-agent/gate-0.md`
**Gate 3 reference:** `examples/document-classification-agent/gate-3.md`

Reference: `manual.md` Phase 6.

**Stop Criteria:** Halt if runbooks are untested, if the recovery and rollback
procedure fails rehearsal, or if any Gate 3 verification signal is not confirmed Green.

**Note:** High-impact downstream changes identified as irreversible in Gate 2
are executed only after this gate is approved — not before. For this worked
example, no irreversible downstream changes are executed because no production
system is deployed.

---

## Sustainability and Controls

### Standard Operating Procedures

Are runbooks written and tested by someone other than the author?

| Runbook | Covers | Tested by | Date tested | Result |
|---|---|---|---|---|
| Classification failure runbook | Provider unavailable, rate limited, invalid output; diagnosis via request_id; escalation path to human queue | Not yet tested by non-author | Not yet | Gap — see notes |
| Taxonomy update runbook | Deploying a new taxonomy version; validating classifier behavior; rollback to prior version if accuracy degrades | Not yet tested by non-author | Not yet | Gap — see notes |
| Model version change runbook | Pinning a new model version in ADR; re-running behavioral evals; updating Prompt Contract; completing Class Drift Audit | Not yet tested by non-author | Not yet | Gap — see notes |

**Gaps:**

```
All three runbooks are described at the level of intent rather than
step-by-step operational procedures. None have been tested by a person
other than the author. This is the primary blocking gap for Gate 4 in
a production deployment.

For the worked example, the runbook content is documented here to
demonstrate what a production runbook covers. A real deployment requires:
1. Step-by-step procedures with exact commands, API calls, and decision points
2. A second engineer or operator to execute each runbook independently
3. Documented results from that rehearsal

The framework observation from this gap: Gate 4 has the highest proportion
of requirements that cannot be satisfied without a deployed system and a
second person. It is the most operationally dependent gate.
```

---

### Operational Controls

Are automated limits or kill switches active for variable operational spend?

| Control | Type | Active? | Threshold | Notes |
|---|---|---|---|---|
| Anthropic API spend limit | Cost circuit-breaker | No — not implemented in worked example | TBD per org policy | Required before production deployment |
| LLM call timeout | Rate limit (per-attempt) | Yes — in llm_client.py | 30 seconds per attempt | Implemented; not infrastructure-enforced |
| Max retry limit | Rate limit | Yes — in llm_client.py | 3 total attempts | Implemented; not infrastructure-enforced |

**Runtime AI — Cost circuit-breaker:**

Is there an automated limit that prevents runaway LLM spend before it becomes a financial incident?

- [ ] Yes — threshold: [value] per [period]
- [x] No — not implemented in the worked example

```
The worked example has no spend monitoring or automated circuit-breaker.
A production deployment requires a spend limit configured at the Anthropic
account level or via a proxy layer that can halt API calls when a daily
or monthly threshold is exceeded.

The implementation has client-side retry limits (MAX_LLM_RETRIES = 2) and
per-attempt timeouts (PER_ATTEMPT_TIMEOUT_SECONDS = 30) which bound per-request
cost, but these do not prevent accumulating cost from high volume or from a
bug that causes repeated classification attempts on the same documents.
```

**Runtime AI — Privilege scope enforcement:**

Are privilege scopes of agentic components enforced at the infrastructure level?

- [x] Yes — partially

```
The classification service makes outbound API calls to Anthropic only.
It does not have direct database write access, deployment permissions, or
access grants. The scope is limited by the implementation: the classifier
accepts a request and returns a result; it does not commit downstream routes
autonomously (Supervised oversight per Gate 2 Human Oversight Model).

In production, this should be enforced at the infrastructure level via:
- Network policy restricting egress to Anthropic API endpoints only
- IAM roles or service accounts with minimum required permissions
- No direct write access to downstream workflow systems from the classifier
```

**Runtime AI — Independent halt capability:**

Can AI-triggered state changes be halted independently of the main system?

- [x] Yes — mechanism: fallback_human outcome

```
The system never autonomously commits irreversible downstream routes.
All outcomes that would trigger downstream workflow commits produce either
a success result requiring supervised human approval or a fallback_human
result that routes to a human queue.

To halt autonomous AI action: suspend the supervised approval step.
No downstream workflows execute without human confirmation in the initial
deployment configuration.

In a future autonomous routing configuration, a kill switch that sets all
classification outcomes to fallback_human regardless of model output would
be required. This should be implemented as a feature flag before any
autonomous routing is enabled.
```

---

## Handoff and Rollback

### Rehearsal

Has the recovery and rollback procedure been rehearsed in a non-production environment?

- [ ] Yes — date rehearsed: [date] | rehearsed by: [not the original author]
- [x] No — not completed; known gap in worked example

**Rehearsal result:**

```
No non-production deployment exists for this worked example. The rollback
procedure for a production deployment would cover:

1. Provider outage: verify fallback_human routing is active; confirm human
   queue is processing; monitor queue depth; restore when provider recovers.

2. Taxonomy update rollback: revert taxonomyVersion pin in service config;
   confirm classifier is using prior version; validate with a known-good
   test document.

3. Model version rollback: revert modelId pin; update ADR-001 to note
   the rollback; re-run behavioral evals against the reverted version.

4. Deployment rollback: redeploy prior container image or function version;
   verify health check; confirm request routing is restored.

A production Gate 4 requires each of these procedures to be rehearsed
by a person other than the original author, with documented results.
```

---

### Independence

Does the named system owner have sufficient context to operate this system without assistance from the original builder?

**Named owner:** ai-orchestrator-framework contributors (worked example)

**Evidence of independence:**

```
Not confirmed — no second person has independently operated this system.

For a production deployment, independence would be confirmed by:
- A named individual (not the original author) successfully diagnosing a
  simulated failure using only the runbook and structured logs
- That individual successfully executing the taxonomy update runbook
  in a non-production environment
- Documented result from that exercise

The README at examples/document-classification-agent/README.md and the
structured logging in the implementation provide sufficient context for
a qualified engineer to operate the system. The gap is the absence of a
rehearsed confirmation.
```

---

### Gate 3 Signal Confirmation

All Gate 3 verification signals must be Green before irreversible downstream changes are executed.

| Gate 3 signal | Status |
|---|---|
| Class coverage verified | Green |
| Contract verification passed | Green |
| Prompt Contract outputs verified (Runtime AI) | Green |
| Health signals verified | Green |
| Stress test completed | Not Green — gap documented in gate-3.md |
| Behavioral evals passed (Runtime AI) | Green (with documented gaps on real accuracy measurement) |
| Self-service diagnosis confirmed | Green (structured logging sufficient; formal runbook not yet tested) |
| Traceability verified | Green |
| Logging compliant with Data Boundary (Runtime AI) | Green |

**All signals Green before proceeding:**

- [ ] Confirmed — all signals Green
- [x] Not confirmed — stress test not completed; no production deployment

```
For this worked example, irreversible downstream changes are not executed
because no production system is deployed. The gate documents operational
readiness requirements for a future real deployment.

A production Gate 4 is blocked until:
1. Stress test is completed against the real provider at Gate 1 volume estimates
2. Runbooks are written and tested by a non-author
3. Rollback rehearsal is completed
```

---

### Irreversible Commitment Execution

List the high-impact downstream changes identified in Gate 2 that are executed at this gate.

| Commitment | Executed? | Date | Notes |
|---|---|---|---|
| Downstream supervised route commit | No | N/A | No production deployment; supervised commits require human approval when deployed |
| Archival / retention path trigger | No | N/A | No production deployment |
| Irreversible notifications tied to label | No | N/A | No production deployment |

---

## Gate Approval

- [ ] All runbooks written and tested by non-author — **gap: runbooks at intent level only**
- [ ] Cost circuit-breaker active (Runtime AI) — **gap: not implemented**
- [x] Privilege scopes enforced at infrastructure level (Runtime AI) — **partially: scope limited by implementation design**
- [x] Independent halt capability confirmed (Runtime AI) — **fallback_human mechanism; supervised oversight prevents autonomous commit**
- [ ] Rollback rehearsal completed successfully — **gap: no non-production deployment**
- [ ] Named owner can operate independently — **gap: not confirmed by rehearsal**
- [ ] All Gate 3 signals confirmed Green — **gap: stress test not completed**
- [x] Irreversible commitments executed only after signals confirmed — **no irreversible commits in worked example**

**Approved by:** ai-orchestrator-framework contributors (worked example)
**Date:** 2026-04-05

**Notes:**

This Gate 4 is a **worked example**. Four checklist items are not satisfied
because they require a deployed system, a second operator, and real
infrastructure that do not exist in this repository artifact.

The gaps are:
1. Runbooks at intent level only; not tested by a non-author
2. No cost circuit-breaker at infrastructure level
3. No rollback rehearsal in a non-production environment
4. Named owner independence not confirmed by rehearsal

These are the expected gaps for Minimum Viable Coverage. A production
deployment must resolve all four before Gate 4 can be approved.

The framework observation from this gate: Gate 4 has the highest density
of requirements that depend on organizational process rather than code.
Runbook testing, rollback rehearsal, and operator independence confirmation
require time, a second person, and a deployed environment. They cannot be
automated or approximated. This is intentional — Gate 4 exists precisely
because operational readiness is not provable from code review alone.

See `examples/notes.md` for observations on Gate 4 friction points.
