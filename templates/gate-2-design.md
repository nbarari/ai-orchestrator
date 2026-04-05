# Gate 2: Architecture and Design

**Project:**
**Date:**
**Author:**
**Status:** Draft / Approved / Superseded

**Gate 0 reference:** `docs/gate-0.md`
**Gate 1 reference:** `docs/gate-1.md`

Reference: `manual.md` Phase 3.

---

## Components and Contracts

### Logical Boundaries

Link to C4 Context and Container diagrams.

- Context diagram: 
- Container diagram: 

If diagrams do not exist yet, note the date by which they will be completed before this gate can be approved.

---

### Bill of Materials

List every required infrastructure resource and implementation artifact.

| Item | Type | Owner | Notes |
|---|---|---|---|
| | Infrastructure / Library / Service / Config | | |
| | Infrastructure / Library / Service / Config | | |

---

### Class Interface Contract

The schema defining what a valid input looks like and what a valid output looks like. No implementation begins until this contract exists.

**Link to contract file:** `docs/contracts/class-interface-contract.md`

If the contract is not yet complete, this gate cannot be approved.

**Summary of input schema:**

```
[summary]
```

**Summary of output schema:**

```
[summary]
```

**Contract version:**

---

### Prompt Contracts (Runtime AI)

One Prompt Contract per LLM call. Use `templates/prompt-contract.md` for each.

| LLM call | Contract file | Model version |
|---|---|---|
| | `docs/contracts/prompt-contract-.md` | |
| | `docs/contracts/prompt-contract-.md` | |

Leave blank if Build-Time only.

---

### Data Boundary Declaration (Runtime AI)

What data crosses into any LLM call? Is any of it subject to data classification, residency requirements, privacy regulation, or internal policy constraints?

If uncertain, escalate to data governance or legal before this gate is approved.

| Data element | Classification | LLM calls it enters | Permitted? | Basis for permission |
|---|---|---|---|---|
| | | | Yes / No / Pending | |
| | | | Yes / No / Pending | |

**Declaration:**
All data crossing into LLM calls in this system has been reviewed and is either permitted by the policy basis noted above or is excluded from LLM calls.

- [ ] Confirmed
- [ ] Pending review (block gate approval until resolved)

---

## Architecture and Failure Modes

### Class Boundary Behavior

What happens when the system receives an input that is adjacent to the defined class but outside it?

This is a design decision, not an error condition.

```
[class boundary behavior]
```

---

### Failure Mode Registry

Document the failure mode and user-facing behavior for each dependency.

| Dependency | Failure mode | User-facing behavior | Recovery path |
|---|---|---|---|
| | | | |
| | | | |

**LLM provider failure (Runtime AI):**

| Condition | System behavior |
|---|---|
| Provider unavailable | |
| Rate limited | |
| Invalid output returned | |
| Latency exceeds threshold | |

---

### Breaking Point

At what load does this design fail? What is the first component to fail?

```
[breaking point and failure component]
```

---

### Human Oversight Model (Runtime AI)

For each action the system can take, declare the oversight level.

| Action | Oversight level | Reversible? | Blast Radius | Rationale |
|---|---|---|---|---|
| | Autonomous / Supervised / Advisory | Yes / No | Low / Med / High | |
| | Autonomous / Supervised / Advisory | Yes / No | Low / Med / High | |

Irreversible actions with high blast radius require supervised or advisory oversight. Document the rationale for any autonomous classification in this category.

---

### Architecture Decision Records

List all ADRs created during this phase.

| ADR | Decision summary | File |
|---|---|---|
| ADR-001 | | `docs/adr/001-*.md` |
| ADR-002 | | `docs/adr/002-*.md` |

---

## Verification Strategy

### Behavioral Eval Criteria

What must be true for this system to be considered correct at the class level? Define this before implementation begins.

**Correctness criteria:**

```
[what correct looks like, including edge cases and failure modes]
```

**Class boundary eval criteria:**

```
[what the system should do with adjacent-but-excluded inputs]
```

**Runtime AI eval criteria:**

```
[class-level correctness criteria for nondeterministic outputs, or N/A]
```

---

### Irreversibility Analysis

List any downstream commitments that are difficult or impossible to reverse. These are not executed until Phase 5 verification is complete (Gate 4).

| Commitment | Impact | Tied to Gate 4 |
|---|---|---|
| | | Yes / No |
| | | Yes / No |

---

## Gate Approval

- [ ] C4 diagrams exist and are linked
- [ ] BOM is complete
- [ ] Class Interface Contract exists and is linked
- [ ] Prompt Contracts exist for all LLM calls (Runtime AI)
- [ ] Data Boundary Declaration is complete and reviewed (Runtime AI)
- [ ] Class boundary behavior is explicitly defined
- [ ] All failure modes are documented
- [ ] Human Oversight Model is complete with rationale (Runtime AI)
- [ ] All major decisions have ADRs
- [ ] Behavioral eval criteria are defined
- [ ] Irreversible commitments are identified and tied to Gate 4

**Approved by:**
**Date:**
**Notes:**
