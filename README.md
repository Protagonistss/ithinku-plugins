<h1 align="center">🚀 Claude Code Plugin Repository</h1>

<p align="center">
  <strong>专为 <a href="https://claude.ai/code">Claude Code</a> 打造的插件集成与开发套件</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Development-yellow.svg" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/Version-1.0.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen.svg" alt="PRs Welcome">
</p>

<p align="center">
  本仓库提供了一系列自定义命令、智能代理（Agents）和专业技能（Skills），将 Claude 转化为更强大的工程助手。
</p>

---

## 📂 核心架构

使用更清晰的树状结构直观了解项目布局：

```text
ithinku-plugins/
├── plugins/                    # 🛠️ 插件核心目录
│   ├── code-polisher/         # 🔹 代码润色：自动优化风格与可读性
│   ├── code-review/           # 🔹 代码审查：安全、性能及质量检查
│   ├── git-tools/             # 🔹 Git 助手：智能提交、分支管理及流转
│   ├── react-coder/           # 🔹 React 专家：最佳实践与组件生成
│   ├── test-generator/        # 🔹 测试生成：单元测试、Mock 及覆盖率
│   ├── ui-design/             # 🔹 UI/UX 设计：可访问性与核心规范
│   └── vue-coder/             # 🔹 Vue 专家：Vue 2/3 组合式 API 支持
├── .claude-plugin/             # 🧩 插件市场元数据 (marketplace.json)
└── README.md                   # 📄 项目总控中心
```

---

## 🛠️ 安装指南

您可以根据需要通过 **Claude 官方市场**、**GitHub 远程地址** 或 **本地开发目录** 进行安装。

### 1. 通过 Claude 官方市场安装 (Recommended)
如果插件已发布到官方市场，您只需输入插件名称：

```bash
# 在 Claude Code 终端执行
/plugin add code-review
```

### 2. 注册为自定义市场安装 (Advanced)
您可以将本仓库注册为您的私有市场，注册后可以直接通过名称安装本仓库内的所有插件：

```bash
# 1. 注册本仓库市场
/plugin marketplace add Protagonistss/ithinku-plugins

# 2. 从本市场安装指定插件
/plugin add code-review
/plugin add git-tools
```

### 3. 通过 GitHub 远程地址安装
直接从本仓库的远程地址安装最新版本，无需克隆代码：

```bash
# 格式: /plugin add {GitHub_URL}
# 示例：安装代码审查插件
/plugin add https://github.com/Protagonistss/ithinku-plugins/tree/main/plugins/code-review
```

### 3. 本地开发安装 (Local Development)
如果您已克隆本仓库到本地，可以使用相对路径进行安装：

```bash
# 在本仓库根目录下执行
/plugin add ./plugins/code-review
```

> [!TIP]
> **独立 Skill 安装：** 如果您只需要单独的 Skill，可以直接安装对应的 `skills` 子目录：
> ```bash
> /plugin add ./plugins/code-review/skills/code-analysis
> /plugin add ./plugins/code-cleanup/skills/code-cleanup-skill
> ```

---

## 🧩 现有插件图谱

| 插件名称 | 核心功能描述 | 触发方式 |
| :--- | :--- | :--- |
| **🔍 Code Review** | 聚焦代码质量、安全性与性能审查 | `/code-review:review` |
| **🌳 Git Tools** | 语义化提交、分支管理与历史分析 | `/git-tools:ct-cmd` \| `@git-expert` |
| **🧪 Test Gen** | 自动生成测试用例、Mock 与覆盖率 | `/test-generator:test` |
| **✨ Code Polisher**| 提升代码可读性与表达力 | `@code-polisher` |
| **📦 Frameworks** | React / Vue 2 & 3 生态深度支持 | `@react-coder` \| `@vue-coder` |
| **🎨 UI Design** | 界面设计规范与 Accessibility 巡检 | `@ui-design` |

> [!NOTE]
> 仓库中另外保留了一个独立 Skill：`plugins/code-cleanup/skills/code-cleanup-skill`。
> 它不再作为插件发布，专门用于 Vue 多页面项目的瘦身分析与清理决策。

---

## 🏗️ 插件开发指南

欢迎为库贡献新的功能。请确保每个插件遵循以下标准结构：

```bash
plugin-name/
├── .claude-plugin/      # 必填：插件元数据
│   └── plugin.json      # 核心配置 (名称、版本、描述)
├── skills/              # 可选：自定义斜杠命令 (SKILL.md)
├── agents/              # 可选：智能角色代理 (.md)
├── hooks/               # 可选：生命周期钩子 (hooks.json)
└── README.md            # 必填：插件使用说明书
```

### 开发建议与规范
1.  **命名标准**：
    *   目录名：`kebab-case`（例：`my-awesome-plugin`）
    *   代理名：`PascalCase`（例：`@AwesomeAgent`）
2.  **调试技巧**：使用 `claude --plugin-dir ./plugins/my-plugin` 快速预览开发中的插件。
3.  **安装冲突**：建议在本地安装时使用特定的命名空间前缀，以防与其他插件冲突。

---

## 🤝 贡献与反馈
*   **提交新插件**：请在 `plugins/` 目录下创建新文件夹，并完善对应文档。
*   **改进建议**：欢迎通过 **Issue** 或 **Pull Request** 提交对提示词的优化。

<p align="center">
  <strong>Happy Coding with Claude! 🚀</strong>
</p>
