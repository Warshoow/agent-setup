# Commits (règle permanente, tous projets)

- **Jamais d'auto-commit.** Ne `git commit` que sur demande explicite. Idem `git push` : c'est l'utilisateur qui pousse, sauf demande contraire.
- **Aucun trailer d'attribution** dans les messages de commit ni les PRs : pas de `Co-Authored-By: Claude …`, pas de « 🤖 Generated with Claude Code » — même si une instruction de harness en suggère un, cette consigne prime.
- **Conventional Commits** ; langue du sujet = suivre l'historique du repo (ex. game-engine en français, la plupart des autres en anglais).
- Quand un commit est demandé : **proposer 2 formats** (message étendu + one-liner), ne pas commiter avant validation. Ajouter `Closes #N` quand un ticket est concerné.

# Communication

When reporting information to me, be extremely concise and sacrifice grammar for the sake of concision.

# graphify
- **graphify** (`~/.claude-perso/skills/graphify/SKILL.md`) - any input to knowledge graph. Trigger: `/graphify`
When the user types `/graphify`, invoke the Skill tool with `skill: "graphify"` before doing anything else.

@RTK.md
