# 🤖 AI Orchestrator's SDLC Manual

A 7-phase framework for building high-integrity systems where humans provide the architecture and AI provides the implementation.

---

## The Problem This Solves

"Prompt engineering" — asking an AI to write code — produces working prototypes. It does not produce maintainable systems. The gap between the two is **structural integrity**: clear contracts, documented decisions, verified behavior, and defined ownership.

This framework closes that gap. But it does not close it by solving specific problems — it closes it by defining the **class of problems** a system handles before a single line is written.

---

## The Core Philosophy

**Define the class before building the instance.**

Every design decision — architecture, interface, test, decommission — is evaluated against the problem class definition, not the specific problem that motivated it. A system built for a class is maintainable, transferable, and honest about its limits. A system built for an instance becomes legacy the day requirements change.

Three principles follow from this:

**1. Class before instance.**
No implementation begins until the Problem Class and Success Predicate are documented and approved. Features are a byproduct of a well-defined class, not a starting point.

**2. Cognitive speed bumps over momentum.**
Each gate forces a mindset shift — from builder to strategist. The question at every gate is not "how do I implement this?" but "does this belong to the class I defined, and does it serve the Success Predicate?"

**3. Every solution is a future liability.**
Design for the cost of *owning* the system, not just building it. The Decommission Gate exists because nothing lasts forever and undocumented class drift is how legacy systems are born.

---

## Who This Is For

Engineers who have moved beyond "AI writes my code" and are asking:

- How do I define what a system is *supposed to do* precisely enough that AI can safely build it?
- How do I verify what the AI built without reading every line?
- How do I prevent architectural drift across a long build cycle?
- How do I hand this off without it becoming a black box?
- How do I handle the parts of AI systems that are nondeterministic?

---

## The 7 Phases at a Glance

| Phase | Gate | Mindset |
|---|---|---|
| 1. Planning | Concept Validation | Does this problem class warrant a system? |
| 2. Feasibility | Discovery & Context | What are the landmines? |
| 3. Design | Architecture & Liability | What does owning this cost? |
| 4. Implementation | Task-Level Gate | Does this serve the class or expand it? |
| 5. Testing | Technical Verification | How do I break my own assumptions? |
| 6. Deployment | Operational Readiness | How do I minimize blast radius? |
| 7. Maintenance | Post-Deploy Validation | Did the Success Predicate evaluate to true? |

---

## Key Concepts

**Problem Class**
A bounded category of problems the system handles, with explicit inclusion *and* exclusion criteria. A system that handles everything handles nothing well. Defined in Phase 1. Every subsequent phase is evaluated against it.

**Success Predicate**
A logical condition — which may be composite — that determines whether the system is correctly handling its problem class. If the predicate cannot be evaluated, the class is not yet well-defined. Validated in Phase 7.

**Class Interface Contract**
The schema defining what a valid problem in the class looks like as a system input, and what a valid resolution looks like as an output. Defined before implementation begins. For AI systems, this includes **Prompt Contracts** — the structured definition of inputs to and expected outputs from any LLM call. Prompts are interfaces; they require the same version control and contract discipline as APIs.

**Blast Radius**
The maximum impact of a single failure. Mapped in Phase 2. Minimized in Phase 6. Every design decision should reduce it — especially for agentic AI components that can trigger real-world state changes.

**ADR (Architecture Decision Record)**
A persistent record of major decisions and their reasoning. The long-term memory that neither LLMs nor rotating team members retain naturally. For AI systems, ADRs include model version pins and the rationale for LLM use vs. deterministic logic.

**Class Drift**
The condition where a system's operational problem class has diverged from its designed problem class without a corresponding design revision. The primary failure mode of maintained systems. For AI systems, model version changes are a form of class drift — system behavior may shift even when no code changes.

**The Decommission Gate**
When maintenance cost exceeds value, retire cleanly. Revoke access, archive records, purge data. A system that isn't decommissioned intentionally becomes technical debt indefinitely.

---

## AI-Specific Considerations

Standard SDLC frameworks assume deterministic systems. AI systems introduce additional failure surfaces that map to existing gates rather than requiring separate treatment:

| AI Concern | Where It Lives |
|---|---|
| Prompt contracts and versioning | Phase 3 — Class Interface Contract |
| Nondeterminism in testing | Phase 5 — Behavioral Evals |
| Agentic blast radius and privilege scope | Phase 3 ADR + Phase 6 Kill Switches |
| Model drift and version pinning | Phase 3 ADR + Phase 7 Class Drift Audit |
| AI output auditability | Phase 5 Traceability + Phase 6 SOP |

None of these are exceptions to the framework — they are specializations of class-level thinking applied to systems with nondeterministic components.

---

## Repository Structure

```
/
├── manual.md                   # The full 7-phase SDLC Manual
├── curriculum.md               # The AI Orchestrator's reading list (Levels 1–6)
├── templates/
│   ├── gate-0-concept.md       # Phase 1 worksheet — Problem Class + Success Predicate
│   ├── gate-1-feasibility.md   # Phase 2 worksheet — Class Volume + Blast Radius
│   ├── gate-2-design.md        # Phase 3 worksheet — Class Interface Contract + ADR
│   ├── adr-template.md         # Architecture Decision Record template
│   └── prompt-contract.md      # LLM interface contract template
├── examples/
│   └── [worked example]        # End-to-end SDLC applied to a simple agentic system
└── appendix/
    ├── glossary.md
    └── rigor-by-risk.md
```

---

## How to Use This

**Starting a new project:** Begin at Phase 1. Do not write code until the Problem Class Definition and Success Predicate are documented and approved at Gate 0.

**Starting a task within a project:** Apply the Task-Level Gate. If the task touches a data schema, Class Interface Contract, public interface, auth, an external dependency, or an LLM call — the gate applies.

**The key question at every gate:**
> Does this serve the defined problem class and Success Predicate, or am I expanding the class without approval?

**Scaling rigor:** See `appendix/rigor-by-risk.md`. Low-risk work requires verbal verification. High-risk work requires formal artifacts, peer review, behavioral evals, and documented stop criteria.

---

## Companion Resources

This manual is the implementation guide. The [AI Orchestrator's Curriculum](./curriculum.md) provides the theoretical foundation — from mental models through strategic governance. The curriculum and the manual are designed to be read together: the curriculum explains *why* the gates exist, the manual defines *how* to pass them.

---

## Status

`v0.1 — Framework draft. Templates and worked examples in progress.`

Contributions, critiques, and worked examples welcome.
