# CLAUDE.md

This project uses the AI Orchestrator framework. The full manual is at `docs/manual.md`. The curriculum is at `docs/curriculum.md`.

## Project State

Before beginning any session, read the following if they exist:

- `docs/gate-0.md` — Problem Class Definition, Success Predicate, AI Deployment Mode
- `docs/gate-2.md` — Class Interface Contracts, Data Boundary Declaration, Human Oversight Model
- `docs/adr/` — Architecture Decision Records

If `docs/gate-0.md` does not exist, the project has not passed Gate 0. Surface this before writing any code.

## Task-Level Gate

Apply at the start of any task that involves the following. Do not proceed until each question has a documented answer.

**Significance Triggers:**
- Data schemas or Class Interface Contracts
- Public interfaces or APIs
- Authentication or authorization logic
- New external dependencies
- LLM calls, agent actions, or nondeterministic execution paths

**Questions:**
1. Does this change serve the Success Predicate?
2. Is it backward compatible?
3. What happens if it runs more than once?
4. What is the recovery path on failure?
5. Does it exceed Minimum Class Coverage?
6. (Runtime AI) Does it introduce data into an LLM call not in the Data Boundary Declaration?

After completing a task, confirm: what drift occurred from the original design, is it documented, and does it contradict the approved architecture?

## Contract Requirements

Do not implement across a system boundary without a documented Class Interface Contract. For Runtime AI, this includes a Prompt Contract for every LLM call.

Prompt Contracts must specify:
- Input structure and format
- Expected output structure and constraints
- Model version validated against
- Behavior on contract violation
- Data Boundary compliance confirmation

## Runtime AI Requirements

For every LLM call:
- Check that a Prompt Contract exists. If not, draft one for review before writing the call.
- Define fallback behavior for provider unavailability, rate limiting, and invalid output. Unhandled exceptions are not acceptable failure paths.
- Pin to a specific model version. Note that pinning delays drift; flag for Phase 7 Class Drift Audit when the version is deprecated.
- Log inputs and outputs by default. Confirm logging is compliant with the Data Boundary Declaration.
- Define human oversight level: autonomous, supervised, or advisory.

## ADR Triggers

Prompt the user to write an ADR when:
- A model or provider is selected
- A data boundary decision is made
- An oversight level is set for an agent action
- A schema or contract is finalized
- An external dependency is introduced

ADRs live in `docs/adr/`. Each requires: title, status, date, context, decision, alternatives considered, consequences, and review trigger.

## Phase Reference

| Phase | Gate | Primary Question |
|---|---|---|
| 1. Planning | Gate 0 | Does this problem class warrant a system? |
| 2. Feasibility | Gate 1 | What are the constraints and risks? |
| 3. Design | Gate 2 | What does owning this cost over time? |
| 4. Implementation | Task-Level Gate | Does this serve the class or expand it? |
| 5. Testing | Gate 3 | Does the system satisfy the Phase 3 contracts? |
| 6. Deployment | Gate 4 | Is the system safe to activate? |
| 7. Maintenance | Gate 5 | Did the Success Predicate evaluate to true? |
