# Claude Code 插件开发库

这是一个用于开发和管理 Claude Code 插件的个人仓库，帮助积累和组织自定义的命令、代理、技能和事件处理程序。

## 项目简介

Claude Code 支持通过插件系统扩展功能。本仓库用于：

- 📦 开发和维护多个 Claude Code 插件
- 🔧 管理自定义斜杠命令（Commands）
- 🤖 创建智能代理（Agents）
- ⚡ 定义代理技能（Skills）
- 🪝 配置事件钩子（Hooks）
- 📚 积累可复用的提示词和模板

## 项目结构

```
claude-plugins/
├── plugins/                      # 插件目录
│   ├── code-review/             # 代码审查插件
│   ├── dev-tools/               # 开发工具插件
│   └── unit-test-generator/     # 单元测试生成插件
├── shared/                       # 共享资源
│   ├── prompts/                 # 通用提示词片段
│   └── templates/               # 通用模板
├── .claude-plugin/               # 插件市场配置
│   └── marketplace.json          # 插件元数据和发布信息
├── .gitignore                   # Git 忽略文件
└── README.md                    # 项目说明（本文件）
```

## 快速开始

### 1. 安装插件

将插件目录复制到 Claude Code 的插件目录：

**Windows:**
```powershell
# 复制所有插件到 Claude Code
Copy-Item -Recurse plugins\* "$env:APPDATA\Claude\plugins\"
```

**macOS/Linux:**
```bash
# 复制所有插件到 Claude Code
cp -r plugins/* ~/.config/claude/plugins/
```

### 2. 重启 Claude Code

安装插件后，重启 Claude Code 以加载新插件。

### 3. 使用插件

在 Claude Code 中：

- 使用 `/command-name` 调用自定义命令
  - 例如：`/gen component Button` - 生成React组件
  - 例如：`/test src/utils/calculator.js` - 生成测试文件
  - 例如：`/review` - 审查当前代码
- 通过 `@agent-name` 与代理交互
  - 例如：`@TestExpert 如何测试异步函数？`
  - 例如：`@Architect 这个系统架构合理吗？`
- 代理会自动使用配置的技能

## 插件标准结构

每个插件应遵循以下结构：

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json              # 插件元数据（必需）
├── commands/                     # 自定义斜杠命令（可选）
│   └── command-name.md
├── agents/                       # 自定义代理（可选）
│   └── agent-name.md
├── skills/                       # 代理技能（可选）
│   └── skill-name/
│       └── SKILL.md
├── hooks/                        # 事件处理程序（可选）
│   └── hooks.json
└── README.md                     # 插件使用说明
```

### 文件说明

#### plugin.json（插件元数据）

定义插件的基本信息：

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "插件描述",
  "author": "作者名称",
  "homepage": "https://github.com/username/repo"
}
```

#### commands/（斜杠命令）

使用 Markdown 文件定义命令，文件名即为命令名：

```markdown
# Command: /hello

这是一个简单的问候命令。

## 用法

/hello [name]

## 示例

/hello World
```

#### agents/（代理）

使用 Markdown 文件定义代理的行为和特性：

```markdown
# Agent: Helper

我是一个助手代理，专门帮助你完成各种任务。

## 能力

- 回答问题
- 提供建议
- 执行任务
```

#### skills/（技能）

每个技能一个目录，包含 SKILL.md 文件：

```markdown
# Skill: My Skill

这个技能的描述和用途。

## 功能

- 功能 1
- 功能 2
```

#### hooks/（事件钩子）

使用 JSON 配置文件定义事件处理：

```json
{
  "onLoad": "console.log('Plugin loaded')",
  "onCommand": "handleCommand()"
}
```

## 现有插件

### 1. Code Review Plugin（代码审查插件）

专业的代码审查工具，提供全面的代码质量分析、安全检查和性能优化建议。

- **版本**: 1.0.0
- **Commands**: `/review` - 代码审查命令
- **Agents**:
  - `@CodeReviewer` - 代码审查代理
  - `@SecurityExpert` - 安全专家代理
- **Skills**:
  - 代码质量分析
  - 安全漏洞检测
  - 性能优化建议
  - 最佳实践指导

[查看详情](plugins/code-review/README.md)

### 2. Dev Tools Plugin（开发工具插件）

面向开发者的专业工具集，提供代码生成、Git管理、架构设计和重构支持。

- **版本**: 1.1.0
- **Commands**:
  - `/gen` - 代码生成（API、数据模型、UI组件等）
  - `/commit` - 智能Git提交管理
- **Agents**:
  - `@Architect` - 架构设计专家
  - `@GitExpert` - Git工作流专家
- **Skills**:
  - 代码生成模板
  - Git提交管理
  - 架构设计指导
  - 测试集成（可调用 unit-test-generator）

[查看详情](plugins/dev-tools/README.md)

### 3. Unit Test Generator Plugin（单元测试生成插件）

专业的单元测试生成工具，支持多种编程语言和测试框架。

- **版本**: 1.0.0
- **Commands**:
  - `/test` - 生成单元测试（默认使用 Vitest）
  - `/mock` - 生成Mock数据和Stub函数
  - `/coverage` - 测试覆盖率分析
- **Agents**:
  - `@TestExpert` - 测试专家代理
- **Skills**:
  - 智能代码分析
  - 多框架测试生成（Jest、Vitest、Pytest、JUnit等）
  - Mock数据生成
  - 测试断言生成

[查看详情](plugins/unit-test-generator/README.md)

## 插件协作

这些插件可以协同工作，提供完整的开发工作流：

```
开发流程示例：
1. /gen feature          → 生成功能代码（dev-tools）
2. /test src/feature.js  → 生成测试（unit-test-generator）
3. /review               → 代码审查（code-review）
4. /commit --push        → 提交代码（dev-tools）
```

## 开发新插件

### 步骤 1: 创建插件目录

```bash
cd plugins
mkdir my-new-plugin
cd my-new-plugin
```

### 步骤 2: 创建基础结构

```bash
mkdir -p .claude-plugin commands agents skills hooks
```

### 步骤 3: 编写插件元数据

创建 `.claude-plugin/plugin.json`：

```json
{
  "name": "my-new-plugin",
  "version": "0.1.0",
  "description": "我的新插件",
  "author": "Your Name"
}
```

### 步骤 4: 添加功能

根据需要添加 commands、agents、skills 或 hooks。

### 步骤 5: 测试和调试

将插件复制到 Claude Code 插件目录进行测试。

## 共享资源

### prompts/（提示词片段）

可复用的提示词模板，用于跨插件共享。

### templates/（配置模板）

常用的配置文件模板，快速创建新插件。

## 最佳实践

1. **命名规范**
   - 插件名使用小写和连字符：`my-plugin`
   - 命令名简短明了：`/gen`, `/review`
   - 代理名首字母大写：`CodeReviewer`

2. **文档完整**
   - 每个插件包含详细的 README
   - 命令和代理包含使用示例
   - 技能说明清晰的功能和用途

3. **版本管理**
   - 使用语义化版本号（Semantic Versioning）
   - 在 plugin.json 中更新版本
   - Git 提交时标注版本变更

4. **安全考虑**
   - 不在代码中硬编码敏感信息
   - 使用 .gitignore 排除密钥文件
   - 遵循最小权限原则

## 贡献指南

这是个人学习和积累的仓库，欢迎自己不断添加和改进：

1. 创建新分支进行开发
2. 完成功能后合并到主分支
3. 及时更新文档和示例

## 参考资料

- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
- [插件市场配置](.claude-plugin/marketplace.json)
- [共享提示词模板](shared/prompts/)
- [配置模板](shared/templates/)

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

**Happy Coding with Claude! 🚀**

