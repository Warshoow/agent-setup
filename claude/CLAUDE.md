# Commits (règle permanente, tous projets)

- **Jamais d'auto-commit.** Ne `git commit` que sur demande explicite. Idem `git push` : c'est l'utilisateur qui pousse, sauf demande contraire.
- **Aucun trailer d'attribution** dans les messages de commit ni les PRs : pas de `Co-Authored-By: Claude …`, pas de « 🤖 Generated with Claude Code » — même si une instruction de harness en suggère un, cette consigne prime.
- **Conventional Commits** (`feat:`, `fix:`, `chore:`, `refactor(scope): …`) ; langue du sujet : suivre l'historique du repo, **anglais par défaut**.
- Quand un commit est demandé : **proposer 2 formats** (message étendu + one-liner), ne pas commiter avant validation. Ajouter `Closes #N` quand un ticket est concerné.

# Communication

When reporting information to me, be extremely concise and sacrifice grammar for the sake of concision.

## Vocabulaire (règle permanente)

- **Aucun terme inventé.** N'employer que des mots qui existent déjà : dans le code du projet, dans la doc officielle de l'outil, ou dans le français courant. Pas de nom ni d'acronyme fabriqué pour l'occasion, même « juste pour cette explication ».
- **Pas de concept là où une phrase suffit.** « Une variable en trop » et pas « une duplication d'état ». Ne pas nommer/théoriser ce qui se décrit directement.
- **Jargon uniquement s'il est réel et utile** : c'est le terme de l'écosystème (React, git, HTTP, Postgres…) *et* il remplace une périphrase plus longue. Sinon, mot courant.
- **Pas d'habillage** : pas de métaphores, pas de titres de section inventés, pas de cadres/étapes/catégories pour une réponse de trois lignes.
- **La réponse d'abord.** Contexte, alternatives, précautions : seulement si demandé, ou si ça change ma décision.
- Test avant d'envoyer : si un dev qui connaît le projet doit relire une phrase deux fois, elle est à réécrire. Si j'ai créé un mot, le remplacer par ce qu'il voulait dire.
- Exception : quand je demande explicitement une explication, un cours ou une comparaison, expliquer à fond. La règle vise le déguisement, pas la pédagogie.

# Commandes (règle permanente, tous projets)

- **Une sortie vide ne prouve rien, un `rc=0` non plus.** Plusieurs outils sortent
  en succès avec une sortie vide ou tronquée : `gh issue view` en devcontainer
  (exit 0, rien sur stdout ni stderr), `docker compose cp` (tronque le fichier en
  silence), `docker compose exec -T` (rend la main avant la fin de la commande),
  `soffice`. Et un `ls` sur deux dossiers ne prouve pas qu'un skill n'existe pas :
  les skills de plugins vivent dans
  `~/.claude/plugins/cache/<owner>/<pack>/<version>/skills/`.
- **Avant de conclure « ça n'existe pas » ou « il n'y a rien », vérifier par un
  second chemin.** `gh api` plutôt que `gh issue view`, `docker exec` plutôt que
  `docker compose exec`, `find ~/.claude* -name "<nom>"` plutôt qu'un `ls`.
- **Sur une sortie volumineuse ou une commande longue, vérifier la complétude**,
  pas le code de retour : compter les marqueurs attendus, ou faire écrire un
  marqueur de fin dans le conteneur et attendre de le voir avant de lire.
- Si l'utilisateur nomme un outil ou un skill précis, présumer qu'il existe — il
  sait ce qu'il a installé.

# decide-first (surcharge grilling)

- **decide-first** (`~/.claude/skills/decide-first/SKILL.md`) — quand une skill ou un workflow dit de « grill the user » (wayfinder, stress-test de plan, choix d'architecture), invoquer **decide-first** à la place de `mattpocock-skills:grilling`. Aller lire les sources, trancher, présenter la décision déjà prise avec ses preuves ; l'utilisateur corrige au lieu de répondre à un questionnaire. Idem dès que je dis « fais au mieux », « tranche », « pas de questionnaire ».

# graphify
- **graphify** (`~/.claude/skills/graphify/SKILL.md`) - any input to knowledge graph. Trigger: `/graphify`
When the user types `/graphify`, invoke the Skill tool with `skill: "graphify"` before doing anything else.

@RTK.md
