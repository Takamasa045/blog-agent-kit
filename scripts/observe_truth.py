#!/usr/bin/env python3
"""Read-only repository state snapshot for Blog Agent Kit agents."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SURFACE_FILES = [
    "VISION.md",
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CHECKS.md",
    "LOOPS.md",
    "MEMORY.md",
    "NEXT_ACTIONS.md",
]
REQUIRED_TOPIC_OUTPUTS = [
    "outline.md",
    "research_pack.md",
    "draft.md",
    "claims_table.md",
    "sources.md",
    "handoff.json",
    "image_prompts.md",
    "x_posts.md",
]


def run_git(args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return result.stdout.rstrip("\n")


def git_state() -> dict[str, Any]:
    status = run_git(["status", "--short"]) or ""
    return {
        "branch": run_git(["rev-parse", "--abbrev-ref", "HEAD"]),
        "commit": run_git(["rev-parse", "--short", "HEAD"]),
        "dirty_files": [line for line in status.splitlines() if line],
    }


def surface_state() -> dict[str, Any]:
    files = {name: (ROOT / name).exists() for name in SURFACE_FILES}
    return {
        "files": files,
        "missing": [name for name, exists in files.items() if not exists],
    }


def docs_state() -> dict[str, Any]:
    docs_root = ROOT / "docs"
    docs = sorted(path.relative_to(ROOT).as_posix() for path in docs_root.glob("*.md"))
    return {"count": len(docs), "files": docs}


def topic_state() -> dict[str, Any]:
    topics_root = ROOT / "topics"
    if not topics_root.exists():
        return {"topics_root_exists": False, "count": 0, "newest": None}

    topics = sorted(path for path in topics_root.iterdir() if path.is_dir())
    newest = topics[-1] if topics else None
    if newest is None:
        return {"topics_root_exists": True, "count": 0, "newest": None}

    output_root = newest / "output"
    missing_outputs = [
        name for name in REQUIRED_TOPIC_OUTPUTS if not (output_root / name).exists()
    ]
    return {
        "topics_root_exists": True,
        "count": len(topics),
        "newest": newest.relative_to(ROOT).as_posix(),
        "newest_missing_outputs": missing_outputs,
    }


def observe() -> dict[str, Any]:
    return {
        "root": str(ROOT),
        "git": git_state(),
        "surface": surface_state(),
        "docs": docs_state(),
        "topics": topic_state(),
        "verification": [
            "python3 scripts/observe_truth.py --json",
            "PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'",
            "PYTHONPATH=src python3 -m blog_agent_kit.cli init --root /tmp/blog-demo --force",
            'PYTHONPATH=src python3 -m blog_agent_kit.cli new "Example article" --root /tmp/blog-demo --date 2026-06-17',
            "PYTHONPATH=src python3 -m blog_agent_kit.cli check --topic /tmp/blog-demo/topics/2026-06-17_example-article",
        ],
    }


def print_text(snapshot: dict[str, Any]) -> None:
    git = snapshot["git"]
    surface = snapshot["surface"]
    docs = snapshot["docs"]
    topics = snapshot["topics"]

    print("Blog Agent Kit truth")
    print(f"root: {snapshot['root']}")
    print(f"branch: {git['branch']}")
    print(f"commit: {git['commit']}")
    print(f"dirty files: {len(git['dirty_files'])}")
    for dirty_file in git["dirty_files"]:
        print(f"  {dirty_file}")
    print(f"surface missing: {', '.join(surface['missing']) or 'none'}")
    print(f"docs files: {docs['count']}")
    print(f"topics: {topics['count']}")
    if topics["newest"]:
        print(f"newest topic: {topics['newest']}")
        print(
            "newest missing outputs: "
            + (", ".join(topics["newest_missing_outputs"]) or "none")
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print JSON")
    args = parser.parse_args()

    snapshot = observe()
    if args.json:
        print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    else:
        print_text(snapshot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
