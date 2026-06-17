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

Agents may draft and revise local files. They must not publish, post, email, or change a CMS without explicit human approval.
"""


def template_style() -> str:
    return """# STYLE

## Default Voice

- Clear, useful, and grounded.
- Prefer concrete examples over vague claims.
- Keep facts, inference, opinion, and speculation separate.
- Avoid hype, moralizing, and unsupported certainty.

## Article Structure

1. Hook: question, scene, problem, or direct promise.
2. Context: why this matters now.
3. Core explanation: definitions, steps, examples, tradeoffs.
4. Evidence: sources, examples, and counterpoints.
5. Practical close: next action, checklist, or decision frame.

## Citation Rules

- Material claims need sources.
- If web research is unavailable, mark research limitations in `research_pack.md`.
- Do not invent citations or source titles.
- Prefer primary sources, official docs, academic papers, and reputable reporting.

## Risk Topics

For health, finance, legal, politics, identity, religion, or safety topics:

- show multiple perspectives
- reduce certainty
- include scope limits
- avoid personal diagnosis or prescriptive advice
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

## Quality Gates

- The draft starts with one `# Title`.
- `handoff.json.title` matches the draft title.
- Major claims appear in `claims_table.md`.
- Sources are listed in `sources.md`.
- Facts, inference, opinion, and speculation are not mixed.
- Web research limitations are explicit when browsing is unavailable.

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
Brief -> Plan -> Research -> Draft -> Verify -> Package -> Stop
```

1. Read `brief.yml`, `STYLE.md`, and `CHECKS.md`.
2. Write `output/outline.md` with title candidates and section plan.
3. Write `output/research_pack.md` with terms, evidence, open questions, and search queries.
4. Write `output/draft.md`.
5. Write `output/claims_table.md` and `output/sources.md`.
6. Write `output/handoff.json`.
7. Run `blog-agent check --topic <topic>`.

## Stop Conditions

- The article needs current facts and browsing is unavailable.
- The topic is high-risk and sources are insufficient.
- The user asks for publishing or external posting without explicit confirmation.
- The article would require invented quotes, citations, links, or statistics.
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
- If browsing is unavailable, say so in `research_pack.md` and list verification queries.

## Default Prompt

Find the newest topic under `topics/` with missing or incomplete outputs. Follow the brief and generate the required files under `output/`. Separate facts, inference, opinion, and speculation. Do not perform external actions.
"""


def template_claude() -> str:
    return """# CLAUDE.md

This is a Blog Agent Kit workspace for Claude Code and Claude Desktop scheduled tasks.

## Contract

- Read `STYLE.md`, `CHECKS.md`, `LOOPS.md`, and the topic `brief.yml`.
- Generate or revise local files only.
- Run `blog-agent check --topic <topic>` before final status.
- Do not publish, post, email, update a CMS, or invent citations.
- Mark web research limitations explicitly when browsing is unavailable.

## Scheduled Task Prompt

Find the newest incomplete topic under `topics/`. Generate or revise the required output files. Return a short status with completed files, warnings, and next human review actions. Do not perform external actions.
"""


def template_next_actions() -> str:
    return """# NEXT_ACTIONS

- Create a topic with `blog-agent new "Theme"`.
- Ask Codex or Claude to generate the missing outputs.
- Run `blog-agent check --topic topics/...`.
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

Rules:

- Separate facts, inference, opinion, and speculation.
- Cite material claims.
- If browsing is unavailable, state that clearly in `research_pack.md`.
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


def template_handoff(slug: str) -> str:
    payload = {
        "title": "TODO Title",
        "subtitle": "",
        "slug": slug,
        "summary": "",
        "sections": [],
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
