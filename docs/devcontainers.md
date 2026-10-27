# Devcontainers

Le setup repose sur des symlinks `~/.claude/…  →  ~/.agents/…`. Dans un
conteneur, ces cibles n'existent pas : **les liens sont morts et les agents/skills
disparaissent silencieusement**.

La parade : bind-monter les cibles **au même chemin absolu** que sur l'hôte.

Extrait du `devcontainer.json` du projet qui sert de référence aux autres :

```jsonc
"mounts": [
  // Cibles réelles des symlinks ~/.claude/skills/* (sinon liens morts dans le conteneur).
  "source=${localEnv:HOME}/.agents,target=${localEnv:HOME}/.agents,type=bind,readonly",
  // Seul endroit où un conteneur écrit : le log Laya.
  "source=${localEnv:HOME}/.agents/laya,target=${localEnv:HOME}/.agents/laya,type=bind",
  "source=${localEnv:HOME}/.claude,target=${localEnv:HOME}/.claude,type=bind",
  "source=${localEnv:HOME}/.gitconfig,target=/home/node/.gitconfig,type=bind",
  "source=${localEnv:HOME}/.ssh,target=/home/node/.ssh,type=bind,readonly",
  "source=${localEnv:HOME}/.local/bin/claude,target=/usr/local/bin/claude,type=bind,readonly",
  "source=${localEnv:HOME}/.graphify-cache,target=/home/node/.graphify-cache,type=bind",
  // Vault Obsidian pour l'export graphify (OBSIDIAN_VAULT_PATH défini côté hôte)
  "source=${localEnv:OBSIDIAN_VAULT_PATH},target=/workspaces/<projet>/vault,type=bind"
],
"remoteEnv": {
  "CLAUDE_CONFIG_DIR": "${localEnv:HOME}/.claude",
  "GIT_CONFIG_GLOBAL": "/tmp/gitconfig"
}
```

Trois points qui comptent :

1. **`target` == `source`** pour `.agents`. Pas `/home/node/.agents` :
   `~/.claude` est monté au chemin de l'hôte, et ses liens relatifs
   (`../.agents/…`) doivent retomber sur ce même chemin dans le conteneur.
2. **`readonly`** sur `~/.agents` — un conteneur ne réécrit pas mes skills, agents, hooks ni instructions. Seul `~/.agents/laya` est en écriture.
3. **`remoteEnv.CLAUDE_CONFIG_DIR`** est obligatoire ici, alors qu'il n'est plus
   posé sur l'hôte : le `$HOME` du conteneur (`/home/node`) n'est pas celui où la
   config est montée, donc le défaut `~/.claude` tomberait à côté. Le monter sur
   `/home/node/.claude` à la place ne marche pas : les plugins Claude Code
   enregistrent des chemins absolus, une install faite dans le conteneur casse
   celle de l'hôte et réciproquement.

Le dossier de config (`.claude`) est monté **en écriture** : sessions,
mémoire et plugins du travail fait dans le conteneur remontent sur l'hôte.

L'agent [`devops`](../agents/devops.md) connaît ce standard et sait aligner un
projet dessus, en diffant contre le projet de référence.
