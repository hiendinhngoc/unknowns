# unknowns

Agent skills for systematically discovering and closing knowledge gaps before,
during, and after implementation.

The techniques come from
[Know Your Unknowns](https://thariqs.github.io/html-effectiveness/unknowns/)
by Thariq Shihipar — all credit for the ideas goes to him. This repo turns
them into invocable [Agent Skills](https://www.agensi.io/learn/agent-skills-open-standard)
(SKILL.md format) for Claude Code, Codex CLI, OpenCode, and other agents.

## Skills

| Skill | Phase | What it does |
|---|---|---|
| `/unknowns:blindspot` | pre-implementation | Read-only risk recon of an unfamiliar system |
| `/unknowns:verify-ref` | pre-implementation | Comprehension proof before porting existing code |
| `/unknowns:mock` | pre-implementation | Throwaway interactive prototype before production code |
| `/unknowns:log-deviation` | during | Log every place the code forced a plan deviation |
| `/unknowns:merge-quiz` | pre-merge | Quiz the USER on the riskiest parts of the diff |
| `/unknowns:unknowns` | any | Orchestrator: detects phase, routes to the right skill |

## Installation

### Claude Code (as a plugin)

```
/plugin marketplace add hiendinhngoc/unknowns
/plugin install unknowns@unknowns
```

Restart Claude Code. Skills appear as `/unknowns:<name>` in every project.

For local development, add your clone by path instead:

```
/plugin marketplace add /path/to/unknowns
```

### Codex CLI

Copy the skill directories into Codex's skills folder:

```bash
cp -r skills/* ~/.codex/skills/
```

### OpenCode

```bash
# global (all projects)
cp -r skills/* ~/.config/opencode/skills/
# or per project
cp -r skills/* .opencode/skills/
```

### Other agents (Gemini CLI, Cursor, Cline, Hermes, ...)

The skills are plain `SKILL.md` files following the open Agent Skills standard
(YAML frontmatter + markdown instructions). Any agent that supports the
standard can load them from its skills directory. For agents without native
skill support, paste a SKILL.md's body into the system/custom prompt — it
works as a plain instruction set.

## Usage

Invoke skills directly by name, or let the agent auto-trigger them from the
descriptions ("what am I missing here?" triggers blindspot, "port X" triggers
verify-ref, etc.).

**Starting work in unfamiliar code:**

```
/unknowns:blindspot src/billing/
```

→ ranked list of 5–7 risks, each with a ready-to-paste follow-up prompt.

**Porting or adapting existing code:**

```
/unknowns:verify-ref port the retry logic from legacy/http_client.py
```

→ the agent must produce a comprehension proof (data flow, edge cases,
invariants, hidden deps) and get your confirmation before writing any code.

**Undecided UX or behavior:**

```
/unknowns:mock the new filter panel — inline vs sidebar?
```

→ disposable interactive HTML prototype; ends with a short spec of validated
decisions. Prototype code is never copied into the codebase.

**Mid-implementation, when reality contradicts the plan:**

```
/unknowns:log-deviation the API doesn't support batch deletes after all
```

→ appends a structured entry to `docs/deviations/YYYY-MM-DD-<task>.md`.

**Before merging:**

```
/unknowns:merge-quiz
```

→ 3–5 questions about the riskiest parts of your diff. Missed answers get
explained and flagged; ends with a paste-ready merge-readiness note for the PR.

**Not sure which applies:**

```
/unknowns:unknowns
```

→ detects your phase from git state and routes to the right skill.

## Portability notes

Three skills mention Claude Code-specific tools; each degrades gracefully
elsewhere (the SKILL.md files say so inline):

- **mock** renders via the Artifact tool → other agents write the HTML file
  and you open it in a browser.
- **merge-quiz** uses AskUserQuestion for multiple choice → other agents ask
  in plain text.
- **unknowns** invokes sub-skills via the Skill tool → other agents follow the
  named skill's instructions directly.

The plugin packaging (`.claude-plugin/`) is Claude Code-only; the `skills/`
directory is the portable part.

## Contributing

New skills welcome — the bar is that they surface unknowns and don't duplicate
what the ecosystem already covers. See [CONTRIBUTING.md](CONTRIBUTING.md) for
skill structure conventions and local testing. `tests/eval.sh` behavior-tests
the non-interactive skills against a live agent (manual, costs tokens). Design
docs live in [`docs/specs/`](docs/specs/), with historical implementation plans
in [`docs/plans/`](docs/plans/).

## Releases

Automated by [release-please](https://github.com/googleapis/release-please)
from conventional commits: `fix:` bumps patch, `feat:` bumps minor, `feat!:`
bumps major. It keeps a release PR open on main; merging it tags the release,
writes the changelog, and bumps the version in `.claude-plugin/plugin.json`.

This repo also uses Lore trailers in commit bodies. The two conventions are
meant to be combined, not chosen between. Put the conventional commit prefix on
the first line, then keep the Lore body and trailers below it. Examples:

```text
fix: keep local agent state out of reviews
feat: add a skill for pre-merge comprehension checks
feat!: rename the public skill namespace
```

To force a specific version, add a `Release-As: x.y.z` footer to any commit
on main.

## License

[MIT](LICENSE) © 2026 Hien Dinh. Techniques by
[Thariq Shihipar](https://thariqs.github.io/html-effectiveness/unknowns/).
