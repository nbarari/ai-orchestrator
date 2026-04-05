# ai-orchestrator-framework

A framework for architects and designers who direct AI-assisted development. Covers the full lifecycle from problem class definition through decommission.

---

## Background

Asking an AI to write code produces working prototypes. It does not produce maintainable systems. The missing piece is structural integrity: clear contracts, documented decisions, verified behavior, and defined ownership.

Most frameworks address this by prescribing a specific solution. This one addresses it by requiring that you define the *class of problems* a system handles before any implementation begins. A system built for a well-defined class can be verified, transferred, and decommissioned. A system built for a specific instance tends to become unmaintainable as soon as requirements shift.

---

## Design Principles

**Problem class before implementation.** No implementation begins until the Problem Class and Success Predicate are documented and approved. Features follow from a well-defined class; they are not the starting point.

**Gates as checkpoints, not formalities.** Each gate requires documented answers to phase-specific questions before the next phase can begin. The questions are designed to surface assumptions early, when they are cheap to address.

**Ownership is a design requirement.** Every phase considers the cost of owning what gets built, not just the cost of building it. The Decommission Gate reflects the reality that all systems eventually need to be retired cleanly.

---

## Who This Is For

This framework is designed for non-coding architects and designers who direct AI-assisted development. No programming experience is required.

It is also applicable for engineers who want a more structured design discipline for AI-assisted work, particularly for systems where an LLM executes at runtime.

Relevant questions this framework helps answer:

- How do I specify what a system should do precisely enough that AI can safely build it?
- How do I verify what AI built without reading the source code?
- How do I prevent architectural drift across a long build cycle?
- How do I produce documentation sufficient for someone else to take over?
- How do I manage the parts of AI systems that produce nondeterministic outputs?

---

## Build-Time AI vs. Runtime AI

This framework treats these two modes of AI involvement as distinct, because the design requirements differ significantly.

**Build-Time AI** means AI assists in writing, testing, or documenting the system during development. No LLM runs when the system is in production. The primary concerns are verification, structural integrity, and documentation discipline.

**Runtime AI** means an LLM executes as part of the live system, processing inputs, generating outputs, or taking actions on behalf of users or other systems. All Build-Time concerns apply, with these additional requirements:

| Concern | Reason |
|---|---|
| Prompt Contracts | Prompts are interfaces and require version control and contract discipline equivalent to APIs |
| Data Boundary Declaration | Data that cannot legally enter an LLM call must be identified before design is finalized |
| Human Oversight Model | Each autonomous action the system can take requires a defined oversight level |
| Operational Cost Model | Inference cost is a design constraint; a financially untenable system fails feasibility |
| Provider Reliability and Fallback | LLM provider outages are routine operational events, not edge cases |
| Behavioral Evals | Nondeterministic outputs require class-level correctness criteria defined before implementation |
| LLM Observability | Each AI decision affecting system state must be reconstructable from logs |
| Model Version Drift | Version pinning delays drift but does not prevent it; the Phase 7 audit exists for this reason |
| Cost Circuit-Breaker | Automated spend limits prevent runaway LLM cost from becoming a financial incident |

The AI Deployment Mode (Build-Time, Runtime, or Both) is declared at Gate 0 and determines which gate criteria apply in subsequent phases.

---

## The 7 Phases

| Phase | Gate | Primary Question |
|---|---|---|
| 1. Planning | Concept Validation | Does this problem class warrant a system? |
| 2. Feasibility | Discovery and Context | What are the constraints and risks? |
| 3. Design | Architecture and Liability | What does owning this cost over time? |
| 4. Implementation | Task-Level Gate | Does this change serve the class or expand it? |
| 5. Testing | Technical Verification | Does the system satisfy the contracts defined in Phase 3? |
| 6. Deployment | Operational Readiness | Is the system safe to activate? |
| 7. Maintenance | Post-Deploy Validation | Did the Success Predicate evaluate to true? |

---

## Key Terms

**Problem Class.** A bounded category of problems the system handles, with explicit inclusion and exclusion criteria. Defined in Phase 1. All subsequent phase decisions are evaluated against it.

**Success Predicate.** A logical condition, which may be composite, that determines whether the system is correctly handling its problem class. If the predicate cannot be evaluated, the class definition is incomplete. Validated in Phase 7.

**AI Deployment Mode.** A declaration of whether AI is present at build time, runtime, or both. Made at Gate 0. Determines which gate criteria are active for the remainder of the SDLC.

**Class Interface Contract.** The schema defining what a valid input looks like and what a valid output looks like. Defined before implementation begins. For Runtime AI systems, this includes Prompt Contracts.

**Prompt Contract.** The defined structure of inputs to and expected outputs from an LLM call. The Runtime AI equivalent of an API specification.

**Data Boundary Declaration.** A documented statement of what data crosses into any LLM call and whether it is subject to classification, residency, or privacy constraints. Required before the Class Interface Contract is finalized for Runtime AI systems.

**Human Oversight Model.** The defined level of human involvement for each action a Runtime AI system can take: autonomous, supervised, or advisory. Determined by action reversibility and blast radius.

**Blast Radius.** The maximum impact of a single failure or change. Mapped in Phase 2, minimized in Phase 6.

**ADR (Architecture Decision Record).** A persistent record of a design decision, the context behind it, and the alternatives considered. Written at the moment of decision, not retrospectively.

**Class Drift.** The condition where a system's operational behavior has diverged from its designed problem class without a corresponding design revision. For Runtime AI systems, model version changes can produce class drift even when no code changes.

**Living Document Protocol.** A defined set of event-based triggers, beyond calendar cadence, that require review and update of design artifacts.

---

## Repository Structure

```
/
├── README.md
├── manual.md                       # The 7-phase SDLC Manual
├── curriculum.md                   # Reading list, Levels 0-6
```

---

## Usage

**New project:** Start at Phase 1. Do not begin implementation until the Problem Class Definition, Success Predicate, and AI Deployment Mode are documented and approved at Gate 0.

**Task within an existing project:** Apply the Task-Level Gate if the task touches a data schema, Class Interface Contract, public interface, authentication or authorization logic, an external dependency, an LLM call, or introduces new data into an existing LLM call.

**Scaling rigor:** See `appendix/rigor-by-risk.md`. Low-risk work can be handled with verbal verification. High-risk work requires formal artifacts, peer review, behavioral evals, and documented stop criteria.

---

## Documents

**[manual.md](./manual.md)** covers the gate questions, stop criteria, and phase-by-phase design requirements. Start here when beginning a project.

**[curriculum.md](./curriculum.md)** covers the theoretical foundation for the framework, organized as a reading list from Levels 0 through 6. Start here when building background knowledge.

---

`v0.1 — draft. Templates and worked examples in progress.`
