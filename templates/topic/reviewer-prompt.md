# Reviewer Prompt

Act as a second agent. Read `brief.yml`, workspace `STYLE.md`, `CHECKS.md`,
`LOOPS.md`, and the current files under `output/`.

Run exactly two local improvement rounds:

```text
DISCOVER -> PLAN -> EXECUTE -> VERIFY -> ITERATE
```

For each round:

1. DISCOVER: identify weak points in reader fit, title/opening, structure, claims, sources, style, handoff metadata, image prompts, and X posts.
2. PLAN: choose the smallest concrete set of fixes for this round.
3. EXECUTE: revise local output files only.
4. VERIFY: check the revised files against `CHECKS.md`, source limits, and the brief.
5. ITERATE: write the review record and change summary.

Write:

- round 1 findings to `output/review_round_1.md`
- round 2 findings to `output/review_round_2.md`
- applied changes from both rounds to `output/iteration_log.md`

Rules:

- Do not publish, post, email, upload assets, or update a CMS.
- Do not invent citations, quotes, URLs, statistics, or publication status.
- If a claim cannot be verified, weaken it or mark the limitation.
- Preserve useful previous work; only revise what improves the article.
- After round 2, run `blog-agent check --topic <topic>`, then `blog-agent package --topic <topic> --write`.
