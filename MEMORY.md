# MEMORY

Durable project decisions for future agents. Keep this file public-safe and
free of private topics, private paths, secrets, tokens, or customer data.

## Decisions

- Blog Agent Kit is local-first. The CLI scaffolds files; the agent writes and
  revises files locally.
- Publishing is intentionally out of scope. `package` prepares review material
  but does not post, email, or update a CMS.
- The article artifact chain is:

```text
brief -> outline -> research pack -> draft -> claims table -> sources -> handoff -> image prompts -> X posts
```

- Material claims need sources. If current web research is unavailable, the
  limitation must be stated in the article artifacts.
- The project should stay dependency-free unless a concrete feature requires a
  dependency and the benefit is larger than the maintenance cost.
- Docs must describe repeatable workflows, not private operational habits.

## Stable Agent Loop

```text
Goal -> Observe -> Plan -> Act -> Verify -> Record -> Stop
```

Use `scripts/observe_truth.py` for the observe step when working in this repo.
Record durable decisions here only when they should guide future agents.
