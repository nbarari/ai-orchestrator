# Contributing

Contributions are welcome. This document describes what kinds of contributions are most useful and how to make them.

---

## What Is Most Useful Right Now

**Worked examples.** A complete pass through the framework on a real, bounded system, with artifacts at each gate, is the highest-value contribution. See `examples/README.md` for the expected structure. Sanitized artifacts from real projects are more useful than purpose-built examples.

**Template improvements.** If a gate worksheet is missing a question that came up in practice, or if a question is phrased in a way that produced ambiguous answers, open an issue with the proposed change and the reasoning.

**Cursor rule corrections.** If a rule in `.cursor/rules/` produces unhelpful behavior in practice, open an issue describing the observed behavior, the context, and what behavior would have been more useful.

**Gap documentation.** If you applied the framework and encountered a situation it did not handle well, document it in an issue. Gaps that are named explicitly are more useful than gaps that are silently worked around.

---

## How to Propose a Change

Open an issue before opening a pull request for any change that affects the manual, curriculum, or templates. The issue should describe the problem the change addresses, not just the change itself.

Use the framework's own vocabulary when describing the problem. If a section of the manual does not handle a class of situation it should handle, say what that class is.

For bug fixes and minor corrections (typos, broken links, formatting), a pull request without a prior issue is fine.

---

## Applying the Framework to Contributions

Contributions that add new gate criteria, new templates, or new appendix content should apply the framework to themselves where practical.

For a new gate criterion, state the problem class it addresses, the evidence that the class exists in practice, and the failure mode it prevents.

For a new template, state what phase it belongs to and what artifact it produces.

This is not a rigid requirement, but contributions that can answer these questions are easier to evaluate.

---

## Commit Convention

```
type: short description

- type: feat, fix, docs, template, example, rule, refactor
- description: present tense, lowercase, no period
```

Examples:
```
feat: add gate-3 worksheet template
fix: correct class boundary behavior field in gate-2 template
docs: add model drift to glossary
example: add document classification agent walkthrough
rule: update runtime-ai.mdc to require fallback logging
```

---

## ADR for Structural Changes

Changes to the framework's own structure (adding a phase, changing a gate criterion, adding a new required artifact) require an ADR in `docs/adr/` explaining the decision and the alternatives considered. This applies the framework's own documentation discipline to its own development.

---

## Questions

Open an issue with the label `question`. There are no guarantees on response time, but questions that reveal gaps in the documentation are treated as bug reports.
