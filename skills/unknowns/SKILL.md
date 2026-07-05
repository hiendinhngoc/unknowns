---
name: unknowns
description: Lifecycle orchestrator for the unknowns plugin. Detects the current phase of work (pre-implementation, mid-implementation, pre-merge) and routes to the right technique skill. Use when the user says "/unknowns", "know my unknowns", or is unsure which unknowns skill applies.
---

# Unknowns Orchestrator

Pure router. Detect the phase, invoke the right skill via the Skill tool.
No technique logic lives here.

## Phase detection

Check, in order:

1. **Pre-merge:** `git status` clean or nearly clean AND the current branch has
   commits ahead of the default branch (`git log <default-branch>..HEAD --oneline`
   is non-empty) → invoke `unknowns:merge-quiz`.
2. **Mid-implementation:** uncommitted changes exist, or the conversation shows
   an agreed plan being executed → if a deviation was just discussed, invoke
   `unknowns:log-deviation`; otherwise remind the user the deviation log exists
   and ask what they need.
3. **Pre-implementation:** no changes yet for the task at hand → ask ONE
   question: what kind of unknown are they facing?
   - Unfamiliar system / risky area → invoke `unknowns:blindspot`
   - Porting or adapting existing code → invoke `unknowns:verify-ref`
   - Undecided UX or behavior → invoke `unknowns:mock`

## Rules

- Route and invoke — never inline a technique's logic here.
- If git state and conversation disagree, trust the conversation and confirm
  with the user.
- Outside a git repo, skip detection and just ask which phase they're in.
