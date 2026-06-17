# AGENTS.md

This repository is an OSS template and CLI for blog article generation workspaces.

## Codex Behavior

- Keep changes small and focused.
- Use `rg` for search.
- Keep the CLI dependency-free unless there is a strong reason.
- Do not add CMS, social posting, email, Discord, OpenClaw, or hosted-service assumptions by default.
- Article generation is local-file generation. Publishing is out of scope unless explicitly requested.

## Verification

```bash
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
- `AGENTS.md`
- `CLAUDE.md`
- `.claude/skills/blog-article-generate/SKILL.md`
