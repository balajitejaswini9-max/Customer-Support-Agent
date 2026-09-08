# Architecture

## 1. Purpose

This document is the architectural source of truth for the complete Customer Support Agent.

It defines:

- the target system architecture;
- component responsibilities;
- architectural boundaries;
- interfaces;
- data flow;
- reliability boundaries;
- phase evolution;
- architectural invariants.

It does NOT define the detailed implementation work for an individual phase.

Phase-specific implementation contracts live under:

    docs/phases/phase-xx/

Each phase owns its own:

- `PHASE-XX.md`
- `PHASE-XX-FEATURES.json`
- `PHASE-XX-EVALS.json`

---

# 2. Architectural Principles

The system is designed around six principles.

### 2.1 Grounding over completion

The agent must prefer escalation over an unsupported answer.

### 2.2 Progressive capability

Capabilities are introduced one phase at a time.

A future capability may exist in this architecture as a design target, but must not be implemented before its phase.

### 2.3 Separation of reasoning and side effects

The agent decides what should happen.

Adapters perform external actions.

For example:

    Agent
      |
      v
    Escalation Decision
      |
      v
    Escalation Service
      |
      +--> Ticket Adapter
      +--> Email Adapter

The agent should not directly contain email, database, or HTTP implementation details.

### 2.4 Replaceable integrations

External systems are accessed through interfaces.

Examples:

- `StoreClient`
- `ConversationRepository`
- `EscalationRepository`
- `EmailClient`

Concrete implementations can therefore be replaced without changing agent reasoning.

### 2.5 Observable behaviour

Important agent behaviour must be independently testable.

The system must be able to demonstrate:

- why an answer was produced;
- what evidence was retrieved;
- why escalation occurred;
- which capability was used;
- whether the response remained grounded.

### 2.6 Explicit phase boundaries

Each phase has a defined contract.

The active phase is determined by `session-handoff.md`.

The corresponding phase documentation is the implementation authority for that phase.

---

# 3. Target System

```text
                         +----------------+
                         |    Customer    |
                         +-------+--------+
                                 |
                                 v
                       +-------------------+
                       | Frontend / Client |
                       +---------+---------+
                                 |
                                 v
                       +-------------------+
                       |    FastAPI API    |
                       |      /chat        |
                       +---------+---------+
                                 |
                                 v
                 +-----------------------------+
                 |       Customer Support       |
                 |            Agent            |
                 |                             |
                 |  Intent Detection            |
                 |  Planning / Reasoning        |
                 |  Tool Selection              |
                 |  Grounding                    |
                 |  Escalation Assessment       |
                 +-------------+---------------+
                               |
             +-----------------+------------------+
             |                 |                  |
             v                 v                  v
      +-------------+   +-------------+   +-------------+
      | Knowledge   |   | Store       |   | Escalation |
      | Retrieval   |   | Client      |   | Service    |
      +------+------+   +------+------+   +------+------+
             |                 |                  |
             v                 v                  +------+
      +-------------+   +-------------+                  |
      | ChromaDB    |   | Mock Store  |                  v
      | / Vector DB |   | / Real      |          +---------------+
      +-------------+   | Store       |          | Ticket / Email|
                        +-------------+          | / Human Queue |
                                                 +---------------+

                 +-----------------------------+
                 |      Grounded Generation    |
                 |          Claude             |
                 +-----------------------------+

                 +-----------------------------+
                 | Persistence / Observability |
                 +-----------------------------+