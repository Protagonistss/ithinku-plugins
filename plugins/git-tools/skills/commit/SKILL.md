---
name: commit
description: >-
  用户明确要求提交代码、生成提交信息或检查这次提交时使用。
  用户说「提交」「commit」「写 commit message」时使用。
  只分析变更时不要提交。不要添加 Co-Authored-By 或 AI 标识。
---

# Commit

只有用户明确要求提交时才执行 `git commit`。用户只要求看变更或写说明时，给出说明，不要暂存，也不要提交。

## 提交前

同时查看：

- `git status`
- `git diff` 与 `git diff --staged`
- `git log -8 --oneline`，说明跟这个仓库最近的格式

不要提交 `.env`、密钥和凭据。发现这类文件就停下来告诉用户。

`console.log`、TODO、单次变更行数多，只在说明里提一句。用户已经要求提交时，这些不阻止提交。

不要用 `--no-verify` 跳过钩子。钩子失败就修问题，再做一次新的提交。

## 说明

用仓库最近提交的语言和格式。说明写这次改动的原因。

不要添加 `Co-Authored-By`、Generated with、模型名称或其他 AI 标识。

## 暂存

只加入这次要提交的文件。不要 `git add -A` 或 `git add .`，除非用户明确说全部暂存，并且状态里没有密钥和不相关的文件。

## 修改上一次提交

同时满足才使用 `--amend`：

- 用户明确要求 amend
- 这次提交是当前对话里创建的
- `git status` 显示还没有推送到远程

否则新建一次提交。不要 amend 已经推送的提交。

## 推送

用户没有明确要求推送时，提交后不要 `git push`。
