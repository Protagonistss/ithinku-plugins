# Code Cleanup Plugin

面向任意项目的多语言安全清理插件，支持 JS/TS、Python、Go、Java、PHP、Ruby、Rust、C++ 等多门语言。用于识别未引用模块、未使用组件和历史死代码，并生成可视化交互报告与 AI 辅助的自动化清理方案。

## 核心能力

- **多语言引用识别**：识别各语言 import/require 语法的精确引用（JS/TS/Py/Go/Java 等）。
- **原生 Git 与 .gitignore 支持**：自动遵守项目的 `.gitignore` 规则，并优先使用 Git 指令（`git ls-files`）获取文件，扫描速度极快。
- **项目个性化配置 (By-Project Config)**：支持在项目根目录创建 `.code-cleanup/` 文件夹（包含 `keep-list.txt` 等文件）来实现针对性配置，无需修改插件源码。
- **自动剪枝 (Directory Pruning)**：智能跳过 `node_modules`、`.idea` 等巨大目录，非 Git 环境下也能高效完成。
- **交互式可视化报告**：生成带风险统计卡片和可折叠表格的 HTML 报告。
- **AI 自动化清理闭环**：Agent 可根据扫描结果，在用户确认后自动执行文件清理。
- **历史死代码识别**：自动发现 `*-copy.*`, `*-bf.*`, `*-old.*` 等备份残留。
- **风险分级策略**：提供 `high` / `medium` / `low` 风险评估，确保清理安全。

## 产物说明

执行完成后，在工作区生成以下产物：

| 文件 | 用途 |
|------|------|
| `cleanup-report.html` | **核心交互式报告**，建议在浏览器查看 |
| `cleanup-report.md` | 文本摘要报告 |
| `deletion-candidates.json` | 机器可读数据，供 AI 执行自动清理 |
| `patch-plan.md` | 补丁计划与回滚指南 |

## 安全边界

- 默认只生成候选，不直接删除
- 动态加载、运行时注册、字符串路径命中时，降级为 `medium`
- 建议按小批次清理并执行最小回归测试
