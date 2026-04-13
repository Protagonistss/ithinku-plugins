#!/usr/bin/env python3
import argparse
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Sequence, Set


CODE_EXTS = {".js", ".ts", ".vue", ".jsx", ".tsx", ".html"}
PAGE_EXTS = {".js", ".vue", ".html"}
COMPONENT_EXTS = {".js", ".ts", ".vue", ".jsx", ".tsx"}
IGNORE_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".cursor",
    "static/lib",
}
HISTORY_PATTERNS = [
    re.compile(r".*[-_.](copy|bf|old)(\.[^.]+)?$", re.IGNORECASE),
    re.compile(r".*(copy|backup|bak)\.[^.]+$", re.IGNORECASE),
]


@dataclass
class Candidate:
    path: str
    category: str
    risk_level: str
    evidence: List[str]
    suggested_action: str = "delete_after_confirm"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def normalize_rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


def collect_code_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = str(p.relative_to(root)).replace("\\", "/")
        if any(rel == x or rel.startswith(f"{x}/") for x in IGNORE_DIRS):
            continue
        if p.suffix.lower() in CODE_EXTS:
            files.append(p)
    return files


def build_reference_pool(files: Sequence[Path], root: Path) -> Dict[str, str]:
    return {normalize_rel(file, root): read_text(file) for file in files}


def non_self_reference_hits(target_rel: str, pool: Dict[str, str], keywords: Sequence[str]) -> List[str]:
    hits: List[str] = []
    if not keywords:
        return hits
    for rel, text in pool.items():
        if rel == target_rel:
            continue
        if any(k and k in text for k in keywords):
            hits.append(rel)
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


def extract_component_tag_name(component_path: Path) -> str:
    stem = component_path.stem
    # myCourseItem -> my-course-item
    kebab = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", stem).replace("_", "-").lower()
    return kebab


def infer_history_file(path: Path) -> bool:
    rel = str(path).replace("\\", "/")
    return any(p.match(rel) for p in HISTORY_PATTERNS)


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
            # 在本仓库插件目录运行时的默认位置
            root / "plugins" / "code-cleanup" / "skills" / "code-cleanup-skill" / "config" / "keep-list.txt",
            # 脚本同仓打包时的相对位置（优先保证可移植）
            script_dir.parent / "config" / "keep-list.txt",
            # 兼容 Cursor 本地 Skill 的默认位置（兜底）
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


def analyze_pages(root: Path, reference_pool: Dict[str, str], keep_list: Set[str]) -> List[Candidate]:
    page_root = root / "src" / "page"
    if not page_root.exists():
        return []

    candidates: List[Candidate] = []
    for file in page_root.rglob("*"):
        if not file.is_file() or file.suffix.lower() not in PAGE_EXTS:
            continue

        rel = normalize_rel(file, root)
        if rel in keep_list:
            continue
        stem = file.stem
        parent = file.parent.name
        keywords = [rel, f"/{parent}/", stem]
        hits = non_self_reference_hits(rel, reference_pool, keywords)
        weak_signals: List[str] = []
        history_pattern_hit = infer_history_file(file)
        weak_hits = find_weak_mentions(rel, reference_pool, parent)
        if weak_hits:
            weak_signals.append("存在弱引用线索（字符串路径/动态拼接），建议人工复核")
        if hits:
            continue

        risk = pick_risk(weak_signals, history_pattern_hit=history_pattern_hit)
        evidence = ["未在其他源码文件中找到直接引用或路径命中"]
        if history_pattern_hit:
            evidence.append("命中历史文件命名模式(copy/bf/old)")
        evidence.extend(weak_signals)
        candidates.append(
            Candidate(
                path=rel,
                category="unused_page",
                risk_level=risk,
                evidence=evidence,
            )
        )
    return candidates


def analyze_components(root: Path, reference_pool: Dict[str, str], keep_list: Set[str]) -> List[Candidate]:
    component_root = root / "src" / "components"
    if not component_root.exists():
        return []

    candidates: List[Candidate] = []
    for file in component_root.rglob("*"):
        if not file.is_file() or file.suffix.lower() not in COMPONENT_EXTS:
            continue

        rel = normalize_rel(file, root)
        if rel in keep_list:
            continue
        stem = file.stem
        tag = extract_component_tag_name(file)
        keywords = [rel, stem, tag]
        hits = non_self_reference_hits(rel, reference_pool, keywords)
        weak_signals: List[str] = []
        history_pattern_hit = infer_history_file(file)
        weak_hits = find_weak_mentions(rel, reference_pool, tag)
        if weak_hits:
            weak_signals.append("存在弱引用线索（可能运行时注册或动态模板）")
        if hits:
            continue

        risk = pick_risk(weak_signals, history_pattern_hit=history_pattern_hit)
        evidence = [f"未发现 import/注册/模板标签对 `{stem}` 的使用"]
        if history_pattern_hit:
            evidence.append("命中历史文件命名模式(copy/bf/old)")
        evidence.extend(weak_signals)
        candidates.append(
            Candidate(
                path=rel,
                category="unused_component",
                risk_level=risk,
                evidence=evidence,
            )
        )
    return candidates


def analyze_history_files(root: Path, reference_pool: Dict[str, str]) -> List[Candidate]:
    candidates: List[Candidate] = []
    for rel, _ in reference_pool.items():
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
    parser = argparse.ArgumentParser(description="Analyze cleanup candidates for Vue project.")
    parser.add_argument("--project-root", default=".", help="Project root path")
    parser.add_argument(
        "--targets",
        nargs="*",
        default=[],
        help="Optional targets. Empty means auto-scan current workspace.",
    )
    parser.add_argument("--keep-list", default="", help="Optional keep-list file path")
    parser.add_argument("--output", required=True, help="Output JSON path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.project_root).resolve()
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    files = collect_code_files(root)
    reference_pool = build_reference_pool(files, root)
    keep_list = load_keep_list(root, args.keep_list)

    candidates: List[Candidate] = []
    targets = {t.replace("\\", "/").strip("/") for t in args.targets}
    # Empty targets => auto-scan from current workspace root.
    scan_all = len(targets) == 0 or "." in targets or "src" in targets
    if scan_all or "src/page" in targets or "src/pages" in targets:
        candidates.extend(analyze_pages(root, reference_pool, keep_list))
    if scan_all or "src/components" in targets:
        candidates.extend(analyze_components(root, reference_pool, keep_list))
    # dead code history scan can apply globally
    candidates.extend(analyze_history_files(root, reference_pool))

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
