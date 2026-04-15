"""单元测试：符号级导出/导入分析"""
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from analyze_cleanup_candidates import (
    ImportRef,
    build_barrel_map,
    build_export_map,
    build_import_map,
    build_resolver_context,
    build_symbol_usage,
)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class TestBuildExportMap(unittest.TestCase):
    def test_js_named_exports(self):
        pool = {
            "src/utils.js": "export function formatData() {}\nexport const VERSION = '1.0'",
        }
        exports = build_export_map(pool)
        self.assertIn("src/utils.js", exports)
        self.assertIn("formatData", exports["src/utils.js"])
        self.assertIn("VERSION", exports["src/utils.js"])

    def test_python_exports(self):
        pool = {
            "src/utils.py": "def helper():\n    pass\nclass MyHelper:\n    pass\nCONST = 42",
        }
        exports = build_export_map(pool)
        self.assertIn("src/utils.py", exports)
        self.assertIn("helper", exports["src/utils.py"])
        self.assertIn("MyHelper", exports["src/utils.py"])


class TestBuildImportMap(unittest.TestCase):
    def test_js_named_import_resolves_source(self):
        pool = {
            "src/page.js": 'import { Button, Input as LocalInput } from "./components"',
            "src/components.js": "export const Button = 1\nexport const Input = 2",
        }
        imports = build_import_map(pool, set(pool.keys()))
        self.assertIn("src/page.js", imports)
        ref = imports["src/page.js"][0]
        self.assertEqual(ref.resolved_path, "src/components.js")
        self.assertEqual(ref.import_kind, "named")
        self.assertEqual(ref.imported_names, ["Button", "Input"])

    def test_js_default_import_resolves_source(self):
        pool = {
            "src/app.js": 'import App from "./App"',
            "src/App.js": "export default function App() {}",
        }
        imports = build_import_map(pool, set(pool.keys()))
        default_refs = [ref for ref in imports["src/app.js"] if ref.import_kind == "default"]
        self.assertEqual(len(default_refs), 1)
        self.assertEqual(default_refs[0].resolved_path, "src/App.js")

    def test_python_relative_import_resolves_source(self):
        pool = {
            "src/main.py": "from .utils import helper, format_data as fmt",
            "src/utils.py": "def helper(): pass",
        }
        imports = build_import_map(pool, set(pool.keys()))
        ref = imports["src/main.py"][0]
        self.assertEqual(ref.resolved_path, "src/utils.py")
        self.assertEqual(ref.imported_names, ["helper", "format_data"])

    def test_python_absolute_import_resolves_source(self):
        pool = {
            "src/main.py": "from utils import helper",
            "src/utils.py": "def helper(): pass",
        }
        context = build_resolver_context(Path.cwd(), [], set(pool.keys()))
        imports = build_import_map(pool, set(pool.keys()), context)
        ref = imports["src/main.py"][0]
        self.assertEqual(ref.resolved_path, "src/utils.py")

    def test_js_alias_import_resolves_source(self):
        pool = {
            "src/page.ts": 'import { Button } from "@/components/Button"',
            "src/components/Button.tsx": "export const Button = () => null",
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write(
                root / "tsconfig.json",
                """
                {
                  "compilerOptions": {
                    "baseUrl": ".",
                    "paths": {
                      "@/*": ["src/*"]
                    }
                  }
                }
                """,
            )
            context = build_resolver_context(root, [root / "tsconfig.json"], set(pool.keys()))
            imports = build_import_map(pool, set(pool.keys()), context)
            ref = imports["src/page.ts"][0]
            self.assertEqual(ref.resolved_path, "src/components/Button.tsx")
            self.assertEqual(ref.imported_names, ["Button"])


class TestBuildSymbolUsage(unittest.TestCase):
    def test_direct_named_import_marks_only_matching_source(self):
        export_map = {
            "src/services/user.js": ["getUser", "deleteUser"],
        }
        import_map = {
            "src/page/login.js": [
                ImportRef(
                    raw_path="./services/user",
                    resolved_path="src/services/user.js",
                    imported_names=["getUser"],
                    import_kind="named",
                )
            ],
        }
        usage = build_symbol_usage(export_map, import_map)
        self.assertEqual(usage["src/services/user.js"].used_exports, ["getUser"])
        self.assertEqual(usage["src/services/user.js"].unused_exports, ["deleteUser"])

    def test_same_name_in_other_module_does_not_mark_used(self):
        export_map = {
            "src/services/user.js": ["helper"],
            "src/utils/helper.js": ["helper"],
        }
        import_map = {
            "src/page/login.js": [
                ImportRef(
                    raw_path="../utils/helper",
                    resolved_path="src/utils/helper.js",
                    imported_names=["helper"],
                    import_kind="named",
                )
            ],
        }
        usage = build_symbol_usage(export_map, import_map)
        self.assertEqual(usage["src/utils/helper.js"].used_exports, ["helper"])
        self.assertEqual(usage["src/services/user.js"].used_exports, [])
        self.assertEqual(usage["src/services/user.js"].unused_exports, ["helper"])
        self.assertFalse(usage["src/services/user.js"].has_precise_consumers)

    def test_namespace_import_is_treated_as_ambiguous(self):
        export_map = {
            "src/utils.js": ["formatData", "parseData"],
        }
        import_map = {
            "src/page.js": [
                ImportRef(
                    raw_path="./utils",
                    resolved_path="src/utils.js",
                    imported_names=["*"],
                    import_kind="namespace",
                )
            ],
        }
        usage = build_symbol_usage(export_map, import_map)
        self.assertTrue(usage["src/utils.js"].has_ambiguous_consumers)
        self.assertEqual(usage["src/utils.js"].used_exports, [])


class TestBuildBarrelMap(unittest.TestCase):
    def test_js_named_reexport(self):
        pool = {
            "src/components/index.js": "export { Button, Input } from './components'",
            "src/components/components": "// components file",
        }
        barrel = build_barrel_map(pool)
        self.assertIn("src/components/index.js", barrel)
        self.assertIn("src/components/components", barrel["src/components/index.js"])
        self.assertIn("Button", barrel["src/components/index.js"]["src/components/components"])
        self.assertIn("Input", barrel["src/components/index.js"]["src/components/components"])

    def test_python_init_reexport(self):
        pool = {
            "src/utils/__init__.py": "from .helper import format_data\nfrom .core import process",
        }
        barrel = build_barrel_map(pool)
        self.assertIn("src/utils/__init__.py", barrel)
        self.assertIn("src/utils/helper", barrel["src/utils/__init__.py"])
        self.assertIn("src/utils/core", barrel["src/utils/__init__.py"])


class TestSymbolUsageWithBarrel(unittest.TestCase):
    def test_barrel_reexport_marks_source_used(self):
        export_map = {
            "src/components/Button.js": ["Button"],
        }
        import_map = {
            "src/page.js": [
                ImportRef(
                    raw_path="./components",
                    resolved_path="src/components/index.js",
                    imported_names=["Button"],
                    import_kind="named",
                )
            ],
        }
        pool = {
            "src/components/Button.js": "export function Button() {}",
            "src/components/index.js": "export { Button } from './Button'",
            "src/page.js": 'import { Button } from "./components"',
        }
        barrel_map = build_barrel_map(pool)
        usage = build_symbol_usage(export_map, import_map, barrel_map)
        self.assertEqual(usage["src/components/Button.js"].used_exports, ["Button"])
        self.assertEqual(usage["src/components/Button.js"].unused_exports, [])

    def test_barrel_export_star(self):
        export_map = {
            "src/utils/helpers.js": ["formatData", "parseData"],
        }
        import_map = {
            "src/page.js": [
                ImportRef(
                    raw_path="../utils",
                    resolved_path="src/utils/index.js",
                    imported_names=["formatData"],
                    import_kind="named",
                )
            ],
        }
        pool = {
            "src/utils/helpers.js": "export function formatData() {}\nexport function parseData() {}",
            "src/utils/index.js": "export * from './helpers'",
            "src/page.js": 'import { formatData } from "../utils"',
        }
        barrel_map = build_barrel_map(pool)
        usage = build_symbol_usage(export_map, import_map, barrel_map)
        self.assertEqual(usage["src/utils/helpers.js"].used_exports, ["formatData"])
        self.assertEqual(usage["src/utils/helpers.js"].unused_exports, ["parseData"])
