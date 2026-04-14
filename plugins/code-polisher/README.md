<h1 align="center">✨ Code Polisher Plugin</h1>

<p align="center">
  <strong>专业的代码优化工具，在保持功能不变的前提下，提供代码简化、优化和规范化处理</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Plugin-Claude_Code-blueviolet.svg" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
</p>

---

## 🚀 核心特性

- **功能等价 (Preserve Functionality)**：在优化过程中严防死守，绝不改变代码的业务逻辑，只重构“怎么写”。
- **规范对齐 (Apply Project Standards)**：深度集成项目定义的编码规范（如 `CLAUDE.md`, `GEMINI.md`），确保优化后的代码严丝合缝。
- **清晰度飞效 (Enhance Clarity)**：通过减少认知负荷、消除冗余逻辑，让代码像诗一样易读。
- **平衡之道 (Maintain Balance)**：拒绝极端的“单行代码主义”，在简洁性与可读性之间寻找最优解。
- **精准作用域 (Focus Scope)**：默认聚焦于最近修改或指定的代码片段，避免无关干扰。

## 🤖 智能代理 (Agents)

### `@code-polisher`
**代码润色专家**：专注于提升代码的清晰度、一致性和长期可维护性。

- **使用场景**：
  - ✨ 完成新功能开发后的收尾优化
  - 🛠️ 重构遗留的“屎山”或复杂逻辑
  - 📏 统一团队内部的代码风格与类型规范

- **交互示例**：
  > “帮我优化这段逻辑，提高它的可读性”
  > “这个函数嵌套太深了，能用更现代的方式重写吗？”

## 💡 最佳实践原则

Code Polisher 严格遵循以下工业级标准：
1. **函数定义**：优先使用 `function` 声明，确保更好的调试堆栈和提升（Hoisting）。
2. **显式类型**：顶层函数必须显式声明返回类型，拒绝隐式推断。
3. **组件规范**：React/Vue 组件必须显式定义 Props 或接口类型。
4. **拒绝嵌套**：严禁过度使用嵌套三元运算符，优先考虑早期返回（Early Return）。
5. **逻辑清晰**：多条件分支优先使用 `switch` 或结构清晰的 `if/else` 块。
