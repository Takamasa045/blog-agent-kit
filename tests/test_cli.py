from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from blog_agent_kit import cli


def run_silent(args: list[str]) -> int:
    buffer = StringIO()
    with redirect_stdout(buffer):
        return cli.main(args)


class CliTest(unittest.TestCase):
    def test_init_and_new_topic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "blog"
            self.assertEqual(run_silent(["init", "--root", str(root)]), 0)
            self.assertTrue((root / "STYLE.md").exists())

            self.assertEqual(
                run_silent(["new", "Example article", "--root", str(root), "--date", "2026-06-17"]),
                0,
            )
            topic = root / "topics" / "2026-06-17_example-article"
            self.assertTrue((topic / "brief.yml").exists())
            self.assertTrue((topic / "output" / "draft.md").exists())

    def test_check_reports_todo_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "blog"
            run_silent(["init", "--root", str(root)])
            run_silent(["new", "Example article", "--root", str(root), "--date", "2026-06-17"])
            topic = root / "topics" / "2026-06-17_example-article"
            status = cli.topic_status(topic)
            self.assertTrue(status.warnings)
            self.assertIn("draft.md still contains TODO.", status.warnings)

    def test_title_mismatch_warning_disappears_when_fixed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "blog"
            run_silent(["init", "--root", str(root)])
            run_silent(["new", "Example article", "--root", str(root), "--date", "2026-06-17"])
            topic = root / "topics" / "2026-06-17_example-article"
            output = topic / "output"
            (output / "draft.md").write_text("# Real Title\n\nBody.\n", encoding="utf-8")
            payload = json.loads((output / "handoff.json").read_text(encoding="utf-8"))
            payload["title"] = "Real Title"
            (output / "handoff.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

            status = cli.topic_status(topic)
            self.assertNotIn("handoff.json title does not match draft.md H1.", status.warnings)


if __name__ == "__main__":
    unittest.main()
