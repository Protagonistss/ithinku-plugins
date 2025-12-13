# Git Tools Common Types

通用类型定义和接口。

## Git 对象类型

### 提交对象
```typescript
interface GitCommit {
  hash: string;
  shortHash: string;
  author: {
    name: string;
    email: string;
    date: Date;
  };
  committer: {
    name: string;
    email: string;
    date: Date;
  };
  message: string;
  subject: string;
  body: string;
  type: string; // feat, fix, docs, etc.
  scope?: string;
  breaking: boolean;
  stats: {
    insertions: number;
    deletions: number;
    files: number;
    total: number;
  };
  files: GitFileChange[];
  parents: string[];
}
```

### 文件变更对象
```typescript
interface GitFileChange {
  path: string;
  oldPath?: string; // 重命名时的原路径
  type: 'added' | 'modified' | 'deleted' | 'renamed' | 'copied';
  extension: string;
  fileType: string; // javascript, typescript, etc.
  scope: string;
  stats: {
    insertions: number;
    deletions: number;
    total: number;
  };
  diff?: string;
  complexity: number;
}
```

### 分支对象
```typescript
interface GitBranch {
  name: string;
  type: 'local' | 'remote';
  current: boolean;
  tracking?: string;
  ahead: number;
  behind: number;
  lastCommit: {
    hash: string;
    message: string;
    date: Date;
    author: string;
  };
  protected: boolean;
  lifecycle?: 'permanent' | 'temporary';
}
```

### 远程仓库对象
```typescript
interface GitRemote {
  name: string;
  url: string;
  type: 'https' | 'ssh' | 'git';
  fetch: string;
  push: string;
  primary?: boolean;
}
```

## 操作结果类型

### 操作结果基类
```typescript
interface OperationResult {
  success: boolean;
  message?: string;
  timestamp: Date;
  duration?: number;
}

interface SuccessResult extends OperationResult {
  success: true;
  data?: any;
}

interface ErrorResult extends OperationResult {
  success: false;
  error: {
    code: string;
    message: string;
    suggestion?: string;
    details?: any;
  };
}

type Result = SuccessResult | ErrorResult;
```

### 提交结果
```typescript
interface CommitResult extends SuccessResult {
  data: {
    commit: GitCommit;
    hash: string;
    message: string;
    stats: {
      files: number;
      insertions: number;
      deletions: number;
    };
  };
}
```

### 合并结果
```typescript
interface MergeResult extends Result {
  data?: {
    merged: boolean;
    conflicts?: GitConflict[];
    strategy: 'merge' | 'rebase' | 'squash';
    targetBranch: string;
  };
}

interface GitConflict {
  file: string;
  type: 'content' | 'add-add' | 'delete-modify' | 'rename';
  markers: {
    start: string;
    separator: string;
    end: string;
  };
  sections: {
    base: string;
    current: string;
    incoming: string;
  };
}
```

### 推送结果
```typescript
interface PushResult extends Result {
  data?: {
    remote: string;
    branch: string;
    pushed: string[];
    rejected: string[];
    ahead: number;
  };
}
```

## 配置类型

### 插件配置
```typescript
interface GitToolsConfig {
  defaultWorkflow: 'gitflow' | 'github' | 'gitlab' | 'custom';
  autoSafetyCheck: boolean;
  enableIntegrations: boolean;
  logLevel: 'debug' | 'info' | 'warn' | 'error';
  skills: {
    [skillName: string]: SkillConfig;
  };
}

interface SkillConfig {
  enabled: boolean;
  options: Record<string, any>;
  integrations: IntegrationConfig[];
}
```

### 提交配置
```typescript
interface CommitConfig {
  typeDetection: {
    customTypes: CustomCommitType[];
    strategy: 'pattern' | 'ml' | 'hybrid';
  };
  scopeMapping: Record<string, string>;
  qualityChecks: {
    enabled: string[];
    severity: Record<string, 'error' | 'warning' | 'info'>;
    thresholds: Record<string, number>;
  };
  messageFormat: {
    template?: string;
    maxLength?: number;
    requireBody?: boolean;
    includeFooter?: boolean;
  };
}

interface CustomCommitType {
  type: string;
  description: string;
  emoji?: string;
  semver: 'major' | 'minor' | 'patch';
  patterns: RegExp[];
  fileTypes: string[];
}
```

### 分支配置
```typescript
interface BranchConfig {
  strategy: BranchStrategy;
  naming: NamingRules;
  protection: ProtectionRules;
  lifecycle: LifecycleRules;
}

interface BranchStrategy {
  name: string;
  branches: Record<string, BranchDefinition>;
  workflow: WorkflowStep[];
}

interface BranchDefinition {
  type: string;
  purpose: string;
  source?: string;
  target?: string | string[];
  protection: ProtectionRules;
  mergeStrategy: string;
  autoDelete?: boolean;
  lifecycle?: 'permanent' | 'temporary';
}
```

## 集成类型

### 插件集成
```typescript
interface PluginIntegration {
  name: string;
  version?: string;
  required?: boolean;
  config?: Record<string, any>;
  hooks?: {
    pre?: string[];
    post?: string[];
  };
}

interface IntegrationConfig {
  type: 'code-review' | 'unit-test' | 'ci-cd' | 'project-management' | 'communication';
  enabled: boolean;
  autoTrigger: boolean;
  options: Record<string, any>;
}
```

### CI/CD 集成
```typescript
interface CIConfig {
  type: 'github-actions' | 'gitlab-ci' | 'jenkins' | 'circleci';
  webhook?: string;
  token?: string;
  events: string[];
  autoTrigger: boolean;
  environment?: Record<string, string>;
}

interface CDConfig {
  type: 'github-pages' | 'vercel' | 'netlify' | 'heroku' | 'docker';
  provider: string;
  token?: string;
  environments: Environment[];
  autoDeploy?: boolean;
}

interface Environment {
  name: string;
  branch: string;
  url?: string;
  deployCommand?: string;
  healthCheck?: {
    url: string;
    timeout: number;
  };
}
```

## 分析类型

### 代码质量分析
```typescript
interface QualityAnalysis {
  score: number;
  issues: QualityIssue[];
  suggestions: string[];
  metrics: {
    complexity: number;
    duplication: number;
    coverage?: number;
  };
}

interface QualityIssue {
  file: string;
  line?: number;
  type: 'error' | 'warning' | 'info';
  category: 'style' | 'logic' | 'security' | 'performance';
  message: string;
  suggestion?: string;
}
```

### 历史分析
```typescript
interface HistoryAnalysis {
  commitCount: number;
  dateRange: {
    start: Date;
    end: Date;
  };
  contributors: Contributor[];
  patterns: CommitPattern[];
  qualityScore: number;
  recommendations: string[];
}

interface Contributor {
  name: string;
  email: string;
  commits: number;
  insertions: number;
  deletions: number;
  firstCommit: Date;
  lastCommit: Date;
}

interface CommitPattern {
  type: string;
  count: number;
  percentage: number;
  trend: 'increasing' | 'decreasing' | 'stable';
}
```

## 事件类型

### Git 事件
```typescript
interface GitEvent {
  type: GitEventType;
  timestamp: Date;
  data: any;
  source: string;
}

type GitEventType =
  | 'branch.created'
  | 'branch.deleted'
  | 'branch.merged'
  | 'commit.created'
  | 'commit.pushed'
  | 'pull_request.opened'
  | 'pull_request.merged'
  | 'tag.created'
  | 'release.created';
```

### 技能事件
```typescript
interface SkillEvent {
  skill: string;
  action: string;
  status: 'started' | 'completed' | 'failed';
  duration?: number;
  result?: Result;
  context?: Record<string, any>;
}
```

## 工具类型

### 条件类型
```typescript
// 根据成功状态返回不同类型
type SuccessData<T> = T extends { success: true } ? T['data'] : never;

// 提取错误的详细信息
type ErrorInfo<T> = T extends { success: false } ? T['error'] : never;

// 严格的布尔类型
type StrictBoolean = true | false;

// 语义化版本
interface SemVer {
  major: number;
  minor: number;
  patch: number;
  prerelease?: string;
  build?: string;
}
```

### 函数类型
```typescript
// 异步函数类型
type AsyncFunction<T = void> = (...args: any[]) => Promise<T>;

// 回调函数类型
type Callback<T = void> = (error?: Error | null, result?: T) => void;

// 事件处理器
type EventHandler<T = any> = (event: T) => void | Promise<void>;

// 验证函数
type Validator<T> = (value: T) => boolean | string;
```

## 使用方式

```typescript
// 定义函数返回类型
async function createCommit(message: string): Promise<CommitResult> {
  // 实现
}

// 使用联合类型
function handleResult(result: Result) {
  if (result.success) {
    console.log('成功:', result.data);
  } else {
    console.error('失败:', result.error.message);
  }
}

// 使用泛型约束
class Repository<T extends GitCommit | GitBranch> {
  items: T[];

  add(item: T): void {
    this.items.push(item);
  }

  find(predicate: (item: T) => boolean): T | undefined {
    return this.items.find(predicate);
  }
}
```