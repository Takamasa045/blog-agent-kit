# LOOPS

## Development Loop

```text
Goal -> Inspect -> Patch -> Test -> Document -> Stop
```

## Article Loop

```text
Brief -> Plan -> Research -> Draft -> Verify -> Package -> Stop
```

1. Create a topic with `blog-agent new`.
2. Ask Codex or Claude to follow the generated `agent-prompt.md`.
3. Run `blog-agent check`.
4. Fix warnings.
5. Run `blog-agent package --write` for human review.

## Stop Conditions

- Current facts are required and browsing is unavailable.
- Sources are not strong enough for the article's claims.
- The task requires publication or external side effects.
