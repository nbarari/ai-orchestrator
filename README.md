# 🤖 ai-orchestrator-framework

A framework for engineers and architects who design systems that AI builds. From problem class definition through decommission.

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

This framework is designed for **non-coding architects and designers** who direct AI-assisted development — people who define what gets built, not people who build it. No coding experience is required or assumed.

It is also useful for engineers who want a more rigorous design discipline for AI-assisted work, particularly for systems where AI executes at runtime.

If you are asking any of these questions, this framework is for you:

- How do I define what a system is supposed to do precisely enough that AI can safely build it?
- How do I verify what AI built without reading every line of code?
- How do I prevent architectural drift across a long build cycle?
- How do I hand this off without it becoming a black box?
- How do I handle the parts of AI systems that are nondeterministic?

---

## A Critical Distinction: Build-Time vs. Runtime AI

Not all AI involvement is the same. This framework distinguishes two modes — because the design concerns are different.

### Build-Time AI
AI assists in writing, testing, or documenting the system during development. No LLM executes when the system runs in production. Primary concerns are verification, structural integrity, and documentation discipline.

### Runtime AI
An LLM executes as part of the live system — processing inputs, generating outputs, or taking actions on behalf of users or other systems. All Build-Time concerns apply, plus:

| Additional Concern | Why It Matters |
|---|---|
| **Prompt Contracts** | Prompts are interfaces — they require the same version control and contract discipline as APIs |
| **Data Boundary Declaration** | Data that cannot legally enter an LLM call must be identified before design is finalized |
| **Human Oversight Model** | Every autonomous action the system can take requires a defined oversight level |
| **Operational Cost Model** | Inference cost is a design constraint — a financially untenable system has failed feasibility |
| **Provider Reliability & Fallback** | LLM provider outages are scheduled events, not edge cases — fallback is a design requirement |
| **Behavioral Evals** | Nondeterministic outputs require class-level correctness criteria, not just deterministic assertions |
| **LLM Observability** | Every AI decision affecting system state must be reconstructable from logs |
| **Model Version Drift** | Pinning delays drift; the Class Drift Audit in Phase 7 exists because pinning eventually fails |
| **Cost Circuit-Breaker** | Automated spend limits prevent runaway LLM cost from becoming a financial incident |

The AI Deployment Mode — Build-Time, Runtime, or Both — is declared at Gate 0 and determines which gate criteria are active throughout all subsequent phases.

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

**AI Deployment Mode**
A declaration of whether AI is present at build time, runtime, or both. Made at Gate 0. Determines which gate criteria are active throughout the SDLC.

**Class Interface Contract**
The schema defining what a valid problem in the class looks like as a system input, and what a valid resolution looks like as an output. Defined before implementation begins. For Runtime AI systems, this includes **Prompt Contracts** — the structured definition of inputs to and expected outputs from any LLM call.

**Data Boundary Declaration**
A documented statement of what data crosses into any LLM call and whether it is subject to classification, residency, or privacy constraints. Required before the Class Interface Contract is finalized for Runtime AI systems.

**Human Oversight Model**
The defined level of human involvement for each action a Runtime AI system can take: autonomous, supervised, or advisory. Determined by action reversibility and blast radius.

**Blast Radius**
The maximum impact of a single failure. Mapped in Phase 2. Minimized in Phase 6. For Runtime AI: explicitly includes LLM provider unavailability and agentic action consequences.

**ADR (Architecture Decision Record)**
A persistent record of major decisions and their reasoning. The long-term memory that neither LLMs nor rotating team members retain naturally.

**Class Drift**
The condition where a system's operational problem class has diverged from its designed problem class without a corresponding design revision. For Runtime AI systems, model version changes are a form of class drift — system behavior may shift even when no code changes.

**Living Document Protocol**
A defined set of triggers — beyond calendar cadence — that require review and update of design artifacts. Prevents documents from becoming liabilities as systems age.

**The Decommission Gate**
When maintenance cost exceeds value, retire cleanly. Revoke access, archive records, purge data — including LLM credentials and logged prompt/response data for Runtime AI systems.

---

## Repository Structure

```
/
├── README.md                   # This file
├── manual.md                   # The full 7-phase SDLC Manual
├── curriculum.md               # The AI Orchestrator's reading list (Levels 0–6)
├── templates/
│   ├── gate-0-concept.md       # Phase 1 worksheet — Problem Class + Success Predicate + AI Deployment Mode
│   ├── gate-1-feasibility.md   # Phase 2 worksheet — Class Volume + Blast Radius + Cost Model
│   ├── gate-2-design.md        # Phase 3 worksheet — Class Interface Contract + Data Boundary + Human Oversight + ADR
│   ├── adr-template.md         # Architecture Decision Record template
│   └── prompt-contract.md      # LLM interface contract template (Runtime AI)
├── examples/
│   └── [worked example]        # End-to-end SDLC applied to a simple agentic system
└── appendix/
    ├── glossary.md
    ├── rigor-by-risk.md
    └── deployment-mode-reference.md
```

---

## How to Use This

**Starting a new project:** Begin at Phase 1. Do not write code until the Problem Class Definition, Success Predicate, and AI Deployment Mode are documented and approved at Gate 0.

**Starting a task within a project:** Apply the Task-Level Gate. If the task touches a data schema, Class Interface Contract, public interface, auth, an external dependency, an LLM call, or introduces new data into an existing LLM call — the gate applies.

**The key question at every gate:**
> Does this serve the defined problem class and Success Predicate, or am I expanding the class without approval?

**Scaling rigor:** See `appendix/rigor-by-risk.md`. Low-risk work requires verbal verification. High-risk work requires formal artifacts, peer review, behavioral evals, and documented stop criteria.

---

## Companion Resources

This README is the orientation. The two primary documents are:

**[manual.md](./manual.md)** — The 7-phase SDLC Manual. Gate questions, mindset shifts, stop criteria, and phase-by-phase design requirements. Start here when beginning a project.

**[curriculum.md](./curriculum.md)** — The AI Orchestrator's reading list. Levels 0–6, from failure mode fundamentals through strategic governance. Explains why the gates exist. Start here when building your foundation.

The curriculum and the manual are designed to be used together — the curriculum explains the *why*, the manual defines the *how*.

---

## Status

`v0.1 — Framework draft. Templates and worked examples in progress.`

Contributions, critiques, and worked examples welcome.
