# Agent Prompt

Follow `brief.yml`, workspace `STYLE.md`, `CHECKS.md`, and `LOOPS.md`.

Write all required files under `output/`.

Include:

- `output/image_prompts.md` with 16:9 and 5:2 title-image prompts, plus no-text section illustration prompts.
- `output/x_posts.md` with 5 draft X posts for manual review.

Rules:

- In `output/outline.md`, start with a Reader Entry section: reader, problem, promise, article role, title hook, and next step.
- Lead titles and openings from reader problem/value or a concrete story before jargon or internal tool names.
- Choose one article role: practical guide, experiment story, or worldview essay; keep the CTA aligned.
- After the first complete draft, hand off to a second agent with `blog-agent review-prompt --topic <topic>` for two review and brush-up rounds.

Do not publish, post, email, update a CMS, or invent citations.
