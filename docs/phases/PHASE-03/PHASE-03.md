# Phase 3 — Order Lookup

## Purpose
Introduce order awareness through a `StoreClient` abstraction and a deterministic `MockStoreClient`.

The agent can answer order-specific questions when authoritative mock-store data exists, while preserving the core rule: **never invent customer-specific state**.

## Goal
Support questions such as:
- "Where is order ORD-1001?"
- "What's the status of my order?"
- "Has my order shipped?"
- "What items are in my order?"

## In scope
- `StoreClient` interface
- `MockStoreClient`
- deterministic mock order dataset
- order-ID extraction
- `lookup_order` agent capability
- order-grounded responses
- unknown-order handling
- Phase 3 tests and behavioural evaluations
- regression coverage for Phase 1 behaviour

## Out of scope
- return-eligibility reasoning
- refunds or cancellations
- real store/e-commerce integration
- human handoff workflow
- email/ticket creation
- conversation history
- new frontend functionality
- observability API
- broad autonomous tool discovery

## Architecture

```text
Customer
   │
   ▼
FastAPI /chat
   │
   ▼
Customer Support Agent
   ├── Knowledge Retrieval
   ├── lookup_order
   │       │
   │       ▼
   │   StoreClient
   │       │
   │       ▼
   │   MockStoreClient
   │       │
   │       ▼
   │   Mock Order Data
   └── Escalation
```

The dependency direction must remain:

```text
Agent → StoreClient interface → MockStoreClient
```

The agent must never depend directly on the mock data structure.

## StoreClient contract

Conceptually:

```python
class StoreClient(Protocol):
    def get_order(self, order_id: str) -> Order | None:
        ...
```

The exact implementation may vary, but the abstraction must remain replaceable by a future real-store implementation.

## Order data
The mock model should contain, at minimum:
- order ID
- customer identifier
- order status
- items
- order date
- shipment/tracking information where available
- estimated delivery information where explicitly available

The dataset must contain multiple distinct orders so cross-order leakage can be detected.

## Grounding rules

**General policy facts → Knowledge Base**

**Customer/order-specific facts → StoreClient**

The agent must:
- treat returned store data as authoritative for order-specific facts;
- never invent status, tracking, shipment or delivery facts;
- never expose another order's data;
- never fabricate an order;
- never treat a customer's assertion as verified store state.

Order data is not a KB citation. Responses should make clear that order-specific information came from the order lookup capability.

## Unknown orders

```text
Customer request
      ↓
Extract order ID
      ↓
lookup_order
      ↓
Not found
      ↓
Do not fabricate
      ↓
Safe response / escalation
```

If an order-specific request lacks an identifier, the agent must not guess.

## Capability boundary
Phase 3 must not implement return eligibility or write actions.

For example:

```text
"Where is ORD-1001?"
        → StoreClient

"Is ORD-1001 eligible for a return?"
        → Phase 4 capability

"Cancel ORD-1001."
        → Phase 3 cannot perform this action
```

## API
The existing `/chat` contract remains unchanged:

```json
{
  "message": "Where is order ORD-1001?",
  "conversation_id": "optional-id"
}
```

Example:

```json
{
  "answer": "Order ORD-1001 is currently shipped.",
  "sources": [],
  "escalated": false,
  "escalation_reason": null
}
```

## Dependencies

```text
Phase 1
  │
  ├── RAG
  ├── grounded generation
  ├── escalation
  └── /chat
       │
       ▼
Phase 3
  ├── StoreClient
  ├── MockStoreClient
  ├── order lookup
  └── order-grounded responses
       │
       ▼
Future return-eligibility reasoning
```

## Definition of Done
- [ ] StoreClient abstraction exists.
- [ ] MockStoreClient implements it.
- [ ] Mock order data is deterministic.
- [ ] Known orders can be retrieved.
- [ ] Unknown orders are handled safely.
- [ ] Agent can answer supported order-specific questions.
- [ ] No order state is fabricated.
- [ ] No cross-order data leakage occurs.
- [ ] Phase 1 behaviour remains intact.
- [ ] Phase 3 feature ledger is complete.
- [ ] Phase 3 evaluations pass.
- [ ] Tests pass.
- [ ] `init.sh` initializes/verifies the environment.
- [ ] No Phase 4+ functionality is implemented.

## Engineering principle

> **General knowledge comes from the knowledge base; customer-specific state comes from an authoritative integration.**

This boundary prevents the language model from becoming the source of truth for information it cannot actually know.
