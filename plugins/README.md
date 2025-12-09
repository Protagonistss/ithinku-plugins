# Claude Code 插件开发指南

这个目录包含所有自定义的 Claude Code 插件。每个插件都遵循标准的目录结构和配置格式。

## 现有插件

### 1. Code Review Plugin（代码审查插件）

专业的代码审查和安全分析工具。

**功能**：
- 🔍 全面代码审查（/review）
- 🔒 安全专项检查（/security）
- ⚡ 性能分析（/performance）
- 🤖 代码审查专家（CodeReviewer）
- 🛡️ 安全审查专家（SecurityExpert）
- 📊 代码分析技能
- 🔐 安全审查技能
- 🚀 性能审查技能

**使用场景**：代码质量把控、安全检查、性能优化

[查看详情](code-review/README.md)

### 2. Dev Tools Plugin（开发工具插件）

面向开发者的专业工具集。

**功能**：
- 🚀 代码生成（/gen）
- 🏗️ 架构设计专家（Architect）
- 🔧 重构技能

**使用场景**：代码开发、架构设计、代码重构

[查看详情](dev-tools/README.md)

## 插件结构

每个 Claude Code 插件都遵循以下标准结构：

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # 插件元数据（必需）
├── commands/                 # 自定义斜杠命令（可选）
│   └── command-name.md
├── agents/                   # 自定义代理（可选）
│   └── agent-name.md
├── skills/                   # 代理技能（可选）
│   └── skill-name/
│       └── SKILL.md
├── hooks/                    # 事件处理程序（可选）
│   └── hooks.json
└── README.md                 # 插件使用说明
```

## 插件开发

### 快速开始

1. **创建插件目录**
```bash
cd plugins
mkdir my-new-plugin
cd my-new-plugin
```

2. **创建基础结构**
```bash
mkdir -p .claude-plugin commands agents skills hooks
```

3. **编写插件元数据**
创建 `.claude-plugin/plugin.json`：
```json
{
  "name": "my-new-plugin",
  "version": "1.0.0",
  "description": "我的新插件",
  "author": "Your Name"
}
```

4. **添加功能**
根据需要创建：
- 命令文件（Markdown）
- 代理定义（Markdown）
- 技能文件（SKILL.md）
- 事件钩子（JSON）

### 插件规范

#### 命令（Commands）
- 文件名即为命令名
- 使用 Markdown 格式
- 包含用法说明和示例

#### 代理（Agents）
- 定义代理的角色和能力
- 描述专业领域和工作方式
- 提供使用示例

#### 技能（Skills）
- 每个技能一个目录
- 包含 SKILL.md 文件
- 描述技能的具体能力

#### 钩子（Hooks）
- JSON 格式配置文件
- 定义事件处理程序
- 支持 onLoad、onCommand 等事件

## 安装使用

### 安装插件

```bash
# 复制插件到 Claude Code 插件目录
cp -r plugins/my-plugin ~/.config/claude/plugins/my-plugin
```

### 使用插件

在 Claude Code 中：
- 使用斜杠命令：`/command-name`
- 调用代理：`@agent-name`
- 技能会自动被代理使用

## 最佳实践

1. **命名规范**
   - 插件名：小写字母和连字符
   - 命令名：简短明了
   - 代理名：首字母大写

2. **文档完整**
   - 每个插件都有 README
   - 命令和代理包含示例
   - 技能说明清晰

3. **功能聚焦**
   - 每个插件专注特定领域
   - 避免功能重复
   - 保持插件独立性

## 开发路线图

### 已完成

- ✅ Code Review Plugin - 专业的代码审查和安全分析
- ✅ Dev Tools Plugin - 代码生成和架构设计工具

### 计划中

- 🔄 更多专业领域插件
- 🔄 插件间协作机制
- 🔄 更丰富的工具集成