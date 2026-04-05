# Rigor by Risk

The framework scales to the risk level of the work. Not every change requires formal artifacts and peer review. Use this table to determine the appropriate level of documentation and gate enforcement.

---

## Risk Classification

### Low Risk

**Characteristics:**
- Change is isolated to a single component with no downstream consumers
- No changes to public interfaces, schemas, or authentication
- Reversible within one deployment cycle
- Blast Radius is contained to a single team or system
- No LLM calls introduced or modified (Build-Time AI projects only)

**Gate requirements:**
- Gate questions answered verbally or in a brief comment
- Problem Class, Success Predicate, and AI Deployment Mode stated informally if not already documented
- No formal artifact required for the Task-Level Gate
- ADR optional; use judgment based on whether future readers would benefit from the reasoning

**Examples:**
- Bug fix in an internal utility with no external interface
- Documentation update
- Dependency version bump with no API changes
- Configuration change with a tested rollback path

---

### Medium Risk

**Characteristics:**
- Change affects a public interface or shared schema
- Downstream consumers exist but impact is bounded and recoverable
- Reversible within one sprint
- Blast Radius is cross-team but not cross-system
- Runtime AI: LLM call exists but is not on a critical path

**Gate requirements:**
- Gate 0: Completed worksheet in `docs/gate-0.md`
- Gate 1: Lightweight documentation of class volume, dependencies, and cost model
- Gate 2: Class Interface Contract required; Prompt Contract required for any LLM call; Data Boundary Declaration required for Runtime AI
- ADR required for any decision that a future engineer would need to understand without context
- Task-Level Gate: written answers, attached to the PR or ticket
- Build Reconciliation: documented in PR description

**Examples:**
- New API endpoint added to an existing service
- Schema change with a migration path
- New LLM call added to an existing pipeline
- New external dependency introduced

---

### High Risk

**Characteristics:**
- Change affects multiple systems or teams
- Downstream impact is difficult to fully enumerate
- Partial reversibility; some commitments are irreversible
- Blast Radius is organization-wide or customer-facing
- Runtime AI: LLM call is on a critical path, handles sensitive data, or takes autonomous actions

**Gate requirements:**
- All gate worksheets completed in full and linked
- C4 Context and Container diagrams required
- Full BOM required
- Class Interface Contract and all Prompt Contracts required before implementation begins
- Data Boundary Declaration reviewed by data governance or legal (Runtime AI)
- Human Oversight Model complete with documented rationale for each autonomous classification (Runtime AI)
- Behavioral eval criteria defined before implementation
- All ADRs peer-reviewed
- Stop Criteria documented and agreed upon before Gate 3
- Runbooks tested by someone other than the author before Gate 4
- Cost circuit-breaker active before Gate 4 (Runtime AI)
- Irreversible commitments explicitly tied to Gate 4 and not executed before Phase 5 verification is complete

**Examples:**
- New system that crosses organizational boundaries
- Data migration affecting production records
- LLM agent with autonomous actions on customer data
- Change to authentication or authorization architecture
- Infrastructure change affecting multiple services

---

## Escalation

When in doubt about risk classification, treat the change as one level higher than your initial assessment. The cost of over-engineering a gate review is a few hours. The cost of under-engineering one is a production incident.

If a Medium Risk change reveals dependencies or blast radius that were not anticipated at the start, stop and re-classify before continuing.
