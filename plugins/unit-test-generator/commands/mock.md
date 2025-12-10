# Mock数据生成命令

专门用于生成测试所需的Mock数据和Stub函数，帮助隔离测试环境。

## 使用方法

```bash
/mock <target> [options]
```

### 参数

- `target`: Mock目标，可以是：
  - 模块路径：`src/api/userService`
  - 包名：`axios`
  - 数据库模块：`src/db/models`

### 选项

- `--type, -t`: Mock类型
  - `full` - 完整Mock（默认）
  - `partial` - 部分Mock
  - `spy` - Spy模式（保留原始实现）

- `--framework, -f`: 指定测试框架
  - `vitest` (默认)
  - `jest`
  - `mocha`

- `--output, -o`: 输出文件路径
- `--methods, -m`: 指定要Mock的方法（逗号分隔）
- `--return, -r`: 指定返回值模式
  - `default` - 默认值
  - `random` - 随机值
  - `custom` - 自定义值

## 示例

```bash
# 为整个API模块生成Mock
/mock src/api/userService

# 为特定方法生成Mock
/mock src/utils/httpClient --methods get,post

# 生成随机返回值的Mock
/mock src/db/models --type partial --return random

# 使用Vitest风格生成Mock
/mock src/api/userService --framework vitest
```

## Mock生成示例

### Jest Mock示例

```javascript
// 生成的Mock文件：src/api/userService.mock.js
import { UserGenerator } from '../test-generators/data';

export const userServiceMock = {
  getUser: jest.fn(),
  createUser: jest.fn(),
  updateUser: jest.fn(),
  deleteUser: jest.fn(),
  findAll: jest.fn()
};

// 默认返回值设置
userServiceMock.getUser.mockReturnValue(UserGenerator.generate());
userServiceMock.createUser.mockImplementation(async (userData) => {
  return UserGenerator.generate(userData);
});
userServiceMock.findAll.mockResolvedValue(UserGenerator.generateList(5));
```

### Vitest Mock示例

```typescript
// 生成的Mock文件：src/api/userService.mock.ts
import { vi } from 'vitest';
import { UserGenerator } from '../test-generators/data';

export const userServiceMock = {
  getUser: vi.fn(),
  createUser: vi.fn(),
  updateUser: vi.fn(),
  deleteUser: vi.fn(),
  findAll: vi.fn()
};

// 设置默认行为
userServiceMock.getUser.mockReturnValue(UserGenerator.generate());
userServiceMock.createUser.mockResolvedValue(UserGenerator.generate());
```

## Mock数据类型

### 基础类型Mock

```javascript
// 字符串Mock
mockString.mockReturnValue('test-string');
mockString.mockReturnValueOnce('specific-value');

// 数字Mock
mockNumber.mockReturnValue(42);
mockNumber.mockReturnValue(Math.random() * 100);

// 布尔Mock
mockBoolean.mockReturnValue(true);
mockBoolean.mockReturnValue(false);

// 数组Mock
mockArray.mockReturnValue([1, 2, 3]);
mockArray.mockImplementation(() => Array.from({ length: 5 }, (_, i) => i));
```

### 对象Mock

```javascript
// 用户对象Mock
const userMock = {
  id: 1,
  name: 'Test User',
  email: 'test@example.com',
  createdAt: new Date()
};

// 动态对象Mock
const dynamicMock = {
  ...userMock,
  id: Math.floor(Math.random() * 1000),
  name: generateRandomName()
};
```

### API响应Mock

```javascript
// 成功响应
mockApi.mockResolvedValue({
  success: true,
  data: UserGenerator.generateList(10),
  pagination: {
    page: 1,
    total: 100
  }
});

// 错误响应
mockApi.mockRejectedValue(new Error('API Error'));

// 网络错误
mockApi.mockRejectedValue({
  code: 'NETWORK_ERROR',
  message: 'Network timeout'
});
```

## 高级功能

### 条件Mock

```javascript
// 根据参数返回不同值
mockFunction.mockImplementation((id) => {
  if (id === 999) {
    return null; // 未找到
  }
  return UserGenerator.generate({ id });
});

// 异步条件Mock
mockAsyncFunction.mockImplementation(async (type) => {
  switch (type) {
    case 'success':
      return { status: 'ok' };
    case 'error':
      throw new Error('Failed');
    default:
      return { status: 'unknown' };
  }
});
```

### 序列化Mock

```javascript
// 多次调用返回不同值
mockFunction
  .mockReturnValueOnce('first')
  .mockReturnValueOnce('second')
  .mockReturnValue('default');

// 多次Promise
mockAsyncFunction
  .mockResolvedValueOnce('first success')
  .mockRejectedValueOnce(new Error('first error'))
  .mockResolvedValue('default success');
```

### Spy Mock

```javascript
// 保留原始实现但记录调用
const originalFunction = require('./module').function;
const spy = jest.spyOn(module, 'function');

// 验证调用
expect(spy).toHaveBeenCalled();
expect(spy).toHaveBeenCalledWith(expectedArgs);
```

## Mock最佳实践

### 1. 命名规范
- 使用描述性的Mock名称
- 保持Mock文件组织清晰
- 使用统一的命名约定

### 2. 重用策略
- 创建可重用的Mock工厂
- 使用基础Mock并扩展
- 保持Mock数据一致性

### 3. 维护性
- 定期更新Mock数据
- 保持Mock与真实API同步
- 清理未使用的Mock

### 4. 测试隔离
- 在每个测试后重置Mock
- 避免Mock之间的依赖
- 使用独立的Mock实例

## 相关命令

- `/test` - 生成测试用例（自动包含Mock）
- `/coverage` - 分析测试覆盖率
- @test-expert - 获取Mock设计建议