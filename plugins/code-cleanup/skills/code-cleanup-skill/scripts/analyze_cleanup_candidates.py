#!/usr/bin/env python3
import argparse
import json
import re
import os
import subprocess
import fnmatch
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Sequence, Set, Tuple


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
}
HISTORY_PATTERNS = [
    re.compile(r".*[-_.](copy|bf|old)(\.[^.]+)?$", re.IGNORECASE),
    re.compile(r".*(copy|backup|bak)\.[^.]+$", re.IGNORECASE),
]

# 按语言分组的 import 语法模式，用于精确引用检测
# 键为扩展名集合，值为正则列表；匹配到正则后的 200 字符内出现 stem 视为引用
IMPORT_PATTERNS: List[Tuple[Set[str], List[re.Pattern]]] = [
    # JS / TS / Vue / JSX / TSX
    (
        {".js", ".ts", ".vue", ".jsx", ".tsx"},
        [
            re.compile(r"(?:import\s+.*?from\s*|import\s*|require\s*\(\s*|import\s*\(\s*)['\"`]", re.IGNORECASE),
        ],
    ),
    # Python
    (
        {".py"},
        [
            re.compile(r"(?:from\s+[\w.]+\s+import\s+|import\s+)['\"`]?", re.IGNORECASE),
            re.compile(r"from\s+([\w.]+)\s+import", re.IGNORECASE),
            re.compile(r"import\s+([\w.]+)", re.IGNORECASE),
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
    suggested_action: str = "delete_after_confirm"


@dataclass
class ScanDir:
    dir_path: str  # 相对路径，如 src/page
    category: str  # 如 unused_page
    # 额外关键词提取策略: "stem"=文件名, "parent"=父目录名, "tag"=kebab-case 标签名
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


def collect_code_files(root: Path, exts: Set[str]) -> List[Path]:
    """获取项目中的代码文件列表，优先使用 Git 以支持 .gitignore。"""
    files: List[Path] = []
    
    # 1. 优先尝试使用 Git 命令获取文件列表 (自动支持 .gitignore)
    try:
        # 已跟踪文件
        cmd1 = ["git", "ls-files"]
        res1 = subprocess.run(cmd1, cwd=root, capture_output=True, text=True, check=True)
        
        # 未跟踪但未被忽略的文件
        cmd2 = ["git", "ls-files", "--others", "--exclude-standard"]
        res2 = subprocess.run(cmd2, cwd=root, capture_output=True, text=True, check=True)
        
        all_git_files = res1.stdout.splitlines() + res2.stdout.splitlines()
        
        for rel_path in all_git_files:
            if not rel_path:
                continue
            # 双重保险：排除硬编码的忽略目录
            if any(rel_path == x or rel_path.startswith(f"{x}/") for x in IGNORE_DIRS):
                continue
            
            p = root / rel_path
            if p.is_file() and p.suffix.lower() in exts:
                files.append(p)
                
        if files:
            return files
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # 2. 如果不是 Git 仓库或命令失败，回退到 os.walk 模式
    ignore_patterns = load_gitignore_patterns(root)
    
    for dirpath, dirnames, filenames in os.walk(root):
        # 计算相对于 root 的路径
        rel_dir = os.path.relpath(dirpath, root).replace("\\", "/")
        if rel_dir == ".":
            rel_dir = ""
            
        # 就地修改 dirnames 以剪枝忽略的目录，os.walk 会自动停止进入这些目录
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
            p = Path(dirpath) / f
            if p.suffix.lower() in exts:
                files.append(p)

    return files


def build_reference_pool(files: Sequence[Path], root: Path) -> Dict[str, str]:
    return {normalize_rel(file, root): read_text(file) for file in files}


def _is_path_keyword(kw: str) -> bool:
    """路径类关键词（含 / 或 .）本身足够具体，允许子串匹配。"""
    return "/" in kw or "\\" in kw or kw.startswith(".") or kw.endswith(".")


def has_import_reference(text: str, stem: str, ext: str) -> bool:
    """检测 text 中是否存在对 stem 的 import 精确引用。
    根据文件扩展名选择对应语言的 import 语法模式。
    """
    patterns = _EXT_IMPORT_INDEX.get(ext)
    if not patterns:
        # 未知扩展名回退到简单子串检测
        return stem in text
    for pattern in patterns:
        for m in pattern.finditer(text):
            start = m.end()
            snippet = text[start: start + 200]
            if stem in snippet:
                return True
    return False


def non_self_reference_hits(target_rel: str, pool: Dict[str, str], keywords: Sequence[str]) -> List[str]:
    hits: List[str] = []
    if not keywords:
        return hits
    for rel, text in pool.items():
        if rel == target_rel:
            continue
        ext = Path(rel).suffix.lower()
        for kw in keywords:
            if not kw:
                continue
            if _is_path_keyword(kw):
                if kw in text:
                    hits.append(rel)
                    break
            else:
                if has_import_reference(text, kw, ext):
                    hits.append(rel)
                    break
    return hits


def find_weak_mentions(target_rel: str, pool: Dict[str, str], token: str) -> List[str]:
    if not token:
        return []
    hits: List[str] = []
    pattern = re.compile(rf"['\"/\\-]({re.escape(token)})['\"/\\-]", re.IGNORECASE)
    for rel, text in pool.items():
        if rel == target_rel:
            continue
        if pattern.search(text):
            hits.append(rel)
    return hits


def extract_component_tag_name(file_path: Path) -> str:
    stem = file_path.stem
    kebab = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", stem).replace("_", "-").lower()
    return kebab


def infer_history_file(path: Path) -> bool:
    name = path.name
    return any(p.match(name) for p in HISTORY_PATTERNS)


def pick_risk(weak_signals: List[str], history_pattern_hit: bool = False) -> str:
    if weak_signals:
        return "medium"
    if history_pattern_hit:
        return "low"
    return "high"


def load_keep_list(root: Path, explicit: str = "") -> Set[str]:
    if explicit:
        candidates = [Path(explicit).resolve()]
    else:
        script_dir = Path(__file__).resolve().parent
        candidates = [
            root / ".code-cleanup" / "keep-list.txt",
            root / "plugins" / "code-cleanup" / "skills" / "code-cleanup-skill" / "config" / "keep-list.txt",
            script_dir.parent / "config" / "keep-list.txt",
            root / ".cursor" / "skills" / "code-cleanup-skill" / "config" / "keep-list.txt",
        ]
    for candidate in candidates:
        if candidate.exists():
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
        candidates = [
            root / ".code-cleanup" / "ext-list.txt",
            root / "plugins" / "code-cleanup" / "skills" / "code-cleanup-skill" / "config" / "ext-list.txt",
            script_dir.parent / "config" / "ext-list.txt",
            root / ".cursor" / "skills" / "code-cleanup-skill" / "config" / "ext-list.txt",
        ]
    for candidate in candidates:
        if candidate.exists():
            exts: Set[str] = set()
            for line in candidate.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                ext = line if line.startswith(".") else f".{line}"
                exts.add(ext.lower())
            return exts if exts else CODE_EXTS
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
        candidates = [
            root / ".code-cleanup" / "scan-dirs.txt",
            root / "plugins" / "code-cleanup" / "skills" / "code-cleanup-skill" / "config" / "scan-dirs.txt",
            script_dir.parent / "config" / "scan-dirs.txt",
            root / ".cursor" / "skills" / "code-cleanup-skill" / "config" / "scan-dirs.txt",
        ]
    for candidate in candidates:
        if candidate.exists():
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
    return _default_scan_dirs()


def _default_scan_dirs() -> List[ScanDir]:
    """未找到配置文件时的默认扫描目录。"""
    return [
        ScanDir("src/page", "unused_page", ["stem", "parent"]),
        ScanDir("src/pages", "unused_page", ["stem", "parent"]),
        ScanDir("src/components", "unused_component", ["stem", "tag"]),
        ScanDir("src/views", "unused_view", ["stem", "parent"]),
        ScanDir("src/controllers", "unused_handler", ["stem"]),
        ScanDir("src/services", "unused_service", ["stem"]),
        ScanDir("src/utils", "unused_util", ["stem"]),
        ScanDir("src/helpers", "unused_util", ["stem"]),
    ]


def analyze_modules(root: Path, reference_pool: Dict[str, str], keep_list: Set[str], scan_dirs: List[ScanDir], targets: Set[str]) -> List[Candidate]:
    """通用模块扫描：根据 scan_dirs 配置扫描各目录中未被引用的文件。"""
    candidates: List[Candidate] = []
    scan_all = len(targets) == 0 or "." in targets or "src" in targets

    for sd in scan_dirs:
        if not scan_all and sd.dir_path not in targets:
            continue
        module_root = root / sd.dir_path
        if not module_root.exists():
            continue

        for file in module_root.rglob("*"):
            if not file.is_file():
                continue
            ext = file.suffix.lower()
            # 排除非代码文件（图片、字体等）
            if ext in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".map"}:
                continue

            rel = normalize_rel(file, root)
            if rel in keep_list:
                continue

            # 根据关键词策略构建搜索关键词
            keywords = [rel]
            stem = file.stem
            parent = file.parent.name
            for hint in sd.keyword_hints:
                if hint == "stem" and stem:
                    keywords.append(stem)
                elif hint == "parent" and parent:
                    keywords.append(f"/{parent}/")
                elif hint == "tag":
                    keywords.append(extract_component_tag_name(file))

            hits = non_self_reference_hits(rel, reference_pool, keywords)
            weak_signals: List[str] = []
            history_pattern_hit = infer_history_file(file)

            # 弱引用检测：用父目录名或文件名做模糊匹配
            weak_token = parent if "parent" in sd.keyword_hints else stem
            weak_hits = find_weak_mentions(rel, reference_pool, weak_token)
            if weak_hits:
                weak_signals.append("存在弱引用线索（字符串路径/动态引用），建议人工复核")
            if hits:
                continue

            risk = pick_risk(weak_signals, history_pattern_hit=history_pattern_hit)
            evidence = [f"未在其他源码文件中找到对 `{stem}` 的直接引用"]
            if history_pattern_hit:
                evidence.append("命中历史文件命名模式(copy/bf/old)")
            evidence.extend(weak_signals)
            candidates.append(
                Candidate(
                    path=rel,
                    category=sd.category,
                    risk_level=risk,
                    evidence=evidence,
                )
            )
    return candidates


def analyze_history_files(root: Path, reference_pool: Dict[str, str], keep_list: Set[str]) -> List[Candidate]:
    candidates: List[Candidate] = []
    for rel, _ in reference_pool.items():
        if rel in keep_list:
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
            )
        )
    return candidates


def summarize(candidates: Sequence[Candidate]) -> Dict[str, int]:
    summary = {"high": 0, "medium": 0, "low": 0}
    for item in candidates:
        if item.risk_level not in summary:
            summary[item.risk_level] = 0
        summary[item.risk_level] += 1
    return summary


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

    exts = load_ext_list(root, args.ext_list)
    files = collect_code_files(root, exts)
    reference_pool = build_reference_pool(files, root)
    keep_list = load_keep_list(root, args.keep_list)
    scan_dirs = load_scan_dirs(root, args.scan_dirs)
    targets = {t.replace("\\", "/").strip("/") for t in args.targets}

    candidates: List[Candidate] = []
    candidates.extend(analyze_modules(root, reference_pool, keep_list, scan_dirs, targets))
    candidates.extend(analyze_history_files(root, reference_pool, keep_list))

    # deduplicate by path + category
    seen = set()
    deduped: List[Candidate] = []
    for item in candidates:
        key = (item.path, item.category)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root).replace("\\", "/"),
        "summary": summarize(deduped),
        "candidates": [asdict(item) for item in sorted(deduped, key=lambda c: (c.risk_level, c.category, c.path))],
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {len(deduped)} candidates -> {output}")


if __name__ == "__main__":
    main()
