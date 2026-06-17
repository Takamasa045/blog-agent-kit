# CLAUDE.md

Blog Agent Kit is local-first. It does not publish, post, email, or update a CMS.

## Claude Instructions

- Use local files as the source of truth.
- For article workspaces, read `STYLE.md`, `CHECKS.md`, `LOOPS.md`, and the topic `brief.yml`.
- Generate local files under `output/`.
- Include image-generation prompts for 16:9 and 5:2 title images, plus no-text section illustrations.
- Include 5 draft X posts in `output/x_posts.md` for manual review.
- Run `blog-agent check --topic <topic>` before final status.
- Do not invent citations, quotes, URLs, statistics, or publication status.
- Mark web research limitations clearly when browsing is unavailable.

## Scheduled Task Prompt

```text
Find the newest incomplete topic under topics/. Follow CLAUDE.md, STYLE.md, CHECKS.md, LOOPS.md, and the topic brief. Generate or revise local output files only, including image prompts and X post drafts. Run blog-agent check. Report completed files, warnings, and next human review actions. Do not publish, post, email, update a CMS, or invent citations.
```
