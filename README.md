# Building an AI Agent by Decomposing the Problem

What happens when you give an AI coding agent a complex product requirement and simply ask it to **build the whole thing**?

It can produce a lot of code.

But how do you know it is solving the **right problem**, in the **right order**, with the **right boundaries**?

This project explores a different approach.

## The idea

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

The system is built incrementally from these smaller, verifiable problems.

## Why this matters

With AI coding agents, the limiting factor is increasingly not:

> **"Can the model write the code?"**

It is:

> **"Can we give the model the right environment in which to make good engineering decisions?"**

A large prompt leaves too much to the model:

* what to build first;
* what not to build;
* where the boundaries are;
* what "done" means;
* how to verify the result;
* what context should survive into the next session.

Instead, these decisions become part of the **repository itself**.

## The repository becomes the harness

The repository captures the context that the agent needs to work effectively:

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

The coding agent operates inside this environment.

It doesn't have to reconstruct the entire project from a conversation or decide the whole development strategy from scratch.

The repository tells it:

**What are we building?**

**What are we solving now?**

**What is explicitly out of scope?**

**How do we know it works?**

**Where do we continue from?**

## The important shift

The interesting change is from:

```text
"Build this application."
```

to:

```text
"Here is the problem.

Here is the part we are solving now.

Here are the boundaries.

Here is what success looks like.

Here is how you prove it."
```

That makes the coding agent part of an **engineering loop**, rather than simply a code generator.

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

## Why this is particularly important for AI systems

AI systems have another layer of complexity.

The application itself also needs boundaries.

For example, an agent should not simply answer every customer question because it can generate a plausible response.

It needs to know:

> **When should I answer, and when should I not answer?**

So the same principle is applied twice:

```text
                 Engineering Harness
                         │
                  controls what
                  the agent builds
                         │
                         ▼
                  AI Application
                         │
                  controls what
                  the agent can do
```

The coding agent has bounded responsibilities.

The AI application has bounded capabilities.

Both are governed by explicit contracts and verification.

## What this project is really exploring

The customer-support agent is the application.

The deeper experiment is:

> **Can we use harness engineering and problem decomposition to build increasingly complex AI systems in a way that remains understandable, verifiable and resumable across coding-agent sessions?**

Instead of expecting one model interaction to produce the final system, the system emerges through a sequence of **small, explicit, verified engineering decisions**.

The model provides the intelligence.

**The harness provides the structure.**
