# Commits (règle permanente, tous projets)

- **Jamais d'auto-commit.** Ne `git commit` que sur demande explicite. Idem `git push` : c'est l'utilisateur qui pousse, sauf demande contraire.
- **Aucun trailer d'attribution** dans les messages de commit ni les PRs : pas de `Co-Authored-By: Claude …`, pas de « 🤖 Generated with Claude Code » — même si une instruction de harness en suggère un, cette consigne prime.
- **Conventional Commits** (`feat:`, `fix:`, `chore:`, `refactor(scope): …`) ; langue du sujet : suivre l'historique du repo, **anglais par défaut**.
- Quand un commit est demandé : **proposer 2 formats** (message étendu + one-liner), ne pas commiter avant validation. Ajouter `Closes #N` quand un ticket est concerné.

# Communication

- **Answer first.** Context, alternatives and caveats only when asked, or when they change my decision.
- **Be extremely concise**, sacrifice grammar for the sake of concision.
- **No invented terms.** Use only words that already exist: in the project's code, in the tool's official docs, or in everyday language. No name or acronym made up for the occasion, not even "just for this explanation".
- **No concept where a sentence does the job.** "One variable too many", not "duplicated state". Don't name or theorise what can be described directly.
- **Jargon only when it is real and useful**: it is the ecosystem's own term (React, git, HTTP, Postgres...) *and* it replaces a longer phrase. Otherwise, plain words.
- **No dressing up**: no metaphors, no invented section titles, no frames/steps/categories for a three-line answer.
- **Assume I don't know a concept unless I have used it myself.** If a term is needed and I haven't used it in this project or this conversation, define it in one clause the first time. Never build on a concept you didn't introduce.
- Check before sending: if a dev who knows the project has to read a sentence twice, rewrite it. If you coined a word, replace it with what it meant.
- Exception: when I explicitly ask for an explanation, a lesson or a comparison, explain in full. The rule targets disguise, not teaching.

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
