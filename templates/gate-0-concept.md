# Gate 0: Concept Validation

**Project:**
**Date:**
**Author:**
**Status:** Draft / Approved / Superseded

Reference: `manual.md` Phase 1.

---

## Problem Class Definition

### Problem Class

What is the bounded category of problems this system is designed to handle?

State this without referencing a solution. Be explicit about what falls outside the class. A useful test: can you describe a problem that is adjacent to the class but explicitly excluded?

**In scope:**

```
[describe the problem class]
```

**Out of scope (Anti-Scope):**

```
[describe what this system explicitly does not handle]
```

---

### Success Predicate

What logical condition determines whether the system is correctly handling its problem class?

The predicate may be composite. If it cannot be evaluated against observable system behavior, the class definition is not yet complete.

```
[success predicate]
```

**How will this predicate be evaluated in Phase 7?**

```
[evaluation method]
```

---

### Evidence

What observable signals confirm that this problem class exists and is not merely perceived?

Acceptable evidence: logs showing frequency, support tickets, measured time spent, error rates, incident reports. Not acceptable: anecdote or assumption.

```
[evidence]
```

---

### Class Impact

What does an unaddressed instance of this problem class cost at the expected frequency of occurrence?

Quantify where possible: time per instance, error rate, capital cost, risk exposure.

```
[cost per instance at expected frequency]
```

---

### Inertia Test

What does the problem class cost if left unaddressed at scale over the mid-to-long term?

```
[cost at scale over time]
```

---

## AI Deployment Mode

Select one and document the reasoning.

- [ ] **Build-Time Only.** AI assists in writing, testing, or documenting the system. No LLM executes in production.
- [ ] **Runtime.** An LLM executes as part of the live system.
- [ ] **Both.** AI is present in both the build process and the live system.

**Reasoning:**

```
[why this mode]
```

**Gate criteria activated by this mode:**

For Build-Time Only: verification, structural integrity, documentation discipline.

For Runtime (add to Build-Time): operational cost model, data boundary declaration, provider reliability and fallback, behavioral evals, LLM observability, human oversight model, model version pinning, cost circuit-breaker.

---

## Timing, Origin, and Solution Space

### Root Cause

Why does this problem class exist? Is the gap process-based, technical, organizational, or a knowledge deficit?

```
[root cause]
```

### Catalyst

What changed recently that makes this class addressable now?

```
[catalyst]
```

### Solution Space

What tools or systems already handle adjacent problem classes, and why are they insufficient for this one?

| Tool / System | What it handles | Why insufficient |
|---|---|---|
| | | |
| | | |

---

## Gate Approval

- [ ] Problem Class is bounded with explicit inclusions and exclusions
- [ ] Success Predicate is stated and can be evaluated
- [ ] Evidence is observable, not assumed
- [ ] AI Deployment Mode is declared with reasoning
- [ ] Solution space has been reviewed

**Approved by:**
**Date:**
**Notes:**
