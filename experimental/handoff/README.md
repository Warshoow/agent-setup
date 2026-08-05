# handoff

Passation de contexte entre agents Claude Code, via des handoffs JSON validés plutôt que des notes markdown.

> `SKILL.md` s'adresse à Claude. Ce README s'adresse à toi.

---

## Le problème

Faire écrire un `.md` par un agent pour qu'un autre le relise échoue de façon prévisible :

- **Rien ne force l'agent qui écrit à inclure ce qui compte.** Il résume ce qu'il a fait — la partie que `git diff` raconte déjà — et omet ce qui ne se re-dérive pas : pourquoi il a tranché comme ça, ce qu'il a essayé sans succès, quelle contrainte il a découverte.
- **L'agent qui lit doit interpréter de la prose.** Un « attention, le module de config est délicat » ne se transforme pas en comportement.
- **Deux agents concurrents s'écrasent.** Un fichier markdown n'a aucune sémantique de merge.
- **Les faits recopiés pourrissent.** Une signature de fonction citée dans un `.md` diverge silencieusement du code dès le commit suivant.

## L'approche

Déplacer la qualité du handoff depuis « est-ce que le modèle a bien rédigé » vers « est-ce que le payload passe la validation ». Le schéma est fermé, un script valide, et un handoff incomplet est refusé avec une erreur actionnable.

Trois propriétés structurelles :

| | |
|---|---|
| **Append-only** | un fichier par handoff, écriture unique, jamais de mutation → zéro conflit concurrent |
| **Schéma fermé** | champs inconnus rejetés → impossible de faire redevenir le handoff un `.md` déguisé |
| **Pointeurs > faits** | ce qu'un grep re-dérive se stocke en référence, pas en copie → ne pourrit pas |

---

## Installation

```bash
unzip handoff-skill.zip -d ~/.claude/skills/       # global
# ou
unzip handoff-skill.zip -d .claude/skills/         # par projet
```

Aucune dépendance : Python 3.8+, stdlib uniquement.

Vérification :

```bash
python3 ~/.claude/skills/handoff/scripts/handoff_write.py --template
```

---

## Utilisation

Le skill se déclenche seul en fin d'unité de travail et au démarrage d'une session sur un projet contenant `.handoff/`. Tu n'as normalement rien à taper. Les commandes ci-dessous servent à inspecter le store toi-même.

### Lire

```bash
python3 <skill>/scripts/handoff_read.py                # digest de l'état vivant
python3 <skill>/scripts/handoff_read.py --task auth    # filtre sur le titre
python3 <skill>/scripts/handoff_read.py --since 2026-08-01
python3 <skill>/scripts/handoff_read.py --agent builder
python3 <skill>/scripts/handoff_read.py --list         # index, une ligne par handoff
python3 <skill>/scripts/handoff_read.py --full a89316  # un handoff entier
python3 <skill>/scripts/handoff_read.py --json         # sortie machine
```

Le digest n'est pas une concaténation chronologique. Les handoffs supersédés et les questions résolues en sont sortis, et l'ordre suit le **coût de redécouverte** :

```
## Bloquant maintenant
## Pièges déjà rencontrés
## Invariants à ne pas casser
## Décisions actives
## Reprise
## Questions ouvertes non bloquantes
## Pointeurs
## État des tâches
```

### Écrire

```bash
python3 <skill>/scripts/handoff_write.py --template            # squelette à remplir
python3 <skill>/scripts/handoff_write.py --file payload.json
cat payload.json | python3 <skill>/scripts/handoff_write.py
python3 <skill>/scripts/handoff_write.py --file p.json --dry-run
```

Sortie : le chemin du fichier écrit (exit 0), ou la liste des problèmes (exit 1).

---

## Le schéma

Champs obligatoires : `agent`, `task.title`, `task.status`, `summary`.

| Champ | Ce qu'il capture |
|---|---|
| `decisions[]` | `what` + `why` (+ `alternatives_rejected`). Le champ qui rapporte le plus : sans le `why`, l'agent suivant reverra le choix sans savoir qu'il était délibéré. |
| `failed_attempts[]` | `what` + `why_failed` + `dont_retry`. L'information la plus chère à reproduire, et celle qu'on perd systématiquement. |
| `invariants[]` | `claim` + `scope`. Les contraintes qu'un agent naïf casserait sans le savoir. |
| `pointers[]` | `kind` (file/command/url/symbol) + `ref` + `why`. La règle centrale du protocole. |
| `open_questions[]` | `question` + `blocking`. Une question transmise vaut mieux qu'une décision arbitraire silencieuse. |
| `next_steps[]`, `verified_by[]`, `resolves[]`, `supersedes[]`, `confidence` | |

Schéma complet et annoté : `scripts/schema.json`.

### Règles de validation

Chacune correspond à un mode d'échec observé, pas à une préférence de style :

| Règle | Raison |
|---|---|
| `status=blocked` exige une question `blocking: true` | un blocage sans question formulée n'est pas transmissible |
| `status=done` exige `verified_by` non vide | « ça devrait marcher » n'est pas une vérification |
| `status=partial`/`abandoned` exige `next_steps` | sinon la reprise repart de zéro |
| `why` ≥ 25 caractères | une justification de trois mots ne survit pas à la relecture |
| valeurs creuses rejetées (`N/A`, `TBD`, `voir plus haut`…) | elles remplissent le champ sans porter d'information |
| blocs de code > 5 lignes rejetés | pointe vers le fichier, la copie divergera |
| champs inconnus rejetés | un champ libre annule tout l'intérêt du schéma |
| `resolves`/`supersedes` doivent référencer des ids existants | pas de résolution de question fantôme |

---

## Faire évoluer l'état

Rien n'est jamais muté. Pour faire évoluer l'état, on écrit un **nouveau** handoff qui référence l'ancien :

```json
{ "resolves": ["a89316-q1"], "supersedes": ["a89316"] }
```

- `resolves` → la question sort de l'état vivant
- `supersedes` → les décisions, invariants et points de reprise de l'ancien handoff sortent de l'état vivant

L'historique complet reste consultable via `--list` et `--full`.

### L'asymétrie invariant / échec

Le point de conception le moins évident, et celui qui a demandé une correction en cours de développement :

- Un **invariant** est une affirmation sur l'état courant → il **meurt** avec le handoff qui le portait.
- Un **échec** est un fait historique (« on a essayé X le jour J, ça a cassé sur Y ») → il **survit** à la supersession, marqué `[contexte depuis remplacé, <date>]`.

Sans cette asymétrie, un `dont_retry: true` disparaissait dès que la tâche associée était remplacée — c'est-à-dire exactement l'information qu'on cherchait à préserver.

---

## Le store

`.handoff/` à la racine du projet. Localisé en remontant depuis le répertoire courant jusqu'au premier `.git` — un agent lancé depuis un sous-répertoire n'écrit donc pas dans un store parallèle invisible des autres. `HANDOFF_DIR` force un chemin.

Nommage : `2026-08-05T13-41-43Z--builder--migration-parsing-config--a89316.json` — triable, greppable, lisible sans outil.

**Versionner ou non ?** Commite `.handoff/` si la passation doit franchir les machines ou les personnes. Ajoute-le à `.gitignore` si elle reste locale à un poste. Les deux sont des choix défendables ; le fichier étant append-only, le versionner ne produit pas de conflits de merge sur du contenu existant.

---

## Limites connues

**Le skill sous-déclenchera au début.** C'est la tendance générale des skills Claude Code : ils ne se déclenchent pas sur des tâches que le modèle pense pouvoir gérer seul. Si tu vois des sessions se terminer sans handoff, le levier est la `description` en frontmatter du `SKILL.md` — il faut la rendre plus insistante, pas modifier le corps.

**Le digest grossit linéairement.** Sur un projet à plusieurs centaines de handoffs, `handoff_read.py` sans filtre finit par être long. Utilise `--task` ou `--since`, ou fais du ménage en supersédant les handoffs clos. Si tu atteins cette échelle, c'est le signal pour passer à un vrai store indexé (graphe temporel type Graphiti/Zep) — le schéma reste transposable.

**Claude Code uniquement.** Le format `SKILL.md` est spécifique. Le schéma et les scripts sont eux portables : pour couvrir Codex ou Cursor, garde `scripts/` partagé et écris un `AGENTS.md` équivalent pointant sur les mêmes commandes. N'essaie pas d'écrire un fichier d'instructions universel — les modèles sont post-entraînés sur leur harness et ne pondèrent pas la mémoire de la même façon.

**Pas de garantie sur le contenu.** La validation garantit qu'un champ est rempli et non creux, pas qu'il est *juste*. Un `why` de 200 caractères peut être faux. C'est un plancher, pas un plafond.

---

## Structure

```
handoff/
├── SKILL.md                    # instructions pour Claude
├── README.md                   # ce fichier
└── scripts/
    ├── schema.json             # le contrat, annoté
    ├── handoff_write.py        # validation + écriture
    ├── handoff_read.py         # agrégation + digest
    └── _common.py              # découverte du store, chargement
```
