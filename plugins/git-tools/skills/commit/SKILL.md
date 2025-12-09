# Skill: Commit

这个技能实现了智能化的 Git 提交功能，能够分析代码变更、生成符合规范的提交信息，并管理整个提交流程。

## 核心能力

### 1. 变更分析 (Change Analysis)

**功能描述**：
- 解析 `git status` 输出，识别已暂存、未暂存和未跟踪的文件
- 分析 `git diff --staged` 的具体变更内容
- 识别变更的文件类型和影响范围
- 统计变更数量和复杂度

**实现逻辑**：
```javascript
// 分析文件变更类型
function analyzeFileChanges(filePath, status) {
  const changeType = status[0]; // A=新增, M=修改, D=删除, R=重命名
  const extension = path.extname(filePath);

  return {
    type: changeType,
    path: filePath,
    extension: extension,
    scope: detectScope(filePath),
    category: categorizeFile(filePath)
  };
}
```

### 2. 提交类型检测 (Commit Type Detection)

**类型映射规则**：
```javascript
const commitTypeRules = {
  feat: {
    patterns: [
      /new|create|add|implement/i,
      /class|function|component|module/i
    ],
    fileTypes: ['.jsx', '.tsx', '.js', '.ts', '.py', '.java'],
    score: 10
  },
  fix: {
    patterns: [
      /fix|bug|error|issue|patch/i,
      /crash|exception|fail|problem/i
    ],
    fileTypes: ['.js', '.ts', '.py', '.java'],
    score: 10
  },
  refactor: {
    patterns: [
      /refactor|improve|optimize|enhance/i,
      /restructure|reorganize|rewrite/i
    ],
    score: 8
  },
  docs: {
    patterns: [/readme|doc|comment|documentation/i],
    fileTypes: ['.md', '.txt', '.rst'],
    score: 10
  },
  style: {
    patterns: [/format|style|css|lint/i],
    fileTypes: ['.css', '.scss', '.less', '.html'],
    score: 8
  },
  test: {
    patterns: [/test|spec|coverage/i],
    fileTypes: ['.test.js', '.spec.js', '.test.ts', '.spec.ts'],
    score: 10
  },
  chore: {
    patterns: [
      /config|package|dependency|version/i,
      /cleanup|update|upgrade/i
    ],
    fileTypes: ['.json', '.yml', '.yaml', '.lock'],
    score: 6
  }
};
```

**评分算法**：
```javascript
function detectCommitType(changes, diffContent) {
  const scores = {};

  // 基于文件模式评分
  changes.forEach(change => {
    Object.entries(commitTypeRules).forEach(([type, rule]) => {
      if (rule.fileTypes.includes(change.extension)) {
        scores[type] = (scores[type] || 0) + rule.score;
      }
    });
  });

  // 基于内容模式评分
  Object.entries(commitTypeRules).forEach(([type, rule]) => {
    rule.patterns.forEach(pattern => {
      if (diffContent.match(pattern)) {
        scores[type] = (scores[type] || 0) + rule.score;
      }
    });
  });

  // 返回最高分的类型
  return Object.entries(scores).sort((a, b) => b[1] - a[1])[0][0] || 'chore';
}
```

### 3. Scope 自动识别 (Auto Scope Detection)

**路径映射规则**：
```javascript
const scopeMappings = {
  // 前端相关
  'src/components/': 'components',
  'src/pages/': 'pages',
  'src/hooks/': 'hooks',
  'src/store/': 'store',
  'src/utils/': 'utils',
  'src/styles/': 'styles',
  'src/assets/': 'assets',

  // 后端相关
  'src/api/': 'api',
  'src/controllers/': 'controllers',
  'src/models/': 'models',
  'src/services/': 'services',
  'src/middleware/': 'middleware',
  'src/routes/': 'routes',
  'src/database/': 'db',

  // 配置和工具
  'config/': 'config',
  'scripts/': 'scripts',
  'build/': 'build',
  'docs/': 'docs',
  'tests/': 'test',
  'test/': 'test',

  // 语言特定
  'client/': 'client',
  'server/': 'server',
  'shared/': 'shared',
  'common/': 'common',
  'lib/': 'lib',
  'vendor/': 'vendor'
};
```

**Scope 检测逻辑**：
```javascript
function detectScope(filePath) {
  // 精确匹配
  for (const [path, scope] of Object.entries(scopeMappings)) {
    if (filePath.startsWith(path)) {
      return scope;
    }
  }

  // 模糊匹配
  const pathParts = filePath.split('/');
  if (pathParts.length >= 2) {
    return pathParts[1];
  }

  // 默认值
  return 'app';
}
```

### 4. 提交信息生成 (Commit Message Generation)

**标题生成**：
```javascript
function generateSubject(type, scope, changes) {
  // 识别关键操作
  const actions = identifyActions(changes);

  // 生成动词
  const verbs = {
    feat: ['add', 'create', 'implement', 'introduce'],
    fix: ['fix', 'resolve', 'correct', 'patch'],
    refactor: ['refactor', 'improve', 'optimize', 'restructure'],
    docs: ['update', 'add', 'improve', 'document'],
    style: ['format', 'style', 'adjust', 'align'],
    test: ['add', 'update', 'improve', 'test'],
    chore: ['update', 'configure', 'setup', 'maintain']
  };

  const verb = actions.verb || verbs[type][0];
  const object = actions.object || inferObject(changes);

  // 限制长度在50字符内
  let subject = `${verb} ${object}`;
  if (subject.length > 50) {
    subject = subject.substring(0, 47) + '...';
  }

  return `${type}${scope ? `(${scope})` : ''}: ${subject}`;
}
```

**主体生成**：
```javascript
function generateBody(type, changes, diff) {
  const body = [];

  // 根据类型生成不同的主体结构
  switch (type) {
    case 'feat':
      body.push('## 新增功能');
      body.push(generateFeatureDescription(changes));
      break;

    case 'fix':
      body.push('## 问题描述');
      body.push(generateBugDescription(changes, diff));
      body.push('## 修复方案');
      body.push(generateFixDescription(changes));
      break;

    case 'refactor':
      body.push('## 重构原因');
      body.push(generateRefactorReason(changes));
      body.push('## 改进效果');
      body.push(generateImprovementEffect(changes));
      break;

    default:
      body.push('## 变更内容');
      body.push(generateGenericDescription(changes));
  }

  return body.join('\n\n');
}
```

### 5. 质量检查 (Quality Checks)

**提交前检查清单**：
```javascript
const qualityChecks = {
  hasTestFile: (changes) => {
    // 检查是否有对应的测试文件
    return changes.some(change =>
      change.path.includes('test') ||
      change.path.includes('spec')
    );
  },

  hasBreakingChange: (diff) => {
    // 检查是否有破坏性变更
    return diff.includes('BREAKING CHANGE') ||
           diff.includes('breaking change');
  },

  hasLargeFile: (changes) => {
    // 检查是否有大文件变更
    return changes.some(change => change.additions > 500);
  },

  hasSecret: (diff) => {
    // 检查是否有敏感信息
    const secretPatterns = [
      /password/i,
      /api[_-]?key/i,
      /secret/i,
      /token/i
    ];
    return secretPatterns.some(pattern => diff.match(pattern));
  },

  hasTODO: (diff) => {
    // 检查是否有未完成的 TODO
    return diff.includes('TODO') || diff.includes('FIXME');
  }
};
```

### 6. 智能分支管理 (Smart Branch Management)

**分支命名规则**：
```javascript
const branchNamingPatterns = {
  feature: {
    template: 'feature/{scope}-{description}',
    maxLength: 50,
    separator: '-'
  },
  hotfix: {
    template: 'hotfix/{version}-{description}',
    maxLength: 50,
    separator: '-'
  },
  release: {
    template: 'release/{version}',
    maxLength: 30,
    separator: '-'
  },
  bugfix: {
    template: 'bugfix/{description}',
    maxLength: 40,
    separator: '-'
  }
};

function generateBranchName(type, scope, description, version = null) {
  const pattern = branchNamingPatterns[type] || branchNamingPatterns.feature;

  // 清理描述
  const cleanDesc = description
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, pattern.separator)
    .replace(new RegExp(`^${pattern.separator}+|${pattern.separator}+$`, 'g'), '');

  // 截断长度
  const truncatedDesc = cleanDesc.substring(0, pattern.maxLength);

  // 替换模板变量
  let branchName = pattern.template
    .replace('{scope}', scope || 'misc')
    .replace('{description}', truncatedDesc)
    .replace('{version}', version || 'x.x.x');

  return branchName;
}
```

### 7. 推送安全检查 (Push Safety Checks)

**推送前验证**：
```javascript
const pushSafetyChecks = {
  checkBranchProtection: (branch, config) => {
    const protection = config.branchProtection[branch];
    if (protection) {
      if (protection.includes('require-review') && !hasReview(branch)) {
        return { valid: false, message: '分支需要代码审查' };
      }
      if (protection.includes('require-ci') && !isCIPassing()) {
        return { valid: false, message: 'CI 检查未通过' };
      }
    }
    return { valid: true };
  },

  checkConflicts: async (remote, branch) => {
    const status = await git.fetch(remote);
    const ahead = status.ahead;
    const behind = status.behind;

    if (behind > 0) {
      return {
        valid: false,
        message: `远程分支有 ${behind} 个新提交，建议先拉取`
      };
    }

    return { valid: true };
  },

  checkLargePush: (commits) => {
    if (commits > 10) {
      return {
        valid: false,
        message: `包含 ${commits} 个提交，建议分批推送`
      };
    }
    return { valid: true };
  }
};
```

## 插件集成功能

### 检测其他插件

```javascript
// 检测依赖的插件是否安装
function detectPlugins() {
  const plugins = {
    codeReview: checkPluginExists('code-review'),
    unitTestGenerator: checkPluginExists('unit-test-generator')
  };
  return plugins;
}

// 提示安装缺失的插件
function suggestPlugin(pluginName, feature) {
  return `⚠️  ${pluginName} 插件未安装\n💡 安装后可以${feature}\n📦 安装命令: claude plugin install ${pluginName}`;
}
```

### 集成代码审查

```javascript
// 当使用 --check 参数时集成代码审查
async function runCodeReviewCheck() {
  const hasCodeReview = checkPluginExists('code-review');

  if (!hasCodeReview) {
    console.log(suggestPlugin('code-review', '获得更全面的代码质量检查'));
    return { canContinue: true };
  }

  // 调用 code-review 插件
  const reviewResult = await invokePlugin('code-review', {
    mode: 'quick',
    files: getStagedFiles()
  });

  if (reviewResult.criticalIssues > 0) {
    return {
      canContinue: false,
      message: '发现严重问题，建议修复后再提交'
    };
  }

  return { canContinue: true };
}
```

### 集成单元测试

```javascript
// 当使用 --check-test 参数时集成测试生成
async function runTestCheck() {
  const hasUnitTestGenerator = checkPluginExists('unit-test-generator');

  if (!hasUnitTestGenerator) {
    console.log(suggestPlugin('unit-test-generator', '自动生成缺失的测试用例'));
    return { canContinue: true };
  }

  // 检查是否有文件缺少测试
  const filesWithoutTests = findFilesWithoutTests();

  if (filesWithoutTests.length > 0) {
    console.log(`📝 发现 ${filesWithoutTests.length} 个文件缺少测试`);

    const userChoice = await askUser('是否生成测试用例? [Y/n]');
    if (userChoice === 'y') {
      // 调用 unit-test-generator 插件
      await invokePlugin('unit-test-generator', {
        files: filesWithoutTests,
        autoGenerate: true
      });
    }
  }

  return { canContinue: true };
}
```

## 使用方式

这个技能被 `/commit` 命令自动调用，也可以通过其他代理使用：

```javascript
// 在命令中使用
skill: commit
action: analyzeAndCommit
params: {
  autoMode: false,
  includePush: false,
  runChecks: true,
  integrations: {
    codeReview: true,
    unitTest: true
  }
}

// 在代理中使用
skill: commit
action: generateCommitMessage
params: {
  changes: fileChanges,
  diffContent: diff
}
```

## 配置选项

技能行为可以通过项目配置文件自定义：

```json
{
  "commit": {
    "typeDetection": {
      "customTypes": [
        {
          "type": "perf",
          "description": "性能优化",
          "patterns": ["performance", "optimize", "speed"],
          "score": 8
        }
      ]
    },
    "scopeMapping": {
      "src/": "src",
      "lib/": "lib",
      "pkg/": "pkg"
    },
    "qualityChecks": {
      "enabled": ["hasTestFile", "hasSecret", "hasTODO"],
      "severity": {
        "hasSecret": "error",
        "hasTODO": "warning",
        "hasTestFile": "info"
      }
    },
    "branchManagement": {
      "autoCreate": true,
      "defaultType": "feature",
      "naming": {
        "maxWords": 5,
        "useCamelCase": false
      }
    },
    "integrations": {
      "codeReview": {
        "enabled": true,
        "severity": "warning",
        "autoFix": false
      },
      "unitTest": {
        "enabled": true,
        "coverage": 80,
        "autoGenerate": false
      }
    }
  }
}
```

## 集成示例

### 与代码审查集成

```javascript
// 在提交前运行代码审查
const commitWithReview = async (changes) => {
  // 1. 检测插件
  const plugins = detectPlugins();

  if (!plugins.codeReview) {
    console.log(suggestPlugin('code-review', '获得更全面的代码质量检查'));
  }

  // 2. 运行质量检查
  const qualityResult = await runQualityChecks(changes);

  if (qualityResult.warnings.length > 0 && plugins.codeReview) {
    // 3. 运行代码审查
    const reviewResult = await skill('code-review', {
      files: changes.map(c => c.path),
      mode: 'quick'
    });

    if (reviewResult.criticalIssues > 0) {
      return {
        canCommit: false,
        reason: '发现严重问题，建议修复后再提交'
      };
    }
  }

  return { canCommit: true };
};
```

### 与 CI/CD 集成

```javascript
// 推送后触发 CI
const pushAndTriggerCI = async (branch, commits) => {
  // 1. 执行推送
  await git.push('origin', branch);

  // 2. 触发 CI
  const ciUrl = await triggerCI({
    repository: process.env.GITHUB_REPO,
    branch: branch,
    commits: commits
  });

  return {
    pushed: true,
    ciUrl: ciUrl,
    status: 'pending'
  };
};
```

## 性能优化

### 缓存机制

```javascript
// 缓存分析结果
const analysisCache = new Map();

function getCachedAnalysis(fileHash) {
  return analysisCache.get(fileHash);
}

function setCachedAnalysis(fileHash, result) {
  analysisCache.set(fileHash, {
    result,
    timestamp: Date.now()
  });

  // 清理过期缓存
  if (analysisCache.size > 100) {
    const oldest = Array.from(analysisCache.entries())
      .sort((a, b) => a[1].timestamp - b[1].timestamp)[0];
    analysisCache.delete(oldest[0]);
  }
}
```

### 异步处理

```javascript
// 异步分析大型变更
async function analyzeLargeChanges(changes) {
  const batchSize = 10;
  const results = [];

  for (let i = 0; i < changes.length; i += batchSize) {
    const batch = changes.slice(i, i + batchSize);
    const batchResult = await Promise.all(
      batch.map(change => analyzeFileChange(change))
    );
    results.push(...batchResult);

    // 让出控制权
    await new Promise(resolve => setTimeout(resolve, 0));
  }

  return results;
}
```

## 错误处理

### 错误类型定义

```javascript
const CommitErrors = {
  NO_CHANGES: 'NO_CHANGES',
  NOTHING_STAGED: 'NOTHING_STAGED',
  LARGE_COMMIT: 'LARGE_COMMIT',
  CONFLICT: 'CONFLICT',
  NETWORK_ERROR: 'NETWORK_ERROR',
  PERMISSION_DENIED: 'PERMISSION_DENIED',
  PLUGIN_MISSING: 'PLUGIN_MISSING'
};

function handleError(error, context) {
  const errorMap = {
    [CommitErrors.NOTHING_STAGED]: {
      message: '没有暂存的变更',
      suggestion: '使用 git add 暂存文件'
    },
    [CommitErrors.LARGE_COMMIT]: {
      message: '提交过大',
      suggestion: '考虑拆分成多个提交'
    },
    [CommitErrors.PLUGIN_MISSING]: {
      message: '缺少依赖插件',
      suggestion: '安装建议的插件以获得完整功能'
    }
  };

  const errorInfo = errorMap[error.code] || {
    message: '未知错误',
    suggestion: '查看错误详情'
  };

  return {
    ...errorInfo,
    context,
    timestamp: new Date().toISOString()
  };
}
```

这个技能提供了完整的 Git 提交管理能力，从变更分析到提交信息生成，再到质量检查和推送管理，形成了一个完整的解决方案。同时通过插件检测和集成机制，可以与其他插件协作，提供更强大的功能。