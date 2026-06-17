# VISION

Blog Agent Kit is a local-first article workspace kit for coding agents.

It helps Codex, Claude, and similar agents create reviewable article artifacts
inside local files:

```text
brief -> outline -> research pack -> draft -> claims table -> sources -> handoff -> image prompts -> X posts
```

## Mission

- Make article generation repeatable without requiring a hosted service.
- Give agents a clear contract for what to read, write, verify, and stop on.
- Keep publishing behind human review.
- Keep the OSS template safe to share publicly.

## Source of Truth

- This repository is the template and CLI source of truth.
- Generated article workspaces use their own local files as the article truth.
- Topic output files are review artifacts, not publication events.
- `README.md`, `AGENTS.md`, `CLAUDE.md`, `CHECKS.md`, `LOOPS.md`,
  `MEMORY.md`, and `NEXT_ACTIONS.md` are the operating surface for agents.

## Success State

A fresh agent should be able to:

1. Read the operating surface.
2. Inspect the current repo or article workspace state.
3. Choose the next local article or repo maintenance task.
4. Generate or revise only local files.
5. Run the closest verification command.
6. Report what changed, what remains, and where human review is required.

## Non-Goals

- CMS publishing.
- Social posting.
- Email or Discord sending.
- Hosted schedulers.
- Private style profiles or private source scraping.
- Invented citations, statistics, quotes, URLs, or publication status.

## Agent Operating Surface

- `VISION.md`: why this repo exists and what done means.
- `README.md`: human-facing setup and command overview.
- `AGENTS.md`: Codex-facing working rules.
- `CLAUDE.md`: Claude-facing working rules.
- `LOOPS.md`: repeatable workflows and stop conditions.
- `CHECKS.md`: verification and safety gates.
- `MEMORY.md`: durable decisions future agents should preserve.
- `NEXT_ACTIONS.md`: current forward path.
- `scripts/observe_truth.py`: read-only state snapshot for agents.
