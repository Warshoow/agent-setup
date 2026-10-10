# agent-setup

A record of my **Claude Code** setup on WSL: a single config, custom agents and
skills, hooks, plugins, and the tooling around them (rtk, graphify, afk).

This repo is a **documented archive**, not an installer. It exists so I know what
I had and why, if the machine goes.

Project names and personal paths have been removed, so the config files have to
be put back together by hand, not copied as they are. The docs under `docs/` are
in French.

## The map

```
~/
├── .claude/                full Claude Code config
│     │                          (sessions, memory, plugins, creds)
│     ├── CLAUDE.md               global instructions
│     ├── RTK.md                  @-imported by CLAUDE.md
│     ├── settings.json           model, hooks, statusline, plugins
│     ├── agents  ──symlink──►  ~/agents
│     ├── skills/<name> ─symlink► ~/skills/<name>
│     └── skills/graphify         (installed by the skill itself)
│
├── agents/                 SINGLE SOURCE of the 8 user-level subagents
├── skills/                 SINGLE SOURCE of the custom skills
├── hooks/                  context-watch.sh (Stop) + big-read-gate.py (PreToolUse)
├── afk/                    separate repo → github.com/Warshoow/afk.sh
├── projects-perso/         personal projects
└── projects-pro/           work projects
```

The idea: **one copy of each asset in `~`**, exposed to the config through a
symlink. Edit `~/agents/planner.md` and Claude Code sees it. It is also what makes
devcontainers possible (see [docs/devcontainers.md](docs/devcontainers.md)).

## What is in this repo

| Path | What |
|---|---|
| [claude/](claude/) | `CLAUDE.md`, `RTK.md`, `settings.json` |
| [agents/](agents/) | the 8 subagents and which model each one uses |
| [skills/](skills/) | `audit-360`, `checkpoint`, `coach-craft`, `evolve`, `recall`, `show-me-your-work`, `verify-setup` + two custom design skills |
| [hooks/](hooks/) | `context-watch.sh` (context + running budget), `big-read-gate.py` (blocks full-file reads) |
| [bin/](bin/) | `import-project.sh`, `audit-tokens.py` (what sessions really cost) |
| [shell/](shell/) | the `~/.bashrc` excerpt: PATH, context threshold, ssh-agent |
| [experimental/](experimental/) | drafts (multi-agent handoff) |

## The docs

- **[docs/comptes.md](docs/comptes.md)**: the single config, what it holds, what comes from `~` by symlink, and the history of the two-account setup.
- **[docs/skills.md](docs/skills.md)**: the custom skills, one line each, plus the external ones (graphify), **and the three scopes of pstack**, with what was ruled out and why.
- **[agents/README.md](agents/README.md)**: the subagents and which model each one runs.
- **[docs/design/](docs/design/README.md)**: everything about design: the process for a non-designer, the tools for each step (Claude Design, extraction, visuals, animation), the sourced research, and the skill stack (impeccable, emil, taste-skill, ui-ux-pro-max) **and which ones not to mix**.
- **[docs/plugins.md](docs/plugins.md)**: installed plugins, marketplaces, versions.
- **[docs/hooks.md](docs/hooks.md)**: the three hooks, **and why `context-watch.sh` did not work**.
- **[docs/couts.md](docs/couts.md)**: what sessions cost, measured from the transcripts. 97% of input is context being resent, 20 sessions make up half the bill, **and why rtk's 60–90% does not hold here**.
- **[docs/outils.md](docs/outils.md)**: rtk, graphify, afk.
- **[docs/devcontainers.md](docs/devcontainers.md)**: the mount pattern that keeps the symlinks working inside a container.

## What is NOT here

| What | Why |
|---|---|
| `.credentials.json`, `.claude.json` | OAuth tokens, `userID`, `machineID`. Never in a repo. |
| `~/afk/` | has its own repo: **[github.com/Warshoow/afk.sh](https://github.com/Warshoow/afk.sh)** |
| `skills/graphify/` | third-party skill, installs itself (`uv tool install graphifyy`) |
| `plugins/cache/` | reinstalled from the marketplaces declared in `settings.json` |
| `projects/`, `sessions/`, `history.jsonl` | work history, not config |
| project names | anonymised in the published config files |

## Rebuilding the machine, roughly

1. `claude login` (the config lands in `~/.claude`).
2. Plugins come back on their own at first launch (`extraKnownMarketplaces` + `enabledPlugins`).
3. Reinstall `rtk`, `graphify` (`uv tool install graphifyy`) and `afk` (separate repo).
4. Recreate the symlinks `~/.claude/{agents,skills}` → `~/{agents,skills}`.
5. Source [`shell/bashrc-claude.sh`](shell/bashrc-claude.sh) from `~/.bashrc`.

## Persistent memory

Each project has its memory under `~/.claude/projects/<slug>/memory/`
(`MEMORY.md` as the index + one file per fact). **Not versioned here**: it is work
content, not config.

The [`evolve`](skills/evolve/SKILL.md) skill is the loop that rereads these
memories and suggests turning what keeps coming back into a skill.
