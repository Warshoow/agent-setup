#!/usr/bin/env python3
"""Restitue l'etat vivant des handoffs. Stdlib uniquement.

Usage:
    handoff_read.py                      # digest de l'etat vivant
    handoff_read.py --task auth          # filtre par titre
    handoff_read.py --since 2026-08-01
    handoff_read.py --full <id>          # un handoff entier
    handoff_read.py --list               # index une ligne par handoff
    handoff_read.py --json               # sortie machine

Le digest n'est pas une concatenation: les handoffs superseded sortent, les
questions resolues sortent, et l'ordre suit ce qui coute le plus cher a
redecouvrir (blocages, pieges, invariants) plutot que la chronologie.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import load_all, store_dir  # noqa: E402


def compute_state(records):
    superseded = {sid for r in records for sid in (r.get("supersedes") or [])}
    resolved = {qid for r in records for qid in (r.get("resolves") or [])}
    live = [r for r in records if r.get("id") not in superseded]

    open_q, invariants, traps, decisions, next_steps = [], [], [], [], []

    # Asymetrie voulue: un invariant est une affirmation sur l'etat courant,
    # il meurt avec le handoff qui le portait. Un echec est un fait historique
    # ("on a essaye X le jour J, ca a casse sur Y") — il reste vrai meme quand
    # la tache est superseded, et c'est justement l'information la plus chere
    # a redecouvrir. On la garde toujours, en signalant sa provenance.
    for r in records:
        for f in r.get("failed_attempts") or []:
            traps.append((r, f, r.get("id") in superseded))

    for r in live:
        for q in r.get("open_questions") or []:
            if q.get("id") not in resolved:
                open_q.append((r, q))
        for inv in r.get("invariants") or []:
            invariants.append((r, inv))
        for d in r.get("decisions") or []:
            decisions.append((r, d))
        if r.get("task", {}).get("status") in ("partial", "blocked"):
            for s in r.get("next_steps") or []:
                next_steps.append((r, s))
    return {
        "live": live, "superseded": superseded, "resolved": resolved,
        "open_questions": open_q, "invariants": invariants, "traps": traps,
        "decisions": decisions, "next_steps": next_steps,
    }


def render(st, records):
    out = []
    a = out.append
    if not st["live"]:
        return "Aucun handoff. Le store est vide ou tout est superseded."

    blocking = [(r, q) for r, q in st["open_questions"] if q.get("blocking")]
    if blocking:
        a("## Bloquant maintenant")
        for r, q in blocking:
            a(f"- [{q['id']}] {q['question']}  ({r['agent']}, {r['created_at'][:10]})")
        a("")

    if st["traps"]:
        a("## Pieges deja rencontres")
        for r, f, is_old in st["traps"]:
            tag = " — NE PAS RETENTER" if f.get("dont_retry") else ""
            age = f" [contexte depuis remplace, {r['created_at'][:10]}]" if is_old else ""
            a(f"- {f['what']} -> {f['why_failed']}{tag}{age}")
        a("")

    if st["invariants"]:
        a("## Invariants a ne pas casser")
        for r, inv in st["invariants"]:
            a(f"- ({inv['scope']}) {inv['claim']}")
        a("")

    if st["decisions"]:
        a("## Decisions actives")
        for r, d in st["decisions"]:
            a(f"- {d['what']}")
            a(f"  parce que: {d['why']}")
            if d.get("alternatives_rejected"):
                a(f"  ecarte: {', '.join(d['alternatives_rejected'])}")
        a("")

    if st["next_steps"]:
        a("## Reprise")
        for r, s in st["next_steps"]:
            a(f"- {s}  ({r['task']['title']})")
        a("")

    others = [(r, q) for r, q in st["open_questions"] if not q.get("blocking")]
    if others:
        a("## Questions ouvertes non bloquantes")
        for r, q in others:
            a(f"- [{q['id']}] {q['question']}")
        a("")

    ptrs = [(r, p) for r in st["live"] for p in (r.get("pointers") or [])]
    if ptrs:
        a("## Pointeurs")
        for r, p in ptrs:
            a(f"- ({p['kind']}) {p['ref']} — {p['why']}")
        a("")

    a("## Etat des taches")
    for r in st["live"]:
        conf = r.get("confidence", "medium")
        a(f"- [{r['id']}] {r['task']['title']} — {r['task']['status']} "
          f"(confiance {conf}, {r['agent']}, {r['created_at'][:10]})")
        a(f"  {r['summary']}")

    n_sup = len(st["superseded"])
    if n_sup:
        a("")
        a(f"({n_sup} handoff(s) superseded exclu(s). --list pour tout voir.)")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Lit l'etat vivant des handoffs.")
    ap.add_argument("--task", help="filtre sur le titre de tache (sous-chaine)")
    ap.add_argument("--since", help="date ISO minimale, ex 2026-08-01")
    ap.add_argument("--agent", help="filtre par agent")
    ap.add_argument("--full", help="affiche un handoff complet par id")
    ap.add_argument("--list", action="store_true", help="index compact")
    ap.add_argument("--json", action="store_true", help="sortie machine")
    args = ap.parse_args()

    records, broken = load_all()
    for name, e in broken:
        print(f"[avertissement] {name} illisible et ignore: {e}", file=sys.stderr)

    if not records:
        print(f"Aucun handoff dans {store_dir()}.")
        return 0

    if args.full:
        for r in records:
            if r.get("id") == args.full:
                r.pop("_path", None)
                print(json.dumps(r, indent=2, ensure_ascii=False))
                return 0
        print(f"id {args.full!r} introuvable.", file=sys.stderr)
        return 1

    sel = records
    if args.task:
        sel = [r for r in sel if args.task.lower() in r.get("task", {}).get("title", "").lower()]
    if args.since:
        sel = [r for r in sel if r.get("created_at", "") >= args.since]
    if args.agent:
        sel = [r for r in sel if r.get("agent") == args.agent]

    if args.list:
        for r in sel:
            print(f"{r['id']}  {r['created_at'][:16]}  {r['agent']:<12} "
                  f"{r['task']['status']:<9} {r['task']['title']}")
        return 0

    st = compute_state(sel)
    if args.json:
        for r in st["live"]:
            r.pop("_path", None)
        print(json.dumps({
            "live": st["live"],
            "open_question_ids": [q["id"] for _, q in st["open_questions"]],
            "superseded_ids": sorted(st["superseded"]),
        }, indent=2, ensure_ascii=False))
        return 0

    print(render(st, sel))
    return 0


if __name__ == "__main__":
    sys.exit(main())
