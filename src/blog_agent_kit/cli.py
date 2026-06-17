from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REQUIRED_OUTPUTS = [
    "outline.md",
    "research_pack.md",
    "draft.md",
    "claims_table.md",
    "sources.md",
    "handoff.json",
    "image_prompts.md",
    "x_posts.md",
]


@dataclass
class TopicStatus:
    topic: str
    brief_exists: bool
    output_exists: bool
    missing_outputs: list[str]
    warnings: list[str]
    title: str | None = None


def today() -> str:
    return datetime.now(UTC).date().isoformat()


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")
    if slug:
        return slug[:72].strip("-")
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:8]
    return f"topic-{digest}"


def write_text(path: Path, text: str, *, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def template_workspace_readme() -> str:
    return """# Blog Workspace

This workspace uses Blog Agent Kit.

Use the local files as the source of truth:

- `STYLE.md` for editorial defaults
- `CHECKS.md` for quality gates
- `LOOPS.md` for the generation workflow
- `topics/*/brief.yml` for each article request
- `topics/*/output/image_prompts.md` for cover and section image generation prompts
- `topics/*/output/x_posts.md` for draft X posts

Agents may draft and revise local files. They must not publish, post, email, or change a CMS without explicit human approval.
"""


def template_style() -> str:
    return """# STYLE

## いとぱんスタイル

日本語のブログ記事は、いとぱんスタイルで書く。

- 初心者が「自分にもできそう」と感じるように、やさしく背中を押す。
- 専門用語はかみ砕き、身近なたとえで理解を助ける。
- 情報の正確性を保ちつつ、親しみやすさを両立する。
- 一人称は `僕`、二人称は `あなた` を使う。
- 文末は `だ。/である。` の言い切りを6割、`です/ます` を4割くらいで混ぜる。
- `大丈夫`、`僕も最初は...`、`...じゃないか` など、不安をほどく言葉を自然に入れる。
- 誇張、説教、根拠のない断定、作った自信は避ける。

## リズム

- 1-2文で改行する。
- 1段落は長くても4行以内にする。
- 段落の間には必ず空行を入れる。
- 長い説明は `###` 見出しで細かく区切る。
- `つまり`、`要は`、`言い換えると` を使って定期的に噛み砕く。

## 記事構成

1. あいさつと導入: 共感、問題提起、最近知った話。
2. 結論の一言: 要点を先に出す。
3. たとえ話: 日常の具体物や場面で噛み砕く。
4. 本編: ステップ、仕組み、分類で整理する。
5. 深掘り: 具体例、表、反論、実践方法を入れる。
6. 任意のつまずきや失敗談: 記事のトーンに合う場合だけ入れる。
7. まとめ: 箇条書きと励ましで締める。
8. CTA: 必要に応じてスキ、コメント、フォローを促す。
9. 任意の P.S.: 次回予告や補足を書く。

FAQ/Q&A は、brief で明示されない限り追加しない。

## 見出しと装飾

- 絵文字は主に H2 見出しで使う。
- 1記事で使う絵文字は3-6種類に抑える。
- 絵文字の連打を区切り線や装飾として使わない。
- タイトルの絵文字は0-1個まで。入れるなら末尾寄せを基本にする。
- 比較は表、手順は番号付きリストで整理する。

## 引用と出典

- 重要な事実主張には出典を付ける。
- Web 調査ができない場合は、`research_pack.md` に調査制約を明記する。
- 引用、出典名、URL、統計を作らない。
- 一次情報、公式ドキュメント、論文、信頼できる報道を優先する。
- 本文中の出典表記は `（出典名）` のように簡潔に示す。

## 高リスクなテーマ

健康、金融、法律、政治、アイデンティティ、宗教、安全に関わるテーマでは:

- 複数の見方を示す。
- 断定を弱める。
- 範囲と限界を明記する。
- 個別診断や強い助言を避ける。
"""


def template_checks() -> str:
    return """# CHECKS

## Required Files

- `output/outline.md`
- `output/research_pack.md`
- `output/draft.md`
- `output/claims_table.md`
- `output/sources.md`
- `output/handoff.json`
- `output/image_prompts.md`
- `output/x_posts.md`

## Quality Gates

- The draft starts with one `# Title`.
- `handoff.json.title` matches the draft title.
- Major claims appear in `claims_table.md`.
- Sources are listed in `sources.md`.
- Facts, inference, opinion, and speculation are not mixed.
- Web research limitations are explicit when browsing is unavailable.
- `image_prompts.md` includes title-image prompts for both 16:9 and 5:2.
- Section illustration prompts do not ask for in-image text.
- `x_posts.md` includes 5 single-post drafts, each intended to stay under 280 characters.

## External Actions

- Do not publish.
- Do not post to social media.
- Do not email.
- Do not update a CMS.
- Do not invent citations, quotes, URLs, or statistics.
"""


def template_loops() -> str:
    return """# LOOPS

## Article Generation

```text
Brief -> Plan -> Research -> Draft -> Verify -> Assets -> Package -> Stop
```

1. Read `brief.yml`, `STYLE.md`, and `CHECKS.md`.
2. Write `output/outline.md` with title candidates and section plan.
3. Write `output/research_pack.md` with terms, evidence, open questions, and search queries.
4. Write `output/draft.md`.
5. Write `output/claims_table.md` and `output/sources.md`.
6. Write `output/handoff.json`.
7. Write `output/image_prompts.md`:
   - title image prompt for 16:9
   - title image prompt for 5:2
   - one no-text section illustration prompt per H2
8. Write `output/x_posts.md` with 5 draft X posts.
9. Run `blog-agent check --topic <topic>`.

## Stop Conditions

- The article needs current facts and browsing is unavailable.
- The topic is high-risk and sources are insufficient.
- The user asks for publishing or external posting without explicit confirmation.
- The article would require invented quotes, citations, links, or statistics.
- Image generation is unavailable; keep complete prompts in `image_prompts.md` and stop.
"""


def template_agents() -> str:
    return """# AGENTS.md

This is a Blog Agent Kit workspace for Codex.

## Contract

- Read `STYLE.md`, `CHECKS.md`, `LOOPS.md`, and the topic `brief.yml`.
- Generate or revise local files only.
- Use `blog-agent prompt --topic <topic>` before drafting.
- Use `blog-agent check --topic <topic>` before reporting completion.
- Do not publish, post, email, update a CMS, or invent citations.
- Draft image prompts and X posts locally; do not post to X or upload assets unless explicitly asked.
- If browsing is unavailable, say so in `research_pack.md` and list verification queries.

## Default Prompt

Find the newest topic under `topics/` with missing or incomplete outputs. Follow the brief and generate the required files under `output/`, including image prompts and X post drafts. Separate facts, inference, opinion, and speculation. Do not perform external actions.
"""


def template_claude() -> str:
    return """# CLAUDE.md

This is a Blog Agent Kit workspace for Claude Code and Claude Desktop scheduled tasks.

## Contract

- Read `STYLE.md`, `CHECKS.md`, `LOOPS.md`, and the topic `brief.yml`.
- Generate or revise local files only.
- Run `blog-agent check --topic <topic>` before final status.
- Do not publish, post, email, update a CMS, or invent citations.
- Draft image prompts and X posts locally; do not post to X or upload assets unless explicitly asked.
- Mark web research limitations explicitly when browsing is unavailable.

## Scheduled Task Prompt

Find the newest incomplete topic under `topics/`. Generate or revise the required output files, including image prompts and X post drafts. Return a short status with completed files, warnings, and next human review actions. Do not perform external actions.
"""


def template_next_actions() -> str:
    return """# NEXT_ACTIONS

- Create a topic with `blog-agent new "Theme"`.
- Ask Codex or Claude to generate the missing outputs.
- Run `blog-agent check --topic topics/...`.
- Generate title images from `output/image_prompts.md` when image tools are available.
- Review `output/x_posts.md` before posting manually.
- Review the draft before publishing anywhere.
"""


def template_brief(theme: str, audience: str, goal: str, tone: str, length: str) -> str:
    return f"""theme: "{theme}"
audience: "{audience}"
goal: "{goal}"
tone: "{tone}"
length: "{length}"
must_include:
  - ""
avoid:
  - ""
preferred_sources:
  - ""
blocked_sources:
  - ""
context: |
  Add background notes here.
"""


def template_agent_prompt(theme: str) -> str:
    return f"""# Agent Prompt

Generate a blog article for this topic:

> {theme}

Follow `brief.yml`, workspace `STYLE.md`, `CHECKS.md`, and `LOOPS.md`.

Write these files:

- `output/outline.md`
- `output/research_pack.md`
- `output/draft.md`
- `output/claims_table.md`
- `output/sources.md`
- `output/handoff.json`
- `output/image_prompts.md`
- `output/x_posts.md`

Rules:

- Separate facts, inference, opinion, and speculation.
- Cite material claims.
- If browsing is unavailable, state that clearly in `research_pack.md`.
- In `image_prompts.md`, include title-image prompts for both 16:9 and 5:2, plus one no-text illustration prompt per H2 section.
- In `x_posts.md`, write 5 single-post drafts under 280 characters each: news hook, problem/solution, concrete example, caution, and question/CTA.
- Do not invent citations, quotes, URLs, statistics, or publication status.
- Do not publish, post, email, or update a CMS.
"""


def template_outline(theme: str) -> str:
    return f"""# Outline

Theme: {theme}

## Title Candidates

1. TODO
2. TODO
3. TODO
4. TODO
5. TODO
6. TODO
7. TODO

## Structure

- H2: TODO
  - H3: TODO

## Angle

TODO
"""


def template_research_pack() -> str:
    return """# Research Pack

## Research Status

- Web research: TODO
- Limitation: TODO

## Terms

- TODO

## Key Points

1. TODO

## Counterpoints

- TODO

## Verification Queries

- "TODO"
"""


def template_draft() -> str:
    return """# TODO Title

TODO draft.
"""


def template_claims_table() -> str:
    return """# Claims Table

| Claim | Source URL | Confidence | Notes |
|---|---|---|---|
| TODO |  | low |  |
"""


def template_sources() -> str:
    return """# Sources

| URL | Type | Why it matters |
|---|---|---|
| TODO | TODO | TODO |
"""


def template_image_prompts(theme: str) -> str:
    return f"""# Image Prompts

Theme: {theme}

## Title Image Text

TODO title text, preferably 2-3 short lines.

## Style Direction

- Mood: premium but approachable Japanese tech explainer.
- Visuals: TODO.
- Avoid: exact logos, watermarks, signatures, fake UI text, and unreadable gibberish.

## Cover Prompt - 16:9

```text
Create a 16:9 blog title image.
Article theme: {theme}
Title text to render exactly:
TODO

Style direction:
TODO

Composition:
TODO

Constraints:
No watermark. No signature. Do not reproduce official logos exactly.
```

## Cover Prompt - 5:2

```text
Create an exact 5:2 blog title banner.
Article theme: {theme}
Title text to render exactly:
TODO

Style direction:
TODO

Composition:
TODO

Constraints:
No watermark. No signature. Do not reproduce official logos exactly.
```

## Section Illustration Prompts

Use one prompt per H2 section. Section illustrations should not contain text.

### Section 1

```text
Create a 16:9 no-text section illustration.
Section title: TODO
Section summary: TODO
Style direction: match the title image.
Constraints: no text, no watermark, no signature, no logos.
```
"""


def template_x_posts() -> str:
    return """# X Posts

Draft 5 single posts. Keep each one under 280 characters.

## 案1: ニュース/フック

TODO

## 案2: 問題提起

TODO

## 案3: 具体例

TODO

## 案4: 注意点

TODO

## 案5: 質問/CTA

TODO
"""


def template_handoff(slug: str) -> str:
    payload = {
        "title": "TODO Title",
        "subtitle": "",
        "title_image_text": "",
        "slug": slug,
        "summary": "",
        "sections": [],
        "images": {
            "title_aspect_ratios": ["16:9", "5:2"],
            "section_illustrations": [],
        },
        "x_posts_file": "output/x_posts.md",
        "writer": "blog-agent-kit",
        "writer_version": "0.1.0",
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def init_workspace(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    files = {
        root / "BLOG_WORKSPACE.md": template_workspace_readme(),
        root / "STYLE.md": template_style(),
        root / "CHECKS.md": template_checks(),
        root / "LOOPS.md": template_loops(),
        root / "AGENTS.md": template_agents(),
        root / "CLAUDE.md": template_claude(),
        root / "NEXT_ACTIONS.md": template_next_actions(),
        root / "topics" / ".gitkeep": "",
    }
    created = []
    skipped = []
    for path, text in files.items():
        if write_text(path, text, force=args.force):
            created.append(str(path))
        else:
            skipped.append(str(path))

    print(f"Initialized blog workspace: {root}")
    if created:
        print("Created:")
        for path in created:
            print(f"- {path}")
    if skipped:
        print("Skipped existing files:")
        for path in skipped:
            print(f"- {path}")
    return 0


def new_topic(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    date = args.date or today()
    slug = args.slug or slugify(args.theme)
    topic = root / "topics" / f"{date}_{slug}"
    files = {
        topic / "brief.yml": template_brief(
            args.theme,
            args.audience,
            args.goal,
            args.tone,
            args.length,
        ),
        topic / "agent-prompt.md": template_agent_prompt(args.theme),
        topic / "output" / "outline.md": template_outline(args.theme),
        topic / "output" / "research_pack.md": template_research_pack(),
        topic / "output" / "draft.md": template_draft(),
        topic / "output" / "claims_table.md": template_claims_table(),
        topic / "output" / "sources.md": template_sources(),
        topic / "output" / "handoff.json": template_handoff(slug),
        topic / "output" / "image_prompts.md": template_image_prompts(args.theme),
        topic / "output" / "x_posts.md": template_x_posts(),
    }
    created = []
    skipped = []
    for path, text in files.items():
        if write_text(path, text, force=args.force):
            created.append(str(path))
        else:
            skipped.append(str(path))

    print(f"Topic: {topic}")
    print("Created:")
    for path in created:
        print(f"- {path}")
    if skipped:
        print("Skipped existing files:")
        for path in skipped:
            print(f"- {path}")
    return 0


def draft_title(topic: Path) -> str | None:
    draft = topic / "output" / "draft.md"
    if not draft.exists():
        return None
    for line in read_text(draft).splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return None


def handoff_title(topic: Path) -> str | None:
    path = topic / "output" / "handoff.json"
    if not path.exists():
        return None
    try:
        payload = json.loads(read_text(path))
    except json.JSONDecodeError:
        return None
    value = payload.get("title")
    return value if isinstance(value, str) else None


def count_markdown_table_rows(path: Path) -> int:
    if not path.exists():
        return 0
    rows = 0
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        if cells and cells[0].lower() in {"claim", "url"}:
            continue
        rows += 1
    return rows


def count_x_post_drafts(path: Path) -> int:
    if not path.exists():
        return 0
    count = 0
    for line in read_text(path).splitlines():
        if re.match(r"^\s*(?:#{1,3}\s*)?案\s*\d+", line):
            count += 1
    return count


def topic_status(topic: Path) -> TopicStatus:
    topic = topic.resolve()
    output = topic / "output"
    missing = [name for name in REQUIRED_OUTPUTS if not (output / name).exists()]
    warnings: list[str] = []

    brief_exists = (topic / "brief.yml").exists()
    if not brief_exists:
        warnings.append("brief.yml is missing.")

    if output.exists():
        for name in REQUIRED_OUTPUTS:
            path = output / name
            if path.suffix != ".md" or not path.exists():
                continue
            text = read_text(path)
            if "TODO" in text:
                warnings.append(f"{path.name} still contains TODO.")
    else:
        warnings.append("output directory is missing.")

    title = draft_title(topic)
    handoff = handoff_title(topic)
    if title is None:
        warnings.append("draft.md has no H1 title.")
    if handoff is None:
        warnings.append("handoff.json is missing or invalid.")
    if title and handoff and title != handoff:
        warnings.append("handoff.json title does not match draft.md H1.")

    claims_rows = count_markdown_table_rows(output / "claims_table.md")
    if claims_rows < 3:
        warnings.append("claims_table.md should include at least 3 claim rows.")

    source_rows = count_markdown_table_rows(output / "sources.md")
    if source_rows < 3:
        warnings.append("sources.md should include at least 3 source rows.")

    image_prompts = output / "image_prompts.md"
    if image_prompts.exists():
        image_text = read_text(image_prompts)
        if "16:9" not in image_text:
            warnings.append("image_prompts.md should include a 16:9 title image prompt.")
        if "5:2" not in image_text:
            warnings.append("image_prompts.md should include a 5:2 title image prompt.")

    x_post_count = count_x_post_drafts(output / "x_posts.md")
    if x_post_count < 5:
        warnings.append("x_posts.md should include 5 draft posts.")

    return TopicStatus(
        topic=str(topic),
        brief_exists=brief_exists,
        output_exists=output.exists(),
        missing_outputs=missing,
        warnings=warnings,
        title=title,
    )


def latest_topic(root: Path) -> Path | None:
    topics_dir = root / "topics"
    if not topics_dir.exists():
        return None
    topics = sorted([path for path in topics_dir.iterdir() if path.is_dir()])
    return topics[-1] if topics else None


def resolve_topic(args: argparse.Namespace) -> Path:
    if args.topic:
        return Path(args.topic).resolve()
    topic = latest_topic(Path(args.root).resolve())
    if not topic:
        raise SystemExit("No topic found. Use blog-agent new first.")
    return topic


def print_status(status: TopicStatus, *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(asdict(status), ensure_ascii=False, indent=2))
        return
    print(f"Topic: {status.topic}")
    print(f"Brief: {status.brief_exists}")
    print(f"Output: {status.output_exists}")
    print(f"Title: {status.title}")
    if status.missing_outputs:
        print("Missing outputs:")
        for item in status.missing_outputs:
            print(f"- {item}")
    print("Warnings:")
    if status.warnings:
        for item in status.warnings:
            print(f"- {item}")
    else:
        print("- none")


def command_check(args: argparse.Namespace) -> int:
    topic = resolve_topic(args)
    status = topic_status(topic)
    print_status(status, as_json=args.json)
    has_problems = bool(status.missing_outputs or status.warnings)
    return 1 if args.strict and has_problems else 0


def command_prompt(args: argparse.Namespace) -> int:
    topic = resolve_topic(args)
    parts = []
    for relative in ["brief.yml", "agent-prompt.md"]:
        path = topic / relative
        if path.exists():
            parts.append(read_text(path))
    print("\n\n---\n\n".join(parts))
    return 0


def command_status(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    topics_dir = root / "topics"
    if not topics_dir.exists():
        print(f"No topics directory: {topics_dir}")
        return 1 if args.strict else 0
    statuses = [topic_status(path) for path in sorted(topics_dir.iterdir()) if path.is_dir()]
    if args.json:
        print(json.dumps([asdict(item) for item in statuses], ensure_ascii=False, indent=2))
        return 0
    for item in statuses:
        warning_count = len(item.warnings) + len(item.missing_outputs)
        print(f"{Path(item.topic).name}: {warning_count} issue(s)")
    return 1 if args.strict and any(item.warnings or item.missing_outputs for item in statuses) else 0


def render_package(topic: Path) -> str:
    output = topic / "output"
    sections = [
        ("Draft", output / "draft.md"),
        ("Claims Table", output / "claims_table.md"),
        ("Sources", output / "sources.md"),
        ("Image Prompts", output / "image_prompts.md"),
        ("X Posts", output / "x_posts.md"),
    ]
    lines = [f"# Review Package - {topic.name}", ""]
    for heading, path in sections:
        lines.extend([f"## {heading}", ""])
        if path.exists():
            lines.append(read_text(path).strip())
        else:
            lines.append(f"Missing: {path.name}")
        lines.append("")
    lines.extend(
        [
            "## Publication Gate",
            "",
            "- Human review required before publishing.",
            "- No external action was performed by this command.",
            "",
        ]
    )
    return "\n".join(lines)


def command_package(args: argparse.Namespace) -> int:
    topic = resolve_topic(args)
    package = render_package(topic)
    if args.write:
        path = topic / "output" / "review_package.md"
        write_text(path, package, force=True)
        print(f"Wrote {path}")
    else:
        print(package)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="blog-agent")
    parser.add_argument("--version", action="version", version="blog-agent 0.1.0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Create a blog workspace")
    init.add_argument("--root", default=".")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=init_workspace)

    new = subparsers.add_parser("new", help="Create a new article topic")
    new.add_argument("theme")
    new.add_argument("--root", default=".")
    new.add_argument("--date")
    new.add_argument("--slug")
    new.add_argument("--audience", default="general readers")
    new.add_argument("--goal", default="explain the topic clearly and help readers take the next step")
    new.add_argument("--tone", default="clear and grounded")
    new.add_argument("--length", default="1200-1800 words")
    new.add_argument("--force", action="store_true")
    new.set_defaults(func=new_topic)

    for name, help_text, func in [
        ("check", "Check one topic", command_check),
        ("prompt", "Print the generation prompt for one topic", command_prompt),
        ("package", "Render a review package for one topic", command_package),
    ]:
        command = subparsers.add_parser(name, help=help_text)
        command.add_argument("--root", default=".")
        command.add_argument("--topic")
        if name == "check":
            command.add_argument("--json", action="store_true")
            command.add_argument("--strict", action="store_true")
        if name == "package":
            command.add_argument("--write", action="store_true")
        command.set_defaults(func=func)

    status = subparsers.add_parser("status", help="List topic statuses")
    status.add_argument("--root", default=".")
    status.add_argument("--json", action="store_true")
    status.add_argument("--strict", action="store_true")
    status.set_defaults(func=command_status)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
