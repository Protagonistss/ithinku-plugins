---
name: ct
description: 智能化的 Git 提交命令，自动分析代码变更并生成符合规范的提交信息
---

# Command: /ct

智能化的 Git 提交命令，自动分析代码变更并生成符合规范的提交信息。

## 重要规则

**绝对禁止在提交信息中添加 AI 工具标识**
- ❌ 禁止添加 "🤖 Generated with Claude Code"、"Co-Authored-By: Claude" 等标识
- ✅ 提交信息应专注于描述代码变更本身，保持专业和纯粹

> 💡 **提示**：本命令对应 [commit 技能](../skills/commit/SKILL.md)，技能提供更详细的功能说明和配置选项。

## 用法

```bash
/commit [action] [options]
```

### 主要操作

- `analyze` - 分析当前变更并生成提交信息（默认）
- `check` - 执行质量检查，不实际提交
- `commit` - 一键提交（分析 + 检查 + 提交）

### 常用参数

**提交控制**
- `--type <type>` - 指定提交类型（feat, fix, refactor, docs, style, test, chore 等）
- `--scope <scope>` - 指定影响范围
- `--auto` - 自动模式，不询问直接提交
- `--amend` - 修改上一个提交

**推送相关**
- `--push` - 提交后自动推送
- `--push-to <remote/branch>` - 推送到指定分支

**检查选项**
- `--check-lint` - 提交前运行代码检查
- `--check-test` - 提交前运行测试
- `--check-all` - 运行所有检查（默认）

**分支管理**
- `--create-branch` - 自动创建新分支
- `--branch-type <type>` - 指定分支类型（feature, hotfix, release）

> 📖 完整参数列表和高级功能请参考 [commit 技能文档](../skills/commit/SKILL.md)

## 快速示例

### 基础使用

```bash
# 分析变更并生成提交信息（交互式）
/commit analyze

# 执行质量检查
/commit check

# 一键提交（分析 + 检查 + 提交）
/commit commit

# 自动模式，不询问直接提交
/commit commit --auto
```

### 指定类型和范围

```bash
# 功能提交
/commit commit --type feat --scope auth

# 修复提交
/commit commit --type fix --scope api

# 重构提交
/commit commit --type refactor
```

### 提交并推送

```bash
# 提交并推送到当前分支
/commit commit --push

# 推送到指定分支
/commit commit --push-to origin/main
```

### 代码检查

```bash
# 提交前运行所有检查
/commit commit --check-all

# 只运行 lint 检查
/commit commit --check-lint
```

> 💡 更多示例和高级用法请参考 [commit 技能文档](../skills/commit/SKILL.md)

## 工作流程

1. **变更分析** - 自动识别文件类型和影响范围
2. **类型检测** - 智能识别提交类型（feat/fix/docs 等）
3. **Scope识别** - 根据文件路径自动确定变更模块
4. **信息生成** - 生成符合 Conventional Commits 规范的提交信息
5. **质量检查** - 检查敏感信息、TODO 等
6. **交互确认** - 确认后执行提交

> 📖 详细工作流程和提交类型说明请参考 [commit 技能文档](../skills/commit/SKILL.md)

## 提交信息格式

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**提交类型**：feat, fix, refactor, docs, style, test, chore, perf, ci, build

> 📖 完整的提交类型说明和模板请参考 [提交类型配置](../references/config/commit-types.md)

## 配置

在项目根目录创建 `git-tools.config.json`：

```json
{
  "commit": {
    "messageFormat": "conventional",
    "qualityChecks": true,
    "autoScope": true,
    "defaultType": "feat",
    "preCommitChecks": ["lint", "test"]
  }
}
```

> 📖 完整配置选项请参考 [commit 技能文档](../skills/commit/SKILL.md)

## 相关资源

- 📖 [commit 技能文档](../skills/commit/SKILL.md) - 完整功能说明
- 📖 [提交类型配置](../references/config/commit-types.md) - 提交类型详细说明
- 📖 [Git 工具函数](../references/utils/git-helpers.md) - 底层工具函数
- 📖 [错误处理](../references/errors/error-types.md) - 错误处理说明
- 🤖 [@git-expert](../agents/git-expert.md) - Git 专家代理

## 常见问题

### Q: 没有暂存的变更怎么办？
A: 使用 `git add` 暂存文件，或使用 `/commit commit --auto` 自动暂存所有变更。

### Q: 如何修改已提交的信息？
A: 使用 `--amend` 参数：`/commit commit --amend`

### Q: 推送失败怎么办？
A: 先拉取最新变更：`git pull --rebase origin main`，然后重新推送。

### Q: 如何跳过某些检查？
A: 使用 `--no-verify` 参数（谨慎使用），或配置中禁用特定检查。

## 插件集成

git-tools 会自动检测并集成以下插件：

- **code-review** - 提供更全面的代码质量检查
- **test-generator** - 自动生成缺失的测试用例

> 📖 详细集成说明请参考 [commit 技能文档](../skills/commit/SKILL.md)

## 最佳实践

1. **原子性提交** - 每个提交只做一件事
2. **清晰的提交信息** - 简洁描述做了什么和为什么
3. **及时提交** - 完成功能就提交，避免堆积
4. **使用分支** - feature/hotfix 分支开发
5. **保持专业性** - 不添加任何 AI 工具标识

> 📖 更多最佳实践请参考 [commit 技能文档](../skills/commit/SKILL.md)

## 相关命令和代理

- `/branch` - 分支管理
- `/history` - 历史管理
- `/remote` - 远程仓库管理
- `/workflow` - 工作流管理
- `@git-expert` - Git 专家代理

---

**让提交变得简单而规范！** 🚀

> 💡 需要更多帮助？使用 `@git-expert` 获取专业的 Git 指导