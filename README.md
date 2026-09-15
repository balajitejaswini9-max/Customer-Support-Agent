# Building an AI Agent by Decomposing the Problem

What happens when you give an AI coding agent a complex product requirement and simply ask it to **build the whole thing**?

It can produce a lot of code.

But how do you know it is solving the **right problem**, in the **right order**, with the **right boundaries**?

This project explores a different approach.

## The application

The application is a general e-commerce customer-support agent.

It is designed to help customers with common support requests such as product questions, order information and returns.

The agent uses a knowledge base to ground its responses and is designed to recognise when it does not have enough information or confidence to answer.

Rather than asking the coding agent to build the entire application in one go, the problem is decomposed into smaller, focused phases.

## The approach

Start with the problem statement.

Don't immediately turn it into code.

First, **decompose the problem into smaller engineering problems**.

```text
                Problem Statement
                       │
                       ▼
             Understand the problem
                       │
                       ▼
             Decompose the problem
                       │
                       ▼
              Define boundaries
                       │
                       ▼
             Define how to verify it
                       │
                       ▼
               Give it to the agent
                       │
                       ▼
                  Implement
                       │
                       ▼
                   Verify
                       │
                       ▼
              Preserve the result
                       │
                       ▼
                Next problem
```

The application is built incrementally from these smaller, verifiable problems.

## Breaking the problem into phases

The application is divided into a sequence of focused phases:

```text
Phase 0  →  Development structure
Phase 1  →  Knowledge-based customer support
Phase 2  →  Customer-facing interface
Phase 3  →  Order lookup
Phase 4  →  Return eligibility reasoning
Phase 5  →  Escalation and human handoff
Phase 6  →  Conversation persistence
Phase 7  →  Observability and metrics
Phase 8  →  Benchmarking and repository health
```

Each phase has its own scope, boundaries, acceptance criteria and evaluations.

The coding agent works on one defined problem at a time rather than being asked to reason about the entire application simultaneously.

## Giving the coding agent context

A large prompt leaves many decisions to the model:

* what to build first;
* what not to build;
* where the boundaries are;
* what "done" means;
* how to verify the result;
* what context needs to carry into the next session.

For this project, that context is captured through structured, persistent instructions and project documentation.

```text
Product
   ↓
Architecture
   ↓
Reliability principles
   ↓
Current problem
   ↓
Scope & boundaries
   ↓
Acceptance criteria
   ↓
Evaluation
   ↓
Verified implementation
```

This gives the coding agent a defined context in which to work.

It doesn't have to reconstruct the entire project from a conversation or decide the whole development strategy from scratch.

The instructions make explicit:

**What are we building?**

**What are we solving now?**

**What is explicitly out of scope?**

**What does "done" look like?**

**How do we verify it?**

## From requirement to code

The important shift is from:

```text
"Build this application."
```

to:

```text
"Here is the problem.

Here is the part we are solving now.

Here are the boundaries.

Here is what success looks like.

Here is how we verify it."
```

This creates a clearer path from a product requirement to an implementation.

The coding agent becomes part of an iterative engineering process:

```text
Understand
    ↓
Implement
    ↓
Evaluate
    ↓
Learn
    ↓
Persist
    ↓
Continue
```

Each iteration produces a verified piece of the system and preserves the context needed for the next iteration.

## The key learning

My biggest learning from this project was that this approach gave me a practical way to go from a product requirement to working code.

Instead of taking a large requirement and asking the coding agent to build the whole application, I could progressively translate it into:

```text
Requirement
    ↓
Problem
    ↓
Phase
    ↓
Scope & boundaries
    ↓
Acceptance criteria
    ↓
Evaluation
    ↓
Code
    ↓
Verified outcome
```

The files in this project are one way of capturing that context and structure. They don't have to be files — the same approach could be implemented using tools such as Jira or other product and engineering workflows.

The important part is the structure: creating a clear path from **what needs to be built** to **what the coding agent needs to implement and how we verify it**.

That is what this project is exploring: **using problem decomposition, structured context and verification to create a repeatable path from requirements to code when working with AI coding agents.**

## Repository structure

The project keeps the product and engineering context separate from the implementation:

```text
.
├── AGENTS.md
├── CLAUDE.md
├── session-handoff.md
│
├── docs/
│   ├── PRODUCT.md
│   ├── ARCHITECTURE.md
│   ├── RELIABILITY.md
│   │
│   └── phases/
│       ├── PHASE-00.md
│       ├── PHASE-00-FEATURES.json
│       ├── PHASE-00-EVALS.json
│       ├── ...
│       ├── PHASE-08.md
│       ├── PHASE-08-FEATURES.json
│       └── PHASE-08-EVALS.json
```

The implementation is deliberately developed alongside this context rather than treating documentation as something added after the code is written.

## Final thought

The objective is to make the coding agent effective at solving complex problems by giving it the right level of context, structure and boundaries.

Instead of expecting one model interaction to produce the final system, the system emerges through a sequence of **small, explicit and verified engineering decisions**.

The model provides the intelligence.

**The structure provides the boundaries.**
