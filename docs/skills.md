# Skills

Source unique : `~/skills/`. Chaque compte y accède par un symlink
`~/.claude-<compte>/skills/<nom> → ~/skills/<nom>`.

## Maison — versionnées ici

| Skill | Ce que ça fait | Déclencheur |
|---|---|---|
| [`audit-360`](../skills/audit-360/) | Audit read-only d'un codebase en 5 passes à périmètre exclusif (code, sécurité, produit, architecture, prod-readiness). Le livrable est un `AUDIT.md`, pas des fixes. Chaque finding doit être vérifié dans le code. | `/audit-360 full\|delta` |
| [`checkpoint`](../skills/checkpoint/SKILL.md) | Tient un fichier d'avancement dans le repo pour qu'une session neuve reparte sans démarrage à froid. Règle : **l'index est un index** — il pointe vers git/specs/tickets, il ne les recopie jamais. | `/checkpoint update\|resume\|init` |
| [`coach-craft`](../skills/coach-craft/SKILL.md) | Me colle le vocabulaire de design logiciel (deep module, seam, tracer bullet…) sur mon vrai code, au moment où le concept apparaît, jusqu'à ce que je l'emploie tout seul. Termes en anglais, explications en français. | auto (dès que je code/conçois/teste/revois) |
| [`evolve`](../skills/evolve/SKILL.md) | Boucle **instinct → skill** : relit les mémoires de tous les projets (perso + pro), repère ce qui revient, propose de le promouvoir en skill dans `~/skills/`. Validation explicite avant création. | `/evolve` |

### Design — archivées, pas installées

| Skill | Ce que ça fait |
|---|---|
| [`awwwards-motion-site`](../experimental/awwwards-motion-site/) | landing éditoriale : accent unique, typo grotesque XXL, scroll pinné, clip-path reveals, objet 3D. Next/HTML + Lenis + GSAP + R3F |
| [`cinematic-scroll-site`](../experimental/cinematic-scroll-site/) | le scroll scrube une caméra pré-rendue (technique des pages produit Apple). Livre `ScrollScrubScene.tsx`, `chapters.ts`, `extract-frames.sh` |

Écrites pour reproduire un effet précis repéré sur un site. Trop spécifiques pour
être always-on : on les copie dans le projet qui en a besoin.

```bash
cp -r <ce-repo>/experimental/awwwards-motion-site <projet>/.claude/skills/
```

Le reste du stack design (impeccable, emil, taste-skill, ui-ux-pro-max) vit par
projet — voir [design.md](design.md).

`audit-360` et `checkpoint` ont `disable-model-invocation: true` : elles ne se
déclenchent qu'à la main.

## Externe — pas versionnée ici

### graphify

N'importe quel dossier → graphe de connaissances navigable (god nodes, détection
de communautés, sortie HTML + JSON GraphRAG + `GRAPH_REPORT.md`, export Obsidian).

Vit dans `~/.claude-{perso,pro}/skills/graphify/` — **une copie par compte**, hors
symlink, parce que le skill s'auto-met à jour :

```bash
uv tool install --upgrade graphifyy    # ou pip install graphifyy
```

Le `SKILL.md` détecte l'interpréteur et s'installe seul au premier `/graphify`.
Amont : [safishamsi](https://github.com/sponsors/safishamsi). Cache partagé aux
conteneurs via `~/.graphify-cache`. Export Obsidian piloté par `$OBSIDIAN_VAULT_PATH`.

C'est la seule skill référencée nommément dans les deux `CLAUDE.md`.

### afk-setup

Vit dans le repo [afk.sh](https://github.com/Warshoow/afk.sh), exposée par double symlink :

```
~/skills/afk-setup                 → ~/afk/skills/afk-setup
~/.claude-perso/skills/afk-setup   → ~/skills/afk-setup
```

Écrit le `.afk.env` d'un projet : la porte de vérification qui définit ce que
« ce ticket est fini » veut dire ici. Une fois par repo, avant le premier `./afk.sh`.

## Skills fournies par les plugins

Voir [plugins.md](plugins.md) — mattpocock (méthode), marketing-skills (~50),
ponytail (paresse). Elles arrivent avec le plugin, rien à sauvegarder.

## Brouillons

[`experimental/handoff/`](../experimental/handoff/) — passation de contexte entre
agents (scripts Python + schéma JSON). Pas installée.
