#!/usr/bin/env python3
"""Ce que coûtent vraiment les sessions Claude Code, lu dans les transcripts.

Source : ~/.claude/projects/*/*.jsonl. Chaque message assistant y porte son bloc
`usage` réel (input, cache_creation, cache_read, output) — c'est la facture, pas
une estimation. Rien à installer, rien à surveiller : tout est déjà sur le disque.

    ./bin/audit-tokens.py [jours]      # défaut : 30

Sert à répondre à trois questions, dans cet ordre :
  1. d'où vient le contexte (quel outil, quelle commande le remplit)
  2. où est concentrée la dépense (quelles sessions, quels projets)
  3. à quelle taille de contexte l'argent part réellement

Les chiffres commentés dans docs/couts.md viennent de ce script.
"""
import collections, datetime, glob, json, os, re, sys

DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 30
CUT = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=DAYS)
ROOT = os.path.expanduser("~/.claude/projects/*/*.jsonl")
INTERACTIF = ("claude-vscode", "cli", "claude-desktop")


def entree(u):
    """Tokens d'entrée facturés pour un message."""
    return ((u.get("input_tokens") or 0)
            + (u.get("cache_read_input_tokens") or 0)
            + (u.get("cache_creation_input_tokens") or 0))


def taille(c):
    if isinstance(c, str):
        return len(c)
    if isinstance(c, list):
        return sum(len(b.get("text", "")) if isinstance(b, dict) else 0 for b in c)
    return 0


def nom_commande(s):
    s = re.sub(r"^(rtk|sudo|time|env)\s+", "", (s or "").strip())
    m = re.match(r"[\w./-]+", s)
    return m.group(0).split("/")[-1] if m else "?"


def pct(part, tout):
    return 100 * part / tout if tout else 0.0


# ---------------------------------------------------------------- collecte
cat = collections.Counter()        # contexte par categorie de contenu
outil = collections.Counter()      # sortie par outil
appels = collections.Counter()
cmd_vol = collections.Counter()    # sortie Bash par commande
cmd_n = collections.Counter()
gros = []                          # sorties Bash unitaires enormes
usage = collections.Counter()
par_effort = collections.Counter()
bandes = collections.Counter()     # entree interactive par taille de contexte
bandes_n = collections.Counter()
sessions = []                      # (entree totale, tours, pic, entrypoint, projet)

for path in glob.glob(ROOT):
    noms, cmds = {}, {}
    total = tours = pic = 0
    ep = "?"
    local = collections.Counter()
    ctx = []
    for ligne in open(path, errors="replace"):
        try:
            d = json.loads(ligne)
        except Exception:
            continue
        ts = d.get("timestamp")
        if ts:
            try:
                if datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")) < CUT:
                    continue
            except Exception:
                pass
        if d.get("entrypoint"):
            ep = d["entrypoint"]
        msg = d.get("message") or {}

        contenu = msg.get("content")
        qui = "texte utilisateur" if d.get("type") == "user" else "texte assistant"
        if isinstance(contenu, str):
            local[qui] += len(contenu)
        elif isinstance(contenu, list):
            for b in contenu:
                if not isinstance(b, dict):
                    continue
                t = b.get("type")
                if t == "text":
                    local[qui] += len(b.get("text", ""))
                elif t == "thinking":
                    local["raisonnement"] += len(b.get("thinking", ""))
                elif t == "tool_use":
                    noms[b.get("id")] = b.get("name", "?")
                    entree_outil = b.get("input") or {}
                    if b.get("name") == "Bash":
                        cmds[b.get("id")] = entree_outil.get("command", "")
                    local["parametres d appels d outils"] += len(
                        json.dumps(entree_outil, ensure_ascii=False))
                elif t == "tool_result":
                    n = noms.get(b.get("tool_use_id"), "?")
                    taille_res = taille(b.get("content"))
                    outil[n] += taille_res
                    appels[n] += 1
                    local[f"sortie {n}" if n in ("Bash", "Read", "Agent")
                          else "sortie autres outils"] += taille_res
                    if n == "Bash":
                        c = cmds.get(b.get("tool_use_id"), "")
                        cmd_vol[nom_commande(c)] += taille_res
                        cmd_n[nom_commande(c)] += 1
                        if taille_res > 40000:
                            gros.append((taille_res, c[:80].replace("\n", " ")))

        u = msg.get("usage")
        if u and d.get("type") == "assistant" and not d.get("isSidechain"):
            tours += 1
            e = entree(u)
            total += e
            pic = max(pic, e)
            ctx.append(e)
            for k in ("input_tokens", "cache_creation_input_tokens",
                      "cache_read_input_tokens", "output_tokens"):
                usage[k] += u.get(k, 0) or 0
            par_effort[d.get("effort") or "?"] += 1

    if not tours:
        continue
    cat.update(local)
    sessions.append((total, tours, pic, ep, os.path.basename(os.path.dirname(path))))
    if ep in INTERACTIF:
        for e in ctx:
            b = ("<50k" if e < 50e3 else "50-100k" if e < 100e3 else
                 "100-150k" if e < 150e3 else "150-200k" if e < 200e3 else
                 "200-300k" if e < 300e3 else ">300k")
            bandes[b] += e
            bandes_n[b] += 1

if not sessions:
    sys.exit(f"aucune session dans les {DAYS} derniers jours sous {ROOT}")

# ---------------------------------------------------------------- rapport
tot_in = sum(s[0] for s in sessions)
tot_ctx = sum(cat.values())
tot_outil = sum(outil.values())
print(f"=== {DAYS} derniers jours — {len(sessions)} sessions ===\n")

print("TOKENS FACTURES")
for k in ("input_tokens", "cache_creation_input_tokens",
          "cache_read_input_tokens", "output_tokens"):
    print(f"  {k:<30}{usage[k]/1e6:>10.1f} M")
print(f"  {'part cache_read dans l entree':<30}"
      f"{pct(usage['cache_read_input_tokens'], tot_in):>9.1f} %")

print("\nD OU VIENT LE CONTEXTE")
for k, v in cat.most_common():
    print(f"  {k:<32}{v/1e6:>8.1f} Mchars{pct(v, tot_ctx):>7.1f} %")
print(f"  {'TOTAL':<32}{tot_ctx/1e6:>8.1f} Mchars   (~{tot_ctx/4/1e6:.0f} M tokens)")

print("\nSORTIE DES OUTILS")
for n, v in outil.most_common(8):
    print(f"  {n:<28}{pct(v, tot_outil):>6.1f} %{appels[n]:>8} appels"
          f"{v//max(appels[n],1):>9} chars/appel")
print(f"  -> portee de rtk (Bash seul) : {pct(outil.get('Bash',0), tot_outil):.1f} %")

print("\nSORTIE BASH PAR COMMANDE")
tb = sum(cmd_vol.values())
for k, v in cmd_vol.most_common(12):
    print(f"  {k:<16}{pct(v, tb):>6.1f} %{cmd_n[k]:>8} appels{v//max(cmd_n[k],1):>9} chars/appel")
print(f"  sorties unitaires > 40k chars : {len(gros)}"
      + (f" (max {max(g[0] for g in gros)//1000}k)" if gros else "  <- rien a compresser"))

print("\nCONCENTRATION")
sessions.sort(reverse=True)
for n in (1, 5, 10, 20, 50):
    if n <= len(sessions):
        print(f"  top {n:>3} sessions{pct(sum(s[0] for s in sessions[:n]), tot_in):>7.1f} % de l entree")
proj = collections.Counter()
for total, _, _, _, p in sessions:
    proj[p] += total
print("  par projet :")
for p, v in proj.most_common(5):
    print(f"    {pct(v, tot_in):>5.1f} %  {p[:56]}")

print("\nPAR TYPE DE SESSION")
par_ep = collections.defaultdict(list)
for total, tours, pic, ep, _ in sessions:
    par_ep[ep].append((total, pic))
for ep, v in sorted(par_ep.items(), key=lambda x: -sum(t for t, _ in x[1])):
    pics = sorted(p for _, p in v)
    print(f"  {ep:<18}{pct(sum(t for t,_ in v), tot_in):>6.1f} %{len(v):>5} sessions"
          f"   pic median {pics[len(pics)//2]/1000:>5.0f}k   max {pics[-1]/1000:>5.0f}k")

print("\nEFFORT (messages assistant)")
for e, n in par_effort.most_common():
    print(f"  {e:<10}{n:>8}")

if bandes:
    tb2 = sum(bandes.values())
    print("\nSESSIONS INTERACTIVES — entree par taille de contexte AU MOMENT du tour")
    haut = 0
    for b in ("<50k", "50-100k", "100-150k", "150-200k", "200-300k", ">300k"):
        print(f"  {b:<10}{pct(bandes[b], tb2):>6.1f} %{bandes_n[b]:>8} tours")
        if b in ("150-200k", "200-300k", ">300k"):
            haut += bandes[b]
    print(f"  -> {pct(haut, tb2):.1f} % de l entree interactive part a >150k de contexte")

    inter = sorted(s[0] for s in sessions if s[3] in INTERACTIF)
    n = len(inter)
    print("\nENTREE CUMULEE PAR SESSION INTERACTIVE  (seuil de CTX_BUDGET)")
    for q, lab in ((.5, "median"), (.75, "p75"), (.9, "p90"), (.95, "p95"), (1, "max")):
        print(f"    {lab:<7}{inter[min(int(n*q), n-1)]/1e6:>8.0f} M")
    tot_i = sum(inter)
    for seuil in (20, 30, 50, 80):
        au_dela = [t for t in inter if t > seuil * 1e6]
        exces = sum(t - seuil * 1e6 for t in au_dela)
        print(f"    budget {seuil:>3} M : {len(au_dela):>3} sessions le depassent "
              f"({pct(len(au_dela), n):.0f} %), {pct(exces, tot_i):>4.1f} % de l entree est au-dela")
