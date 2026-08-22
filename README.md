# agent-setup

Sauvegarde et restauration de mon setup **Claude Code** sous WSL : deux comptes,
des agents et des skills maison, un hook de contexte, des plugins, et l'outillage
autour (rtk, graphify, afk).

But : si le PC crame, `git clone` + `./install.sh` + deux `/login` et je suis debout.

```bash
git clone git@github.com:Warshoow/agent-setup.git ~/agent-setup
cd ~/agent-setup && ./install.sh -n   # le plan
./install.sh                          # pour de vrai
```

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
│     └── skills/graphify         (installé par le skill lui-même, pas versionné ici)
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

| Chemin | Quoi | Destination |
|---|---|---|
| [claude/](claude/) | `CLAUDE.md`, `RTK.md`, `settings.json` des deux comptes | `~/.claude-{perso,pro}/` |
| [agents/](agents/) | les 8 subagents + leur politique de modèles | `~/agents/` |
| [skills/](skills/) | `audit-360`, `checkpoint`, `coach-craft`, `evolve` | `~/skills/` |
| [hooks/](hooks/) | `context-watch.sh` | `~/hooks/` |
| [bin/](bin/) | `claude-dev`, `import-project.sh` | `~/bin/`, `~/.local/bin/` |
| [shell/](shell/) | l'extrait de `~/.bashrc` (switch de compte, PATH, ssh-agent) | sourcé par `~/.bashrc` |
| [install.sh](install.sh) | la restauration, idempotente | — |
| [experimental/](experimental/) | brouillons de skills (handoff multi-agents) | — |

## La doc

- **[docs/comptes.md](docs/comptes.md)** — le double compte : comment ça bascule, ce qui est partagé, ce qui ne l'est pas.
- **[docs/skills.md](docs/skills.md)** — les skills maison, une ligne chacune, + les externes (graphify).
- **[agents/README.md](agents/README.md)** — les subagents et quel modèle chacun tourne.
- **[docs/plugins.md](docs/plugins.md)** — plugins installés, marketplaces, versions.
- **[docs/hooks.md](docs/hooks.md)** — les deux hooks, **et pourquoi `context-watch.sh` ne marchait pas**.
- **[docs/outils.md](docs/outils.md)** — rtk, graphify, afk, claude-kit.
- **[docs/devcontainers.md](docs/devcontainers.md)** — le pattern de mounts pour que les symlinks survivent dans un conteneur.

## Ce qui n'est PAS ici (volontairement)

| Quoi | Pourquoi |
|---|---|
| `.credentials.json`, `.claude.json` | tokens OAuth, `userID`, `machineID`. Jamais dans un repo. |
| `~/afk/` | a son propre repo : **[github.com/Warshoow/afk.sh](https://github.com/Warshoow/afk.sh)** |
| `skills/graphify/` | skill tiers, s'auto-installe (`uv tool install graphifyy`) |
| `plugins/cache/` | réinstallé tout seul depuis les marketplaces |
| `projects/`, `sessions/`, `history.jsonl` | historique de travail, pas de la config |
| `~/.claude-assets/` | bibliothèque de [claude-kit](https://github.com/Warshoow/claude-kit), gérée par l'app |

## Mémoire persistante

Chaque projet a sa mémoire sous `~/.claude-{perso,pro}/projects/<slug>/memory/`
(`MEMORY.md` en index + un fichier par fait). **Non versionnée ici** : c'est du
contenu de travail, pas de la config — et ça bouge à chaque session. Si tu veux
la sauver, c'est un `rsync` à part, pas ce repo.

Le skill [`evolve`](skills/evolve/SKILL.md) est la boucle qui relit ces mémoires
et propose de promouvoir en skill ce qui se répète.
