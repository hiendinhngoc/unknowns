# Unknowns Plugin — Design

**Date:** 2026-07-05
**Source:** Thariq's "Know Your Unknowns" (https://thariqs.github.io/html-effectiveness/unknowns/)
**Status:** Approved

## Goal

A personal Claude Code plugin named `unknowns` that turns the novel techniques
from the article into daily-invocable skills. Ideas already covered by installed
skills (brainstorming, grill-me, writing-plans, design-iterator) are deliberately
excluded.

## Structure

One plugin, six thin skills. Each skill is independently invocable; the
orchestrator is a pure router with no logic of its own.

```
unknowns/
├── .claude-plugin/plugin.json
└── skills/
    ├── unknowns/SKILL.md       # orchestrator
    ├── blindspot/SKILL.md
    ├── verify-ref/SKILL.md
    ├── mock/SKILL.md
    ├── log-deviation/SKILL.md
    └── merge-quiz/SKILL.md
```

## Skills

### 1. /unknowns:blindspot — pre-implementation reconnaissance

- **Input:** a directory, system, or feature name; infers from conversation if omitted.
- **Behavior:** read-only exploration of the target. Produces a risk-ranked list
  of ~5–7 unknowns: hidden coupling, unowned edge cases, stale assumptions,
  missing tests around dangerous paths.
- **Output format:** each finding = one-line risk statement + why it matters +
  a ready-to-paste follow-up prompt to investigate or fix it.
- **Hard rule:** applies no fixes. Reconnaissance only.

### 2. /unknowns:verify-ref — comprehension gate before porting

- **Trigger:** "port/copy/adapt X" tasks.
- **Behavior:** before writing any code, Claude reads the reference
  implementation and produces a comprehension proof: data flow, edge cases
  handled, invariants, hidden dependencies. Then it self-challenges with
  "what would break if I got this wrong?" and asks the user to confirm.
- **Gate:** implementation may not start until the user confirms the proof.

### 3. /unknowns:mock — throwaway prototype before production code

- **Behavior:** builds a single self-contained HTML prototype in the session
  scratchpad and renders it via the Artifact tool to validate behavior/UX.
- **Hard rule:** forbidden from touching the real codebase.
- **Exit:** asks "does this match what you wanted?" and extracts the confirmed
  decisions into a short spec (in conversation) to feed implementation.

### 4. /unknowns:log-deviation — during-implementation deviation log

- **Behavior:** appends an entry to `docs/deviations/YYYY-MM-DD-<task>.md` in
  the current repo: what the plan said / what the code forced instead / why.
- **Invocation:** manual mid-task; the orchestrator also instructs Claude to
  log automatically whenever it deviates from an agreed plan.
- **Downstream:** the file feeds future planning sessions and the merge quiz.

### 5. /unknowns:merge-quiz — pre-merge comprehension gate (quizzes the USER)

- **Behavior:** reads the branch diff plus any deviation log, then quizzes the
  user via 3–5 AskUserQuestion rounds on the riskiest parts of the change
  ("what happens if X is null here?", "why did we bypass Y?").
- **Wrong/unsure answers:** explained immediately and flagged as
  review-carefully items.
- **Output:** a merge-readiness note suitable for pasting into the PR
  description.

### 6. /unknowns:unknowns — lifecycle orchestrator

- **Behavior:** inspects git state and conversation context to detect phase:
  - no code written yet → suggests blindspot / verify-ref / mock
  - mid-implementation → deviation logging
  - branch ready / diff exists → merge-quiz
- Pure router: names the right skill and invokes it. No technique logic inline.

## Non-goals

- No hooks/automation (approach C) — revisit after a few weeks of manual use.
- No duplication of existing installed skills (brainstorming, interview-style
  grilling, plan writing, design iteration).

## Error handling

- blindspot/verify-ref with no discernible target: ask for one, don't guess.
- log-deviation outside a git repo: write to the session scratchpad and tell
  the user where it went.
- merge-quiz with no diff against the default branch: say so and stop.

## Testing

Manual: invoke each skill once on a real repo after install. The skills are
prompt-markdown only — no executable code to unit-test.

## Installation

Local plugin: add the repo path via `claude plugin` local install
(`/plugin install` from a local marketplace entry or `--plugin-dir`), so skills
appear as `/unknowns:<name>` in every project.
