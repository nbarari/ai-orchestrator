# Framework Notes

Observations, gaps, and friction points discovered during validation and use. These feed directly into framework iteration.

This file is part of the Living Document Protocol. It is updated whenever a gap is found in practice, not on a calendar schedule.

---

## Intercept Rules: Passive Rules Cannot Reliably Halt Generation

**Discovered during:** Validation of `intercept.mdc` ADR trigger  
**Phase:** IDE Integration (v0.1)

### Observation

The `intercept.mdc` rule reliably fires when the user phrases a request indirectly:

- "I need to document the decision to use X" → checklist presented, generation halted
- "Document the reasoning for choosing X" → checklist presented, generation halted

It does not reliably fire when the user issues a direct imperative:

- "Write an ADR for X" → ADR generated without checklist
- "Create a schema for X" → schema generated with notes but without checklist confirmation

### Root Cause

Cursor injects `alwaysApply: true` rules as system context, but the model weighs the directness of the user's instruction against the rule's instruction to halt. A direct imperative prompt carries enough force that the model treats the rule as guidance rather than a gate. This is a property of how Cursor applies rules, not a fixable wording problem.

### Current Ceiling

Passive rules in Cursor can:
- Shape output quality and add required fields
- Flag gaps and note missing gate documents
- Reliably intercept indirect and ambiguous requests

Passive rules in Cursor cannot:
- Reliably halt generation in response to direct imperative prompts
- Return a blocking result before generation begins

### Workaround

Frame requests as questions or indirect statements rather than direct commands when working with the intercept rules:

| Instead of | Use |
|---|---|
| "Write an ADR for..." | "I need to document the decision to..." |
| "Create a schema for..." | "I need to define the shape of..." |
| "Generate a prompt contract for..." | "Help me think through the contract for..." |

This is a workflow convention, not a technical fix. It works but requires discipline.

### Permanent Fix

Full gate enforcement requires a tool that returns a blocking result before any generation occurs. This is the motivation for:

- **v0.3:** CLI tool with `validate_gate()` that checks gate documents exist before allowing generation to proceed
- **v1.0:** MCP server exposing `check_task_gate()` and `generate_prompt_contract()` as structured tools that Cursor and Claude can call before generating

Until those exist, the intercept rules provide best-effort enforcement with the workaround above.

---

## contracts.mdc Auto-Attach: Glob Matching Inconsistency

**Discovered during:** Validation of `contracts.mdc`  
**Phase:** IDE Integration (v0.1)

### Observation

The original glob pattern used a comma-separated list within one quoted string:

```
globs: "**/*.schema.json, **/*.contract.*"
```

Cursor did not attach the rule to `test.schema.json` with this format. The rule was rewritten with each glob as a separate quoted string, which resolved the attachment.

### Resolution

Fixed in commit `7c8fbe0`. Each glob is now a separate quoted value. If Cursor rules do not attach to expected file types, verify the glob format matches Cursor's expected syntax at the time of implementation — this format has changed across Cursor versions.

---

## ADR Generation: Context Reconstruction vs. Recall

**Discovered during:** ADR generation tests  
**Phase:** IDE Integration (v0.1)

### Observation

When an ADR is generated without the pre-flight checklist, the AI reconstructs context from surrounding code and project files rather than recalling the actual decision. The result is a plausible but not accurate ADR — the context section reflects what the code implies rather than what actually drove the decision.

The intercept rule addresses this by requiring the user to state context explicitly before generation. The generation requirement also instructs the AI to note explicitly when context has been reconstructed rather than recalled.

### Implication for Examples

Any ADR produced during the worked example should be generated through the checklist workflow, not through direct imperative prompts. If an ADR is generated without the checklist, note in the ADR's Context field that the reasoning was reconstructed and may not reflect the original decision accurately.
