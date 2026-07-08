---
name: verify-ref
description: Comprehension gate before porting, copying, or adapting an existing implementation. Proves understanding of the reference code before any new code is written. Use when the task is "port X", "copy how Y does it", "adapt Z", or reimplementing existing behavior.
version: 1.0.0
author: Hien Dinh
license: MIT
---

# Reference Verification

Prove you understand the reference implementation BEFORE porting it.
Misunderstood references produce confidently wrong ports.

<HARD-GATE>Write no implementation code until the user confirms the
comprehension proof below.</HARD-GATE>

## Process

1. **Locate the reference.** Use the argument or conversation context. If
   ambiguous, ask which implementation is the reference — don't guess.
2. **Read it fully.** The whole unit plus everything it calls that affects
   behavior. Skimming is how hidden coupling gets missed.
3. **Produce the comprehension proof**, covering:
   - **Data flow:** inputs → transformations → outputs, in order
   - **Edge cases handled:** every guard, fallback, retry, and special case,
     and what each protects against
   - **Invariants:** what must remain true before/after (ordering, uniqueness,
     idempotency, transactional boundaries)
   - **Hidden dependencies:** globals, config, environment, call-order
     assumptions, side effects the signature doesn't show
4. **Self-challenge.** Add a section: "What would break if I got this wrong?" —
   name the 2-3 misreadings most likely to cause a subtly wrong port and say
   why your reading is correct (cite file:line evidence).
5. **Gate.** Ask the user to confirm the proof or correct it. Only after
   confirmation may implementation begin. If no interactive user is available,
   stop after the proof and do not implement.

## Output format

```
## Comprehension proof: <reference name> (<file:line range>)
### Data flow
### Edge cases handled
### Invariants
### Hidden dependencies
### What would break if I got this wrong?
```
