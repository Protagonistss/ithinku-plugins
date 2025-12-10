# 单元测试生成命令

为指定的文件、函数或类生成单元测试用例。

## 使用方法

```bash
/test <target> [options]
```

### 参数

- `target`: 测试目标，可以是：
  - 文件路径：`src/utils/calculator.js`
  - 函数名：`calculator.add`
  - 类名：`Calculator`
  - 组件路径：`src/components/Button.jsx`

### 选项

- `--framework, -f`: 指定测试框架
  - `vitest` (默认) - JavaScript/TypeScript (Vite项目)
  - `jest` - JavaScript/TypeScript
  - `mocha` - JavaScript/TypeScript
  - `pytest` - Python
  - `unittest` - Python
  - `junit` - Java
  - `testng` - Java

- `--output, -o`: 指定输出文件路径（默认：自动检测）
- `--mock, -m`: 自动生成Mock数据和Stub
- `--coverage, -c`: 生成测试覆盖率分析并补充缺失的测试
- `--update, -u`: 更新现有测试文件（而不是创建新文件）
- `--skip-setup, -s`: 跳过测试设置和导入语句的生成
- `--describe, -d`: 为每个测试用例添加详细的描述

## 示例

```bash
# 为文件生成Jest测试
/test src/utils/calculator.js

# 使用Vitest框架生成测试
/test src/components/Button.jsx --framework vitest

# 为Python文件生成pytest测试
/test utils/calculator.py --framework pytest

# 生成包含Mock数据的测试
/test src/api/userService.js --mock

# 分析测试覆盖率并补充测试
/test src/utils/validator.js --coverage

# 更新现有测试文件
/test src/utils/calculator.js --update
```

## 工作流程

1. **分析目标代码**
   - 解析函数签名和类结构
   - 识别依赖关系和外部模块
   - 分析分支逻辑和边界条件

2. **生成测试场景**
   - 正常流程测试
   - 边界条件测试
   - 异常情况测试
   - 参数验证测试

3. **创建测试文件**
   - 根据选择的框架生成相应格式的测试代码
   - 包含必要的导入和设置
   - 生成具有描述性的测试名称

4. **优化和格式化**
   - 格式化生成的代码
   - 添加必要的注释
   - 确保代码符合最佳实践

## 输出示例

### JavaScript/Jest示例

```javascript
// 测试目标：src/utils/calculator.js
export class Calculator {
  add(a, b) {
    return a + b;
  }

  divide(a, b) {
    if (b === 0) {
      throw new Error('Division by zero');
    }
    return a / b;
  }
}

// 生成的测试：src/utils/calculator.test.js
import { Calculator } from './calculator';

describe('Calculator', () => {
  let calculator;

  beforeEach(() => {
    calculator = new Calculator();
  });

  describe('add', () => {
    it('should return sum of two positive numbers', () => {
      expect(calculator.add(2, 3)).toBe(5);
    });

    it('should return sum of negative numbers', () => {
      expect(calculator.add(-2, -3)).toBe(-5);
    });

    it('should handle zero values', () => {
      expect(calculator.add(0, 5)).toBe(5);
      expect(calculator.add(5, 0)).toBe(5);
    });
  });

  describe('divide', () => {
    it('should return division result', () => {
      expect(calculator.divide(10, 2)).toBe(5);
    });

    it('should throw error when dividing by zero', () => {
      expect(() => calculator.divide(10, 0)).toThrow('Division by zero');
    });
  });
});
```

### Python/pytest示例

```python
# 测试目标：utils/calculator.py
class Calculator:
    def add(self, a, b):
        return a + b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Division by zero")
        return a / b

# 生成的测试：tests/test_calculator.py
import pytest
from utils.calculator import Calculator

class TestCalculator:
    def setup_method(self):
        self.calculator = Calculator()

    def test_add_positive_numbers(self):
        assert self.calculator.add(2, 3) == 5

    def test_add_negative_numbers(self):
        assert self.calculator.add(-2, -3) == -5

    def test_add_with_zero(self):
        assert self.calculator.add(0, 5) == 5
        assert self.calculator.add(5, 0) == 5

    def test_divide(self):
        assert self.calculator.divide(10, 2) == 5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Division by zero"):
            self.calculator.divide(10, 0)
```

## 提示

- 建议在项目根目录使用相对路径
- 使用 `--coverage` 选项可以确保测试覆盖率高
- 对于异步函数，会自动生成相应的异步测试
- 生成的Mock数据会尽量使用真实但安全的示例值

## 相关命令

- `/mock` - 专门生成Mock数据和Stub
- `/coverage` - 分析测试覆盖率
- @test-expert - 与测试专家代理交互获得更详细的指导