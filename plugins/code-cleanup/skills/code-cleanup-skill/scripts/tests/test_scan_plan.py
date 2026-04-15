"""单元测试：扫描计划与 fallback 行为"""
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from analyze_cleanup_candidates import (
    ScanDir,
    _is_keep_listed,
    analyze_history_files,
    analyze_modules,
    detect_project_profile,
    identify_entry_points,
    resolve_scan_plan,
)


class TestResolveScanPlan(unittest.TestCase):
    def test_falls_back_to_generic_scan_when_config_dirs_miss(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            target_file = root / "lib" / "utils.py"
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text("def helper():\n    pass\n", encoding="utf-8")

            scan_dirs = [ScanDir("src/components", "unused_component", ["stem", "tag"])]
            profile = detect_project_profile(root, [target_file])
            effective, fallback_mode, warnings = resolve_scan_plan(
                root,
                [target_file],
                scan_dirs,
                set(),
                {"lib/utils.py": "def helper():\n    pass\n"},
                profile,
            )

            self.assertTrue(fallback_mode)
            self.assertEqual(len(effective), 1)
            self.assertEqual(effective[0].category, "unused_module")
            self.assertEqual(effective[0].dir_path, "")
            self.assertTrue(warnings)

    def test_warns_when_no_supported_code_files_exist(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            readme = root / "README.md"
            readme.write_text("# docs\n", encoding="utf-8")

            profile = detect_project_profile(root, [readme])
            effective, fallback_mode, warnings = resolve_scan_plan(
                root,
                [readme],
                [ScanDir("src/components", "unused_component", ["stem", "tag"])],
                set(),
                {},
                profile,
            )

            self.assertEqual(effective, [])
            self.assertFalse(fallback_mode)
            self.assertTrue(warnings)

    def test_low_confidence_unreachable_candidates_are_downgraded(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            target_file = root / "lib" / "utils.py"
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text("def helper():\n    pass\n", encoding="utf-8")

            candidates = analyze_modules(
                root=root,
                all_files=[target_file],
                reference_pool={"lib/utils.py": "def helper():\n    pass\n"},
                keep_list=set(),
                scan_dirs=[ScanDir("", "unused_module", ["stem", "name_variants"])],
                symbol_usage={},
                config_driven_refs={},
                reachable=set(),
                fallback_mode=True,
                low_confidence_mode=True,
            )

            self.assertEqual(len(candidates), 1)
            self.assertEqual(candidates[0].risk_level, "medium")

    def test_detects_plugin_repository_profile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            marketplace = root / ".claude-plugin" / "marketplace.json"
            marketplace.parent.mkdir(parents=True, exist_ok=True)
            marketplace.write_text("{}", encoding="utf-8")
            skill = root / "plugins" / "demo-plugin" / "skills" / "demo" / "SKILL.md"
            skill.parent.mkdir(parents=True, exist_ok=True)
            skill.write_text("# skill\n", encoding="utf-8")

            profile = detect_project_profile(root, [marketplace, skill])
            self.assertEqual(profile.project_type, "plugin_repository")
            self.assertEqual(profile.default_scan_dirs[0].dir_path, "plugins")

    def test_plugin_repository_protected_paths_are_skipped(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            test_file = root / "plugins" / "demo-plugin" / "skills" / "demo" / "scripts" / "tests" / "test_demo.py"
            test_file.parent.mkdir(parents=True, exist_ok=True)
            test_file.write_text("class TestDemo:\n    pass\n", encoding="utf-8")
            marketplace = root / ".claude-plugin" / "marketplace.json"
            marketplace.parent.mkdir(parents=True, exist_ok=True)
            marketplace.write_text("{}", encoding="utf-8")

            profile = detect_project_profile(root, [test_file, marketplace])
            candidates = analyze_modules(
                root=root,
                all_files=[test_file, marketplace],
                reference_pool={"plugins/demo-plugin/skills/demo/scripts/tests/test_demo.py": "class TestDemo:\n    pass\n"},
                keep_list=set(),
                scan_dirs=profile.default_scan_dirs,
                symbol_usage={},
                config_driven_refs={},
                reachable=set(),
                fallback_mode=False,
                low_confidence_mode=False,
                project_profile=profile,
            )

            self.assertEqual(candidates, [])

    def test_keep_list_glob_matches_module_candidates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            target_file = root / "build" / "webpack.prev.commit.js"
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text("module.exports = {}\n", encoding="utf-8")

            candidates = analyze_modules(
                root=root,
                all_files=[target_file],
                reference_pool={"build/webpack.prev.commit.js": "module.exports = {}\n"},
                keep_list={"build/**"},
                scan_dirs=[ScanDir("", "unused_module", ["stem", "name_variants"])],
                symbol_usage={},
                config_driven_refs={},
                reachable=set(),
                fallback_mode=False,
                low_confidence_mode=False,
            )

            self.assertEqual(candidates, [])

    def test_keep_list_glob_matches_history_candidates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            history_file = root / "src" / "webpack.config.js_release"
            history_file.parent.mkdir(parents=True, exist_ok=True)
            history_file.write_text("module.exports = {}\n", encoding="utf-8")

            candidates = analyze_history_files(
                root=root,
                reference_pool={"src/webpack.config.js_release": "module.exports = {}\n"},
                keep_list={"src/webpack.config.js_*"},
            )

            self.assertEqual(candidates, [])

    def test_keep_list_glob_marks_entry_point(self):
        all_rels = {"src/manifest/manifest.json", "src/page/home/home.js"}
        entries = identify_entry_points(all_rels, {"src/manifest/**"})
        self.assertIn("src/manifest/manifest.json", entries)

    def test_keep_list_helper_supports_glob(self):
        self.assertTrue(_is_keep_listed("src/widget/teacher/menus.json", {"src/widget/**/*.json"}))
        self.assertFalse(_is_keep_listed("src/widget/teacher/menus.js", {"src/widget/**/*.json"}))
