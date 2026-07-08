---
name: unknowns
description: Lifecycle orchestrator for the unknowns plugin. Detects the current phase of work (pre-implementation, mid-implementation, pre-merge) and routes to the right technique skill. Use when the user says "/unknowns", "know my unknowns", or is unsure which unknowns skill applies.
version: 1.0.0
author: Hien Dinh
license: MIT
---

# Unknowns Orchestrator

Pure router. Detect the phase, invoke the right skill via the Skill tool.
If this agent has no skill-invocation tool, read that skill's SKILL.md and
follow it directly. No technique logic lives here.

## Phase detection

Check, in order:

1. **Pre-merge:** `git status` clean or nearly clean AND there are commits to
   review: on a feature branch, commits ahead of the default branch
   (`git log <default-branch>..HEAD --oneline` non-empty); when HEAD *is* the
   default branch, unpushed commits (`git log @{upstream}..HEAD --oneline`
   non-empty) → invoke `unknowns:merge-quiz`.
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
- Skill names here use the `unknowns:` namespace (Claude Code plugin install).
  If the skills were installed flat (Codex, OpenCode: `cp -r skills/*`), they go
  by their bare directory names — `blindspot`, `verify-ref`, `mock`,
  `log-deviation`, `merge-quiz`.
