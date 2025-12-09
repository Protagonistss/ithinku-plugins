# Claude Code 插件开发库

这是一个用于开发和管理 Claude Code 插件的个人仓库，帮助积累和组织自定义的命令、代理、技能和事件处理程序。

## 项目介绍

Claude Code 支持通过插件系统扩展功能。本仓库用于：

- 📦 开发和维护多个 Claude Code 插件
- 🔧 管理自定义斜杠命令（Commands）
- 🤖 创建智能代理（Agents）
- ⚡ 定义代理技能（Skills）
- 🪝 配置事件钩子（Hooks）
- 📚 积累可复用的提示词和模板

## 项目结构

```
AI/
├── plugins/                      # 插件目录
│   ├── productivity-plugin/     # 生产力增强插件
│   ├── dev-tools-plugin/        # 开发工具插件
│   └── README.md                # 插件开发指南
├── shared/                       # 共享资源
│   ├── prompts/                 # 通用提示词片段
│   └── templates/               # 通用模板
├── .gitignore                   # Git 忽略文件
└── README.md                    # 项目说明（本文件）
```

## 快速开始

### 1. 安装插件

将插件目录复制到 Claude Code 的插件目录：

**Windows:**
```powershell
# 复制插件到 Claude Code
Copy-Item -Recurse plugins\productivity-plugin "$env:APPDATA\Claude\plugins\productivity-plugin"
```

**macOS/Linux:**
```bash
# 复制插件到 Claude Code
cp -r plugins/productivity-plugin ~/.config/claude/plugins/productivity-plugin
```

### 2. 重启 Claude Code

安装插件后，重启 Claude Code 以加载新插件。

### 3. 使用插件

在 Claude Code 中：

- 使用 `/command-name` 调用自定义命令
- 通过 `@agent-name` 与代理交互
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

### 1. Productivity Plugin（生产力插件）

提升日常工作效率的工具集。

- **Commands**: 快捷命令集合
- **Agents**: 任务助手
- **Skills**: 项目管理、时间管理

[查看详情](plugins/productivity-plugin/README.md)

### 2. Dev Tools Plugin（开发工具插件）

面向开发者的专业工具。

- **Commands**: 代码生成、重构工具
- **Agents**: 代码审查助手、架构顾问
- **Skills**: 代码分析、性能优化

[查看详情](plugins/dev-tools-plugin/README.md)

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
- [插件开发指南](plugins/README.md)
- [最佳实践集合](shared/README.md)

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

**Happy Coding with Claude! 🚀**

