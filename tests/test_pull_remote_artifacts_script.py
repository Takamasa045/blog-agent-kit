import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "pull-remote-artifacts.sh"
AUTO_SCRIPT = ROOT / "scripts" / "auto-pull-vps-artifacts.sh"
INSTALL_SCRIPT = ROOT / "scripts" / "install-auto-pull-launch-agent.sh"


class PullRemoteArtifactsScriptTests(unittest.TestCase):
    def test_help_prints_usage_without_remote_access(self) -> None:
        result = subprocess.run(
            ["sh", str(SCRIPT), "--help"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Usage:", result.stdout)
        self.assertIn("does not delete local files", result.stdout)

    def test_missing_arguments_fail_before_remote_access(self) -> None:
        result = subprocess.run(
            ["sh", str(SCRIPT)],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("Usage:", result.stderr)

    def test_auto_pull_help_prints_usage_without_remote_access(self) -> None:
        result = subprocess.run(
            ["sh", str(AUTO_SCRIPT), "--help"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("BLOG_AGENT_VPS_ARTIFACT_ENV", result.stdout)
        self.assertIn("does not remove local files", result.stdout)

    def test_auto_pull_missing_env_fails_before_remote_access(self) -> None:
        result = subprocess.run(
            ["sh", str(AUTO_SCRIPT)],
            check=False,
            capture_output=True,
            text=True,
            env={
                **os.environ,
                "BLOG_AGENT_VPS_ARTIFACT_ENV": "/tmp/blog-agent-kit-missing-env",
            },
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing env file", result.stderr)

    def test_install_launch_agent_help_prints_usage(self) -> None:
        result = subprocess.run(
            ["sh", str(INSTALL_SCRIPT), "--help"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("interval-seconds", result.stdout)

    def test_install_launch_agent_rejects_invalid_interval_before_writing(self) -> None:
        result = subprocess.run(
            ["sh", str(INSTALL_SCRIPT), "not-a-number"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("positive integer", result.stderr)


if __name__ == "__main__":
    unittest.main()
