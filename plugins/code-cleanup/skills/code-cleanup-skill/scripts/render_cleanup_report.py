#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List
from string import Template


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


def render_report_html(data: Dict) -> str:
    grouped = defaultdict(list)
    for item in data.get("candidates", []):
        grouped[item.get("risk_level", "unknown")].append(item)

    summary = data.get("summary", {})
    gen_at = data.get("generated_at", "")
    project_root = data.get("project_root", "")

    html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Cleanup Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 1000px; margin: 0 auto; padding: 20px; background-color: #f8f9fa; }
        h1 { color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        .summary-cards { display: flex; gap: 20px; margin-bottom: 30px; }
        .card { flex: 1; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); text-align: center; color: white; }
        .card.high { background-color: #e74c3c; }
        .card.medium { background-color: #f39c12; }
        .card.low { background-color: #3498db; }
        .card-val { font-size: 2.5em; font-weight: bold; display: block; }
        .section { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .section-title { font-size: 1.5em; margin-top: 0; display: flex; align-items: center; }
        .badge { font-size: 0.6em; padding: 4px 8px; border-radius: 4px; margin-left: 10px; text-transform: uppercase; }
        .badge.high { background: #fee2e2; color: #991b1b; }
        .badge.medium { background: #fef3c7; color: #92400e; }
        .badge.low { background: #dbeafe; color: #1e40af; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { text-align: left; padding: 12px; border-bottom: 1px solid #eee; }
        th { background-color: #fcfcfc; }
        code { background-color: #f1f1f1; padding: 2px 4px; border-radius: 4px; font-family: monospace; font-size: 0.9em; cursor: pointer; }
        code:hover { background-color: #e2e2e2; }
        .evidence { font-size: 0.85em; color: #666; margin: 0; padding-left: 20px; }
        .meta { color: #666; font-size: 0.9em; margin-bottom: 20px; }
        .empty { color: #999; font-style: italic; }
    </style>
</head>
<body>
    <h1>Code Cleanup Report</h1>
    <div class="meta">
        生成时间: $gen_at<br>
        项目根目录: <code>$project_root</code>
    </div>

    <div class="summary-cards">
        <div class="card high"><span class="card-val">$s_high</span>High Risk</div>
        <div class="card medium"><span class="card-val">$s_medium</span>Medium Risk</div>
        <div class="card low"><span class="card-val">$s_low</span>Low Risk</div>
    </div>

    $sections

    <script>
        function copyPath(path) {
            navigator.clipboard.writeText(path).then(() => {
                alert('路径已复制: ' + path);
            });
        }
    </script>
</body>
</html>
    """

    sections_html = []
    for level in ("high", "medium", "low"):
        items = grouped.get(level, [])
        items_html = []
        if not items:
            items_html.append("<p class='empty'>未发现此类候选</p>")
        else:
            items_html.append("<table>")
            items_html.append("<tr><th>路径 (点击复制)</th><th>类别</th><th>证据</th></tr>")
            for item in items:
                evidence_html = "".join([f"<li>{ev}</li>" for ev in item.get("evidence", [])])
                path = item['path'].replace("\\", "/")
                items_html.append(f"""
                <tr>
                    <td><code onclick="copyPath('{path}')">{path}</code></td>
                    <td><span class='badge {level}'>{item['category']}</span></td>
                    <td><ul class='evidence'>{evidence_html}</ul></td>
                </tr>
                """)
            items_html.append("</table>")

        sections_html.append(f"""
        <div class="section">
            <h2 class="section-title">{level.upper()} Risk</h2>
            {"".join(items_html)}
        </div>
        """)

    t = Template(html_template)
    return t.safe_substitute(
        gen_at=gen_at,
        project_root=project_root,
        s_high=summary.get("high", 0),
        s_medium=summary.get("medium", 0),
        s_low=summary.get("low", 0),
        sections="".join(sections_html)
    )


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    data = load_candidates(input_path)
    report = render_report(data)
    patch_plan = render_patch_plan(data)
    html_report = render_report_html(data)

    (output_dir / "cleanup-report.md").write_text(report, encoding="utf-8")
    (output_dir / "patch-plan.md").write_text(patch_plan, encoding="utf-8")
    (output_dir / "cleanup-report.html").write_text(html_report, encoding="utf-8")
    print(f"Generated cleanup-report.md, patch-plan.md and cleanup-report.html in {output_dir}")


if __name__ == "__main__":
    main()
