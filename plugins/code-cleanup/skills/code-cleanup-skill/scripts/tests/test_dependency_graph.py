"""单元测试：依赖图构建与可达性分析"""
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from analyze_cleanup_candidates import (
    _resolve_import_path,
    build_dependency_graph,
    build_resolver_context,
    identify_entry_points,
    find_reachable_files,
)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class TestResolveImportPath(unittest.TestCase):
    def test_exact_match(self):
        """路径精确匹配可用文件"""
        available = {"src/utils.js", "src/page.js"}
        result = _resolve_import_path("src/main.js", "./utils.js", available)
        assert result == "src/utils.js"

    def test_extension_probing_js(self):
        """无扩展名时自动探测 .js"""
        available = {"src/utils.js"}
        result = _resolve_import_path("src/main.js", "./utils", available)
        assert result == "src/utils.js"

    def test_extension_probing_vue(self):
        """自动探测 .vue"""
        available = {"src/components/Button.vue"}
        result = _resolve_import_path("src/components/page.js", "./Button", available)
        assert result == "src/components/Button.vue"

    def test_extension_probing_scss(self):
        """自动探测 .scss（co-file 边）"""
        available = {"src/page/page.scss"}
        result = _resolve_import_path("src/page/page.js", "./page.scss", available)
        assert result == "src/page/page.scss"

    def test_index_probing(self):
        """探测 index.js"""
        available = {"src/components/index.js"}
        result = _resolve_import_path("src/main.js", "./components", available)
        assert result == "src/components/index.js"

    def test_index_probing_ts(self):
        """探测 index.ts"""
        available = {"src/utils/index.ts"}
        result = _resolve_import_path("src/main.ts", "./utils", available)
        assert result == "src/utils/index.ts"

    def test_bare_module_excluded(self):
        """bare module（vue, lodash）返回 None"""
        available = {"src/main.js"}
        result = _resolve_import_path("src/main.js", "vue", available)
        assert result is None

    def test_relative_parent(self):
        """../ 父目录解析"""
        available = {"src/utils/helper.js"}
        result = _resolve_import_path("src/pages/home.js", "../utils/helper", available)
        assert result == "src/utils/helper.js"

    def test_tsconfig_baseurl_resolution(self):
        """tsconfig.baseUrl 支持无相对前缀导入"""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write(
                root / "tsconfig.json",
                """
                {
                  "compilerOptions": {
                    "baseUrl": "./src"
                  }
                }
                """,
            )
            _write(root / "src/main.ts", 'import { helper } from "utils/helper"')
            _write(root / "src/utils/helper.ts", "export const helper = () => {}")
            available = {"src/main.ts", "src/utils/helper.ts"}
            context = build_resolver_context(root, [root / "tsconfig.json"], available)
            result = _resolve_import_path("src/main.ts", "utils/helper", available, context)
            self.assertEqual(result, "src/utils/helper.ts")

    def test_tsconfig_paths_resolution(self):
        """tsconfig.paths 支持 alias 解析"""
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
            _write(root / "src/pages/home.ts", 'import { Button } from "@/components/Button"')
            _write(root / "src/components/Button.tsx", "export const Button = () => null")
            available = {"src/pages/home.ts", "src/components/Button.tsx"}
            context = build_resolver_context(root, [root / "tsconfig.json"], available)
            result = _resolve_import_path("src/pages/home.ts", "@/components/Button", available, context)
            self.assertEqual(result, "src/components/Button.tsx")

    def test_vite_alias_resolution(self):
        """vite alias 支持常见 replacement 配置"""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write(
                root / "vite.config.ts",
                """
                import { fileURLToPath, URL } from "node:url"

                export default {
                  resolve: {
                    alias: {
                      "@": fileURLToPath(new URL("./src", import.meta.url))
                    }
                  }
                }
                """,
            )
            _write(root / "src/main.ts", 'import { helper } from "@/utils/helper"')
            _write(root / "src/utils/helper.ts", "export const helper = 1")
            available = {"src/main.ts", "src/utils/helper.ts"}
            context = build_resolver_context(root, [root / "vite.config.ts"], available)
            result = _resolve_import_path("src/main.ts", "@/utils/helper", available, context)
            self.assertEqual(result, "src/utils/helper.ts")

    def test_python_absolute_import_resolution(self):
        """Python absolute import 支持常见 src 布局"""
        available = {"src/main.py", "src/utils.py"}
        context = build_resolver_context(Path.cwd(), [], available)
        result = _resolve_import_path("src/main.py", "utils", available, context)
        self.assertEqual(result, "src/utils.py")

    def test_empty_path(self):
        """空路径返回 None"""
        available = {"src/main.js"}
        result = _resolve_import_path("src/main.js", "", available)
        assert result is None

    def test_unresolvable(self):
        """无法解析的路径返回 None"""
        available = {"src/main.js"}
        result = _resolve_import_path("src/main.js", "./nonexistent", available)
        assert result is None


class TestBuildDependencyGraph(unittest.TestCase):
    def test_js_import_edge(self):
        """JS import 创建依赖边"""
        pool = {
            "src/main.js": 'import { helper } from "./utils"',
            "src/utils.js": "export function helper() {}",
        }
        available = set(pool.keys())
        forward, reverse = build_dependency_graph(pool, available)
        assert "src/utils.js" in forward.get("src/main.js", set())

    def test_css_import_edge(self):
        """CSS/SCSS import 创建依赖边（co-file 关键）"""
        pool = {
            "src/page/page.js": 'import "./page.scss"',
            "src/page/page.scss": ".button { color: red; }",
        }
        available = set(pool.keys())
        forward, reverse = build_dependency_graph(pool, available)
        assert "src/page/page.scss" in forward.get("src/page/page.js", set())

    def test_reexport_edge(self):
        """export ... from './X' 创建依赖边"""
        pool = {
            "src/components/index.js": "export { Button } from './Button'",
            "src/components/Button.js": "export function Button() {}",
        }
        available = set(pool.keys())
        forward, reverse = build_dependency_graph(pool, available)
        assert "src/components/Button.js" in forward.get("src/components/index.js", set())

    def test_bare_module_no_edge(self):
        """bare module 不创建边"""
        pool = {
            "src/main.js": 'import Vue from "vue"',
        }
        available = set(pool.keys())
        forward, reverse = build_dependency_graph(pool, available)
        assert "src/main.js" not in forward or len(forward.get("src/main.js", set())) == 0

    def test_python_import_edge(self):
        """Python import 创建依赖边"""
        pool = {
            "src/main.py": "from .utils import helper",
            "src/utils.py": "def helper(): pass",
        }
        available = set(pool.keys())
        forward, reverse = build_dependency_graph(pool, available)
        assert "src/utils.py" in forward.get("src/main.py", set())

    def test_alias_import_edge(self):
        """alias import 应写入依赖边"""
        pool = {
            "src/main.ts": 'import { helper } from "@/utils/helper"',
            "src/utils/helper.ts": "export const helper = 1",
        }
        available = set(pool.keys())
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
            context = build_resolver_context(root, [root / "tsconfig.json"], available)
            forward, reverse = build_dependency_graph(pool, available, context)
            self.assertIn("src/utils/helper.ts", forward.get("src/main.ts", set()))
            self.assertIn("src/main.ts", reverse.get("src/utils/helper.ts", set()))

    def test_python_absolute_import_edge(self):
        """Python absolute import 应写入依赖边"""
        pool = {
            "src/main.py": "from utils import helper",
            "src/utils.py": "def helper(): pass",
        }
        available = set(pool.keys())
        context = build_resolver_context(Path.cwd(), [], available)
        forward, reverse = build_dependency_graph(pool, available, context)
        self.assertIn("src/utils.py", forward.get("src/main.py", set()))

    def test_reverse_graph(self):
        """反向图正确反映被依赖关系"""
        pool = {
            "src/main.js": 'import "./page"',
            "src/page.js": 'import "./utils"',
            "src/utils.js": "export const x = 1",
        }
        available = set(pool.keys())
        forward, reverse = build_dependency_graph(pool, available)
        assert "src/main.js" in reverse.get("src/page.js", set())
        assert "src/page.js" in reverse.get("src/utils.js", set())


class TestIdentifyEntryPoints(unittest.TestCase):
    def test_keep_list_entries(self):
        """keep-list 中的文件是入口点"""
        all_rels = {"src/main.js", "src/utils.js", "src/page.js"}
        keep_list = {"src/main.js"}
        entries = identify_entry_points(all_rels, keep_list)
        assert "src/main.js" in entries

    def test_default_keep_entries(self):
        """默认保护文件（router.js 等）是入口点"""
        all_rels = {"src/router.js", "src/utils.js", "src/App.vue"}
        keep_list = set()
        entries = identify_entry_points(all_rels, keep_list)
        assert "src/router.js" in entries
        assert "src/App.vue" in entries

    def test_html_not_auto_entry(self):
        """HTML 文件不是自动入口点（Vue 2 中是 co-file）"""
        all_rels = {"src/page/home/home.html", "src/page/home/home.js"}
        keep_list = set()
        entries = identify_entry_points(all_rels, keep_list)
        assert "src/page/home/home.html" not in entries
        assert "src/page/home/home.js" not in entries

    def test_no_duplicate(self):
        """keep-list + 默认保护不重复"""
        all_rels = {"src/main.js"}
        keep_list = {"src/main.js"}
        entries = identify_entry_points(all_rels, keep_list)
        assert len(entries) == 1


class TestFindReachableFiles(unittest.TestCase):
    def test_simple_chain(self):
        """简单链式依赖：main → page → utils，都可达"""
        graph = {
            "src/main.js": {"src/page.js"},
            "src/page.js": {"src/utils.js"},
            "src/utils.js": set(),
        }
        reachable = find_reachable_files(graph, {"src/main.js"})
        assert reachable == {"src/main.js", "src/page.js", "src/utils.js"}

    def test_unreachable_branch(self):
        """不可达分支：dead.js 不在从入口可达的路径上"""
        graph = {
            "src/main.js": {"src/page.js"},
            "src/page.js": set(),
            "src/dead.js": {"src/dead-utils.js"},
            "src/dead-utils.js": set(),
        }
        reachable = find_reachable_files(graph, {"src/main.js"})
        assert "src/dead.js" not in reachable
        assert "src/dead-utils.js" not in reachable

    def test_co_file_grouping(self):
        """co-file: page.js → page.scss，page.js 不可达则 page.scss 也不可达"""
        graph = {
            "src/main.js": set(),
            "src/page/page.js": {"src/page/page.scss", "src/page/page.html"},
            "src/page/page.scss": set(),
            "src/page/page.html": set(),
        }
        reachable = find_reachable_files(graph, {"src/main.js"})
        assert "src/page/page.js" not in reachable
        assert "src/page/page.scss" not in reachable
        assert "src/page/page.html" not in reachable

    def test_co_file_reachable(self):
        """co-file: page.js 被引用则 page.scss 也可达"""
        graph = {
            "src/main.js": {"src/page/page.js"},
            "src/page/page.js": {"src/page/page.scss"},
            "src/page/page.scss": set(),
        }
        reachable = find_reachable_files(graph, {"src/main.js"})
        assert "src/page/page.js" in reachable
        assert "src/page/page.scss" in reachable

    def test_multiple_entries(self):
        """多个入口点，各自可达不同子图"""
        graph = {
            "src/main.js": {"src/pageA.js"},
            "src/pageA.js": set(),
            "src/admin.js": {"src/pageB.js"},
            "src/pageB.js": set(),
            "src/dead.js": set(),
        }
        reachable = find_reachable_files(graph, {"src/main.js", "src/admin.js"})
        assert "src/pageA.js" in reachable
        assert "src/pageB.js" in reachable
        assert "src/dead.js" not in reachable

    def test_empty_graph(self):
        """空图"""
        reachable = find_reachable_files({}, {"src/main.js"})
        assert reachable == {"src/main.js"}

    def test_cycle(self):
        """循环依赖不会无限循环"""
        graph = {
            "src/a.js": {"src/b.js"},
            "src/b.js": {"src/a.js"},
        }
        reachable = find_reachable_files(graph, {"src/a.js"})
        assert reachable == {"src/a.js", "src/b.js"}

    def test_diamond_dependency(self):
        """菱形依赖：A → B, A → C, B → D, C → D"""
        graph = {
            "src/a.js": {"src/b.js", "src/c.js"},
            "src/b.js": {"src/d.js"},
            "src/c.js": {"src/d.js"},
            "src/d.js": set(),
        }
        reachable = find_reachable_files(graph, {"src/a.js"})
        assert reachable == {"src/a.js", "src/b.js", "src/c.js", "src/d.js"}
