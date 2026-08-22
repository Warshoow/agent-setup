# Outillage autour de Claude

## rtk — Rust Token Killer

Proxy CLI qui filtre et résume la sortie des commandes avant qu'elle n'atteigne
le contexte. 60–90 % d'économie sur les opérations de dev.

- Binaire : `~/.local/bin/rtk` (v0.43.0)
- Branché par le hook `PreToolUse` sur `Bash` → `rtk hook claude` : la réécriture
  est transparente, l'agent n'a rien à faire.
- Documenté à l'agent par `claude/RTK.md`, `@`-importé depuis les deux `CLAUDE.md`.

Proxies : `ls tree read git gh glab aws psql pnpm docker dotnet find diff log json deps env err test smart`.

Méta-commandes (à appeler directement, elles ne passent pas par le hook) :

```bash
rtk gain              # analytics des économies
rtk gain --history    # historique par commande
rtk discover          # repère les occasions ratées dans l'historique Claude Code
rtk proxy <cmd>       # exécution brute, sans filtre (debug)
```

⚠️ Collision de nom : si `rtk gain` échoue, c'est le mauvais `rtk`
(reachingforthejack/rtk, « Rust Type Kit ») qui est dans le PATH.

## afk.sh — repo séparé

**→ [github.com/Warshoow/afk.sh](https://github.com/Warshoow/afk.sh)**

Trois scripts bash, zéro dépendance, aucun LLM dans l'orchestrateur. Enchaîne des
sessions `claude -p "/implement le ticket #N"` sur les tickets `ready-for-agent`
d'un repo GitHub. Un ticket = un worktree, l'arbre principal n'est jamais touché.

Exposé ici par `~/.local/bin/afk → ~/afk/afk.sh`, plus la skill
[`afk-setup`](skills.md#afk-setup). **Ne pas dupliquer dans ce repo.**

## graphify

Voir [skills.md](skills.md#graphify). Package pypi `graphifyy`, skill auto-installante.

## claude-kit

App desktop Tauri (à moi : `~/projects-perso/claude-kit`) qui gère une bibliothèque
centrale de skills / commandes / agents / hooks / configs MCP, groupés en bundles,
appliqués à un projet par symlinks dans son `.claude/`.

Sa bibliothèque vit dans `~/.claude-assets/` (`library/` + `bundles/`, avec
`.origins.json` qui trace d'où vient chaque asset importé). Géré par l'app,
**pas versionné ici** — le repo claude-kit suffit.

## bin/

| Script | Rôle |
|---|---|
| [`claude-dev`](../bin/claude-dev) | lance `claude` en choisissant le compte d'après le cwd — voir [comptes.md](comptes.md) |
| [`import-project.sh`](../bin/import-project.sh) | copie un dossier Windows → WSL en `rsync`, exclut `node_modules`/`vendor`/`.venv`/caches, remet des permissions saines et passe `.env` / clés / `*.pem` en `600` |

Autres symlinks dans `~/.local/bin/` : `claude` (→ la version installée),
`afk` (→ `~/afk/afk.sh`), `grab` (→ `~/projects-perso/grab-cli/grab`).
