---
name: remote
description: |
  远程仓库管理技能 - 智能推送、拉取和多仓库同步。
  当用户说"push"、"pull"、"推送"、"拉取"、"同步仓库"、"git push"、"git pull"、"远程仓库"、"多仓库同步"时使用此技能。
  支持安全推送（带检查）、智能拉取（冲突预防）、多远程仓库同步、分支状态监控。
  重要特性：推送前安全检查，支持多仓库一键同步，防止强制推送事故。
disable-model-invocation: false
argument-hint: [push|pull|sync|push-all] [args...]
---

# Skill: Remote

远程仓库管理技能 - 智能推送、拉取和多仓库同步。

## 核心功能

- 🚀 **智能推送** - 安全检查、分批推送、防强制推送保护
- 📥 **智能拉取** - 冲突预防、自动合并策略选择
- 🔗 **多仓库管理** - 一键同步多个远程仓库
- 🌐 **分支同步** - 自动同步远程分支状态
- 📊 **状态监控** - 实时同步状态和差异报告

## 快速使用

```bash
# 安全推送
/remote push main --safe

# 智能拉取
/remote pull --auto

# 同步所有分支
/remote sync --all

# 多仓库推送
/remote push-all --remotes origin,backup
```

## 推送策略

### 安全推送流程
1. **预检查** - 确认工作区干净
2. **差异分析** - 显示即将推送的提交
3. **冲突检测** - 检查远程是否有新提交
4. **执行推送** - 确认后执行 `git push`
5. **状态确认** - 验证推送成功

### 推送选项
| 选项 | 说明 | 使用场景 |
|------|------|---------|
| `--safe` | 安全部全检查后推送 | 默认推荐 |
| `--force-with-lease` | 安全强制推送 | 确认需要覆盖时 |
| `--no-verify` | 跳过钩子（谨慎） | 紧急修复 |
| `--tags` | 同时推送标签 | 版本发布 |

### 危险操作警告
```bash
# ❌ 危险：可能覆盖他人提交
git push --force

# ✅ 安全：仅在远程无更新时强制
git push --force-with-lease
```

## 拉取策略

### 拉取方式对比
| 命令 | 说明 | 适用场景 |
|------|------|---------|
| `git pull` | 拉取并合并 | 快速同步 |
| `git pull --rebase` | 拉取并变基 | 保持线性历史 |
| `git fetch` | 仅拉取不合并 | 先查看再决定 |

### 智能拉取流程
1. **获取远程更新** - `git fetch origin`
2. **分析差异** - 比较本地与远程
3. **冲突预判** - 检测潜在冲突
4. **选择策略** - merge 或 rebase
5. **执行拉取** - 合并/变基到本地

### 冲突处理
```bash
# 优先使用 rebase 保持历史整洁
git pull --rebase origin main

# 如果有冲突，解决后继续
git add <resolved-files>
git rebase --continue

# 放弃 rebase
git rebase --abort
```

## 多仓库同步

### 配置多远程
```bash
# 添加备用远程
git remote add backup https://github.com/org/backup.git

# 查看所有远程
git remote -v
```

### 同步命令
```bash
# 推送到所有远程
git push --all origin backup

# 同步特定分支
git push origin main && git push backup main

# 使用 sync 命令一键同步
/remote sync --all --remotes origin,backup,upstream
```

## 状态监控

### 检查远程状态
```bash
# 查看远程分支
git branch -r

# 查看本地与远程差异
git log HEAD..origin/main --oneline

# 查看远程提交
git log origin/main --oneline -5
```

## 配置

```json
{
  "remote": {
    "safetyChecks": true,
    "autoSync": false,
    "multiRemote": true,
    "defaultPushStrategy": "safe",
    "remotes": {
      "origin": "https://github.com/org/repo.git",
      "backup": "https://github.com/org/backup.git"
    }
  }
}
```

## 最佳实践

### ✅ 推荐做法
- 推送前先拉取最新代码
- 使用 `--force-with-lease` 替代 `--force`
- 定期同步远程分支状态
- 配置多远程备份

### ❌ 避免做法
- 直接使用 `--force` 强制推送
- 长时间不同步远程更新
- 在 main 分支上强制推送
- 忽略远程冲突警告

## 详细信息

- 🔗 [Git 工具函数](../../references/utils/git-helpers.md)
- 🔗 [错误处理](../../references/errors/error-types.md)
- 🔗 [通用类型定义](../../references/types/common-types.md)
