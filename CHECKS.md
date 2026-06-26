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
- `outline.md` has a Reader Entry section with reader, problem, promise, and next step.
- If a named writing style is specified, `draft.md` satisfies the concrete style requirements captured in the brief, such as required opening phrase, tone, and reader level.
- For itopan-style Japanese note/blog articles, confirm the `itopan-style` skill was used, including article log review and style reference application.
- For itopan-style Japanese note/blog articles, `draft.md` includes `どうも、いとぱんです。` near the opening and uses the expected short-paragraph, beginner-friendly tone.
- If a target character count is specified, verify real body text length instead of raw Markdown length.
- For itopan-style Japanese note/blog articles without a different user target, verify about 3000 real body characters.
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
