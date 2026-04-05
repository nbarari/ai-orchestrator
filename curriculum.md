# 📖 The AI Orchestrator's Curriculum

## The Manifesto

In the age of Large Language Models, the bottleneck of software development has shifted. **Syntax is now a commodity. Context is the new scarcity.**

Most engineers respond to this shift by becoming better prompt engineers — asking AI for better code. An **AI Orchestrator** responds differently. They treat LLMs as a high-velocity construction crew and themselves as the architect: responsible for the blueprint, the contracts, the verification, and the long-term cost of ownership.

The distinction is not about skill level. It is about **where you apply your thinking.**

A prompt engineer asks: *"How do I get the AI to write this?"*
An AI Orchestrator asks: *"What class of problems does this system handle, and how do I define that precisely enough that AI can safely build it?"*

This curriculum provides the theoretical foundation for that shift. It maps to the [AI Orchestrator's SDLC Manual](./manual.md) — the curriculum explains *why* the gates exist, the manual defines *how* to pass them.

---

## 🛠️ The Orchestrator's Control Artifacts

Before the reading list: understand what an Orchestrator produces. These are not deliverables in the traditional sense — they are **control artifacts** that constrain what AI can build and prove that what it built is correct.

| Artifact | Purpose | SDLC Gate |
|---|---|---|
| **Problem Class Definition** | Bounds what the system handles and what it explicitly does not | Gate 0 — Concept Validation |
| **Success Predicate** | Defines the logical condition for correctness at the class level | Gate 0 — Concept Validation |
| **System Context Diagrams (C4)** | Environmental map — where the system lives and what it touches | Gate 2 — Architecture |
| **Class Interface Contracts (Schema)** | Rigid input/output constraints the AI cannot violate | Gate 2 — Architecture |
| **Prompt Contracts** | The AI-specific form of interface contracts — versioned, typed, and enforced | Gate 2 — Architecture |
| **ADRs (Architecture Decision Records)** | Long-term memory for decisions that LLMs and rotating teams cannot retain | Gate 2 — Architecture |
| **Behavioral Eval Suites** | Proof of class-level correctness for nondeterministic systems | Gate 3 — Technical Verification |
| **Runbooks & SOPs** | Operational contracts — how the system is owned, not just how it was built | Gate 4 — Operational Readiness |

The curriculum below provides the theoretical grounding for each of these artifacts. Every level maps back to one or more of them.

---

## 🗺️ The Learning Path (Levels 0–6)

---

### Level 0: The Failure Modes of Prompt Engineering (The Entry Point)

*Focus: Understanding why prompt engineering fails at scale — before investing in the alternative.*

This level exists because the rest of the curriculum only makes sense if you have felt the specific pain it addresses. If you have never shipped a prompt-engineered system and watched it become unmaintainable, start here.

**The three failure modes to internalize:**

**1. Structural amnesia.** LLMs have no memory between sessions. Every conversation starts from zero. A system built through iterative prompting accumulates decisions that exist nowhere except in chat history — and chat history is not architecture. The result is a system no one can fully describe, including the person who built it.

**2. Nondeterminism without contracts.** The same prompt produces different outputs across model versions, temperature settings, and time. Without a defined contract for what "correct" looks like at the class level, there is no principled way to know whether the system is working or slowly drifting.

**3. Scope creep as the default.** LLMs are optimized to be helpful. Left unconstrained, they will generate more than you asked for — more features, more abstraction layers, more complexity. Without explicit class boundaries, the system grows until it is unmaintainable.

**Reading:**
- **[How Complex Systems Fail](https://how.complexsystems.fail/) — Dr. Richard Cook.** Eighteen observations about why failures in complex systems are rarely caused by a single root cause. Apply this to AI-assisted development: "AI hallucination" is not a primary cause of failure — it is a symptom of absent contracts, undefined class boundaries, and insufficient verification. Essential reframe before proceeding.

---

### Level 1: Mental Models (The Foundation)

*Focus: Understanding how parts interact to form a whole.*

- **Thinking in Systems — Donella Meadows.** Feedback loops, stocks, flows, and leverage points. Essential for defining a Success Predicate that actually measures system behavior rather than a local proxy metric. If you cannot draw the feedback loop your system creates, you do not yet understand the system.

- **A Philosophy of Software Design — John Ousterhout.** The concept of "Deep Modules" — interfaces that are simple but hide substantial complexity. Use this to evaluate AI-generated code: does it create deep modules or shallow sprawl? The AI's default is shallow. Your job as Orchestrator is to enforce depth through interface contracts.

---

### Level 2: Contract-First Design (The Language of Intent)

*Focus: Creating the rules of engagement that AI cannot break.*

- **[OpenAPI / JSON Schema](https://swagger.io/specification/).** Schemas are the primary source of truth. **The Orchestrator's Rule:** Never ask AI to write code until it has agreed to a schema. This applies equally to data contracts between services and to prompt contracts between your system and an LLM. The schema is not documentation — it is the constraint.

- **[Design Patterns](https://refactoring.guru/design-patterns) — Refactoring.Guru.** Patterns are compressed context. Telling an AI to implement a "Strategy Pattern" is more precise and more efficient than describing the behavior in prose. Patterns are the shared vocabulary between the Orchestrator and the construction crew.

- **[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — Yao et al.** The foundational paper for agentic AI systems. Understand how LLMs interleave reasoning and action before designing any system where AI takes real-world actions. The Prompt Contract for an agentic component must define the boundary between reasoning steps and executable actions — this paper shows you what that boundary looks like in practice.

---

### Level 3: Structural Mapping (The Blueprint)

*Focus: Defining boundaries so AI does not create spaghetti infrastructure.*

- **[The C4 Model](https://c4model.com/) — Simon Brown.** Focus on Level 1 (Context) and Level 2 (Container) diagrams. These are the visual maps that keep the AI's worldview consistent across sessions. A context diagram is also the most efficient way to communicate the Problem Class boundary — what is inside the system and what is explicitly outside it.

- **[Context Mapping](https://github.com/ddd-crew/context-mapping) — Domain-Driven Design.** Bounded Contexts define where one system ends and another begins. This is the theoretical foundation of the Class Interface Contract — you cannot write a contract for an interface you have not yet bounded. Apply this before Phase 3 of the SDLC.

- **[Context Engineering](https://www.anthropic.com/research) — Emerging Practice.** How to structure, compress, and retrieve context across long-running agentic workflows. LLMs degrade as context windows fill — understanding how to manage what the AI knows at each step is foundational to building systems that maintain coherent behavior over time. Supplement with Anthropic's published research on context management and retrieval-augmented generation patterns.

---

### Level 4: Verification & Integrity (The Safety Net)

*Focus: Proving the AI's output is correct without reading every line of code.*

- **Test-Driven Development — Kent Beck.** As an Orchestrator, the test suite is written first — or directed first, if AI writes it. The test is the cage that AI-generated code must live in. TDD discipline applied to AI-assisted development means: define the behavioral contract before asking AI to implement it. The test is a form of the Class Interface Contract made executable.

- **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/).** The specific security vulnerabilities introduced by AI-generated code and agentic systems. Prompt injection, insecure output handling, and excessive agency are not theoretical — they are the failure modes of systems built without Phase 3 rigor. Read this before designing any system where AI outputs influence real-world state.

- **LLM Evaluation — Hamel Husain.** [Hamel's writing on LLM evals](https://hamel.dev) is the most practical available treatment of a largely unsolved problem: how do you systematically verify LLM output quality at the system level? The behavioral eval suites in Phase 5 of the SDLC require this thinking. Golden output sets, domain expert review, and failure taxonomy are the tools. This is where the nondeterminism problem gets addressed — not by eliminating it, but by defining what class-level correctness looks like despite it.

- **[Black-Box Testing Principles](https://www.softwaretestinghelp.com/black-box-testing/).** Verifying inputs and outputs rather than internal logic. For AI systems, internal logic is often opaque by definition — black-box testing is not a fallback, it is the primary verification strategy. Apply this to prompt contracts the same way you would apply it to any external API.

---

### Level 5: Observability & Socio-Technical Strategy (The Maintenance Loop)

*Focus: Ensuring the system is human-readable and operationally honest for the long haul.*

- **Team Topologies — Skelton & Pais.** Cognitive Load is the metric that determines whether an AI-generated system is maintainable or a legacy nightmare from day one. If the system exceeds the cognitive load of the team that owns it, it will be abandoned or worked around. Design for cognitive load as a first-class constraint in Phase 3.

- **Accelerate — Nicole Forsgren et al.** MTTR, Lead Time, Deployment Frequency, Change Failure Rate. These are the metrics that determine whether your AI-assisted workflow is actually productive or just fast at creating problems. Establish baselines at Phase 7 Gate 5. A system that ships quickly but degrades MTTR has not improved engineering.

- **Observability for Agentic Systems — OpenTelemetry + LLM-Specific Tracing.** Distributed tracing (OpenTelemetry), LLM-specific observability tools (LangSmith, Langfuse), and structured logging of prompt/response pairs are not optional for production AI systems — they are how you audit class drift, diagnose failures, and satisfy the Phase 5 traceability requirement. The principle: every AI decision that affects system state must be reconstructable from logs. Understand this before Phase 6.

---

### Level 6: Strategic Governance (The Long Game)

*Focus: Managing the evolution of a system class over years, not sprints.*

- **[Architecture Decision Records (ADRs)](https://adr.github.io/).** Every major decision must be documented with its context and reasoning. This is the long-term memory that LLMs cannot provide and that rotating teams will need. ADRs are not retrospective documentation — they are written at the moment of decision, at Gate 2, before implementation begins.

- **[Wardley Mapping](https://learnwardleymapping.com/).** A strategy tool for deciding what to build with AI (Custom) vs. what to buy or use as commodity. Applied to AI orchestration: use Wardley Maps to determine which components of your system class are genuinely differentiated and which should be delegated to existing tools or services. Prevents the common failure mode of building custom infrastructure for commodity problems.

- **[Failure Mode and Effects Analysis (FMEA)](https://asq.org/quality-resources/fmea).** A systematic method for identifying failure modes, their causes, and their downstream effects. Apply this in Phase 3 when mapping unhappy paths and class boundary behavior. More directly applicable than the NASA Systems Engineering Handbook for most software contexts — same rigor, lower translation overhead.

---

## 📋 Prerequisites for the Transition

To move from prompt engineer to AI Orchestrator, develop these three capabilities before the technical reading:

**Reading over Writing.** You must be able to identify architectural problems in code you did not write — and code the AI wrote. If you can only evaluate code you produced yourself, you cannot verify what the construction crew built.

**Abstraction Mastery.** Describe systems in terms of interfaces, data flows, and state machines rather than implementation details. The Class Interface Contract requires this — you must be able to define what the system does at the boundary level before specifying how it does it.

**Defensive Verification.** Write tests — or direct AI to write tests — that specifically target failure modes and class boundary cases identified in Phase 3. The default AI test suite covers the happy path. Your job is to define the adversarial cases.

---

## 🚀 How to Navigate This Curriculum

**Levels 0–2** are for immediate improvement in daily AI-assisted work. Start here regardless of experience level.

**Levels 3–4** are for engineers building multi-component or production systems. Apply these before Phase 3 of any High-risk SDLC engagement.

**Levels 5–6** are for engineers managing systems over time or leading teams that use AI at scale. The governance and observability concerns here become critical as systems age.

The curriculum is not a prerequisite for the manual — you can use the SDLC framework before finishing the reading list. But every gate in the manual will make more sense with the corresponding theoretical foundation behind it.
