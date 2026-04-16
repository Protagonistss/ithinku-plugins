<h1 align="center">🛠️ Claude Code 插件全集</h1>

<p align="center">
  <strong>一套高度模块化、工程化的 Claude Code 增强套件，助力开发者实现极致生产力</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Total_Plugins-7-blueviolet.svg" alt="Total Plugins">
  <img src="https://img.shields.io/badge/Language-Multi-green.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Frameworks-React_|_Vue-orange.svg" alt="Frameworks">
</p>

---

## 📂 插件矩阵

本仓库包含以下精心打造的插件模块，旨在覆盖软件开发的完整生命周期：

### 🔍 质量与安全 (Quality & Security)
*   **[Code Review](./code-review/README.md)**：全方位代码审查专家，涵盖安全 (OWASP Top 10)、性能瓶颈及架构合理性。
*   **[Code Polisher](./code-polisher/README.md)**：代码润色工具，在不改变功能的前提下提升代码的清晰度与规范性。

### 🏗️ 框架与工程 (Development & Engineering)
*   **[React Coder](./react-coder/README.md)**：React 架构专家，支持高性能组件生成、Hooks 深度提取及最佳实践审计。
*   **[Vue Coder](./vue-coder/README.md)**：Vue 全版本助手，精通 Vue 3 Composition API 与 Vue 2 遗留代码重构。
*   **[UI Design](./ui-design/README.md)**：视觉设计插件，打破 AI 平庸审美，生成具有大胆风格 (Neo-Brutalism/Glassmorphism) 的界面。

### ⚙️ 工具与自动化 (Tools & Automation)
*   **[Git Tools](./git-tools/README.md)**：智能 Git 助手，提供语义化提交、规范化分支管理及复杂工作流自动化。
*   **[Test Generator](./test-generator/README.md)**：测试自动化专家，一键生成高覆盖率的单元测试、Mock 数据及边界用例。

### 🎯 独立 Skill (Standalone Skills)
*   **Code Cleanup Skill**：位于 `./code-cleanup/skills/code-cleanup-skill/SKILL.md`，专注于 Vue 多页面项目的瘦身分析，不再作为插件发布。

---

## 📖 插件标准结构

每一个插件都遵循严格的目录规范，确保高度的可插拔性：

```text
plugin-name/
├── agents/             # 🤖 智能代理定义 (Agent Prompts)
├── commands/           # ⌨️ 斜杠命令扩展 (/commands)
├── skills/             # 🎨 专业技能逻辑 (Skills & Business Logic)
├── .claude-plugin/     # 🧩 插件元数据 (plugin.json)
└── README.md           # 📄 详细说明文档
```

## 🛠️ 开发者指南

1. **创建新插件**：建议参考 `plugins/code-review` 的目录结构。
2. **本地调试**：使用符号链接 `ln -s` 将插件映射到 `~/.config/claude/plugins/`。
3. **元数据配置**：确保 `plugin.json` 中的 `description` 与 `README.md` 保持一致。
