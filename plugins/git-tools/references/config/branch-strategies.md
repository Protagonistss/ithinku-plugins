# Branch Strategies Configuration

标准分支策略配置模板。

## GitFlow

### 分支定义
```javascript
const gitFlowConfig = {
  name: 'GitFlow',
  description: '经典的 Git 分支管理模型',
  branches: {
    master: {
      type: 'production',
      purpose: '生产环境代码',
      protection: {
        requireReview: true,
        requireCI: true,
        forbidForcePush: true,
        requireLinearHistory: true,
        enforceAdmins: true
      },
      mergeStrategy: 'merge-commit',
      autoMerge: false
    },
    develop: {
      type: 'integration',
      purpose: '开发集成分支',
      protection: {
        requireReview: false,
        requireCI: true,
        forbidForcePush: false,
        enforceAdmins: false
      },
      mergeStrategy: 'merge-commit',
      autoMerge: true
    },
    feature: {
      type: 'development',
      pattern: 'feature/*',
      purpose: '新功能开发',
      source: 'develop',
      target: 'develop',
      protection: {
        requireReview: false,
        requireCI: false,
        forbidForcePush: false
      },
      mergeStrategy: 'rebase-merge',
      autoDelete: true,
      lifecycle: 'temporary'
    },
    release: {
      type: 'preparation',
      pattern: 'release/*',
      purpose: '发布准备',
      source: 'develop',
      target: ['master', 'develop'],
      protection: {
        requireReview: true,
        requireCI: true,
        forbidForcePush: true
      },
      mergeStrategy: 'merge-commit',
      autoDelete: true,
      lifecycle: 'temporary'
    },
    hotfix: {
      type: 'emergency',
      pattern: 'hotfix/*',
      purpose: '紧急修复',
      source: 'master',
      target: ['master', 'develop'],
      protection: {
        requireReview: true,
        requireCI: true,
        forbidForcePush: true
      },
      mergeStrategy: 'merge-commit',
      autoDelete: true,
      lifecycle: 'temporary'
    }
  }
};
```

### 工作流程
```javascript
const gitFlowWorkflow = [
  {
    name: 'Start Feature',
    trigger: 'feature_request',
    actions: [
      {
        type: 'create_branch',
        config: {
          name: 'feature/{ticket}-{description}',
          from: 'develop'
        }
      },
      {
        type: 'assign_issue',
        config: {
          status: 'In Progress'
        }
      }
    ]
  },
  {
    name: 'Complete Feature',
    trigger: 'feature_ready',
    actions: [
      {
        type: 'run_tests',
        config: {
          suite: 'full'
        }
      },
      {
        type: 'code_review',
        config: {
          reviewers: 2,
          auto_assign: true
        }
      },
      {
        type: 'merge',
        config: {
          to: 'develop',
          strategy: 'rebase'
        }
      },
      {
        type: 'delete_branch',
        config: {
          branch: 'current'
        }
      }
    ]
  },
  {
    name: 'Start Release',
    trigger: 'release_needed',
    actions: [
      {
        type: 'create_branch',
        config: {
          name: 'release/v{version}',
          from: 'develop'
        }
      },
      {
        type: 'update_version',
        config: {
          file: 'package.json',
          type: 'minor'
        }
      }
    ]
  }
];
```

## GitHub Flow

### 分支定义
```javascript
const gitHubFlowConfig = {
  name: 'GitHub Flow',
  description: '简化的持续部署模型',
  branches: {
    main: {
      type: 'production',
      purpose: '生产环境代码',
      protection: {
        requireReview: true,
        requireCI: true,
        requireUpToDate: true,
        forbidForcePush: true,
        enforceAdmins: true
      },
      mergeStrategy: 'merge-commit',
      autoMerge: false,
      autoDeploy: true
    },
    feature: {
      type: 'development',
      pattern: '*',
      purpose: '功能开发',
      source: 'main',
      target: 'main',
      protection: {
        requireReview: true,
        requireCI: true,
        requireUpToDate: true
      },
      mergeStrategy: 'squash-merge',
      autoDelete: true,
      lifecycle: 'temporary'
    }
  }
};
```

### 工作流程
```javascript
const gitHubFlowWorkflow = [
  {
    name: 'Create Pull Request',
    trigger: 'branch_pushed',
    condition: 'branch != main',
    actions: [
      {
        type: 'create_pr',
        config: {
          draft: true,
          auto_assign: true
        }
      },
      {
        type: 'run_checks',
        config: {
          tests: true,
          lint: true,
          build: true
        }
      }
    ]
  },
  {
    name: 'Ready for Review',
    trigger: 'pr_ready',
    actions: [
      {
        type: 'mark_ready',
        config: {}
      },
      {
        type: 'request_reviews',
        config: {
          count: 2
        }
      }
    ]
  },
  {
    name: 'Merge and Deploy',
    trigger: 'pr_approved',
    actions: [
      {
        type: 'merge',
        config: {
          method: 'squash'
        }
      },
      {
        type: 'deploy',
        config: {
          environment: 'production'
        }
      }
    ]
  }
];
```

## GitLab Flow

### 分支定义
```javascript
const gitLabFlowConfig = {
  name: 'GitLab Flow',
  description: '环境分支模型',
  branches: {
    master: {
      type: 'production',
      purpose: '生产环境代码',
      protection: {
        requireReview: true,
        requireCI: true,
        forbidForcePush: true
      },
      mergeStrategy: 'merge-commit',
      autoMerge: false
    },
    develop: {
      type: 'development',
      purpose: '开发环境代码',
      protection: {
        requireReview: false,
        requireCI: true
      },
      mergeStrategy: 'merge-commit',
      autoMerge: true
    },
    staging: {
      type: 'environment',
      purpose: '预发布环境',
      protection: {
        requireReview: true,
        requireCI: true
      },
      mergeStrategy: 'merge-commit',
      autoMerge: false
    },
    feature: {
      type: 'development',
      pattern: 'feature/*',
      purpose: '功能开发',
      source: 'develop',
      target: 'develop',
      protection: {
        requireReview: false,
        requireCI: true
      },
      mergeStrategy: 'merge-commit',
      autoDelete: true
    }
  }
};
```

## 自定义策略示例

### 微服务策略
```javascript
const microserviceConfig = {
  name: 'Microservice',
  description: '微服务架构分支策略',
  branches: {
    main: {
      type: 'production',
      purpose: '生产环境',
      protection: {
        requireReview: true,
        requireCI: true,
        requireSecurityScan: true
      }
    },
    develop: {
      type: 'development',
      purpose: '开发集成分支',
      protection: {
        requireCI: true
      }
    },
    service: {
      type: 'feature',
      pattern: 'service/*',
      purpose: '服务功能开发',
      source: 'develop',
      target: 'develop'
    },
    api: {
      type: 'feature',
      pattern: 'api/*',
      purpose: 'API 变更',
      source: 'develop',
      target: 'develop',
      protection: {
        requireBreakingChangeDoc: true
      }
    }
  }
};
```

### 移动应用策略
```javascript
const mobileAppConfig = {
  name: 'Mobile App',
  description: '移动应用开发策略',
  branches: {
    main: {
      type: 'production',
      purpose: '生产环境'
    },
    release: {
      type: 'release',
      pattern: 'release/*',
      purpose: '版本发布准备',
      protection: {
        requireCodeSigning: true,
        requireAppStoreCheck: true
      }
    },
    feature: {
      type: 'feature',
      pattern: 'feature/*',
      purpose: '功能开发'
    },
    hotfix: {
      type: 'hotfix',
      pattern: 'hotfix/*',
      purpose: '热修复'
    }
  }
};
```

## 分支命名规则

### 通用命名规则
```javascript
const namingRules = {
  feature: {
    template: 'feature/{scope}-{description}',
    maxLength: 50,
    separator: '-',
    allowedChars: 'a-z0-9-',
    requireTicket: true,
    examples: [
      'feature/auth-add-login',
      'feature/ui-user-profile',
      'feature/api-payment-gateway'
    ]
  },
  bugfix: {
    template: 'bugfix/{ticket}-{description}',
    maxLength: 45,
    separator: '-',
    allowedChars: 'a-z0-9-',
    requireTicket: true,
    examples: [
      'bugfix-PROJ-123-login-validation',
      'bugfix-PROJ-456-memory-leak'
    ]
  },
  hotfix: {
    template: 'hotfix/{version}-{description}',
    maxLength: 40,
    separator: '-',
    allowedChars: 'a-z0-9-',
    examples: [
      'hotfix-v1.2.1-security-patch',
      'hotfix-v1.3.0-crash-fix'
    ]
  },
  release: {
    template: 'release/v{major}.{minor}',
    maxLength: 20,
    separator: '.',
    allowedChars: 'v0-9.',
    examples: [
      'release/v1.2.0',
      'release/v2.0.0'
    ]
  },
  refactor: {
    template: 'refactor/{component}-{description}',
    maxLength: 50,
    separator: '-',
    allowedChars: 'a-z0-9-',
    examples: [
      'refactor-auth-service-performance',
      'refactor-ui-component-library'
    ]
  }
};
```

### 验证规则
```javascript
const validationRules = {
  // 检查分支名称是否符合规则
  validateBranchName: (name, type) => {
    const rule = namingRules[type];
    if (!rule) return { valid: false, reason: '未知的分支类型' };

    // 检查长度
    if (name.length > rule.maxLength) {
      return { valid: false, reason: `分支名过长，最多 ${rule.maxLength} 字符` };
    }

    // 检查字符
    const pattern = new RegExp(`^[${rule.allowedChars}]+$`);
    if (!pattern.test(name)) {
      return { valid: false, reason: '包含非法字符' };
    }

    // 检查必需的字段
    if (rule.requireTicket && !extractTicket(name)) {
      return { valid: false, reason: '缺少任务编号' };
    }

    return { valid: true };
  },

  // 提取任务编号
  extractTicket: (branchName) => {
    const match = branchName.match(/[A-Z]+-\d+/);
    return match ? match[0] : null;
  }
};
```

## 使用方式

```javascript
// 获取分支策略配置
function getBranchStrategy(name) {
  const strategies = {
    gitflow: gitFlowConfig,
    github: gitHubFlowConfig,
    gitlab: gitLabFlowConfig,
    microservice: microserviceConfig,
    mobile: mobileAppConfig
  };

  return strategies[name] || gitFlowConfig;
}

// 生成分支名称
function generateBranchName(type, params) {
  const rule = namingRules[type];
  if (!rule) throw new Error(`未知的分支类型: ${type}`);

  let name = rule.template;

  // 替换占位符
  Object.keys(params).forEach(key => {
    const value = sanitizeValue(params[key]);
    name = name.replace(new RegExp(`{${key}}`, 'g'), value);
  });

  // 验证生成的名称
  const validation = validationRules.validateBranchName(name, type);
  if (!validation.valid) {
    throw new Error(`生成的分支名无效: ${validation.reason}`);
  }

  return name;
}

// 清理值
function sanitizeValue(value) {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
}
```