# The AI Orchestrator's Curriculum

## Overview

Large Language Models have changed where the bottleneck in software development sits. Writing code is no longer the hard part. Defining what should be built, specifying it precisely enough that AI can build it correctly, and verifying the result without reading every line of output — that is where the work is now.

This curriculum covers the theoretical foundation for that kind of work. It is organized as a reading list across six levels, from failure mode fundamentals through long-term governance. Each level maps to one or more phases in the [AI Orchestrator's SDLC Manual](./manual.md).

---

## The Orchestrator's Role

Nothing in this curriculum assumes coding ability. The Orchestrator's work happens upstream of implementation:

- Defining what the system handles and what it does not
- Specifying the contracts that AI and engineers build against
- Determining what "correct" looks like before implementation begins
- Requiring the verification, observability, and operational standards that make the system trustworthy

AI and engineers execute against those definitions. The Orchestrator is responsible for the precision of the design. A vague design produces a system that may technically function but cannot be verified, transferred, or maintained. A precise design can be built by AI, verified by engineers, and operated by whoever takes ownership.

---

## AI Deployment Mode

Before working through this curriculum, identify which of the following applies to your system. The concerns differ substantially.

**Build-Time AI:** AI assists in writing, testing, or documenting the system during development. No LLM runs when the system is in production. Primary concerns are verification, structural integrity, and documentation discipline.

**Runtime AI:** An LLM executes as part of the live system, processing inputs, generating outputs, or taking actions. All Build-Time concerns apply, plus: operational cost, data classification, provider reliability, observability, and human oversight of autonomous actions.

**Both:** The system is built with AI assistance and runs AI components in production. All concerns apply.

Where a concern applies only to Runtime AI, it is noted explicitly throughout this curriculum.

---

## Control Artifacts

The Orchestrator's primary output is design artifacts, not code. These artifacts constrain what AI can build and define correctness before implementation begins.

| Artifact | Purpose | SDLC Gate |
|---|---|---|
| Problem Class Definition | Bounds what the system handles and what it explicitly does not | Gate 0 |
| Success Predicate | Defines the logical condition for correctness at the class level | Gate 0 |
| AI Deployment Mode | Declares whether AI is present at build time, runtime, or both | Gate 0 |
| System Context Diagrams (C4) | Maps where the system lives and what it connects to | Gate 2 |
| Class Interface Contracts | Defines the input/output schema the AI builds against | Gate 2 |
| Prompt Contracts | Defines the structure of inputs to and expected outputs from each LLM call | Gate 2 |
| Data Boundary Declaration | Documents what data crosses into LLM calls and any applicable constraints | Gate 2 |
| Human Oversight Model | Defines which system actions are autonomous, supervised, or advisory | Gate 2 |
| ADRs (Architecture Decision Records) | Records design decisions and their reasoning for future reference | Gate 2 |
| Behavioral Eval Criteria | Defines what the system must demonstrate; engineers implement the tests | Gate 3 |
| Runbooks and SOPs | Documents how the system is operated and maintained | Gate 4 |

---

## Learning Path

### Level 0: Failure Modes of Prompt Engineering

*Why prompt engineering fails at scale, before investing in the alternative.*

Three failure modes recur in systems built primarily through iterative prompting:

**Structural amnesia.** LLMs have no memory between sessions. Decisions accumulate in chat history rather than in durable documentation. The result is a system that cannot be explained, modified, or handed off with confidence. The corrective is documentation that lives outside the conversation: ADRs, class definitions, interface contracts.

**Nondeterminism without contracts.** The same prompt produces different outputs across model versions, temperature settings, and time. Without a defined contract for what correct looks like at the class level, there is no principled way to detect whether the system is working or drifting. The corrective is a Success Predicate and behavioral eval criteria defined before implementation begins. Note that defining correctness criteria for nondeterministic systems is an active area of development in the field; what matters most is the precision of the criteria, not the specific testing methodology used.

**Scope creep as the default.** LLMs generate more than asked when left unconstrained. Without explicit class boundaries, systems grow until they cannot be maintained. The corrective is a Problem Class Definition with an explicit Anti-Scope.

**Reading:**
[How Complex Systems Fail](https://how.complexsystems.fail/) by Dr. Richard Cook. Eighteen observations on failure in complex systems. The central reframe for this curriculum: AI hallucination is a symptom of absent contracts and undefined boundaries, not a root cause.

---

### Level 1: Mental Models

*Understanding how components interact as a system.*

**Thinking in Systems by Donella Meadows.** Covers feedback loops, stocks, flows, and leverage points. Useful for defining a Success Predicate that measures actual system behavior rather than a proxy metric. Systems thinking does not require coding ability; it concerns relationships between components, which is where the Orchestrator's work is focused.

**A Philosophy of Software Design by John Ousterhout.** Introduces the concept of deep modules: interfaces that are simple on the outside and handle substantial complexity inside. Useful for evaluating whether AI has produced a clean design. The relevant question is not whether the code is correct but whether the interface is simple enough that someone unfamiliar with the implementation can use it correctly.

---

### Level 2: Contract-First Design

*Defining the rules of engagement before implementation begins.*

**[OpenAPI / JSON Schema](https://swagger.io/specification/) — concepts, not syntax.** Schemas define the shape of data that crosses a system boundary. The Orchestrator's role is to define the requirements that schemas must enforce; AI or engineers produce the schemas against those requirements. Writing schemas is not required. Understanding what they constrain and why they matter is.

The core rule: do not ask AI to build anything until it has agreed to a contract. The contract is the constraint, not documentation of something that already exists.

**[Design Patterns](https://refactoring.guru/design-patterns) by Refactoring.Guru.** Patterns are compressed vocabulary for communicating intent to AI. Specifying that a component should use a Strategy Pattern or an Observer Pattern is more precise and more efficient than describing the behavior in prose. Refactoring.Guru presents patterns with diagrams and plain-language explanations that do not require coding experience.

**Stateless service design.** Systems that maintain state inside a running process are difficult to scale and recover. As an Orchestrator, require that engineers explain where state lives and how it is managed. State should live in an external store, not inside the service. This is a design question, not an implementation question. *Applies to Runtime AI systems.*

**[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) by Yao et al.** The foundational paper for understanding how AI agents interleave reasoning and action. The Orchestrator must define the boundary between AI reasoning steps and AI executable actions before any agentic system is designed. This paper establishes the vocabulary for that boundary. Reading the abstract and examples is sufficient; the mathematical notation is not required. Note that the field has moved significantly since this paper's 2022 publication. Read it for the mental model, then supplement with current practitioner writing for implementation patterns. *Applies to Runtime AI systems.*

---

### Level 3: Structural Mapping

*Defining system boundaries so AI does not produce unmaintainable output.*

**[The C4 Model](https://c4model.com/) by Simon Brown.** A four-level diagramming approach for describing software systems. Focus on Level 1 (Context: what the system is and what it connects to) and Level 2 (Container: what the major components are). These diagrams are the Orchestrator's primary tool for keeping AI's worldview consistent across sessions and for communicating Problem Class boundaries visually. C4 diagrams require no coding knowledge; they use boxes, arrows, and labels. The C4 website provides free tooling and templates.

**[Context Mapping](https://github.com/ddd-crew/context-mapping) from Domain-Driven Design.** A method for defining where one system ends and another begins. You cannot write a contract for an interface that has not been bounded. Context Mapping provides a rigorous vocabulary for conversations at system boundaries: who owns what, what agreements exist, and what happens when those agreements change.

**Context engineering.** How to structure and manage what AI knows at each step of a long-running workflow. LLM performance degrades as context windows fill. An agent that has lost track of its own state becomes unpredictable. As an Orchestrator, require context management as a design constraint and ask: what does the AI know at this step, what has it lost, and what happens when context is exhausted mid-task? This is an active area of research. Follow Anthropic's published work and current practitioner writing rather than relying on any single source. *Applies to Runtime AI systems.*

---

### Level 4: Verification and Integrity

*Defining what correct looks like so that AI and engineers can demonstrate it.*

**Test-driven design as philosophy, adapted from Kent Beck.** The Orchestrator's application of this principle is not about writing tests. It is about specifying the conditions that tests must verify before implementation begins. Before directing AI to build anything, answer: what must be true for this to be considered correct, what inputs should produce what outputs, and what should happen at the class boundary? Those answers become the criteria that AI or engineers implement as tests. The discipline of specifying correctness before implementation is the transferable principle.

**[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/).** Covers the specific risks introduced by AI-generated code and agentic systems, including prompt injection, insecure output handling, and excessive agency. The Orchestrator's role is to design against these risks in Phase 3 and require that they are addressed before Gate 4. This document is written for a general technical audience and does not require coding experience. *Applies to Runtime AI systems; some items also apply to Build-Time AI.*

**LLM evaluation methodology.** Verifying that an AI system produces correct outputs when correctness cannot be defined as an exact string match is a largely unsolved problem at the industry level. The Orchestrator defines the behavioral eval criteria: what good looks like, what failure looks like, and what the boundary cases are. AI or engineers implement those criteria using whatever methodology is current. Domain expertise in the problem class produces better eval criteria than coding expertise does. [Hamel Husain's writing on evals](https://hamel.dev) is a useful practitioner entry point, though the field is moving quickly enough that it should be treated as a starting point rather than a definitive reference. *Applies to Runtime AI systems.*

**[Black-box testing principles](https://www.softwaretestinghelp.com/black-box-testing/).** Verifying a system by its inputs and outputs without knowledge of its internal implementation. For an Orchestrator who does not read code, this is the natural verification mode. The Class Interface Contract is a black-box specification. Require that verification suites demonstrate compliance with the contracts defined in Phase 3.

---

### Level 5: Observability and Socio-Technical Strategy

*Keeping the system operationally honest over time.*

**Team Topologies by Skelton and Pais.** Introduces cognitive load as a design constraint. A system that exceeds the cognitive load of the team that owns it will be worked around or abandoned regardless of how well it was built. Before finalizing a design, verify that the team responsible for operating it can understand it well enough to debug and evolve it.

**Accelerate by Nicole Forsgren et al.** Covers four metrics for evaluating whether a system improves engineering outcomes: Deployment Frequency, Lead Time for Changes, Mean Time to Recovery, and Change Failure Rate. Establish baselines at Phase 7. A system that ships quickly but increases recovery time has traded one problem for another.

**Observability for agentic systems.** The ability to reconstruct what happened inside a system after the fact. For AI systems, each AI decision that affects system state must be reconstructable from logs. As an Orchestrator, require observability as a Phase 3 design constraint and verify it at Gate 4. Key questions: can we see what the AI was given as input, what it decided, and what it did? Can we reconstruct a failure without access to the original builder? Is the logging approach compliant with the Data Boundary Declaration? LLM-specific observability tooling, which captures prompt/response pairs and agent decision traces, is an active and fast-moving category. LangSmith and Langfuse are current examples; evaluate options at implementation time. *Applies to Runtime AI systems.*

---

### Level 6: Strategic Governance

*Managing the evolution of a system class over years.*

**[Architecture Decision Records](https://adr.github.io/).** A lightweight format for documenting design decisions: what was decided, why, what alternatives were considered, and what the consequences are. ADRs are written at the moment of decision, not after the fact. Writing an ADR requires no technical knowledge, only the discipline to record decisions before moving on. For Runtime AI systems, ADRs should include model version rationale, human oversight decisions, and data boundary decisions, as these are the choices most likely to require revisiting as the system ages.

**[Wardley Mapping](https://learnwardleymapping.com/).** A tool for deciding what to build versus what to buy or use as a commodity. Applied here: use Wardley Maps to identify which components of a system class are genuinely differentiated and which should be delegated to existing tools. The common failure mode is directing AI to build custom infrastructure for problems that commodity tooling already solves.

**[Failure Mode and Effects Analysis (FMEA)](https://asq.org/quality-resources/fmea).** A systematic method for identifying failure modes before they occur: what could fail, why, and what the downstream effect would be. Apply this in Phase 3 when mapping unhappy paths and class boundary behavior. For Runtime AI systems, explicitly include LLM provider unavailability, model version deprecation, and cost overrun. These are routine events in the lifecycle of a production AI system, not edge cases. Domain knowledge produces better FMEA than technical knowledge does.

---

## Prerequisites

Three capabilities support the transition from prompt engineer to Orchestrator. None requires coding experience.

**Structural reading.** The ability to evaluate a system's design through diagrams, contracts, and ADRs. An Orchestrator who can read a C4 diagram, evaluate a class interface contract, and identify gaps in an ADR can govern a system they did not implement.

**Abstraction discipline.** The ability to describe systems in terms of boundaries, interfaces, and data flows rather than features or implementation details. The Class Interface Contract requires this. You must define what the system does at its boundary before specifying how it does it.

**Adversarial specification.** The ability to define failure cases, boundary scenarios, and edge cases that verification must cover, before implementation begins. AI-generated systems tend to handle the happy path. The Orchestrator's job is to specify the cases that stress-test whether the class definition holds under real conditions. Domain expertise in the problem class is the primary input here.

---

## Navigation

**Levels 0 through 2** apply immediately to daily AI-directed work. Start here.

**Levels 3 and 4** apply when designing multi-component or production systems. Work through these before Phase 3 of any high-risk SDLC engagement.

**Levels 5 and 6** apply when managing systems over time or governing teams that use AI at scale.

The curriculum is not a prerequisite for the manual. The SDLC framework can be applied before finishing the reading list. Each level provides context that makes the corresponding gate questions more legible.
