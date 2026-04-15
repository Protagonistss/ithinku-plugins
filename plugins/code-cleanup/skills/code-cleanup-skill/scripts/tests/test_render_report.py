"""单元测试：报告渲染输出"""
import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from render_cleanup_report import render_patch_plan, render_report, render_report_html


SAMPLE_DATA = {
    "generated_at": "2026-04-15T00:00:00+00:00",
    "project_root": "/project",
    "summary": {"high": 0, "medium": 0, "low": 0},
    "project_stats": {
        "health_score": 100,
        "total_files_scanned": 10,
        "total_size_bytes": 1024,
        "unused_files_count": 0,
        "unused_size_bytes": 0,
    },
    "analysis_warnings": ["Configured scan-dirs did not match any files; fell back to generic code scan."],
    "candidates": [],
}


class TestRenderReport(unittest.TestCase):
    def test_markdown_report_includes_warnings(self):
        report = render_report(SAMPLE_DATA)
        self.assertIn("## Analysis Warnings", report)
        self.assertIn("fell back to generic code scan", report)

    def test_patch_plan_uses_python3(self):
        patch_plan = render_patch_plan(SAMPLE_DATA)
        self.assertIn("python3 -c", patch_plan)
        self.assertIn("python3 analyze_cleanup_candidates.py", patch_plan)
        self.assertNotIn("## Step 4: 清理残留空目录\n\n## Step 4", patch_plan)

    def test_html_report_includes_warning_panel(self):
        html = render_report_html(SAMPLE_DATA)
        self.assertIn("Analysis Warnings", html)
        self.assertIn("Confidence warnings present", html)
