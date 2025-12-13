# Command: /gen

快速生成常用代码模板和样板代码的命令。

## 描述

/gen 命令帮助开发者快速生成各种常用的代码模板，提高开发效率，减少重复劳动。

## 用法

```
/gen <type> [options]
```

### 支持的代码类型

- `api` - REST API 端点
- `model` - 数据模型/实体类
- `test` - 单元测试
- `component` - UI 组件
- `crud` - CRUD 操作
- `middleware` - 中间件
- `config` - 配置文件

## 示例

### 生成 REST API 端点

```
/gen api User
```

生成：
```javascript
// routes/user.js
const express = require('express');
const router = express.Router();

// GET /api/users
router.get('/', async (req, res) => {
  try {
    // TODO: 实现获取用户列表逻辑
    res.json({ success: true, data: [] });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// GET /api/users/:id
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    // TODO: 实现获取单个用户逻辑
    res.json({ success: true, data: null });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// POST /api/users
router.post('/', async (req, res) => {
  try {
    const userData = req.body;
    // TODO: 实现创建用户逻辑
    res.status(201).json({ success: true, data: userData });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// PUT /api/users/:id
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const userData = req.body;
    // TODO: 实现更新用户逻辑
    res.json({ success: true, data: userData });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// DELETE /api/users/:id
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    // TODO: 实现删除用户逻辑
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

module.exports = router;
```

### 生成数据模型

```
/gen model Product name:string price:number description:text
```

生成：
```javascript
// models/Product.js
class Product {
  constructor(data) {
    this.id = data.id || null;
    this.name = data.name || '';
    this.price = data.price || 0;
    this.description = data.description || '';
    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
  }

  validate() {
    if (!this.name) {
      throw new Error('Name is required');
    }
    if (this.price < 0) {
      throw new Error('Price must be non-negative');
    }
    return true;
  }

  toJSON() {
    return {
      id: this.id,
      name: this.name,
      price: this.price,
      description: this.description,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt
    };
  }
}

module.exports = Product;
```

### 生成测试文件

```
/gen test UserService
```

**专业测试生成模式**

如果检测到您已安装 `test-generator` 插件，系统会提示是否使用专业模式：

```
检测到 test-generator 插件，是否使用专业测试生成模式？
[Y] 是 - 使用专业测试插件
[N] 否 - 使用基础测试生成
```

**使用专业模式的优势：**
- 支持更多测试框架（Jest、Vitest、Pytest、JUnit等）
- 自动生成Mock数据和Stub函数
- 智能边界值和错误场景测试
- 测试覆盖率分析和优化建议

**直接调用专业测试插件：**
```bash
# 生成带Mock的测试
/gen test src/api/userService.js --mock

# 使用特定框架
/gen test src/components/Button.jsx --framework vitest

# 分析覆盖率并补充测试
/gen test src/utils/validator.js --coverage
```

**基础测试生成**（未安装专业插件时）：

生成：
```javascript
// tests/UserService.test.js
const { describe, it, expect, beforeEach, afterEach } = require('@jest/globals');
const UserService = require('../services/UserService');

describe('UserService', () => {
  let userService;

  beforeEach(() => {
    userService = new UserService();
  });

  afterEach(() => {
    // 清理
  });

  describe('创建用户', () => {
    it('应该成功创建用户', async () => {
      const userData = {
        name: 'Test User',
        email: 'test@example.com'
      };

      const result = await userService.create(userData);

      expect(result).toBeDefined();
      expect(result.name).toBe(userData.name);
      expect(result.email).toBe(userData.email);
    });

    it('应该验证必填字段', async () => {
      const userData = {};

      await expect(
        userService.create(userData)
      ).rejects.toThrow();
    });
  });

  describe('获取用户', () => {
    it('应该返回用户列表', async () => {
      const users = await userService.findAll();

      expect(Array.isArray(users)).toBe(true);
    });

    it('应该根据ID获取用户', async () => {
      const userId = 1;

      const user = await userService.findById(userId);

      expect(user).toBeDefined();
      expect(user.id).toBe(userId);
    });
  });

  describe('更新用户', () => {
    it('应该成功更新用户', async () => {
      const userId = 1;
      const updateData = { name: 'Updated Name' };

      const result = await userService.update(userId, updateData);

      expect(result.name).toBe(updateData.name);
    });
  });

  describe('删除用户', () => {
    it('应该成功删除用户', async () => {
      const userId = 1;

      const result = await userService.delete(userId);

      expect(result).toBe(true);
    });
  });
});
```

### 生成 React 组件

```
/gen component Button
```

生成：
```javascript
// components/Button.jsx
import React from 'react';
import PropTypes from 'prop-types';
import './Button.css';

const Button = ({ 
  children, 
  onClick, 
  variant = 'primary',
  size = 'medium',
  disabled = false,
  className = ''
}) => {
  const buttonClass = `button button--${variant} button--${size} ${className}`;

  return (
    <button
      className={buttonClass}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

Button.propTypes = {
  children: PropTypes.node.isRequired,
  onClick: PropTypes.func,
  variant: PropTypes.oneOf(['primary', 'secondary', 'danger']),
  size: PropTypes.oneOf(['small', 'medium', 'large']),
  disabled: PropTypes.bool,
  className: PropTypes.string
};

export default Button;
```

## 高级用法

### 指定编程语言

```
/gen api User --lang python
/gen model Product --lang typescript
```

### 自定义模板

```
/gen api User --template rest-advanced
```

## 特性

- 🚀 快速生成常用代码
- 📝 遵循最佳实践
- 🔧 支持多种语言和框架
- ✨ 代码格式规范
- 📚 包含注释和文档

## 支持的语言

- JavaScript / Node.js
- TypeScript
- Python
- Java
- Go
- Rust

## 注意事项

- 生成的代码是起点，需要根据实际需求调整
- 包含 TODO 注释标记需要实现的逻辑
- 遵循项目现有的代码风格

## 相关命令

- `/refactor` - 重构现有代码
- `/optimize` - 性能优化

### 代码审查相关

> **注意**：代码审查功能已迁移到独立的 [code-review 插件](../../code-review/)，提供以下命令：
> - `/review` - 全面代码审查
> - `/security` - 安全专项检查
> - `/performance` - 性能分析

