import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "pull-remote-artifacts.sh"


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


if __name__ == "__main__":
    unittest.main()
