# Gate 4: Operational Readiness

**Project:**
**Date:**
**Author:**
**Status:** Draft / Approved / Superseded

**Gate 0 reference:** `docs/gate-0.md`
**Gate 3 reference:** `docs/gate-3.md`

Reference: `manual.md` Phase 6.

**Stop Criteria:** Halt if runbooks are untested, if the recovery and rollback procedure fails rehearsal, or if any Gate 3 verification signal is not confirmed Green.

**Note:** High-impact downstream changes identified as irreversible in Gate 2 are executed only after this gate is approved — not before.

---

## Sustainability and Controls

### Standard Operating Procedures

Are runbooks written and tested by someone other than the author?

| Runbook | Covers | Tested by | Date tested | Result |
|---|---|---|---|---|
| | | [not the author] | | Pass / Fail |
| | | [not the author] | | Pass / Fail |

**Gaps:**

```
[Any operational scenario not yet covered by a runbook.]
```

---

### Operational Controls

Are automated limits or kill switches active for variable operational spend?

| Control | Type | Active? | Threshold | Notes |
|---|---|---|---|---|
| | Kill switch / Rate limit / Alert | Yes / No | | |
| | Kill switch / Rate limit / Alert | Yes / No | | |

**Runtime AI — Cost circuit-breaker:**

Is there an automated limit that prevents runaway LLM spend before it becomes a financial incident?

- [ ] Yes — threshold: [value] per [period]
- [ ] No — resolve before this gate is approved

**Runtime AI — Privilege scope enforcement:**

Are privilege scopes of agentic components enforced at the infrastructure level, not only at the prompt level?

- [ ] Yes
- [ ] No — resolve before this gate is approved

**Runtime AI — Independent halt capability:**

Can AI-triggered state changes (data mutations, access grants, downstream workflow triggers) be halted independently of the main system?

- [ ] Yes — mechanism: [describe]
- [ ] No — resolve before this gate is approved

---

## Handoff and Rollback

### Rehearsal

Has the recovery and rollback procedure been rehearsed in a non-production environment?

- [ ] Yes — date rehearsed: [date] | rehearsed by: [not the original author]
- [ ] No — resolve before this gate is approved

**Rehearsal result:**

```
[What happened during the rehearsal. If any step failed, describe the fix applied.]
```

---

### Independence

Does the named system owner have sufficient context to operate this system without assistance from the original builder?

**Named owner:**

**Evidence of independence:**

```
[How was this confirmed? Did the owner successfully complete a diagnostic or
operational task without assistance?]
```

---

### Gate 3 Signal Confirmation

All Gate 3 verification signals must be Green before irreversible downstream changes are executed.

| Gate 3 signal | Status |
|---|---|
| Class coverage verified | Green / Not Green |
| Contract verification passed | Green / Not Green |
| Prompt Contract outputs verified (Runtime AI) | Green / Not Green |
| Health signals verified | Green / Not Green |
| Stress test completed | Green / Not Green |
| Behavioral evals passed (Runtime AI) | Green / Not Green |
| Self-service diagnosis confirmed | Green / Not Green |
| Traceability verified | Green / Not Green |
| Logging compliant with Data Boundary (Runtime AI) | Green / Not Green |

**All signals Green before proceeding:**

- [ ] Confirmed — irreversible downstream changes may now be executed
- [ ] Not confirmed — identify which signals are not Green and resolve

---

### Irreversible Commitment Execution

List the high-impact downstream changes identified in Gate 2 that are executed at this gate.

| Commitment | Executed? | Date | Notes |
|---|---|---|---|
| | Yes / No | | |
| | Yes / No | | |

---

## Gate Approval

- [ ] All runbooks written and tested by non-author
- [ ] Cost circuit-breaker active (Runtime AI)
- [ ] Privilege scopes enforced at infrastructure level (Runtime AI)
- [ ] Independent halt capability confirmed (Runtime AI)
- [ ] Rollback rehearsal completed successfully
- [ ] Named owner can operate independently
- [ ] All Gate 3 signals confirmed Green
- [ ] Irreversible commitments executed only after signals confirmed

**Approved by:** [Named individual — not a team or group]
**Date:**
**Notes:**
