#!/usr/bin/env python3
"""Valide et ecrit un handoff. Stdlib uniquement.

Usage:
    handoff_write.py --template                # squelette JSON a remplir
    handoff_write.py --file payload.json
    cat payload.json | handoff_write.py
    handoff_write.py --file payload.json --dry-run

Sortie: chemin du fichier ecrit (exit 0), ou liste d'erreurs actionnables
(exit 1). Les erreurs sont formulees pour etre corrigees et resoumises telles
quelles, sans avoir a relire le schema.
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import load_all, slug, store_dir  # noqa: E402

STATUSES = ["done", "partial", "blocked", "abandoned"]
POINTER_KINDS = ["file", "command", "url", "symbol"]
CONFIDENCES = ["high", "medium", "low"]
PLACEHOLDERS = {"n/a", "na", "none", "tbd", "todo", "see above", "voir plus haut",
                "idem", "cf above", "-", "aucun", "aucune", "unknown", "?"}

TEMPLATE = {
    "agent": "builder",
    "task": {"title": "", "status": "partial"},
    "summary": "",
    "decisions": [{"what": "", "why": "", "alternatives_rejected": []}],
    "failed_attempts": [{"what": "", "why_failed": "", "dont_retry": False}],
    "invariants": [{"claim": "", "scope": ""}],
    "pointers": [{"kind": "file", "ref": "", "why": ""}],
    "open_questions": [{"question": "", "blocking": False}],
    "next_steps": [],
    "resolves": [],
    "supersedes": [],
    "verified_by": [],
    "confidence": "medium",
}


class Errors(list):
    def add(self, path, msg):
        self.append(f"  [{path}] {msg}")


def _is_placeholder(s):
    return s.strip().lower().rstrip(".") in PLACEHOLDERS


def _has_code_block(s):
    """Detecte un bloc de code de plus de 5 lignes.

    Recopier du code dans un handoff garantit sa divergence avec le fichier
    reel. Le protocole veut un pointeur a la place.
    """
    if "```" in s:
        for block in re.findall(r"```.*?\n(.*?)```", s, re.S):
            if len(block.strip().splitlines()) > 5:
                return True
    lines = s.splitlines()
    run = 0
    for ln in lines:
        if ln.startswith("    ") and ln.strip():
            run += 1
            if run > 5:
                return True
        else:
            run = 0
    return False


def _check_text(err, path, value, min_len=0, max_len=None, required=True):
    if value is None or (isinstance(value, str) and not value.strip()):
        if required:
            err.add(path, "champ obligatoire, vide ou absent")
        return
    if not isinstance(value, str):
        err.add(path, f"attendu: chaine, recu: {type(value).__name__}")
        return
    v = value.strip()
    if _is_placeholder(v):
        err.add(path, f"valeur creuse ({v!r}). Ecris le contenu reel ou "
                      "supprime l'entree.")
    elif len(v) < min_len:
        err.add(path, f"trop court ({len(v)} car., minimum {min_len}). "
                      "Une justification d'une poignee de mots ne survit pas "
                      "a la relecture par un autre agent.")
    if max_len and len(v) > max_len:
        err.add(path, f"trop long ({len(v)} car., maximum {max_len}). "
                      "Decoupe, ou pointe vers un fichier.")
    if _has_code_block(v):
        err.add(path, "contient un bloc de code de plus de 5 lignes. "
                      "Ajoute un pointer {kind: file} vers la source.")


def _check_list_of_str(err, path, value, min_len=0):
    if value is None:
        return []
    if not isinstance(value, list):
        err.add(path, f"attendu: liste, recu: {type(value).__name__}")
        return []
    for i, item in enumerate(value):
        _check_text(err, f"{path}[{i}]", item, min_len=min_len)
    return value


def validate(p, known_ids, known_question_ids):
    err = Errors()

    if not isinstance(p, dict):
        err.add("racine", "le payload doit etre un objet JSON")
        return err

    unknown = set(p) - set(TEMPLATE) - {"schema_version"}
    if unknown:
        err.add("racine", f"champs inconnus: {sorted(unknown)}. Le schema est "
                          "ferme volontairement: un champ libre redevient un .md.")

    _check_text(err, "agent", p.get("agent"), min_len=2, max_len=40)

    task = p.get("task")
    if not isinstance(task, dict):
        err.add("task", "champ obligatoire, doit etre un objet {title, status}")
        task = {}
    else:
        _check_text(err, "task.title", task.get("title"), min_len=5, max_len=120)
        if task.get("status") not in STATUSES:
            err.add("task.status", f"attendu l'un de {STATUSES}, recu "
                                   f"{task.get('status')!r}")

    _check_text(err, "summary", p.get("summary"), min_len=30, max_len=600)

    for i, d in enumerate(p.get("decisions") or []):
        if not isinstance(d, dict):
            err.add(f"decisions[{i}]", "attendu un objet {what, why}")
            continue
        _check_text(err, f"decisions[{i}].what", d.get("what"), min_len=10, max_len=300)
        _check_text(err, f"decisions[{i}].why", d.get("why"), min_len=25)
        _check_list_of_str(err, f"decisions[{i}].alternatives_rejected",
                           d.get("alternatives_rejected"), min_len=5)

    for i, f in enumerate(p.get("failed_attempts") or []):
        if not isinstance(f, dict):
            err.add(f"failed_attempts[{i}]", "attendu un objet {what, why_failed}")
            continue
        _check_text(err, f"failed_attempts[{i}].what", f.get("what"), min_len=10, max_len=300)
        _check_text(err, f"failed_attempts[{i}].why_failed", f.get("why_failed"), min_len=15)

    for i, inv in enumerate(p.get("invariants") or []):
        if not isinstance(inv, dict):
            err.add(f"invariants[{i}]", "attendu un objet {claim, scope}")
            continue
        _check_text(err, f"invariants[{i}].claim", inv.get("claim"), min_len=10, max_len=300)
        _check_text(err, f"invariants[{i}].scope", inv.get("scope"), min_len=2)

    for i, ptr in enumerate(p.get("pointers") or []):
        if not isinstance(ptr, dict):
            err.add(f"pointers[{i}]", "attendu un objet {kind, ref, why}")
            continue
        if ptr.get("kind") not in POINTER_KINDS:
            err.add(f"pointers[{i}].kind", f"attendu l'un de {POINTER_KINDS}")
        _check_text(err, f"pointers[{i}].ref", ptr.get("ref"), min_len=1)
        _check_text(err, f"pointers[{i}].why", ptr.get("why"), min_len=10)

    for i, q in enumerate(p.get("open_questions") or []):
        if not isinstance(q, dict):
            err.add(f"open_questions[{i}]", "attendu un objet {question, blocking}")
            continue
        _check_text(err, f"open_questions[{i}].question", q.get("question"), min_len=15)

    _check_list_of_str(err, "next_steps", p.get("next_steps"), min_len=8)
    _check_list_of_str(err, "verified_by", p.get("verified_by"), min_len=3)

    for i, rid in enumerate(p.get("resolves") or []):
        if rid not in known_question_ids:
            err.add(f"resolves[{i}]", f"question {rid!r} introuvable. "
                                      "Lance handoff_read.py pour lister les ids ouverts.")
    for i, sid in enumerate(p.get("supersedes") or []):
        if sid not in known_ids:
            err.add(f"supersedes[{i}]", f"handoff {sid!r} introuvable.")

    if p.get("confidence") and p["confidence"] not in CONFIDENCES:
        err.add("confidence", f"attendu l'un de {CONFIDENCES}")

    # Regles inter-champs: c'est ici que le schema gagne sur le markdown.
    status = task.get("status")
    if status == "blocked":
        if not any(q.get("blocking") for q in (p.get("open_questions") or [])
                   if isinstance(q, dict)):
            err.add("open_questions", "status=blocked exige au moins une question "
                                      "avec blocking=true. Un blocage sans question "
                                      "formulee n'est pas transmissible.")
    if status == "done" and not (p.get("verified_by") or []):
        err.add("verified_by", "status=done exige au moins une commande de "
                               "verification reellement executee.")
    if status in ("partial", "abandoned") and not (p.get("next_steps") or []):
        err.add("next_steps", f"status={status} exige next_steps non vide.")

    return err


def make_id(payload, created_at):
    h = hashlib.sha256(
        (created_at + json.dumps(payload, sort_keys=True, ensure_ascii=False))
        .encode("utf-8")
    ).hexdigest()[:6]
    return h


def main():
    ap = argparse.ArgumentParser(description="Ecrit un handoff valide.")
    ap.add_argument("--file", help="payload JSON (defaut: stdin)")
    ap.add_argument("--template", action="store_true", help="affiche un squelette")
    ap.add_argument("--dry-run", action="store_true", help="valide sans ecrire")
    args = ap.parse_args()

    if args.template:
        print(json.dumps(TEMPLATE, indent=2, ensure_ascii=False))
        return 0

    raw = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON invalide: {e}", file=sys.stderr)
        return 1

    # Les listes vides du template sont tolerees, mais les entrees vides
    # laissees telles quelles sont rejetees plus bas: c'est voulu.
    payload = {k: v for k, v in payload.items() if v not in ([], {}, "", None)}

    existing, _ = load_all()
    known_ids = {r.get("id") for r in existing}
    known_qids = {q.get("id") for r in existing
                  for q in (r.get("open_questions") or []) if q.get("id")}

    errs = validate(payload, known_ids, known_qids)
    if errs:
        print(f"Handoff refuse ({len(errs)} probleme(s)):", file=sys.stderr)
        print("\n".join(errs), file=sys.stderr)
        print("\nCorrige et resoumets le payload complet.", file=sys.stderr)
        return 1

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    hid = make_id(payload, created_at)
    record = {"schema_version": "1.0", "id": hid, "created_at": created_at, **payload}

    for i, q in enumerate(record.get("open_questions") or []):
        q.setdefault("id", f"{hid}-q{i + 1}")
        q.setdefault("blocking", False)
    record.setdefault("confidence", "medium")

    if args.dry_run:
        print(f"OK (dry-run). id={hid}")
        return 0

    d = store_dir(create=True)
    fname = (f"{created_at.replace(':', '-')}--{slug(record['agent'], 20)}"
             f"--{slug(record['task']['title'])}--{hid}.json")
    path = d / fname
    # Un fichier par handoff, jamais de reecriture: deux agents concurrents
    # ne peuvent pas s'ecraser.
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    print(str(path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
