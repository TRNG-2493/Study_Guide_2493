#!/usr/bin/env bash
# setup_conflict.sh -- build the Part D conflict lab, the same way every time.
#
# Usage:
#   bash setup_conflict.sh                 # creates ./conflict-lab, ALREADY STOPPED in a conflicted merge
#   bash setup_conflict.sh my-folder       # use another folder name or path
#   bash setup_conflict.sh --force         # delete an existing conflict-lab (only if it is a lab repo) and rebuild
#   bash setup_conflict.sh --no-merge      # build the two diverged branches but do NOT run the merge yet
#
# What it builds (branches: main and feature/strict-gate; HEAD on main):
#   * Add strict gate and payments suite   <- feature/strict-gate
#   | * Lower gate and add checkout suite  <- main (HEAD)
#   |/
#   * Add nightly gate settings and report <- common ancestor
# Then it runs:  git merge feature/strict-gate
# Result: settings.py and report.py are in conflict; CHANGELOG.md merges by itself.
#
# Setup commits use fixed names, dates and a local-only config so the repo is identical on every
# machine. The MERGE COMMIT you make yourself uses YOUR Git identity (git config --global user.name ...).
set -u

DIR="conflict-lab"; FORCE=0; MERGE=1
for arg in "$@"; do
  case "$arg" in
    --force)    FORCE=1 ;;
    --no-merge) MERGE=0 ;;
    -h|--help)  sed -n '2,19p' "$0"; exit 0 ;;
    *)          DIR="$arg" ;;
  esac
done

command -v git >/dev/null 2>&1 || { echo "git is not installed or not on PATH" >&2; exit 1; }

if [ -e "$DIR" ]; then
  if [ "$FORCE" -eq 1 ] && [ -d "$DIR/.git" ] && [ -f "$DIR/settings.py" ] && [ -f "$DIR/report.py" ]; then
    rm -rf "$DIR"        # only ever removes a folder that looks like THIS lab
  else
    echo "Folder '$DIR' already exists. Re-run with --force to rebuild it (only lab repos are removed)." >&2
    exit 1
  fi
fi

mkdir -p "$DIR" && cd "$DIR" || exit 1
git init -q -b main 2>/dev/null || { git init -q && git checkout -q -b main; }   # -b needs Git 2.28+
git config core.autocrlf false          # local to this repo: identical files on Windows and Linux
git config merge.conflictstyle merge    # classic markers (<<<<<<< ======= >>>>>>>)

# portable in-place edit (GNU and BSD/macOS sed differ on -i)
sedit() { sed "$1" "$2" > "$2.tmp" && mv "$2.tmp" "$2"; }

# commit helper: fixed author + date so the setup is reproducible
commit() {  # usage: commit "message" "Author Name" "2026-01-05T10:00:00"
  GIT_AUTHOR_NAME="$2" GIT_AUTHOR_EMAIL="setup@example.com" GIT_AUTHOR_DATE="$3 +0000" \
  GIT_COMMITTER_NAME="$2" GIT_COMMITTER_EMAIL="setup@example.com" GIT_COMMITTER_DATE="$3 +0000" \
  git commit -q -a -m "$1"
}

# ---- common ancestor ----------------------------------------------------------
printf '%s\n' \
  '# Nightly smoke run: shared team settings' \
  'PASS_THRESHOLD = 90   # percent of tests that must pass for a GREEN run' \
  'RETRIES = 1' \
  'TIMEOUT_SECONDS = 30' \
  'REPORT_FORMAT = "text"' \
  'REPORT_DIR = "out"' \
  'SUITES = ["login", "search"]' > settings.py

printf '%s\n' \
  '"""Print the verdict for the nightly smoke run."""' \
  'from settings import PASS_THRESHOLD, SUITES' \
  '' \
  '' \
  'def verdict(rate):' \
  '    return "GREEN" if rate >= PASS_THRESHOLD else "RED"' \
  '' \
  '' \
  'def main():' \
  '    print("Suites:", ", ".join(SUITES))' \
  '    print("Verdict for 93.0%:", verdict(93.0))' \
  '' \
  '' \
  'if __name__ == "__main__":' \
  '    main()' > report.py

printf '%s\n' '# Changelog' '' '## Unreleased' '- Nightly smoke run reports a GREEN or RED verdict' > CHANGELOG.md
git add settings.py report.py CHANGELOG.md
git add -A && commit "Add nightly gate settings and report" "Team Lead" "2026-01-05T09:00:00"

# ---- feature/strict-gate: Sam wants a stricter gate and the payments suite --------
git switch -q -c feature/strict-gate
sedit 's/^PASS_THRESHOLD = 90 .*/PASS_THRESHOLD = 95   # percent of tests that must pass for a GREEN run/' settings.py
sedit 's/^SUITES = .*/SUITES = ["login", "search", "payments"]/' settings.py
awk '{print} /return "GREEN" if rate/ {print ""; print ""; print "def failing_suites(results):"; print "    \"\"\"Names of suites that have at least one failed test, sorted.\"\"\""; print "    return sorted({r[\"suite\"] for r in results if r[\"status\"] == \"fail\"})"}' report.py > report.tmp && mv report.tmp report.py
printf '%s\n' '- Strict gate: payments suite added, threshold raised (Sam)' >> CHANGELOG.md
commit "Add strict gate and payments suite" "Sam" "2026-01-05T11:00:00"

# ---- main: Priya lowers the gate and adds the checkout suite ---------------------
git switch -q main
sedit 's/^PASS_THRESHOLD = 90 .*/PASS_THRESHOLD = 92   # percent of tests that must pass for a GREEN run/' settings.py
sedit 's/^SUITES = .*/SUITES = ["login", "search", "checkout"]/' settings.py
awk '{print} /return "GREEN" if rate/ {print ""; print ""; print "def summary_line(passed, total):"; print "    \"\"\"One line for the morning email, e.g. \"3/4 passed (75.0%)\".\"\"\""; print "    return f\"{passed}/{total} passed ({passed / total * 100:.1f}%)\""}' report.py > report.tmp && mv report.tmp report.py
{ printf '%s\n' '# Changelog (team: QE Foundations)'; tail -n +2 CHANGELOG.md; } > CHANGELOG.tmp && mv CHANGELOG.tmp CHANGELOG.md
commit "Lower gate and add checkout suite" "Priya" "2026-01-05T10:30:00"

echo "Lab repo ready in: $(pwd)"
git log --oneline --graph --all

if [ "$MERGE" -eq 1 ]; then
  echo
  echo "--- git merge feature/strict-gate ---"
  git merge feature/strict-gate || true      # a conflict is the point; do not stop the script
  echo "--- git status -s ---"
  git status -s
  echo
  echo "You are now in the middle of a conflicted merge. cd \"$DIR\" and start Part D."
else
  echo
  echo "Next: cd \"$DIR\" and run:  git merge feature/strict-gate"
fi
exit 0
