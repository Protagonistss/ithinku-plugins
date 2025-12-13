# Git Tools Plugin

智能Git工具集，提供模块化的Git管理能力。

## 📋 技能概览

| 技能 | 核心功能 | 常用命令 |
|------|----------|----------|
| **[Commit](./skills/commit/SKILL.md)** | 智能提交、信息生成、质量检查 | `/commit analyze`, `/commit check`, `/commit commit` |
| **[Branch](./skills/branch/SKILL.md)** | 分支管理、策略、冲突解决 | `/branch create feature`, `/branch merge`, `/branch cleanup` |
| **[History](./skills/history/SKILL.md)** | 历史分析、重写、搜索 | `/history analyze`, `/history rebase`, `/history search` |
| **[Remote](./skills/remote/SKILL.md)** | 推送拉取、多仓库同步 | `/remote push --safe`, `/remote sync`, `/remote status` |
| **[Workflow](./skills/workflow/SKILL.md)** | 团队协作、工作流、发布 | `/workflow init`, `/workflow start-feature`, `/workflow release` |

## 🚀 快速开始

### 1. 安装

```bash
# 从本地安装
cp -r plugins/git-tools ~/.config/claude/plugins/

# 或使用 Claude 包管理器
claude plugin install git-tools
```

### 2. 基础提交流程

```bash
# 分析当前变更
/commit analyze

# 生成提交信息并提交
/commit commit

# 推送到远程
/remote push
```

### 3. 功能开发流程

```bash
# 创建功能分支
/branch create feature PROJ-123 "添加用户认证"

# 开发过程中提交
/commit commit

# 完成功能，合并到主分支
/branch merge feature/auth into main

# 清理分支
/branch cleanup
```

### 4. 团队协作

```bash
# 初始化团队工作流
/workflow init --template gitflow

# 代码审查
/workflow assign-review

# 发布版本
/workflow release --type minor
```

## ⚙️ 配置

创建 `git-tools.config.json`：

```json
{
  "git-tools": {
    "defaultWorkflow": "gitflow",
    "autoSafetyCheck": true,
    "enableIntegrations": true
  },
  "commit": {
    "messageFormat": "conventional",
    "qualityChecks": true,
    "autoScope": true
  },
  "branch": {
    "strategy": "gitflow",
    "autoNaming": true,
    "protection": true
  },
  "remote": {
    "safetyChecks": true,
    "autoSync": false
  },
  "workflow": {
    "autoReview": true,
    "autoRelease": false
  }
}
```

## 🔗 详细文档

- **[技能系统](./SKILLS.md)** - 完整的技能说明和架构
- **[References](./references/README.md)** - 通用组件和工具
  - [Git 工具函数](./references/utils/git-helpers.md)
  - [提交类型配置](./references/config/commit-types.md)
  - [分支策略配置](./references/config/branch-strategies.md)
  - [错误处理](./references/errors/error-types.md)

## 🔌 插件集成

### 可选依赖

- **code-review** - 全面的代码质量检查
  ```bash
  claude plugin install code-review
  ```

- **unit-test-generator** - 自动生成单元测试
  ```bash
  claude plugin install unit-test-generator
  ```

### 自动检测

Git Tools 会自动检测这些插件并启用相应功能，不会因缺少依赖而影响核心功能。

## 🤖 代理

### Git Expert

处理各种 Git 相关任务：

```
@GitExpert 我的提交历史很混乱，能帮我整理吗？
@GitExpert 如何处理合并冲突？
@GitExpert 帮我设计一个适合团队的 Git 工作流
```

## 💡 最佳实践

### 提交规范
- 使用 Conventional Commits 格式：`feat(scope): description`
- 提交前检查：敏感信息、TODO 标记
- 保持提交小而专注

### 分支管理
- 使用功能分支开发
- 定期同步远程分支
- 及时删除已合并的分支

### 历史管理
- 定期清理历史
- 使用 rebase 保持线性历史
- 创建重要节点的快照

### 团队协作
- 建立清晰的分支策略
- 自动化代码审查分配
- 使用集成工具提高效率

## ❓ 常见问题

**Q: 如何修改提交类型规则？**
A: 参考 [commit-types.md](./references/config/commit-types.md) 自定义类型和模式

**Q: 如何配置分支保护规则？**
A: 在分支策略配置中设置 protection 规则

**Q: 如何解决合并冲突？**
A: 使用 `/branch check-conflicts` 预测，`/branch merge --resolve` 自动解决

**Q: 如何设置多仓库推送？**
A: 配置 `remote.multiRemote.remotes` 列表

## 📚 命令参考

### Commit 命令
```bash
/commit analyze          # 分析变更
/commit check            # 质量检查
/commit commit           # 执行提交
/commit --auto           # 自动模式
```

### Branch 命令
```bash
/branch create <type>    # 创建分支
/branch merge <source>   # 合并分支
/branch check-conflicts  # 检查冲突
/branch cleanup          # 清理分支
```

### History 命令
```bash
/history analyze         # 分析历史
/history rebase <base>   # Interactive rebase
/history search <query>  # 搜索提交
/history snapshot        # 创建快照
```

### Remote 命令
```bash
/remote push --safe      # 安全推送
/remote pull --auto      # 智能拉取
/remote sync             # 同步分支
/remote status           # 查看状态
```

### Workflow 命令
```bash
/workflow init           # 初始化工作流
/workflow start-feature  # 开始功能
/workflow release        # 发布版本
/workflow check-compliance # 检查规范
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

---

**让 Git 操作变得简单而高效！** 🚀