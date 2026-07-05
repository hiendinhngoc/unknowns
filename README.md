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
