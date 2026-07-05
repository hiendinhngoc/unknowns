---
name: merge-quiz
description: Pre-merge comprehension gate that quizzes the USER on the riskiest parts of the branch diff. Use before merging or opening a PR, or when the user says "merge quiz", "am I ready to merge", or "quiz me on this diff".
---

# Merge Readiness Quiz

Before shipping, verify the HUMAN understands what's being merged. The quiz
tests the user, not Claude.

## Process

1. **Gather the material.**
   - Diff: `git diff <default-branch>...HEAD`. If there is no diff against the
     default branch, say so and stop.
   - Deviation log: read `docs/deviations/*.md` entries dated during this branch's
     lifetime, if any exist.
2. **Pick the 3–5 riskiest spots.** Prioritize: behavior changes on dangerous
   paths (auth, money, deletion, migrations), deviations from the plan, error
   handling changes, anything irreversible.
3. **Quiz one question at a time** using AskUserQuestion (or plain-text
   multiple choice if this agent has no such tool). Each question:
   - Cites the exact file:line it's about
   - Asks about consequences, not trivia: "what happens if X is null here?",
     "why did we bypass Y?", "what breaks if this runs twice?"
   - Offers 3-4 plausible answers (one correct, distractors that reflect real
     misunderstandings)
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
  best surprises.
- Questions must be answerable from the diff the user supposedly reviewed; no
  gotchas about untouched code.
