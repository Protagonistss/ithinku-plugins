# Git Helper Functions

通用 Git 操作辅助函数集合。

## 基础操作

### 获取提交信息
```javascript
// 获取指定范围的提交
async function getCommits(range = 'HEAD~10..HEAD', options = {}) {
  return await git.log({
    from: range.split('..')[0],
    to: range.split('..')[1] || 'HEAD',
    ...options
  });
}

// 获取文件变更统计
async function getFileStats(commitHash) {
  const diff = await git.diff([`${commitHash}^`, commitHash, '--stat']);
  return parseDiffStats(diff);
}

// 解析 diff 统计信息
function parseDiffStats(diffOutput) {
  const lines = diffOutput.split('\n');
  const stats = {
    files: [],
    total: { insertions: 0, deletions: 0, files: 0 }
  };

  for (const line of lines) {
    const match = line.match(/\s*(\d+)\s+(\d+)\s+(.+)/);
    if (match) {
      const [, insertions, deletions, file] = match;
      stats.files.push({
        file,
        insertions: parseInt(insertions),
        deletions: parseInt(deletions)
      });
      stats.total.insertions += parseInt(insertions);
      stats.total.deletions += parseInt(deletions);
      stats.total.files++;
    }
  }

  return stats;
}
```

### 分支操作
```javascript
// 获取所有分支
async function getAllBranches() {
  const branches = await git.branch(['-a']);
  return {
    local: branches.branches,
    remote: branches.remote,
    current: branches.current
  };
}

// 获取分支跟踪关系
async function getTrackingBranches() {
  const tracking = new Map();
  const branches = await git.branch(['-vv']);

  for (const branch of Object.keys(branches.branches)) {
    const trackingInfo = branches.branches[branch].match(/^\[([^\]]+)\]/);
    if (trackingInfo) {
      tracking.set(branch, trackingInfo[1]);
    }
  }

  return tracking;
}

// 检查分支是否受保护
function isProtectedBranch(branchName) {
  const protected = ['main', 'master', 'develop', 'dev'];
  return protected.includes(branchName) || branchName.startsWith('release/');
}
```

### 暂存操作
```javascript
// 智能暂存
async function smartStash(options = {}) {
  const status = await git.status();
  if (!status.dirty) return { stashed: false, reason: '工作区干净' };

  const stashMessage = options.message || generateStashMessage();
  await git.stash(['push', '-m', stashMessage]);

  return { stashed: true, message: stashMessage };
}

// 生成暂存消息
function generateStashMessage() {
  const now = new Date();
  return `WIP on ${process.cwd()} at ${now.toISOString()}`;
}
```

## 分析工具

### 文件类型分析
```javascript
// 获取文件类型
function getFileType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const typeMap = {
    '.js': 'javascript',
    '.ts': 'typescript',
    '.jsx': 'react',
    '.tsx': 'react',
    '.py': 'python',
    '.java': 'java',
    '.go': 'go',
    '.rs': 'rust',
    '.md': 'documentation',
    '.json': 'config',
    '.yml': 'config',
    '.yaml': 'config',
    '.test.js': 'test',
    '.spec.js': 'test',
    '.test.ts': 'test',
    '.spec.ts': 'test'
  };

  return typeMap[ext] || 'unknown';
}

// 分析文件变更
function analyzeFileChange(filePath, status, diff) {
  return {
    path: filePath,
    type: status.charAt(0), // A=Added, M=Modified, D=Deleted
    fileType: getFileType(filePath),
    scope: extractScope(filePath),
    complexity: calculateComplexity(diff),
    impact: assessImpact(diff)
  };
}

// 提取文件 scope
function extractScope(filePath) {
  const parts = filePath.split('/');
  if (parts.length > 1) {
    return parts[0];
  }
  return 'root';
}

// 计算变更复杂度
function calculateComplexity(diff) {
  const lines = diff.split('\n');
  let additions = 0;
  let deletions = 0;
  let changes = 0;

  for (const line of lines) {
    if (line.startsWith('+') && !line.startsWith('+++')) {
      additions++;
    } else if (line.startsWith('-') && !line.startsWith('---')) {
      deletions++;
    } else if (line.startsWith(' ')) {
      changes++;
    }
  }

  return {
    additions,
    deletions,
    changes,
    total: additions + deletions + changes,
    score: Math.max(additions, deletions) + (changes * 0.1)
  };
}
```

## 搜索和过滤

### 搜索提交
```javascript
// 按关键词搜索提交
async function searchCommits(query, options = {}) {
  return await git.log({
    grep: query,
    all: options.all || false,
    maxCount: options.limit || 50
  });
}

// 按作者搜索
async function searchByAuthor(author, options = {}) {
  return await git.log({
    author,
    all: options.all || false,
    maxCount: options.limit || 50
  });
}

// 按文件搜索
async function searchByFile(filePath, options = {}) {
  return await git.log({
    file: filePath,
    all: options.all || false,
    maxCount: options.limit || 50
  });
}
```

## 网络和远程

### 网络检查
```javascript
// 测试远程连接
async function testRemoteConnection(remoteUrl) {
  try {
    await git.lsRemote(remoteUrl);
    return { connected: true };
  } catch (error) {
    return { connected: false, error: error.message };
  }
}

// 获取远程状态
async function getRemoteStatus(remote = 'origin') {
  try {
    await git.fetch(remote, '--dry-run');
    return { reachable: true };
  } catch (error) {
    return { reachable: false, error: error.message };
  }
}
```

## 实用工具

### 颜色输出
```javascript
const colors = {
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m',
  reset: '\x1b[0m'
};

function colorize(text, color) {
  return `${colors[color]}${text}${colors.reset}`;
}

// 彩色输出状态
function colorizeStatus(status) {
  const statusColors = {
    added: 'green',
    modified: 'yellow',
    deleted: 'red',
    renamed: 'blue',
    untracked: 'magenta'
  };
  return colorize(status, statusColors[status] || 'white');
}
```

### 进度显示
```javascript
// 显示进度条
function showProgressBar(current, total, width = 50) {
  const percentage = Math.round((current / total) * 100);
  const filled = Math.round((width * current) / total);
  const empty = width - filled;

  const bar = '█'.repeat(filled) + '░'.repeat(empty);
  return `[${bar}] ${percentage}%`;
}

// 格式化时间
function formatDuration(ms) {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);

  if (hours > 0) {
    return `${hours}h ${minutes % 60}m`;
  } else if (minutes > 0) {
    return `${minutes}m ${seconds % 60}s`;
  } else {
    return `${seconds}s`;
  }
}
```

### 数据转换
```javascript
// 将字节转换为可读格式
function formatBytes(bytes) {
  const units = ['B', 'KB', 'MB', 'GB'];
  let size = bytes;
  let unitIndex = 0;

  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }

  return `${size.toFixed(1)} ${units[unitIndex]}`;
}

// 短文本截断
function truncateText(text, maxLength = 50, suffix = '...') {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength - suffix.length) + suffix;
}