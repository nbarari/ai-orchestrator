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

---

## Gate 0: Approval Requires a Named Individual, Not a Group

**Discovered during:** Gate 0 worked example  
**Phase:** Worked Example (v0.2)

### Observation

The Gate 0 approval block in the worked example uses "ai-orchestrator-framework contributors (worked example)" as the Approved By value. This is acceptable for a framework example but would be a gap in a live deployment.

A group approval has no accountability when questions arise in Phase 7. If the Success Predicate is disputed or the Problem Class is challenged, "contributors" cannot be contacted, cannot recall the reasoning, and cannot confirm what was understood at the time of approval.

### Implication for Template

The `templates/gate-0-concept.md` Approved By field should include a note making this explicit:

```
**Approved by:** [Name of individual — not a team or group. 
A group approval has no accountability at Phase 7.]
```

This applies to all gate worksheets, not only Gate 0. The same principle applies to the ADR template's Author field.

### Fix

Update gate worksheet templates and the ADR template in v0.2 to include this note inline. Add it to the generation requirements in `intercept.mdc` for ADRs: "Approved By and Author must be a named individual, not a team or group."

---

## Gate 0: Evidence Section in Worked Examples

**Discovered during:** Gate 0 worked example  
**Phase:** Worked Example (v0.2)

### Observation

The Evidence section of a gate worksheet requires observable signals — logs, tickets, measured time, error rates. A worked example cannot provide real telemetry without a live system.

The resolution used in this example is to document the categories of evidence rather than real instances, and to note explicitly in the Gate Approval section that the checklist item is satisfied on the basis of evidence categories rather than attached telemetry.

This is the correct approach for a worked example, but it creates a risk: a practitioner copying the example for a real deployment may leave the evidence section in its illustrative form without replacing it with real data.

### Implication for Template

The Evidence section in `templates/gate-0-concept.md` should include a warning:

```
If this is a worked example or template, note that explicitly in the 
Gate Approval section. For a live deployment, replace illustrative 
signal types with concrete references: system names, time ranges, 
ticket IDs, or measured figures. The checklist item cannot be satisfied 
by illustrative content alone in a production context.
```

### Fix

Add this warning to `templates/gate-0-concept.md` in v0.2. Consider adding a similar note to the gate approval checklist item itself so it is visible at sign-off time.

---

## Gate 1: Cost Model Checkbox Tension

**Discovered during:** Gate 1 worked example
**Phase:** Worked Example (v0.2)

### Observation

The "Operational cost model completed" checklist item is checked despite all
figures being illustrative rather than measured. This mirrors the Gate 0
evidence tension: the checkbox is satisfied on the basis of model structure
(correct cost categories, correct scenarios, correct viability framing) rather
than real numbers.

### Implication for Template

The gate-1-feasibility.md template should add a note to the cost model
checklist item equivalent to the evidence note in gate-0-concept.md:

> For a live deployment, this checklist item requires real figures — provider
> pricing applied to measured token volumes at expected document lengths.
> Illustrative figures satisfy the structure requirement only; a production
> Gate 1 cannot proceed to Gate 2 without at least a rough order-of-magnitude
> estimate grounded in actual intake data and current model pricing.

### Fix

Add this note to the Operational Cost Model section of
`templates/gate-1-feasibility.md` in v0.2.

---

## Gate 1: Volume Profile Allows Multiple Distributions

**Discovered during:** Gate 1 worked example
**Phase:** Worked Example (v0.2)

### Observation

The Class Volume Analysis section uses checkboxes for volume distribution
(Low and steady / Bursty / Continuous and high-volume) but the document
classification agent is both bursty and continuous — two boxes checked
simultaneously. The template implies mutually exclusive options but real
systems often combine profiles.

### Implication for Template

The checkbox format creates a false choice. Replace it with a free-form
field or change the framing to "select all that apply" with an explicit
prompt to describe the relationship between profiles (e.g., continuous
baseline with identifiable burst periods).

### Fix

Update the Class Volume Analysis section in `templates/gate-1-feasibility.md`
to read "Select all that apply" and add a follow-up field:

> **Distribution description:** How do these profiles interact? (e.g.,
> continuous baseline of X with burst periods of Y at Z frequency)

## ADR Output Path Not Specified in Pre-Flight

**Discovered during:** ADR intercept validation testing
**Phase:** IDE Integration (v0.1)

### Observation

ADR-001 was generated to `docs/adr/` rather than
`examples/document-classification-agent/adr/` because the output path
was not specified during the pre-flight checklist. The AI chose a
reasonable default path based on convention, which was wrong for this
project's structure.

### Fix

Add an output path question to the ADR pre-flight checklist in
`intercept.mdc`:

> **Output path:** Where should this ADR be created?
> Confirm the exact file path before generating.

### Additional Finding

The "Record completeness" table the AI appended to the ADR is a useful
pattern for ADRs written under incomplete information. Consider adding it
as an optional closing section to `templates/adr-template.md` so
incomplete fields are explicitly flagged rather than silently omitted.

---

## Class Interface Contract: Success Predicate Alignment Section

**Discovered during:** Gate 2 worked example
**Phase:** Worked Example (v0.2)

### Observation

The generated Class Interface Contract included a section explicitly
mapping contract fields to the three Success Predicate conditions from
Gate 0 (routing accuracy, operational safety, traceability). This section
is not in the current Class Interface Contract template but is genuinely
useful — it makes the contract's relationship to the gate artifacts
explicit and auditable.

### Fix

Add an optional "Alignment with Success Predicate" section to
`templates/gate-2-design.md` and the contract template, linking
contract fields to the conditions defined in Gate 0.

---

## Gate 2: Success Predicate Numerics Section

**Discovered during:** Gate 2 worked example
**Phase:** Worked Example (v0.2)

### Observation

Gate 2 included a "Success Predicate Numerics" section that closes the
threshold deferral from Gate 0 — pinning accuracy targets, confidence
thresholds, retry limits, and timeout values as explicit design decisions.
This section is not in the current gate-2-design.md template but is
genuinely valuable: it makes Gate 0's composite predicate numerically
evaluable and gives Gate 3 concrete pass/fail criteria.

### Fix

Add a "Success Predicate Numerics" section to `templates/gate-2-design.md`
as the last section before Gate Approval, with fields for:
- Accuracy threshold on evaluation set
- Confidence threshold below which automated commit is blocked
- Max retries on invalid output
- Per-attempt timeout
- Any always-supervised label categories

---

## Class Boundary Behavior: Deferring Route Values to Gate 4

**Discovered during:** Gate 2 worked example
**Phase:** Worked Example (v0.2)

### Observation

The class boundary behavior section defined system behavior for adjacent
inputs while explicitly deferring specific route values to Gate 4 runbooks:
"route to human triage or documented default low-risk bucket only if Gate 4
runbooks define one — default is human queue."

This is the correct pattern. Class boundary behavior defines what the system
does (does not silently classify, routes to a defined path) without inventing
specific route names or queue identifiers that belong in operational runbooks.

### Implication for Template

The gate-2-design.md class boundary behavior section should include a note:

> Behavior statements may defer specific route values, queue names, or
> threshold numbers to Gate 4 runbooks. The requirement is that the behavior
> is defined (not left to implementation judgment) — not that all values are
> pinned in this document.

---