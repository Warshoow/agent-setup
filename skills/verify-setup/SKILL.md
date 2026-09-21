---
name: verify-setup
description: Génère dans un repo une skill locale `verify-<app>` qui pilote la vraie app comme un utilisateur (lancer, piloter, capturer la preuve, nettoyer) plus une carte des features, et la maintient quand l'app change. À lancer une fois par projet, avant le premier run afk. Déclencheurs : /verify-setup, « comment on prouve que ça marche ici ? », « ce projet n'a aucun moyen de vérifier », « prépare la vérification pour afk », « mets à jour la carte des features ».
---

# Verify setup

Un projet sérieux a un moyen scripté de piloter la vraie app et de prouver un
comportement : la lancer, exercer une feature comme un utilisateur, capturer la
preuve. Ici on écrit ce moyen **dans le repo**, pour le prochain agent qui
arrivera froid au milieu d'une tâche — pas pour un humain.

Porté de pstack (`cursor/plugins`), branché sur `visual-check` pour le web.

Deux modes : **générer** (le repo n'a rien) et **maintenir** (la skill existe,
l'app a bougé). Va directement à *Maintenir* si `.claude/skills/verify-*/` existe.

## 1. Interroger le repo, pas l'utilisateur

Réponds à ça depuis le code, et ne demande que ce que tu ne peux pas observer :

- **Surface** — ce que l'utilisateur touche vraiment : UI web, CLI/TUI, app
  desktop, API, lib. Plusieurs possibles : prends la principale, note les autres.
- **Lancer** — comment l'app démarre en local. Prends la commande documentée du
  repo (scripts package.json, Makefile, README), pas une que tu inventes. Note
  ports, variables d'env, données de seed, auth.
- **Piloter** — comment un agent interagit avec, par ordre de préférence :
  1. un harnais déjà là (spec Playwright/Cypress, script expect, endpoint curl,
     port de debug) ;
  2. **surface web → `visual-check`** : le container `~/projects-perso/playright-env/pw`
     est déjà installé et gère les cas WSL/devcontainer. N'ajoute jamais
     `playwright` aux dépendances du projet pour ça ;
  3. sinon : tmux/PTY pour un CLI/TUI, `curl` pour un service.
- **Observer** — ce qui peut servir de preuve : screenshots, transcript terminal,
  corps de réponse, logs, codes de sortie, état en base.
- **Isoler** — deux instances peuvent-elles tourner côte à côte (ports, dossiers
  de données, profils) ? Si non, dis-le dans la skill générée : refuser de
  piloter une instance partagée vaut mieux que corrompre la session en cours.

Si le checkout ne build pas ou ne démarre pas tel quel, répare ça d'abord (ou
rapporte-le précisément). Une skill écrite contre une base cassée enseigne des
gestes faux.

## 2. Générer la skill

`.claude/skills/verify-<app>/SKILL.md`, avec frontmatter YAML (`name: verify-<app>`
et une `description` qui nomme l'app, la surface et quand y recourir — sans
frontmatter la skill ne s'enregistre pas). Chaque section ancrée dans ce que
l'étape 1 a trouvé, aucun placeholder :

- **Lancer** — la commande exacte, et comment savoir que c'est prêt (une ligne de
  log, un port qui répond, un prompt). Pour un CLI court il n'y a pas de serveur
  à garder en vie : lancer = builder le binaire une fois, puis démarrer chaque
  pilotage dans son propre tmux/PTY isolé.
- **Doctor** — un contrôle en lecture seule qui répond « cette instance vaut-elle
  la peine d'être pilotée ? » : process up, bonne version, port à nous, auth
  valide. À lancer dès que quelque chose cloche.
- **Piloter** — la recette, avec les vrais sélecteurs et commandes de **ce** repo.
  Préfère les poignées stables (labels ARIA, attributs `data-`, chaînes de
  prompt, chemins de route) aux coordonnées et à l'ordre de tabulation.
- **Preuve** — quoi capturer et où ça va. Les règles : exercer le vrai chemin
  utilisateur et pas un setter interne ou un endpoint de test ; capturer l'action
  **et** l'état résultant, pas seulement l'écran final ; vérifier les effets de
  bord (fichiers écrits, lignes insérées, messages envoyés) autant que le
  visible ; mocker seulement là où une frontière de prod isole déjà le système
  externe. Quand le chemin sûr est un `--dry-run`, vérifie par observation ce
  qu'il saute vraiment (fichiers, réseau, refs git) : certains dry-runs touchent
  quand même le réseau.
- **Nettoyer** — comment démonter ce que le run a créé. Jamais de kill par nom de
  process : tue ce que tu as démarré. Le nettoyage enlève les instances et l'état
  jetable, **jamais** les preuves, qui survivent à un endroit que la skill nomme.
- **Helpers** — tout script livré est exécutable et son appel est montré dans le
  corps de la skill. Un helper qu'il faut rétro-analyser n'est pas un helper.

## 3. Semer la carte des features

`.claude/skills/verify-<app>/features/README.md` (l'index) plus un fichier par
feature visible par l'utilisateur. Vise les 3 à 5 principales pour commencer,
repérées depuis les routes, les commandes, les menus ou la doc. Forme dans
[`references/feature-map.md`](references/feature-map.md).

La carte est la source de vérité de la vérification du repo. Une preuve qui
pilote un seul point d'entrée pratique est incomplète dès que la carte en liste
d'autres.

## 4. Prouver la skill générée avant de la rendre

Fais tourner ses propres instructions de bout en bout une fois : lancer, doctor,
piloter **une** feature de la carte, capturer la preuve, nettoyer. Après le
nettoyage, vérifie que la preuve existe encore à l'endroit annoncé — un nettoyage
qui mange la preuve échoue cette étape. Relance le nettoyage après chaque
itération ratée aussi, pour ne pas laisser traîner de process ni de ports.

Une skill générée jamais exécutée est un brouillon, pas un livrable.

## 5. Brancher sur afk

Si le repo a un `.afk.env`, son gate doit appeler la skill générée plutôt que de
redéfinir sa propre liste de commandes. Et dans `docs/spec.md`, un critère dont
la preuve passe par l'app se référence à un fichier de la carte des features.

## Maintenir

Quand l'app a bougé, ou sur demande :

1. Relis les routes, commandes et menus, et diffe avec `features/`. Une feature
   ajoutée sans fichier, un fichier dont le point d'entrée n'existe plus.
2. Rejoue **Lancer + Doctor**. S'ils échouent, c'est ça le bug, avant la carte.
3. Rejoue le pilotage d'une feature au hasard parmi celles qui ont changé.
4. Corrige les sélecteurs et commandes morts dans la carte, supprime les fichiers
   des features supprimées.

Ne réécris pas la carte entière : une carte régénérée perd les *Gotchas*, qui
sont la seule partie que personne ne peut re-déduire du code.
