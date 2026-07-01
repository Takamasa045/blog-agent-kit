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
            style = (root / "STYLE.md").read_text(encoding="utf-8")
            self.assertIn("## いとぱんスタイル", style)
            self.assertIn("一人称は `僕`", style)
            self.assertIn("FAQ/Q&A は、brief で明示されない限り追加しない。", style)
            self.assertIn("## 読者入口", style)

            self.assertEqual(
                run_silent(["new", "Example article", "--root", str(root), "--date", "2026-06-17"]),
                0,
            )
            topic = root / "topics" / "2026-06-17_example-article"
            self.assertTrue((topic / "brief.yml").exists())
            self.assertTrue((topic / "output" / "draft.md").exists())
            brief = (topic / "brief.yml").read_text(encoding="utf-8")
            self.assertIn("reader_problem:", brief)
            outline = (topic / "output" / "outline.md").read_text(encoding="utf-8")
            self.assertIn("## Reader Entry", outline)
            self.assertIn("- Problem: TODO", outline)
            agent_prompt = (topic / "agent-prompt.md").read_text(encoding="utf-8")
            self.assertIn("Reader Entry", agent_prompt)
            reviewer_prompt = (topic / "reviewer-prompt.md").read_text(encoding="utf-8")
            self.assertIn("DISCOVER -> PLAN -> EXECUTE -> VERIFY -> ITERATE", reviewer_prompt)
            image_prompts = (topic / "output" / "image_prompts.md").read_text(encoding="utf-8")
            self.assertIn("Cover Prompt - 16:9", image_prompts)
            self.assertIn("Cover Prompt - 5:2", image_prompts)
            x_posts = (topic / "output" / "x_posts.md").read_text(encoding="utf-8")
            self.assertIn("案5: 質問/CTA", x_posts)
            review_round = (topic / "output" / "review_round_1.md").read_text(encoding="utf-8")
            self.assertIn("# Review Round 1", review_round)
            iteration_log = (topic / "output" / "iteration_log.md").read_text(encoding="utf-8")
            self.assertIn("## Round 2 Changes", iteration_log)

    def test_check_reports_todo_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "blog"
            run_silent(["init", "--root", str(root)])
            run_silent(["new", "Example article", "--root", str(root), "--date", "2026-06-17"])
            topic = root / "topics" / "2026-06-17_example-article"
            status = cli.topic_status(topic)
            self.assertTrue(status.warnings)
            self.assertIn("draft.md still contains TODO.", status.warnings)
            self.assertIn("image_prompts.md still contains TODO.", status.warnings)
            self.assertIn("x_posts.md still contains TODO.", status.warnings)
            self.assertIn("review_round_1.md still contains TODO.", status.warnings)
            self.assertIn("iteration_log.md still contains TODO.", status.warnings)

    def test_review_prompt_command_prints_second_agent_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "blog"
            run_silent(["init", "--root", str(root)])
            run_silent(["new", "Example article", "--root", str(root), "--date", "2026-06-17"])
            topic = root / "topics" / "2026-06-17_example-article"

            buffer = StringIO()
            with redirect_stdout(buffer):
                self.assertEqual(cli.main(["review-prompt", "--topic", str(topic)]), 0)

            prompt = buffer.getvalue()
            self.assertIn("Reviewer Prompt", prompt)
            self.assertIn("two local improvement rounds", prompt)

    def test_review_prompt_command_handles_legacy_topic_without_prompt_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "blog"
            run_silent(["init", "--root", str(root)])
            run_silent(["new", "Example article", "--root", str(root), "--date", "2026-06-17"])
            topic = root / "topics" / "2026-06-17_example-article"
            (topic / "reviewer-prompt.md").unlink()

            buffer = StringIO()
            with redirect_stdout(buffer):
                self.assertEqual(cli.main(["review-prompt", "--topic", str(topic)]), 0)

            prompt = buffer.getvalue()
            self.assertIn("Reviewer Prompt", prompt)
            self.assertIn("DISCOVER -> PLAN -> EXECUTE -> VERIFY -> ITERATE", prompt)

    def test_check_warns_when_completed_outline_missing_reader_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "blog"
            run_silent(["init", "--root", str(root)])
            run_silent(["new", "Example article", "--root", str(root), "--date", "2026-06-17"])
            topic = root / "topics" / "2026-06-17_example-article"
            output = topic / "output"
            (output / "outline.md").write_text(
                "# Outline\n\n## Title Candidates\n\n1. Useful title\n",
                encoding="utf-8",
            )

            status = cli.topic_status(topic)
            self.assertIn(
                "outline.md should include a Reader Entry section with reader, "
                "problem, promise, and next step.",
                status.warnings,
            )

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

    def test_sync_latest_topic_without_overwriting_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            destination = Path(tmp) / "destination"
            run_silent(["init", "--root", str(source)])
            run_silent(["new", "Example article", "--root", str(source), "--date", "2026-06-17"])

            source_topic = source / "topics" / "2026-06-17_example-article"
            (source_topic / "output" / "draft.md").write_text(
                "# Remote Draft\n\nRemote body.\n",
                encoding="utf-8",
            )

            self.assertEqual(
                run_silent(["sync", "--source", str(source), "--root", str(destination)]),
                0,
            )
            synced_draft = destination / "topics" / "2026-06-17_example-article" / "output" / "draft.md"
            self.assertEqual(synced_draft.read_text(encoding="utf-8"), "# Remote Draft\n\nRemote body.\n")

            synced_draft.write_text("# Local Draft\n\nKeep me.\n", encoding="utf-8")
            (source_topic / "output" / "draft.md").write_text(
                "# Remote Draft 2\n\nRemote body 2.\n",
                encoding="utf-8",
            )
            self.assertEqual(
                run_silent(["sync", "--source", str(source), "--root", str(destination)]),
                0,
            )
            self.assertEqual(synced_draft.read_text(encoding="utf-8"), "# Local Draft\n\nKeep me.\n")

            self.assertEqual(
                run_silent(["sync", "--source", str(source), "--root", str(destination), "--force"]),
                0,
            )
            self.assertEqual(synced_draft.read_text(encoding="utf-8"), "# Remote Draft 2\n\nRemote body 2.\n")


if __name__ == "__main__":
    unittest.main()
