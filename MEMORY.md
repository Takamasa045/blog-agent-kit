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
brief -> outline -> research pack -> draft -> claims table -> sources -> handoff -> image prompts -> X posts -> review rounds -> iteration log
```

- Material claims need sources. If current web research is unavailable, the
  limitation must be stated in the article artifacts.
- Article outlines should define the reader entry before drafting: reader,
  problem, promise, article role, title hook, and next step.
- Article topics should run two local review/brush-up rounds after the first
  complete draft. Use a second-agent prompt, record findings in
  `review_round_1.md` and `review_round_2.md`, and record applied changes in
  `iteration_log.md`.
- The project should stay dependency-free unless a concrete feature requires a
  dependency and the benefit is larger than the maintenance cost.
- Docs must describe repeatable workflows, not private operational habits.
- OpenClaw integration is an optional orchestration recipe. It must call the
  local CLI and stop at review artifacts; it must not become a default
  dependency or publishing path.
- Remote OpenClaw workspaces can be pulled back with `blog-agent sync`, but the
  remote host/path must be supplied explicitly. The CLI must not hard-code a
  private VPS or channel.

## Stable Agent Loop

```text
Goal -> Observe -> Plan -> Act -> Verify -> Record -> Stop
```

Use `scripts/observe_truth.py` for the observe step when working in this repo.
Record durable decisions here only when they should guide future agents.

## Article Review Loop

```text
DISCOVER -> PLAN -> EXECUTE -> VERIFY -> ITERATE
```

Run the article review loop twice after generation. Keep the loop local-only:
the reviewer agent may edit topic files and write review notes, but must not
publish, post, email, upload, or update a CMS.
