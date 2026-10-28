---
name: remote
description: >-
  用户明确要求 push、pull、fetch 或查看远程差异时使用。
  不强制推送，不跳过钩子，不把当前分支变基到 main。
---

# Remote

先看 `git status` 和 `git branch -vv`，确认当前分支和它的上游。

## 推送

只有用户明确要求推送时才 `git push`。推送到当前分支的上游。用户没指定目标时，不要推到 `main` 或 `master`。

不要使用 `--force`、`--force-with-lease` 或 `--no-verify`。用户明确要求强制推送时，先说明远程哪些提交会被覆盖，并拒绝强制推送 `main` 和 `master`。

推送被拒绝时，先 `git fetch`，用 `git log HEAD..@{upstream}` 和 `git log @{upstream}..HEAD` 说明两边差了什么。不要自动 `git pull --rebase`，也不要变基到 `main`。

## 拉取

用户要求更新当前分支时，先 `git fetch`。上游有新提交且本地有未推送的提交时，说明差异。用户没选择合并或变基时，不要变基。

工作区有未提交改动时先告诉用户。不要 `git reset --hard`。不要为了继续操作而 `git stash`，除非用户要求暂存。

## 多远程

只推送用户点名的远程。`git push --all` 后面只能有一个远程名。不要一次推到所有远程。
