---
name: history
description: |
  Git 历史管理技能 - 重写、优化和分析历史。
  当用户说"分析提交历史"、"git rebase"、"交互式rebase"、"搜索提交"、"历史快照"、"修改历史"、"压缩提交"、"编辑提交信息"时使用此技能。
  支持提交质量分析、安全的 interactive rebase、多维度提交搜索、历史快照管理、异常提交检测。
  重要特性：rebase 前自动备份，支持撤销操作。
disable-model-invocation: false
argument-hint: [analyze|rebase|search|snapshot] [args...]
---

# Skill: History

Git 历史管理技能 - 重写、优化和分析历史。

## 核心功能

- 📊 **历史分析** - 提交质量评分和问题检测
- ✏️ **历史重写** - 安全的 interactive rebase
- 🔍 **智能搜索** - 多维度提交搜索
- 📸 **历史快照** - 创建和恢复历史状态
- ⚠️ **异常检测** - 识别历史问题模式

## 快速使用

```bash
# 分析历史质量
/history analyze --depth 100

# Interactive rebase
/history rebase HEAD~10

# 搜索提交
/history search --author "john"

# 创建快照
/history snapshot pre-release
```

## 历史分析

### 提交质量指标
| 指标 | 说明 | 健康标准 |
|------|------|---------|
| 提交频率 | 每日提交次数 | 稳定，无长期中断 |
| 提交粒度 | 每次提交的变更量 | 适中（<500行/次） |
| 信息质量 | 提交信息规范性 | 遵循 Conventional Commits |
| 原子性 | 提交的独立性 | 每个提交独立完整 |

### 常见问题检测
- 🚫 大体积提交（>1000行变更）
- 🚫 无意义提交信息（如"fix"、"update"）
- 🚫 敏感信息泄露
- 🚫 提交信息格式不规范
- 🚫 合并提交过多

## Interactive Rebase

### 安全操作流程
1. **创建备份** - 自动创建临时分支
2. **启动 rebase** - `git rebase -i <base>`
3. **编辑操作** - 选择 squash/reword/edit/drop
4. **处理冲突** - 逐个解决冲突
5. **完成重写** - 确认无问题后删除备份

### Rebase 操作说明
| 命令 | 说明 | 使用场景 |
|------|------|---------|
| pick | 保留提交 | 默认操作 |
| reword | 修改提交信息 | 修正拼写错误 |
| squash | 合并到前一提交 | 压缩多个小提交 |
| fixup | 合并但丢弃信息 | 自动化压缩 |
| drop | 删除提交 | 移除无用提交 |
| edit | 暂停修改 | 分割提交 |

### 常用 Rebase 场景

```bash
# 压缩最近 3 个提交
git rebase -i HEAD~3
# 将后两个改为 squash

# 修改历史提交信息
git rebase -i HEAD~5
# 将目标提交改为 reword

# 分割提交
git rebase -i HEAD~3
# 将目标提交改为 edit
# 然后 git reset HEAD~ && git add -p 分次提交
```

## 提交搜索

### 搜索维度
```bash
# 按作者搜索
git log --author="john"

# 按日期范围
git log --since="2024-01-01" --until="2024-01-31"

# 按提交信息
git log --grep="fix"

# 按文件变更
git log --follow -- path/to/file

# 按内容搜索
git log -S "function_name"
```

### 高级搜索
```bash
# 查找引入特定代码的提交
git log -p -S "deprecated_code" --all

# 查找空提交信息的提交
git log --oneline --no-merges | grep -E '^[a-f0-9]+ $'

# 查找大体积提交
git log --no-merges --format="%H %s" --stat | \
  awk '/files? changed/ { if ($4 > 500) print }'
```

## 历史快照

### 创建快照
```bash
# 创建命名快照
git tag snapshot-pre-release-2024-01-15

# 创建分支快照
git branch backup/pre-refactor HEAD

# 使用 stash 保存工作区
git stash push -m "WIP: feature-in-progress"
```

### 恢复快照
```bash
# 恢复到标签
git reset --hard snapshot-pre-release-2024-01-15

# 恢复到分支
git reset --hard backup/pre-refactor

# 恢复 stash
git stash pop
```

## 配置

```json
{
  "history": {
    "autoAnalysis": true,
    "rebaseSafety": true,
    "snapshotRetention": 30,
    "autoBackup": true
  }
}
```

## 安全警告

### ⚠️ 危险操作
以下操作会重写历史，已推送到远程的提交需要谨慎操作：
- `git rebase -i` 交互式变基
- `git commit --amend` 修改最后提交
- `git filter-branch` 历史重写
- `git reset --hard` 硬重置

### 🔒 安全措施
- 操作前自动创建备份
- 记录操作日志
- 提供 `--dry-run` 预览模式
- 支持一键撤销

## 详细信息

- 🔗 [Git 工具函数](../../references/utils/git-helpers.md)
- 🔗 [错误处理](../../references/errors/error-types.md)
- 🔗 [通用类型定义](../../references/types/common-types.md)
