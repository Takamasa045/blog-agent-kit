---
name: blog-article-generate
description: Generate or revise a Blog Agent Kit topic into outline, research pack, draft, claims table, sources, and handoff files.
---

# Blog Article Generate

Use this skill when the user asks Claude to generate, continue, check, or package a blog article in a Blog Agent Kit workspace.

## Steps

1. Read `CLAUDE.md`, `STYLE.md`, `CHECKS.md`, `LOOPS.md`, and the topic `brief.yml`.
2. Run:

```bash
blog-agent prompt --topic <topic>
```

3. Generate or revise:

- `output/outline.md`
- `output/research_pack.md`
- `output/draft.md`
- `output/claims_table.md`
- `output/sources.md`
- `output/handoff.json`
- `output/image_prompts.md`
- `output/x_posts.md`
- `output/review_round_1.md`
- `output/review_round_2.md`
- `output/iteration_log.md`

Before drafting, make sure `output/outline.md` includes a Reader Entry:
reader, problem, promise, article role, title hook, and next step.

After the first complete draft, use:

```bash
blog-agent review-prompt --topic <topic>
```

Run two local review and brush-up rounds before final completion.

4. Run:

```bash
blog-agent check --topic <topic>
```

5. Report completed files, warnings, and next human review actions.

## Hard Rules

- Do not publish.
- Do not post to social media.
- Do not email.
- Do not update a CMS.
- Do not lead with jargon or internal tool names unless the reader problem and value are clear first.
- Do not invent citations, quotes, URLs, statistics, or publication status.
- If browsing is unavailable, state that limitation in `research_pack.md`.
