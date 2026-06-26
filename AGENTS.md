# AGENTS.md

This repository is a local template and CLI for blog article generation workspaces.

## Read Order

1. `VISION.md` for purpose, boundaries, and done state.
2. `MEMORY.md` for durable project decisions.
3. `LOOPS.md` for the repeatable workflow.
4. `CHECKS.md` for verification and safety gates.
5. `NEXT_ACTIONS.md` for the current forward path.

## Codex Behavior

- Keep changes small and focused.
- Use `rg` for search.
- Keep the CLI dependency-free unless there is a strong reason.
- Do not add CMS, social posting, email, Discord, OpenClaw, or hosted-service assumptions by default.
- Article generation is local-file generation. Publishing is out of scope unless explicitly requested.
- For article topics, define a Reader Entry before drafting: reader, problem, promise, article role, title hook, and next step.
- When the user or brief names a writing style, read that style's instructions and turn concrete requirements such as opening phrase, tone, and target character count into explicit done conditions before drafting.
- For itopan-style Japanese note/blog articles, use the `itopan-style` skill first. Apply its required read order, article log, opening phrase, tone, short paragraph rhythm, and real-body character target. Default to `どうも、いとぱんです。` near the opening and about 3000 real body characters unless the user gives a different target.
- For article topics, prepare local image-generation prompts for 16:9 and 5:2 title images, plus no-text section illustrations.
- Draft X posts locally in `output/x_posts.md`; do not post them or assume an account connection.

## Verification

```bash
python3 scripts/observe_truth.py --json
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'
PYTHONPATH=src python3 -m blog_agent_kit.cli init --root /tmp/blog-demo --force
PYTHONPATH=src python3 -m blog_agent_kit.cli new "Example article" --root /tmp/blog-demo --date 2026-06-17
PYTHONPATH=src python3 -m blog_agent_kit.cli check --topic /tmp/blog-demo/topics/2026-06-17_example-article
```

## Stable Surface

- `blog-agent init`
- `blog-agent new`
- `blog-agent prompt`
- `blog-agent check`
- `blog-agent status`
- `blog-agent package`
- `VISION.md`
- `AGENTS.md`
- `CLAUDE.md`
- `MEMORY.md`
- `CHECKS.md`
- `LOOPS.md`
- `NEXT_ACTIONS.md`
- `scripts/observe_truth.py`
- `.claude/skills/blog-article-generate/SKILL.md`
