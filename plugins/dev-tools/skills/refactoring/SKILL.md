# Skill: 代码重构

这个技能使代理能够识别重构机会并提供系统化的重构方案。

## 技能描述

代码重构技能使代理能够：
- 识别需要重构的代码
- 提供重构步骤和方案
- 确保重构安全性
- 应用重构模式
- 改善代码设计

## 重构原则

### 1. 小步快跑

每次重构改动要小，频繁提交：
- ✅ 每次只做一个重构
- ✅ 保持测试通过
- ✅ 频繁提交
- ✅ 可以随时回滚

### 2. 测试保护

重构前后功能不变：
- ✅ 重构前有测试
- ✅ 重构过程中测试通过
- ✅ 重构后添加新测试

### 3. 渐进改进

不追求一步到位：
- ✅ 逐步改善
- ✅ 持续重构
- ✅ 保持简单

## 常用重构技巧

### 1. 提取函数（Extract Function）

**时机**：函数过长、代码重复、注释解释代码

**重构前**：
```javascript
function printOwing(invoice) {
  printBanner();
  
  // 计算未付金额
  let outstanding = 0;
  for (const order of invoice.orders) {
    outstanding += order.amount;
  }
  
  // 打印详情
  console.log(`客户：${invoice.customer}`);
  console.log(`未付金额：${outstanding}`);
}
```

**重构后**：
```javascript
function printOwing(invoice) {
  printBanner();
  const outstanding = calculateOutstanding(invoice);
  printDetails(invoice, outstanding);
}

function calculateOutstanding(invoice) {
  let result = 0;
  for (const order of invoice.orders) {
    result += order.amount;
  }
  return result;
}

function printDetails(invoice, outstanding) {
  console.log(`客户：${invoice.customer}`);
  console.log(`未付金额：${outstanding}`);
}
```

### 2. 内联函数（Inline Function）

**时机**：函数体比函数名更清晰

**重构前**：
```javascript
function getRating(driver) {
  return moreThanFiveLateDeliveries(driver) ? 2 : 1;
}

function moreThanFiveLateDeliveries(driver) {
  return driver.numberOfLateDeliveries > 5;
}
```

**重构后**：
```javascript
function getRating(driver) {
  return driver.numberOfLateDeliveries > 5 ? 2 : 1;
}
```

### 3. 提取变量（Extract Variable）

**时机**：表达式难以理解

**重构前**：
```javascript
function price(order) {
  return order.quantity * order.itemPrice -
    Math.max(0, order.quantity - 500) * order.itemPrice * 0.05 +
    Math.min(order.quantity * order.itemPrice * 0.1, 100);
}
```

**重构后**：
```javascript
function price(order) {
  const basePrice = order.quantity * order.itemPrice;
  const quantityDiscount = Math.max(0, order.quantity - 500) * order.itemPrice * 0.05;
  const shipping = Math.min(basePrice * 0.1, 100);
  return basePrice - quantityDiscount + shipping;
}
```

### 4. 引入参数对象（Introduce Parameter Object）

**时机**：一组参数总是一起出现

**重构前**：
```javascript
function amountInvoiced(startDate, endDate) { }
function amountReceived(startDate, endDate) { }
function amountOverdue(startDate, endDate) { }
```

**重构后**：
```javascript
class DateRange {
  constructor(startDate, endDate) {
    this.startDate = startDate;
    this.endDate = endDate;
  }
}

function amountInvoiced(dateRange) { }
function amountReceived(dateRange) { }
function amountOverdue(dateRange) { }
```

### 5. 以多态取代条件表达式（Replace Conditional with Polymorphism）

**重构前**：
```javascript
function getSpeed(bird) {
  switch (bird.type) {
    case 'European':
      return getEuropeanSpeed(bird);
    case 'African':
      return getAfricanSpeed(bird);
    case 'Norwegian':
      return getNorwegianSpeed(bird);
    default:
      throw new Error('Unknown bird');
  }
}
```

**重构后**：
```javascript
class Bird {
  getSpeed() {
    throw new Error('Must be implemented by subclass');
  }
}

class EuropeanBird extends Bird {
  getSpeed() {
    // 欧洲燕的速度计算
  }
}

class AfricanBird extends Bird {
  getSpeed() {
    // 非洲燕的速度计算
  }
}

class NorwegianBird extends Bird {
  getSpeed() {
    // 挪威燕的速度计算
  }
}

function getSpeed(bird) {
  return bird.getSpeed();
}
```

### 6. 拆分循环（Split Loop）

**重构前**：
```javascript
let youngest = people[0] ? people[0].age : Infinity;
let totalSalary = 0;

for (const person of people) {
  if (person.age < youngest) youngest = person.age;
  totalSalary += person.salary;
}

return { youngest, totalSalary };
```

**重构后**：
```javascript
function youngestAge() {
  let youngest = people[0] ? people[0].age : Infinity;
  for (const person of people) {
    if (person.age < youngest) youngest = person.age;
  }
  return youngest;
}

function totalSalary() {
  let total = 0;
  for (const person of people) {
    total += person.salary;
  }
  return total;
}

return {
  youngest: youngestAge(),
  totalSalary: totalSalary()
};
```

### 7. 移除死代码（Remove Dead Code）

**重构前**：
```javascript
function example() {
  doSomething();
  
  // 这段代码已经不用了
  // if (oldFeature) {
  //   doOldThing();
  // }
  
  doAnotherThing();
}
```

**重构后**：
```javascript
function example() {
  doSomething();
  doAnotherThing();
}
```

## 重构流程

### 第一步：识别坏味道

```
1. 代码审查
   - 人工审查
   - 静态分析工具
   - 代码度量

2. 问题分类
   - 命名问题
   - 结构问题
   - 设计问题

3. 优先级排序
   - 影响程度
   - 修复难度
   - 风险评估
```

### 第二步：制定计划

```
1. 选择重构技巧
   - 匹配问题类型
   - 考虑代码规模
   - 评估风险

2. 拆分步骤
   - 小步重构
   - 定义检查点
   - 准备回滚

3. 准备测试
   - 现有测试
   - 补充测试
   - 集成测试
```

### 第三步：执行重构

```
1. 运行测试
   - 确保测试通过
   - 记录基准

2. 应用重构
   - 一次一个改动
   - 频繁运行测试
   - 及时提交

3. 验证结果
   - 测试通过
   - 功能正常
   - 性能无退化
```

### 第四步：清理优化

```
1. 代码清理
   - 移除注释
   - 统一格式
   - 更新文档

2. 性能检查
   - 基准测试
   - 性能对比
   - 优化瓶颈

3. 团队评审
   - Code Review
   - 知识分享
   - 经验总结
```

## 重构模式

### 模式 1：逐步提取

适用：大函数拆分

```
步骤1：识别代码块
步骤2：提取第一个函数
步骤3：测试
步骤4：提交
步骤5：重复 2-4
```

### 模式 2：平行重构

适用：接口变更

```
步骤1：创建新接口
步骤2：新旧接口并存
步骤3：逐步迁移调用方
步骤4：所有调用方迁移完成
步骤5：删除旧接口
```

### 模式 3：分支抽象

适用：大规模重构

```
步骤1：创建特性分支
步骤2：在分支上重构
步骤3：保持分支同步主干
步骤4：通过测试
步骤5：合并回主干
```

## 重构检查清单

### 重构前
- [ ] 有充分的测试覆盖
- [ ] 所有测试通过
- [ ] 代码已提交
- [ ] 明确重构目标
- [ ] 评估风险和影响

### 重构中
- [ ] 每次改动都很小
- [ ] 频繁运行测试
- [ ] 保持测试通过
- [ ] 及时提交代码
- [ ] 可以随时回滚

### 重构后
- [ ] 所有测试通过
- [ ] 功能没有变化
- [ ] 代码更清晰
- [ ] 更新了文档
- [ ] 团队已评审

## 安全重构技巧

### 1. 使用 IDE 重构功能

现代 IDE 提供安全的重构：
- 重命名（Rename）
- 提取方法（Extract Method）
- 移动（Move）
- 内联（Inline）

### 2. 频繁运行测试

重构时持续运行测试：
```bash
# 监视文件变化，自动运行测试
npm run test:watch
```

### 3. 小步提交

每完成一个小重构就提交：
```bash
git add .
git commit -m "refactor: 提取 calculateTotal 函数"
```

### 4. 结对编程

两人一起重构：
- 一人重构，一人审查
- 降低出错风险
- 知识共享

## 常见误区

❌ **一次重构太多**
- 问题：改动大，风险高
- 正确：小步重构，逐步改进

❌ **没有测试就重构**
- 问题：无法验证正确性
- 正确：先补充测试

❌ **重构时添加新功能**
- 问题：混淆目的，容易出错
- 正确：重构和新功能分开

❌ **过度重构**
- 问题：浪费时间，收益递减
- 正确：适可而止，聚焦问题

## 集成说明

这个技能会被以下代理使用：
- Architect - 架构级重构方案
- CodeReviewer (通过 code-review 插件) - 提供重构建议

> **注意**：CodeReviewer 功能已迁移到独立的 [code-review 插件](../../code-review/)，提供更专业的代码审查和重构建议。

## 版本历史

- v1.0.0 - 初始版本，支持常用重构技巧

