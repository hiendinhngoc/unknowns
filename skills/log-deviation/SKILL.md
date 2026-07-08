---
name: log-deviation
description: Record a place where the code forced a deviation from the agreed plan. Use mid-implementation whenever reality contradicts the plan, or when the user says "log this deviation". The log feeds future planning and the merge quiz.
version: 1.0.0
author: Hien Dinh
license: MIT
---

# Deviation Log

The plan said one thing; the code demanded another. Record it while it's fresh —
these entries are the highest-value input to the next plan.

## Where the log lives

- In a git repo: `docs/deviations/YYYY-MM-DD-<task-slug>.md` at the repo root
  (create `docs/deviations/` if needed). `<task-slug>` = short kebab-case name
  of the current task. Before creating a new file, glob
  `docs/deviations/*-<task-slug>.md` — if a file for this task already exists
  (even from an earlier day/session), append to it instead of creating another.
- Outside a git repo: write to the session scratchpad instead and tell the user
  the path.

## Entry format (append, newest last)

```markdown
## <HH:MM> — <one-line summary>
- **Plan said:** <what the plan/spec assumed>
- **Code forced:** <what was actually done instead>
- **Why:** <the real-world constraint that made the plan wrong>
- **Ripple:** <other plan steps this invalidates, or "none">
```

## Rules

- One entry per deviation, logged at the moment it happens — not batched at the end.
- "Why" names the constraint (API limitation, hidden coupling, wrong assumption),
  never just "it didn't work".
- If invoked with no deviation to log, ask what deviated rather than inventing one.
- Do not commit the log automatically; leave staging to the user's normal flow.
