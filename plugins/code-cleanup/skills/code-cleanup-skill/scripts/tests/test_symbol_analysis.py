"""单元测试：符号级导出/导入分析"""
import sys
import pytest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from analyze_cleanup_candidates import (
    build_export_map,
    build_import_map,
    build_barrel_map,
    build_symbol_usage,
)


class TestBuildExportMap:
    def test_js_named_exports(self):
        pool = {
            "src/utils.js": "export function formatData() {}\nexport const VERSION = '1.0'",
        }
        exports = build_export_map(pool)
        assert "src/utils.js" in exports
        assert "formatData" in exports["src/utils.js"]
        assert "VERSION" in exports["src/utils.js"]

    def test_js_export_list(self):
        pool = {
            "src/index.js": "export { Button, Input } from './components'",
        }
        exports = build_export_map(pool)
        assert "src/index.js" in exports
        assert "Button" in exports["src/index.js"]
        assert "Input" in exports["src/index.js"]

    def test_js_default_export(self):
        pool = {
            "src/app.js": "export default function App() {}",
        }
        exports = build_export_map(pool)
        assert "src/app.js" in exports
        assert "App" in exports["src/app.js"]

    def test_js_module_exports(self):
        pool = {
            "src/legacy.js": "module.exports = myObject",
        }
        exports = build_export_map(pool)
        assert "src/legacy.js" in exports
        assert "myObject" in exports["src/legacy.js"]

    def test_python_exports(self):
        pool = {
            "src/utils.py": "def helper():\n    pass\nclass MyHelper:\n    pass\nCONST = 42",
        }
        exports = build_export_map(pool)
        assert "src/utils.py" in exports
        assert "helper" in exports["src/utils.py"]
        assert "MyHelper" in exports["src/utils.py"]

    def test_go_exports(self):
        pool = {
            "src/service.go": "func ProcessData() {}\ntype Service struct{}\nconst MaxSize = 100",
        }
        exports = build_export_map(pool)
        assert "src/service.go" in exports
        assert "ProcessData" in exports["src/service.go"]
        assert "Service" in exports["src/service.go"]
        assert "MaxSize" in exports["src/service.go"]

    def test_go_unexported(self):
        """Go 中首字母小写的函数不应被识别为导出"""
        pool = {
            "src/helper.go": "func processData() {}\nfunc ProcessData() {}",
        }
        exports = build_export_map(pool)
        assert "src/helper.go" in exports
        assert "processData" not in exports["src/helper.go"]
        assert "ProcessData" in exports["src/helper.go"]

    def test_no_exports(self):
        pool = {
            "src/page.js": "console.log('no exports here')",
        }
        exports = build_export_map(pool)
        assert "src/page.js" not in exports

    def test_unknown_ext(self):
        pool = {
            "src/style.css": ".button { color: red; }",
        }
        exports = build_export_map(pool)
        assert "src/style.css" not in exports


class TestBuildImportMap:
    def test_js_named_import(self):
        pool = {
            "src/page.js": 'import { Button, Input } from "./components"',
        }
        imports = build_import_map(pool, Path("/project"))
        assert "src/page.js" in imports
        # 应该识别出命名导入
        named_imports = [imp for imp in imports["src/page.js"] if imp[0] == "__named_import__"]
        assert len(named_imports) > 0
        names = named_imports[0][1]
        assert "Button" in names
        assert "Input" in names

    def test_js_default_import(self):
        pool = {
            "src/app.js": 'import App from "./App"',
        }
        imports = build_import_map(pool, Path("/project"))
        assert "src/app.js" in imports
        default_imports = [imp for imp in imports["src/app.js"] if imp[0] == "__default_import__"]
        assert len(default_imports) > 0

    def test_python_import(self):
        pool = {
            "src/main.py": "from utils import helper, format_data",
        }
        imports = build_import_map(pool, Path("/project"))
        assert "src/main.py" in imports
        named = [imp for imp in imports["src/main.py"] if imp[0] == "__named_import__"]
        assert len(named) > 0
        assert "helper" in named[0][1]
        assert "format_data" in named[0][1]

    def test_no_imports(self):
        pool = {
            "src/standalone.js": "const x = 42",
        }
        imports = build_import_map(pool, Path("/project"))
        assert "src/standalone.js" not in imports


class TestBuildSymbolUsage:
    def test_all_exports_used(self):
        """所有导出都被导入 → 无未使用导出"""
        export_map = {"src/utils.js": ["formatData", "parseData"]}
        import_map = {"src/page.js": [("__named_import__", ["formatData", "parseData"])]}
        pool = {"src/utils.js": "...", "src/page.js": "..."}
        usage = build_symbol_usage(export_map, import_map, pool)
        used, unused = usage["src/utils.js"]
        assert "formatData" in used
        assert "parseData" in used
        assert len(unused) == 0

    def test_all_exports_unused(self):
        """所有导出都未被导入 → 全部未使用"""
        export_map = {"src/dead.js": ["deadFunc", "DEAD_CONST"]}
        import_map = {}  # 没有任何导入
        pool = {"src/dead.js": "..."}
        usage = build_symbol_usage(export_map, import_map, pool)
        used, unused = usage["src/dead.js"]
        assert len(used) == 0
        assert "deadFunc" in unused
        assert "DEAD_CONST" in unused

    def test_partial_exports_used(self):
        """部分导出被导入，部分未使用"""
        export_map = {"src/utils.js": ["usedFunc", "deadFunc", "DEAD_CONST"]}
        import_map = {"src/page.js": [("__named_import__", ["usedFunc"])]}
        pool = {"src/utils.js": "...", "src/page.js": "..."}
        usage = build_symbol_usage(export_map, import_map, pool)
        used, unused = usage["src/utils.js"]
        assert "usedFunc" in used
        assert "deadFunc" in unused
        assert "DEAD_CONST" in unused

    def test_no_exports(self):
        """没有导出的文件不会出现在结果中"""
        export_map = {}
        import_map = {}
        pool = {}
        usage = build_symbol_usage(export_map, import_map, pool)
        assert len(usage) == 0

    def test_cross_file_import(self):
        """A 文件的导出被 B 文件导入"""
        export_map = {
            "src/services/user.js": ["getUser", "deleteUser"],
        }
        import_map = {
            "src/page/login.js": [("__named_import__", ["getUser"])],
        }
        pool = {"src/services/user.js": "...", "src/page/login.js": "..."}
        usage = build_symbol_usage(export_map, import_map, pool)
        used, unused = usage["src/services/user.js"]
        assert "getUser" in used
        assert "deleteUser" in unused


class TestBuildBarrelMap:
    def test_js_named_reexport(self):
        """JS barrel 文件: export { Button, Input } from './components'"""
        pool = {
            "src/components/index.js": "export { Button, Input } from './components'",
            "src/components/components": "// components file",
        }
        barrel = build_barrel_map(pool)
        assert "src/components/index.js" in barrel
        assert "src/components/components" in barrel["src/components/index.js"]
        names = barrel["src/components/index.js"]["src/components/components"]
        assert "Button" in names
        assert "Input" in names

    def test_js_default_as_reexport(self):
        """JS barrel 文件: export { default as Button } from './Button'"""
        pool = {
            "src/components/index.js": "export { default as Button } from './Button'",
        }
        barrel = build_barrel_map(pool)
        assert "src/components/index.js" in barrel
        names = barrel["src/components/index.js"]["src/components/Button"]
        assert "Button" in names

    def test_js_export_star(self):
        """JS barrel 文件: export * from './utils'"""
        pool = {
            "src/utils/index.js": "export * from './helpers'",
        }
        barrel = build_barrel_map(pool)
        assert "src/utils/index.js" in barrel
        names = barrel["src/utils/index.js"]["src/utils/helpers"]
        assert "*" in names

    def test_js_export_default_from(self):
        """JS barrel 文件: export { default } from './App'"""
        pool = {
            "src/index.js": "export { default } from './App'",
        }
        barrel = build_barrel_map(pool)
        assert "src/index.js" in barrel
        names = barrel["src/index.js"]["src/App"]
        assert "__default__" in names

    def test_python_init_reexport(self):
        """Python __init__.py: from .helper import format_data"""
        pool = {
            "src/utils/__init__.py": "from .helper import format_data\nfrom .core import process",
        }
        barrel = build_barrel_map(pool)
        assert "src/utils/__init__.py" in barrel
        assert "src/utils/helper" in barrel["src/utils/__init__.py"]
        assert "src/utils/core" in barrel["src/utils/__init__.py"]
        assert "format_data" in barrel["src/utils/__init__.py"]["src/utils/helper"]
        assert "process" in barrel["src/utils/__init__.py"]["src/utils/core"]

    def test_non_barrel_file_ignored(self):
        """非 barrel 文件不应被识别为 barrel"""
        pool = {
            "src/components/Button.js": "export default function Button() {}",
        }
        barrel = build_barrel_map(pool)
        assert len(barrel) == 0

    def test_multiple_sources(self):
        """一个 barrel 文件从多个源 re-export"""
        pool = {
            "src/components/index.ts": (
                "export { Button } from './Button'\n"
                "export { Input } from './Input'\n"
            ),
        }
        barrel = build_barrel_map(pool)
        assert "src/components/index.ts" in barrel
        assert "src/components/Button" in barrel["src/components/index.ts"]
        assert "src/components/Input" in barrel["src/components/index.ts"]
        assert "Button" in barrel["src/components/index.ts"]["src/components/Button"]
        assert "Input" in barrel["src/components/index.ts"]["src/components/Input"]

    def test_rust_mod_rs(self):
        """Rust mod.rs 作为 barrel 文件"""
        pool = {
            "src/crud/mod.rs": "pub mod user;\npub mod post;",
        }
        barrel = build_barrel_map(pool)
        # Rust mod 声明不匹配 re-export 模式，但 mod.rs 应被检查
        # mod 声明不是 re-export，所以 barrel_map 可能为空
        # 这取决于实现是否处理 Rust 的 mod 声明为 re-export
        # 当前实现仅检查 JS re-export 和 Python re-export 模式
        # 所以 mod.rs 存在但没有可识别的 re-export 模式时，不在结果中
        assert "src/crud/mod.rs" not in barrel


class TestSymbolUsageWithBarrel:
    def test_barrel_reexport_marks_source_used(self):
        """源文件 A 导出 Button，barrel B re-export Button，C 从 B 导入 Button
        → A 的 Button 应被标记为 used"""
        export_map = {
            "src/components/Button.js": ["Button"],
        }
        import_map = {
            "src/page.js": [("__named_import__", ["Button"])],
        }
        pool = {
            "src/components/Button.js": "export function Button() {}",
            "src/components/index.js": "export { Button } from './Button'",
            "src/page.js": 'import { Button } from "./components"',
        }
        barrel_map = build_barrel_map(pool)
        usage = build_symbol_usage(export_map, import_map, pool, barrel_map)
        used, unused = usage["src/components/Button.js"]
        assert "Button" in used
        assert len(unused) == 0

    def test_no_barrel_file(self):
        """没有 barrel 文件时，barrel_map=None 不影响正常分析"""
        export_map = {
            "src/utils.js": ["formatData"],
        }
        import_map = {
            "src/page.js": [("__named_import__", ["formatData"])],
        }
        pool = {"src/utils.js": "...", "src/page.js": "..."}
        usage = build_symbol_usage(export_map, import_map, pool, barrel_map=None)
        used, unused = usage["src/utils.js"]
        assert "formatData" in used
        assert len(unused) == 0

    def test_barrel_reexport_unused(self):
        """源文件 A 导出 Button，barrel B re-export Button，但没有人导入 Button
        → A 的 Button 应被标记为 unused"""
        export_map = {
            "src/components/Button.js": ["Button"],
        }
        import_map = {}  # 没有任何导入
        pool = {
            "src/components/Button.js": "export function Button() {}",
            "src/components/index.js": "export { Button } from './Button'",
        }
        barrel_map = build_barrel_map(pool)
        usage = build_symbol_usage(export_map, import_map, pool, barrel_map)
        used, unused = usage["src/components/Button.js"]
        assert "Button" in unused
        assert len(used) == 0

    def test_barrel_export_star(self):
        """export * from './Y' 模式：如果消费者导入了 Y 中的某个名称，则该名称标记为 used"""
        export_map = {
            "src/utils/helpers.js": ["formatData", "parseData"],
        }
        import_map = {
            "src/page.js": [("__named_import__", ["formatData"])],
        }
        pool = {
            "src/utils/helpers.js": "export function formatData() {}\nexport function parseData() {}",
            "src/utils/index.js": "export * from './helpers'",
            "src/page.js": 'import { formatData } from "../utils"',
        }
        barrel_map = build_barrel_map(pool)
        usage = build_symbol_usage(export_map, import_map, pool, barrel_map)
        used, unused = usage["src/utils/helpers.js"]
        assert "formatData" in used
        assert "parseData" in unused

    def test_barrel_default_as_reexport(self):
        """export { default as Button } from './Button' → Button 被识别为 used"""
        export_map = {
            "src/components/Button.js": ["Button"],
        }
        import_map = {
            "src/page.js": [("__named_import__", ["Button"])],
        }
        pool = {
            "src/components/Button.js": "export default function Button() {}",
            "src/components/index.js": "export { default as Button } from './Button'",
            "src/page.js": 'import { Button } from "./components"',
        }
        barrel_map = build_barrel_map(pool)
        usage = build_symbol_usage(export_map, import_map, pool, barrel_map)
        used, unused = usage["src/components/Button.js"]
        assert "Button" in used
        assert len(unused) == 0

    def test_python_barrel_reexport(self):
        """Python __init__.py re-export 使源文件导出标记为 used"""
        export_map = {
            "src/utils/helper.py": ["format_data"],
        }
        import_map = {
            "src/main.py": [("__named_import__", ["format_data"])],
        }
        pool = {
            "src/utils/helper.py": "def format_data():\n    pass",
            "src/utils/__init__.py": "from .helper import format_data",
            "src/main.py": "from src.utils import format_data",
        }
        barrel_map = build_barrel_map(pool)
        usage = build_symbol_usage(export_map, import_map, pool, barrel_map)
        used, unused = usage["src/utils/helper.py"]
        assert "format_data" in used
        assert len(unused) == 0
