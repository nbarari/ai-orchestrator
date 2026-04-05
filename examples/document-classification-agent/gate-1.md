# Gate 1: Feasibility Analysis

**Project:** Document Classification Agent (Worked Example)
**Date:** 2026-04-05
**Author:** ai-orchestrator-framework contributors
**Status:** Accepted

**Gate 0 reference:** `examples/document-classification-agent/gate-0.md`

Reference: `manual.md` Phase 2.

---

## Environmental Mapping

### Upstream Dependencies

What systems or teams provide the inputs this system depends on? Are those agreements stable?

| Dependency | Owner | Agreement stability | Notes |
|---|---|---|---|
| Intake channels (email ingest, secure upload API, SFTP drop, ticketing attachments) | Operations / IT | Stable / At risk (varies by channel) | Delivers authoritative text or text extracted upstream; classifier assumes text-in, not raw binary layout. |
| OCR or document-extraction pipeline (when source is scanned PDF or image) | Platform or vendor | At risk | Quality affects input text; mixed-quality OCR remains in scope per Gate 0 but increases fallback and review load. |
| Versioned taxonomy definition (labels, descriptions, hierarchy) | Product / governance | Stable when change-controlled | Classifier consumes a pinned taxonomy artifact; evolving taxonomy is out of scope for the classifier’s problem class but changes require re-validation. |
| Identity and tenant context (which org, which workflow tenant) | Identity / platform | Stable | Needed for routing and audit; not for defining labels. |
| Secrets and LLM API access | Platform / security | Stable | Runtime AI dependency; credentials and network paths are integration work. |

---

### Downstream Impact

Who consumes this system's output? What is the Blast Radius if the system fails or handles a class-boundary case incorrectly?

| Consumer | Impact on failure | Blast Radius (Low / Medium / High) |
|---|---|---|
| Workflow orchestration / case management (per-label routes) | Wrong queue → wrong SLA path, delayed handling, possible compliance miss for time-bound workflows | High |
| Human review / exception queues | Surge of misfiled items or false confidence → reviewer load and slower clearance | Medium |
| Archival and retention systems | Wrong retention bucket or legal hold path | High (if regulated content) |
| Analytics and reporting (volume by label) | Distorted operational metrics; not usually safety-critical | Low |

**Runtime AI: LLM provider failure.**
What happens when the LLM provider is unavailable, rate-limited, or degraded? This must be defined as a design requirement in Phase 3, not left as a production discovery.

```
The system must not silently assign a high-confidence route when inference did not complete successfully.

Design requirements for Gate 2 (to be detailed in contracts):

1. **Unavailable or hard failure:** Do not emit a primary classification for production routing; enqueue the document for retry with backoff, or hand off to a documented default route (e.g., human triage queue) according to policy. User-visible and operator-visible signals distinguish “not classified” from “classified with label X.”

2. **Rate limiting:** Apply client-side throttling, queueing, and prioritization so the intake path remains stable; if backlog exceeds SLO, escalate per runbook (additional capacity, temporary degradation to human triage, or capped intake).

3. **Degraded latency:** Timeouts treat the attempt as failed for routing purposes (same as hard failure path for the safety predicate: no silent wrong route).

4. **Idempotency:** Retries must not double-post downstream effects; classification is invoked with a stable document idempotency key.

Exact thresholds (timeout seconds, queue depth, default route) are pinned in Gate 2 with the Class Interface Contract and operational runbooks.
```

---

### Class Volume Analysis

What is the expected cardinality and distribution of problems in this class?

- [ ] Low and steady
- [x] Bursty
- [x] Continuous and high-volume

**Expected volume at steady state:**

```
Illustrative for this worked example (not measured telemetry): on the order of hundreds to low thousands of documents per business day for a mid-sized intake operation; adjust proportionally for org size. Steady state excludes end-of-period spikes.
```

**Expected peak volume:**

```
Peaks at month-end, quarter-end, or campaign-driven intake can reach a multiple of steady state (e.g., 2–5×) for short windows. Tail latency and provider rate limits matter more during peaks than at steady state.
```

**Tail cases and outliers to account for:**

```
- Very large documents (token limits): truncation strategy or chunking with explicit “uncertain / human” path must be defined in Gate 2, not ad hoc in code.
- Empty or near-empty text after extraction: adjacent to class; explicit boundary behavior (reject, default route, or human queue).
- Sudden taxonomy or model updates: evaluation and rollback strategy; no silent drift of labels in production without versioning.
```

**Does the design assumption match the actual volume profile?**

```
For a real deployment, validate against intake logs or pilot metrics. This worksheet assumes continuous volume with identifiable bursts—the profile described in Gate 0 (operational mailrooms and intake queues). If actual volume is orders of magnitude lower, fixed operational cost (integration, monitoring, LLM minimums) may dominate per-document economics and should be revisited at Gate 2.
```

---

### The Landlord

Who owns and manages the infrastructure this system will run on?

```
The organization’s cloud or internal platform team (e.g., AWS/GCP/Azure account, Kubernetes or serverless runtime, secrets store, observability stack). The classification service is a tenant of that platform; LLM calls egress via approved network paths and monitored endpoints.
```

---

### Integration Assessment

What proportion of the implementation effort is core class logic versus integration work (authentication, logging, data translation, glue code)?

- Core class logic: approximately **25–35%**
- Integration and glue: approximately **65–75%**

**Primary integration concerns:**

```
- Authenticated intake and tenant isolation; no cross-tenant taxonomy or routing.
- Stable handoff to downstream workflow APIs (idempotent writes, dead-letter handling).
- Structured logging and tracing: document id, taxonomy version, model version, latency, outcome (success, fallback, error), without logging data outside the future Data Boundary Declaration (Gate 2).
- Prompt assembly and response validation against the Prompt Contract; retries and circuit breaking for the LLM client.
- Configuration for taxonomy version, model version, and thresholds—deployed as versioned artifacts, not only environment variables without audit trail.
```

---

## Feasibility and Skills

### Capability

Is this buildable with the available team? Are there knowledge silos or single points of failure?

```
Feasible for a typical product engineering team: backend engineers for APIs and integration, plus access to ML/LLM operations practices (prompt iteration, eval harnesses, monitoring). No exotic research requirement—the problem class is established LLM text classification with explicit contracts.

For this worked example, “team” is illustrative; a real project should name roles and backup coverage.
```

**Single points of failure:**

```
- One engineer owns all prompt + eval logic with no second reviewer (knowledge silo).
- Exclusive dependence on a single LLM vendor without a documented degradation path (operational SPOF).
- Taxonomy changes without a governance owner (process SPOF affecting correctness across the board).
```

---

### Justification

Is the required investment proportionate to the value of the Success Predicate?

```
Yes, when intake volume and mis-route cost exceed the combined cost of integration, ongoing inference, monitoring, and governance. Gate 0 already framed class impact (rework, SLA, FTE load). Gate 1 adds: inference is a recurring line item; if operational cost at expected volume exceeds manual triage cost without meeting the Success Predicate thresholds, the project should not proceed to Gate 2 until economics or scope change.

The worked example does not replace a business case with real numbers; a production Gate 1 should attach rough order-of-magnitude cost and benefit.
```

---

### Operational Cost Model (Runtime AI)

What is the estimated cost per problem-class instance?

Inference cost is a design constraint. A system that is architecturally sound but financially untenable at scale has failed feasibility. If this cannot be estimated, Phase 3 should not begin.

| Scenario | Estimated cost per instance | Volume | Total estimated cost |
|---|---|---|---|
| Steady state | Illustrative: low cents per document (depends on document length in tokens, model list price, caching absent). | e.g., 1,000 docs/day | Illustrative: daily inference spend scales linearly with tokens × price; dominated by long documents. |
| Peak | Same per-token price; higher concurrent requests may require provisioned throughput or queue depth (ops cost, not only tokens). | 2–5× steady | Peak token cost scales with volume; rate-limit handling may add marginal infrastructure. |
| Tail | Very long documents: cost per instance spikes with tokens; may hit context limits requiring chunking (multiple calls) or early escalation to human review—must be bounded in Gate 2. | Small fraction of volume | Disproportionate share of cost; worth explicit caps or “oversize → human” policy. |

**Volume threshold at which cost becomes unviable:**

```
Not numerically fixed in this example. Viability turns when (annual inference + platform + maintenance) ≥ avoided cost of manual triage and mis-routes at the Minimum Class Coverage you commit to, with margin for risk.

Rule of thumb for feasibility: if steady-state daily volume is in the tens of documents and taxonomy is stable, a smaller rules-first or human-first approach may beat LLM TCO until volume grows. Above sustained thousands per day with material mis-route cost, LLM routing with contracts and fallbacks is more likely to justify its operational cost.
```

---

## Class Coverage and Scope

### Minimum Class Coverage

What percentage of the problem class must be handled for the system to be viable?

```
For viability, the system should handle automated primary-label routing for the majority of in-scope documents, with explicit non-silent handling for the remainder. A typical planning range is **80–95%** of eligible documents receiving an automated primary label that meets the accuracy threshold on the evaluation set—exact percentage and eligibility rules (e.g., excluding blank inputs) are finalized in Gate 2 with thresholds.

Below that band, manual triage remains the dominant cost and the Success Predicate is hard to satisfy without redefining scope.
```

**What is intentionally left as manual or out of scope at this stage?**

```
- Taxonomy definition and change management (Gate 0 anti-scope).
- Extracting fields beyond routing needs (anti-scope).
- End-to-end execution of downstream workflows (consumers’ responsibility).
- Novel multimodal understanding without text (anti-scope).

Within scope but **manual path by design:** low-confidence predictions, invalid model output, provider failure, and documents flagged by policy (e.g., safety-critical categories always reviewed if required in Gate 2).
```

---

### Minimum Viable Coverage

What is the smallest version that validates the core class assumption?

```
A thin vertical slice: single intake source, pinned taxonomy subset (e.g., a handful of labels), one downstream route mapping, full path for one LLM call with logging, validation, and fallback to human queue. Demonstrates that text + taxonomy → label → route works end-to-end with observability and failure behavior before scaling label breadth or volume.
```

---

### Anti-Scope

What is explicitly excluded from this version, and why?

| Excluded item | Reason |
|---|---|
| Active learning or automatic taxonomy suggestions | Expands problem class into governance; out of Gate 0 class. |
| Multi-label optimization across many labels beyond routing need | Adds complexity; defer until single primary-label path is stable and measured. |
| Cross-language support without explicit Gate 2 contract and eval | Feasibility assumes language coverage is defined and tested; “all languages” is not assumed. |
| Replacing human oversight for regulated or irreversible workflows | Oversight model in Gate 2 may require supervised or advisory paths regardless of model confidence. |

---

## Gate Approval

- [x] All upstream dependencies identified with stability assessment
- [x] Blast Radius mapped for downstream consumers
- [x] LLM provider failure fallback defined (Runtime AI)
- [x] Class volume analysis is evidence-based, not assumed
- [x] Capability assessment identifies single points of failure
- [x] Operational cost model completed (Runtime AI)
- [x] Minimum Class Coverage and Anti-Scope are documented

**Approved by:** ai-orchestrator-framework contributors (worked example)
**Date:** 2026-04-05

**Notes:**

This worksheet is a **worked example**. Volume, cost figures, and dependency stability are **illustrative** unless replaced by project-specific measurements and agreements. For a live deployment:

- Replace volume and cost tables with data from intake metrics and provider pricing.
- Name infrastructure owners and upstream/downstream system owners.
- Treat the operational cost model as a gate: if estimates cannot be produced, defer Gate 2 until they can.

For **class volume**, the checklist item “evidence-based, not assumed” is checked here on the basis that the **profile** (continuous, bursty, tail behaviors) is grounded in Gate 0’s operational context and that a production worksheet must attach **measured** intake data—not on the basis of real telemetry in this repository artifact.

**Status:** Set to **Approved** for the worked-example narrative; a real project should use a **named individual** in Approved by (see `examples/notes.md`) and attach real figures where the checklist requires evidence.
