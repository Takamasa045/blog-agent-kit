# LOOPS

## Development Loop

```text
Goal -> Observe -> Plan -> Act -> Verify -> Record -> Stop
```

1. Read `VISION.md`, `MEMORY.md`, and `NEXT_ACTIONS.md`.
2. Run `python3 scripts/observe_truth.py --json` for a read-only snapshot.
3. Patch the smallest relevant surface.
4. Run the closest verification command from `CHECKS.md`.
5. Record durable decisions in `MEMORY.md` only when they should guide future agents.

## Article Loop

```text
Brief -> Plan -> Research -> Draft -> Verify -> Assets -> Package -> Stop
```

1. Create a topic with `blog-agent new`.
2. Ask Codex or Claude to follow the generated `agent-prompt.md`.
3. Generate `output/image_prompts.md` with 16:9 and 5:2 title-image prompts, plus no-text section illustration prompts.
4. Generate `output/x_posts.md` with 5 draft X posts for manual review.
5. Run `blog-agent check`.
6. Fix warnings.
7. Run `blog-agent package --write` for human review.

## Stop Conditions

- Current facts are required and browsing is unavailable.
- Sources are not strong enough for the article's claims.
- The task requires publication or external side effects.
- Image generation tools are unavailable; keep complete prompts and stop.
- The task would put private paths, private names, API keys, or secrets into the OSS template.
