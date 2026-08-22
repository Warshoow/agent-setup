# Plugins & marketplaces

Rien à sauvegarder : les plugins se réinstallent seuls au premier lancement, à
partir des deux clés `extraKnownMarketplaces` et `enabledPlugins` du
`settings.json`. Le `plugins/cache/` sur disque est jetable.

## Installés

| Plugin | Marketplace | Version | perso | pro |
|---|---|---|:--:|:--:|
| `ponytail` | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | 4.8.4 / 4.8.3 | ✅ | ✅ |
| `mattpocock-skills` | [mattpocock/skills](https://github.com/mattpocock/skills) | 1.2.0 | ✅ | ✅ |
| `marketing-skills` | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | 2.9.0 | ✅ | — |
| `ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 2.13.0 | ✅ | — |

La marketplace officielle (`claude-plugins-official`) est présente dans les deux,
auto-installée par Claude Code, sans plugin activé.

## ponytail

Force la solution la plus paresseuse qui marche (YAGNI, stdlib avant dépendance,
une ligne avant cinquante). **Actif en permanence**, niveau `full` — l'état est
dans `~/.claude-{perso,pro}/.ponytail-active`.

Il fournit aussi la **statusline** des deux comptes :

```json
"statusLine": {
  "type": "command",
  "command": "bash \"$CLAUDE_CONFIG_DIR/plugins/marketplaces/ponytail/hooks/ponytail-statusline.sh\""
}
```

> Le chemin est écrit en absolu dans chaque `settings.json` (`.claude-perso/…` vs
> `.claude-pro/…`) — c'est la seule ligne à ne pas copier bêtement d'un compte à l'autre.

Commandes : `/ponytail lite|full|ultra`, `/ponytail-review`, `/ponytail-audit`,
`/ponytail-debt`, `/ponytail-gain`.

## mattpocock-skills

Le socle de méthode : `grilling`, `tdd`, `diagnosing-bugs`, `research`,
`domain-modeling`, `codebase-design`, `code-review`, `prototype`,
`resolving-merge-conflicts`. C'est ce dont dépend le workflow décrit dans
[afk.sh](https://github.com/Warshoow/afk.sh) : grill → tickets → une session
neuve par ticket.

## marketing-skills (perso seulement)

~50 skills marketing (SEO, ads, copywriting, pricing, launch…). Compte perso
uniquement, pour les projets produit.

## ui-ux-pro-max (perso seulement)

Base de données de design consultable — 84 styles, 192 palettes, 74 pairings de
polices, 98 règles UX, sur 22 stacks. Ce n'est pas une skill qui décide, c'est un
oracle. Voir [design.md](design.md) pour sa place dans le stack design et les
combinaisons à éviter. Nécessite Python 3 (stdlib seule).

## Réglages communs aux deux comptes

```json
"model": "opus[1m]", "effortLevel": "xhigh", "tui": "fullscreen",
"theme": "dark", "agentPushNotifEnabled": true
```

## MCP

**Aucun serveur MCP configuré au niveau utilisateur ni projet.** Les connecteurs
claude.ai (Canva, Gmail, Drive, Calendar, Stripe) sont branchés côté compte
claude.ai, pas dans un fichier — ils se réautorisent via `/mcp`.
