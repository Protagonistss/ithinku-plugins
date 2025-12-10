# Git Tools Plugin

智能Git工具集，提供自动化提交、分支管理和Git工作流优化。

## 功能特性

### 🔧 智能提交
- 自动分析代码变更
- 生成符合 Conventional Commits 规范的提交信息
- 智能检测提交类型和影响范围
- 支持交互式和自动模式

### 🌿 分支管理
- 智能分支命名
- 自动创建功能分支
- 分支保护规则检查
- 合并冲突处理

### 🔍 质量检查
- 提交前代码审查
- 自动生成测试用例
- 敏感信息检测
- 大文件变更警告

### 🔗 插件集成
- 与 code-review 插件集成，提供全面的代码质量检查
- 与 unit-test-generator 插件集成，自动生成缺失的测试
- 智能检测已安装的插件并动态启用相应功能

## 安装

```bash
# 从本地安装
cp -r plugins/git-tools ~/.config/claude/plugins/

# 或使用 Claude 包管理器（如果可用）
claude plugin install git-tools
```

## 使用方法

### 基础提交

```bash
# 智能分析和提交
/commit

# 自动模式，无需交互
/commit --auto

# 仅检查变更，不提交
/commit --check
```

### 指定提交类型

```bash
# 功能提交
/commit --type feat --scope auth

# 修复提交
/commit --type fix --scope api

# 重构提交
/commit --type refactor --scope performance
```

### 推送和分支管理

```bash
# 提交并推送
/commit --push

# 创建功能分支并提交
/commit --create-branch --branch-type feature

# 推送后创建 Pull Request
/commit --push --create-pr
```

### 与其他插件集成

```bash
# 运行代码审查
/commit --check

# 生成缺失的测试
/commit --check-test

# 运行所有检查
/commit --check-all
```

## 配置

在项目根目录创建 `.commit-config.json`：

```json
{
  "commit": {
    "defaultType": "feat",
    "defaultScope": "app",
    "maxSubjectLength": 50,
    "requireBody": true,
    "autoDetectScope": true,
    "pushDefault": false,
    "addSignature": false,
    "preCommitChecks": ["lint", "test"],
    "prePushChecks": ["security", "build"],
    "branchProtection": {
      "main": ["require-review", "require-ci"],
      "develop": ["require-ci"]
    },
    "autoCreateBranch": true,
    "branchNaming": {
      "feature": "feat/{scope}-{description}",
      "hotfix": "fix/{version}-{description}",
      "release": "release/{version}"
    },
    "integrations": {
      "codeReview": {
        "enabled": true,
        "severity": "warning",
        "autoFix": false
      },
      "unitTest": {
        "enabled": true,
        "coverage": 80,
        "autoGenerate": false
      }
    }
  }
}
```

## 插件依赖

### 可选依赖

- **code-review** (>=1.0.0) - 提供全面的代码质量检查
  - 安装：`claude plugin install code-review`
  - 功能：安全检查、性能分析、最佳实践建议

- **unit-test-generator** (>=1.0.0) - 自动生成单元测试
  - 安装：`claude plugin install unit-test-generator`
  - 功能：智能测试用例生成、Mock数据生成、覆盖率优化

### 依赖检测

Git Tools 会自动检测这些插件是否安装：

- 如果插件未安装，会显示友好的提示信息
- 提供 `--check` 和 `--check-test` 参数的降级处理
- 不会因为缺少依赖插件而影响核心功能

## 命令参考

### /commit

所有参数：

- `--type` - 提交类型 (feat, fix, refactor, docs, style, test, chore, perf, ci, build)
- `--scope` - 提交影响范围
- `--interactive` - 交互式模式（默认）
- `--auto` - 自动模式，不询问直接提交
- `--check` - 运行代码检查（需要 code-review 插件）
- `--check-test` - 生成缺失测试（需要 unit-test-generator 插件）
- `--push` - 提交后自动推送
- `--create-branch` - 自动创建新分支
- `--branch-type` - 分支类型 (feature, hotfix, release)
- `--no-signature` - 不添加 Claude Code 签名

## 代理

### @GitExpert

Git 专家代理，可以处理各种 Git 相关的任务：

- 智能提交分析
- 分支策略设计
- 历史管理
- 工作流优化
- 问题诊断

使用示例：

```
@GitExpert 我的提交历史很混乱，能帮我整理吗？

@GitExpert 如何处理合并冲突？

@GitExpert 帮我设计一个适合团队的 Git 工作流
```

## 最佳实践

1. **原子性提交**
   - 每个提交只做一件事
   - 保持提交的独立性

2. **清晰的提交信息**
   - 使用 Conventional Commits 规范
   - 说明为什么这么做，而不仅仅是做了什么

3. **及时提交**
   - 完成一个功能就提交
   - 避免堆积大量变更

4. **使用分支**
   - 功能开发使用 feature 分支
   - 修复使用 hotfix 分支
   - 保持主分支的稳定

## 故障排除

### 常见问题

**Q: 提示 "code-review 插件未安装"**
A: 这是正常的提示。安装 code-review 插件可以获得更全面的代码质量检查，但不影响基本的提交功能。

**Q: 如何禁用插件集成？**
A: 在配置文件中设置 `"integrations": {"codeReview": {"enabled": false}}`

**Q: 提交信息太长怎么办？**
A: Git Tools 会自动截断过长的提交信息，保持在前50字符内。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

---

**让 Git 操作变得简单而高效！** 🚀