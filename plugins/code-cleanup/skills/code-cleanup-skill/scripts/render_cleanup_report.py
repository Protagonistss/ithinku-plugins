#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List
from string import Template


def format_size(bytes_num: int) -> str:
    """将字节大小转换为可读格式。"""
    if bytes_num < 0: bytes_num = 0
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.2f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.2f} PB"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render cleanup report and patch plan from candidates JSON.")
    parser.add_argument("--input", required=True, help="Input deletion-candidates.json")
    parser.add_argument("--previous", default="", help="Optional previous deletion-candidates.json for comparison")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    return parser.parse_args()


def load_candidates(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def render_report(data: Dict) -> str:
    grouped = defaultdict(list)
    for item in data.get("candidates", []):
        grouped[item.get("risk_level", "unknown")].append(item)

    stats = data.get("project_stats", {})
    
    lines: List[str] = []
    lines.append("# Cleanup Report")
    lines.append("")
    lines.append(f"- 生成时间: {data.get('generated_at', '')}")
    lines.append(f"- 项目根目录: `{data.get('project_root', '')}`")
    lines.append("")
    
    lines.append("## Global Dashboard (项目全局状况)")
    lines.append("")
    lines.append(f"- **项目健康度 (Health Score): {stats.get('health_score', 0)}%**")
    lines.append(f"- 总扫描文件数: {stats.get('total_files_scanned', 0)}")
    lines.append(f"- 项目总代码体积: {format_size(stats.get('total_size_bytes', 0))}")
    lines.append(f"- 待清理死代码文件数: {stats.get('unused_files_count', 0)}")
    lines.append(f"- 待清理死代码总体积: {format_size(stats.get('unused_size_bytes', 0))}")
    lines.append("")

    summary = data.get("summary", {})
    lines.append("## Candidate Summary (风险摘要)")
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
            size_str = format_size(item.get("file_size_bytes", 0))
            lines.append(f"- 路径: `{item['path']}` ({size_str})")
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
            size_str = format_size(item.get("file_size_bytes", 0))
            lines.append(f"- 删除候选: `{item['path']}` ({size_str})")
    lines.append("")
    lines.append("## Step 2: 处理中风险候选")
    lines.append("")
    if not medium:
        lines.append("- 当前没有中风险候选。")
    else:
        for item in medium:
            size_str = format_size(item.get("file_size_bytes", 0))
            lines.append(f"- 人工确认后处理: `{item['path']}` ({size_str})")
    lines.append("")
    lines.append("## Step 3: 处理低风险候选")
    lines.append("")
    if not low:
        lines.append("- 当前没有低风险候选。")
    else:
        lines.append("- 低风险项通常由命名模式命中，证据较弱，建议先观察后处理。")
        for item in low:
            size_str = format_size(item.get("file_size_bytes", 0))
            lines.append(f"- 建议延后处理: `{item['path']}` ({size_str})")
    lines.append("")
    lines.append("## Step 4: 清理残留空目录")
    lines.append("")
    lines.append("- 文件删除后，建议执行以下命令清扫空目录：")
    lines.append("  - **Linux/macOS**: `find . -type d -empty -not -path './.git/*' -not -path './node_modules/*' -delete`")
    lines.append("  - **Windows (PS)**: `Get-ChildItem -Path . -Recurse -Directory | Where-Object { \$_.GetFileSystemInfos().Count -eq 0 } | Remove-Item`")
    lines.append("")
    lines.append("## Step 5: 生成战果对比报告")
    lines.append("")
    lines.append("- 清理完成后，再次运行扫描并执行对比：")
    lines.append("  `python analyze_cleanup_candidates.py --output after.json`")
    lines.append("  `python render_cleanup_report.py --input after.json --previous before.json --output-dir result/`")
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
    # No changes needed
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


def render_report_html(data: Dict, prev_data: Dict = None) -> str:
    grouped = defaultdict(list)
    for item in data.get("candidates", []):
        grouped[item.get("risk_level", "unknown")].append(item)

    summary = data.get("summary", {})
    gen_at = data.get("generated_at", "")
    project_root = data.get("project_root", "")
    stats = data.get("project_stats", {})

    health_score = stats.get("health_score", 0)
    health_color = "#22c55e" if health_score > 90 else "#f59e0b" if health_score > 70 else "#ef4444"

    # 处理对比逻辑 (Diff Logic)
    diff_html = ""
    if prev_data:
        prev_stats = prev_data.get("project_stats", {})
        files_removed = prev_stats.get("total_files_scanned", 0) - stats.get("total_files_scanned", 0)
        size_reduced_bytes = prev_stats.get("total_size_bytes", 0) - stats.get("total_size_bytes", 0)
        health_improved = stats.get("health_score", 0) - prev_stats.get("health_score", 0)
        
        if files_removed > 0 or size_reduced_bytes > 0:
            diff_html = f"""
            <div class="diff-banner">
                <div class="diff-title">🏆 CLEANUP ACHIEVED / 清理战果</div>
                <div class="diff-grid">
                    <div class="diff-item">
                        <span class="diff-label">Files Removed</span>
                        <span class="diff-value">+{files_removed}</span>
                    </div>
                    <div class="diff-item">
                        <span class="diff-label">Space Saved</span>
                        <span class="diff-value">{format_size(size_reduced_bytes)}</span>
                    </div>
                    <div class="diff-item">
                        <span class="diff-label">Health Boost</span>
                        <span class="diff-value">{"+" if health_improved >= 0 else ""}{health_improved} PTS</span>
                    </div>
                </div>
            </div>
            """

    html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cleanup Scan Report</title>
    <style>
        :root {
            --black: #000000;
            --white: #ffffff;
            --gray: #f0f0f0;
            --danger: #ff4d4d;
            --warning: #ffcc00;
            --info: #3399ff;
            --success-bg: #22c55e;
            --border-width: 3px;
        }
        * { box-sizing: border-box; }
        body { 
            font-family: 'JetBrains Mono', 'IBM Plex Mono', 'SFMono-Regular', Consolas, monospace;
            background-color: var(--white);
            color: var(--black);
            margin: 0;
            padding: 40px;
            line-height: 1.4;
        }

        header { 
            border: var(--border-width) solid var(--black);
            padding: 24px;
            margin-bottom: 40px;
            box-shadow: 8px 8px 0 var(--black);
        }
        h1 { 
            font-size: 32px; 
            font-weight: 900; 
            margin: 0 0 12px 0; 
            text-transform: uppercase; 
            letter-spacing: -1px;
        }
        .meta { font-size: 13px; font-weight: 500; }
        .meta code { background: var(--gray); padding: 2px 6px; border: 1px solid var(--black); }

        .diff-banner {
            background: var(--success-bg);
            border: var(--border-width) solid var(--black);
            padding: 20px;
            margin-bottom: 40px;
            box-shadow: 8px 8px 0 var(--black);
        }
        .diff-title { font-weight: 900; font-size: 18px; text-transform: uppercase; margin-bottom: 15px; border-bottom: 2px solid var(--black); padding-bottom: 5px; }
        .diff-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .diff-item { display: flex; flex-direction: column; }
        .diff-label { font-size: 11px; font-weight: 900; text-transform: uppercase; }
        .diff-value { font-size: 24px; font-weight: 900; }

        .dashboard { 
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 40px;
        }
        .stat-card { 
            border: var(--border-width) solid var(--black);
            padding: 20px;
            background: var(--white);
            box-shadow: 6px 6px 0 var(--black);
            transition: transform 0.1s;
        }
        .stat-card:hover { transform: translate(-2px, -2px); box-shadow: 8px 8px 0 var(--black); }
        .stat-label { font-size: 11px; font-weight: 900; text-transform: uppercase; color: #666; display: block; margin-bottom: 8px; }
        .stat-value { font-size: 24px; font-weight: 900; display: block; }
        .stat-sub { font-size: 12px; font-weight: 600; margin-top: 4px; border-top: 1px solid var(--black); padding-top: 4px; }
        
        .risk-summary { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 40px; }
        .risk-box { 
            padding: 16px; 
            border: var(--border-width) solid var(--black);
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 4px 4px 0 var(--black);
        }
        .risk-box.high { background: var(--danger); }
        .risk-box.medium { background: var(--warning); }
        .risk-box.low { background: var(--info); }
        .risk-count { font-size: 28px; font-weight: 900; }
        .risk-label { font-size: 14px; font-weight: 900; text-transform: uppercase; }

        .section { margin-bottom: 60px; }
        .section-header { 
            background: var(--black);
            color: var(--white);
            padding: 10px 16px;
            font-size: 18px;
            font-weight: 900;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .section-header .count { background: var(--white); color: var(--black); padding: 0 8px; font-size: 14px; }

        .table-container { border: var(--border-width) solid var(--black); border-top: none; }
        table { width: 100%; border-collapse: collapse; background: var(--white); }
        th { 
            background: var(--gray);
            border-bottom: var(--border-width) solid var(--black);
            text-align: left;
            padding: 12px;
            font-size: 12px;
            font-weight: 900;
            text-transform: uppercase;
        }
        td { padding: 16px 12px; border-bottom: 1px solid var(--black); vertical-align: top; }
        tr:last-child td { border-bottom: none; }
        tr:hover td { background: var(--gray); }

        .file-path { font-weight: 700; color: var(--black); cursor: pointer; word-break: break-all; border-bottom: 2px solid transparent; }
        .file-path:hover { border-bottom-color: var(--black); }
        .file-size { font-size: 11px; font-weight: 700; margin-top: 4px; display: block; opacity: 0.6; }
        
        .category-tag { font-size: 11px; font-weight: 900; text-transform: uppercase; background: var(--black); color: var(--white); padding: 2px 8px; display: inline-block; }
        .evidence-list { margin: 0; padding: 0; list-style: none; font-size: 12px; font-weight: 500; }
        .evidence-list li { margin-bottom: 4px; padding-left: 12px; position: relative; }
        .evidence-list li::before { content: ">"; position: absolute; left: 0; font-weight: 900; }

        .empty-text { padding: 40px; text-align: center; font-weight: 900; text-transform: uppercase; border: var(--border-width) solid var(--black); border-top: none; }

        #copy-toast {
            position: fixed; bottom: 30px; right: 30px; background: var(--black); color: var(--white); padding: 12px 20px; font-weight: 900;
            font-size: 13px; display: none; border: var(--border-width) solid var(--white); box-shadow: 8px 8px 0 rgba(0,0,0,0.2); z-index: 1000; text-transform: uppercase;
        }
    </style>
</head>
<body>
    <header>
        <h1>Cleanup Analysis</h1>
        <div class="meta">DATE: <b>$gen_at</b> | ROOT: <code>$project_root</code></div>
    </header>

    $diff_html

    <div class="dashboard">
        <div class="stat-card">
            <span class="stat-label">HEALTH SCORE</span>
            <span class="stat-value health-score">$health_score%</span>
            <div class="stat-sub">Overall system integrity</div>
        </div>
        <div class="stat-card">
            <span class="stat-label">TOTAL SCAN</span>
            <span class="stat-value">$total_files</span>
            <div class="stat-sub">Size: $total_size</div>
        </div>
        <div class="stat-card">
            <span class="stat-label">CANDIDATES</span>
            <span class="stat-value">$unused_files</span>
            <div class="stat-sub">Waste: $unused_size</div>
        </div>
        <div class="stat-card">
            <span class="stat-label">POTENTIAL GAIN</span>
            <span class="stat-value">-$unused_perc%</span>
            <div class="stat-sub">Storage reduction</div>
        </div>
    </div>

    <div class="risk-summary">
        <div class="risk-box high"><span class="risk-label">High Risk</span><span class="risk-count">$s_high</span></div>
        <div class="risk-box medium"><span class="risk-label">Medium Risk</span><span class="risk-count">$s_medium</span></div>
        <div class="risk-box low"><span class="risk-label">Low Risk</span><span class="risk-count">$s_low</span></div>
    </div>

    $sections

    <div id="copy-toast">Path Copied</div>

    <script>
        function copyPath(path) {
            navigator.clipboard.writeText(path).then(() => {
                const toast = document.getElementById('copy-toast');
                toast.style.display = 'block';
                setTimeout(() => { toast.style.display = 'none'; }, 1500);
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
            items_html.append("<div class='empty-text'>No Candidates Identified</div>")
        else:
            items_html.append("<div class='table-container'><table>")
            items_html.append("<tr><th>Target File Path</th><th>Category</th><th>Evidence / Reasoning</th></tr>")
            for item in items:
                evidence_html = "".join([f"<li>{ev}</li>" for ev in item.get("evidence", [])])
                path = item['path'].replace("\\", "/")
                size_str = format_size(item.get("file_size_bytes", 0))
                items_html.append(f"""
                <tr>
                    <td>
                        <span class="file-path" onclick="copyPath('{path}')" title="Copy Path">{path}</span>
                        <span class="file-size">Size: {size_str}</span>
                    </td>
                    <td><span class="category-tag">{item['category'].replace('_', ' ')}</span></td>
                    <td><ul class="evidence-list">{evidence_html}</ul></td>
                </tr>
                """)
            items_html.append("</table></div>")

        sections_html.append(f"""
        <div class="section">
            <div class="section-header">
                <span>{level.upper()} RISK MODULES</span>
                <span class="count">{len(items)} FILES</span>
            </div>
            {"".join(items_html)}
        </div>
        """)

    # 计算百分比
    total_f = stats.get("total_files_scanned", 1)
    if total_f == 0: total_f = 1
    unused_f = stats.get("unused_files_count", 0)
    unused_perc = round((unused_f / total_f) * 100, 1)

    t = Template(html_template)
    return t.safe_substitute(
        gen_at=gen_at,
        project_root=project_root,
        diff_html=diff_html,
        health_score=health_score,
        total_files=stats.get("total_files_scanned", 0),
        total_size=format_size(stats.get("total_size_bytes", 0)),
        unused_files=unused_f,
        unused_size=format_size(stats.get("unused_size_bytes", 0)),
        unused_perc=unused_perc,
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
    
    prev_data = None
    if args.previous and Path(args.previous).exists():
        prev_data = load_candidates(Path(args.previous))

    report = render_report(data)
    patch_plan = render_patch_plan(data)
    html_report = render_report_html(data, prev_data)

    (output_dir / "cleanup-report.md").write_text(report, encoding="utf-8")
    (output_dir / "patch-plan.md").write_text(patch_plan, encoding="utf-8")
    (output_dir / "cleanup-report.html").write_text(html_report, encoding="utf-8")
    print(f"Generated cleanup-report.md, patch-plan.md and cleanup-report.html in {output_dir}")


if __name__ == "__main__":
    main()
