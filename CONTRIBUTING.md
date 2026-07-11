# Contributing

Contributions welcome — especially new skills that surface unknowns the
existing ones miss.

## What makes a good skill for this repo

- **It implements a knowledge-gap technique.** The theme is discovering and
  closing unknowns across the dev lifecycle, not general productivity.
- **It's novel in the ecosystem.** This repo deliberately excludes techniques
  already covered by widely-installed skills (brainstorming, plan writing,
  interview-style grilling, design iteration). Check before proposing.
- **It's portable.** Stick to the core Agent Skills format. If you reference an
  agent-specific tool (Artifact, AskUserQuestion, ...), include a one-line
  plain-text fallback so the skill degrades gracefully in other agents.

## Skill structure

Each skill is one directory with portable instructions and client metadata:

```text
skills/<kebab-name>/
├── SKILL.md
└── agents/openai.yaml
```

```markdown
---
name: <kebab-name>            # must match the directory name
description: <what it does + when to use it, including trigger phrases>
---

# Title

One-line purpose statement.

<HARD-RULE>Non-negotiable constraints go in a tag like this, near the top.</HARD-RULE>

## Process
Numbered steps. Concrete, not aspirational.

## Output format
A fenced template of exactly what the skill should produce.
```

Conventions:

- The `description` frontmatter decides auto-triggering — include the phrases
  a user would actually say.
- Hard constraints (`read-only`, `don't touch the codebase`, gates) go in
  `<HARD-RULE>`/`<HARD-GATE>` tags before the process steps.
- Every technique skill defines a verifiable output contract. Routers may
  instead define deterministic routing outcomes.
- If input is ambiguous, the skill should ask — never guess.
- Keep `SKILL.md` below 500 lines. Add directly linked `references/`, `scripts/`,
  or `assets/` only when progressive disclosure or deterministic execution
  justifies the extra file.
- Keep `agents/openai.yaml` aligned with the skill. Its `default_prompt` must
  name the skill as `$<kebab-name>`.

## Testing locally

```
/plugin marketplace add /path/to/your/clone
/plugin install unknowns@unknowns
```

Restart Claude Code, invoke your skill on a real project, and check it follows
its own hard rules and output format. Other agents: copy `skills/<name>/` into
the agent's skills directory (see README).

## Validation

CI checks that the JSON manifests parse and every SKILL.md has valid
frontmatter, README coverage, and portable tool fallbacks. Run it locally:

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Pull requests

One skill (or one focused change) per PR. In the description, say what unknown
the skill surfaces and give one real example of using it.
