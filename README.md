# Building an AI Agent by Decomposing the Problem

What happens when you give an AI coding agent a complex product requirement and ask it to build the whole thing?

It can produce a lot of code.

But how do you know it is solving the right problem, in the right order, with the right boundaries?

This project explores a different approach.

## Start with the problem, not the code

Instead of turning the entire problem into one large prompt, I break it down into smaller engineering problems that can be implemented and verified independently.

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
             Define verification
                       │
                       ▼
               Give it to agent
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

The application is built incrementally, with each step providing a verified foundation for the next.

## The repository becomes the harness

With AI coding agents, the challenge is increasingly less about whether the model can write code.

The bigger challenge is giving it enough context and constraints to make good engineering decisions.

A large prompt leaves many decisions to the model:

* What should be built first?
* What is out of scope?
* Where are the boundaries?
* What does "done" mean?
* How should the result be verified?
* What context needs to carry into the next session?

Instead, these decisions become part of the repository.

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

The coding agent operates within this environment rather than reconstructing the entire project from a conversation every time.

The repository provides the context for:

**What are we building?**

**What are we solving now?**

**What is out of scope?**

**How do we know it works?**

**Where do we continue from?**

## From code generation to an engineering loop

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

The coding agent then becomes part of an engineering loop:

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

Each iteration produces not just code, but a verified piece of the system and the context needed for the next iteration.

## Applying the same principle to AI systems

There is another interesting layer when the application itself is an AI system.

The application also needs boundaries.

For example, a customer-support agent should not answer every question simply because it can generate a plausible response.

It needs to know when it has enough evidence to answer — and when it should stop and escalate.

So the principle is applied at two levels:

```text
                 Engineering Harness
                         │
                  controls what
                  the coding agent builds
                         │
                         ▼
                  AI Application
                         │
                  controls what
                  the AI agent can do
```

The coding agent has bounded responsibilities.

The AI application has bounded capabilities.

Both are governed by explicit contracts and verification.

## What this project is really exploring

The customer-support agent is the application.

The deeper experiment is whether we can use problem decomposition and harness engineering to build increasingly complex AI systems while keeping the development process understandable, verifiable, and resumable across coding-agent sessions.

Rather than expecting a single model interaction to produce the final system, the system emerges through a sequence of small, explicit, verified engineering decisions.

The model provides the intelligence.

The harness provides the structure.
