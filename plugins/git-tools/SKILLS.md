# Git-Tools 技能系统

Git-Tools 插件采用模块化的技能系统设计，将复杂的 Git 操作拆分为独立的专业技能，提供灵活、可扩展的 Git 管理能力。

## 系统架构

```
git-tools/
├── skills/             # 技能实现
│   ├── commit/        # 提交技能
│   ├── branch/        # 分支技能
│   ├── history/       # 历史技能
│   ├── remote/        # 远程技能
│   └── workflow/      # 工作流技能
├── references/         # 通用组件
│   ├── utils/         # 工具函数
│   ├── config/        # 配置模板
│   ├── errors/        # 错误处理
│   ├── types/         # 类型定义
│   └── integrations/  # 插件集成
├── agents/            # 智能代理
└── commands/          # 命令定义
```

### References 系统

为了避免代码重复和提高可维护性，我们建立了 references 系统：

- **[utils/git-helpers.md](./references/utils/git-helpers.md)** - Git 操作通用函数
- **[config/commit-types.md](./references/config/commit-types.md)** - 提交类型和检测规则
- **[config/branch-strategies.md](./references/config/branch-strategies.md)** - 分支策略模板
- **[errors/error-types.md](./references/errors/error-types.md)** - 统一错误处理
- **[types/common-types.md](./references/types/common-types.md)** - TypeScript 类型定义

## 技能概览

### 1. [Commit](./skills/commit/SKILL.md)
**智能代码提交管理**

#### 核心功能
- 智能提交信息生成（Conventional Commits）
- 提交质量检查（敏感信息、TODO 标记、测试文件）
- 批量提交管理和分组
- 自动分支命名策略
- 推送安全检查

#### 使用场景
```javascript
// 生成提交信息
skill: commit
action: generateMessage
params: { changes: fileChanges }

// 执行质量检查
skill: commit
action: qualityCheck
params: { severity: 'warning' }
```

### 2. [Branch](./skills/branch/SKILL.md)
**分支策略与管理**

#### 核心功能
- 多种分支策略支持（GitFlow、GitHub Flow）
- 智能分支命名和创建
- 冲突预测与自动解决
- 分支保护规则执行
- 分支清理与维护

#### 使用场景
```javascript
// 创建功能分支
skill: branch
action: createFeatureBranch
params: {
  ticket: "PROJ-123",
  description: "添加用户认证",
  strategy: "gitflow"
}

// 合并分支
skill: branch
action: mergeWithConflictResolution
params: {
  source: "feature/auth",
  target: "develop"
}
```

### 3. [History](./skills/history/SKILL.md)
**历史管理与优化**

#### 核心功能
- 历史质量分析与评分
- 安全的交互式 rebase
- 智能提交搜索与过滤
- 历史异常检测
- 历史快照与恢复

#### 使用场景
```javascript
// 分析历史质量
skill: history
action: analyzeQuality
params: {
  branch: "main",
  depth: 100
}

// 执行 rebase
skill: history
action: interactiveRebase
params: {
  base: "HEAD~10",
  autoSquash: true
}
```

### 4. [Remote](./skills/remote/SKILL.md)
**远程仓库管理**

#### 核心功能
- 智能推送策略和安全检查
- 多远程仓库管理
- 增量获取优化
- 远程分支同步
- 实时同步状态监控

#### 使用场景
```javascript
// 安全推送
skill: remote
action: safePush
params: {
  branch: "main",
  safetyChecks: true
}

// 多仓库推送
skill: remote
action: multiRemotePush
params: {
  remotes: ["origin", "github", "gitlab"],
  stopOnError: false
}
```

### 5. [Workflow](./skills/workflow/SKILL.md)
**团队协作与工作流**

#### 核心功能
- 工作流模板（GitFlow、GitHub Flow）
- 自定义工作流构建器
- 代码审查自动分配
- 发布管理自动化
- 团队规范执行

#### 使用场景
```javascript
// 初始化工作流
skill: workflow
action: initialize
params: {
  template: "gitflow",
  team: { reviewers: ["alice", "bob"] }
}

// 发布版本
skill: workflow
action: release
params: {
  versionStrategy: "conventional",
  autoMerge: true
}
```

## 技能协作机制

### 技能间调用
技能可以相互调用，形成复杂的工作流：

```javascript
// 完整的功能提交流程
async function featureComplete() {
  // 1. 代码审查（如果有 code-review 插件）
  if (hasPlugin('code-review')) {
    await skill('code-review', { mode: 'full' });
  }

  // 2. 质量检查（commit 技能）
  await skill('commit', { action: 'qualityCheck' });

  // 3. 生成提交信息（commit 技能）
  const message = await skill('commit', {
    action: 'generateMessage',
    type: 'feat'
  });

  // 4. 创建提交（commit 技能）
  await git.commit(message);

  // 5. 推送安全检查（remote 技能）
  await skill('remote', {
    action: 'checkPushSafety',
    branch: 'current'
  });

  // 6. 推送到远程（remote 技能）
  await skill('remote', {
    action: 'safePush',
    branch: 'current'
  });

  // 7. 创建 PR（workflow 技能）
  await skill('workflow', {
    action: 'createPullRequest',
    autoAssign: true
  });
}
```

### 插件集成检测
技能可以检测其他插件的存在，提供增强功能：

```javascript
// 在 commit 技能中
const integrations = {
  codeReview: checkPluginExists('code-review'),
  unitTest: checkPluginExists('unit-test-generator'),
  cicd: checkPluginExists('ci-cd')
};

if (integrations.codeReview) {
  await runCodeReview();
}
```

## 配置系统

### 全局配置
```json
{
  "git-tools": {
    "defaultWorkflow": "gitflow",
    "autoSafetyCheck": true,
    "enableIntegrations": true,
    "logLevel": "info"
  }
}
```

### 技能特定配置
每个技能都有独立的配置选项，可以单独配置：

```json
{
  "commit": {
    "messageFormat": "conventional",
    "qualityChecks": true,
    "autoPush": false
  },
  "branch": {
    "namingStrategy": "ticket-description",
    "protectionRules": true
  }
}
```

## 扩展性

### 添加新技能
1. 在 `skills/` 目录创建新文件夹
2. 创建 `SKILL.md` 文件
3. 更新 `plugin.json` 的 skills 数组

### 自定义技能集成
```javascript
// 自定义技能示例
const customSkill = {
  name: 'custom-merge',
  dependencies: ['branch', 'history'],
  execute: async (params) => {
    // 使用其他技能
    const conflicts = await skill('branch', {
      action: 'predictConflicts',
      ...params
    });

    if (conflicts.hasConflicts) {
      return await skill('history', {
        action: 'resolveConflicts',
        conflicts: conflicts.conflicts
      });
    }

    return await skill('branch', {
      action: 'merge',
      ...params
    });
  }
};
```

## 最佳实践

1. **技能组合使用**：根据需要组合不同技能的功能
2. **配置优化**：根据团队习惯调整各技能配置
3. **集成利用**：充分利用与其他插件的集成功能
4. **安全第一**：始终启用安全检查，特别是推送操作
5. **渐进采用**：从基础功能开始，逐步使用高级特性

## 故障排除

### 常见问题
- **技能未找到**：检查 plugin.json 中的 skills 配置
- **权限错误**：确保有足够的 Git 权限
- **网络问题**：检查远程仓库连接
- **冲突解决失败**：手动解决复杂冲突

### 调试模式
```javascript
// 启用详细日志
const DEBUG = true;

skill('commit', {
  action: 'generateMessage',
  debug: DEBUG
});
```

通过这种模块化的技能系统，Git-Tools 插件能够提供灵活、专业且可扩展的 Git 管理能力，满足从个人开发者到大型团队的各种需求。