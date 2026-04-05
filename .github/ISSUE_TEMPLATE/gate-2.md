---
name: Gate 2 — Architecture and Design Review
about: Open a Gate 2 review before implementation begins
title: "[Gate 2] "
labels: gate-2, review-required
assignees: ""
---

## Gate 2: Architecture and Design Review

Complete each field before requesting review. Implementation does not begin until this gate is approved.

Reference: `manual.md` Phase 3. Link the approved Gate 0 issue below.

**Gate 0 issue:** #

---

### Components and Contracts

**Link to C4 context and container diagrams:**

**Link to Bill of Materials (BOM):**

**Link to Class Interface Contract:**
The schema defining valid inputs and valid outputs. This must exist before implementation begins.

**Link to Prompt Contracts (Runtime AI):**
One contract per LLM call. Leave blank if Build-Time only.

**Data Boundary Declaration (Runtime AI):**
What data crosses into any LLM call? Is any of it subject to classification, residency, or privacy constraints?

```
[data boundary declaration or N/A]
```

---

### Architecture and Failure Modes

**Class boundary behavior:**
What happens when the system receives an input adjacent to the class but outside it?

```
[class boundary behavior]
```

**Failure mode for each external dependency:**

```
[failure modes]
```

**LLM provider fallback (Runtime AI):**
What does the system do when the provider is unavailable, rate-limited, or degraded?

```
[fallback behavior or N/A]
```

**Breaking point:**
At what load does this design fail?

```
[breaking point]
```

**Human Oversight Model (Runtime AI):**
For each action the system can take, declare the oversight level: autonomous, supervised, or advisory.

```
[oversight model or N/A]
```

---

### ADRs

List all ADRs created for this design phase:

- [ ] `docs/adr/`
- [ ] `docs/adr/`

---

### Verification Strategy

**Behavioral eval criteria:**
What must be true for this system to be considered correct at the class level?

```
[eval criteria]
```

**Irreversible commitments:**
List any downstream changes that cannot be reversed, and confirm they are tied to Gate 4.

```
[irreversible commitments]
```

---

### Approval

- [ ] Class Interface Contract exists and is linked
- [ ] Class boundary behavior is explicitly defined
- [ ] All failure modes are documented
- [ ] Human Oversight Model is complete (Runtime AI)
- [ ] Data Boundary Declaration is complete (Runtime AI)
- [ ] Behavioral eval criteria are defined
- [ ] ADRs cover all major decisions

**Approved by:**
**Date:**
