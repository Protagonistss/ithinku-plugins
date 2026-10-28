---
name: history
description: >-
  用户要求查看提交历史、搜索某次改动或说明某段历史时使用。
  不交互式变基，不硬重置，不重写已经推送的提交。
---

# History

查看历史用 `git log`、`git show`、`git log -S`、`git log --follow`。按用户给的范围查，不要默认重写。

## 不要执行

- `git rebase -i`。不要改用脚本去 squash 或 drop 已有提交
- `git reset --hard`
- `git filter-branch` 或 `git filter-repo`
- 对已经推送的提交做 rebase、amend 或 reset

用户要整理尚未推送、且由当前对话产生的提交时，先说明会改哪些提交，等用户明确同意后再处理。已经在远程的提交保持原样。

## 留恢复点

需要留恢复点时新建分支，例如 `backup/<说明>`。不要用 `reset --hard` 回到标签。要查看旧提交时，新建分支指向它，让当前分支上的提交还在。
