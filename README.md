# Blog Agent Kit

Local-first blog article generation workspace for Codex and Claude.

Blog Agent Kit gives AI coding agents a repeatable article pipeline:

```text
brief -> outline -> research pack -> draft -> claims table -> sources -> handoff -> image prompts -> X posts -> review rounds -> iteration log
```

It does not require an LLM API, CMS, Discord, Slack, OpenClaw, or a VPS. Codex or Claude writes and revises the article inside local files; the CLI scaffolds topics and checks whether the required artifacts are complete enough to review.

## What It Creates

Each article topic lives under `topics/YYYY-MM-DD_slug/`:

```text
brief.yml              # Article request and constraints
agent-prompt.md        # Prompt for Codex / Claude
reviewer-prompt.md     # Prompt for a second-agent review loop
output/outline.md      # Titles and section plan
output/research_pack.md
output/draft.md
output/claims_table.md
output/sources.md
output/handoff.json    # Structured metadata for downstream tools
output/image_prompts.md # Cover and section illustration prompts
output/x_posts.md       # Draft X posts for manual review
output/review_round_1.md
output/review_round_2.md
output/iteration_log.md
```

## Quick Start

```bash
python3 -m pip install -e .
blog-agent init --root ./my-blog-workspace
blog-agent new "How local AI agents help editorial teams" --root ./my-blog-workspace
blog-agent prompt --topic ./my-blog-workspace/topics/2026-06-17_how-local-ai-agents-help-editorial-teams
blog-agent review-prompt --topic ./my-blog-workspace/topics/2026-06-17_how-local-ai-agents-help-editorial-teams
blog-agent check --topic ./my-blog-workspace/topics/2026-06-17_how-local-ai-agents-help-editorial-teams
```

For one-off use without installing:

```bash
PYTHONPATH=src python3 -m blog_agent_kit.cli init --root /tmp/blog-workspace
PYTHONPATH=src python3 -m blog_agent_kit.cli new "My article theme" --root /tmp/blog-workspace
```

## Agent Contract

Codex or Claude should:

- read `brief.yml`, `STYLE.md`, `CHECKS.md`, and `LOOPS.md`
- follow the generated Itopan-style `STYLE.md` for Japanese articles: short line breaks, beginner-friendly explanations, direct/polite ending mix, restrained emoji headings, and concrete metaphors
- define the Reader Entry before drafting: reader, problem, promise, article role, title hook, and next step
- produce all required files under `output/`
- prepare title-image prompts for both 16:9 and 5:2, plus no-text section illustration prompts
- prepare 5 draft X posts, but never post them automatically
- use `reviewer-prompt.md` for a second-agent review loop and run two local brush-up rounds
- separate facts, inference, opinion, and speculation
- cite sources for material claims
- mark web research limitations explicitly when browsing is unavailable
- avoid publishing, posting, emailing, or CMS changes unless a human explicitly asks

## Commands

```bash
blog-agent init
blog-agent new "theme"
blog-agent prompt --topic topics/...
blog-agent review-prompt --topic topics/...
blog-agent check --topic topics/...
blog-agent status
blog-agent package --topic topics/... --write
```

`package` creates a local publish-review bundle. It does not publish.

## Automation

Codex app automation or Claude scheduled tasks can run:

```text
Read this Blog Agent Kit workspace. Follow AGENTS.md or CLAUDE.md.
Find the newest topic with incomplete outputs.
Run blog-agent prompt, blog-agent review-prompt, and blog-agent check.
If files are missing, generate or revise them locally.
Include image prompts and X post drafts.
Use the reviewer prompt for two local review and brush-up rounds.
Do not publish, post, email, upload assets, or invent citations.
```

## VPS で重い成果物を作る場合

動画、画像、ZIP などの大きい成果物を VPS 側で作る場合は、Blog Agent Kit の標準フローに VPS 前提を混ぜず、任意手順として `docs/vps-artifact-workflow.md` を使います。

基本は、GitHub 経由で VPS 上に clone を作り、VPS 側の `output/artifacts/<run-id>/` に成果物を出し、ローカル側から `scripts/pull-remote-artifacts.sh` で `output/remote-artifacts/<run-id>/` へ回収します。

OpenClaw に記事作成を頼み、Hermes が回収済み成果物を read-only で読む場合は `docs/openclaw-hermes-operations.md` を使います。

## Development

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'
PYTHONPATH=src python3 -m blog_agent_kit.cli init --root /tmp/blog-demo --force
PYTHONPATH=src python3 -m blog_agent_kit.cli new "Example article" --root /tmp/blog-demo --date 2026-06-17
PYTHONPATH=src python3 -m blog_agent_kit.cli review-prompt --topic /tmp/blog-demo/topics/2026-06-17_example-article
```

## License

MIT
