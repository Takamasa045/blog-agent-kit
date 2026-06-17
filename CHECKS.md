# CHECKS

## Repo Development

- CLI commands work without third-party dependencies.
- `python3 scripts/observe_truth.py --json` works.
- Agent operating files exist: `VISION.md`, `AGENTS.md`, `CLAUDE.md`, `CHECKS.md`, `LOOPS.md`, `MEMORY.md`, and `NEXT_ACTIONS.md`.
- Templates do not include private style, private paths, or service assumptions.
- Tests pass with `unittest`.

## Article Workspace

- `brief.yml` exists.
- Required output files exist.
- `draft.md` has an H1 title.
- `handoff.json.title` matches the H1 title.
- Claims and sources are present.
- Web research limitations are explicit when needed.
- `image_prompts.md` includes title image prompts for both 16:9 and 5:2.
- Section illustration prompts avoid in-image text.
- `x_posts.md` includes 5 draft posts for manual review.

## External Actions

- Do not publish.
- Do not post to social media.
- Do not email.
- Do not update a CMS.
- Do not upload generated images or assets unless explicitly requested.
- Do not invent citations or statistics.

## Public OSS Safety

- Do not include private paths, private names, API keys, tokens, or secrets.
- Do not include generated drafts from private topics.
- Do not describe publication as completed unless a human explicitly confirms it.
