#!/usr/bin/env bash
# Behavioral smoke-eval for the non-interactive skills. Manual run (costs API
# tokens): ./tests/eval.sh   Requires the claude CLI with this plugin installed.
# For each skill: fire a realistic trigger prompt in a throwaway fixture repo
# and assert the output contains the skill's required format marker.
# ponytail: covers blindspot/verify-ref/log-deviation only; mock and merge-quiz
# are interactive (Artifact/AskUserQuestion) — test those by hand.
set -u

fixture=$(mktemp -d)
trap 'rm -rf "$fixture"' EXIT
git -C "$fixture" init -q
cat > "$fixture/pay.py" <<'EOF'
def charge(amount, retries=3):
    # TODO: handle currency mismatch
    for i in range(retries):
        try:
            return gateway.charge(amount)
        except Exception:
            pass  # swallow and retry
EOF
git -C "$fixture" add -A && git -C "$fixture" -c user.email=t@t -c user.name=t commit -qm init

run() { # name / prompt / marker
  out=$(cd "$fixture" && claude -p "$2" --max-turns 15 2>&1)
  if grep -qi "$3" <<<"$out"; then echo "OK   $1"; else echo "FAIL $1 (marker '$3' missing)"; fail=1; fi
}

fail=0
run blindspot     "/unknowns:blindspot pay.py"                                   "risk:"
run verify-ref    "/unknowns:verify-ref port the retry logic from pay.py"       "comprehension proof"
run log-deviation "/unknowns:log-deviation the gateway has no batch API, plan assumed it did" "plan said"
exit $fail
