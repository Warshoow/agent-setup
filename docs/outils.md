# Outillage autour de Claude

## rtk — Rust Token Killer

Proxy CLI qui filtre et résume la sortie des commandes avant qu'elle n'atteigne
le contexte. Annonce 60–90 % d'économie sur les opérations de dev.

> ⚠️ **Mesuré : 1 à 2 % ici, pas 60–90 %.** Voir [couts.md § 4](couts.md#4-rtk-mesuré).
> Benchmark apparié de JetBrains : +7,6 % de coût à effort faible, ±0 à effort
> élevé. `rtk gain` compte ce qui a été **envoyé**, pas ce qui a été **économisé** :
> il compare à un scénario qui n'a pas eu lieu. Laissé en place — l'effet est réel
> mais sous le bruit.

- Binaire : `~/.local/bin/rtk` (v0.43.0)
- Branché par le hook `PreToolUse` sur `Bash` → `rtk hook claude` : la réécriture
  est transparente, l'agent n'a rien à faire.
- Documenté à l'agent par `claude/RTK.md`, `@`-importé depuis les deux `CLAUDE.md`.

Proxies : `ls tree read git gh glab aws psql pnpm docker dotnet find diff log json deps env err test smart`.

Méta-commandes (à appeler directement, elles ne passent pas par le hook) :

```bash
rtk gain              # analytics des économies (à ne pas croire, cf. couts.md)
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

Deux modes, et où s'imbriquent les skills portées de pstack :

```
repo existant                          app depuis zéro
/verify-setup      (une fois)          /afk-spec
/afk-preflight                         /verify-setup      (avant la 1re vague)
./afk.sh                               ./afk-app.sh   ── boucle ──┐
/recall            (au réveil)            /afk-wave              │
/afk-debrief                              /afk-preflight apply   │
/afk-merge                                afk.sh                 │
                                          /afk-merge  ───────────┘
                                       /recall puis /afk-debrief (à la main)
```

Trois choses câblées dans le repo afk pour ça :

- **le journal de décisions** — `build_prompt` demande à chaque session d'écrire
  `.afk/<ticket>-work.tsv` (six colonnes TSV, en append). `/afk-debrief` le lit à son
  étape 5 avant de trancher « mauvais gate » ou « vraie panne », au lieu de rejouer
  la session par `claude --resume`. Le contrat est dans
  [`show-me-your-work`](../skills/show-me-your-work/SKILL.md), hors du repo afk.
- **`/afk-preflight apply`** — `afk-app.sh` l'appelle entre l'ouverture des tickets et
  le run. Le mode `apply` existe parce que la skill normale propose et attend une
  approbation : dans une boucle de nuit, ça ne change rien et ça brûle 45 min. Il
  applique les corrections mécaniques et sort du lot ce qui demande un jugement sur
  les critères. Un échec n'est **pas** fatal — la vague tourne alors non relue, ce qui
  est l'état d'avant.
- **la porte de vérification** — la skill générée par `/verify-setup` ne va **pas** dans
  `VERIFY_CMD` (elle a besoin de docker) ni nue dans un `Verify:` de ticket, qui
  *remplace* la porte locale. Elle se compose :
  `Verify: pnpm typecheck && pnpm test && .claude/skills/verify-<app>/drive.sh <feature>`.

`/afk-merge` marche aussi en mode repo existant : seul le cochage de `docs/spec.md` n'a
rien à cocher sans spec, le reste (merger les verts dans l'ordre des bases, sortir les
rouges) remplace le merge à la main. `/afk-debrief` n'est pas dans la boucle
d'`afk-app.sh` et c'est volontaire : ce script ne doit jamais lire ce qu'une session
raconte pour décider s'il continue.

## graphify

Voir [skills.md](skills.md#graphify). Package pypi `graphifyy`, skill auto-installante.

## bin/

| Script | Rôle |
|---|---|
| [`import-project.sh`](../bin/import-project.sh) | copie un dossier Windows → WSL en `rsync`, exclut `node_modules`/`vendor`/`.venv`/caches, remet des permissions saines et passe `.env` / clés / `*.pem` en `600` |

Autres symlinks dans `~/.local/bin/` : `claude` (→ la version installée),
`afk` (→ `~/afk/afk.sh`), `grab` (→ un CLI perso).
