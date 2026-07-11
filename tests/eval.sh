#!/usr/bin/env bash
# Opt-in live behavioral eval. Requires the Claude CLI and installed plugin;
# each case consumes API tokens. Outputs exist only for the duration of the run.
set -euo pipefail

command -v claude >/dev/null || { echo "SKIP: claude CLI not installed"; exit 2; }

fixture=$(mktemp -d)
trap 'rm -rf "$fixture"' EXIT
git -C "$fixture" init -q
git -C "$fixture" branch -m main
cat > "$fixture/pay.py" <<'EOF'
def charge(amount, retries=3):
    # TODO: handle currency mismatch
    for i in range(retries):
        try:
            return gateway.charge(amount)
        except Exception:
            pass  # swallow and retry
EOF
git -C "$fixture" add -A
git -C "$fixture" -c user.email=t@t -c user.name=t commit -qm init

fail=0
run_read_only() { # name / prompt / required fixed strings...
  local name=$1 prompt=$2 output="$fixture/$1.out" before after marker case_failed=0
  shift 2
  before=$(git -C "$fixture" status --porcelain=v1)
  if ! (cd "$fixture" && claude -p "$prompt" --max-turns 15) >"$output" 2>&1; then
    echo "FAIL $name (claude command failed)"; fail=1; return
  fi
  after=$(git -C "$fixture" status --porcelain=v1 | grep -vF "?? $name.out" || true)
  for marker in "$@"; do
    grep -Fqi "$marker" "$output" || { echo "FAIL $name (missing '$marker')"; fail=1; case_failed=1; }
  done
  [[ "$before" == "$after" ]] || { echo "FAIL $name (modified fixture)"; fail=1; case_failed=1; }
  [[ $case_failed -eq 0 ]] && echo "OK   $name"
}

run_read_only blindspot "/unknowns:blindspot pay.py" "[risk:" "Why it matters:" "Investigate:"
run_read_only verify-ref "/unknowns:verify-ref port the retry logic from pay.py" \
  "## Comprehension proof:" "### Data flow" "### Hidden dependencies" \
  "### What would break if I got this wrong?"

deviation_output="$fixture/log-deviation.out"
if ! (cd "$fixture" && claude -p "/unknowns:log-deviation the gateway has no batch API, plan assumed it did" --max-turns 15) >"$deviation_output" 2>&1; then
  echo "FAIL log-deviation (claude command failed)"; fail=1
fi
deviation_file=$(find "$fixture/docs/deviations" -type f -name '*.md' -print -quit 2>/dev/null || true)
if [[ -z "$deviation_file" ]]; then
  echo "FAIL log-deviation (no deviation file)"; fail=1
else
  case_failed=0
  for marker in "**Plan said:**" "**Code forced:**" "**Why:**" "**Ripple:**"; do
    grep -Fq "$marker" "$deviation_file" || { echo "FAIL log-deviation (missing '$marker')"; fail=1; case_failed=1; }
  done
  git -C "$fixture" diff --cached --quiet || { echo "FAIL log-deviation (staged changes)"; fail=1; case_failed=1; }
  [[ $case_failed -eq 0 ]] && echo "OK   log-deviation"
fi

exit "$fail"
