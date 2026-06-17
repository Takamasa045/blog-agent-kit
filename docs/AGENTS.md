# AGENTS.md

These instructions apply to files under `docs/`.

## Purpose

The docs folder explains how Blog Agent Kit is operated by Codex, Claude, and
human maintainers. It is public OSS documentation, not a private runbook.

## Editing Rules

- Keep examples local-first.
- Do not add CMS, social posting, email, Discord, or hosted scheduler
  assumptions to the default workflow.
- Do not include private paths, private names, API keys, secrets, or generated
  drafts from private topics.
- Prefer short prompts that point agents to `VISION.md`, `AGENTS.md`,
  `CLAUDE.md`, `CHECKS.md`, `LOOPS.md`, `MEMORY.md`, and `NEXT_ACTIONS.md`.
- Keep publication behind explicit human review.

## Checks

Before finalizing docs changes:

```bash
python3 scripts/observe_truth.py --json
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'
```

