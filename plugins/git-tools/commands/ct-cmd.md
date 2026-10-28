---
name: ct
description: 用户明确要求提交时，按仓库现有格式写出提交说明并提交。只分析时不要提交。
---

# /ct

用户明确要求提交时才执行。只要求分析或写说明时，不要暂存，不要提交，不要推送。

## 步骤

1. 查看 `git status`、`git diff`、`git diff --staged`、`git log -8 --oneline`。
2. 说明跟这个仓库最近的提交格式，写这次改动的原因。
3. 不提交 `.env`、密钥和凭据。发现就停下来。
4. 只暂存这次相关的文件。不要 `git add -A`，除非用户明确说全部暂存，且其中没有密钥。
5. 不要添加 `Co-Authored-By`、Generated with 或模型名称。
6. 不要使用 `--no-verify`。钩子失败就修问题，再做一次新的提交。
7. 用户没要求推送就不要 `git push`。

## 不要做

- `--auto` 直接提交
- 为了通过检查去跳过钩子
- 推送失败时 `git pull --rebase origin main`
- amend 已经推送的提交。amend 只在用户明确要求、提交是这次对话创建的、并且尚未推送时使用
