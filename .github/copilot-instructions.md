# Copilot Instructions

This project uses the AI Orchestrator framework. Apply the following requirements to all code generation and review in this workspace.

## Before generating any implementation

Check whether the following exist for this project. If they do not, surface the gap before writing code.

- Problem Class Definition (what the system handles and what it does not)
- Success Predicate (the condition that determines whether the system is handling its class correctly)
- AI Deployment Mode (Build-Time, Runtime, or Both)

If none of these are defined, the project has not passed Gate 0 and implementation should not begin.

## Task-Level Gate

Apply before any change that touches data schemas, public interfaces, authentication or authorization logic, new external dependencies, or LLM calls.

1. Does this change serve the Success Predicate, or does it expand the problem class?
2. Is it backward compatible with existing state?
3. What happens if this logic runs more than once?
4. What is the recovery path if it fails mid-execution?
5. Does this exceed the Minimum Class Coverage defined for this project?
6. (Runtime AI) Does this introduce data into an LLM call not covered by the Data Boundary Declaration?

## Contracts before implementation

Do not generate code that crosses a system boundary until a Class Interface Contract exists for that boundary. For Runtime AI systems, this includes a Prompt Contract for every LLM call.

## Runtime AI requirements

For any LLM call or agent action:

- Require a Prompt Contract before generating the call
- Require a defined fallback for provider unavailability and invalid output
- Reference a specific model version, not a floating alias
- Include structured logging of inputs and outputs by default
- Confirm data crossing into the LLM call is covered by the Data Boundary Declaration
- Define the human oversight level for each action the component can take

## ADRs

When a significant design decision is made, prompt the user to create an ADR. Significant decisions include: choice of model or provider, data boundary decisions, human oversight levels, schema design, and external dependency selection.
