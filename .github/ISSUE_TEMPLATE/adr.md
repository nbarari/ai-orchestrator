---
name: Architecture Decision Record
about: Document a significant design decision
title: "[ADR] "
labels: adr
assignees: ""
---

## Architecture Decision Record

Reference: `templates/adr-template.md`

ADRs are written at the moment of decision. If this decision was made before this issue was opened, note that in the Context field and record when it was actually made.

---

**Title:**
Short noun phrase describing the decision, not the outcome.

**Status:** Proposed / Accepted / Deprecated / Superseded

**Date of decision:**

**SDLC phase when decision was made:**

---

### Context

What situation made this decision necessary?

```
[context]
```

### Decision

What was decided? State it as a declarative sentence.

```
[decision]
```

### Alternatives considered

What other options were evaluated and why were they not chosen?

```
[alternatives]
```

### Consequences

What becomes easier and what becomes harder as a result of this decision?

```
[consequences]
```

### Review trigger

What event would require this ADR to be revisited?

```
[review trigger]
```

---

### Runtime AI fields (complete if applicable)

**Model version rationale:**

```
[why this model version or N/A]
```

**Human oversight level for affected actions:**

```
[oversight levels or N/A]
```

**Data boundary decision:**

```
[what data was permitted into LLM calls and why, or N/A]
```

**Pinning expiry plan:**

```
[what happens when this model version is deprecated, or N/A]
```
