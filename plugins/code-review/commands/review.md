---
name: review
description: 对代码进行全面的专业审查，提供代码质量、安全性和性能优化建议。
skills:
  - code-analysis
  - performance-review
  - security-review
---

# Command: /review

对代码进行全面的专业审查，提供代码质量、安全性和性能优化建议。

## 描述

/review 命令启动一个专业的代码审查流程，使用多个专门的代理来分析代码的不同方面，包括代码质量、安全性、性能和最佳实践。

## 用法

```
/review [target] [options]
```

### 参数

- `target` - 审查目标（文件路径、目录、PR链接、或代码片段）
- `--focus` - 审查重点（security, performance, quality, architecture, all）
- `--depth` - 审查深度（quick, standard, deep）
- `--format` - 输出格式（summary, detailed, report）
- `--language` - 代码语言（自动检测或指定）

## 示例

### 审查当前文件
```
/review
```

### 审查特定文件
```
/review src/components/UserList.jsx
```

### 专注于安全性审查
```
/review --focus security src/api/auth.js
```

### 深度审查整个目录
```
/review src/ --depth deep --format report
```

### 审查代码片段
```
/review `
function getUser(id) {
  return db.query("SELECT * FROM users WHERE id = " + id);
}
`
```

## 审查流程

### 1. 自动分析
- 检测编程语言和框架
- 分析代码结构和复杂度
- 识别潜在的问题区域

### 2. 多维度审查
- 🔒 **安全审查**：SQL注入、XSS、认证授权等
- ⚡ **性能分析**：算法效率、资源使用、缓存策略
- 🏗️ **架构评估**：设计模式、代码结构、可维护性
- 📋 **代码质量**：可读性、规范性、最佳实践

### 3. 问题分级
- 🔴 **严重**：必须立即修复的安全和功能问题
- 🟡 **重要**：影响性能和维护性的问题
- 🟢 **建议**：代码风格和优化建议

### 4. 改进建议
- 提供具体的修复方案
- 展示代码重构示例
- 推荐学习资源和最佳实践

## 审查报告模板

```markdown
# 代码审查报告

## 基本信息
- **文件**: src/components/UserProfile.jsx
- **语言**: React/JavaScript
- **代码行数**: 156
- **审查时间**: 2024-01-15 10:30:00
- **总体评分**: 7.8/10

## 审查摘要
代码整体质量良好，存在2个严重安全问题需要立即修复，3个性能优化机会。

## 详细问题

### 🔴 严重问题 (必须修复)

#### 1. SQL注入漏洞
**位置**: 第45行
**风险等级**: 高
```javascript
// 问题代码
const query = `SELECT * FROM users WHERE id = ${userId}`;

// 修复建议
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

### 🟡 重要问题 (建议修复)

#### 2. 未处理的Promise rejection
**位置**: 第78-82行
**风险等级**: 中

### 🟢 优化建议

#### 3. 可以使用React.memo优化渲染性能
**位置**: 第12-25行

## 改进建议
1. 立即修复SQL注入漏洞
2. 添加错误处理机制
3. 实施性能优化

## 学习资源
- [OWASP安全指南](https://owasp.org/)
- [React性能最佳实践](https://react.dev/learn/render-and-commit)
```

## 配置选项

可以通过项目根目录的 `.codereview.json` 文件自定义审查规则：

```json
{
  "review": {
    "defaultDepth": "standard",
    "autoFix": false,
    "ignorePatterns": ["*.test.js", "node_modules/**"],
    "rules": {
      "security": {
        "enabled": true,
        "severity": "error"
      },
      "performance": {
        "enabled": true,
        "severity": "warn"
      },
      "style": {
        "enabled": true,
        "severity": "info"
      }
    },
    "customRules": [
      {
        "name": "no-console-in-production",
        "pattern": "console\\.",
        "message": "生产环境不应该有console语句"
      }
    ]
  }
}
```

## 集成开发流程

### Git Hooks
```bash
#!/bin/sh
# pre-commit hook
npx claude /review --focus security,quality
```

### CI/CD集成
```yaml
# .github/workflows/code-review.yml
name: Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Code Review
        run: npx claude /review --format report > review-report.md
```

## 最佳实践

1. **定期审查**：每个PR都应该进行代码审查
2. **分层审查**：先关注安全问题，再检查性能和质量
3. **建设性反馈**：提供具体的改进建议，而不是只指出问题
4. **持续学习**：将审查过程中学到的最佳实践应用到未来的代码中

## 相关命令

- `/security` - 专门进行安全审查
- `/performance` - 专门进行性能分析
- `/refactor` - 代码重构建议
- `/fix` - 自动修复简单问题

## 技术支持

如果遇到问题或需要帮助：
- 查看文档：`/help code-review`
- 反馈问题：GitHub Issues
- 获取帮助：`@CodeReviewer`