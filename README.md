# agent-setup

Trace de mon setup **Claude Code** sous WSL : deux comptes, des agents et des
skills maison, des hooks, des plugins, et l'outillage autour (rtk, graphify, afk).

Ce repo est une **archive documentée**, pas un installeur. Il sert à savoir ce
que j'avais et pourquoi, si la machine part.

Noms de projets et chemins personnels retirés — les fichiers de config sont
donc à recoller à la main, pas à copier tels quels.

---

## La carte

```
~/
├── .claude-perso/          compte perso  ─┐  configs Claude Code complètes
├── .claude-pro/            compte pro    ─┘  (sessions, mémoire, plugins, creds)
│     ├── CLAUDE.md               instructions globales du compte
│     ├── RTK.md                  @-importé par CLAUDE.md
│     ├── settings.json           modèle, hooks, statusline, plugins
│     ├── agents  ──symlink──►  ~/agents
│     ├── skills/<nom> ─symlink►  ~/skills/<nom>
│     └── skills/graphify         (installé par le skill lui-même)
│
├── agents/                 SOURCE UNIQUE des 8 subagents user-level
├── skills/                 SOURCE UNIQUE des skills maison
├── hooks/context-watch.sh  hook Stop : alerte quand le contexte se remplit
├── bin/claude-dev          lance claude en choisissant le compte d'après le cwd
├── afk/                    repo séparé → github.com/Warshoow/afk.sh
├── projects-perso/         projets → compte perso
└── projects-pro/           projets → compte pro
```

Le principe : **une seule copie de chaque asset dans `~`**, exposée aux deux
comptes par symlink. On édite `~/agents/planner.md`, les deux comptes le voient.
C'est aussi ce qui rend les devcontainers possibles (voir [docs/devcontainers.md](docs/devcontainers.md)).

## Ce qu'il y a dans ce repo

| Chemin | Quoi |
|---|---|
| [claude/](claude/) | `CLAUDE.md`, `RTK.md`, `settings.json` des deux comptes |
| [agents/](agents/) | les 8 subagents + leur politique de modèles |
| [skills/](skills/) | `audit-360`, `checkpoint`, `coach-craft`, `evolve` + deux skills design maison |
| [hooks/](hooks/) | `context-watch.sh` |
| [bin/](bin/) | `claude-dev`, `import-project.sh` |
| [shell/](shell/) | l'extrait de `~/.bashrc` : switch de compte, PATH, ssh-agent |
| [experimental/](experimental/) | brouillons (handoff multi-agents) |

## La doc

- **[docs/comptes.md](docs/comptes.md)** — le double compte : comment ça bascule, ce qui est partagé, ce qui ne l'est pas.
- **[docs/skills.md](docs/skills.md)** — les skills maison, une ligne chacune, + les externes (graphify).
- **[agents/README.md](agents/README.md)** — les subagents et quel modèle chacun tourne.
- **[docs/design.md](docs/design.md)** — le stack design : impeccable, emil, taste-skill, ui-ux-pro-max — **et lesquels ne pas mélanger**. Porte aussi l'index des repos et outils design évalués, et le mode d'emploi (expérimental).
- **[docs/plugins.md](docs/plugins.md)** — plugins installés, marketplaces, versions.
- **[docs/hooks.md](docs/hooks.md)** — les deux hooks, **et pourquoi `context-watch.sh` ne marchait pas**.
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

1. `claude login` sur chaque compte, avec `CLAUDE_CONFIG_DIR` pointé sur le bon dossier.
2. Les plugins reviennent seuls au premier lancement (`extraKnownMarketplaces` + `enabledPlugins`).
3. `rtk`, `graphify` (`uv tool install graphifyy`), `afk` (repo séparé) à réinstaller.
4. Recoller les symlinks `~/.claude-*/{agents,skills}` → `~/{agents,skills}`.
5. Sourcer [`shell/bashrc-claude.sh`](shell/bashrc-claude.sh) depuis `~/.bashrc`.

## Mémoire persistante

Chaque projet a sa mémoire sous `~/.claude-{perso,pro}/projects/<slug>/memory/`
(`MEMORY.md` en index + un fichier par fait). **Non versionnée ici** : c'est du
contenu de travail, pas de la config.

Le skill [`evolve`](skills/evolve/SKILL.md) est la boucle qui relit ces mémoires
et propose de promouvoir en skill ce qui se répète.
