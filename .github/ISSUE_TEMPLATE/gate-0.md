---
name: Gate 0 — Concept Validation
about: Open a Gate 0 review before starting a new project or capability
title: "[Gate 0] "
labels: gate-0, review-required
assignees: ""
---

## Gate 0: Concept Validation

Complete each field before requesting review. The next phase does not begin until this gate is approved.

Reference: `manual.md` Phase 1.

---

### Problem Class Definition

**What is the bounded category of problems this system is designed to handle?**
State this without referencing a solution. Include what falls outside the class.

```
[problem class]
```

**What is the Success Predicate?**
The logical condition, which may be composite, that determines whether the system is correctly handling its problem class. If this cannot be evaluated, the class definition is incomplete.

```
[success predicate]
```

**What evidence confirms this problem class is real?**
Observable signals, not assumptions.

```
[evidence]
```

**What does an unaddressed instance of this problem class cost?**
Time, capital, errors, or risk at the expected frequency of occurrence.

```
[cost]
```

**What does the problem class cost if left unaddressed at scale over the mid-to-long term?**

```
[inertia test]
```

---

### AI Deployment Mode

- [ ] Build-Time Only
- [ ] Runtime
- [ ] Both

**Reasoning:**

```
[why this mode]
```

---

### Timing and Solution Space

**Why does this problem class exist?**

```
[root cause]
```

**What changed recently that makes this addressable now?**

```
[catalyst]
```

**What tools or systems already handle adjacent classes, and why are they insufficient?**

```
[solution space]
```

---

### Approval

- [ ] Problem Class is bounded and includes explicit exclusions
- [ ] Success Predicate can be evaluated
- [ ] AI Deployment Mode is declared
- [ ] Evidence provided is observable, not assumed

**Approved by:**
**Date:**
