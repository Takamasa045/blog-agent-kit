# Claude Scheduled Tasks

Blog Agent Kit can be used with Claude Desktop scheduled tasks, Claude Code, and Claude Routines.

## Local Desktop Task

Use a local scheduled task when the article workspace is on your machine.

```text
Read VISION.md, CLAUDE.md, CHECKS.md, LOOPS.md, MEMORY.md, NEXT_ACTIONS.md, and the topic brief. Run python3 scripts/observe_truth.py --json. Find the newest incomplete topic under topics/. Generate or revise local output files only, including Reader Entry, image prompts, X post drafts, and two local review rounds. Run blog-agent check. Report completed files, warnings, and next human review actions. Do not publish, post, email, upload assets, update a CMS, or invent citations.
```

## Cloud Routine

Use cloud routines only when the topic files and sources are available in cloud context.

## Publishing

Publishing is intentionally not part of the default task. Keep publication behind human review.
