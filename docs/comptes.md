# Le double compte

Deux abonnements Claude sur la même machine : **perso** et **pro**. Ils ne se
parlent pas — sessions, mémoire, plugins, credentials sont séparés.

## Le mécanisme : une seule variable

Claude Code lit tout depuis `$CLAUDE_CONFIG_DIR`. Changer cette variable = changer
de compte, y compris le login.

```bash
export CLAUDE_CONFIG_DIR="$HOME/.claude-perso"   # défaut, posé dans ~/.bashrc
claude-pro                                        # bascule le shell courant
claude-perso                                      # revient
```

Les deux fonctions sont définies dans [`shell/bashrc-claude.sh`](../shell/bashrc-claude.sh) :
elles ne font qu'un `export`. Elles n'agissent que sur le shell courant — un
nouvel onglet repart sur perso.

## La bascule automatique : `claude-dev`

[`bin/claude-dev`](../bin/claude-dev) choisit le compte d'après le chemin du projet,
puis lance `claude` :

| cwd contient | compte |
|---|---|
| `/projects-pro/` | `~/.claude-pro` 🏢 |
| `/projects-perso/` | `~/.claude-perso` 🏠 |
| autre | refuse de démarrer |

C'est le garde-fou anti-« j'ai bossé le projet client sur le compte perso ».
Dans les devcontainers, le même choix se fait par `remoteEnv.CLAUDE_CONFIG_DIR`
dans le `devcontainer.json` du projet.

## Ce qui est partagé entre les deux comptes

Par symlink, source unique dans `~` :

```
~/.claude-perso/agents      → ~/agents
~/.claude-pro/agents        → ~/agents
~/.claude-{perso,pro}/skills/<nom> → ~/skills/<nom>
```

Plus, de fait : `~/hooks/context-watch.sh` (les deux `settings.json` le pointent),
`~/.gitconfig`, `~/.ssh`, le binaire `claude` lui-même.

## Ce qui diverge

| | perso | pro |
|---|---|---|
| `CLAUDE.md` | langue de commit = celle du repo | commits **en anglais** |
| plugins | ponytail, mattpocock, **marketing-skills** | ponytail, mattpocock |
| skills | + `afk-setup` | — |
| `remoteControlAtStartup` | `false` (explicite) | absent |
| `graphify` | v0.9.25 | v0.9.46 |

Les deux `CLAUDE.md` sont sinon identiques : pas d'auto-commit, pas de trailer
d'attribution, Conventional Commits, deux formats de message proposés avant de
commiter, communication ultra-concise. Ils `@`-importent `RTK.md`.

> Les versions de graphify ont divergé — le skill s'auto-met à jour au lancement,
> ça se recalera tout seul.
