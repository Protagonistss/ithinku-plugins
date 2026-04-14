<h1 align="center">✨ Git Tools Plugin</h1>

<p align="center">
  <strong>智能 Git 工作流助手，提供模块化、语义化的代码仓库管理能力</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Plugin-Claude_Code-blueviolet.svg" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
</p>

---

## 🚀 技能概览

本插件由多个核心技能模块组成，覆盖了从开发到发布的完整 Git 生命周期：

| 模块 | 核心能力 | 常用指令示例 |
|------|----------|----------|
| **[Commit](./skills/commit/SKILL.md)** | 智能提交信息生成、变更质量分析 | `/ct analyze`, `/ct create` |
| **[Branch](./skills/branch/SKILL.md)** | 分支策略执行、规范化命名、冲突处理 | `/branch create feature` |
| **[History](./skills/history/SKILL.md)** | 历史记录深度检索、提交重写与压缩 | `/history analyze`, `/history rebase` |
| **[Remote](./skills/remote/SKILL.md)** | 多远程仓库管理、安全推送与同步 | `/remote status`, `/remote push` |
| **[Workflow](./skills/workflow/SKILL.md)** | Git Flow/Trunk-based 工作流引导 | `/workflow init`, `/workflow release` |

## 🛠️ 快速开始

### 1. 安装插件
```bash
# 建议通过符号链接保持与开发目录同步
ln -s $(pwd)/plugins/git-tools ~/.config/claude/plugins/git-tools
```

### 2. 标准提交流程
```bash
# 第一步：分析当前暂存区变更的语义
/ct analyze

# 第二步：交互式生成符合 Angular 规范的提交信息
/ct create

# 第三步：安全推送到当前分支的远程追踪分支
/remote push
```

### 3. 分支管理示例
```bash
# 快速开启一个遵循命名规范的功能分支
/branch create feature "user-auth-module"

# 完成后执行安全的合并操作
/branch merge feature/user-auth-module into main
```

## 🤖 智能代理 (Agents)

- **`@git-expert`**：Git 领域的全知专家，能够处理复杂的变基、冲突和仓库恢复任务。

## 📖 参考指南
- **[分支策略](./references/config/branch-strategies.md)**
- **[提交规范](./references/config/commit-types.md)**
- **[错误对照表](./references/errors/error-types.md)**
