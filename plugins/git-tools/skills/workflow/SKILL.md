---
name: workflow
description: >-
  用户询问当前仓库的分支、提交或发布方式时使用。
  按仓库现有分支回答，不初始化 GitFlow，不改 JIRA、Slack 或分支保护。
---

# Workflow

先看现有分支、最近提交和是否已有 PR 模板。用仓库已经在用的流程回答。

集成分支是 `dev` 时，不要创建 `develop`，也不要把功能分支合并到 `develop`。

不要执行：

- 初始化 GitFlow、GitHub Flow 或 Trunk Based 模板
- 修改远程分支保护
- 更新 JIRA 工单状态或发送 Slack
- 自动打版本标签、写 CHANGELOG 并合并到主分支

用户要求发布时，先说明当前版本和将要推送的分支，等用户确认后再做他点名的那一步。
