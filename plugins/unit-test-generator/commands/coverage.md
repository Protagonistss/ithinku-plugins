# 测试覆盖率分析命令

分析测试覆盖率，识别未覆盖的代码路径，并生成补充测试用例。

## 使用方法

```bash
/coverage <target> [options]
```

### 参数

- `target`: 分析目标，可以是：
  - 文件路径：`src/utils/calculator.js`
  - 目录路径：`src/services/`
  - 测试文件：`tests/calculator.test.js`

### 选项

- `--threshold, -t`: 覆盖率阈值（默认：80）
- `--format, -f`: 输出格式
  - `text` (默认)
  - `json`
  - `html`
- `--generate, -g`: 自动生成缺失的测试
- `--output, -o`: 报告输出目录
- `--include, -i`: 包含的文件模式
- `--exclude, -e`: 排除的文件模式
- `--branch`: 包含分支覆盖率分析

## 示例

```bash
# 分析单个文件的覆盖率
/coverage src/utils/calculator.js

# 生成覆盖率报告
/coverage src/ --format html --output coverage-report

# 自动生成缺失的测试
/coverage src/api/userService.js --generate --threshold 90

# 排除特定文件
/coverage src/ --exclude "*.test.js" --exclude "mocks/*"
```

## 覆盖率分析

### 覆盖率类型

1. **语句覆盖率**（Statement Coverage）
   - 执行的代码语句百分比
   - 最基础的覆盖率指标

2. **分支覆盖率**（Branch Coverage）
   - 执行的条件分支百分比
   - 检测if/else、三元运算符等

3. **函数覆盖率**（Function Coverage）
   - 调用的函数百分比
   - 确保所有函数都被测试

4. **行覆盖率**（Line Coverage）
   - 执行的代码行百分比
   - 类似语句覆盖率但更精确

### 分析输出示例

```
覆盖率报告 - src/utils/calculator.js
==========================================

语句覆盖率: 75% (6/8)
分支覆盖率: 50% (2/4)
函数覆盖率: 100% (2/2)
行覆盖率: 75% (6/8)

未覆盖的代码:
----------------
第 10 行:   if (b === 0) {
第 11 行:     throw new Error('Division by zero');
第 15 行:   return a * b;
第 16 行: }

建议生成的测试:
----------------
1. 测试除数为零的异常情况
2. 测试乘法函数的功能
```

## 自动测试生成

### 缺失测试识别

```javascript
// 源代码
function calculate(a, b, operation) {
  switch (operation) {
    case 'add':
      return a + b;
    case 'subtract':
      return a - b;
    case 'multiply':
      return a * b;
    case 'divide':
      if (b === 0) throw new Error('Division by zero');
      return a / b;
    default:
      throw new Error('Invalid operation');
  }
}

// 现有测试
test('should add two numbers', () => {
  expect(calculate(2, 3, 'add')).toBe(5);
});

test('should subtract two numbers', () => {
  expect(calculate(5, 3, 'subtract')).toBe(2);
});

// 覆盖率分析结果
{
  uncovered: [
    {
      type: 'branch',
      line: 8, // multiply case
      description: 'multiply operation not tested'
    },
    {
      type: 'branch',
      line: 10, // divide error case
      description: 'division by zero not tested'
    },
    {
      type: 'branch',
      line: 12, // default case
      description: 'invalid operation not tested'
    }
  ]
}
```

### 自动生成补充测试

```javascript
// 生成的补充测试
describe('calculate - missing cases', () => {
  test('should multiply two numbers', () => {
    expect(calculate(3, 4, 'multiply')).toBe(12);
  });

  test('should handle division by zero', () => {
    expect(() => calculate(10, 0, 'divide')).toThrow('Division by zero');
  });

  test('should handle invalid operation', () => {
    expect(() => calculate(2, 3, 'mod')).toThrow('Invalid operation');
  });

  // 边界值测试
  test('should handle edge cases', () => {
    expect(calculate(0, 5, 'add')).toBe(5);
    expect(calculate(-2, 3, 'add')).toBe(1);
  });
});
```

## 覆盖率报告格式

### 文本格式

```
=== 覆盖率汇总 ===
文件总数: 25
语句覆盖率: 78.5% (450/573)
分支覆盖率: 65.2% (132/203)
函数覆盖率: 85.0% (85/100)

=== 未覆盖的文件 ===
src/utils/logger.js (0%)
src/helpers/dateFormatter.js (45%)

=== 覆盖率最低的文件 ===
src/services/auth.js (45%)
src/api/client.js (50%)
src/utils/validator.js (55%)
```

### JSON格式

```json
{
  "summary": {
    "totalFiles": 25,
    "statements": { "total": 573, "covered": 450, "percent": 78.5 },
    "branches": { "total": 203, "covered": 132, "percent": 65.2 },
    "functions": { "total": 100, "covered": 85, "percent": 85.0 }
  },
  "files": [
    {
      "path": "src/utils/calculator.js",
      "statements": { "total": 8, "covered": 6, "percent": 75 },
      "branches": { "total": 4, "covered": 2, "percent": 50 },
      "uncoveredLines": [10, 11, 15, 16]
    }
  ]
}
```

### HTML格式

生成可视化的HTML报告，包含：
- 交互式覆盖率图表
- 文件级覆盖率详情
- 代码高亮显示未覆盖部分
- 历史趋势分析

## 高级功能

### 覆盖率阈值配置

```javascript
// .coverage.config.js
module.exports = {
  thresholds: {
    global: {
      statements: 80,
      branches: 70,
      functions: 90,
      lines: 80
    },
    file: {
      statements: 60,
      branches: 50,
      functions: 80,
      lines: 60
    }
  },
  excludePatterns: [
    "*.test.js",
    "*.mock.js",
    "node_modules/**",
    "coverage/**"
  ]
};
```

### 增量覆盖率分析

```bash
# 只分析变更的文件
/coverage src/ --incremental --base main

# 对比覆盖率变化
/coverage src/ --compare-with coverage-report-previous.json
```

### 覆盖率趋势分析

```bash
# 生成趋势报告
/coverage src/ --trend --output coverage-trend.json

# 查看历史数据
/coverage-history --days 30
```

## 集成配置

### Jest配置

```javascript
// jest.config.js
module.exports = {
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  coverageThreshold: {
    global: {
      statements: 80,
      branches: 70,
      functions: 90,
      lines: 80
    }
  },
  collectCoverageFrom: [
    'src/**/*.{js,ts}',
    '!src/**/*.d.ts',
    '!src/**/*.test.{js,ts}'
  ]
};
```

### Vitest配置

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      threshold: {
        global: {
          statements: 80,
          branches: 70,
          functions: 90,
          lines: 80
        }
      }
    }
  }
});
```

## 最佳实践

### 1. 设定合理的覆盖率目标
- 100%覆盖率往往不现实
- 根据代码重要性设定不同标准
- 专注于核心业务逻辑

### 2. 关注代码质量而非数字
- 高覆盖率不等于好测试
- 确保测试有意义
- 避免为了覆盖率而测试

### 3. 持续监控覆盖率
- 在CI/CD中集成覆盖率检查
- 设置覆盖率阈值门禁
- 定期审查覆盖率报告

### 4. 使用覆盖率作为指导
- 识别复杂和未测试的代码
- 指导重构和测试优化
- 发现潜在的死代码

## 相关命令

- `/test` - 生成测试用例
- `/mock` - 生成Mock数据
- @TestExpert - 获取测试覆盖率优化建议