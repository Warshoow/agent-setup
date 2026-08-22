#!/usr/bin/env bash
set -uo pipefail

LIMIT=${CTX_LIMIT:-200000}
WARN=$(( LIMIT * 85 / 100 ))

input=$(cat)

# extraction d'un champ string du JSON reçu sur stdin
field() {
  printf '%s' "$input" \
    | grep -o "\"$1\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" | head -n 1 \
    | sed 's/.*:[[:space:]]*"//; s/"$//'
}

transcript=$(field transcript_path)
session=$(field session_id)
[ -f "${transcript:-/nonexistent}" ] || exit 0

# dernière ligne portant un bloc usage (hors sous-agents)
line=$(tail -n 500 "$transcript" | grep '"usage"' | grep -v '"isSidechain":true' | tail -n 1)
[ -n "$line" ] || exit 0

num() {
  v=$(printf '%s' "$line" \
        | grep -o "\"$1\"[[:space:]]*:[[:space:]]*[0-9][0-9]*" | tail -n 1 \
        | grep -o '[0-9][0-9]*$')
  printf '%s' "${v:-0}"
}

tokens=$(( $(num input_tokens) \
         + $(num cache_read_input_tokens) \
         + $(num cache_creation_input_tokens) \
         + $(num output_tokens) ))

state="${TMPDIR:-/tmp}/cc-ctx-${session:-x}"
prev=$(cat "$state" 2>/dev/null || echo 0)

if   [ "$tokens" -ge "$LIMIT" ]; then level=2
elif [ "$tokens" -ge "$WARN"  ]; then level=1
else level=0; fi

echo "$level" > "$state"
[ "$level" -le "$prev" ] && exit 0

pct=$(( tokens * 100 / LIMIT ))
if [ "$level" -eq 2 ]; then
  msg="Contexte : ${tokens} tokens (${pct}% de ${LIMIT}) - pense a /compact ou /clear."
else
  msg="Contexte : ${tokens} tokens (${pct}% de ${LIMIT}) - tu approches de la limite."
fi

cat <<EOF
{"systemMessage": "$msg", "terminalSequence": "\u001b]777;notify;Claude Code;$msg\u0007"}
EOF
exit 0
