# 🚀 Claude Code 插件开发库 (ithinku-plugins)

本仓库是一个专为 **Claude Code** 打造的插件集成与开发环境。它旨在通过自定义命令、智能代理（Agents）和专业技能（Skills），将 Claude 转化为更强大的工程助手。

```text
ithinku-plugins/
├── plugins/                    # 插件核心目录
│   ├── code-polisher/         # 代码润色：自动优化代码风格与可读性
│   ├── code-review/           # 代码审查：安全、性能及质量全方位检查
│   ├── git-tools/             # Git 助手：智能提交、分支管理及工作流
│   ├── react-coder/           # React 专家：最佳实践与组件生成
│   ├── test-generator/        # 测试生成：单元测试、Mock 及覆盖率分析
│   ├── ui-design/             # UI/UX 设计：可访问性与核心设计规范
│   └── vue-coder/             # Vue 专家：Vue 2/3 组合式 API 支持
├── .claude-plugin/             # 插件市场元数据
└── README.md                   # 项目主文档
```

## 🛠️ 快速开始

### 1. 插件安装
在 Claude Code 会话中，使用 `/plugin add` 命令添加本地插件：

```bash
# 进入本仓库根目录后启动 Claude Code
claude

# 在 Claude Code 终端中执行安装命令
/plugin add ./plugins/code-review
/plugin add ./plugins/git-tools
# ...以此类推
```

或者手动将插件目录复制到 Claude 的全局插件目录：
- **Windows**: `%USERPROFILE%\.claude\plugins\`
- **macOS/Linux**: `~/.claude/plugins/`

### 2. 使用插件
安装后，插件提供的命令通常带有命名空间前缀。格式为：`/插件名:命令名`。

例如：
- `/code-review:review` - 执行代码审查
- `/git-tools:ct-cmd` - 执行 Git 提交助手

---

## 🧩 现有插件一览

| 插件名称 | 核心功能 | 触发示例 |
| :--- | :--- | :--- |
| **Code Review** | 代码质量、安全、性能审查 | `/code-review:review` |
| **Git Tools** | 语义化提交、分支策略、历史分析 | `/git-tools:ct-cmd`, `@git-expert` |
| **Test Gen** | 自动生成测试用例、Mock 数据 | `/test-generator:test` |
| **Code Polisher**| 提升代码可读性与表达力 | `@code-polisher` |
| **Frameworks** | React/Vue 框架开发支持 | `@react-coder`, `@vue-coder` |
| **UI Design** | 界面设计规范与辅助功能检查 | `@ui-design` |

---

## 🏗️ 插件开发标准

每个插件应遵循以下标准目录结构，以确保兼容性：

```bash
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # 必填：插件元数据（名称、版本、描述）
├── skills/              # 可选：自定义斜杠命令 (每个命令一个文件夹/SKILL.md)
├── agents/              # 可选：特定角色的智能代理 (.md)
├── hooks/               # 可选：生命周期或事件钩子 (hooks.json)
└── README.md            # 必填：插件使用说明书
```

### 开发建议
1. **命名规范**：文件夹使用 `kebab-case`（如 `my-plugin`），代理名使用 `PascalCase`（如 `@GitExpert`）。
2. **命令调用**：本地添加的插件在调用时需注意命名空间，防止命令冲突。
3. **路径测试**：开发时可使用 `claude --plugin-dir ./plugins/my-plugin` 快速预览。

---

## 🤝 贡献与反馈
- **新增插件**：请在 `plugins/` 下创建新文件夹并补全文档。
- **报告问题**：欢迎通过 Issue 或直接提交 PR 优化现有提示词。

---
**Happy Coding with Claude! 🚀**
