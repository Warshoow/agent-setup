# agent-setup

Trace de mon setup **Claude Code** sous WSL : une config unique, des agents et
des skills maison, des hooks, des plugins, et l'outillage autour (rtk, graphify, afk).

Ce repo est une **archive documentée**, pas un installeur. Il sert à savoir ce
que j'avais et pourquoi, si la machine part.

Noms de projets et chemins personnels retirés — les fichiers de config sont
donc à recoller à la main, pas à copier tels quels.

---

## La carte

```
~/
├── .claude/                config Claude Code complète
│     │                          (sessions, mémoire, plugins, creds)
│     ├── CLAUDE.md               instructions globales
│     ├── RTK.md                  @-importé par CLAUDE.md
│     ├── settings.json           modèle, hooks, statusline, plugins
│     ├── agents  ──symlink──►  ~/agents
│     ├── skills/<nom> ─symlink►  ~/skills/<nom>
│     └── skills/graphify         (installé par le skill lui-même)
│
├── agents/                 SOURCE UNIQUE des 8 subagents user-level
├── skills/                 SOURCE UNIQUE des skills maison
├── hooks/                  context-watch.sh (Stop) + big-read-gate.py (PreToolUse)
├── afk/                    repo séparé → github.com/Warshoow/afk.sh
├── projects-perso/         projets personnels
└── projects-pro/           projets professionnels
```

Le principe : **une seule copie de chaque asset dans `~`**, exposée à la config
par symlink. On édite `~/agents/planner.md`, Claude Code le voit.
C'est aussi ce qui rend les devcontainers possibles (voir [docs/devcontainers.md](docs/devcontainers.md)).

## Ce qu'il y a dans ce repo

| Chemin | Quoi |
|---|---|
| [claude/](claude/) | `CLAUDE.md`, `RTK.md`, `settings.json` |
| [agents/](agents/) | les 8 subagents + leur politique de modèles |
| [skills/](skills/) | `audit-360`, `checkpoint`, `coach-craft`, `evolve` + deux skills design maison |
| [hooks/](hooks/) | `context-watch.sh` (contexte + budget cumulé), `big-read-gate.py` (bloque les lectures pleines) |
| [bin/](bin/) | `import-project.sh`, `audit-tokens.py` (ce que coûtent vraiment les sessions) |
| [shell/](shell/) | l'extrait de `~/.bashrc` : PATH, seuil de contexte, ssh-agent |
| [experimental/](experimental/) | brouillons (handoff multi-agents) |

## La doc

- **[docs/comptes.md](docs/comptes.md)** — la config unique : ce qu'elle contient, ce qui vient de `~` par symlink, et l'historique du double compte.
- **[docs/skills.md](docs/skills.md)** — les skills maison, une ligne chacune, + les externes (graphify).
- **[agents/README.md](agents/README.md)** — les subagents et quel modèle chacun tourne.
- **[docs/design.md](docs/design.md)** — le stack design : impeccable, emil, taste-skill, ui-ux-pro-max — **et lesquels ne pas mélanger**. Porte aussi l'index des repos et outils design évalués, et le mode d'emploi (expérimental).
- **[docs/plugins.md](docs/plugins.md)** — plugins installés, marketplaces, versions.
- **[docs/hooks.md](docs/hooks.md)** — les trois hooks, **et pourquoi `context-watch.sh` ne marchait pas**.
- **[docs/couts.md](docs/couts.md)** — ce que coûtent les sessions, mesuré dans les transcripts : 97 % de l'entrée est du renvoi de contexte, 20 sessions font la moitié de la facture, **et pourquoi les 60–90 % de rtk ne se vérifient pas ici**.
- **[docs/outils.md](docs/outils.md)** — rtk, graphify, afk.
- **[docs/devcontainers.md](docs/devcontainers.md)** — le pattern de mounts pour que les symlinks survivent dans un conteneur.

## Ce qui n'est PAS ici

| Quoi | Pourquoi |
|---|---|
| `.credentials.json`, `.claude.json` | tokens OAuth, `userID`, `machineID`. Jamais dans un repo. |
| `~/afk/` | a son propre repo : **[github.com/Warshoow/afk.sh](https://github.com/Warshoow/afk.sh)** |
| `skills/graphify/` | skill tiers, s'auto-installe (`uv tool install graphifyy`) |
| `plugins/cache/` | réinstallé depuis les marketplaces déclarées dans `settings.json` |
| `projects/`, `sessions/`, `history.jsonl` | historique de travail, pas de la config |
| les noms de projets | anonymisés dans les fichiers de config publiés |

## Remonter la machine, en gros

1. `claude login` (la config atterrit dans `~/.claude`).
2. Les plugins reviennent seuls au premier lancement (`extraKnownMarketplaces` + `enabledPlugins`).
3. `rtk`, `graphify` (`uv tool install graphifyy`), `afk` (repo séparé) à réinstaller.
4. Recoller les symlinks `~/.claude/{agents,skills}` → `~/{agents,skills}`.
5. Sourcer [`shell/bashrc-claude.sh`](shell/bashrc-claude.sh) depuis `~/.bashrc`.

## Mémoire persistante

Chaque projet a sa mémoire sous `~/.claude/projects/<slug>/memory/`
(`MEMORY.md` en index + un fichier par fait). **Non versionnée ici** : c'est du
contenu de travail, pas de la config.

Le skill [`evolve`](skills/evolve/SKILL.md) est la boucle qui relit ces mémoires
et propose de promouvoir en skill ce qui se répète.
