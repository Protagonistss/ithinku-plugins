#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render cleanup report and patch plan from candidates JSON.")
    parser.add_argument("--input", required=True, help="Input deletion-candidates.json")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    return parser.parse_args()


def load_candidates(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def render_report(data: Dict) -> str:
    grouped = defaultdict(list)
    for item in data.get("candidates", []):
        grouped[item.get("risk_level", "unknown")].append(item)

    lines: List[str] = []
    lines.append("# Cleanup Report")
    lines.append("")
    lines.append(f"- 生成时间: {data.get('generated_at', '')}")
    lines.append(f"- 项目根目录: `{data.get('project_root', '')}`")
    lines.append("")
    summary = data.get("summary", {})
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- high: {summary.get('high', 0)}")
    lines.append(f"- medium: {summary.get('medium', 0)}")
    lines.append(f"- low: {summary.get('low', 0)}")
    lines.append("")

    for level in ("high", "medium", "low"):
        items = grouped.get(level, [])
        lines.append(f"## {level.upper()} Risk")
        lines.append("")
        if not items:
            lines.append("- 无")
            lines.append("")
            continue
        for item in items:
            lines.append(f"- 路径: `{item['path']}`")
            lines.append(f"  - 类型: `{item['category']}`")
            lines.append(f"  - 建议: `{item.get('suggested_action', '')}`")
            evidence = item.get("evidence", [])
            if evidence:
                lines.append("  - 证据:")
                for ev in evidence:
                    lines.append(f"    - {ev}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_patch_plan(data: Dict) -> str:
    high = [x for x in data.get("candidates", []) if x.get("risk_level") == "high"]
    medium = [x for x in data.get("candidates", []) if x.get("risk_level") == "medium"]
    low = [x for x in data.get("candidates", []) if x.get("risk_level") == "low"]

    lines: List[str] = []
    lines.append("# Patch Plan")
    lines.append("")
    lines.append(f"- 生成时间: {datetime.now(timezone.utc).isoformat()}")
    lines.append("- 默认策略: 先处理高风险候选，再人工验证中风险候选")
    lines.append("")
    lines.append("## Step 1: 处理高风险候选")
    lines.append("")
    if not high:
        lines.append("- 当前没有高风险候选。")
    else:
        for item in high:
            lines.append(f"- 删除候选: `{item['path']}` (`{item['category']}`)")
    lines.append("")
    lines.append("## Step 2: 处理中风险候选")
    lines.append("")
    if not medium:
        lines.append("- 当前没有中风险候选。")
    else:
        for item in medium:
            lines.append(f"- 人工确认后处理: `{item['path']}`")
    lines.append("")
    lines.append("## Step 3: 处理低风险候选")
    lines.append("")
    if not low:
        lines.append("- 当前没有低风险候选。")
    else:
        lines.append("- 低风险项通常由命名模式命中，证据较弱，建议先观察后处理。")
        for item in low:
            lines.append(f"- 建议延后处理: `{item['path']}`")
    lines.append("")
    lines.append("## 回滚建议")
    lines.append("")
    lines.append("- 建议先创建分支并分批提交，每批删除 5-10 个文件。")
    lines.append("- 每批执行最小回归（登录、课程列表、页面跳转、关键组件渲染）。")
    lines.append("- 若有异常，按提交粒度回滚最近批次。")
    lines.append("")
    lines.append("## 回滚命令")
    lines.append("")
    lines.append("```bash")
    lines.append("# 恢复单个文件")
    lines.append("git checkout -- <file_path>")
    lines.append("")
    lines.append("# 回滚最近一次提交（保留工作区修改）")
    lines.append("git reset --soft HEAD~1")
    lines.append("")
    lines.append("# 回滚最近一次提交（完全撤销）")
    lines.append("git revert HEAD")
    lines.append("```")
    lines.append("")
    if high or medium or low:
        lines.append("## 按文件恢复示例")
        lines.append("")
        all_candidates = high + medium + low
        for item in all_candidates[:20]:  # 最多展示前 20 个
            lines.append(f"- `git checkout -- {item['path']}`")
        if len(all_candidates) > 20:
            lines.append(f"- ... 以及其他 {len(all_candidates) - 20} 个文件")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    data = load_candidates(input_path)
    report = render_report(data)
    patch_plan = render_patch_plan(data)

    (output_dir / "cleanup-report.md").write_text(report, encoding="utf-8")
    (output_dir / "patch-plan.md").write_text(patch_plan, encoding="utf-8")
    print(f"Generated cleanup-report.md and patch-plan.md in {output_dir}")


if __name__ == "__main__":
    main()
