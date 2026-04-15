"""单元测试：日志级别与配置摘要"""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from analyze_cleanup_candidates import LOGGER, main


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class TestLoggingBehavior(unittest.TestCase):
    def tearDown(self) -> None:
        LOGGER.configure("summary")

    def test_summary_logs_config_without_hit_lines(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write(root / "package.json", '{"name":"demo"}')
            _write(root / ".code-cleanup" / "scan-dirs.txt", "src/page:unused_page:stem,parent\n")
            _write(root / "src" / "router.js", "export default []\n")
            _write(root / "src" / "page" / "home" / "home.js", "console.log('home')\n")
            _write(root / "src" / "page" / "detail" / "detail.js", "const path = '/home/'\n")

            output = root / "result.json"
            stderr = io.StringIO()
            argv = [
                "analyze_cleanup_candidates.py",
                "--project-root",
                str(root),
                "--output",
                str(output),
            ]
            with patch.object(sys, "argv", argv), redirect_stderr(stderr):
                main()

            log_output = stderr.getvalue()
            self.assertIn("scan-dirs: source=project", log_output)
            self.assertIn("effective scan plan: src/page", log_output)
            self.assertIn("Phase 4 complete", log_output)
            self.assertNotIn("HIT:", log_output)
            self.assertTrue(output.exists())

    def test_debug_logs_hit_samples(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write(root / "package.json", '{"name":"demo"}')
            _write(root / ".code-cleanup" / "scan-dirs.txt", "src/page:unused_page:stem,parent\n")
            _write(root / "src" / "router.js", "export default []\n")
            _write(root / "src" / "page" / "home" / "home.js", "console.log('home')\n")
            _write(root / "src" / "page" / "detail" / "detail.js", "const path = '/home/'\n")

            output = root / "result.json"
            stderr = io.StringIO()
            argv = [
                "analyze_cleanup_candidates.py",
                "--project-root",
                str(root),
                "--log-level",
                "debug",
                "--output",
                str(output),
            ]
            with patch.object(sys, "argv", argv), redirect_stderr(stderr):
                main()

            self.assertIn("HIT: Found '/home/'", stderr.getvalue())

    def test_quiet_suppresses_phase_logs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write(root / "package.json", '{"name":"demo"}')
            _write(root / "src" / "router.js", "export default []\n")

            output = root / "result.json"
            stderr = io.StringIO()
            argv = [
                "analyze_cleanup_candidates.py",
                "--project-root",
                str(root),
                "--log-level",
                "quiet",
                "--output",
                str(output),
            ]
            with patch.object(sys, "argv", argv), redirect_stderr(stderr):
                main()

            log_output = stderr.getvalue()
            self.assertNotIn("Phase 1:", log_output)
            self.assertIn("Generation complete:", log_output)
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(data["project_root"], str(root.resolve()).replace("\\", "/"))
