# Git-Tools References

这个目录包含了 Git-Tools 插件的通用组件、配置和工具函数，用于减少技能文件中的重复代码，提高可维护性。

## 目录结构

```
references/
├── utils/              # 通用工具函数
│   └── git-helpers.md  # Git 操作辅助函数
├── config/             # 配置模板
│   ├── commit-types.md # 提交类型配置
│   └── branch-strategies.md # 分支策略配置
├── errors/             # 错误处理
│   └── error-types.md  # 错误类型定义
├── types/              # 类型定义
│   └── common-types.md # 通用类型
└── integrations/       # 插件集成
    └── plugin-integration.md # 插件集成接口（待实现）
```

## 如何使用

### 在技能中引用

```javascript
// 引用工具函数
const { getCommits, analyzeFileChange } = require('../references/utils/git-helpers');

// 引用配置
const { standardTypes, detectCommitType } = require('../references/config/commit-types');

// 引用错误处理
const { createError, ErrorHandler } = require('../references/errors/error-types');

// 使用
async function analyzeCommit() {
  try {
    const commits = await getCommits();
    // ...
  } catch (error) {
    const handled = errorHandler.handle(error);
    return handled;
  }
}
```

### 在 Markdown 中引用

在技能文档中使用 Markdown 链接来引用：

```markdown
参考：[Git Helper Functions](../utils/git-helpers.md)

使用标准提交类型：[Commit Types](../config/commit-types.md)
```

## 贡献指南

### 添加新的工具函数

1. 在相应的 `utils/` 文件中添加函数
2. 提供清晰的文档和示例
3. 确保函数是通用的，可被多个技能使用
4. 添加错误处理

### 添加新的配置

1. 在 `config/` 目录创建新文件或扩展现有文件
2. 提供默认值和示例
3. 说明配置项的作用和影响

### 添加新的错误类型

1. 在 `errors/error-types.md` 中定义新错误
2. 提供错误代码、消息和建议
3. 添加恢复策略（如果适用）

## 最佳实践

1. **保持通用性** - 只添加被多个技能使用的功能
2. **文档完整** - 每个函数和配置都要有清晰的文档
3. **错误处理** - 统一使用定义的错误类型
4. **类型安全** - 使用 TypeScript 类型定义确保类型安全
5. **版本兼容** - 注意保持向后兼容

## 维护说明

- 定期检查是否有重复代码可以抽取
- 更新文档保持最新
- 测试通用函数的正确性
- 优化性能和内存使用