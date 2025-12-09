# Command: /commit

智能化的 Git 提交命令，自动分析代码变更并生成符合规范的提交信息。

## 描述

/commit 命令帮助开发者进行标准化的 Git 提交，自动分析代码变更、生成符合 Conventional Commits 规范的提交信息，并提供完整的提交流程管理。

## 用法

```
/commit [options]
```

### 参数

- `--type` - 提交类型（feat, fix, refactor, docs, style, test, chore, perf, ci, build）
- `--scope` - 提交影响范围
- `--interactive` - 交互式模式（默认）
- `--auto` - 自动模式，不询问直接提交
- `--split` - 智能拆分提交建议
- `--check` - 仅检查，不实际提交
- `--template` - 使用自定义模板
- `--amend` - 修改上一个提交
- `--push` - 提交后自动推送到远程仓库
- `--push-to <remote/branch>` - 推送到指定的远程分支
- `--no-push` - 明确不推送（默认行为）
- `--create-branch` - 如果需要，自动创建新分支
- `--branch-type <type>` - 指定分支类型（feature, hotfix, release）
- `--branch-name <name>` - 自定义分支名称
- `--check-lint` - 提交前运行代码检查
- `--check-test` - 提交前运行测试
- `--check-format` - 检查代码格式
- `--check-all` - 运行所有检查（默认配置）
- `--create-pr` - 推送后创建 Pull Request
- `--draft-pr` - 创建草稿 PR
- `--assign <user>` - 指定 PR 审查人
- `--label <label>` - 添加 PR 标签
- `--no-signature` - 不添加 "Generated with Claude Code" 签名

## 示例

### 基础使用

```bash
# 智能分析和提交
/commit

# 自动模式，不需要交互
/commit --auto

# 仅检查变更，不提交
/commit --check

# 提交但不添加 Claude Code 签名
/commit --no-signature
```

### 指定提交类型

```bash
# 指定功能类型和范围
/commit --type feat --scope auth

# 修复类型
/commit --type fix --scope api

# 重构类型
/commit --type refactor --scope performance
```

### 推送相关

```bash
# 提交并推送到当前分支的远程跟踪分支
/commit --push

# 提交并推送到指定分支
/commit --push-to origin/main

# 强制推送（谨慎使用）
/commit --push --force-with-lease
```

### 分支管理

```bash
# 自动创建 feature 分支并提交
/commit --create-branch --branch-type feature

# 创建指定名称的分支
/commit --create-branch --branch-name feature/user-auth

# 创建 hotfix 分支
/commit --branch-type hotfix --push
```

### 代码检查集成

```bash
# 提交前运行所有检查
/commit --check-all

# 只运行 lint 检查
/commit --check-lint

# 运行测试和 lint
/commit --check-test --check-lint
```

### Pull Request 集成

```bash
# 提交并推送后创建 PR
/commit --push --create-pr

# 创建草稿 PR 并指定审查人
/commit --push --draft-pr --assign @reviewer

# 带标签的 PR
/commit --push --create-pr --label enhancement
```

## 工作流程

### 1. 变更分析

```
🔍 分析代码变更...
📋 Git 状态:
  - 已暂存: 5 个文件
  - 未暂存: 2 个文件
  - 未跟踪: 1 个文件

📂 变更详情:
  + src/components/LoginForm.jsx (新增)
  M src/api/auth.js (修改)
  M tests/auth.test.js (修改)
  A .env.example (新增)
  D src/utils/old-helper.js (删除)
```

### 2. 类型检测

自动分析变更内容，识别提交类型：

- **feat**: 新增功能、新文件、新的 API
- **fix**: Bug 修复、异常处理
- **refactor**: 代码重构、性能优化
- **docs**: 文档更新、注释添加
- **style**: 代码格式化、样式调整
- **test**: 测试用例、测试覆盖率
- **chore**: 构建配置、依赖更新
- **perf**: 性能优化
- **ci**: CI/CD 配置
- **build**: 构建系统或外部依赖

### 3. Scope 识别

根据文件路径自动识别影响范围：

```javascript
const scopeMappings = {
  'src/auth/': 'auth',
  'src/api/': 'api',
  'src/ui/': 'ui',
  'src/components/': 'components',
  'docs/': 'docs',
  'tests/': 'test',
  'config/': 'config',
  'scripts/': 'scripts'
};
```

### 4. 提交信息生成

基于分析结果生成标准化提交信息：

```markdown
feat(auth): 实现用户登录功能

- 添加登录表单组件
- 集成认证 API
- 实现错误处理
- 添加单元测试

Closes #123
```

### 5. 交互确认

提供友好的交互界面：

```
💡 建议提交信息:
feat(auth): 实现用户登录功能

📝 详细描述:
- 添加登录表单组件
- 集成认证 API
- 实现错误处理
- 添加单元测试

✅ 是否继续提交? [Y/n/edit/skip] y
```

## 提交信息模板

### 功能提交

```markdown
feat(scope): 添加功能描述

## 主要变更
- 具体变更内容1
- 具体变更内容2

## 影响
- 对现有功能的影响
- 新增的能力

## 测试
- 测试覆盖率情况

Closes #issue-number
```

### 修复提交

```markdown
fix(scope): 修复问题描述

## 问题原因
- 问题产生的原因
- 影响范围

## 修复方案
- 修复的具体方法
- 预防措施

Fixes #issue-number
```

### 重构提交

```markdown
refactor(scope): 重构描述

## 重构原因
- 代码异味问题
- 性能瓶颈

## 改进效果
- 可读性提升
- 性能提升数据
- 维护性改善
```

## 配置选项

项目根目录创建 `.commit-config.json`：

```json
{
  "commit": {
    "defaultType": "feat",
    "defaultScope": "app",
    "maxSubjectLength": 50,
    "requireBody": true,
    "requireIssue": false,
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
    "customTypes": [
      {
        "type": "perf",
        "description": "性能优化"
      }
    ],
    "scopes": [
      "auth",
      "api",
      "ui",
      "db",
      "config",
      "docs"
    ]
  }
}
```

## 高级功能

### 提交拆分

对于大型变更，智能建议拆分方案：

```bash
/commit --split

📊 变更分析:
- 总变更: 23 个文件
- 建议: 拆分为 3 个提交

💡 拆分建议:
1. feat(auth): 用户认证基础设施
   - 包含: auth.js, auth.test.js, config/auth.js

2. feat(ui): 登录界面组件
   - 包含: LoginForm.jsx, Login.css, Login.test.jsx

3. fix(api): 修复认证 API 问题
   - 包含: user.js, middleware/auth.js

是否按照建议拆分? [Y/n]
```

### 批量操作

```bash
# 批量提交所有暂存的变更
/commit --batch

# 批量提交并推送多个分支
/commit --batch --push --branches "feature/*"
```

### 历史分析

分析提交历史，提供改进建议：

```bash
/commit --analyze-history

📊 提交历史分析:
- 最近7天: 15 个提交
- 类型分布: feat(40%), fix(20%), refactor(15%)
- 平均提交大小: 3.2 个文件

💡 改进建议:
- 考虑合并小型提交
- 增加 chore 类型提交
- 保持提交信息一致性
```

## 错误处理

### 常见错误

1. **没有暂存的变更**
```
❌ 没有检测到暂存的变更
💡 使用 'git add <files>' 暂存文件
📋 或使用 'git add -A' 暂存所有变更
```

2. **工作区有未暂存的变更**
```
⚠️  检测到未暂存的变更:
  - src/example.js (未暂存)
💡 是否要暂存这些文件? [Y/n/all]
```

3. **推送冲突**
```
❌ 推送失败: 远程有新的提交
💡 建议先拉取最新变更:
  git pull --rebase origin main
```

### 恢复操作

```bash
# 取消最近的提交（保留变更）
/commit --undo

# 完全删除最近的提交
/commit --undo --hard

# 恢复到指定的提交
/commit --restore <commit-hash>
```

## 集成示例

### 与代码审查集成

```bash
# 提交前自动运行代码审查
/commit --check --review

# 输出:
🔍 运行代码审查...
📋 审查结果:
  - 1 个安全问题 (高优先级)
  - 2 个性能建议
  - 3 个代码规范问题

❌ 发现问题，建议修复后再提交
```

### 与 CI/CD 集成

```bash
# 提交并触发 CI
/commit --push --trigger-ci

# 输出:
✅ 提交成功
📤 推送到远程
🔄 触发 CI 流程...
🔗 构建链接: https://ci.example.com/build/123
```

## 最佳实践

1. **原子性提交**
   - 每个提交只做一件事
   - 保持提交的独立性
   - 避免混合不同类型的变更

2. **清晰的提交信息**
   - 用简洁的语言描述做了什么
   - 说明为什么这么做
   - 包含相关 Issue 或 PR 编号

3. **及时提交**
   - 完成一个功能就提交
   - 避免堆积大量变更
   - 保持提交历史的连贯性

4. **使用分支**
   - 开发新功能使用 feature 分支
   - 修复使用 hotfix 分支
   - 保持主分支的稳定性

## 常见问题

### Q: 如何处理大型功能开发？

A: 建议使用 feature 分支，定期提交，最后通过 PR 合并：
```bash
/commit --branch-type feature --create-branch
```

### Q: 如何修改已提交的信息？

A: 使用 amend 功能：
```bash
/commit --amend
```

### Q: 如何处理提交冲突？

A: 建议先拉取最新变更，然后重新提交：
```bash
git pull --rebase origin main
/commit --continue
```

### Q: 如何跳过某些检查？

A: 使用 --skip-<check> 参数：
```bash
/commit --skip-lint --skip-test
```

## 相关命令

- `/review` - 代码审查
- `/gen` - 代码生成
- `/refactor` - 代码重构
- `@GitExpert` - Git 专家代理

## 快捷键配置

可以在 `.gitconfig` 中添加快捷别名：

```bash
[alias]
  cm = "!claude /commit"
  cma = "!claude /commit --auto"
  cmp = "!claude /commit --push"
  cmr = "!claude /commit --review"
```

## 扩展和自定义

### 自定义提交类型

在 `.commit-config.json` 中添加：

```json
{
  "customTypes": [
    {
      "type": "perf",
      "description": "性能优化",
      "emoji": "⚡"
    },
    {
      "type": "revert",
      "description": "回滚提交",
      "emoji": "⏪"
    }
  ]
}
```

### 自定义模板

创建 `.commit-templates/` 目录：

```
.commit-templates/
  ├── feature.md
  ├── bugfix.md
  └── hotfix.md
```

然后在配置中指定：

```json
{
  "templates": {
    "feature": ".commit-templates/feature.md",
    "bugfix": ".commit-templates/bugfix.md"
  }
}
```

---

**让提交变得简单而规范！** 🚀