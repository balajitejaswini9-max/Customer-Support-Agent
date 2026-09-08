# Phase 2 — Customer Support Frontend

## 1. Objective

Build a minimal customer-facing frontend for the Customer Support Agent.

The frontend consumes the existing Phase 1 `/chat` API and presents:

* customer messages;
* agent responses;
* source citations;
* escalation state;
* loading state;
* API errors.

Phase 2 is a presentation-layer phase.

It must not introduce new agent capabilities or move business logic from the backend into the frontend.

---

## 2. Phase Boundary

### Phase 2 owns

* Customer chat interface
* Message rendering
* Source/citation rendering
* Escalation-state presentation
* Loading states
* Error states
* API integration with `POST /chat`
* Basic accessibility and responsive behaviour

### Phase 2 does not own

* Knowledge-base ingestion
* Retrieval
* Prompt engineering
* Grounding decisions
* Escalation decisions
* Order lookup
* Return eligibility
* Refund processing
* Human handoff
* Ticket creation
* Email notification
* Conversation persistence
* Observability API
* Backend agent logic

The frontend must treat the `/chat` API as the authoritative source of agent behaviour.

---

## 3. User Journey

```text
Customer
   |
   v
Open Support Chat
   |
   v
Enter Question
   |
   v
Frontend POST /chat
   |
   v
Backend Agent
   |
   +--------------------+
   |                    |
   v                    v
Grounded Answer      Escalation
   |                    |
   v                    v
Answer + Sources     Escalation Message
```

---

## 4. API Contract

The frontend consumes the Phase 1 chat API.

### Request

```json
{
  "message": "How long does standard delivery take?",
  "conversation_id": "optional-id"
}
```

### Response

```json
{
  "answer": "Standard delivery usually takes 3–5 business days.",
  "sources": [
    {
      "source": "shipping_info.txt",
      "section": "Shipping Information"
    }
  ],
  "escalated": false,
  "escalation_reason": null
}
```

The frontend must not infer additional business meaning that is not represented by the API response.

---

## 5. Functional Requirements

### 5.1 Chat Input

The customer can:

* enter a message;
* submit the message;
* submit using Enter where appropriate;
* see the submitted message in the conversation.

Empty messages must not be submitted.

---

### 5.2 Agent Response

The frontend displays:

* the agent answer;
* source citations when supplied;
* escalation state when `escalated=true`.

The frontend must not alter the meaning of the backend response.

---

### 5.3 Source Citations

When sources are returned, the UI must make them visibly distinguishable from the answer.

At minimum, display:

* source name;
* section when available.

When no sources are returned, no fabricated source may be displayed.

---

### 5.4 Escalation

When the API returns:

```json
"escalated": true
```

the UI must clearly communicate that the request requires human assistance.

The frontend must not state that:

* a human has already reviewed the case;
* a ticket has been created;
* an email has been sent;
* a refund has been processed;

unless the API explicitly provides evidence of that capability.

---

### 5.5 Loading State

While waiting for `/chat`:

* the submitted message remains visible;
* the user receives clear feedback that the agent is processing the request;
* duplicate submissions are prevented.

---

### 5.6 Error State

If the API request fails:

* the customer sees a clear error message;
* the application remains usable;
* the customer can retry;
* raw backend errors, stack traces, or secrets are not exposed.

---

### 5.7 Responsive Layout

The chat interface must remain usable on:

* desktop;
* tablet;
* mobile-sized screens.

---

### 5.8 Accessibility

The interface should provide:

* keyboard-accessible controls;
* appropriate labels for inputs;
* readable message structure;
* visible focus states;
* meaningful loading/error status information.

---

## 6. Frontend Architecture

The frontend should be separated into presentation and API integration.

```text
Frontend
│
├── Chat UI
│   ├── Message List
│   ├── Message Input
│   ├── Loading State
│   ├── Error State
│   └── Escalation State
│
└── Chat API Client
        |
        v
    POST /chat
        |
        v
    Phase 1 Backend
```

The frontend must not contain:

* RAG logic;
* retrieval thresholds;
* prompt construction;
* escalation rules;
* policy interpretation;
* order lookup logic.

---

## 7. State Model

The frontend should represent at least:

```text
idle
  |
  v
submitting
  |
  +-------> success
  |
  +-------> error
```

An API success response may additionally contain:

```text
success
   |
   +--> normal answer
   |
   +--> escalated answer
```

---

## 8. Feature Dependencies

Phase 2 depends on:

* Phase 0 repository and agent harness;
* Phase 1 `/chat` API;
* Phase 1 response contract;
* Phase 1 behavioural guarantees.

Phase 2 must not require Phase 3+ capabilities.

---

## 9. Out of Scope

The following must not be implemented during Phase 2:

* order lookup UI backed by a StoreClient;
* return eligibility UI;
* refund workflows;
* ticket creation;
* support-team email;
* persistent conversation history;
* authentication;
* customer accounts;
* real-time order tracking;
* agent streaming;
* analytics dashboard;
* observability dashboard.

These may be future capabilities but are outside the Phase 2 contract.

---

## 10. Definition of Done

Phase 2 is complete when:

1. The frontend can submit a customer question to `/chat`.
2. Customer messages are rendered.
3. Agent responses are rendered.
4. Sources are rendered when provided.
5. Escalated responses are clearly distinguished.
6. Loading state works.
7. API failure state works.
8. Empty submissions are prevented.
9. Duplicate submissions are prevented while a request is pending.
10. The UI works at mobile and desktop widths.
11. Basic accessibility requirements are satisfied.
12. Frontend behavioural evaluations pass.
13. Phase 1 backend behaviour remains unchanged.
14. No Phase 3+ capability has been implemented.
15. Phase 2 feature and evaluation ledgers are updated with evidence.

---

## 11. Implementation Rule

The coding agent must implement only features listed as active in:

```text
docs/phases/PHASE-02-FEATURES.json
```

The behavioural contract is defined by:

```text
docs/phases/PHASE-02-EVALS.json
```

The active phase is determined by:

```text
session-handoff.md
```

Do not create a project-level `feature_list.json`.
