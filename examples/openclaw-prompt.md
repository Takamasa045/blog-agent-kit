# OpenClaw Prompt

```text
Read this Blog Agent Kit workspace. Follow VISION.md, AGENTS.md, CHECKS.md,
LOOPS.md, MEMORY.md, and NEXT_ACTIONS.md.

Run python3 scripts/observe_truth.py --json if scripts/observe_truth.py exists.
If it does not exist, continue with blog-agent status --json.

If I gave a new article theme, create a topic with blog-agent new.
Otherwise, run blog-agent status --json and choose the newest incomplete topic.

Run blog-agent prompt --topic <topic>. Generate or revise local output files
only: outline, research pack, draft, claims table, sources, handoff, image
prompts, and X post drafts.

Run blog-agent check --topic <topic> --json.
Run blog-agent package --topic <topic> --write when a review package is useful.

Report the topic path, changed files, warnings, review package path, and next
human review actions. Do not publish, post, email, upload assets, update a CMS,
or invent citations, quotes, URLs, statistics, or publication status.

If this ran on a remote OpenClaw workspace, tell me I can pull the result back
with blog-agent sync from my local Blog Agent Kit checkout.
```

## Short Requests

With an optional Discord mention:

```text
<@BOT_USER_ID> 最新の未完了記事を進めて。公開はしないで。
```

Without a mention in a dedicated article channel:

```text
最新の未完了記事を進めて。公開はしないで。
```

```text
このテーマでtopicを作って、レビュー用packageまで作って止めて。
```

```text
checkの警告を見て、ローカルファイルだけ直して。投稿はしないで。
```
