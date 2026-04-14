<h1 align="center">✨ React Coder Plugin</h1>

<p align="center">
  <strong>专业的 React 代码生成与重构专家，助力编写高性能、可维护的现代 React 架构</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Plugin-Claude_Code-blueviolet.svg" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
</p>

---

## 🚀 核心特性

- **原子化组件生成**：遵循“单一职责”原则，生成高度解耦、专注且易于测试的功能组件。
- **Hooks 深度提取**：自动识别组件内的复杂业务逻辑，智能提取为语义化的自定义 Hooks（Custom Hooks）。
- **性能瓶颈诊断**：精准定位不必要的重渲染，提供 `useMemo`, `useCallback` 及 `React.memo` 的最佳应用时机。
- **现代生态集成**：深度支持 Next.js (App Router)、Tailwind CSS、Zustand、TanStack Query 及 Shadcn UI 等主流技术栈。
- **最佳实践审计**：基于 React 官方最新文档与社区共识，自动审查 useEffect 依赖、闭包陷阱等反模式。

## 🛠️ 核心技能

### `🎨 React Best Practices`
本技能是 React Coder 的灵魂，贯穿于每一个代码生成与评审环节。

- **组件设计模式**：组合优于继承（Composition vs Inheritance）、高阶组件拆解。
- **状态管理策略**：状态提升（Lifting State Up）与 Context API 的合理边界。
- **逻辑与展示分离**：在 Hooks 模式下完美实践容器/展示模式（Container/Presenter Pattern）。

## 📖 使用场景

### ⚡ 性能优化
> “优化这个组件的渲染性能，检查是否有不必要的重渲染隐患。”

### 🏗️ 架构重构
> “将这个庞大的 UserProfile 组件拆分成多个子组件，并将数据请求逻辑提取到单独的 Hook 中。”

### ✅ 规范审查
> “检查这段代码是否符合现代 React 开发规范，特别是状态同步和 Effect 处理方面。”

### ✨ 组件生成
> “使用 Tailwind CSS 生成一个响应式的仪表盘侧边栏组件，支持多级折叠和当前状态高亮。”

## 📦 推荐技术栈

| 类别 | 推荐方案 |
|------|----------|
| **框架/构建** | Vite / Next.js (App Router) |
| **状态管理** | Zustand (Client) / TanStack Query (Server) |
| **样式方案** | Tailwind CSS / Headless UI |
| **表单校验** | React Hook Form + Zod |
| **单元测试** | Vitest + React Testing Library |
