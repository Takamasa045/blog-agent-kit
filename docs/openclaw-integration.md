# OpenClaw Integration

Use OpenClaw as an optional local orchestrator for Blog Agent Kit workspaces.
OpenClaw should remember the repeatable steps; Blog Agent Kit remains the
source of truth for local article files.

This integration does not add an OpenClaw dependency to the CLI and does not
require a VPS, hosted scheduler, CMS, social account, email account, or LLM API.

## Goal

Let a human give a short instruction such as:

```text
最新の未完了記事を進めて。公開はしないで。
```

OpenClaw then runs the same local loop every time:

```text
Observe -> Select Topic -> Prompt Agent -> Check -> Package -> Report -> Stop
```

## Discord Mention Mode

If the workspace is wired to a Discord channel, the channel may accept both
plain requests and bot mentions. Keep mention handling optional unless the
operator wants every message in the channel ignored by default.

Example mention request:

```text
<@BOT_USER_ID> 最新の未完了記事を進めて。公開はしないで。
```

If Discord autocomplete does not show the bot name, use the raw bot user ID
mention string supplied by the operator.

## Required Access

- A local Blog Agent Kit workspace.
- Shell access in that workspace.
- A coding agent that can edit local files.

No credentials are required for the default workflow.

Use `blog-agent ...` when the CLI is installed. In a source checkout without an
installed CLI, use this equivalent form:

```bash
PYTHONPATH=src python3 -m blog_agent_kit.cli ...
```

## Default Runbook

1. Observe the workspace state.

   ```bash
   if [ -f scripts/observe_truth.py ]; then
     python3 scripts/observe_truth.py --json
   fi
   ```

   Generated article workspaces may not include `scripts/observe_truth.py`; in
   that case, continue with `blog-agent status --json`.

2. Select a topic.

   If the user gives a new theme, create a topic:

   ```bash
   blog-agent new "Article theme"
   ```

   Otherwise, inspect existing topics and choose the newest incomplete one:

   ```bash
   blog-agent status --json
   ```

3. Prepare the topic prompt.

   ```bash
   blog-agent prompt --topic topics/YYYY-MM-DD_slug
   ```

4. Ask the coding agent to generate or revise local files only.

   Required output files are:

   - `output/outline.md`
   - `output/research_pack.md`
   - `output/draft.md`
   - `output/claims_table.md`
   - `output/sources.md`
   - `output/handoff.json`
   - `output/image_prompts.md`
   - `output/x_posts.md`

5. Check the topic.

   ```bash
   blog-agent check --topic topics/YYYY-MM-DD_slug --json
   ```

6. Write a review package for human review.

   ```bash
   blog-agent package --topic topics/YYYY-MM-DD_slug --write
   ```

7. Report and stop.

   The report should include:

   - selected topic path
   - files completed or changed
   - check warnings
   - review package path, if written
   - confirmation that no external action was performed

## Stop Gates

Stop and report instead of continuing when:

- Current web facts are required but browsing is unavailable.
- Sources are not strong enough for material claims.
- `blog-agent check` reports warnings that need human judgment.
- The user asks for publishing, posting, emailing, uploading, or CMS updates
  without explicit confirmation.
- The task would require private paths, private names, API keys, tokens, or
  secrets in the workspace.

## OpenClaw Prompt

Use this as the orchestration prompt:

```text
Read this Blog Agent Kit workspace. Follow VISION.md, AGENTS.md, CHECKS.md,
LOOPS.md, MEMORY.md, and NEXT_ACTIONS.md.

Run python3 scripts/observe_truth.py --json if scripts/observe_truth.py exists.
If it does not exist, continue with blog-agent status --json.

If the user gave a new article theme, create a topic with blog-agent new.
Otherwise, run blog-agent status --json and choose the newest incomplete topic.

Run blog-agent prompt --topic <topic>. Generate or revise local output files
only: outline, research pack, draft, claims table, sources, handoff, image
prompts, and X post drafts.

Run blog-agent check --topic <topic> --json.
Run blog-agent package --topic <topic> --write when a review package is useful.

Report the topic path, changed files, warnings, review package path, and next
human review actions. Do not publish, post, email, upload assets, update a CMS,
or invent citations, quotes, URLs, statistics, or publication status.
```

## Result Shape

OpenClaw should keep a compact run summary like this:

```json
{
  "topic": "topics/YYYY-MM-DD_slug",
  "changed_files": [],
  "check_warnings": [],
  "review_package": "topics/YYYY-MM-DD_slug/output/review_package.md",
  "external_actions_performed": false,
  "next_human_actions": []
}
```

## Pull Results Back

When OpenClaw runs on another machine, keep the generated topic as a normal Blog
Agent Kit topic and pull it back explicitly:

```bash
blog-agent sync --source host:/path/to/blog-agent-kit --topic latest --root .
```

The sync source is another Blog Agent Kit workspace root containing `topics/`.
The source may be a local path or an SSH-style path such as
`host:/path/to/blog-agent-kit`.

Default behavior is conservative:

- `--topic latest` pulls only the newest topic.
- `--topic all` pulls all topics.
- Existing local files are not overwritten.
- `--dry-run` previews copied files.
- `--force` allows the remote topic to overwrite local copies.

This is still a local-file workflow. Pulling a topic does not publish to note,
post to social media, email anyone, upload assets, or update a CMS.
