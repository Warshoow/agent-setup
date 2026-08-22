# Devcontainers

Le setup repose sur des symlinks `~/.claude-*/…  →  ~/{agents,skills}`. Dans un
conteneur, ces cibles n'existent pas : **les liens sont morts et les agents/skills
disparaissent silencieusement**.

La parade : bind-monter les cibles **au même chemin absolu** que sur l'hôte.

Extrait du `devcontainer.json` du projet qui sert de référence aux autres :

```jsonc
"mounts": [
  // Cibles réelles des symlinks ~/.claude-*/skills/* (sinon liens morts dans le conteneur).
  "source=${localEnv:HOME}/skills,target=${localEnv:HOME}/skills,type=bind,readonly",
  "source=${localEnv:HOME}/agents,target=${localEnv:HOME}/agents,type=bind,readonly",
  "source=${localEnv:HOME}/.claude-perso,target=${localEnv:HOME}/.claude-perso,type=bind",
  "source=${localEnv:HOME}/.gitconfig,target=/home/node/.gitconfig,type=bind",
  "source=${localEnv:HOME}/.ssh,target=/home/node/.ssh,type=bind,readonly",
  "source=${localEnv:HOME}/.local/bin/claude,target=/usr/local/bin/claude,type=bind,readonly",
  "source=${localEnv:HOME}/.graphify-cache,target=/home/node/.graphify-cache,type=bind",
  // Vault Obsidian pour l'export graphify (OBSIDIAN_VAULT_PATH défini côté hôte)
  "source=${localEnv:OBSIDIAN_VAULT_PATH},target=/workspaces/<projet>/vault,type=bind"
],
"remoteEnv": {
  "CLAUDE_CONFIG_DIR": "${localEnv:HOME}/.claude-perso",
  "GIT_CONFIG_GLOBAL": "/tmp/gitconfig"
}
```

Trois points qui comptent :

1. **`target` == `source`** pour `skills` et `agents`. Pas `/home/node/skills` :
   le symlink pointe vers le `$HOME` de l'hôte en dur, il faut ce
   chemin-là dans le conteneur.
2. **`readonly`** sur les sources partagées — un conteneur ne réécrit pas mes skills.
3. **`remoteEnv.CLAUDE_CONFIG_DIR`** choisit le compte du projet. C'est
   l'équivalent conteneur de [`claude-dev`](../bin/claude-dev).

Le dossier de config (`.claude-perso`) est monté **en écriture** : sessions,
mémoire et plugins du travail fait dans le conteneur remontent sur l'hôte.

L'agent [`devops`](../agents/devops.md) connaît ce standard et sait aligner un
projet dessus, en diffant contre le projet de référence.
