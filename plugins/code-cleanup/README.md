<h1 align="center">✨ Code Cleanup Plugin</h1>

<p align="center">
  <strong>面向任意项目的多语言安全清理工具，智能识别未引用资源与死代码</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Plugin-Claude_Code-blueviolet.svg" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
</p>

---

## 🚀 核心能力

- **多语言引用识别**：支持 JS/TS、Python、Go、Java、PHP、Ruby、Rust、C++ 等各语言 `import/require` 语法的精确引用检测。
- **原生 Git 与 .gitignore 支持**：自动遵守项目的忽略规则，并优先使用 Git 指令（`git ls-files`）获取文件，扫描速度极快。
- **项目个性化配置**：支持在项目根目录创建 `.code-cleanup/` 文件夹（包含 `keep-list.txt` 等）实现差异化配置。
- **自动剪枝 (Directory Pruning)**：智能跳过 `node_modules`、`.idea`、`.vscode` 等巨大目录，非 Git 环境下也能高效完成。
- **工业风可视化报告**：生成带项目健康分看板、风险分级表格和“清理战果”对比横幅的 HTML 报告。
- **AI 自动化清理闭环**：Agent 可根据扫描结果，在用户授权后自动执行文件清理及残留空目录清扫。
- **历史死代码识别**：自动发现 `*-copy.*`, `*-bf.*`, `*-old.*` 等历史备份残留。

## 📦 产物说明

执行完成后，在**当前执行命令的目录 (CWD)** 下的 `.skill-workspace/code-cleanup/latest/` 生成以下产物：

| 文件 | 用途 |
|------|------|
| `cleanup-report.html` | **核心交互式报告**，建议在浏览器查看（包含清理前后战果对比） |
| `cleanup-report.md` | 文本摘要报告，供 AI 快速检索 |
| `deletion-candidates.json` | 机器可读数据，记录文件死因与风险等级 |
| `patch-plan.md` | 行动计划，包含空目录清理指令与回滚指南 |

## 🛡️ 安全边界

- **授权执行**：默认只生成候选名单，严禁在未获得用户明确确认的情况下执行物理删除。
- **风险降级**：遇到动态加载、运行时注册、字符串路径命中时，风险等级自动降级为 `medium`。
- **彻底清扫**：删除文件后会自动清扫因文件删除产生的空目录。
- **建议回滚**：始终提供 `git checkout` 等回滚建议，确保操作可逆。
