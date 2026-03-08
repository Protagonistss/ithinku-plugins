---
name: branch
description: |
  智能分支管理技能 - 策略、操作自动化和冲突解决。
  当用户说"创建分支"、"新建分支"、"合并分支"、"删除分支"、"清理分支"、"检查冲突"、"解决冲突"、"分支管理"时使用此技能。
  支持多种分支策略(GitFlow/GitHub Flow/Trunk Based)、自动生成分支名、合并分支、预测和解决冲突、分支保护规则检查。
  重要特性：智能命名遵循规范，自动检测合并冲突风险。
disable-model-invocation: false
argument-hint: [create|merge|check-conflicts|cleanup] [args...]
---

# Skill: Branch

智能分支管理技能 - 策略、操作自动化和冲突解决。

## 核心功能

- 🌳 **分支策略** - 支持 GitFlow、GitHub Flow、Trunk Based Development
- 📝 **智能命名** - 自动生成规范的分支名
- 🔄 **操作自动化** - 创建、合并、清理一键完成
- ⚔️ **冲突解决** - 预测冲突风险，提供解决建议
- 🛡️ **分支保护** - 规则验证和合规检查

## 快速使用

```bash
# 创建功能分支
/branch create feature PROJ-123 "添加用户认证"

# 合并分支
/branch merge feature/auth into develop

# 检查冲突
/branch check-conflicts feature/auth develop

# 清理分支
/branch cleanup
```

## 分支策略

### GitFlow 策略
```
main (生产)
  └── develop (开发)
        ├── feature/* (功能)
        ├── release/* (发布)
        └── hotfix/* (热修)
```

**适用场景**：
- 有明确的发布周期
- 需要同时维护多个版本
- 团队规模较大（>10人）

### GitHub Flow 策略
```
main (始终可部署)
  └── feature/* (功能分支，合并后删除)
```

**适用场景**：
- 持续部署
- 单一版本维护
- 小型团队

### Trunk Based Development
```
main (主干)
  └── short-lived-feature/* (短期分支，<1天)
```

**适用场景**：
- 高频发布
- 成熟团队
- 完善的 CI/CD

## 分支命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 功能 | `feature/<ticket>-<desc>` | `feature/PROJ-123-user-auth` |
| 修复 | `fix/<ticket>-<desc>` | `fix/PROJ-456-login-error` |
| 热修 | `hotfix/<version>-<desc>` | `hotfix/v1.2.1-security-patch` |
| 发布 | `release/<version>` | `release/v2.0.0` |
| 实验 | `experiment/<desc>` | `experiment/new-algorithm` |

## 合并冲突处理

### 冲突检测流程
1. 使用 `git merge --no-commit --no-ff` 预检
2. 分析冲突文件和内容
3. 评估冲突复杂度
4. 提供解决建议

### 冲突解决策略
- **优先保留当前分支**：`git checkout --ours <file>`
- **优先保留合并来源**：`git checkout --theirs <file>`
- **手动合并**：编辑冲突标记
- **使用合并工具**：`git mergetool`

## 分支清理

### 清理规则
- 已合并到主分支的功能分支
- 超过 30 天未更新的分支
- 远程已删除的本地追踪分支

### 清理命令
```bash
# 清理已合并的本地分支
git branch --merged main | grep -v "^\*\|main\|develop" | xargs git branch -d

# 清理远程已删除的追踪分支
git fetch --prune

# 批量清理
/branch cleanup --merged --stale=30
```

## 配置

```json
{
  "branch": {
    "strategy": "gitflow",
    "autoNaming": true,
    "protection": true,
    "autoCleanup": true,
    "mainBranches": ["main", "develop"],
    "staleDays": 30
  }
}
```

## 最佳实践

### ✅ 推荐做法
- 保持分支简短（建议 < 3 天完成）
- 频繁从主分支同步更新
- 合并前进行代码审查
- 删除已合并的分支

### ❌ 避免做法
- 长期存在的功能分支
- 直接在主分支上开发
- 跳过代码审查直接合并
- 不清理过期分支

## 详细信息

- 🔗 [分支策略配置](../../references/config/branch-strategies.md)
- 🔗 [Git 工具函数](../../references/utils/git-helpers.md)
- 🔗 [错误处理](../../references/errors/error-types.md)
