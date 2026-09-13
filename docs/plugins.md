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
  "command": "bash \"${HOME}/.claude/plugins/marketplaces/ponytail/hooks/ponytail-statusline.sh\""
}
```

> Le chemin est écrit en absolu dans `settings.json` : `$CLAUDE_CONFIG_DIR` n'est
> plus posé dans l'environnement depuis l'unification des comptes.

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

**Rien au niveau utilisateur** — pas de `mcpServers` dans les `.claude.json`.
Tout est déclaré **par projet**, dans un `.mcp.json` à la racine du repo. Les
serveurs qui reviennent :

| Serveur | Transport | À quoi |
|---|---|---|
| `magic` ([21st.dev](https://21st.dev/)) | stdio, `npx @21st-dev/magic` | bibliothèque de composants React/Tailwind — voir [design.md](design.md) |
| `stripe-test` / `stripe-live` | http, `mcp.stripe.com` | deux entrées, deux clés, jamais confondues |
| `supabase` | http, `mcp.supabase.com` | base, storage, branching, edge functions |
| `resend` | stdio, `npx resend-mcp` | emails transactionnels |
| `dokploy-mcp` | stdio, `npx @dokploy/mcp` | déploiement |
| `gsc` | stdio, `uvx mcp-search-console` | Search Console |

Les clés passent par `${VAR}` dans `.mcp.json`, résolues depuis le bloc `env` du
`.claude/settings.local.json` du projet — **gitignoré, jamais versionné**.
Attention : Claude Code n'expanse pas `${VAR}` partout (le `.mcp.json` d'un
projet le note en commentaire pour `dokploy`).

Les connecteurs claude.ai (Canva, Gmail, Drive, Calendar, Stripe) sont branchés
côté compte claude.ai, pas dans un fichier — ils se réautorisent via `/mcp`.
