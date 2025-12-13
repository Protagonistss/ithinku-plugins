# Test Generator Plugin

专业的单元测试生成工具，支持多种编程语言和测试框架。能够智能分析代码并生成高质量的测试用例。

## 功能特性

### 🎯 核心功能
- **智能代码分析**：自动解析函数、类和模块结构
- **多语言支持**：JavaScript/TypeScript、Python、Java
- **多测试框架**：Jest、Vitest、Mocha、Pytest、JUnit等
- **自动Mock生成**：智能识别并生成Mock数据和Stub函数

### 🔍 高级特性
- **边界值测试**：自动生成边界条件测试用例
- **错误场景覆盖**：包含异常和错误处理测试
- **测试覆盖率分析**：识别未覆盖的代码路径
- **测试数据生成**：生成真实且安全的测试数据

## 安装

1. 确保已安装 Claude Code
2. 克隆或下载本插件到 Claude 插件目录
3. 重启 Claude Code 以加载插件

## 快速开始

### 基础使用

```bash
# 为JavaScript文件生成Jest测试
/test src/utils/calculator.js

# 为Python文件生成pytest测试
/test utils/calculator.py --framework pytest

# 使用Vitest框架生成测试
/test src/components/Button.jsx --framework vitest
```

### 高级功能

```bash
# 生成包含Mock数据的测试
/test src/api/userService.js --mock

# 分析测试覆盖率并补充缺失测试
/test src/utils/validator.js --coverage

# 更新现有测试文件
/test src/utils/calculator.js --update
```

## 命令参考

### /test

生成单元测试的主要命令。

**语法**：
```bash
/test <target> [options]
```

**参数**：
- `target`: 文件路径、函数名或类名

**选项**：
- `--framework, -f`: 测试框架 (jest, vitest, mocha, pytest, junit等)
- `--output, -o`: 指定输出路径
- `--mock, -m`: 自动生成Mock数据
- `--coverage, -c`: 分析测试覆盖率
- `--update, -u`: 更新现有测试
- `--describe, -d`: 添加详细描述

### /mock

专门生成Mock数据和Stub函数。

**语法**：
```bash
/mock <module> [options]
```

### /coverage

分析测试覆盖率并生成补充测试。

**语法**：
```bash
/coverage <target> [options]
```

## 支持的语言和框架

### JavaScript/TypeScript
- **测试框架**：Jest, Vitest, Mocha, Jasmine
- **Mock库**：jest.mock, vi.mock, sinon
- **断言库**：expect, chai, should

### Python
- **测试框架**：pytest, unittest, nose2
- **Mock库**：unittest.mock, pytest-mock
- **断言**：assert, pytest.raises

### Java
- **测试框架**：JUnit 5, TestNG, Spock
- **Mock库**：Mockito, PowerMock
- **断言**：Assertions, AssertJ

## 使用示例

### JavaScript/TypeScript 示例

```javascript
// 源代码：src/calculator.js
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

// 生成的测试：src/calculator.test.js
import { Calculator } from './calculator';

describe('Calculator', () => {
  let calculator;

  beforeEach(() => {
    calculator = new Calculator();
  });

  describe('add', () => {
    it('should return sum of two numbers', () => {
      expect(calculator.add(2, 3)).toBe(5);
    });

    it('should handle negative numbers', () => {
      expect(calculator.add(-2, -3)).toBe(-5);
    });

    it('should handle zero', () => {
      expect(calculator.add(0, 5)).toBe(5);
    });
  });

  describe('divide', () => {
    it('should return division result', () => {
      expect(calculator.divide(10, 2)).toBe(5);
    });

    it('should throw error for division by zero', () => {
      expect(() => calculator.divide(10, 0)).toThrow('Division by zero');
    });
  });
});
```

### Python 示例

```python
# 源代码：calculator.py
class Calculator:
    def add(self, a, b):
        return a + b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Division by zero")
        return a / b

# 生成的测试：test_calculator.py
import pytest
from calculator import Calculator

class TestCalculator:
    def setup_method(self):
        self.calculator = Calculator()

    def test_add_positive_numbers(self):
        assert self.calculator.add(2, 3) == 5

    def test_add_negative_numbers(self):
        assert self.calculator.add(-2, -3) == -5

    def test_divide(self):
        assert self.calculator.divide(10, 2) == 5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Division by zero"):
            self.calculator.divide(10, 0)
```

## 配置选项

### 项目级配置

创建 `test-generator.config.json` 在项目根目录：

```json
{
  "framework": "jest",
  "outputDir": "tests",
  "testPattern": "**/*.test.{js,ts}",
  "mockPattern": "**/*.mock.{js,ts}",
  "generateMocks": true,
  "coverageThreshold": 80,
  "customTemplates": {
    "beforeEach": "// Custom setup code",
    "afterEach": "// Custom cleanup code"
  }
}
```

### 全局配置

在用户配置目录创建 `test-generator.json`：

```json
{
  "defaultFramework": "jest",
  "autoDetectFramework": true,
  "promptForMocks": true,
  "generateDescriptions": true,
  "preferredAssertionStyle": "expect"
}
```

## 与其他插件集成

### 与 dev-tools 集成

当安装了 dev-tools 插件时，可以使用 `/gen test` 命令自动调用测试生成功能：

```bash
# 在 dev-tools 中使用
/gen test src/utils/calculator.js

# 检测到测试插件后，会提示使用专业模式
检测到 test-generator 插件，是否使用专业测试生成模式？
```

### 与 code-review 集成

code-review 插件可以分析测试覆盖率并提供改进建议：

```bash
# 代码审查时会自动检查测试覆盖
/review src/components/UserProfile.jsx

# 输出包含测试覆盖率信息
⚠️  UserProfile 组件缺少错误处理的测试
建议：添加对 loading 状态和错误状态的测试用例
```

## 最佳实践

### 1. 测试命名
- 使用描述性的测试名称
- 遵循 "should [behavior] when [condition]" 模式

### 2. 测试结构
- 使用 AAA 模式（Arrange, Act, Assert）
- 每个测试验证一个行为
- 保持测试简短和专注

### 3. Mock 使用
- 只 Mock 外部依赖
- 避免过度 Mock
- 验证 Mock 调用

### 4. 测试数据
- 使用工厂函数生成数据
- 保持数据一致性
- 避免魔法数字

## 故障排除

### 常见问题

**Q: 生成的测试无法运行？**
A: 检查测试框架是否正确安装，确保导入路径正确。

**Q: Mock 不工作？**
A: 确保在测试文件顶部正确配置 Mock，检查 Mock 路径。

**Q: 生成的测试覆盖率高但质量低？**
A: 使用 `--describe` 选项添加更详细的测试描述，手动调整测试逻辑。

### 调试模式

```bash
# 启用详细输出
/test src/utils/calculator.js --verbose

# 查看生成的 AST
/test src/utils/calculator.js --debug-ast

# 保存中间结果
/test src/utils/calculator.js --save-intermediate
```

## 贡献

欢迎贡献代码！请查看 [贡献指南](CONTRIBUTING.md) 了解详情。

### 开发环境设置

1. 克隆仓库
2. 安装依赖：`npm install`
3. 运行测试：`npm test`
4. 构建插件：`npm run build`

## 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情。

## 更新日志

### v1.0.0 (2024-01-09)
- 初始版本发布
- 支持 JavaScript/TypeScript、Python、Java
- 集成 Jest、Vitest、Pytest、JUnit 框架
- 添加智能 Mock 生成功能

## 支持

- 📖 [文档](https://github.com/Protagonisths/claude-plugins/tree/main/plugins/test-generator)
- 🐛 [问题反馈](https://github.com/Protagonisths/claude-plugins/issues)
- 💬 [讨论区](https://github.com/Protagonisths/claude-plugins/discussions)
- 📧 [邮件支持](mailto:support@protagonisths.com)

---

Made with ❤️ by [Protagonisths](https://github.com/Protagonisths)