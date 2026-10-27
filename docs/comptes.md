# La config Claude

Une seule config, dans `~/.claude`. Claude Code la lit par défaut : plus de
variable à poser, plus de bascule à faire.

```
~/.claude/
├── CLAUDE.md          instructions globales
├── RTK.md             @-importé par CLAUDE.md
├── settings.json      modèle, hooks, statusline, plugins
├── .credentials.json  OAuth Claude + OAuth des serveurs MCP
├── .claude.json       identité du compte, état par projet
├── CLAUDE.md, RTK.md, statusline.sh, rules, laya  ─symlink─►  ~/.agents/…
├── agents  ──symlink──►  ~/.agents/agents
├── skills/<nom> ─symlink►  ~/.agents/skills/<nom>
├── projects/<slug>/   sessions + mémoire, un dossier par cwd
└── plugins/           marketplaces + cache
```

## Ce qui vient de `~/.agents`, par symlink

```
~/.claude/{CLAUDE.md,RTK.md,statusline.sh,rules}  → ~/.agents/claude/…
~/.claude/laya                                    → ~/.agents/laya
~/.claude/agents                                  → ~/.agents/agents
~/.claude/skills/<nom>                            → ~/.agents/skills/<nom>
```

`~/.agents` est un repo git privé : une seule copie de chaque asset, éditée à un
seul endroit, poussée sur GitHub, réinstallée par `~/.agents/install.sh`. Les hooks
sont appelés à `$HOME/.agents/hooks/…` depuis `settings.json`.

`settings.json` reste un vrai fichier dans `~/.claude` (Claude Code, Orca et Coucou
écrivent dedans) ; le repo en garde une copie sans les hooks propres à la machine.

## `CLAUDE_CONFIG_DIR`

Posée en haut de `~/.bashrc`, avant la garde « shell interactif », pour que les
shells de login non interactifs l'aient aussi (sans elle, Claude Code lit
`~/.claude.json` au lieu de `~/.claude/.claude.json`). Elle reste **obligatoire dans les devcontainers** : le `$HOME` du
conteneur (`/home/node`) n'est pas celui où la config de l'hôte est montée. Voir
[devcontainers.md](devcontainers.md).

## Historique : le double compte

Jusqu'à septembre 2026, deux abonnements Claude cohabitaient sur la machine,
dans `~/.claude-perso` et `~/.claude-pro`. `CLAUDE_CONFIG_DIR` basculait de l'un
à l'autre — posée dans `~/.bashrc` (défaut perso), deux fonctions shell
`claude-pro` / `claude-perso` pour le shell courant, un script `bin/claude-dev`
qui choisissait d'après le chemin du projet, et `remoteEnv.CLAUDE_CONFIG_DIR`
dans chaque `devcontainer.json`.

Ce que ça coûtait, et qui a motivé l'unification :

- deux jeux de plugins, de skills et de `CLAUDE.md` à tenir en phase ;
- la mémoire d'un même projet éclatée sur les deux configs selon le shell
  utilisé ce jour-là ;
- les chemins absolus des plugins (`installed_plugins.json`,
  `known_marketplaces.json`) écrasés par les chemins d'un conteneur, cassant
  l'installation côté hôte.

L'abonnement perso a été abandonné ; le compte pro a gardé son identité. Tout le
reste — projets, sessions, mémoires, historique, plugins, jetons MCP — a été
fusionné dans `~/.claude`.
