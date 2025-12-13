# Commit Types Configuration

标准提交类型配置和扩展规则。

## Conventional Commits 标准

### 基础类型
```javascript
const standardTypes = {
  feat: {
    description: '新功能',
    emoji: '✨',
    semver: 'minor',
    patterns: [/add|create|implement|introduce|new/i],
    fileTypes: ['.js', '.ts', '.jsx', '.tsx', '.py', '.java', '.go', '.rs']
  },
  fix: {
    description: '修复问题',
    emoji: '🐛',
    semver: 'patch',
    patterns: [/fix|bug|error|issue|problem|patch|resolve/i],
    fileTypes: ['.js', '.ts', '.py', '.java', '.go', '.rs']
  },
  docs: {
    description: '文档更新',
    emoji: '📝',
    semver: 'patch',
    patterns: [/doc|readme|comment|documentation|guide/i],
    fileTypes: ['.md', '.rst', '.txt', '.doc']
  },
  style: {
    description: '格式调整',
    emoji: '💄',
    semver: 'patch',
    patterns: [/format|style|css|lint|prettier|beautify/i],
    fileTypes: ['.css', '.scss', '.less', '.html', '.json', '.yml']
  },
  refactor: {
    description: '代码重构',
    emoji: '♻️',
    semver: 'patch',
    patterns: [/refactor|improve|optimize|enhance|restructure|reorganize/i],
    fileTypes: ['.js', '.ts', '.py', '.java', '.go', '.rs']
  },
  test: {
    description: '测试相关',
    emoji: '✅',
    semver: 'patch',
    patterns: [/test|spec|coverage|jest|mocha|cypress/i],
    fileTypes: ['.test.js', '.spec.js', '.test.ts', '.spec.ts', '.test.py']
  },
  chore: {
    description: '构建/工具',
    emoji: '🔧',
    semver: 'patch',
    patterns: [/config|package|dependency|version|build|ci|cd/i],
    fileTypes: ['.json', '.yml', '.yaml', '.lock', 'Dockerfile']
  }
};
```

### 扩展类型
```javascript
const extendedTypes = {
  perf: {
    description: '性能优化',
    emoji: '⚡',
    semver: 'patch',
    patterns: [/performance|speed|fast|slow|optimize|cache/i],
    fileTypes: ['.js', '.ts', '.py', '.java', '.go', '.rs']
  },
  build: {
    description: '构建系统',
    emoji: '📦',
    semver: 'patch',
    patterns: [/webpack|babel|rollup|vite|gulp|grunt/i],
    fileTypes: ['webpack.config.js', 'babel.config.js', 'rollup.config.js']
  },
  ci: {
    description: 'CI/CD',
    emoji: '👷',
    semver: 'patch',
    patterns: [/github|gitlab|travis|circle|jenkins|action/i],
    fileTypes: ['.github/workflows/*.yml', '.gitlab-ci.yml', '.travis.yml']
  },
  revert: {
    description: '回滚更改',
    emoji: '⏪',
    semver: 'patch',
    patterns: [/revert|rollback|undo|backout/i],
    fileTypes: []
  },
  security: {
    description: '安全修复',
    emoji: '🔒',
    semver: 'patch',
    patterns: [/security|vulnerability|cve|exploit|protect/i],
    fileTypes: ['.js', '.ts', '.py', '.java', '.go', '.rs']
  },
  deps: {
    description: '依赖更新',
    emoji: '⬆️',
    semver: 'patch',
    patterns: [/update|upgrade|bump|version|npm|yarn|pip/i],
    fileTypes: ['package.json', 'requirements.txt', 'pom.xml', 'build.gradle']
  }
};
```

### 类型检测权重
```javascript
const typeWeights = {
  // 文件类型匹配权重
  fileTypeMatch: 5,

  // 内容模式匹配权重
  contentPatternMatch: 3,

  // 文件路径匹配权重
  pathPatternMatch: 2,

  // 默认权重
  default: 1
};
```

## 自定义类型示例

### 前端项目
```javascript
const frontendTypes = {
  ...standardTypes,
  ui: {
    description: 'UI组件',
    emoji: '🎨',
    semver: 'minor',
    patterns: [/component|ui|view|template/i],
    fileTypes: ['.jsx', '.tsx', '.vue', '.svelte']
  },
  assets: {
    description: '静态资源',
    emoji: '🖼️',
    semver: 'patch',
    patterns: [/image|icon|font|asset/i],
    fileTypes: ['.png', '.jpg', '.svg', '.woff', '.woff2']
  },
  i18n: {
    description: '国际化',
    emoji: '🌐',
    semver: 'patch',
    patterns: [/i18n|locale|translation|lang/i],
    fileTypes: ['.json', '.po', '.mo', '.properties']
  }
};
```

### 后端项目
```javascript
const backendTypes = {
  ...standardTypes,
  api: {
    description: 'API变更',
    emoji: '🔌',
    semver: 'minor',
    patterns: [/api|endpoint|route|controller/i],
    fileTypes: ['.js', '.ts', '.py', '.java', '.go']
  },
  db: {
    description: '数据库',
    emoji: '🗄️',
    semver: 'patch',
    patterns: [/migration|schema|query|model|entity/i],
    fileTypes: ['.sql', '.migration.js', 'models/*.js']
  },
  middleware: {
    description: '中间件',
    emoji: '🔧',
    semver: 'patch',
    patterns: [/middleware|interceptor|filter|guard/i],
    fileTypes: ['.js', '.ts', '.py', '.java', '.go']
  }
};
```

### 数据科学项目
```javascript
const dataScienceTypes = {
  ...standardTypes,
  data: {
    description: '数据处理',
    emoji: '📊',
    semver: 'patch',
    patterns: [/data|process|clean|transform|extract/i],
    fileTypes: ['.py', '.ipynb', '.r', '.sql']
  },
  model: {
    description: '模型相关',
    emoji: '🤖',
    semver: 'minor',
    patterns: [/model|train|predict|ml|ai|deep/i],
    fileTypes: ['.py', '.ipynb', '.pkl', '.joblib']
  },
  analysis: {
    description: '数据分析',
    emoji: '📈',
    semver: 'patch',
    patterns: [/analysis|explore|visualize|report/i],
    fileTypes: ['.py', '.ipynb', '.r', '.html']
  }
};
```

## 使用方式

```javascript
// 获取所有类型
function getAllTypes(projectType = 'default') {
  const baseTypes = { ...standardTypes, ...extendedTypes };

  switch (projectType) {
    case 'frontend':
      return { ...baseTypes, ...frontendTypes };
    case 'backend':
      return { ...baseTypes, ...backendTypes };
    case 'data-science':
      return { ...baseTypes, ...dataScienceTypes };
    default:
      return baseTypes;
  }
}

// 检测提交类型
function detectCommitType(changes, diff, projectType = 'default') {
  const types = getAllTypes(projectType);
  const scores = {};

  for (const [type, config] of Object.entries(types)) {
    let score = 0;

    // 文件类型匹配
    changes.forEach(change => {
      if (config.fileTypes.includes(change.extension)) {
        score += typeWeights.fileTypeMatch;
      }
    });

    // 内容模式匹配
    config.patterns.forEach(pattern => {
      if (diff.match(pattern)) {
        score += typeWeights.contentPatternMatch;
      }
    });

    if (score > 0) {
      scores[type] = score;
    }
  }

  // 返回得分最高的类型
  if (Object.keys(scores).length === 0) {
    return 'chore'; // 默认类型
  }

  return Object.entries(scores)
    .sort(([, a], [, b]) => b - a)[0][0];
}
```