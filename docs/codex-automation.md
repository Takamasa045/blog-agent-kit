# Codex Automation

Use Codex app automations to continue local article work.

## Suggested Prompt

```text
Read this Blog Agent Kit workspace. Follow VISION.md, AGENTS.md, CHECKS.md, LOOPS.md, MEMORY.md, and NEXT_ACTIONS.md.
Run python3 scripts/observe_truth.py --json.
Find the newest incomplete topic under topics/.
Run blog-agent prompt and blog-agent check.
Generate or revise local output files only, including image prompts and X post drafts.
Report completed files, warnings, and next human review actions.
Do not publish, post, email, upload assets, update a CMS, or invent citations.
```

## Good Cadence

- Daily: continue the newest incomplete draft.
- Weekly: create a report of topics waiting for human review.
- Before publishing: run check and package, then stop for human review.
