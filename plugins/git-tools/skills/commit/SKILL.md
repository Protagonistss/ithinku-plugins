---
name: commit
description: |
  智能代码提交技能 - 分析变更并生成规范提交信息。
  当用户说"提交代码"、"commit"、"生成提交信息"、"帮我commit"、"写commit message"、"检查提交质量"时使用此技能。
  支持分析代码变更、自动识别提交类型(feat/fix/docs/refactor等)、生成符合 Conventional Commits 规范的提交信息、执行质量检查。
  重要特性：绝不添加任何 AI 工具标识(如 Co-Authored-By AI)，保持提交历史专业和干净。
disable-model-invocation: false
argument-hint: [analyze|check|create]
---

# Skill: Commit

智能代码提交技能 - 分析变更并生成规范提交信息。

## 核心功能

- 📊 **变更分析** - 识别文件类型、影响范围和修改性质
- 🏷️ **类型检测** - 自动识别 feat/fix/docs/refactor/style/test/chore 等类型
- 📍 **Scope识别** - 自动确定变更所属模块或功能区域
- 📝 **信息生成** - 生成符合 Conventional Commits 规范的提交信息
- ✅ **质量检查** - 检查敏感信息、未完成 TODO、调试代码等
- 🚫 **纯净提交** - 绝不添加 AI 工具标识，保持提交历史专业

## 快速使用

```bash
# 分析并生成提交信息
/commit analyze

# 执行质量检查
/commit check

# 一键提交
/commit create
```

## Conventional Commits 规范

### 提交信息格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型说明
| 类型 | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | feat(auth): 添加用户登录功能 |
| fix | Bug 修复 | fix(api): 修复用户列表分页问题 |
| docs | 文档更新 | docs(readme): 更新安装说明 |
| refactor | 重构代码 | refactor(utils): 优化日期格式化函数 |
| style | 代码格式 | style: 统一缩进为2空格 |
| test | 测试相关 | test(user): 添加用户服务单元测试 |
| chore | 构建/工具 | chore(deps): 升级依赖版本 |
| perf | 性能优化 | perf(list): 优化列表渲染性能 |

### Scope 命名规范
- 按模块：`auth`, `api`, `ui`, `db`
- 按功能：`login`, `search`, `payment`
- 按层级：`components`, `services`, `utils`

## 分析流程

1. **获取变更** - 使用 `git diff --staged` 获取暂存区变更
2. **分类识别** - 分析文件类型和修改性质
3. **类型推断** - 根据变更内容推断提交类型
4. **Scope 确定** - 识别变更影响的模块范围
5. **信息生成** - 组装符合规范的提交信息
6. **质量检查** - 检测潜在问题

## 质量检查项

- [ ] 无敏感信息泄露（密钥、密码、token）
- [ ] 无调试代码残留（console.log、debugger）
- [ ] 无未完成的 TODO 标记
- [ ] 无过大的提交（建议单次提交 < 500 行）
- [ ] 提交信息清晰描述变更内容

## 配置

```json
{
  "commit": {
    "messageFormat": "conventional",
    "qualityChecks": true,
    "autoScope": true,
    "maxSubjectLength": 72,
    "signCommits": false
  }
}
```

## 最佳实践

### ✅ 推荐做法
- 原子提交：每个提交只做一件事
- 频繁提交：小步快跑，便于回滚
- 有意义的描述：说明"为什么"而不仅是"做了什么"
- 使用祈使句："添加功能"而非"添加了功能"

### ❌ 避免做法
- 一个提交包含多个不相关的修改
- 提交信息过于模糊（如"fix bug"、"update"）
- 提交未编译或无法运行的代码
- 在提交信息中添加 AI 工具标识

## 详细信息

- 🔗 [提交类型配置](../../references/config/commit-types.md)
- 🔗 [Git 工具函数](../../references/utils/git-helpers.md)
- 🔗 [错误处理](../../references/errors/error-types.md)