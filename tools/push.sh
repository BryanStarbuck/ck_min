#!/bin/sh
# Safe push for charlie-kirk.
#
# WHY THIS EXISTS
# ---------------
# A plain `git push` here fails intermittently with:
#
#   ! [remote rejected] main -> main (cannot lock ref 'refs/heads/main':
#     is at <A> but expected <B>)
#
# That is NOT a size problem, NOT a non-fast-forward, and NOT lost data. It is a
# lost compare-and-swap on the remote ref. This repo pushes ~180 MB of gzipped
# ADS-B evidence at a few MB/s, so a push holds the connection open for the best
# part of a minute, and an external auto-commit job on the other machine
# ("Bryan 26 Tower" / "Bryan 27 Laptop") can land its own push inside that
# window. GitHub then rejects the WHOLE upload even though every object arrived.
#
# The objects are already on the server at that point. Retrying after a rebase
# costs almost nothing because the objects do not need re-uploading.
#
# This script never force-pushes and never creates or switches a branch, per the
# repo's git rules in CLAUDE.md.
#
# Usage:  sh tools/push.sh [max_attempts]     (default 5)

set -e

REPO=$(git rev-parse --show-toplevel 2>/dev/null) || {
    echo "push.sh: not inside a git repository" >&2
    exit 1
}
cd "$REPO"

BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "main" ]; then
    echo "push.sh: refusing to run on branch '$BRANCH'; this repo works on main only." >&2
    exit 1
fi

ATTEMPTS=${1:-5}
n=1

# Already-there check: if our HEAD is contained in origin/main, the content is
# live no matter what an earlier push printed.
already_pushed() {
    git fetch --quiet origin main 2>/dev/null || return 1
    git merge-base --is-ancestor HEAD origin/main 2>/dev/null
}

while [ "$n" -le "$ATTEMPTS" ]; do
    echo "== push attempt $n/$ATTEMPTS =="

    if git push origin HEAD:main; then
        echo "== pushed OK on attempt $n =="
        exit 0
    fi

    echo "-- push rejected; checking whether the content landed anyway --"

    if already_pushed; then
        echo "== HEAD ($(git rev-parse --short HEAD)) is already contained in origin/main. =="
        echo "== Nothing was lost. The rejection was a ref race, not a failed upload. =="
        exit 0
    fi

    # We are genuinely behind or diverged. Replay our commits on top of theirs.
    echo "-- rebasing onto origin/main and retrying --"
    if ! git pull --rebase origin main; then
        git rebase --abort 2>/dev/null || true
        echo "push.sh: rebase onto origin/main hit a conflict. Resolve it by hand," >&2
        echo "         then re-run this script. Nothing was force-pushed." >&2
        exit 1
    fi

    n=$((n + 1))
    [ "$n" -le "$ATTEMPTS" ] && sleep $((n * 3))
done

echo "push.sh: still rejected after $ATTEMPTS attempts." >&2
echo "         Run 'git fetch origin && git log --oneline origin/main..HEAD' to see" >&2
echo "         what is genuinely unpushed. Do NOT force-push." >&2
exit 1
