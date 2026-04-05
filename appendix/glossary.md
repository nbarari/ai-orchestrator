# Glossary

Definitions for terms used in the AI Orchestrator framework. Where a term appears in the manual or templates, it carries the meaning defined here.

---

**ADR (Architecture Decision Record)**
A file capturing a design decision, the context that made it necessary, the alternatives that were considered, and the consequences of the choice. Written at the moment of decision, not retrospectively. Stored in `docs/adr/`.

**Anti-Scope**
The explicit declaration of what a system does not handle. Documented alongside the Problem Class Definition in Gate 0. A system without an Anti-Scope has no enforceable boundary.

**Behavioral Eval**
A test that verifies class-level correctness of nondeterministic outputs against criteria defined by the Orchestrator. The criteria take precedence over the testing methodology, which is the engineer's determination. Behavioral evals cover the cases where exact output matching is not a valid correctness criterion.

**Blast Radius**
The maximum potential impact of a single component failure or change. Mapped in Phase 2 for each downstream consumer. Minimized in Phase 6 through staged activation and kill switches.

**BOM (Bill of Materials)**
A complete list of all infrastructure resources, libraries, services, and implementation artifacts required by the system. Produced in Phase 3.

**Build-Time AI**
AI used during the development process to write, test, or document the system. No LLM executes when the system runs in production. Contrast with Runtime AI.

**C4 Model**
A four-level diagramming approach for describing software systems: Context, Container, Component, and Code. This framework uses Level 1 (Context) and Level 2 (Container). See https://c4model.com.

**Class Boundary**
The explicit definition of what inputs fall within the problem class versus adjacent to it. Adjacent inputs are not errors; they are a design case that must be handled explicitly.

**Class Boundary Behavior**
The defined behavior of the system when it receives an input that is adjacent to the problem class but outside it. A design decision made in Phase 3, not an implementation detail.

**Class Drift**
The condition where a system's operational behavior has diverged from its designed problem class without a corresponding design revision. For Runtime AI systems, model version changes can produce class drift even when no code changes. Detected in the Phase 7 Class Drift Audit.

**Class Interface Contract**
The schema defining what a valid input looks like and what a valid output looks like at the system boundary. The primary design artifact of Phase 3. No implementation begins until this contract exists. For Runtime AI systems, includes Prompt Contracts for each LLM call.

**Class Volume Analysis**
An assessment of the expected cardinality and distribution of problems in the problem class: steady and low, bursty, or continuous and high-volume. Produced in Phase 2 to validate that the design assumption matches the actual volume profile.

**Data Boundary Declaration**
A documented statement of what data crosses into any LLM call and whether it is subject to data classification, residency requirements, privacy regulation, or internal policy constraints. Required before the Class Interface Contract is finalized for Runtime AI systems. A blocking requirement; if uncertain, escalate to data governance or legal before proceeding.

**Human Oversight Model**
The defined level of human involvement for each action a Runtime AI system can take. Three levels: autonomous (AI acts without human confirmation), supervised (human reviews before execution), advisory (human decides, AI informs). Determined by action reversibility and blast radius. Documented in Phase 3 and the ADR.

**IaC (Infrastructure as Code)**
The practice of provisioning and managing infrastructure through machine-readable definition files rather than manual configuration.

**Idempotency**
The property of an operation that produces the same result when executed one time as when executed multiple times. A Task-Level Gate question for any implementation change.

**Living Document Protocol**
A defined set of event-based triggers, beyond calendar cadence, that require review and update of design artifacts. Events include: model version change, significant volume change, new class-adjacent use case discovered in production, team ownership change, Class Drift finding. Established in Phase 7.

**Minimum Class Coverage**
The minimum percentage of the problem class the system must handle to be viable. Established in Phase 2. Anything below this threshold means the system does not justify its cost.

**Minimum Viable Coverage**
The smallest version of the system that validates the core class assumption. Smaller than Minimum Class Coverage; sufficient to confirm that the class definition is correct before full implementation.

**Model Drift**
A form of Class Drift specific to Runtime AI systems. The underlying model's behavior has changed relative to the system's Prompt Contracts and Behavioral Eval criteria, even though no code has changed. Can occur when a model version is updated or when provider behavior changes for the same version identifier.

**Orchestrator**
The role responsible for defining the problem class, specifying contracts, setting verification criteria, and requiring operational standards. Does not require coding ability. Distinct from the builder role, which implements against the Orchestrator's specifications.

**Problem Class**
A bounded category of problems the system is designed to handle, with explicit inclusion and exclusion criteria. Defined in Phase 1. Every subsequent phase decision is evaluated against it.

**Prompt Contract**
The schema defining the structure of inputs to and expected outputs from a single LLM call. The Runtime AI equivalent of an API specification. A component of the Class Interface Contract. Includes input structure, output structure, contract violation handling, and data boundary compliance confirmation.

**Runtime AI**
An LLM that executes as part of the live system in production, processing inputs, generating outputs, or taking actions. Contrast with Build-Time AI. Runtime AI systems require additional gate criteria beyond those required for Build-Time AI.

**SDLC (Software Development Life Cycle)**
The process used to design, develop, test, deploy, and maintain software. This framework defines a seven-phase SDLC with gate reviews between phases.

**Significance Trigger**
A condition that activates the Task-Level Gate in Phase 4. Triggers include: changes to data schemas or Class Interface Contracts, changes to public interfaces or APIs, changes to authentication or authorization logic, introduction of new external dependencies, and any LLM call, agent action, or nondeterministic execution path.

**SLO (Service Level Objective)**
A target level for the performance of a service, expressed as a measurable condition. For example: 99% of requests resolved within 200ms. Used in Phase 7 to evaluate whether the Success Predicate is being met.

**SOP (Standard Operating Procedure)**
Step-by-step instructions for a routine operational task. Produced in Phase 6. Must be tested by someone other than the author before Gate 4 approval.

**Success Predicate**
A logical condition, which may be composite, that determines whether the system is correctly handling its problem class. Defined in Phase 1. If the predicate cannot be evaluated against observable system behavior, the class definition is incomplete. Validated in Phase 7.

**YAGNI (You Ain't Gonna Need It)**
A principle from software engineering: do not implement functionality until there is a validated need for it. Applied in this framework as a Task-Level Gate question: does this implementation exceed the Minimum Class Coverage defined in Phase 2?
