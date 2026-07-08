---
name: merge-quiz
description: Pre-merge comprehension gate that quizzes the USER on the riskiest parts of the branch diff. Use before merging or opening a PR, or when the user says "merge quiz", "am I ready to merge", or "quiz me on this diff".
version: 1.0.0
author: Hien Dinh
license: MIT
---

# Merge Readiness Quiz

Before shipping, verify the HUMAN understands what's being merged. The quiz
tests the user, not Claude.

## Process

1. **Gather the material.**
   - Diff, first base that yields one:
     1. On a feature branch: `git diff <default-branch>...HEAD`
     2. HEAD is the default branch: `git diff @{upstream}..HEAD` (unpushed commits)
     3. Neither yields a diff: ask the user for a base ref; if they have none, stop.
   - Deviation log: read every `docs/deviations/*.md` file whose date (from the
     filename) is on or after the merge-base commit's date
     (`git log -1 --format=%cs $(git merge-base <base> HEAD)`), if any exist.
2. **Pick the 3–5 riskiest spots.** If the diff is too small for 3 real
   questions, ask fewer and say why. Prioritize: behavior changes on dangerous
   paths (auth, money, deletion, migrations), deviations from the plan, error
   handling changes, anything irreversible.
3. **Quiz one question at a time** using AskUserQuestion (or plain-text
   multiple choice if this agent has no such tool). If no interactive user is
   available, output the quiz and stop without answering for them. Each question:
   - Cites the exact file:line it's about
   - Asks about consequences, not trivia: "what happens if X is null here?",
     "why did we bypass Y?", "what breaks if this runs twice?"
   - Offers 3-4 plausible answers (one correct, distractors that reflect real
     misunderstandings)
   - Has one correct answer backed by the exact diff hunk or file:line; if no
     evidence exists in the diff, do not ask that question
4. **On a wrong or unsure answer:** explain the correct answer immediately with
   evidence from the diff, and flag that spot as review-carefully.
5. **Produce the merge-readiness note** (paste-ready for the PR description):

```markdown
## Merge readiness
- Quiz: N/M correct
- Review carefully: <file:line — why, for each missed question; or "nothing flagged">
- Deviations from plan: <one line each, from the deviation log; or "none">
```

## Rules

- Never skip the quiz because the diff "looks simple" — simple diffs hide the
  best surprises. But never pad with fake-risk questions.
- Questions must be answerable from the diff the user supposedly reviewed; no
  gotchas about untouched code.
