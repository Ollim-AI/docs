#!/usr/bin/env bash
set -euo pipefail

MODEL="${MODEL:-opus}"
MAX_ITERATIONS="${MAX_ITERATIONS:-42}"
PROMPT_FILE="PROMPT.md"
DOCS_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_DIR="literal:../ollim-bot"

ITERATION=0
TMPFILE=$(mktemp)
trap 'rm -f "$TMPFILE"' EXIT

remaining_pages() {
    grep -rl "Content coming soon" "$DOCS_DIR" --include="*.mdx" 2>/dev/null | wc -l
}

echo "ralph loop: model=$MODEL max=$MAX_ITERATIONS"
echo ""

REMAINING=$(remaining_pages)
if [ "$REMAINING" -eq 0 ]; then
    echo "all pages already written — nothing to do"
    exit 0
fi
echo "$REMAINING pages remaining"

while [ "$ITERATION" -lt "$MAX_ITERATIONS" ]; do
    ITERATION=$((ITERATION + 1))
    echo ""
    echo "━━━ iteration $ITERATION / $MAX_ITERATIONS ━━━"
    echo ""

    cat "$DOCS_DIR/$PROMPT_FILE" | claude -p \
        --dangerously-skip-permissions \
        --model "$MODEL" \
        --no-session-persistence \
        --add-dir "$SOURCE_DIR" \
        2>&1 | tee "$TMPFILE"

    # primary exit: check file state
    REMAINING=$(remaining_pages)
    echo ""
    echo "pages remaining: $REMAINING"

    if [ "$REMAINING" -eq 0 ]; then
        echo ""
        echo "━━━ ALL PAGES WRITTEN after $ITERATION iterations ━━━"
        exit 0
    fi

    # secondary exit: promise in output
    if grep -q "ALL PAGES COMPLETE" "$TMPFILE" 2>/dev/null; then
        echo ""
        echo "━━━ PROMISE detected after $ITERATION iterations ━━━"
        exit 0
    fi
done

echo ""
echo "━━━ MAX ITERATIONS ($MAX_ITERATIONS) reached — $REMAINING pages remaining ━━━"
exit 1
