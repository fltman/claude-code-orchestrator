# Claude Code Orchestrator (W.O.P.R.)

[![Support me on Patreon](https://img.shields.io/badge/Patreon-Support%20my%20work-FF424D?style=flat&logo=patreon&logoColor=white)](https://www.patreon.com/AndersBjarby)

A retro, WarGames/Matrix-themed terminal UI for orchestrating multiple Claude Code agents, each running in its own `tmux` session. Deploy agents into project directories, send them commands, broadcast to all of them, watch their output, and tear them down — all from one dramatic command console.

## Features

- Deploy a Claude Code agent into any directory (each gets a Matrix codename and its own tmux session)
- Send commands to a single agent or broadcast to the whole fleet
- Attach to ("jack into") an agent's live session, or capture its recent output
- Terminate individual agents or purge them all
- Typewriter effects, loading bars and ASCII art for full retro-terminal flavor

## Usage

Requires `tmux` and the `claude` CLI on your `PATH`.

```bash
python3 claude_orchestrator_tmux.py
```

Then use the menu, or the shortcuts: `deploy agent in <dir>` to spawn one and `AGENT: <message>` to send a command to a named agent.

## Tech

Single-file Python 3 script using only the standard library; drives Claude Code agents through `tmux`.
