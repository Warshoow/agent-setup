# Subagents user-level — politique de modèles

Agents **génériques** disponibles dans tous les projets. Source unique : `~/agents/`,
exposée à la config Claude par un symlink :

```
~/.claude/agents → ~/agents
```

Dans les devcontainers, `~/agents` est bind-mounté (même chemin absolu) pour que
les symlinks se résolvent — même mécanique que `~/skills`.

Un projet peut **surcharger** un agent en plaçant un fichier du même nom dans son
`.claude/agents/` (le niveau projet gagne) — utile pour un repo dont la stack
justifie des versions spécialisées.

| Agent            | Modèle | Rôle                                        | Écrit ? |
|------------------|--------|---------------------------------------------|:------:|
| `planner`        | opus   | Architecture & plan d'implémentation        | non    |
| `debugger`       | opus   | Cause racine de bugs complexes              | non*   |
| `reviewer`       | opus   | Revue sensible (auth, sécu, contrats d'API) | non    |
| `reviewer-quick` | sonnet | Revue courante, escalade vers `reviewer`    | non    |
| `builder`        | sonnet | Implémentation bien spécifiée               | oui    |
| `tester`         | sonnet | Tests de comportement                       | oui    |
| `devops`         | sonnet | Infra de dev : devcontainer/compose/CI, standard commun | oui |
| `scout`          | haiku  | Recherche lecture seule (Read/Grep/Glob)    | non    |

\* le debugger investigue et propose ; il n'applique le fix que sur demande.

Principe : **performance et fiabilité d'abord, économie de tokens ensuite.**
Opus pour le raisonnement/l'ambiguïté/la revue critique, Sonnet pour
l'implémentation bien spécifiée, Haiku pour le mécanique. Les alias de modèles
suivent automatiquement les meilleures versions.

Pas de `scribe` au niveau user : les messages de commit et la doc courante se
font très bien dans la session principale, l'aller-retour agent coûte plus qu'il
ne rapporte. Le rajouter ici si le besoin revient.
