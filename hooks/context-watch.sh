#!/usr/bin/env bash
set -uo pipefail

LIMIT=${CTX_LIMIT:-200000}          # contexte du tour courant (= ce que montre /context)
BUDGET=${CTX_BUDGET:-20000000}      # entree cumulee sur toute la session (= la facture)
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

state="${TMPDIR:-/tmp}/cc-ctx-${session:-x}"
msgs=()

# ---------- 1. contexte du tour courant ----------
line=$(tail -n 500 "$transcript" | grep '"usage"' | grep -v '"isSidechain":true' | tail -n 1)
if [ -n "$line" ]; then
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

  prev=$(cat "$state" 2>/dev/null || echo 0)
  if   [ "$tokens" -ge "$LIMIT" ]; then level=2
  elif [ "$tokens" -ge "$WARN"  ]; then level=1
  else level=0; fi
  echo "$level" > "$state"

  if [ "$level" -gt "$prev" ]; then
    pct=$(( tokens * 100 / LIMIT ))
    if [ "$level" -eq 2 ]; then
      msgs+=("Contexte : ${tokens} tokens (${pct}% de ${LIMIT}) - pense a /compact ou /clear.")
    else
      msgs+=("Contexte : ${tokens} tokens (${pct}% de ${LIMIT}) - tu approches de la limite.")
    fi
  fi
fi

# ---------- 2. entree cumulee de la session ----------
# lecture incrementale : on ne reparse que les octets ajoutes depuis le dernier tour.
cum=$(python3 - "$transcript" "${state}.cum" 2>/dev/null <<'PY'
import json, os, sys
tp, sp = sys.argv[1], sys.argv[2]
off = tot = 0
try:
    off, tot = (int(x) for x in open(sp).read().split()[:2])
except Exception:
    pass
if os.path.getsize(tp) < off:          # transcript remplace ou tronque
    off = tot = 0
with open(tp, "rb") as f:
    f.seek(off)
    data = f.read()
end = data.rfind(b"\n")                # ignorer une derniere ligne incomplete
if end >= 0:
    for raw in data[:end].split(b"\n"):
        if not raw.strip():
            continue
        try:
            d = json.loads(raw)
        except Exception:
            continue
        if d.get("type") != "assistant" or d.get("isSidechain"):
            continue
        u = (d.get("message") or {}).get("usage") or {}
        tot += ((u.get("input_tokens") or 0)
                + (u.get("cache_read_input_tokens") or 0)
                + (u.get("cache_creation_input_tokens") or 0))
    off += end + 1
    try:
        open(sp, "w").write(f"{off} {tot}")
    except OSError:
        pass
print(tot)
PY
)

if [[ "${cum:-0}" =~ ^[0-9]+$ ]] && [ "$cum" -gt 0 ]; then
  cprev=$(cat "${state}.lvl" 2>/dev/null || echo 0)
  mult=$(( cum / BUDGET ))
  cpct=$(( cum * 100 / BUDGET ))
  # au-dela du budget on realerte a chaque multiple : 1x, 2x, 3x...
  if   [ "$mult" -ge 1 ];  then clevel=$(( mult + 1 ))
  elif [ "$cpct" -ge 85 ]; then clevel=1
  else clevel=0; fi
  echo "$clevel" > "${state}.lvl"

  if [ "$clevel" -gt "$cprev" ]; then
    cm=$(( cum / 1000000 )); bm=$(( BUDGET / 1000000 ))
    if [ "$mult" -ge 1 ]; then
      msgs+=("Budget cumule depasse : ${cm} M tokens d entree, ${cpct}% de ${bm} M. A ce niveau chaque tour se paie au prix du contexte courant - /clear pour repartir a zero.")
    else
      msgs+=("Budget cumule : ${cm} M / ${bm} M tokens d entree (${cpct}%).")
    fi
  fi
fi

# ---------- 3. sortie ----------
[ ${#msgs[@]} -eq 0 ] && exit 0
msg=$(printf '%s ' "${msgs[@]}"); msg=${msg% }
msg=${msg//\"/}
cat <<EOF
{"systemMessage": "$msg", "terminalSequence": "\u001b]777;notify;Claude Code;$msg\u0007"}
EOF
exit 0
