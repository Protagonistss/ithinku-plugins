# 单元测试生成技能

这个技能负责分析源代码并生成对应的单元测试用例。支持多种编程语言和测试框架。

## 技能能力

### 1. 代码分析
- AST解析，识别函数、类、方法
- 分析函数签名和参数类型
- 识别依赖关系和导入模块
- 检测异步函数和Promise使用

### 2. 测试场景生成
- 正常流程测试（Happy Path）
- 边界条件测试（Boundary Values）
- 异常情况测试（Error Cases）
- 参数验证测试

### 3. 测试代码生成
- 根据选择的框架生成测试代码
- 生成合适的测试名称和描述
- 添加必要的设置和清理代码
- 生成有意义的断言

## 使用方式

### 基础调用

```typescript
// 生成单个函数的测试
await generateUnitTest('src/utils/calculator.js', {
  functionName: 'add',
  framework: 'vitest'
});

// 生成整个文件的测试
await generateUnitTest('src/services/userService.js', {
  framework: 'vitest',
  includeMocks: true
});
```

### 高级选项

```typescript
await generateUnitTest(targetFile, {
  framework: 'vitest',
  outputDir: 'tests/unit',
  includeCoverage: true,
  mockExternalDependencies: true,
  generateDataProviders: true,
  testPatterns: ['happy-path', 'edge-cases', 'error-handling']
});
```

## 测试模板

### JavaScript/TypeScript - Jest模板

```javascript
{{#if isClass}}
describe('{{className}}', () => {
  let instance;

  beforeEach(() => {
    instance = new {{className}}();
  });

  {{#each methods}}
  describe('{{name}}', () => {
    it('should work correctly with valid inputs', async () => {
      // TODO: Add test implementation
    });
  });
  {{/each}}
});
{{else}}
{{#each functions}}
describe('{{name}}', () => {
  it('should work correctly with valid inputs', async () => {
    // TODO: Add test implementation
  });
});
{{/each}}
{{/if}}
```

### JavaScript/TypeScript - Vitest模板

```typescript
import { describe, it, expect, beforeEach } from 'vitest';

{{#if hasImports}}
{{#each imports}}
import { {{name}} } from '{{path}}';
{{/each}}
{{/if}}

{{#if isClass}}
describe('{{className}}', () => {
  let instance: {{className}};

  beforeEach(() => {
    instance = new {{className}}();
  });

  {{#each methods}}
  describe('{{name}}', () => {
    it('should return correct result', () => {
      const result = instance.{{name}}({{#if hasParams}}/* parameters */{{/if}});
      expect(result).toBeDefined();
    });
  });
  {{/each}}
});
{{/if}}
```

### Python - pytest模板

```python
import pytest
from pathlib import Path
import sys

# Add source directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

{{#each imports}}
{{.}}
{{/each}}

{{#if isClass}}
class Test{{className}}:
    def setup_method(self):
        """Setup before each test method"""
        self.instance = {{className}}()

    {{#each methods}}
    def test_{{name}}_success(self):
        """Test {{name}} with valid inputs"""
        # TODO: Add test implementation
        pass

    def test_{{name}}_edge_cases(self):
        """Test {{name}} with edge cases"""
        # TODO: Add edge case tests
        pass
    {{/each}}
{{/if}}
```

## 测试数据生成

### 基础数据类型

```typescript
function generateTestData(type: string, constraints?: any): any {
  switch (type) {
    case 'string':
      return constraints?.enum ?
        constraints.enum[0] :
        generateRandomString();

    case 'number':
      return constraints?.range ?
        getRandomNumber(constraints.range) :
        Math.random() * 100;

    case 'boolean':
      return Math.random() > 0.5;

    case 'array':
      return Array.from({ length: 3 }, (_, i) =>
        generateTestData(constraints?.itemType));

    case 'object':
      return generateObjectData(constraints?.properties);
  }
}
```

### 边界值生成

```typescript
function generateBoundaryValues(type: string): any[] {
  switch (type) {
    case 'number':
      return [0, 1, -1, Number.MAX_SAFE_INTEGER, Number.MIN_SAFE_INTEGER];

    case 'string':
      return ['', 'a', 'a'.repeat(255), 'a'.repeat(256)];

    case 'array':
      return [[], [1], Array.from({ length: 1000 })];
  }
}
```

## Mock生成策略

### 自动识别需要Mock的依赖

```typescript
function detectDependencies(ast: any): DependencyInfo[] {
  const dependencies: DependencyInfo[] = [];

  // 识别外部模块导入
  ast.body.forEach(node => {
    if (node.type === 'ImportDeclaration') {
      if (isExternalModule(node.source.value)) {
        dependencies.push({
          name: node.source.value,
          type: 'external',
          importedNames: extractImportedNames(node)
        });
      }
    }
  });

  return dependencies;
}
```

### Mock代码生成

```javascript
// Jest Mock生成
{{#each mocks}}
jest.mock('{{name}}', () => ({
  {{#each exported}}
  {{name}}: jest.fn(),
  {{/each}}
}));
{{/each}}

// 测试中的Mock使用
beforeEach(() => {
  {{#each mocks}}
  {{#each exported}}
  {{name}}.mockClear();
  {{/each}}
  {{/each}}
});
```

## 覆盖率优化

### 未覆盖代码检测

```typescript
function analyzeCoverage(code: string, tests: string): CoverageGap[] {
  const gaps: CoverageGap[] = [];

  // 分析代码分支
  const branches = extractBranches(code);

  // 检查每个分支是否有对应测试
  branches.forEach(branch => {
    if (!hasTestForBranch(branch, tests)) {
      gaps.push({
        type: 'branch',
        line: branch.line,
        condition: branch.condition,
        suggestion: generateTestSuggestion(branch)
      });
    }
  });

  return gaps;
}
```

### 自动生成补充测试

```javascript
// 基于覆盖率分析生成额外测试
function generateAdditionalTests(gaps: CoverageGap[]): string[] {
  return gaps.map(gap => {
    switch (gap.type) {
      case 'branch':
        return generateBranchTest(gap);
      case 'edge-case':
        return generateEdgeCaseTest(gap);
      default:
        return generateGeneralTest(gap);
    }
  });
}
```

## 最佳实践

### 1. 测试命名
- 使用描述性的测试名称
- 遵循 "should [expected behavior] when [condition]" 模式
- 避免使用数字编号

### 2. 测试结构
- 使用AAA模式（Arrange, Act, Assert）
- 每个测试只验证一个行为
- 保持测试简短和专注

### 3. 测试数据
- 使用工厂函数生成测试数据
- 避免硬编码的魔法数字
- 使用有意义的测试数据

### 4. Mock使用
- 只Mock外部依赖
- 避免过度Mock
- 验证Mock的调用

## 错误处理

### 常见错误及解决方案

1. **无法解析的代码**
   ```typescript
   if (parseError) {
     return {
       success: false,
       error: 'Unable to parse source code',
       suggestion: 'Check syntax and ensure file is valid'
     };
   }
   ```

2. **缺少类型信息**
   ```typescript
   if (!typeInfo) {
     console.warn(`No type info for ${functionName}, using generic tests`);
     return generateGenericTests(functionName);
   }
   ```

3. **循环依赖**
   ```typescript
   if (hasCircularDependency(dependencies)) {
     console.warn('Circular dependency detected, skipping some mocks');
     dependencies = resolveCircularDependencies(dependencies);
   }
   ```

## 性能优化

### 1. 增量测试生成
- 只生成新增或修改的函数的测试
- 缓存AST解析结果
- 重用已有的测试模板

### 2. 并行处理
- 并行分析多个文件
- 使用Web Worker处理大型文件
- 流式处理生成结果

### 3. 智能去重
- 识别相似的测试用例
- 合并重复的测试逻辑
- 优化测试数据生成