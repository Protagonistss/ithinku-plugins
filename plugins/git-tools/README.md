<h1 align="center">Git Tools</h1>

<p align="center">
  <strong>按仓库现有分支和提交格式处理 Git 操作。用户没明确要求时不提交、不推送、不重写历史。</strong>
</p>

---

## 技能

| 模块 | 做什么 |
|------|--------|
| **[Commit](./skills/commit/SKILL.md)** | 用户要求提交时，按最近的提交格式写说明。不跳过钩子，不加入密钥。 |
| **[Branch](./skills/branch/SKILL.md)** | 按现有分支创建、合并或删除。冲突预检不进入合并状态。 |
| **[History](./skills/history/SKILL.md)** | 查看和搜索历史。不交互式变基，不硬重置。 |
| **[Remote](./skills/remote/SKILL.md)** | 用户要求时才推送或拉取。不强制推送，不自动变基到 main。 |
| **[Workflow](./skills/workflow/SKILL.md)** | 按仓库已有流程回答。不初始化 GitFlow，不改外部工单。 |

## 命令

`/ct` 只在用户明确要求提交时执行。只要求看变更时，它给出说明，不暂存也不推送。

## 代理

`@git-expert` 使用上面的技能。已推送的提交保持原样。
