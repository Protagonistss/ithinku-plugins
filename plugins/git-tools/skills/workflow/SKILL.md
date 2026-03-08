---
name: workflow
description: |
  团队工作流管理技能 - 协作规范、自动化流程和最佳实践。
  当用户说"初始化工作流"、"创建功能分支"、"分配代码审查"、"发布版本"、"版本发布"、"code review"、"团队协作"、"gitflow"时使用此技能。
  支持工作流模板初始化(GitFlow/GitHub Flow)、功能分支管理、自动分配代码审查、版本发布管理、团队规范执行。
  重要特性：自动化团队协作流程，集成 JIRA/Slack 等工具。
disable-model-invocation: false
argument-hint: [init|start-feature|assign-review|release] [args...]
---

# Skill: Workflow

团队工作流管理技能 - 协作规范、自动化流程和最佳实践。

## 核心功能

- 🏗️ **工作流模板** - GitFlow、GitHub Flow、Trunk Based
- 👥 **代码审查** - 自动分配审查者和跟踪状态
- 🚀 **发布管理** - 版本控制和自动化发布流程
- 📋 **团队规范** - 提交规范、分支保护执行
- 🔗 **工具集成** - JIRA、Slack、GitHub/GitLab

## 快速使用

```bash
# 初始化工作流
/workflow init --template gitflow

# 创建功能分支
/workflow start-feature PROJ-123 "用户认证"

# 分配代码审查
/workflow assign-review

# 发布版本
/workflow release --type minor
```

## 工作流模板

### GitFlow（适合有发布周期的团队）
```
main (生产)
  └── develop (开发)
        ├── feature/* → 开发完成后合并到 develop
        ├── release/* → 从 develop 创建，测试后合并到 main
        └── hotfix/* → 从 main 创建，修复后合并到 main 和 develop
```

**初始化命令**：
```bash
/workflow init --template gitflow
# 创建：main, develop 分支
# 配置：分支保护规则
```

### GitHub Flow（适合持续部署）
```
main (始终可部署)
  └── feature/* → 开发完成后创建 PR 合并到 main
```

**初始化命令**：
```bash
/workflow init --template github-flow
# 配置：PR 模板、CI/CD
```

### Trunk Based（适合高频发布）
```
main (主干)
  └── short-lived/* → 短期分支（<1天），快速合并
```

## 功能开发流程

### 开始新功能
```bash
# 创建功能分支（自动命名）
/workflow start-feature PROJ-123 "用户认证"

# 等同于
git checkout develop
git pull origin develop
git checkout -b feature/PROJ-123-user-auth
```

### 功能完成流程
1. **代码自审** - 检查代码质量和规范
2. **提交变更** - 使用规范的 commit message
3. **创建 PR/MR** - 填写完整的描述
4. **请求审查** - 自动分配审查者
5. **处理反馈** - 修改并回复评论
6. **合并代码** - Squash 或保留提交历史

## 代码审查

### 自动分配审查者
```bash
# 基于代码所有权分配
/workflow assign-review --strategy codeowners

# 基于负载均衡分配
/workflow assign-review --strategy balanced

# 随机分配（排除作者）
/workflow assign-review --strategy random
```

### 审查检查清单
- [ ] 代码功能正确
- [ ] 有足够的测试覆盖
- [ ] 遵循编码规范
- [ ] 无安全漏洞
- [ ] 文档已更新
- [ ] 提交信息清晰

### 审查状态跟踪
```bash
# 查看待审查列表
/workflow review-status --pending

# 查看我的审查任务
/workflow review-status --mine
```

## 版本发布

### 语义化版本
- **MAJOR** (主版本) - 不兼容的 API 变更
- **MINOR** (次版本) - 向后兼容的功能新增
- **PATCH** (补丁版本) - 向后兼容的问题修复

### 发布流程
```bash
# 创建发布分支
/workflow release --type minor --version 2.1.0

# 执行步骤：
# 1. 从 develop 创建 release/2.1.0
# 2. 更新版本号
# 3. 更新 CHANGELOG
# 4. 测试和修复
# 5. 合并到 main 并打标签
# 6. 合并回 develop
# 7. 推送到远程
```

### 自动化发布
```json
{
  "release": {
    "autoChangelog": true,
    "autoTag": true,
    "notifySlack": true,
    "environments": ["staging", "production"]
  }
}
```

## 工具集成

### JIRA 集成
```bash
# 关联分支到 JIRA 工单
/workflow link-jira PROJ-123

# 自动更新工单状态
# feature 开始 → In Progress
# PR 创建 → In Review
# 合并完成 → Done
```

### Slack 集成
```bash
# 配置通知
/workflow config-slack --channel "#dev-notifications"

# 触发通知的事件：
# - 新 PR 创建
# - 审查请求
# - 合并完成
# - 发布开始/完成
```

## 配置

```json
{
  "workflow": {
    "template": "gitflow",
    "autoReview": true,
    "autoRelease": false,
    "integrations": ["slack", "jira"],
    "branchProtection": {
      "main": { "requiredReviews": 2, "requiredStatusChecks": ["ci"] },
      "develop": { "requiredReviews": 1 }
    }
  }
}
```

## 最佳实践

### ✅ 推荐做法
- 保持功能分支简短（< 3天）
- 及时响应代码审查请求
- 发布前进行充分测试
- 保持 CHANGELOG 更新

### ❌ 避免做法
- 跳过代码审查直接合并
- 长期存在的功能分支
- 不关联工单的提交
- 在发布分支上开发新功能

## 详细信息

- 🔗 [分支策略配置](../../references/config/branch-strategies.md)
- 🔗 [提交类型配置](../../references/config/commit-types.md)
- 🔗 [错误处理](../../references/errors/error-types.md)
