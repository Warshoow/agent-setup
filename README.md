# agent-setup

A record of my **Claude Code** setup on WSL: a single config, custom agents and
skills, hooks, plugins, and the tooling around them (rtk, graphify, afk).

This repo is a **documented archive**, not an installer. It exists so I know what
I had and why. The live config is a private repo cloned at `~/.agents`, with its
own `install.sh`; this one is a cleaned-up copy of it.

Project names and personal paths have been removed, so the config files have to
be put back together by hand, not copied as they are. The docs under `docs/` are
in French.

## The map

```
~/
├── .claude/                Claude Code config (sessions, memory, plugins, creds)
│     ├── settings.json           real file (Claude Code, Orca, Coucou write it)
│     ├── CLAUDE.md, RTK.md, statusline.sh, rules  ─symlink─► ~/.agents/claude/…
│     ├── laya     ─symlink─► ~/.agents/laya
│     ├── agents   ─symlink─► ~/.agents/agents
│     ├── skills/<name> ─symlink─► ~/.agents/skills/<name>
│     └── skills/graphify         (installed by the skill itself)
│
├── .agents/                SINGLE SOURCE, private git repo
│     ├── skills/                 custom skills (+ 3 from Orca/Vercel)
│     ├── agents/                 the 8 user-level subagents
│     ├── hooks/                  context-watch.sh (Stop) + big-read-gate.py (PreToolUse)
│     ├── mods/                   local plugin marketplace (Claude Code mods)
│     ├── claude/                 CLAUDE.md, RTK.md, statusline.sh, rules/, settings.json (copy without machine hooks)
│     ├── laya/                   decision log + scripts
│     └── install.sh              rebuilds all of the above on a new machine
├── afk/                    separate repo → github.com/Warshoow/afk.sh
├── projects-perso/         personal projects
└── projects-pro/           work projects
```

The idea: **one copy of each asset, in `~/.agents`**, exposed to the config through a
symlink. Edit `~/.agents/agents/planner.md` and Claude Code sees it. It is also what makes
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

With the private repo: `git clone … ~/.agents && ~/.agents/install.sh`, then `claude`.
It creates the symlinks, seeds `settings.json`, installs claude/uv/rtk, clones `afk`,
and reinstalls the plugins. Run it before the first `claude` launch.

From this public copy, by hand:
1. Put `agents/`, `skills/`, `hooks/` and `claude/` under `~/.agents/` and recreate the symlinks above.
2. `claude login`; reinstall the plugins listed in `settings.json` (`claude plugin install …`).
3. Install `rtk`, `graphify` (`uv tool install graphifyy`) and `afk` (separate repo).
4. Source [`shell/bashrc-claude.sh`](shell/bashrc-claude.sh) from `~/.bashrc`.

## Persistent memory

Each project has its memory under `~/.claude/projects/<slug>/memory/`
(`MEMORY.md` as the index + one file per fact). **Not versioned here**: it is work
content, not config.

The [`evolve`](skills/evolve/SKILL.md) skill is the loop that rereads these
memories and suggests turning what keeps coming back into a skill.
