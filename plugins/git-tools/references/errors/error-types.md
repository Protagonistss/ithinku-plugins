# Git Tools Error Types

统一的错误类型定义和处理机制。

## 错误分类

### Git 操作错误
```javascript
const GitErrors = {
  // 仓库错误
  NOT_GIT_REPOSITORY: {
    code: 'NOT_GIT_REPOSITORY',
    message: '当前目录不是 Git 仓库',
    suggestion: '执行 git init 初始化仓库',
    severity: 'error'
  },
  NO_REMOTE: {
    code: 'NO_REMOTE',
    message: '没有配置远程仓库',
    suggestion: '使用 git remote add 添加远程仓库',
    severity: 'error'
  },
  REMOTE_NOT_FOUND: {
    code: 'REMOTE_NOT_FOUND',
    message: '远程仓库不存在或无法访问',
    suggestion: '检查远程仓库 URL 和网络连接',
    severity: 'error'
  },

  // 分支错误
  BRANCH_NOT_FOUND: {
    code: 'BRANCH_NOT_FOUND',
    message: '分支不存在',
    suggestion: '使用 git branch 查看可用分支',
    severity: 'error'
  },
  BRANCH_ALREADY_EXISTS: {
    code: 'BRANCH_ALREADY_EXISTS',
    message: '分支已存在',
    suggestion: '使用其他分支名称或删除现有分支',
    severity: 'error'
  },
  DETACHED_HEAD: {
    code: 'DETACHED_HEAD',
    message: '处于游离头状态',
    suggestion: '使用 git checkout 切换到分支',
    severity: 'warning'
  },

  // 提交错误
  NOTHING_TO_COMMIT: {
    code: 'NOTHING_TO_COMMIT',
    message: '没有需要提交的更改',
    suggestion: '使用 git add 暂存文件',
    severity: 'warning'
  },
  EMPTY_COMMIT: {
    code: 'EMPTY_COMMIT',
    message: '空的提交',
    suggestion: '添加 --allow-empty 标志或更改文件',
    severity: 'warning'
  },
  LARGE_COMMIT: {
    code: 'LARGE_COMMIT',
    message: '提交过大',
    suggestion: '考虑拆分成多个提交',
    severity: 'warning'
  },

  // 合并错误
  MERGE_CONFLICT: {
    code: 'MERGE_CONFLICT',
    message: '合并冲突',
    suggestion: '解决冲突后继续或中止合并',
    severity: 'error'
  },
  UNMERGED_PATHS: {
    code: 'UNMERGED_PATHS',
    message: '存在未合并的路径',
    suggestion: '解决所有冲突后提交',
    severity: 'error'
  },

  // 推送/拉取错误
  PUSH_REJECTED: {
    code: 'PUSH_REJECTED',
    message: '推送被拒绝',
    suggestion: '先拉取远程更改或使用强制推送',
    severity: 'error'
  },
  PERMISSION_DENIED: {
    code: 'PERMISSION_DENIED',
    message: '权限不足',
    suggestion: '检查认证信息或仓库权限',
    severity: 'error'
  },
  NETWORK_ERROR: {
    code: 'NETWORK_ERROR',
    message: '网络连接错误',
    suggestion: '检查网络连接或代理设置',
    severity: 'error'
  }
};
```

### 配置错误
```javascript
const ConfigErrors = {
  INVALID_CONFIG: {
    code: 'INVALID_CONFIG',
    message: '配置格式错误',
    suggestion: '检查配置文件格式',
    severity: 'error'
  },
  MISSING_CONFIG: {
    code: 'MISSING_CONFIG',
    message: '缺少必需的配置',
    suggestion: '添加必需的配置项',
    severity: 'error'
  },
  CONFIG_CONFLICT: {
    code: 'CONFIG_CONFLICT',
    message: '配置项冲突',
    suggestion: '检查并解决配置冲突',
    severity: 'error'
  }
};
```

### 插件错误
```javascript
const PluginErrors = {
  PLUGIN_NOT_FOUND: {
    code: 'PLUGIN_NOT_FOUND',
    message: '插件未安装',
    suggestion: '使用 claude plugin install 安装插件',
    severity: 'warning'
  },
  PLUGIN_VERSION_MISMATCH: {
    code: 'PLUGIN_VERSION_MISMATCH',
    message: '插件版本不兼容',
    suggestion: '更新插件到兼容版本',
    severity: 'error'
  },
  PLUGIN_DEPENDENCY_MISSING: {
    code: 'PLUGIN_DEPENDENCY_MISSING',
    message: '插件依赖缺失',
    suggestion: '安装缺失的依赖插件',
    severity: 'error'
  }
};
```

## 错误处理工具

### 错误创建器
```javascript
class GitToolError extends Error {
  constructor(errorType, context = {}) {
    super(errorType.message);
    this.name = 'GitToolError';
    this.code = errorType.code;
    this.severity = errorType.severity;
    this.suggestion = errorType.suggestion;
    this.context = context;
    this.timestamp = new Date().toISOString();
  }

  // 转换为用户友好的格式
  toUserFormat() {
    return {
      error: true,
      code: this.code,
      message: this.message,
      suggestion: this.suggestion,
      severity: this.severity,
      context: this.context,
      timestamp: this.timestamp
    };
  }

  // 转换为 JSON
  toJSON() {
    return this.toUserFormat();
  }
}

// 创建错误
function createError(errorCode, context = {}) {
  const allErrors = {
    ...GitErrors,
    ...ConfigErrors,
    ...PluginErrors
  };

  const errorType = allErrors[errorCode];
  if (!errorType) {
    return new GitToolError({
      code: 'UNKNOWN_ERROR',
      message: '未知错误',
      suggestion: '查看日志获取更多信息',
      severity: 'error'
    }, context);
  }

  return new GitToolError(errorType, context);
}
```

### 错误处理器
```javascript
class ErrorHandler {
  constructor(options = {}) {
    this.logger = options.logger || console;
    this.throwOnError = options.throwOnError || false;
    this.exitOnError = options.exitOnError || false;
  }

  // 处理错误
  handle(error, context = {}) {
    // 标准化错误
    const standardError = this.standardizeError(error);

    // 记录错误
    this.logError(standardError, context);

    // 决定是否抛出或退出
    if (this.throwOnError || standardError.severity === 'error') {
      if (this.exitOnError) {
        process.exit(1);
      }
      throw standardError;
    }

    return standardError;
  }

  // 标准化错误对象
  standardizeError(error) {
    if (error instanceof GitToolError) {
      return error;
    }

    // Git 命令错误
    if (error.git) {
      return this.parseGitError(error);
    }

    // Node.js 错误
    if (error instanceof Error) {
      return createError('UNKNOWN_ERROR', {
        originalError: error.message,
        stack: error.stack
      });
    }

    // 字符串错误
    if (typeof error === 'string') {
      return createError('UNKNOWN_ERROR', {
        message: error
      });
    }

    // 其他类型
    return createError('UNKNOWN_ERROR', {
      originalError: error
    });
  }

  // 解析 Git 错误
  parseGitError(error) {
    const message = error.message || error.toString();

    // 常见错误模式
    if (message.includes('not a git repository')) {
      return createError('NOT_GIT_REPOSITORY');
    }

    if (message.includes('fatal: couldn\'t find remote ref')) {
      return createError('BRANCH_NOT_FOUND', { branch: extractBranch(message) });
    }

    if (message.includes('CONFLICT')) {
      return createError('MERGE_CONFLICT', {
        conflicts: extractConflicts(error.stdout)
      });
    }

    if (message.includes('Permission denied')) {
      return createError('PERMISSION_DENIED');
    }

    if (message.includes('network')) {
      return createError('NETWORK_ERROR', {
        details: message
      });
    }

    // 通用 Git 错误
    return createError('UNKNOWN_ERROR', {
      gitError: message
    });
  }

  // 记录错误
  logError(error, context) {
    const logEntry = {
      ...error.toJSON(),
      context
    };

    if (error.severity === 'error') {
      this.logger.error('GitTools Error:', logEntry);
    } else if (error.severity === 'warning') {
      this.logger.warn('GitTools Warning:', logEntry);
    } else {
      this.logger.info('GitTools Info:', logEntry);
    }
  }
}
```

## 错误恢复策略

### 自动恢复
```javascript
const recoveryStrategies = {
  // 处理合并冲突
  MERGE_CONFLICT: {
    autoResolve: false,
    steps: [
      {
        name: 'abort_merge',
        action: 'git merge --abort',
        description: '中止合并'
      },
      {
        name: 'pull_changes',
        action: 'git pull',
        description: '拉取最新更改'
      },
      {
        name: 'retry_merge',
        action: 'git merge',
        description: '重试合并'
      }
    ]
  },

  // 处理推送拒绝
  PUSH_REJECTED: {
    autoResolve: false,
    steps: [
      {
        name: 'stash_changes',
        action: 'git stash',
        description: '暂存本地更改'
      },
      {
        name: 'pull_remote',
        action: 'git pull',
        description: '拉取远程更改'
      },
      {
        name: 'pop_stash',
        action: 'git stash pop',
        description: '恢复暂存的更改'
      },
      {
        name: 'retry_push',
        action: 'git push',
        description: '重试推送'
      }
    ]
  },

  // 处理权限错误
  PERMISSION_DENIED: {
    autoResolve: false,
    steps: [
      {
        name: 'check_auth',
        action: 'checkAuthentication',
        description: '检查认证信息'
      },
      {
        name: 'refresh_token',
        action: 'refreshAuthenticationToken',
        description: '刷新认证令牌'
      },
      {
        name: 'retry_operation',
        action: 'retry',
        description: '重试操作'
      }
    ]
  }
};

// 执行恢复步骤
async function recover(error, options = {}) {
  const strategy = recoveryStrategies[error.code];
  if (!strategy) {
    return { recovered: false, reason: '没有可用的恢复策略' };
  }

  if (strategy.autoResolve === false && options.auto !== true) {
    return {
      recovered: false,
      reason: '需要手动干预',
      steps: strategy.steps
    };
  }

  // 执行恢复步骤
  for (const step of strategy.steps) {
    try {
      await executeStep(step);
    } catch (stepError) {
      return {
        recovered: false,
        reason: `恢复步骤 "${step.name}" 失败: ${stepError.message}`,
        failedStep: step
      };
    }
  }

  return { recovered: true };
}
```

## 使用方式

```javascript
// 初始化错误处理器
const errorHandler = new ErrorHandler({
  throwOnError: false,
  exitOnError: false
});

// 使用示例
async function safeGitOperation() {
  try {
    await git.push('origin', 'main');
  } catch (error) {
    const handled = errorHandler.handle(error, {
      operation: 'push',
      branch: 'main'
    });

    if (handled.code === 'PUSH_REJECTED') {
      const recovery = await recover(handled);
      if (recovery.recovered) {
        console.log('自动恢复成功！');
      }
    }
  }
}

// 创建自定义错误
function validateCommit(commit) {
  if (!commit.message) {
    throw createError('EMPTY_COMMIT', { commit });
  }
  if (commit.stats.total > 1000) {
    throw createError('LARGE_COMMIT', {
      size: commit.stats.total,
      commit: commit.hash
    });
  }
}
```