<h1 align="center">✨ Test Generator Plugin</h1>

<p align="center">
  <strong>专业的单元测试自动化专家，智能分析代码逻辑并生成高覆盖率的测试用例</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Plugin-Claude_Code-blueviolet.svg" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
</p>

---

## 🚀 核心特性

### 🎯 自动化生产力
- **智能架构分析**：深度解析函数调用链、类继承关系及模块依赖，生成结构化的测试套件。
- **全自动 Mock**：精准识别网络请求、数据库操作及第三方库，自动生成语义化的 Mock 数据与 Stub 桩函数。
- **覆盖率驱动**：智能扫描未触达的代码路径，自动补全条件分支与异常处理的测试场景。

### 🔍 工业级深度
- **边界值探测**：自动针对 `null`, `undefined`, 空集合及数值极限等边界条件设计用例。
- **异步逻辑支持**：完美处理 Promise, async/await 及定时器等异步场景的测试同步。
- **数据驱动测试**：支持生成符合业务逻辑的伪造数据（Faker 数据），确保测试贴近真实场景。

## 🛠️ 包含技能 (Skills)

| 技能 | 核心能力 |
|------|----------|
| **[Test Gen](./skills/test-generation/SKILL.md)** | 基础用例生成、异步逻辑测试、多框架适配 |
| **[Mock Gen](./skills/mock-generation/SKILL.md)** | API 模拟、第三方模块 Mock、依赖注入替换 |
| **[Assertion](./skills/assertion-helper/SKILL.md)** | 语义化断言建议、复杂对象深度对比 |

## 📖 快速指令

在 Claude Code 终端中输入以下指令即可快速开启测试之旅：

| 常用命令 | 描述 | 示例 |
|------|------|------|
| `/test` | 为指定文件生成单元测试 | `/test src/utils/auth.ts` |
| `/mock` | 仅生成 Mock 数据或工厂函数 | `/mock src/api/user.ts` |
| `/coverage` | 分析覆盖率并补充缺失用例 | `/coverage src/core/engine.js` |

## 📦 支持框架

- **JavaScript / TS**：Jest, Vitest, Mocha, Jasmine
- **Python**：Pytest, Unittest
- **Java**：JUnit 5, TestNG
- **Go**：Testing (Built-in), Ginkgo
