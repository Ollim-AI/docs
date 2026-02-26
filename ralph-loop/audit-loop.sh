#!/usr/bin/env bash
set -euo pipefail

MODEL="${MODEL:-opus}"
MAX_ITERATIONS="${MAX_ITERATIONS:-50}"
PROMPT_FILE="AUDIT-PROMPT.md"
DOCS_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_DIR="$(cd "$DOCS_DIR/.." && pwd)/ollim-bot"

ITERATION=0
TMPFILE=$(mktemp)
trap 'rm -f "$TMPFILE"' EXIT

remaining_pages() {
    grep -c '^\- \[ \]' "$DOCS_DIR/AUDIT.md" 2>/dev/null || echo 0
}

echo "audit loop: model=$MODEL max=$MAX_ITERATIONS"
echo ""

REMAINING=$(remaining_pages)
if [ "$REMAINING" -eq 0 ]; then
    echo "all pages already audited — nothing to do"
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

    # primary exit: check AUDIT.md state
    REMAINING=$(remaining_pages)
    echo ""
    echo "pages remaining: $REMAINING"

    if [ "$REMAINING" -eq 0 ]; then
        echo ""
        echo "━━━ ALL PAGES AUDITED after $ITERATION iterations ━━━"
        exit 0
    fi

    # secondary exit: COMPLETE signal in output
    if grep -q "AUDIT COMPLETE" "$TMPFILE" 2>/dev/null; then
        echo ""
        echo "━━━ COMPLETE signal after $ITERATION iterations ━━━"
        exit 0
    fi
done

echo ""
echo "━━━ MAX ITERATIONS ($MAX_ITERATIONS) reached — $REMAINING pages remaining ━━━"
exit 1
