# 📖 The AI Orchestrator's Curriculum

## The Manifesto

In the age of Large Language Models, the bottleneck of software development has shifted. **Syntax is now a commodity. Context is the new scarcity.**

Most people respond to this shift by becoming better prompt engineers — asking AI for better code. An **AI Orchestrator** responds differently. They treat LLMs as a high-velocity construction crew and themselves as the architect: responsible for the blueprint, the contracts, the verification criteria, and the long-term cost of ownership.

This is not a role that requires the ability to write code. It requires the ability to **define systems precisely enough that AI can safely build them** — and to verify that what was built matches what was designed.

The distinction between a prompt engineer and an AI Orchestrator is not skill level. It is **where you apply your thinking.**

A prompt engineer asks: *"How do I get the AI to write this?"*
An AI Orchestrator asks: *"What class of problems does this system handle, and how do I define that precisely enough that AI can safely build it?"*

This curriculum provides the theoretical foundation for that shift. It maps to the [AI Orchestrator's SDLC Manual](./manual.md) — the curriculum explains *why* the gates exist, the manual defines *how* to pass them.

---

## A Note on the Orchestrator's Role

Nothing in this curriculum assumes you write code. The Orchestrator's job is upstream of code:

- **You define** what the system handles and what it does not.
- **You specify** the contracts that AI and engineers build against.
- **You determine** what "correct" looks like before a single line is written.
- **You require** the verification, observability, and operational standards that make the system trustworthy.
- **AI and engineers execute** against those definitions.

The value of the Orchestrator is not in the implementation — it is in the precision of the design. A vague design produces a system that technically works but is unmaintainable, untestable, and impossible to hand off. A precise design produces a system that AI can build, engineers can verify, and operators can own.

---

## 🛠️ The Orchestrator's Control Artifacts

These are what an Orchestrator produces. They are not code — they are **design artifacts** that constrain what AI can build and define what correct looks like before implementation begins.

| Artifact | Purpose | SDLC Gate |
|---|---|---|
| **Problem Class Definition** | Bounds what the system handles and what it explicitly does not | Gate 0 — Concept Validation |
| **Success Predicate** | Defines the logical condition for correctness at the class level | Gate 0 — Concept Validation |
| **System Context Diagrams (C4)** | Environmental map — where the system lives and what it touches | Gate 2 — Architecture |
| **Class Interface Contracts** | Rigid input/output definitions the AI builds against | Gate 2 — Architecture |
| **Prompt Contracts** | The AI-specific form of interface contracts — what goes into an LLM call and what must come out | Gate 2 — Architecture |
| **ADRs (Architecture Decision Records)** | Long-term memory for decisions that LLMs and rotating teams cannot retain | Gate 2 — Architecture |
| **Behavioral Eval Criteria** | The definition of what the system must prove — which AI or engineers then implement as tests | Gate 3 — Technical Verification |
| **Runbooks & SOPs** | Operational contracts — how the system is owned, not just how it was built | Gate 4 — Operational Readiness |

The curriculum below provides the theoretical grounding for each of these artifacts. Every level maps back to one or more of them.

---

## 🗺️ The Learning Path (Levels 0–6)

---

### Level 0: The Failure Modes of Prompt Engineering (The Entry Point)

*Focus: Understanding why prompt engineering fails at scale — before investing in the alternative.*

This level exists because the rest of the curriculum only makes sense if you understand the specific pain it addresses. If you have never watched a prompt-engineered system become unmaintainable, start here.

**The three failure modes to internalize:**

**1. Structural amnesia.** LLMs have no memory between sessions. Every conversation starts from zero. A system built through iterative prompting accumulates decisions that exist nowhere except in chat history — and chat history is not architecture. The result is a system no one can fully describe, including the person who built it. The Orchestrator's response is documentation that exists outside the conversation: ADRs, class definitions, interface contracts.

**2. Nondeterminism without contracts.** The same prompt produces different outputs across model versions, temperature settings, and time. Without a defined contract for what "correct" looks like at the class level, there is no principled way to know whether the system is working or slowly drifting. The Orchestrator's response is a Success Predicate and behavioral eval criteria defined before implementation begins.

**3. Scope creep as the default.** LLMs are optimized to be helpful. Left unconstrained, they generate more than asked — more features, more abstraction, more complexity. Without explicit class boundaries, the system grows until it is unmaintainable. The Orchestrator's response is a Problem Class Definition with an explicit Anti-Scope.

**Reading:**
- **[How Complex Systems Fail](https://how.complexsystems.fail/) — Dr. Richard Cook.** Eighteen observations about why failures in complex systems are rarely caused by a single root cause. Apply this to AI-assisted development: "AI hallucination" is not a primary cause of failure — it is a symptom of absent contracts, undefined class boundaries, and insufficient verification criteria. This reframe is the foundation of the Orchestrator mindset.

---

### Level 1: Mental Models (The Foundation)

*Focus: Understanding how parts interact to form a whole.*

- **Thinking in Systems — Donella Meadows.** Feedback loops, stocks, flows, and leverage points. Essential for defining a Success Predicate that actually measures system behavior rather than a local proxy metric. If you cannot describe the feedback loop your system creates, you do not yet understand what you are building. Non-coders often have an advantage here — systems thinking is not about code, it is about relationships between components.

- **A Philosophy of Software Design — John Ousterhout.** The concept of "Deep Modules" — interfaces that are simple on the outside but handle substantial complexity inside. As an Orchestrator, use this to evaluate whether AI has produced a clean design or shallow sprawl. You do not need to read the code to ask: *"Is this interface simple? Can someone who didn't build it use it without understanding its internals?"* If the answer is no, the design has failed regardless of whether the code works.

---

### Level 2: Contract-First Design (The Language of Intent)

*Focus: Creating the rules of engagement that AI cannot break.*

- **[OpenAPI / JSON Schema](https://swagger.io/specification/) — Concepts, not syntax.** Schemas define what valid inputs and outputs look like for a system — the shape of data that crosses a boundary. As an Orchestrator, you do not write schemas; you define the *requirements* that schemas must enforce, and AI or engineers produce the schemas against those requirements. The Orchestrator's Rule: never ask AI to build anything until it has agreed to a contract. The contract is not documentation — it is the constraint. Understanding what schemas are and what they enforce is sufficient. Writing them is not required.

- **[Design Patterns](https://refactoring.guru/design-patterns) — Refactoring.Guru.** Patterns are compressed context — a shared vocabulary between the Orchestrator and the construction crew. Telling AI to implement a "Strategy Pattern" or an "Observer Pattern" is more precise and more efficient than describing the behavior in prose. You do not need to implement patterns; you need to recognize which pattern fits the problem class and direct AI accordingly. Refactoring.Guru uses visual diagrams and plain-language explanations that do not require coding experience.

- **[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — Yao et al.** The foundational paper for understanding how AI agents interleave reasoning and action. Before designing any system where AI takes real-world actions — sending messages, modifying data, triggering deployments — understand what is happening underneath. The Orchestrator must define the boundary between AI reasoning steps and AI executable actions. This paper shows what that boundary looks like in practice. Read the abstract and the examples; the mathematical notation is not required.

---

### Level 3: Structural Mapping (The Blueprint)

*Focus: Defining boundaries so AI does not create unmaintainable systems.*

- **[The C4 Model](https://c4model.com/) — Simon Brown.** A four-level diagramming approach for describing software systems. Focus on Level 1 (Context — what the system is and what it talks to) and Level 2 (Container — what the major components are). These diagrams are the Orchestrator's primary design tool — they keep AI's worldview consistent across sessions and communicate the Problem Class boundary visually. C4 diagrams require no coding knowledge. They are boxes, arrows, and labels. The C4 website includes free tooling and templates.

- **[Context Mapping](https://github.com/ddd-crew/context-mapping) — Domain-Driven Design.** A method for defining where one system ends and another begins. This is the theoretical foundation of the Class Interface Contract — you cannot write a contract for an interface you have not yet bounded. Context Mapping gives non-coders a rigorous vocabulary for the conversations that happen at system boundaries: who owns what, what agreements exist between systems, and what happens when those agreements change.

- **Context Engineering — Emerging Practice.** How to structure and manage what AI knows at each step of a long-running workflow. LLMs degrade as their context windows fill — an AI agent that has lost track of its own state is a liability, not an asset. As an Orchestrator, you do not implement context management; you require it as a design constraint and ask the right questions: *"What does the AI know at this step? What has it forgotten? How do we ensure it has what it needs without exceeding its limits?"* Follow Anthropic's published research and practitioner writing in this space for the current state of the art.

---

### Level 4: Verification & Integrity (The Safety Net)

*Focus: Defining what correct looks like so that AI and engineers can prove it.*

- **Test-Driven Design as Philosophy — Kent Beck (adapted).** The Orchestrator's version of test-driven development is not about writing tests — it is about defining the conditions that tests must verify before implementation begins. This is a design discipline, not a coding discipline. Before directing AI to build anything, answer: *"What must be true for this to be considered correct? What inputs should produce what outputs? What should happen at the class boundary?"* Those answers become the criteria that AI or engineers implement as tests. The philosophy matters more than the syntax.

- **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/).** The specific risks introduced by AI-generated code and agentic systems — prompt injection, insecure output handling, excessive agency, and others. As an Orchestrator, you do not fix these vulnerabilities; you design against them at Phase 3 and require that they be addressed before Gate 4. Understanding what they are and why they occur is sufficient. This document is written for a general technical audience and does not require coding experience.

- **LLM Evaluation — Hamel Husain.** [Hamel's writing on LLM evals](https://hamel.dev) addresses a largely unsolved problem: how do you verify that an AI system is producing correct outputs when "correct" cannot always be defined as an exact match? The Orchestrator's role is to define the behavioral eval criteria — the description of what good looks like, including edge cases and failure modes — and to require that AI or engineers implement those criteria as automated checks. Domain expertise, not coding expertise, is what makes eval criteria valuable. A non-coder who deeply understands the problem class will write better eval criteria than a coder who does not.

- **[Black-Box Thinking](https://www.softwaretestinghelp.com/black-box-testing/).** Verifying a system by its inputs and outputs, without knowledge of its internal implementation. For an Orchestrator who does not read code, black-box thinking is not a limitation — it is the natural verification mode. You define what goes in and what must come out. The Class Interface Contract is a black-box specification. Require that verification suites test the contracts you defined, and evaluate results at the boundary level. Internal implementation is the engineer's domain. Correctness at the boundary is the Orchestrator's.

---

### Level 5: Observability & Socio-Technical Strategy (The Maintenance Loop)

*Focus: Ensuring the system remains human-readable and operationally honest over time.*

- **Team Topologies — Skelton & Pais.** Cognitive Load is the metric that determines whether a system is maintainable or a liability from day one. If the system exceeds the cognitive load of the team that owns it, it will be abandoned or worked around — regardless of how well it was built. As an Orchestrator, design for cognitive load as a first-class constraint: *"Can the team that will own this system understand it well enough to operate, debug, and evolve it?"* If not, the design is not finished.

- **Accelerate — Nicole Forsgren et al.** Four metrics that determine whether a system is actually improving engineering outcomes: Deployment Frequency, Lead Time for Changes, Mean Time to Recovery (MTTR), and Change Failure Rate. Establish baselines at Phase 7. A system that ships quickly but degrades recovery time has not improved engineering — it has moved risk. These metrics do not require technical implementation knowledge to understand or to require.

- **Observability for Agentic Systems.** The ability to reconstruct what happened inside a system after the fact. For AI systems, this means every AI decision that affects system state must be reconstructable from logs. As an Orchestrator, you do not configure observability tools — you require observability as a Phase 3 design constraint and evaluate it at Gate 4. The questions to ask: *"Can we see what the AI was given as input? Can we see what it decided? Can we see what it did? Can we reconstruct a failure without the original builder?"* If any answer is no, the system is not ready for production. Tools in this space include LangSmith and Langfuse for LLM-specific tracing; understanding what they provide is more important than knowing how to configure them.

---

### Level 6: Strategic Governance (The Long Game)

*Focus: Managing the evolution of a system class over years, not sprints.*

- **[Architecture Decision Records (ADRs)](https://adr.github.io/).** A lightweight method for documenting design decisions — what was decided, why, what alternatives were considered, and what the consequences are. ADRs are written at the moment of decision, not retrospectively. They are the Orchestrator's primary tool for ensuring that the reasoning behind design choices survives team changes, model updates, and time. An ADR requires no technical knowledge to write — it requires the discipline to document decisions before moving on. This is where the Orchestrator's long-term value compounds.

- **[Wardley Mapping](https://learnwardleymapping.com/).** A strategic tool for deciding what to build vs. what to buy or use as a commodity. Applied to AI orchestration: use Wardley Maps to determine which components of your system class are genuinely differentiated and which should be delegated to existing tools or services. This prevents the common failure mode of directing AI to build custom infrastructure for commodity problems. Wardley Mapping requires no technical background — it is a strategy and positioning tool that happens to apply well to technology decisions.

- **[Failure Mode and Effects Analysis (FMEA)](https://asq.org/quality-resources/fmea).** A systematic method for identifying failure modes before they occur — what could fail, why, and what the downstream effect would be. Apply this in Phase 3 when mapping unhappy paths and class boundary behavior. As an Orchestrator, FMEA is a design conversation, not a technical analysis: *"What breaks here? What happens downstream when it does? How do we reduce the blast radius?"* Domain knowledge drives better FMEA than technical knowledge does.

---

## 📋 Prerequisites for the Transition

To move from prompt engineer to AI Orchestrator, develop these three capabilities:

**Structural Reading.** The ability to evaluate a system's design through diagrams, contracts, and ADRs — not source code. An Orchestrator who can read a C4 diagram, evaluate a class interface contract, and identify gaps in an ADR can govern a system they cannot implement. This is the primary verification skill for non-coding architects.

**Abstraction Discipline.** The ability to describe systems in terms of boundaries, interfaces, and data flows rather than features and implementation details. The Class Interface Contract requires this — you must be able to define what the system does at its boundary before specifying, or directing AI to determine, how it does it. This is a design skill, not a technical skill.

**Adversarial Specification.** The ability to define failure cases, class boundary scenarios, and edge cases that verification must cover — before implementation begins. The default AI system handles the happy path. Your job as Orchestrator is to specify the adversarial cases that reveal whether the class definition holds under real conditions. Domain expertise, not coding expertise, is what makes these specifications valuable.

---

## 🚀 How to Navigate This Curriculum

**Levels 0–2** are for immediate improvement in daily AI-directed work. Start here regardless of experience level.

**Levels 3–4** are for Orchestrators designing multi-component or production systems. Apply these before Phase 3 of any high-risk SDLC engagement.

**Levels 5–6** are for Orchestrators managing systems over time or governing teams that use AI at scale. The governance and observability concerns here become critical as systems age.

The curriculum is not a prerequisite for the manual — you can apply the SDLC framework before finishing the reading list. But every gate in the manual will make more sense with the corresponding theoretical foundation behind it.
