# Product

## Product Vision
Build a customer support agent that answers customer questions accurately when it has sufficient evidence and knows when it should not answer.

> A trustworthy support agent is not the agent that answers the most questions. It is the agent that gives reliable answers and correctly hands off questions it cannot safely resolve.

## Target Experience
A customer sends a support question through a conversational interface. The system should understand the request, use authorised information sources, answer when evidence exists, cite information where appropriate, avoid inventing facts, escalate when a human is required or evidence is insufficient, and preserve enough context for downstream support workflows.

## Product Principles
### Grounded by Evidence
Answers should be supported by authoritative business information.

### Honest Uncertainty
The system must not manufacture an answer simply because the customer expects one.

### Human in the Loop
Questions requiring human authority, judgement, investigation, or intervention should be escalated.

### Progressive Capability
Capabilities are introduced incrementally rather than building the entire system at once.

### Replaceable Integrations
External systems should be accessed through clear interfaces so they can be replaced or mocked.

### Observable Behaviour
Correctness must be measurable through automated tests and behavioural evaluations.

## Eventual Product Capabilities
- knowledge-grounded support
- order lookup
- return-eligibility reasoning
- human escalation and handoff
- conversation history
- operational observability
- benchmarking and reliability tooling

## Product Evolution
- Phase 0: engineering harness and repository foundation
- Phase 1: knowledge-grounded support with safe escalation
- Phase 2: customer-facing frontend
- Phase 3: order lookup through a store integration
- Phase 4: return-eligibility reasoning
- Phase 5: full human escalation and handoff
- Phase 6: conversation persistence and history
- Phase 7: operational observability
- Phase 8: benchmarking and clean-state tooling

## What Good Means
The product is successful when supported questions receive useful, grounded answers; unsupported questions do not produce fabricated answers; human-required cases are escalated; evidence is exposed where required; behaviour is reproducible and testable; and new capabilities can be added without destabilising existing ones.
