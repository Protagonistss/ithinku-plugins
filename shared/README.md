# 共享资源

这个目录包含可以跨插件复用的共享资源，包括提示词模板、配置模板等。

## 目录结构

```
shared/
├── prompts/                 # 提示词模板
│   └── code-prompt-templates.md
├── templates/               # 配置模板
│   └── plugin-template.json
└── README.md               # 本文件
```

## prompts/ - 提示词模板

包含各种常用的提示词模板，可以在与 Claude 交互时使用。

### code-prompt-templates.md

代码相关的提示词模板集合，包括：

**代码审查**
- 基础代码审查
- 安全审查
- 性能审查

**代码生成**
- REST API 生成
- 数据模型生成
- 单元测试生成
- UI 组件生成

**重构**
- 函数提取
- 消除代码重复
- 简化条件逻辑

**架构设计**
- 系统架构设计
- 数据库设计
- API 设计

**问题诊断**
- Bug 诊断
- 性能问题诊断

**代码解释**
- 代码理解
- 算法解释

**文档生成**
- API 文档生成
- 代码注释生成

[查看完整模板](prompts/code-prompt-templates.md)

## templates/ - 配置模板

包含各种配置文件的模板。

### plugin-template.json

标准的 Claude Code 插件元数据模板。

**包含字段**：
- `name` - 插件名称
- `version` - 版本号
- `description` - 描述
- `author` - 作者
- `homepage` - 项目主页
- `keywords` - 关键词
- `license` - 许可证
- `dependencies` - 依赖
- `engines` - 引擎要求

**使用方法**：
1. 复制模板文件
2. 修改字段值
3. 保存为 `plugin.json`
4. 放置在插件的 `.claude-plugin/` 目录下

[查看模板文件](templates/plugin-template.json)

## 如何使用共享资源

### 1. 使用提示词模板

从 `prompts/` 目录中选择合适的模板：

```
1. 打开对应的提示词模板文件
2. 复制需要的模板
3. 替换 [占位符] 为实际内容
4. 在 Claude Code 中使用
```

**示例**：

原始模板：
```
请审查以下代码，关注：
1. 代码质量和可读性
2. 潜在的 Bug
3. 性能问题
4. 安全漏洞

代码：
[粘贴代码]
```

使用时：
```
请审查以下代码，关注：
1. 代码质量和可读性
2. 潜在的 Bug
3. 性能问题
4. 安全漏洞

代码：
function getUserData(userId) {
  const query = `SELECT * FROM users WHERE id = ${userId}`;
  return db.query(query);
}
```

### 2. 使用配置模板

从 `templates/` 目录中选择需要的配置模板：

```
1. 复制模板文件
2. 根据需要修改内容
3. 重命名（去掉 -template 后缀）
4. 放置在正确的位置
```

### 3. 自定义模板

你可以基于现有模板创建自己的版本：

**步骤**：
1. 复制现有模板
2. 添加项目特定的内容
3. 调整格式和细节
4. 保存为新文件
5. 在项目中使用

## 添加新的共享资源

欢迎添加新的共享资源！

### 添加提示词模板

1. 在 `prompts/` 目录下创建或编辑 Markdown 文件
2. 使用清晰的标题组织模板
3. 提供使用说明和示例
4. 更新本 README

### 添加配置模板

1. 在 `templates/` 目录下创建配置文件
2. 添加必要的注释说明
3. 提供默认值和示例
4. 更新本 README

## 最佳实践

### 1. 模板命名

- 使用描述性的文件名
- 多个单词用连字符分隔
- 添加 `-template` 后缀（对于配置文件）

**好的命名**：
- `code-prompt-templates.md`
- `plugin-template.json`
- `workflow-template.yml`

**不好的命名**：
- `template1.md`
- `config.json`
- `file.txt`

### 2. 文档完整性

每个模板都应该包含：
- 清晰的描述
- 使用说明
- 示例
- 注意事项

### 3. 保持简单

- 模板应该是起点，不是终点
- 提供足够的灵活性
- 避免过度复杂
- 易于理解和使用

### 4. 及时更新

- 根据使用反馈改进模板
- 添加新的常用模板
- 移除过时的内容
- 保持与最新实践一致

## 贡献指南

### 提交新模板

1. 确保模板有实用价值
2. 提供完整的文档
3. 包含使用示例
4. 测试模板可用性

### 改进现有模板

1. 基于实际使用经验
2. 保持向后兼容
3. 说明改进原因
4. 提供迁移指南（如果需要）

## 相关资源

- [插件开发指南](../plugins/README.md)
- [Code Review Plugin](../plugins/code-review/README.md)
- [Git Tools Plugin](../plugins/git-tools/README.md)

## 反馈

如果你有任何建议或发现问题，欢迎：
- 提出改进建议
- 分享使用经验
- 贡献新模板
- 报告问题

---

**让我们一起构建更好的开发工具！🚀**

