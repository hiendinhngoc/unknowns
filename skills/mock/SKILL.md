---
name: mock
description: Build a throwaway interactive prototype to validate behavior and UX before writing production code. Use when requirements are vague, the user says "mock it up first", "prototype this", or before wiring a feature whose look/behavior is undecided.
version: 1.0.0
author: Hien Dinh
license: MIT
---

# Mock Before Wiring

Validate the idea with a disposable prototype. Cheap to throw away, cheap to redo.

<HARD-RULE>Do not touch the real codebase. The prototype lives ONLY in the
session scratchpad directory. No production files created or modified.</HARD-RULE>

## Process

1. **Pin down what's being validated.** One sentence: "This mock answers: <question>"
   (e.g. "should filtering be inline or a sidebar?"). If you can't write that
   sentence, ask the user what's undecided.
2. **Build one self-contained HTML file** in the scratchpad directory:
   - Inline all CSS/JS — no external requests
   - Fake all data with hardcoded fixtures; fake all backend calls with
     setTimeout + canned responses
   - Make the undecided part interactive; keep everything else minimal
3. **Render it with the Artifact tool** so the user can click through it.
   If this agent has no Artifact tool, tell the user the file path to open in
   a browser instead.
4. **Iterate.** Apply requested changes to the same file and redeploy to the
   same artifact URL.
5. **Exit.** When the user is satisfied, ask: "Does this match what you wanted?"
   Then extract the confirmed decisions into a short spec in conversation:

```
## Decisions validated by mock
- <decision 1>
- <decision 2>
## Explicitly rejected
- <alternative that was tried and declined>
```

The spec — not the prototype code — is the input to real implementation.
Never copy prototype code into the codebase.
