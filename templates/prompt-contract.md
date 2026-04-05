# Prompt Contract: [Name]

A Prompt Contract defines the interface for a single LLM call. It is a component of the Class Interface Contract for Runtime AI systems.

**System:**
**LLM call name / identifier:**
**Model version validated against:**
**Date:**
**Author:**
**Status:** Draft / Accepted / Deprecated / Superseded by [name]

---

## Purpose

What problem-class operation does this LLM call perform? State this in terms of the Problem Class Definition from Gate 0, not in terms of the model or prompt.

```
[purpose]
```

---

## Input Contract

### Required inputs

| Field | Type | Description | Constraints |
|---|---|---|---|
| | | | |
| | | | |

### Optional inputs

| Field | Type | Description | Default |
|---|---|---|---|
| | | | |

### Input validation

What makes an input invalid for this call? What does the system do with an invalid input before it reaches the LLM?

```
[input validation rules and handling]
```

### Data Boundary Compliance

Confirm that all input fields are permitted to cross into this LLM call per the Data Boundary Declaration in Gate 2.

| Field | Permitted | Policy basis |
|---|---|---|
| | Yes / No | |
| | Yes / No | |

---

## Output Contract

### Expected output structure

| Field | Type | Description | Required |
|---|---|---|---|
| | | | Yes / No |
| | | | Yes / No |

### Output constraints

What properties must the output satisfy to be considered valid?

```
[output constraints]
```

### Class-level correctness criteria

What does a correct output look like at the problem-class level? These become the behavioral eval criteria for this call.

```
[correctness criteria]
```

---

## Contract Violation Handling

### Invalid output

What does the system do when the LLM returns output that violates this contract?

- [ ] Retry with the same input (maximum __ retries)
- [ ] Retry with a modified input
- [ ] Fall back to: [fallback behavior]
- [ ] Reject and surface error to caller
- [ ] Other:

```
[violation handling detail]
```

### Provider unavailability

What does the system do when the LLM provider cannot be reached?

```
[unavailability handling]
```

### Rate limiting

What does the system do when the call is rate-limited?

```
[rate limit handling]
```

---

## Observability

### Logged fields

| Field | Logged | Privacy classification |
|---|---|---|
| Input | Yes / No / Partial | |
| Output | Yes / No / Partial | |
| Latency | Yes / No | |
| Token count | Yes / No | |
| Model version | Yes / No | |

**Logging complies with Data Boundary Declaration:**
- [ ] Confirmed

---

## Human Oversight

What oversight level applies to any actions taken based on this call's output?

- [ ] Autonomous: system acts on output without human review
- [ ] Supervised: human reviews output before action is taken
- [ ] Advisory: human makes the decision; this call informs it

**Rationale:**

```
[oversight rationale]
```

---

## Model Version

**Validated against:** [model version]

**Pinning strategy:**

```
[how the model version is pinned in the implementation]
```

**Pinning expiry plan:**
What happens when this version is deprecated?

```
[expiry plan]
```

---

## Review Trigger

What event requires this Prompt Contract to be revisited?

Minimum triggers: model version change, output quality degradation detected in Phase 7 audit, change to the Class Interface Contract, Data Boundary Declaration update.

```
[additional review triggers]
```
