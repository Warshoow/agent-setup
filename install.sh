#!/usr/bin/env bash
# Restaure le setup Claude Code sur une machine neuve (WSL / Linux).
# Idempotent : relançable sans casse. Ne touche jamais aux credentials.
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRY=0
[[ "${1:-}" == "-n" || "${1:-}" == "--dry-run" ]] && DRY=1

say()  { printf '  %s\n' "$*"; }
step() { printf '\n▸ %s\n' "$*"; }
run()  { if (( DRY )); then say "[dry] $*"; else eval "$@"; fi; }

step "Sources uniques : ~/agents, ~/skills, ~/hooks, ~/bin"
for d in agents skills hooks bin; do
  run "mkdir -p \"\$HOME/$d\""
  run "cp -rn \"$REPO/$d/.\" \"\$HOME/$d/\" 2>/dev/null || true"
done
run "chmod +x \"\$HOME/hooks/\"*.sh \"\$HOME/bin/\"* 2>/dev/null || true"
# import-project.sh vit dans ~/.local/bin (déjà dans le PATH)
run "mkdir -p \"\$HOME/.local/bin\" && cp -n \"$REPO/bin/import-project.sh\" \"\$HOME/.local/bin/\" 2>/dev/null || true"

step "Les deux configs Claude"
for acct in perso pro; do
  CFG="$HOME/.claude-$acct"
  run "mkdir -p \"$CFG/skills\""
  run "cp -n \"$REPO/claude/CLAUDE.$acct.md\" \"$CFG/CLAUDE.md\" 2>/dev/null || true"
  run "cp -n \"$REPO/claude/RTK.md\"          \"$CFG/RTK.md\"    2>/dev/null || true"
  run "cp -n \"$REPO/claude/settings.$acct.json\" \"$CFG/settings.json\" 2>/dev/null || true"
  # agents : un seul dossier, exposé par symlink aux deux configs
  run "ln -sfn \"\$HOME/agents\" \"$CFG/agents\""
  # skills perso : idem, un symlink par skill (Claude Code les suit)
  for s in audit-360 checkpoint coach-craft evolve; do
    run "ln -sfn \"\$HOME/skills/$s\" \"$CFG/skills/$s\""
  done
done

step "afk (repo séparé : github.com/Warshoow/afk.sh)"
if [[ -d "$HOME/afk" ]]; then
  run "ln -sfn \"\$HOME/afk/skills/afk-setup\" \"\$HOME/skills/afk-setup\""
  run "ln -sfn \"\$HOME/skills/afk-setup\" \"\$HOME/.claude-perso/skills/afk-setup\""
  run "ln -sfn \"\$HOME/afk/afk.sh\" \"\$HOME/.local/bin/afk\""
else
  say "~/afk absent — git clone git@github.com:Warshoow/afk.sh.git ~/afk, puis relancer."
fi

step "Shell"
BRC="$HOME/.bashrc"
if grep -qF 'bashrc-claude.sh' "$BRC" 2>/dev/null; then
  say "déjà sourcé dans ~/.bashrc"
elif (( DRY )); then
  say "[dry] ajout du 'source $REPO/shell/bashrc-claude.sh' dans ~/.bashrc"
else
  {
    printf '\n# Claude Code (agent-setup)\n'
    printf '[ -f "%s/shell/bashrc-claude.sh" ] && . "%s/shell/bashrc-claude.sh"\n' "$REPO" "$REPO"
  } >> "$BRC"
  say "ajouté à ~/.bashrc — ouvre un nouveau shell"
fi

step "À faire à la main"
cat <<'MANUAL'
  1. claude login          — pour CHAQUE compte :
       CLAUDE_CONFIG_DIR=~/.claude-perso claude   puis /login
       CLAUDE_CONFIG_DIR=~/.claude-pro   claude   puis /login
  2. Les plugins se réinstallent seuls au 1er lancement (extraKnownMarketplaces
     + enabledPlugins dans settings.json). Sinon : /plugin
  3. rtk  : cargo install rtk  (ou binaire) → ~/.local/bin/rtk
  4. graphify : `uv tool install graphifyy` — le skill s'auto-installe au 1er /graphify.
     Le skill lui-même n'est PAS vendored ici (voir docs/skills.md).
  5. git : ~/.gitconfig (user Warshoow), clé ~/.ssh/id_ed25519 à restaurer.
MANUAL
