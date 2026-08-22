# ─── Claude Code — à sourcer depuis ~/.bashrc ────────────────────────────────
# (extrait de ~/.bashrc ; `install.sh` ajoute la ligne `source` qui va bien)

export PATH="$HOME/bin:$HOME/.local/bin:$PATH"

# Compte par défaut. Tout le reste (skills, agents, plugins, mémoire, sessions)
# vit sous ce dossier — c'est LA variable qui bascule d'un compte à l'autre.
export CLAUDE_CONFIG_DIR="$HOME/.claude-perso"

# Bascule manuelle, dans le shell courant.
claude-pro()   { export CLAUDE_CONFIG_DIR="$HOME/.claude-pro";   echo "Claude: compte pro actif"; }
claude-perso() { export CLAUDE_CONFIG_DIR="$HOME/.claude-perso"; echo "Claude: compte perso actif"; }

# Seuil du hook context-watch. Défaut du script = 200k ; le modèle est opus[1m].
export CTX_LIMIT=1000000

# graphify → export Obsidian (relu par les devcontainers via ${localEnv:OBSIDIAN_VAULT_PATH}).
# À adapter : chemin WSL du vault côté Windows.
export OBSIDIAN_VAULT_PATH="/mnt/c/Users/<user-windows>/Documents/obsidian-vault/ai-vault"

# ssh-agent pour les creds GitHub
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval "$(ssh-agent -s)" > /dev/null
    ssh-add ~/.ssh/id_ed25519 2>/dev/null
fi
