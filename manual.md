# 📖 The AI Orchestrator's Software Development Lifecycle Manual

## 🚀 How to Use This Manual
*   **New Projects:** Start at **Phase 1: Planning**. No implementation should begin until the **Problem Class Definition** and **Success Predicate** are documented and approved.
*   **Routine Tasks:** Use the **Task-Level Implementation Gate** at the start of any change that exceeds the defined **Significance Triggers** (See Phase 4).
*   **Scaling:** Adjust the depth of documentation and interrogation based on the **Rigor by Risk** table in the Appendix.

---

## 0. The Framework Philosophy

*   **Class Before Instance:** We do not build for a specific problem; we define the class of problems a system handles and build for that class. A system built for a class is maintainable, transferable, and honest about its limits. A system built for an instance becomes legacy the day requirements change.
*   **Cognitive Speed Bumps:** Each gate is designed to force a mindset shift — from "How do I implement this?" to "Should this exist, and does it belong to the class I defined?"
*   **The Dependency Rule:** You cannot proceed to a later phase until the thinking requirements of the prior phase are documented and approved.

---

## 1. The Process Logic (Mermaid Map)

```mermaid
graph TD
  %% Phase 1
  subgraph P1 [Phase 1: Planning]
    G0{Gate 0: Concept Validation}
  end

  %% Phase 2
  subgraph P2 [Phase 2: Feasibility]
    G1{Gate 1: Discovery & Context}
  end

  %% Phase 3
  subgraph P3 [Phase 3: Design]
    G2{Gate 2: Architecture & Design}
  end

  %% Phase 4
  subgraph P4 [Phase 4: Implementation]
    TaskGate[Task-Level Gate]
    Build[Iterative Build Cycles]
  end

  %% Phase 5
  subgraph P5 [Phase 5: Testing]
    G3{Gate 3: Technical Verification}
  end

  %% Phase 6
  subgraph P6 [Phase 6: Deployment]
    G4{Gate 4: Operational Readiness}
  end

  %% Phase 7
  subgraph P7 [Phase 7: Maintenance]
    G5{Gate 5: Post-Deploy Validation}
    Ops[Ongoing Operations]
  end

  %% Main Logic Flow
  G0 -->|Validated Problem Class| G1
  G1 -->|Technical Viability| G2
  G2 -->|Approved Blueprint| TaskGate
  TaskGate --> Build
  Build -->|Code Complete| G3
  G3 -->|Technically Verified| G4
  G4 -->|Operationally Ready| G5
  G5 -->|Success Predicate Baselined| Ops

  %% Cognitive Feedback Loops
  Build -.->|Discovery Conflicts Design| G2
  G5 -.->|Success Predicate Not Met| G0
  Ops -.->|Trigger Condition Met| Decom{{Decommission Gate}}
```

---

## Phase 1: Planning (Gate 0 — Concept Validation)

**Mindset Shift:** *Strategic Thinking — Does this problem class warrant a system?*

### Step 1: Problem Class Definition (The "What")

*   **The Problem Class:** What is the bounded category of problems this system is designed to handle? State this without referencing a solution. Be explicit about what is *outside* the class — a system that handles everything handles nothing well.
*   **The Success Predicate:** What is the logical condition — which may be composite — that determines whether the system is handling its problem class correctly? If this predicate cannot be evaluated, the class is not yet well-defined.
*   **Evidence:** How do you know this problem class is real and not perceived? What observable signals validate its existence?
*   **Class Impact:** What does an unaddressed instance of this problem class cost (time, capital, errors, risk) at the expected frequency of occurrence?
*   **The Inertia Test:** What does the problem class cost if left unaddressed at scale over the mid-to-long term?

### Step 2: Timing, Origin & Solution Space

*   **Root Cause:** Why does this problem class exist — is it a process, technology, knowledge, or organizational gap?
*   **The Catalyst:** What changed recently (technically or organizationally) that makes this class addressable **now**?
*   **Solution Space:** What tools or systems already handle adjacent classes? Why are they insufficient for this class?

---

## Phase 2: Feasibility Analysis (Gate 1 — Discovery & Context)

**Mindset Shift:** *Situational Awareness — Map the landmines before you walk.*

### Step 1: Environmental Mapping (The Ecosystem Check)

*   **Upstream Dependencies:** What systems or teams provide the inputs? Are those agreements stable?
*   **Downstream Impact:** Who relies on our output? What is the potential **Blast Radius** for them if the system fails or handles a class-boundary case incorrectly?
*   **Class Volume Analysis:** What is the expected cardinality and distribution of problems in this class — low/bursty/continuous? Does the design assumption match the actual volume profile, including tail cases?
*   **The Landlord:** Who owns and manages the infrastructure this system is built on?
*   **Integration Assessment:** How much of the effort is core class logic vs. "Glue Code" (integration, auth, logging)?

### Step 2: Feasibility & Skills Gap

*   **Capability:** Is this buildable with available skills? Are there knowledge-silo or single-point-of-failure risks?
*   **Justification:** Is the required investment justified by the value of the Success Predicate?

### Step 3: Class Coverage & Scope

*   **Minimum Class Coverage:** What percentage of the problem class must be handled for the system to be viable? What is intentionally left as manual or out of scope?
*   **The MVP (Minimum Viable Coverage):** What is the minimum version required to validate that the core class assumption holds?
*   **The Anti-Scope:** What is explicitly excluded — and why? Document class boundaries as clearly as class inclusions.

---

## Phase 3: System Design (Gate 2 — Architecture & Liability)

**Mindset Shift:** *Liability Thinking — Minimize the cost of owning the solution.*

### Step 1: Components & Inventory

*   **Logical Boundaries:** What are the components and their boundaries? (Use contextual mapping models like **C4**.)
*   **BOM (Bill of Materials):** List every required infrastructure resource and implementation artifact.
*   **Class Interface Contract:** Define the schema that determines what a valid problem *in this class* looks like as a system input, and what a valid resolution looks like as an output. This is the primary source of truth — no implementation begins until this contract exists.
    *   *For AI systems:* The Class Interface Contract must include **Prompt Contracts** — the defined structure of inputs to and expected outputs from any LLM call. Prompts are interfaces; treat them with the same version control and contract discipline as APIs.

### Step 2: Architecture & Unhappy Paths

*   **Class Boundary Behavior:** What happens when the system receives an input that is *adjacent* to the defined class but not within it? This is distinct from an error condition — it is a design decision that must be explicit.
*   **Failure Mode Discovery:** What is the user experience when a dependency fails?
*   **The Breaking Point:** At what load does this design fundamentally break?
*   **ADR (Architecture Decision Record):** Document major decisions and the "why" behind them in a persistent record. This is the long-term memory that neither LLMs nor rotating teams retain naturally.
    *   *For AI systems:* Record model version pins, rationale for LLM use vs. deterministic logic, and privilege scope granted to any agentic components.

### Step 3: Environment & Test Strategy

*   **IaC (Infrastructure as Code):** How is infrastructure provisioned and managed?
*   **Irreversibility Analysis:** Which commitments are high-impact? Tie these to **Gate 4 (Operational Readiness)** criteria.
*   **Verification Strategy:** Define the **Automated Verification Suite** expectations.
    *   *For AI systems:* Production behavior must not rely on nondeterministic AI outputs for control flow or safety-critical decisions. Define golden output sets or behavioral contract tests. Specify model version pinning strategy.

---

## Phase 4: Implementation (The Build Cycles)

**Mindset Shift:** *Integrity — Is this solving the problem class or just adding complexity?*

### The Task-Level Gate (Start of Task)

*A "Significant Change" that triggers this gate includes any modification to: (1) Data Schemas or Class Interface Contracts, (2) Public Interfaces/APIs, (3) Authentication/Authorization, (4) Introduction of new external dependencies, or (5) Any LLM call, agent action, or nondeterministic execution path.*

1.  **Class Alignment:** Does this change serve the Success Predicate, or does it expand the problem class without Gate 0 approval?
2.  **Compatibility:** Is this change backward compatible with existing state?
3.  **Idempotency:** What happens if this logic executes multiple times?
4.  **Error Path:** If this fails mid-execution, what is the recovery path?
5.  **YAGNI (You Ain't Gonna Need It):** Am I implementing beyond the Minimum Class Coverage defined in Phase 2?

### Build Reconciliation (End of Task)

*   **Variance:** What drift occurred from the original design, and is it documented?
*   **Reality Check:** If the build reveals a mismatch between "Design Ceiling" and "Actual Floor," stop and return to Phase 2.
*   **Escalation:** Does the implementation contradict the approved architecture or expand the class definition? **(If yes, escalate back to Design.)**

---

## Phase 5: Testing (Gate 3 — Technical Verification)

**Mindset Shift:** *Adversarial Thinking — How do I break the assumptions of Phase 2?*

**Stop Criteria:** If core functional requirements fail, or if the system cannot reach the required Breaking Point, or if class boundary behavior is undefined.

### Step 1: Verification

*   **Class Coverage Verification:** Does the test suite cover the full breadth of the defined problem class, including boundary cases and class-adjacent inputs the system should reject or handle gracefully?
*   **Contract Verification:** Does the system adhere to the **Class Interface Contracts** and **Strict Data Contracts** defined in Phase 3?
*   **Signal Verification:** Do health signals and alerts fire correctly under failure conditions?
*   **Stress Test:** Has the system been pushed to the **Breaking Point** identified in Phase 3?
*   *For AI systems:* Does the verification suite include **behavioral evals** that test class-level correctness, not just deterministic assertions? Behavioral evals must cover the nondeterministic surface area — the same input producing different outputs is a design reality, not a test failure, unless it violates the class contract.

### Step 2: Diagnostic Audit

*   **Self-Service Diagnosis:** Can a qualified person diagnose a problem without the original builder?
*   **Traceability:** Are logs, traces, and metrics sufficient to reconstruct a failure?
    *   *For AI systems:* Are AI prompts, responses, and decisions logged in a privacy-safe and auditable way? Is the behavior of agentic components traceable to specific inputs?

---

## Phase 6: Deployment (Gate 4 — Operational Readiness)

**Mindset Shift:** *Surgical Precision — Minimize the blast radius of activation.*

**Stop Criteria:** If runbooks are untested or if the recovery/rollback procedure fails rehearsal.

### Step 1: Sustainability & Controls

*   **SOP (Standard Operating Procedure):** Are runbooks written and **tested by someone other than the author**?
*   **Operational Controls:** Are automated limits or **Kill Switches** active for variable operational spend?
    *   *For AI systems:* Are privilege scopes of agentic components enforced at the infrastructure level, not just at the prompt level? Can AI-triggered state changes (data mutations, access grants, deployments) be halted independently?

### Step 2: Handoff & Rollback

*   **Rehearsal:** Has the recovery/rollback procedure been rehearsed in a non-production environment?
*   **Independence:** Does the named owner from Phase 1 have sufficient context to operate this independently?
*   **Irreversibility Trigger:** Execute high-impact downstream changes only after all Phase 5 signals are Green.

---

## Phase 7: Maintenance (Gate 5 — Post-Deploy Validation)

**Mindset Shift:** *Responsibility — Every solution is a potential liability.*

### Step 1: Validation Loop

*   **The Audit:** Did the **Success Predicate** actually evaluate to true under real operating conditions?
*   **Adoption:** After sufficient usage, do operators and consumers trust the system enough to rely on it?

### Step 2: Routine Health & Review

*   **Class Drift Audit:** Is the system still handling the problem class it was designed for, or has operational reality shifted the class definition without a corresponding design revision? A class that drifts without documentation becomes an undocumented system.
    *   *For AI systems:* Has the underlying model version changed? If so, re-validate behavioral evals against the Class Interface Contract. Model drift is a form of class drift — the system's behavior relative to its class contract may have changed even if no code changed.
*   **Knowledge Persistence:** Has the operational context — including ADRs, Design Maps, and Class Interface Contracts — been preserved and remains current?

### Step 3: The Decommission Gate

*   **The Trigger:** Does maintenance cost exceed value? Has the problem class been dissolved, subsumed, or solved at a higher level?
*   **Execution:** Revoke access, archive records, and purge data according to policy.

---

## Appendix A: Glossary of Terms

| Term | Definition |
| :--- | :--- |
| **ADR** | **Architecture Decision Record**: A text file capturing a design decision, its context, and the reasoning behind it. The long-term memory of the system. |
| **Behavioral Eval** | A test that verifies class-level correctness of nondeterministic outputs against a defined contract, rather than asserting exact output equality. |
| **Blast Radius** | The maximum potential impact of a single component failure or change. |
| **BOM** | **Bill of Materials**: A list of all infrastructure, libraries, and resources required. |
| **C4** | **Context, Container, Component, Code**: A mapping model for software architecture. |
| **Class Boundary** | The explicit definition of what inputs are within the problem class vs. adjacent to it. |
| **Class Drift** | The condition where the system's operational problem class has diverged from its designed problem class without a corresponding design revision. |
| **Class Interface Contract** | The schema defining what a valid problem in the class looks like as an input, and what a valid resolution looks like as an output. Includes prompt contracts for AI systems. |
| **IaC** | **Infrastructure as Code**: Provisioning infrastructure through machine-readable definition files. |
| **Minimum Class Coverage** | The minimum percentage of the problem class the system must handle to be viable. |
| **MVP** | **Minimum Viable Coverage**: The smallest version that validates the core class assumption. |
| **Problem Class** | A bounded category of problems the system is designed to handle, with explicit inclusion and exclusion criteria. |
| **Prompt Contract** | The schema defining the structure of inputs to and expected outputs from an LLM call. The AI equivalent of an API spec. |
| **SDLC** | **Software Development Life Cycle**: The process used to design, develop, and test software. |
| **SLO** | **Service Level Objective**: A target level for the performance of a service. |
| **SOP** | **Standard Operating Procedure**: Step-by-step instructions for routine operations. |
| **Success Predicate** | A logical condition — which may be composite — that determines whether the system is correctly handling its problem class. |
| **YAGNI** | **You Ain't Gonna Need It**: Do not implement beyond Minimum Class Coverage until validated demand exists. |

---

## Appendix B: Scaling Rigor by Risk

| Risk Level | Rigor |
| :--- | :--- |
| **Low** | Verbal verification of Gate questions. Problem Class and Success Predicate stated informally. |
| **Medium** | Lightweight documentation of Class Definition, Success Predicate, Class Interface Contract, and ADRs. |
| **High** | Formal artifacts (C4, BOM, Prompt Contracts), peer reviews, behavioral evals, and documented Stop Criteria audits. |
