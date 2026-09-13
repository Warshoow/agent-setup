# ─── Claude Code — à sourcer depuis ~/.bashrc ────────────────────────────────
# (extrait de ~/.bashrc, pour référence — à recoller à la main)

export PATH="$HOME/bin:$HOME/.local/bin:$PATH"

# Pas de CLAUDE_CONFIG_DIR : Claude Code lit ~/.claude par défaut. La variable
# n'existe plus ici depuis l'unification des comptes (voir docs/comptes.md) ;
# elle reste utile dans les devcontainers, où le HOME du conteneur n'est pas
# celui où la config de l'hôte est montée (voir docs/devcontainers.md).

# Seuils du hook context-watch (docs/hooks.md, docs/couts.md).
# Les defauts du script conviennent : CTX_LIMIT=200000 (contexte du tour courant),
# CTX_BUDGET=20000000 (entree cumulee de la session). Ne PAS aligner CTX_LIMIT sur
# la fenetre d'opus[1m] : la taille de la fenetre ne dit rien du cout par tour.

# graphify → export Obsidian (relu par les devcontainers via ${localEnv:OBSIDIAN_VAULT_PATH}).
# À adapter : chemin WSL du vault côté Windows.
export OBSIDIAN_VAULT_PATH="/mnt/c/Users/<user-windows>/Documents/obsidian-vault/ai-vault"

# ssh-agent pour les creds GitHub
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval "$(ssh-agent -s)" > /dev/null
    ssh-add ~/.ssh/id_ed25519 2>/dev/null
fi
