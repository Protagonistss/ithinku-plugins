# Dev Tools Plugin

面向开发者的专业工具插件，提供代码生成、架构设计和重构支持。

## 插件信息

- **名称**：dev-tools
- **版本**：1.1.0
- **作者**：huangshan
- **类型**：开发工具

## 功能概览

这个插件为开发者提供专业的代码开发辅助工具：

- 🚀 快速生成代码模板
- 🏗️ 架构设计指导
- 🔧 重构建议和指导
- 📊 代码质量分析

> **注意**：Git 相关功能已迁移到独立的 [git-tools 插件](../git-tools/)，提供更强大的 Git 工作流支持。

## 包含的命令

### 1. /gen - 代码生成

快速生成各种代码模板和样板代码。

**支持的代码类型**：
- API 端点
- 数据模型
- 单元测试
- UI 组件
- CRUD 操作
- 中间件
- 配置文件

**用法**：
```
/gen api User
/gen model Product name:string price:number
/gen test UserService
/gen component Button
```

[详细文档](commands/gen.md)

> 💡 **Git 功能迁移**：`/commit` 命令已迁移到 [git-tools 插件](../git-tools/)，功能更强大！[查看迁移指南](commands/commit-redirect.md)

## 包含的代理

### 1. Architect - 架构设计专家

软件架构师，帮助你设计可扩展的系统。

**专长**：
- 🏗️ 系统架构设计
- 📐 设计模式应用
- 🔄 架构重构方案
- 🎯 技术选型建议

**使用方式**：
```
@Architect 帮我设计一个电商系统
@Architect 我们的系统该怎么重构？
```

[详细文档](agents/architect.md)

### 2. GitExpert - Git 专家代理

专业的 Git 专家，处理各种 Git 相关的任务和问题。

**专长**：
- 🔄 提交管理和历史优化
- 🌿 分支管理和策略设计
- 📊 Git 历史分析
- 🛠️ 工作流优化
- 🔧 高级 Git 操作

**使用方式**：
```
@GitExpert 帮我分析这个提交历史
@GitExpert 如何处理合并冲突？
@GitExpert 帮我优化 Git 工作流
```

> 💡 **Git 功能迁移**：GitExpert 代理已迁移到 [git-tools 插件](../git-tools/)，提供更专业的 Git 支持！

## 包含的技能

### 1. 重构 (Refactoring)

系统化的重构指导和方案。

**能力**：
- 重构模式应用
- 安全重构流程
- 重构风险控制
- 最佳实践

[详细文档](skills/refactoring/SKILL.md)

## 安装方法

### Windows

```powershell
Copy-Item -Recurse plugins\dev-tools "$env:APPDATA\Claude\plugins\dev-tools"
```

### macOS/Linux

```bash
cp -r plugins/dev-tools ~/.config/claude/plugins/dev-tools
```

安装后重启 Claude Code。

## 使用场景

### 场景 1：快速开发

```
你: /gen api User
（生成 REST API 模板）

你: /gen test UserAPI
（生成对应的测试代码）

```

> 💡 **提示**：需要 Git 提交功能？请安装 [git-tools 插件](../git-tools/)！

### 场景 2：架构设计

```
你: @Architect 我要开发一个博客系统，帮我设计架构

Architect: （提供完整的架构设计）
- 系统分层
- 技术选型
- 数据库设计
- 扩展方案
```

### 场景 3：代码重构

```
你: @Architect 这段代码架构合理吗？
（粘贴代码）

Architect: （提供架构分析和改进建议）
```

## 配置选项
```

### 代码生成配置

```json
{
  "generation": {
    "defaultLanguage": "javascript",
    "template": "standard",
    "includeTests": true
  }
}
```

## 最佳实践

### 1. 开发流程

```
1. 使用 /gen 快速生成代码模板
2. 编写具体的业务逻辑
3. 使用 /commit 进行智能提交
4. 必要时使用 @Architect 进行架构咨询
5. 使用 @GitExpert 解决 Git 问题
```

### 2. Git 工作流

```
1. 功能开发使用 feature 分支
2. 提交信息遵循 Conventional Commits 规范
3. 使用 /commit --auto 进行快速提交
4. 大型功能使用 /commit --split 拆分提交
5. 定期使用 @GitExpert 优化工作流
```

### 3. 架构设计

```
1. 开始前咨询 @Architect
2. 定期评估架构合理性
3. 遇到技术选型问题时寻求建议
4. 使用重构建议改进现有架构
```

## 常见问题

### Q: 如何自定义代码生成模板？

A: 当前版本使用内置模板。可以在配置文件中指定模板类型。

### Q: /commit 命令支持哪些提交类型？

A: 支持 Conventional Commits 规范的所有类型：feat, fix, docs, style, refactor, test, chore, perf, ci, build。

### Q: 如何处理复杂的 Git 操作？

A: 使用 @GitExpert 代理，它能处理各种复杂的 Git 场景，包括历史重写、分支策略等。

### Q: 提交后可以自动创建 PR 吗？

A: 可以，使用 `/commit --push --create-pr` 会在推送后自动创建 Pull Request。

## 相关插件

- **[Code Review Plugin](../code-review/)** - 专业的代码审查插件
  - 🔍 全面代码审查
  - 🔒 安全漏洞检查
  - ⚡ 性能分析

## 更新日志

### v1.1.0 (2024-12-09)

- ✨ 新增 `/commit` 命令：智能 Git 提交管理
- ✨ 新增 `@GitExpert` 代理：专业的 Git 专家
- ✨ 新增 `commit` 技能：提交分析和生成
- 🔄 重命名插件为 dev-tools（原 dev-tools-plugin）
- 📝 更新文档，添加 Git 工作流说明

### v1.0.0 (2024-12-03)

- ✨ 初始版本发布
- 🚀 `/gen` 代码生成命令
- 🏗️ `Architect` 架构设计代理
- 🔧 `refactoring` 重构技能

## 许可证

MIT License - 详见项目根目录 LICENSE 文件

---

**让我们一起写出更好的代码！🚀**