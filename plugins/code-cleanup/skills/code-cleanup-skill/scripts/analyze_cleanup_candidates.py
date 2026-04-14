#!/usr/bin/env python3
import argparse
import json
import re
import os
import sys
import subprocess
import fnmatch
from collections import deque
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set, Tuple


def log_progress(msg: str):
    """向 stderr 输出带有颜色标记的进度日志。"""
    print(f"\033[90m[Cleanup Scan] {msg}\033[0m", file=sys.stderr, flush=True)


CODE_EXTS = {".js", ".ts", ".vue", ".jsx", ".tsx", ".html", ".json", ".scss", ".css", ".less",
             ".py", ".go", ".java", ".php", ".rb", ".rs", ".c", ".cpp", ".h", ".hpp"}
IGNORE_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".cursor",
    ".idea",
    ".vscode",
    "static/lib",
    "__pycache__",
    "vendor",
    ".venv",
    "venv",
    "target",
    ".skill-workspace",
}

# 常见编程语言的 import/require 语法模式
IMPORT_PATTERNS = [
    # JS / TS / Vue
    (
        {".js", ".ts", ".jsx", ".tsx", ".vue"},
        [
            re.compile(r"import\s+.*?\s+from\s+['\"]", re.IGNORECASE),
            re.compile(r"import\s+['\"]", re.IGNORECASE),
            re.compile(r"require\s*\(\s*['\"]", re.IGNORECASE),
            re.compile(r"import\s*\(\s*['\"]", re.IGNORECASE),
        ],
    ),
    # Python
    (
        {".py"},
        [
            re.compile(r"import\s+", re.IGNORECASE),
            re.compile(r"from\s+.*?\s+import\s+", re.IGNORECASE),
        ],
    ),
    # Go
    (
        {".go"},
        [
            re.compile(r'import\s+(?:\w+\s+)?"', re.IGNORECASE),
            re.compile(r"\(\s*['\"]", re.IGNORECASE),
        ],
    ),
    # Java
    (
        {".java"},
        [
            re.compile(r"import\s+[\w.]+;", re.IGNORECASE),
        ],
    ),
    # PHP
    (
        {".php"},
        [
            re.compile(r"(?:require_once|include_once|require|include|use)\s+['\"]", re.IGNORECASE),
            re.compile(r"use\s+[\w\\]+;", re.IGNORECASE),
        ],
    ),
    # C / C++
    (
        {".c", ".cpp", ".h", ".hpp"},
        [
            re.compile(r'#include\s+["<]', re.IGNORECASE),
        ],
    ),
    # Ruby
    (
        {".rb"},
        [
            re.compile(r"(?:require|require_relative|load)\s+['\"]", re.IGNORECASE),
        ],
    ),
    # Rust
    (
        {".rs"},
        [
            re.compile(r"use\s+[\w:]+;", re.IGNORECASE),
            re.compile(r"mod\s+\w+", re.IGNORECASE),
        ],
    ),
]

# 为快速查找构建 ext -> patterns 索引
_EXT_IMPORT_INDEX: Dict[str, List[re.Pattern]] = {}
for exts, patterns in IMPORT_PATTERNS:
    for ext in exts:
        _EXT_IMPORT_INDEX[ext] = patterns


@dataclass
class Candidate:
    path: str
    category: str
    risk_level: str
    evidence: List[str]
    file_size_bytes: int = 0
    suggested_action: str = "delete_after_confirm"
    total_exports: int = 0
    used_exports: Optional[List[str]] = None
    unused_exports: Optional[List[str]] = None


@dataclass
class ScanDir:
    dir_path: str  # 相对路径，如 src/page
    category: str  # 如 unused_page
    # 额外关键词提取策略: "stem"=文件名, "parent"=父目录名, "tag"=kebab-case 标签名, "name"=完整文件名
    keyword_hints: List[str]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def normalize_rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


def load_gitignore_patterns(root: Path) -> List[str]:
    """向上查找并加载所有 .gitignore 模式。"""
    patterns = []
    current = root.resolve()
    while True:
        gitignore_path = current / ".gitignore"
        if gitignore_path.is_file():
            try:
                with gitignore_path.open("r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            patterns.append(line)
            except Exception:
                pass
        parent = current.parent
        if parent == current:
            break
        current = parent
    return patterns


def is_ignored(path_str: str, patterns: List[str]) -> bool:
    """检查路径是否匹配 .gitignore 模式（简单实现）。"""
    for pattern in patterns:
        if pattern.endswith("/"):
            pattern = pattern[:-1]
        # 支持相对路径匹配和文件名匹配
        if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(path_str.split("/")[-1], pattern) or \
           fnmatch.fnmatch(path_str, f"*/{pattern}"):
            return True
    return False


def collect_files(root: Path) -> Tuple[List[Path], Dict[str, int]]:
    """获取项目中的所有非忽略文件列表，同时统计全局扫描指标。"""
    files: List[Path] = []
    stats = {"total_files_scanned": 0, "total_size_bytes": 0}
    
    def add_file(p: Path):
        if p.is_file():
            rel_path = normalize_rel(p, root)
            stats["total_files_scanned"] += 1
            stats["total_size_bytes"] += p.stat().st_size
            files.append(p)

    # 1. 优先尝试使用 Git 命令获取文件列表 (自动支持 .gitignore)
    try:
        cmd1 = ["git", "ls-files"]
        res1 = subprocess.run(cmd1, cwd=root, capture_output=True, text=True, check=True)
        
        cmd2 = ["git", "ls-files", "--others", "--exclude-standard"]
        res2 = subprocess.run(cmd2, cwd=root, capture_output=True, text=True, check=True)
        
        all_git_files = res1.stdout.splitlines() + res2.stdout.splitlines()
        
        for rel_path in all_git_files:
            if not rel_path:
                continue
            if any(rel_path == x or rel_path.startswith(f"{x}/") for x in IGNORE_DIRS):
                continue
            add_file(root / rel_path)
                
        if files:
            return files, stats
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # 2. Fallback to os.walk
    ignore_patterns = load_gitignore_patterns(root)
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace("\\", "/")
        if rel_dir == ".": rel_dir = ""
            
        i = len(dirnames) - 1
        while i >= 0:
            d = dirnames[i]
            d_rel = f"{rel_dir}/{d}" if rel_dir else d
            if d in IGNORE_DIRS or is_ignored(d_rel, ignore_patterns):
                del dirnames[i]
            i -= 1
            
        for f in filenames:
            f_rel = f"{rel_dir}/{f}" if rel_dir else f
            if f in IGNORE_DIRS or is_ignored(f_rel, ignore_patterns):
                continue
            add_file(Path(dirpath) / f)

    return files, stats


def build_reference_pool(files: Sequence[Path], root: Path, exts: Set[str]) -> Dict[str, str]:
    """构建引用池：仅读取符合代码扩展名的文件内容。"""
    pool = {}
    for file in files:
        if file.suffix.lower() in exts:
            rel = normalize_rel(file, root)
            # log_progress(f"  Reading into pool: {rel}")
            pool[rel] = read_text(file)
    return pool

# ── 导出/导入符号分析 ──────────────────────────────────────────────
# 正则提取每个文件的导出符号和导入符号，用于符号级使用追踪

# JS/TS 导出模式
_JS_EXPORT_PATTERNS = [
    re.compile(r'export\s+default\s+function\s+(\w+)'),           # export default function Name
    re.compile(r'export\s+default\s+class\s+(\w+)'),             # export default class Name
    re.compile(r'export\s+(?:default\s+)?(?:const|let|var|function|class)\s+(\w+)'),  # export const/let/var/function/class Name
    re.compile(r'export\s+\{([^}]+)\}'),                          # export { Name1, Name2 }
    re.compile(r'module\.exports\s*=\s*(\w+)'),                   # module.exports = Name
    re.compile(r'exports\.(\w+)\s*='),                            # exports.Name =
]
# Python 导出模式（简化：顶层 def 和 class）
_PY_EXPORT_PATTERNS = [
    re.compile(r'^def\s+(\w+)', re.MULTILINE),
    re.compile(r'^class\s+(\w+)', re.MULTILINE),
    re.compile(r'^(\w+)\s*=\s*', re.MULTILINE),  # 顶层变量赋值
]
# Go 导出模式（首字母大写的函数/类型/变量）
_GO_EXPORT_PATTERNS = [
    re.compile(r'^func\s+([A-Z]\w+)', re.MULTILINE),
    re.compile(r'^type\s+([A-Z]\w+)', re.MULTILINE),
    re.compile(r'^var\s+([A-Z]\w+)', re.MULTILINE),
    re.compile(r'^const\s+([A-Z]\w+)', re.MULTILINE),
]
# Java 导出模式（public class/interface）
_JAVA_EXPORT_PATTERNS = [
    re.compile(r'public\s+(?:class|interface|enum)\s+(\w+)'),
]
# Rust 导出模式（pub fn/struct/enum/trait）
_RUST_EXPORT_PATTERNS = [
    re.compile(r'pub\s+fn\s+(\w+)'),
    re.compile(r'pub\s+struct\s+(\w+)'),
    re.compile(r'pub\s+enum\s+(\w+)'),
    re.compile(r'pub\s+trait\s+(\w+)'),
]
# C/C++ 导出模式（简化：函数定义）
_C_EXPORT_PATTERNS = [
    re.compile(r'(?:^|\n)\w[\w\s*]+\s+(\w+)\s*\([^)]*\)\s*\{', re.MULTILINE),
]

_EXPORT_PATTERNS_MAP: Dict[str, List[re.Pattern]] = {
    ".js": _JS_EXPORT_PATTERNS, ".ts": _JS_EXPORT_PATTERNS,
    ".jsx": _JS_EXPORT_PATTERNS, ".tsx": _JS_EXPORT_PATTERNS,
    ".vue": _JS_EXPORT_PATTERNS,
    ".py": _PY_EXPORT_PATTERNS,
    ".go": _GO_EXPORT_PATTERNS,
    ".java": _JAVA_EXPORT_PATTERNS,
    ".rs": _RUST_EXPORT_PATTERNS,
    ".c": _C_EXPORT_PATTERNS, ".cpp": _C_EXPORT_PATTERNS,
    ".h": _C_EXPORT_PATTERNS, ".hpp": _C_EXPORT_PATTERNS,
}

# JS/TS 导入模式（提取导入的符号名称）
_JS_IMPORT_NAME_PATTERNS = [
    re.compile(r'import\s+\{([^}]+)\}\s+from', re.DOTALL),       # import { A, B } from
    re.compile(r'import\s+(\w+)\s+from', re.DOTALL),              # import Name from
    re.compile(r'import\s+(\w+)\s*$', re.MULTILINE),              # import 'module' (无名称)
    re.compile(r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'),       # require('module')
]
_PY_IMPORT_NAME_PATTERNS = [
    re.compile(r'from\s+[\w.]+\s+import\s+(.+?)(?:\s*$|\s*#)', re.MULTILINE),
    re.compile(r'import\s+([\w.]+)', re.MULTILINE),
]
_GO_IMPORT_NAME_PATTERNS = [
    re.compile(r'import\s+"([^"]+)"'),
]
_JAVA_IMPORT_NAME_PATTERNS = [
    re.compile(r'import\s+([\w.]+)\s*;'),
]
_RUST_IMPORT_NAME_PATTERNS = [
    re.compile(r'use\s+([\w:]+)\s*;'),
]
_C_IMPORT_NAME_PATTERNS = [
    re.compile(r'#include\s*[<"]([^>"]+)[>"]'),
]

_IMPORT_PATTERNS_MAP: Dict[str, List[re.Pattern]] = {
    ".js": _JS_IMPORT_NAME_PATTERNS, ".ts": _JS_IMPORT_NAME_PATTERNS,
    ".jsx": _JS_IMPORT_NAME_PATTERNS, ".tsx": _JS_IMPORT_NAME_PATTERNS,
    ".vue": _JS_IMPORT_NAME_PATTERNS,
    ".py": _PY_IMPORT_NAME_PATTERNS,
    ".go": _GO_IMPORT_NAME_PATTERNS,
    ".java": _JAVA_IMPORT_NAME_PATTERNS,
    ".rs": _RUST_IMPORT_NAME_PATTERNS,
    ".c": _C_IMPORT_NAME_PATTERNS, ".cpp": _C_IMPORT_NAME_PATTERNS,
    ".h": _C_IMPORT_NAME_PATTERNS, ".hpp": _C_IMPORT_NAME_PATTERNS,
}


def build_export_map(reference_pool: Dict[str, str]) -> Dict[str, List[str]]:
    """分析每个代码文件，提取其导出符号名称。

    返回: { rel_path: [export_name1, export_name2, ...] }
    """
    export_map: Dict[str, List[str]] = {}
    for rel, text in reference_pool.items():
        ext = Path(rel).suffix.lower()
        patterns = _EXPORT_PATTERNS_MAP.get(ext)
        if not patterns:
            continue
        names: List[str] = []
        for pattern in patterns:
            for m in pattern.finditer(text):
                group = m.group(1)
                # export { A, B as C } → 提取每个名称
                if "," in group:
                    for part in group.split(","):
                        name = part.strip().split(" as ")[-1].strip()
                        if name and name not in names:
                            names.append(name)
                else:
                    name = group.strip()
                    if name and name not in names:
                        names.append(name)
        if names:
            export_map[rel] = names
    return export_map


def build_import_map(reference_pool: Dict[str, str], root: Path) -> Dict[str, List[Tuple[str, List[str]]]]:
    """分析每个代码文件，提取其导入的模块路径和符号名称。

    返回: { source_rel: [(module_path, [imported_names]), ...] }
    其中 module_path 是尝试解析后的相对路径。
    """
    import_map: Dict[str, List[Tuple[str, List[str]]]] = {}
    for rel, text in reference_pool.items():
        ext = Path(rel).suffix.lower()
        patterns = _IMPORT_PATTERNS_MAP.get(ext)
        if not patterns:
            continue
        imports: List[Tuple[str, List[str]]] = []
        for pattern in patterns:
            for m in pattern.finditer(text):
                group = m.group(1).strip()
                if not group:
                    continue
                # 区分模块路径和导入名称
                if ext in (".js", ".ts", ".jsx", ".tsx", ".vue"):
                    # JS/TS: 模式已经匹配了具体部分
                    # _JS_IMPORT_NAME_PATTERNS[0] 匹配 { A, B }
                    if pattern is _JS_IMPORT_NAME_PATTERNS[0]:
                        names = [n.strip().split(" as ")[-1].strip() for n in group.split(",") if n.strip()]
                        imports.append(("__named_import__", names))
                    elif pattern is _JS_IMPORT_NAME_PATTERNS[1]:
                        imports.append(("__default_import__", [group]))
                    elif pattern is _JS_IMPORT_NAME_PATTERNS[3]:
                        # require('module') → 提取模块路径
                        imports.append((group, ["*"]))
                    else:
                        continue
                elif ext == ".py":
                    if "," in group or (group and group[0].isalpha() and not group.startswith("import")):
                        # from X import A, B → group = "A, B" (逗号分隔的名称列表)
                        # from X import helper → group = "helper" (单个名称)
                        names = [n.strip().split(" as ")[-1].strip() for n in group.split(",") if n.strip()]
                        imports.append(("__named_import__", names))
                    else:
                        # import X → 提取模块名
                        imports.append((group, ["*"]))
                else:
                    # 其他语言：提取模块路径
                    imports.append((group, ["*"]))
        if imports:
            import_map[rel] = imports
    return import_map


# ── Barrel/Index 文件分析 ──────────────────────────────────────────
# 识别 barrel 文件并提取其 re-export 映射关系

_BARREL_FILENAMES = {"index.js", "index.ts", "index.vue", "index.jsx", "index.tsx",
                     "__init__.py", "mod.rs"}

# JS/TS re-export 模式
_JS_REEXPORT_PATTERNS = [
    # export { default as X } from './Y'
    re.compile(r"export\s+\{\s*default\s+as\s+(\w+)\s*\}\s+from\s+['\"]([^'\"]+)['\"]", re.MULTILINE),
    # export { A, B } from './Y'
    re.compile(r"export\s+\{([^}]+)\}\s+from\s+['\"]([^'\"]+)['\"]", re.MULTILINE),
    # export * from './Y'
    re.compile(r"export\s+\*\s+from\s+['\"]([^'\"]+)['\"]", re.MULTILINE),
    # export { default } from './Y'
    re.compile(r"export\s+\{\s*default\s*\}\s+from\s+['\"]([^'\"]+)['\"]", re.MULTILINE),
]
# Python __init__.py re-export 模式
_PY_REEXPORT_PATTERNS = [
    # from .Y import X
    re.compile(r"from\s+\.(\w+)\s+import\s+(.+?)(?:\s*$|\s*#)", re.MULTILINE),
]


def _resolve_relative_import(source_rel: str, import_path: str) -> Optional[str]:
    """将相对导入路径解析为 reference_pool 中的相对路径。

    Args:
        source_rel: 发起 import 的文件的相对路径 (e.g. 'src/components/index.js')
        import_path: import 语句中的路径 (e.g. './Button')

    Returns:
        解析后的相对路径 (e.g. 'src/components/Button')，如果无法解析则返回 None
    """
    if not import_path.startswith("."):
        return None

    # 获取源文件所在目录
    source_dir = str(Path(source_rel).parent)
    if source_dir == ".":
        source_dir = ""

    # 去除前导的 ./ 或 ../ 或 . 前缀
    parts = import_path.replace("\\", "/")
    while parts.startswith("./"):
        parts = parts[2:]
    while parts.startswith("../"):
        # 上一级目录
        if source_dir:
            source_dir = str(Path(source_dir).parent)
            if source_dir == ".":
                source_dir = ""
        parts = parts[3:]
    if parts.startswith("."):
        parts = parts[1:]

    resolved = str(Path(f"{source_dir}/{parts}".lstrip("/"))).replace("\\", "/") if parts else None

    return resolved if resolved else None


# ── 依赖图构建与可达性分析 ──────────────────────────────────────────

# 路径解析时尝试的扩展名（按常见度排序）
_RESOLVE_EXTENSIONS = [".js", ".ts", ".vue", ".jsx", ".tsx", ".scss", ".css", ".less", ".py", ".go", ".java", ".rb", ".rs", ".c", ".cpp", ".h", ".hpp"]
_RESOLVE_INDEX_NAMES = [f"index{ext}" for ext in _RESOLVE_EXTENSIONS]


def _resolve_import_path(
    source_rel: str,
    import_path: str,
    available_files: Set[str],
) -> Optional[str]:
    """将 import 语句中的路径解析为 reference_pool 中的实际文件路径。

    解析策略（按优先级）：
    1. 精确匹配 import_path 在 available_files 中
    2. 扩展名探测：依次尝试 .js, .ts, .vue, .jsx, .tsx, .scss, .css, .less
    3. Index 探测：路径 + /index.js, /index.ts 等

    Args:
        source_rel: 发起 import 的文件的相对路径
        import_path: import 语句中的原始路径
        available_files: reference_pool 中所有可用文件的相对路径集合

    Returns:
        解析后的相对路径，无法解析则返回 None
    """
    if not import_path:
        return None

    # 排除 bare module 导入（vue, vant, lodash 等）
    clean = import_path.strip("'\"")
    if not clean.startswith("."):
        return None

    # 先用现有的 _resolve_relative_import 解析相对路径
    resolved = _resolve_relative_import(source_rel, clean)
    if not resolved:
        return None

    # 1. 精确匹配
    if resolved in available_files:
        return resolved

    # 2. 扩展名探测
    for ext in _RESOLVE_EXTENSIONS:
        candidate = resolved + ext
        if candidate in available_files:
            return candidate

    # 3. Index 探测
    for idx_name in _RESOLVE_INDEX_NAMES:
        candidate = resolved + "/" + idx_name
        if candidate in available_files:
            return candidate

    return None


def build_dependency_graph(
    reference_pool: Dict[str, str],
    available_files: Set[str],
) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """构建文件依赖图（有向邻接表）。

    使用正则提取 import 路径，通过 _resolve_import_path 解析为实际文件，
    构建正/反向邻接表用于后续可达性分析。

    Returns:
        forward:  { file_rel: Set[被该文件导入的目标文件rel] }
        reverse:  { file_rel: Set[导入了该文件的源文件rel] }
    """
    forward: Dict[str, Set[str]] = {}
    reverse: Dict[str, Set[str]] = {}

    # 提取所有 import 路径的正则（跨语言通用）
    _IMPORT_PATH_PATTERNS = [
        # JS/TS: import X from 'path' / import { X } from 'path'
        re.compile(r"""^\s*import\s+.*?\s+from\s+['"]([^'"]+)['"]""", re.MULTILINE),
        # JS/TS: import('path') / require('path')
        re.compile(r"""(?:import|require)\s*\(\s*['"]([^'"]+)['"]""", re.MULTILINE),
        # JS/TS: import 'path' (副作用导入)
        re.compile(r"""^\s*import\s+['"]([^'"]+)['"]""", re.MULTILINE),
        # JS/TS re-export: export ... from 'path'
        re.compile(r"""export\s+(?:\{[^}]*\}\s+from|\*\s+from)\s+['"]([^'"]+)['"]""", re.MULTILINE),
        # Python: from .xxx import / import xxx
        re.compile(r"^\s*(?:from\s+(\.[\w.]+)\s+import|import\s+([\w.]+))", re.MULTILINE),
        # Go: import "path"
        re.compile(r'import\s+(?:\w+\s+)?"([^"]+)"', re.MULTILINE),
        # Java: import pkg.Class
        re.compile(r"import\s+([\w.]+)\s*;", re.MULTILINE),
        # C/C++: #include "path"
        re.compile(r'#include\s+"([^"]+)"', re.MULTILINE),
        # Ruby: require 'path'
        re.compile(r"(?:require|require_relative|load)\s+['\"]([^'\"]+)['\"]", re.MULTILINE),
        # Rust: use path; mod name
        re.compile(r"use\s+([\w:]+)\s*;", re.MULTILINE),
        # CSS/SCSS: @import 'path', @use 'path'
        re.compile(r"@(?:import|use)\s+['\"]([^'\"]+)['\"]", re.MULTILINE),
    ]

    def _add_edge(src: str, dst: str):
        forward.setdefault(src, set()).add(dst)
        reverse.setdefault(dst, set()).add(src)

    for rel, text in reference_pool.items():
        for pattern in _IMPORT_PATH_PATTERNS:
            for m in pattern.finditer(text):
                # Python import 可能匹配 group 1 或 group 2
                raw_path = m.group(1) or (m.group(2) if m.lastindex >= 2 else None)
                if not raw_path:
                    continue
                raw_path = raw_path.strip()
                resolved = _resolve_import_path(rel, raw_path, available_files)
                if resolved:
                    _add_edge(rel, resolved)

    return forward, reverse


def identify_entry_points(
    all_rels: Set[str],
    keep_list: Set[str],
) -> Set[str]:
    """识别依赖图的入口点。

    入口点来源：
    1. keep-list 中的文件
    2. _DEFAULT_KEEP_PATTERNS 匹配的文件（main.js, router.js 等）

    注意：HTML 文件在 Vue 2 多页应用中是 co-file（与 .js/.scss 同组），
    不应作为独立入口点，否则会阻止整个 co-file 组被标记为未使用。

    Args:
        all_rels: 所有文件的相对路径集合
        keep_list: 白名单文件集合

    Returns:
        入口点文件集合
    """
    entry_points: Set[str] = set()

    for rel in all_rels:
        # keep-list 中的文件
        if rel in keep_list:
            entry_points.add(rel)
            continue

        # 默认保护文件也是入口点
        if _is_default_keep(rel):
            entry_points.add(rel)

    return entry_points


def find_reachable_files(
    forward_graph: Dict[str, Set[str]],
    entry_points: Set[str],
) -> Set[str]:
    """从入口点 BFS 遍历依赖图，返回所有可达文件。

    Args:
        forward_graph: 正向邻接表 { file: Set[imports] }
        entry_points: 入口文件集合

    Returns:
        从入口点可达的所有文件集合
    """
    visited: Set[str] = set()
    queue = deque(entry_points)

    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in forward_graph.get(node, set()):
            if neighbor not in visited:
                queue.append(neighbor)

    return visited


def build_barrel_map(reference_pool: Dict[str, str]) -> Dict[str, Dict[str, List[str]]]:
    """识别 barrel/index 文件并提取 re-export 映射。

    返回: { barrel_rel: { source_rel: [exported_name1, exported_name2, ...] } }
    其中 barrel_rel 是 barrel 文件的相对路径，source_rel 是被 re-export 的源文件路径，
    exported_name 列表是从该源文件 re-export 出的符号名称。
    特殊值 '*' 表示 re-export 全部（export * from './Y'）。
    特殊值 '__default__' 表示 re-export 默认导出（export { default } from './Y'）。
    """
    barrel_map: Dict[str, Dict[str, List[str]]] = {}

    for rel, text in reference_pool.items():
        filename = Path(rel).name
        if filename not in _BARREL_FILENAMES:
            continue

        reexports: Dict[str, List[str]] = {}
        ext = Path(rel).suffix.lower()

        if ext in (".js", ".ts", ".jsx", ".tsx", ".vue"):
            for pattern in _JS_REEXPORT_PATTERNS:
                for m in pattern.finditer(text):
                    # export { default as X } from './Y'  → groups: (X, ./Y)
                    if pattern is _JS_REEXPORT_PATTERNS[0]:
                        exported_name = m.group(1).strip()
                        source_path = m.group(2).strip()
                        source_rel = _resolve_relative_import(rel, source_path)
                        if source_rel:
                            reexports.setdefault(source_rel, []).append(exported_name)

                    # export { A, B } from './Y'  → groups: (A, B, ./Y)
                    elif pattern is _JS_REEXPORT_PATTERNS[1]:
                        names_str = m.group(1).strip()
                        source_path = m.group(2).strip()
                        source_rel = _resolve_relative_import(rel, source_path)
                        if source_rel:
                            names = [n.strip().split(" as ")[-1].strip()
                                     for n in names_str.split(",") if n.strip()]
                            # 跳过 "default as X"（已被第一个模式匹配）
                            names = [n for n in names if n != "default"]
                            if names:
                                reexports.setdefault(source_rel, []).extend(names)

                    # export * from './Y'  → groups: (./Y)
                    elif pattern is _JS_REEXPORT_PATTERNS[2]:
                        source_path = m.group(1).strip()
                        source_rel = _resolve_relative_import(rel, source_path)
                        if source_rel:
                            reexports.setdefault(source_rel, []).append("*")

                    # export { default } from './Y'  → groups: (./Y)
                    elif pattern is _JS_REEXPORT_PATTERNS[3]:
                        source_path = m.group(1).strip()
                        source_rel = _resolve_relative_import(rel, source_path)
                        if source_rel:
                            reexports.setdefault(source_rel, []).append("__default__")

        elif ext == ".py":
            for pattern in _PY_REEXPORT_PATTERNS:
                for m in pattern.finditer(text):
                    # from .Y import X, Z  → groups: (Y, X, Z)
                    module_name = m.group(1).strip()
                    names_str = m.group(2).strip()
                    source_rel = _resolve_relative_import(rel, f".{module_name}")
                    if source_rel:
                        names = [n.strip().split(" as ")[-1].strip()
                                 for n in names_str.split(",") if n.strip()]
                        if names:
                            reexports.setdefault(source_rel, []).extend(names)

        if reexports:
            barrel_map[rel] = reexports
            log_progress(f"  Barrel file detected: {rel} -> {list(reexports.keys())}")

    return barrel_map


# ── 配置驱动注册检测 ──────────────────────────────────────────────
# 检测通过配置文件、glob 导入、动态注册等方式引用的模块

# 框架特定的注册模式
_CONFIG_REF_PATTERNS = [
    # Vite glob import
    re.compile(r"import\.meta\.glob\s*\(\s*['\"]([^'\"]+)['\"]", re.MULTILINE),
    # Webpack require.context
    re.compile(r"require\.context\s*\(\s*['\"]([^'\"]+)['\"]", re.MULTILINE),
    # Vue app.component('Name', ...)
    re.compile(r"(?:app|Vue)\.component\s*\(\s*['\"](\w+)['\"]", re.MULTILINE),
    # Vue app.use(module)
    re.compile(r"(?:app|Vue)\.use\s*\(\s*(\w+)", re.MULTILINE),
    # Angular module registration
    re.compile(r"declarations\s*:\s*\[([^\]]+)\]", re.MULTILINE),
    # Next.js dynamic import
    re.compile(r"dynamic\s*\(\s*\(\s*\)\s*=>\s*import\s*\(\s*['\"]([^'\"]+)['\"]", re.MULTILINE),
]

# 配置文件名模式
_CONFIG_FILE_PATTERNS = [
    re.compile(r"vite\.config\.", re.IGNORECASE),
    re.compile(r"webpack\.config\.", re.IGNORECASE),
    re.compile(r"nuxt\.config\.", re.IGNORECASE),
    re.compile(r"vue\.config\.", re.IGNORECASE),
    re.compile(r"next\.config\.", re.IGNORECASE),
    re.compile(r"angular\.json$", re.IGNORECASE),
    re.compile(r"tailwind\.config\.", re.IGNORECASE),
    re.compile(r"\.storybook[/\\]"),
]


def build_config_driven_refs(reference_pool: Dict[str, str]) -> Dict[str, List[str]]:
    """检测通过配置驱动方式引用的模块。

    返回: { source_rel: [evidence1, evidence2, ...] }
    source_rel 是被配置驱动引用的文件路径，
    evidence 描述引用方式（如 "Vite glob import: ./components/*.vue"）。
    """
    config_refs: Dict[str, List[str]] = {}

    for rel, text in reference_pool.items():
        # 检查配置文件模式
        is_config = any(p.search(rel) for p in _CONFIG_FILE_PATTERNS)

        for pattern in _CONFIG_REF_PATTERNS:
            for m in pattern.finditer(text):
                matched = m.group(1).strip()
                if not matched:
                    continue

                # 对 glob 模式（含 * 或 **），查找匹配的文件
                if "*" in matched or "**" in matched:
                    evidence = f"配置驱动引用 (glob): {matched} (来自 {rel})"
                    # glob 匹配到的文件标记为被配置引用
                    glob_prefix = matched.replace("**", "").replace("*", "").strip("/\\")
                    if glob_prefix:
                        for other_rel in reference_pool:
                            if other_rel.startswith(glob_prefix):
                                config_refs.setdefault(other_rel, []).append(evidence)
                else:
                    # 直接名称引用（如 app.component('MyButton', ...)）
                    evidence = f"配置驱动引用 (名称): {matched} (来自 {rel})"
                    # 搜索文件名或导出名匹配的文件
                    for other_rel in reference_pool:
                        stem = Path(other_rel).stem
                        if stem == matched or matched in other_rel:
                            config_refs.setdefault(other_rel, []).append(evidence)

    return config_refs


def build_symbol_usage(export_map: Dict[str, List[str]], import_map: Dict[str, List[Tuple[str, List[str]]]], reference_pool: Dict[str, str], barrel_map: Optional[Dict[str, Dict[str, List[str]]]] = None) -> Dict[str, Tuple[List[str], List[str]]]:
    """交叉比对导出和导入，计算每个文件的符号使用情况。

    支持 barrel 文件间接引用：如果源文件 A 的导出通过 barrel 文件 B 被 C 文件导入，
    则 A 的导出也会被标记为 "used"。

    返回: { rel_path: (used_exports, unused_exports) }
    """
    result: Dict[str, Tuple[List[str], List[str]]] = {}

    # 收集所有导入的符号名称（跨所有文件的并集）
    all_imported_names: Set[str] = set()
    for rel, imports in import_map.items():
        for module_path, names in imports:
            for name in names:
                if name not in ("*", "__named_import__", "__default_import__"):
                    all_imported_names.add(name)

    # 收集通过 barrel 文件间接使用的导出名称
    # barrel_used: { source_rel: Set[str] }  源文件中被 barrel re-export 且最终被消费的符号
    barrel_used: Dict[str, Set[str]] = {}
    if barrel_map:
        for barrel_rel, sources in barrel_map.items():
            # 收集哪些符号从 barrel 文件被其他文件导入
            barrel_imported_names: Set[str] = set()
            for imp_rel, imports in import_map.items():
                if imp_rel == barrel_rel:
                    continue
                for _module_path, names in imports:
                    for name in names:
                        if name not in ("*", "__named_import__", "__default_import__"):
                            barrel_imported_names.add(name)

            for source_rel, exported_names in sources.items():
                if source_rel not in barrel_used:
                    barrel_used[source_rel] = set()
                for exported_name in exported_names:
                    if exported_name == "*":
                        # export * from './Y' → 所有从 Y 导入的名称都视为被使用
                        # 检查 barrel 被导入时使用的名称中，是否有来自 source 的导出
                        source_exports = export_map.get(source_rel, [])
                        for se in source_exports:
                            if se in barrel_imported_names:
                                barrel_used[source_rel].add(se)
                    elif exported_name == "__default__":
                        # export { default } from './Y' → 默认导出被 re-export
                        # 如果 barrel 的默认导出被其他文件导入，则源文件的第一个导出视为被使用
                        barrel_stem = Path(barrel_rel).parent.name  # 目录名作为默认导入名
                        if barrel_stem in barrel_imported_names:
                            source_exports = export_map.get(source_rel, [])
                            if source_exports:
                                barrel_used[source_rel].add(source_exports[0])
                    else:
                        # 具名 re-export: 如果该名称被其他文件从 barrel 导入
                        if exported_name in barrel_imported_names:
                            barrel_used[source_rel].add(exported_name)

    # 对每个有导出的文件，检查其导出符号是否在导入列表中
    for rel, exports in export_map.items():
        used: List[str] = []
        unused: List[str] = []
        barrel_names = barrel_used.get(rel, set())
        for export_name in exports:
            if export_name in all_imported_names:
                used.append(export_name)
            elif export_name in barrel_names:
                # 通过 barrel 文件间接被使用
                used.append(export_name)
            else:
                # 也检查 default import（文件名作为默认导出名）
                stem = Path(rel).stem
                if stem in all_imported_names and export_name == exports[0]:
                    used.append(export_name)
                else:
                    unused.append(export_name)
        result[rel] = (used, unused)

    return result


def _is_path_keyword(kw: str) -> bool:
    """路径类或文件名类关键词（含 /、\\ 或 .）本身足够具体，允许子串匹配。"""
    return "/" in kw or "\\" in kw or "." in kw


def _extract_import_line(text: str, match_start: int) -> str:
    """从匹配位置提取完整的逻辑行（处理多行 import 语句）。

    对于多行 import（JS/TS 常见）：
      import {
        Button,
        Input
      } from './components'
    需要从匹配起始追踪到语句结束。
    """
    # 找到行的起始位置
    line_start = text.rfind("\n", 0, match_start) + 1
    # 找到行的结束位置（追踪括号匹配）
    depth = 0
    pos = match_start
    while pos < len(text):
        ch = text[pos]
        if ch in "({[":
            depth += 1
        elif ch in ")}]":
            depth -= 1
        elif ch == "\n" and depth <= 0:
            # 多行 import 结束（括号已关闭 + 换行）
            break
        elif ch in ";,\n" and depth <= 0:
            break
        pos += 1
    return text[line_start:pos]


def has_import_reference(text: str, stem: str, ext: str) -> bool:
    """检测 text 中是否存在对 stem 的 import 精确引用。
    根据文件扩展名选择对应语言的 import 语法模式。
    使用逻辑行匹配替代固定 200 字符窗口，同时检查匹配内部和完整语句。
    """
    patterns = _EXT_IMPORT_INDEX.get(ext)
    if not patterns:
        # 未知扩展名回退到简单子串检测
        return stem in text
    for pattern in patterns:
        for m in pattern.finditer(text):
            # 检查匹配内部（Java/Rust 等语言的 import 路径在匹配内）
            if stem in m.group(0):
                return True
            # 提取完整逻辑行并在其中搜索
            import_line = _extract_import_line(text, m.start())
            if stem in import_line:
                return True
    return False


def non_self_reference_hits(target_rel: str, pool: Dict[str, str], keywords: Sequence[str], exclude_rels: Optional[Set[str]] = None) -> List[str]:
    hits: List[str] = []
    if not keywords:
        return hits
    for rel, text in pool.items():
        if rel == target_rel:
            continue
        if exclude_rels and rel in exclude_rels:
            continue
        ext = Path(rel).suffix.lower()
        for kw in keywords:
            if not kw:
                continue
            if _is_path_keyword(kw):
                if kw in text:
                    log_progress(f"    HIT: Found '{kw}' in {rel}")
                    hits.append(rel)
                    break
            else:
                if has_import_reference(text, kw, ext):
                    hits.append(rel)
                    break
    return hits


def find_weak_mentions(target_rel: str, pool: Dict[str, str], token: str) -> List[str]:
    """上下文感知的弱引用检测：用多种针对性模式搜索潜在的间接引用。"""
    if not token:
        return []
    hits: List[str] = []
    escaped = re.escape(token)

    # 多种弱引用模式，按优先级排列
    weak_patterns = [
        # 1. 模板标签使用：HTML/Vue 模板中 <token 或 </token
        (re.compile(rf"</?{escaped}[\s>/]", re.IGNORECASE), "模板标签引用"),
        # 2. 路径片段引用：/token/ 或 /token. 或 ./token
        (re.compile(rf"[/'\"\\]{escaped}[/'\"\\\\.]", re.IGNORECASE), "路径片段引用"),
        # 3. 字符串字面量：引号中包含 token
        (re.compile(rf"['\"`]{escaped}['\"`]", re.IGNORECASE), "字符串字面量引用"),
        # 4. 路由配置：path/component 中引用
        (re.compile(rf"(?:path|component|name)\s*:\s*['\"].*{escaped}.*['\"]", re.IGNORECASE), "路由配置引用"),
        # 5. 动态导入模式
        (re.compile(rf"import\s*\(\s*['\"].*{escaped}.*['\"]", re.IGNORECASE), "动态导入引用"),
        (re.compile(rf"require\s*\(\s*['\"].*{escaped}.*['\"]", re.IGNORECASE), "require 引用"),
    ]

    for rel, text in pool.items():
        if rel == target_rel:
            continue
        for pattern, _desc in weak_patterns:
            if pattern.search(text):
                hits.append(rel)
                break  # 每个文件只记录一次
    return hits


def extract_component_tag_name(file_path: Path) -> str:
    stem = file_path.stem
    kebab = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", stem).replace("_", "-").lower()
    return kebab


def extract_name_variants(file_path: Path) -> List[str]:
    """从文件名生成多种命名变体，用于更全面的引用搜索。"""
    stem = file_path.stem
    variants = []
    # PascalCase / camelCase 原始形式
    variants.append(stem)
    # kebab-case
    kebab = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", stem).replace("_", "-").lower()
    if kebab != stem:
        variants.append(kebab)
    # snake_case
    snake = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", stem).replace("-", "_").lower()
    if snake != stem and snake != kebab:
        variants.append(snake)
    # 完整文件名（含扩展名）
    variants.append(file_path.name)
    return variants


def infer_history_file(path: Path) -> bool:
    name = path.name
    patterns = [r"-copy", r"-bf", r"-old", r"_bak", r"\.bak", r"备份"]
    return any(re.search(p, name, re.IGNORECASE) for p in patterns)


def pick_risk(weak_signals: List[str], history_pattern_hit: bool = False) -> str:
    if weak_signals:
        return "medium"
    if history_pattern_hit:
        return "low"
    return "high"


def find_upward_config(start_path: Path, filename: str) -> Optional[Path]:
    """从起始路径开始向上追溯，寻找配置文件。"""
    current = start_path.resolve()
    while True:
        # 1. 检查标准 .code-cleanup 目录
        candidate1 = current / ".code-cleanup" / filename
        if candidate1.is_file():
            return candidate1
            
        # 2. 检查 Cursor 插件配置路径
        candidate2 = current / ".cursor" / "skills" / "code-cleanup-skill" / "config" / filename
        if candidate2.is_file():
            return candidate2
            
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


# 硬编码的默认保护列表：这些文件/模式始终不会被标记为删除候选
_DEFAULT_KEEP_PATTERNS = {
    # 入口文件
    "main.js", "main.ts", "main.jsx", "main.tsx", "main.py", "main.go",
    "index.js", "index.ts", "index.jsx", "index.tsx",
    "app.js", "app.ts", "app.jsx", "app.tsx",
    "App.vue", "App.jsx", "App.tsx",
    "__init__.py", "__main__.py", "mod.rs",
    # 框架配置
    "nuxt.config.js", "nuxt.config.ts",
    "vue.config.js", "vue.config.ts",
    "vite.config.js", "vite.config.ts",
    "webpack.config.js", "webpack.config.ts",
    "next.config.js", "next.config.ts", "next.config.mjs",
    "angular.json",
    "setup.py", "setup.cfg", "manage.py", "pyproject.toml",
    # 路由定义
    "router.js", "router.ts", "router.jsx", "router.tsx",
    "routes.js", "routes.ts", "routes.jsx", "routes.tsx",
    "urls.py",
}


def _is_default_keep(rel_path: str) -> bool:
    """检查文件路径是否匹配默认保护列表。"""
    filename = rel_path.split("/")[-1]
    if filename in _DEFAULT_KEEP_PATTERNS:
        return True
    # 匹配 *.config.* 和 *.rc.* 模式
    parts = filename.split(".")
    if len(parts) >= 3 and parts[-2] == "config":
        return True
    if len(parts) >= 3 and parts[-2] == "rc":
        return True
    # 匹配 *.test.* 和 *.spec.* 模式（要求 test/spec 在中间位置，不是首尾）
    if len(parts) >= 3:
        for i in range(1, len(parts) - 1):
            if parts[i] in ("test", "spec"):
                return True
    # 匹配 __tests__ 目录
    if "/__tests__/" in rel_path:
        return True
    return False


def load_keep_list(root: Path, explicit: str = "") -> Set[str]:
    if explicit:
        candidates = [Path(explicit).resolve()]
    else:
        script_dir = Path(__file__).resolve().parent
        candidates = []
        upward = find_upward_config(root, "keep-list.txt")
        if upward:
            candidates.append(upward)
        candidates.extend([
            root / "plugins" / "code-cleanup" / "skills" / "code-cleanup-skill" / "config" / "keep-list.txt",
            script_dir.parent / "config" / "keep-list.txt",
        ])
    for candidate in candidates:
        if candidate.exists():
            log_progress(f"Loaded keep-list from: {candidate}")
            items: Set[str] = set()
            for line in candidate.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                items.add(line.replace("\\", "/"))
            return items
    return set()


def load_ext_list(root: Path, explicit: str = "") -> Set[str]:
    if explicit:
        candidates = [Path(explicit).resolve()]
    else:
        script_dir = Path(__file__).resolve().parent
        candidates = []
        upward = find_upward_config(root, "ext-list.txt")
        if upward:
            candidates.append(upward)
        candidates.extend([
            root / "plugins" / "code-cleanup" / "skills" / "code-cleanup-skill" / "config" / "ext-list.txt",
            script_dir.parent / "config" / "ext-list.txt",
        ])
    for candidate in candidates:
        if candidate.exists():
            log_progress(f"Loaded ext-list from: {candidate}")
            exts: Set[str] = set()
            for line in candidate.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                ext = line if line.startswith(".") else f".{line}"
                exts.add(ext.lower())
            return exts if exts else CODE_EXTS
    log_progress("Using default ext-list")
    return CODE_EXTS


def load_scan_dirs(root: Path, explicit: str = "") -> List[ScanDir]:
    """从配置文件加载扫描目录列表。格式: 目录路径:类别名:关键词策略(可选)
    例如: src/page:unused_page:stem,parent
    如果未指定关键词策略，默认使用 stem。
    """
    if explicit:
        candidates = [Path(explicit).resolve()]
    else:
        script_dir = Path(__file__).resolve().parent
        candidates = []
        upward = find_upward_config(root, "scan-dirs.txt")
        if upward:
            candidates.append(upward)
        candidates.extend([
            root / "plugins" / "code-cleanup" / "skills" / "code-cleanup-skill" / "config" / "scan-dirs.txt",
            script_dir.parent / "config" / "scan-dirs.txt",
        ])
    for candidate in candidates:
        if candidate.exists():
            log_progress(f"Loaded scan-dirs from: {candidate}")
            dirs: List[ScanDir] = []
            for line in candidate.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(":")
                dir_path = parts[0].strip()
                category = parts[1].strip() if len(parts) > 1 else "unused_module"
                hints_str = parts[2].strip() if len(parts) > 2 else "stem"
                hints = [h.strip() for h in hints_str.split(",") if h.strip()]
                dirs.append(ScanDir(dir_path=dir_path, category=category, keyword_hints=hints))
            return dirs if dirs else _default_scan_dirs()
    log_progress("Using default scan-dirs")
    return _default_scan_dirs()


def _default_scan_dirs() -> List[ScanDir]:
    """未找到配置文件时的默认扫描目录。"""
    return [
        ScanDir("src/page", "unused_page", ["stem", "parent"]),
        ScanDir("src/pages", "unused_page", ["stem", "parent"]),
        ScanDir("src/components", "unused_component", ["stem", "tag"]),
        ScanDir("src/assets", "unused_asset", ["name", "stem"]),
        ScanDir("src/views", "unused_view", ["stem", "parent"]),
        ScanDir("src/controllers", "unused_handler", ["stem"]),
        ScanDir("src/services", "unused_service", ["stem"]),
        ScanDir("src/utils", "unused_util", ["stem"]),
        ScanDir("src/helpers", "unused_util", ["stem"]),
    ]


def analyze_modules(root: Path, all_files: List[Path], reference_pool: Dict[str, str], keep_list: Set[str], scan_dirs: List[ScanDir], targets: Set[str], symbol_usage: Optional[Dict[str, Tuple[List[str], List[str]]]] = None, config_driven_refs: Optional[Dict[str, List[str]]] = None, reachable: Optional[Set[str]] = None) -> List[Candidate]:
    """通用模块扫描：基于依赖图可达性分析识别未引用的文件。

    判定逻辑：
    1. 如果文件在依赖图中从入口点可达 → "在使用中"（检查部分导出）
    2. 如果文件不可达 → 确认为删除候选（弱引用降级风险）
    3. 配置驱动引用作为额外保护
    """
    candidates: List[Candidate] = []
    scan_all = len(targets) == 0 or "." in targets or "src" in targets

    for sd in scan_dirs:
        if not scan_all and sd.dir_path not in targets:
            continue

        # 筛选属于当前扫描目录的文件 (支持深层目录匹配)
        target_prefix = sd.dir_path.strip("/")
        module_files = [
            f for f in all_files
            if normalize_rel(f, root) == target_prefix or normalize_rel(f, root).startswith(f"{target_prefix}/")
        ]

        if not module_files:
            continue

        log_progress(f"  Analyzing {len(module_files)} files in category: {sd.category} (prefix: {target_prefix})")
        for file in module_files:
            rel = normalize_rel(file, root)
            if rel in keep_list or _is_default_keep(rel):
                continue

            stem = file.stem
            parent = file.parent.name
            weak_signals: List[str] = []
            history_pattern_hit = infer_history_file(file)

            # 弱引用检测（用于不可达文件的风险降级）
            weak_token = parent if "parent" in sd.keyword_hints else stem
            weak_hits = find_weak_mentions(rel, reference_pool, weak_token)
            if weak_hits:
                weak_signals.append("存在弱引用线索（字符串路径/动态引用），建议人工复核")

            # ── 符号级导出分析 ──
            file_used_exports: List[str] = []
            file_unused_exports: List[str] = []
            file_total_exports = 0
            all_exports_unused = False
            some_exports_unused = False

            if symbol_usage and rel in symbol_usage:
                used, unused = symbol_usage[rel]
                file_used_exports = used
                file_unused_exports = unused
                file_total_exports = len(used) + len(unused)
                if file_total_exports > 0:
                    if not used:
                        all_exports_unused = True
                    elif unused:
                        some_exports_unused = True

            # ── 配置驱动引用检查 ──
            config_refs = config_driven_refs.get(rel, []) if config_driven_refs else []

            # ── 依赖图可达性判定 ──
            is_reachable = reachable is not None and rel in reachable

            # ── 关键词引用检测（补充 import 图无法覆盖的引用方式）──
            # Vue 2 的 common.openWindow、路由配置等不走 import
            if not is_reachable:
                keywords = [rel, file.name]
                for hint in sd.keyword_hints:
                    if hint == "stem" and stem:
                        keywords.append(stem)
                    elif hint == "parent" and parent:
                        keywords.append(f"/{parent}/")
                    elif hint == "tag":
                        tag_name = extract_component_tag_name(file)
                        keywords.append(tag_name)
                        if stem != tag_name:
                            keywords.append(stem)
                    elif hint == "name_variants":
                        for variant in extract_name_variants(file):
                            if variant not in keywords:
                                keywords.append(variant)

                # 排除 co-file 组内引用：同目录下同名（stem 相同）的文件
                # 这些文件互相引用是正常的（如 page.js import page.scss），
                # 不应被视为"外部引用"
                cofile_excludes: Set[str] = set()
                file_dir = str(file.parent)
                for other_f in all_files:
                    if other_f.parent == file.parent and other_f.stem == stem and other_f != file:
                        other_rel = normalize_rel(other_f, root)
                        cofile_excludes.add(other_rel)

                kw_hits = non_self_reference_hits(rel, reference_pool, keywords, exclude_rels=cofile_excludes)
                if kw_hits:
                    is_reachable = True

            if config_refs:
                # 文件通过配置驱动方式被引用 → 标记为 medium，不标记为删除候选
                evidence = [f"文件被配置驱动方式引用，建议人工确认"]
                evidence.extend(config_refs[:3])
                candidates.append(
                    Candidate(
                        path=rel,
                        category="config_driven_" + sd.category.replace("unused_", ""),
                        risk_level="medium",
                        evidence=evidence,
                        file_size_bytes=file.stat().st_size,
                    )
                )
                continue

            if is_reachable and not all_exports_unused:
                # 文件在依赖图中可达 且 (无导出分析 或 至少一个导出被使用) → 在使用中
                # 但如果有部分导出未使用，添加信息性候选
                if some_exports_unused and file_total_exports > 0:
                    unused_pct = len(file_unused_exports) / file_total_exports * 100
                    evidence = [
                        f"文件被引用但 {len(file_unused_exports)}/{file_total_exports} 个导出未被使用 ({unused_pct:.0f}%)",
                        f"未使用导出: {', '.join(file_unused_exports[:10])}{'...' if len(file_unused_exports) > 10 else ''}",
                        f"已使用导出: {', '.join(file_used_exports[:10])}{'...' if len(file_used_exports) > 10 else ''}",
                    ]
                    candidates.append(
                        Candidate(
                            path=rel,
                            category="partially_used_" + sd.category.replace("unused_", ""),
                            risk_level="medium",
                            evidence=evidence,
                            file_size_bytes=file.stat().st_size,
                            total_exports=file_total_exports,
                            used_exports=file_used_exports,
                            unused_exports=file_unused_exports,
                        )
                    )
                continue

            # 文件不可达 或 所有导出都未被使用 → 确定为候选
            risk = pick_risk(weak_signals, history_pattern_hit=history_pattern_hit)
            evidence = []
            if all_exports_unused:
                evidence.append(f"所有 {file_total_exports} 个导出均未被任何文件导入: {', '.join(file_unused_exports[:10])}")
                risk = "high"  # 所有导出都未使用 = 高风险可删除
            else:
                evidence.append(f"未在依赖图中找到从入口点到 `{file.name}` 的可达路径")
            if history_pattern_hit:
                evidence.append("命中历史文件命名模式(copy/bf/old)")
            evidence.extend(weak_signals)
            candidates.append(
                Candidate(
                    path=rel,
                    category=sd.category,
                    risk_level=risk,
                    evidence=evidence,
                    file_size_bytes=file.stat().st_size,
                    total_exports=file_total_exports,
                    used_exports=file_used_exports if file_used_exports else None,
                    unused_exports=file_unused_exports if file_unused_exports else None,
                )
            )
    return candidates


def analyze_history_files(root: Path, reference_pool: Dict[str, str], keep_list: Set[str]) -> List[Candidate]:
    candidates: List[Candidate] = []
    for rel, _ in reference_pool.items():
        if rel in keep_list or _is_default_keep(rel):
            continue
        full = root / rel
        if not infer_history_file(full):
            continue
        hits = non_self_reference_hits(rel, reference_pool, [rel, Path(rel).stem])
        risk = "medium" if hits else "low"
        evidence = ["命中历史文件命名模式(copy/bf/old)"]
        if hits:
            evidence.append("存在弱引用线索，建议人工确认")
        else:
            evidence.append("未发现直接引用")
        candidates.append(
            Candidate(
                path=rel,
                category="dead_code_history_file",
                risk_level=risk,
                evidence=evidence,
                file_size_bytes=full.stat().st_size,
            )
        )
    return candidates


def summarize(candidates: Sequence[Candidate], project_stats: Dict[str, int]) -> Dict:
    summary = {"high": 0, "medium": 0, "low": 0}
    unused_size = 0
    for item in candidates:
        if item.risk_level not in summary:
            summary[item.risk_level] = 0
        summary[item.risk_level] += 1
        unused_size += item.file_size_bytes

    total_files = project_stats.get("total_files_scanned", 1)
    total_size = project_stats.get("total_size_bytes", 1)
    if total_files == 0: total_files = 1
    if total_size == 0: total_size = 1

    stats = {
        **project_stats,
        "unused_files_count": len(candidates),
        "unused_size_bytes": unused_size
    }
    # 多因子健康度：取文件数惩罚和大小惩罚的较大值
    high_count = summary.get("high", 0)
    medium_count = summary.get("medium", 0)
    low_count = summary.get("low", 0)
    file_penalty = (high_count * 3 + medium_count * 1.5 + low_count * 0.5) / total_files * 100
    size_penalty = unused_size / total_size * 100
    stats["health_score"] = max(0, min(100, int(100 - max(file_penalty, size_penalty))))

    return {"risk_summary": summary, "project_stats": stats}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze cleanup candidates for project.")
    parser.add_argument("--project-root", default=".", help="Project root path")
    parser.add_argument(
        "--targets",
        nargs="*",
        default=[],
        help="Optional targets. Empty means auto-scan current workspace.",
    )
    parser.add_argument("--keep-list", default="", help="Optional keep-list file path")
    parser.add_argument("--ext-list", default="", help="Optional ext-list file path")
    parser.add_argument("--scan-dirs", default="", help="Optional scan-dirs config file path")
    parser.add_argument("--output", required=True, help="Output JSON path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.project_root).resolve()
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    log_progress(f"Initializing scan for: {root}")
    exts = load_ext_list(root, args.ext_list)
    
    log_progress("Phase 1: Collecting all non-ignored files...")
    all_files, project_stats = collect_files(root)
    log_progress(f"Detected {len(all_files)} files in workspace.")

    log_progress("Phase 2: Building reference pool (reading code contents)...")
    reference_pool = build_reference_pool(all_files, root, exts)
    log_progress(f"Reference pool built with {len(reference_pool)} code files.")
    
    keep_list = load_keep_list(root, args.keep_list)
    scan_dirs = load_scan_dirs(root, args.scan_dirs)
    targets = {t.replace("\\", "/").strip("/") for t in args.targets}

    candidates: List[Candidate] = []

    log_progress("Phase 3: Building symbol maps (export/import analysis)...")
    export_map = build_export_map(reference_pool)
    import_map = build_import_map(reference_pool, root)
    barrel_map = build_barrel_map(reference_pool)
    config_driven_refs = build_config_driven_refs(reference_pool)
    symbol_usage = build_symbol_usage(export_map, import_map, reference_pool, barrel_map)
    log_progress(f"Symbol analysis: {len(export_map)} files with exports, {len(import_map)} files with imports, {len(barrel_map)} barrel files, {len(config_driven_refs)} config-driven refs")

    log_progress("Phase 3.5: Building dependency graph and computing reachability...")
    all_rels = set(reference_pool.keys())
    forward_graph, reverse_graph = build_dependency_graph(reference_pool, all_rels)
    entry_points = identify_entry_points(all_rels, keep_list)
    reachable = find_reachable_files(forward_graph, entry_points)
    log_progress(f"Dependency graph: {len(forward_graph)} source nodes, {sum(len(v) for v in forward_graph.values())} edges, {len(entry_points)} entry points, {len(reachable)} reachable files")

    log_progress("Phase 4: Analyzing modules for unused references...")
    candidates.extend(analyze_modules(root, all_files, reference_pool, keep_list, scan_dirs, targets, symbol_usage, config_driven_refs, reachable))
    
    log_progress("Phase 5: Analyzing for history/backup files...")
    candidates.extend(analyze_history_files(root, reference_pool, keep_list))

    log_progress("Finalizing: Deduplicating and summarizing results...")
    # deduplicate by path + category
    seen = set()
    deduped: List[Candidate] = []
    for item in candidates:
        key = (item.path, item.category)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    final_summary = summarize(deduped, project_stats)
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root).replace("\\", "/"),
        "summary": final_summary["risk_summary"],
        "project_stats": final_summary["project_stats"],
        "candidates": [asdict(item) for item in sorted(deduped, key=lambda c: (c.risk_level, c.category, c.path))],
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    log_progress(f"Generation complete: {len(deduped)} candidates identified -> {output}")


if __name__ == "__main__":
    main()
