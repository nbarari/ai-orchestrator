# Gate 3: Technical Verification

**Project:**
**Date:**
**Author:**
**Status:** Draft / Approved / Superseded

**Gate 0 reference:** `docs/gate-0.md`
**Gate 2 reference:** `docs/gate-2.md`

Reference: `manual.md` Phase 5.

**Stop Criteria:** Halt if core functional requirements fail, if the system cannot reach the Breaking Point identified in Phase 3, or if class boundary behavior produces undefined outcomes.

---

## Verification

### Class Coverage

Does the test suite cover the full breadth of the defined problem class?

**In-class cases tested:**

```
[List the representative cases from within the problem class that the test suite covers.]
```

**Boundary cases tested:**

```
[List inputs adjacent to the class that the system should reject or handle gracefully,
and confirm the documented class boundary behavior fires correctly for each.]
```

**Gaps identified:**

```
[Any in-class or boundary cases not yet covered, with the plan to address them
before this gate is approved.]
```

---

### Contract Verification

Does the system adhere to the Class Interface Contracts defined in Phase 3?

**Link to Class Interface Contract:** `docs/contracts/class-interface-contract.md`

| Contract requirement | Verified | Method | Notes |
|---|---|---|---|
| Input schema validation rejects invalid inputs | Yes / No / Partial | | |
| Output schema matches contract on success | Yes / No / Partial | | |
| Contract version enforced | Yes / No / Partial | | |
| Rejection criteria produce documented behavior | Yes / No / Partial | | |

**Prompt Contract verification (Runtime AI):**

| LLM call | Contract file | Output matches contract | Violation handling verified |
|---|---|---|---|
| | `docs/contracts/prompt-contract-.md` | Yes / No / Partial | Yes / No |

---

### Signal Verification

Do health signals and alerts fire correctly under failure conditions?

| Signal | Condition that triggers it | Verified | Notes |
|---|---|---|---|
| | | Yes / No | |
| | | Yes / No | |

**Gaps:**

```
[Any signals that did not fire as expected, or conditions not yet tested.]
```

---

### Stress Test

Has the system been pushed to the Breaking Point identified in Gate 2?

**Breaking Point identified in Gate 2:**

```
[Restate the breaking point from gate-2.md here.]
```

**Stress test results:**

| Load level | Observed behavior | Breaking Point reached? |
|---|---|---|
| Steady state | | |
| Peak (Gate 1 estimate) | | |
| Breaking Point threshold | | Yes / No |

**First component to fail under load:**

```
[What broke first and at what load.]
```

---

### Behavioral Evals (Runtime AI)

Does the verification suite include behavioral evals that test class-level correctness?

**Eval criteria from Gate 2:**

```
[Restate the behavioral eval criteria defined in gate-2.md.]
```

**Coverage of criteria:**

| Eval criterion | Covered | Method | Pass rate or result |
|---|---|---|---|
| | Yes / No | | |
| | Yes / No | | |

**Note on nondeterminism:** The same input producing different outputs is expected behavior for Runtime AI systems, not a test failure, unless the output violates the class contract. Require coverage of the criteria; give engineers latitude on implementation methodology.

**Gaps:**

```
[Criteria not yet covered and the plan to address them.]
```

---

## Diagnostic Audit

### Self-Service Diagnosis

Can a qualified person diagnose a failure without access to the original builder?

- [ ] Yes — a runbook or diagnostic guide exists and has been tested by someone other than the author
- [ ] No — document what is missing before this gate is approved

**Evidence:**

```
[Link to runbook or describe the diagnostic guide and who tested it.]
```

---

### Traceability

Are logs, traces, and metrics sufficient to reconstruct a failure after the fact?

| What must be traceable | Logged? | Location | Notes |
|---|---|---|---|
| Request identifier | Yes / No | | |
| Input received | Yes / No / Partial | | |
| Model version used | Yes / No | | |
| Output produced | Yes / No / Partial | | |
| Latency | Yes / No | | |
| Outcome (success / fallback / error) | Yes / No | | |
| Fallback reason | Yes / No | | |

**Data Boundary compliance (Runtime AI):**
Is the logging approach compliant with the Data Boundary Declaration from Gate 2?

- [ ] Yes — logging reviewed against Data Boundary Declaration
- [ ] No — resolve before this gate is approved

**Note:** Logging what should not be logged is a compliance failure equivalent to not logging what should be.

---

## Gate Approval

- [ ] Class coverage verified including boundary cases
- [ ] All Class Interface Contract requirements verified
- [ ] Prompt Contract outputs verified for all LLM calls (Runtime AI)
- [ ] All health signals verified under failure conditions
- [ ] Stress test completed to Breaking Point
- [ ] Behavioral evals cover all criteria from Gate 2 (Runtime AI)
- [ ] Self-service diagnosis confirmed by non-author
- [ ] Traceability verified for all required fields
- [ ] Logging is compliant with Data Boundary Declaration (Runtime AI)

**Approved by:** [Named individual — not a team or group]
**Date:**
**Notes:**
