---
name: blindspot
description: Read-only reconnaissance pass over an unfamiliar codebase, system, or feature area to surface hidden risks before any code is written. Use when starting work in unfamiliar territory, before a risky change, or when the user says "blindspot pass", "what am I missing", or "scan for risks".
---

# Blindspot Pass

Find the unknowns in a system BEFORE touching it. Reconnaissance only.

<HARD-RULE>Read-only. Do not edit, create, or delete any project file. No fixes, however tempting.</HARD-RULE>

## Process

1. **Identify the target.** Use the argument or infer the directory/system/feature
   from conversation. If no target is discernible, ask for one — don't guess.
2. **Explore.** Use Glob/Grep/Read (and git log for churn hotspots) to understand
   the target. Look specifically for:
   - Hidden coupling: modules that import each other's internals, shared mutable
     state, implicit ordering dependencies
   - Unowned edge cases: error paths that swallow exceptions, TODO/FIXME/HACK
     comments, empty catch blocks
   - Stale assumptions: config or constants that encode outdated facts, comments
     contradicting code, dead feature flags
   - Missing tests around dangerous paths: money, auth, deletion, migrations,
     concurrency — anything irreversible with no test coverage
   - Churn hotspots: files with many recent fixes (`git log --oneline -- <path>`)
3. **Report 5–7 findings, ranked by risk** (highest first).

## Output format (per finding)

```
### N. <one-line risk statement>  [risk: high|medium|low]
Why it matters: <1-2 sentences, concrete failure scenario>
Investigate: `<ready-to-paste follow-up prompt the user can run next>`
```

End with a one-line recommendation of which finding to chase first.
