---
name: code-analysis
description: 代码质量与复杂度等静态分析能力，提供改进建议与报告。
disable-model-invocation: false
---

# Skill: Code Analysis

专业的代码分析技能，能够深入评估代码质量、识别潜在问题并提供改进建议。

## 技能描述

Code Analysis 技能提供全面的代码静态分析能力，包括代码质量评估、复杂度分析、代码重复检测和最佳实践检查。

## 核心功能

### 1. 代码质量评估
- **可读性分析**: 评估代码的清晰度和易理解性
- **命名规范**: 检查变量、函数、类的命名是否合理
- **代码结构**: 分析代码组织和模块化程度
- **注释质量**: 评估注释的完整性和有效性

### 2. 复杂度分析
- **圈复杂度**: 计算代码的线性独立路径数量
- **认知复杂度**: 评估代码理解的难易程度
- **嵌套深度**: 检查代码的嵌套层级
- **函数长度**: 分析函数的行数和职责

### 3. 代码重复检测
- **重复代码**: 识别相似的代码片段
- **复制粘贴**: 检测可能的复制粘贴代码
- **重构机会**: 建议将重复代码提取为函数

### 4. 最佳实践检查
- **设计模式**: 识别和评估设计模式的使用
- **SOLID原则**: 检查是否违反SOLID原则
- **错误处理**: 评估异常处理的完整性
- **资源管理**: 检查资源的正确释放

## 支持的语言

- **JavaScript/TypeScript**: ES6+、Node.js、React、Vue
- **Python**: Python 3.x、Django、Flask
- **Java**: Java 8+、Spring Boot
- **C#**: .NET Core、ASP.NET
- **Go**: 标准库和常用框架
- **Ruby**: Ruby on Rails
- **PHP**: Laravel、Symfony

## 使用方法

```bash
# 分析单个文件
/code-analysis src/components/UserProfile.jsx

# 分析整个目录
/code-analysis src/services/ --depth deep

# 生成分析报告
/code-analysis src/ --format report --output analysis-report.md

# 专注特定问题类型
/code-analysis src/utils/calculator.js --focus complexity
```

## 分析维度

### 功能性
- [ ] 逻辑正确性
- [ ] 边界条件处理
- [ ] 异常情况处理
- [ ] 业务逻辑实现

### 可维护性
- [ ] 代码模块化
- [ ] 耦合度评估
- [ ] 内聚性检查
- [ ] 扩展性分析

### 可测试性
- [ ] 单元测试友好度
- [ ] 依赖注入使用
- [ ] Mock对象支持
- [ ] 测试覆盖建议

### 性能
- [ ] 算法效率
- [ ] 内存使用
- [ ] I/O操作优化
- [ ] 并发安全性

## 质量评分系统

### 评分维度（每项10分）

1. **可读性 (Readability)**
   - 9-10分: 代码如文档般清晰
   - 7-8分: 整体清晰，少数地方需要注释
   - 5-6分: 基本可读，需要改进命名和结构
   - 3-4分: 难以理解，需要大量注释
   - 1-2分: 几乎无法理解

2. **复杂性 (Complexity)**
   - 9-10分: 结构简单，易于理解
   - 7-8分: 适中复杂度，逻辑清晰
   - 5-6分: 偏复杂，部分逻辑需要重构
   - 3-4分: 过于复杂，难以维护
   - 1-2分: 极度复杂，必须重构

3. **可维护性 (Maintainability)**
   - 9-10分: 易于修改和扩展
   - 7-8分: 较易维护，改动影响可控
   - 5-6分: 维护有一定难度
   - 3-4分: 难以维护，改动风险大
   - 1-2分: 几乎无法维护

4. **健壮性 (Robustness)**
   - 9-10分: 异常处理完善
   - 7-8分: 主要异常有处理
   - 5-6分: 基本异常处理
   - 3-4分: 异常处理不足
   - 1-2分: 几乎没有异常处理

## 分析报告模板

```markdown
# 代码分析报告

## 基本信息
- **文件路径**: src/components/UserProfile.jsx
- **语言**: JavaScript/React
- **代码行数**: 245行
- **函数数量**: 8个
- **分析时间**: 2024-01-15 14:30:00

## 质量评分
| 维度 | 评分 | 说明 |
|-----|------|------|
| 可读性 | 7.5/10 | 整体清晰，部分变量名需要改进 |
| 复杂性 | 6.0/10 | 函数较长，嵌套较深 |
| 可维护性 | 6.5/10 | 耦合度适中，需要更好的模块化 |
| 健壮性 | 5.0/10 | 缺少边界条件处理 |

## 详细分析

### 🟢 优秀实践
1. 使用了现代ES6+语法
2. 组件结构清晰
3. Props类型定义完整

### 🟡 需要改进
1. 函数过长（第45-120行，75行）
2. 嵌套层级过深（最深4层）
3. 部分变量名不够描述性

### 🔴 严重问题
1. 缺少错误边界处理
2. 内存泄漏风险（事件监听器未清理）

## 改进建议

### 1. 重构长函数
将 `handleUserUpdate` 函数拆分为多个小函数：
```javascript
// 当前代码（75行）
const handleUserUpdate = async (userData) => {
  // 75行复杂逻辑...
};

// 建议重构为
const validateUserData = (data) => { /* 验证逻辑 */ };
const prepareUpdateData = (data) => { /* 数据准备 */ };
const updateUserProfile = async (data) => { /* 更新逻辑 */ };
const handleUpdateSuccess = (result) => { /* 成功处理 */ };
const handleUpdateError = (error) => { /* 错误处理 */ };

const handleUserUpdate = async (userData) => {
  try {
    validateUserData(userData);
    const updateData = prepareUpdateData(userData);
    const result = await updateUserProfile(updateData);
    handleUpdateSuccess(result);
  } catch (error) {
    handleUpdateError(error);
  }
};
```

### 2. 降低嵌套复杂度
使用早期返回减少嵌套：
```javascript
// 改进前
const processUser = (user) => {
  if (user) {
    if (user.active) {
      if (user.verified) {
        // 处理逻辑
      }
    }
  }
};

// 改进后
const processUser = (user) => {
  if (!user) return;
  if (!user.active) return;
  if (!user.verified) return;

  // 处理逻辑
};
```

## 学习资源
- [Clean Code - Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350884)
- [Refactoring - Martin Fowler](https://refactoring.com/)
- [JavaScript最佳实践](https://github.com/ryanmcdermott/clean-code-javascript)
```

## 配置选项

可以通过 `.code-analysis.json` 配置分析规则：

```json
{
  "analysis": {
    "maxFunctionLength": 30,
    "maxNestingDepth": 3,
    "maxComplexity": 10,
    "excludePatterns": [
      "*.test.js",
      "*.spec.js",
      "node_modules/**",
      "dist/**"
    ],
    "rules": {
      "naming": {
        "enabled": true,
        "camelCase": true,
        "snake_case": false
      },
      "complexity": {
        "enabled": true,
        "maxCognitiveComplexity": 15
      },
      "duplicates": {
        "enabled": true,
        "minLines": 5,
        "similarity": 0.8
      }
    }
  }
}
```

## 集成工具

### IDE插件
- **SonarLint**: 实时代码质量检查
- **ESLint**: JavaScript代码质量工具
- **Pylint**: Python代码分析
- **Checkstyle**: Java代码风格检查

### CI/CD集成
```yaml
# GitHub Actions 示例
name: Code Analysis
on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Code Analysis
        run: |
          npm install
          npm run lint
          npm run test:coverage
          npx sonar-scanner
```

## 高级特性

### 1. 代码异味检测
- **长方法**: 超过50行的方法
- **大类**: 超过300行的类
- **长参数列表**: 超过5个参数
- **重复代码**: 相似度超过80%的代码片段

### 2. 架构分析
- **循环依赖**: 检测模块间的循环引用
- **层级违反**: 分析架构层次结构
- **耦合分析**: 评估模块间耦合度

### 3. 演进分析
- **代码变更频率**: 分析代码的稳定性
- **缺陷密度**: 关联代码变更和bug报告
- **技术债务**: 量化技术债务水平

## 最佳实践

### 开发阶段
1. **编码前**: 设计清晰的代码结构
2. **编码中**: 遵循编码规范和最佳实践
3. **编码后**: 进行自我代码审查
4. **提交前**: 运行自动化分析工具

### 团队协作
1. **统一标准**: 建立团队统一的编码规范
2. **定期审查**: 进行定期的代码审查会议
3. **知识分享**: 分享代码质量改进经验
4. **持续改进**: 根据分析结果改进开发流程

## 使用建议

1. **渐进式改进**: 不需要一次性修复所有问题
2. **优先级排序**: 优先修复严重和高优先级问题
3. **自动化集成**: 将分析工具集成到开发流程中
4. **持续监控**: 定期检查代码质量趋势

通过持续的代码分析和改进，可以显著提升代码质量，降低维护成本，提高开发效率。
