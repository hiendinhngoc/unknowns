# Unknowns Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `unknowns` Claude Code plugin — six markdown skills implementing the novel techniques from Thariq's "Know Your Unknowns" article.

**Architecture:** One plugin repo at `/Users/hien/Developer/unknowns`. Five technique skills plus one orchestrator router, each a `skills/<name>/SKILL.md` with YAML frontmatter. No executable code; verification is JSON validity, frontmatter presence, and manual invocation after install.

**Tech Stack:** Claude Code plugin format (`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `skills/*/SKILL.md`).

**Repo:** `/Users/hien/Developer/unknowns` (already initialized, spec committed). All paths below are relative to it.

---

### Task 1: Plugin scaffold

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/marketplace.json`
- Create: `README.md`

- [ ] **Step 1: Write plugin.json**

```json
{
  "name": "unknowns",
  "description": "Skills for discovering and closing knowledge gaps across the dev lifecycle, from Thariq's 'Know Your Unknowns'",
  "version": "0.1.0",
  "author": { "name": "Hien Dinh" }
}
```

- [ ] **Step 2: Write marketplace.json** (lets the repo act as a local marketplace for installation)

```json
{
  "name": "unknowns-local",
  "owner": { "name": "Hien Dinh" },
  "plugins": [
    {
      "name": "unknowns",
      "source": "./",
      "description": "Know-your-unknowns lifecycle skills"
    }
  ]
}
```

- [ ] **Step 3: Write README.md**

```markdown
# unknowns

Claude Code plugin implementing the novel techniques from
[Know Your Unknowns](https://thariqs.github.io/html-effectiveness/unknowns/).

## Skills

| Skill | Phase | What it does |
|---|---|---|
| `/unknowns:blindspot` | pre-implementation | Read-only risk recon of an unfamiliar system |
| `/unknowns:verify-ref` | pre-implementation | Comprehension proof before porting existing code |
| `/unknowns:mock` | pre-implementation | Throwaway interactive prototype before production code |
| `/unknowns:log-deviation` | during | Log every place the code forced a plan deviation |
| `/unknowns:merge-quiz` | pre-merge | Quiz the USER on the riskiest parts of the diff |
| `/unknowns:unknowns` | any | Orchestrator: detects phase, routes to the right skill |

## Install

```
/plugin marketplace add /Users/hien/Developer/unknowns
/plugin install unknowns@unknowns-local
```
```

- [ ] **Step 4: Verify JSON validity**

Run: `python3 -m json.tool .claude-plugin/plugin.json && python3 -m json.tool .claude-plugin/marketplace.json`
Expected: both files echoed back, exit 0.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: plugin scaffold"
```

---

### Task 2: blindspot skill

**Files:**
- Create: `skills/blindspot/SKILL.md`

- [ ] **Step 1: Write SKILL.md**

````markdown
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
````

- [ ] **Step 2: Verify frontmatter**

Run: `head -4 skills/blindspot/SKILL.md | grep -c 'name: blindspot'`
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add skills/blindspot && git commit -m "feat: blindspot skill"
```

---

### Task 3: verify-ref skill

**Files:**
- Create: `skills/verify-ref/SKILL.md`

- [ ] **Step 1: Write SKILL.md**

````markdown
---
name: verify-ref
description: Comprehension gate before porting, copying, or adapting an existing implementation. Proves understanding of the reference code before any new code is written. Use when the task is "port X", "copy how Y does it", "adapt Z", or reimplementing existing behavior.
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
   confirmation may implementation begin.

## Output format

```
## Comprehension proof: <reference name> (<file:line range>)
### Data flow
### Edge cases handled
### Invariants
### Hidden dependencies
### What would break if I got this wrong?
```
````

- [ ] **Step 2: Verify frontmatter**

Run: `head -4 skills/verify-ref/SKILL.md | grep -c 'name: verify-ref'`
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add skills/verify-ref && git commit -m "feat: verify-ref skill"
```

---

### Task 4: mock skill

**Files:**
- Create: `skills/mock/SKILL.md`

- [ ] **Step 1: Write SKILL.md**

````markdown
---
name: mock
description: Build a throwaway interactive prototype to validate behavior and UX before writing production code. Use when requirements are vague, the user says "mock it up first", "prototype this", or before wiring a feature whose look/behavior is undecided.
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
````

- [ ] **Step 2: Verify frontmatter**

Run: `head -4 skills/mock/SKILL.md | grep -c 'name: mock'`
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add skills/mock && git commit -m "feat: mock skill"
```

---

### Task 5: log-deviation skill

**Files:**
- Create: `skills/log-deviation/SKILL.md`

- [ ] **Step 1: Write SKILL.md**

````markdown
---
name: log-deviation
description: Record a place where the code forced a deviation from the agreed plan. Use mid-implementation whenever reality contradicts the plan, or when the user says "log this deviation". The log feeds future planning and the merge quiz.
---

# Deviation Log

The plan said one thing; the code demanded another. Record it while it's fresh —
these entries are the highest-value input to the next plan.

## Where the log lives

- In a git repo: `docs/deviations/YYYY-MM-DD-<task-slug>.md` at the repo root
  (create `docs/deviations/` if needed). `<task-slug>` = short kebab-case name
  of the current task, stable across the whole task so entries append to one file.
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
````

- [ ] **Step 2: Verify frontmatter**

Run: `head -4 skills/log-deviation/SKILL.md | grep -c 'name: log-deviation'`
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add skills/log-deviation && git commit -m "feat: log-deviation skill"
```

---

### Task 6: merge-quiz skill

**Files:**
- Create: `skills/merge-quiz/SKILL.md`

- [ ] **Step 1: Write SKILL.md**

````markdown
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
3. **Quiz one question at a time** using AskUserQuestion. Each question:
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
````

- [ ] **Step 2: Verify frontmatter**

Run: `head -4 skills/merge-quiz/SKILL.md | grep -c 'name: merge-quiz'`
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add skills/merge-quiz && git commit -m "feat: merge-quiz skill"
```

---

### Task 7: unknowns orchestrator skill

**Files:**
- Create: `skills/unknowns/SKILL.md`

- [ ] **Step 1: Write SKILL.md**

````markdown
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
````

- [ ] **Step 2: Verify frontmatter**

Run: `head -4 skills/unknowns/SKILL.md | grep -c 'name: unknowns'`
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add skills/unknowns && git commit -m "feat: unknowns orchestrator skill"
```

---

### Task 8: Final validation and install

- [ ] **Step 1: Verify all six skills have valid frontmatter**

Run:
```bash
for f in skills/*/SKILL.md; do
  head -1 "$f" | grep -q '^---$' && grep -q '^name: ' "$f" && grep -q '^description: ' "$f" && echo "OK $f" || echo "FAIL $f"
done
```
Expected: six `OK` lines, no `FAIL`.

- [ ] **Step 2: Verify structure matches spec**

Run: `ls skills/`
Expected: `blindspot  log-deviation  merge-quiz  mock  unknowns  verify-ref`

- [ ] **Step 3: Install (user runs in Claude Code)**

```
/plugin marketplace add /Users/hien/Developer/unknowns
/plugin install unknowns@unknowns-local
```

- [ ] **Step 4: Manual smoke test**

In a real project session after restart: invoke `/unknowns:blindspot` on any
directory and confirm it explores read-only and outputs ranked findings. Then
`/unknowns:unknowns` and confirm it detects phase and routes.

- [ ] **Step 5: Commit any remaining files**

```bash
git add -A && git commit -m "chore: final validation" || echo "nothing to commit"
```
