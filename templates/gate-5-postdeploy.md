# Gate 5: Post-Deploy Validation

**Project:**
**Date:**
**Author:**
**Status:** Draft / Approved / Superseded

**Gate 0 reference:** `docs/gate-0.md`
**Gate 4 reference:** `docs/gate-4.md`

Reference: `manual.md` Phase 7.

---

## Validation Loop

### Success Predicate Audit

Did the Success Predicate from Gate 0 evaluate to true under real operating conditions?

**Success Predicate (from Gate 0):**

```
[Restate the Success Predicate here. Do not paraphrase — copy it exactly so
the evaluation is unambiguous.]
```

**Evaluation results:**

| Predicate condition | Result | Evidence | Notes |
|---|---|---|---|
| | Met / Not met / Partial | | |
| | Met / Not met / Partial | | |
| | Met / Not met / Partial | | |

**Composite predicate evaluation:**

- [ ] All conditions met — Success Predicate is satisfied
- [ ] One or more conditions not met — document gap and decision below

**If not fully satisfied:**

```
[What is not met, what is the plan, and whether this triggers a return to
Gate 0 for Problem Class revision or Gate 2 for design revision.]
```

---

### Adoption

After sufficient usage, do operators and consumers trust the system enough to rely on it?

**Usage period evaluated:**

**Signals of adoption:**

```
[Observable evidence: usage rates, reduction in manual fallback, operator
feedback, reduction in exceptions or overrides. Not anecdote.]
```

**Signals of non-adoption or distrust:**

```
[Workarounds, overrides, complaints, or low usage that suggest the system
is not trusted even when it is technically correct.]
```

---

## Routine Health and Review

### Class Drift Audit

Is the system still handling the problem class it was designed for?

**Problem Class (from Gate 0):**

```
[Restate the problem class in scope and anti-scope.]
```

**Observed operational behavior:**

```
[What problem class is the system actually handling in production?
Does it match the Gate 0 definition, or has it drifted?]
```

**Drift finding:**

- [ ] No drift — system handles the documented class
- [ ] Drift identified — describe below and trigger Living Document Protocol

**If drift identified:**

```
[What has changed: the system's behavior, the taxonomy, the intake types,
or the downstream routing rules? Which gate artifact needs to be revised?]
```

**Runtime AI — Model version drift:**

Has the underlying model version changed since Gate 2?

- [ ] No change
- [ ] Changed — re-validate behavioral evals against the Class Interface Contract

**Model version at Gate 2:** [version]
**Current model version:** [version]

**Re-validation result (if applicable):**

```
[Did outputs remain within the class contract after the model version change?
What changed and how was it addressed?]
```

---

### Knowledge Persistence

Have all design artifacts been preserved and updated to reflect current reality?

| Artifact | Current? | Last reviewed | Review trigger met? |
|---|---|---|---|
| Gate 0 — Problem Class Definition | Yes / No | | |
| Gate 2 — Class Interface Contract | Yes / No | | |
| Gate 2 — Prompt Contracts (Runtime AI) | Yes / No | | |
| Gate 2 — Data Boundary Declaration (Runtime AI) | Yes / No | | |
| Gate 2 — Human Oversight Model (Runtime AI) | Yes / No | | |
| ADRs | Yes / No | | |

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
- [ ] None of the above

**Review actions taken:**

```
[For each triggered event, what artifact was reviewed and what was updated.]
```

---

## Decommission Gate

Complete this section only if decommissioning is being considered.

### Trigger Assessment

Does maintenance cost exceed value? Has the problem class been dissolved, subsumed, or solved at a higher level?

```
[Assessment of maintenance cost vs. delivered value. Be specific about
what has changed that makes this system a candidate for decommission.]
```

**Decision:**

- [ ] Continue operating — maintenance cost justified
- [ ] Decommission — proceed to execution below

---

### Decommission Execution

Complete only if the decision above is to decommission.

| Step | Completed | Date | Notes |
|---|---|---|---|
| Access revoked | Yes / No | | |
| Records archived | Yes / No | | |
| Data purged per policy | Yes / No | | |
| LLM provider credentials revoked (Runtime AI) | Yes / No | | |
| API keys and service accounts revoked (Runtime AI) | Yes / No | | |
| Prompt/response log data handled per retention policy (Runtime AI) | Yes / No | | |
| Downstream consumers notified | Yes / No | | |

---

## Gate Approval

- [ ] Success Predicate evaluated against real operating data
- [ ] Adoption signals reviewed
- [ ] Class Drift Audit completed
- [ ] Model version drift checked and re-validated if applicable (Runtime AI)
- [ ] All design artifacts confirmed current
- [ ] Living Document Protocol events reviewed and acted on
- [ ] Decommission decision made explicitly (continue or decommission)

**Approved by:** [Named individual — not a team or group]
**Date:**
**Notes:**
