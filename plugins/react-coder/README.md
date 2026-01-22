# React Coder Plugin

专业的 React 代码生成与优化工具，旨在帮助开发者编写高质量、可维护且符合最佳实践的 React 代码。

## 功能特性

- **组件生成与重构**: 智能生成功能组件，支持将复杂组件拆分为更小、更专注的子组件。
- **Hooks 深度集成**: 提供自定义 Hooks 提取建议，确保遵循 Rules of Hooks。
- **最佳实践指导**: 涵盖组件设计、状态管理、性能优化及反模式审查。
- **性能优化**: 识别不必要的重渲染，提供 `useMemo`、`useCallback` 及 `React.memo` 的使用建议。
- **现代技术栈**: 深度支持 Next.js (App Router)、Tailwind CSS、Zustand、TanStack Query 等主流工具。

## 核心技能

### 🎨 React Best Practices（技能名：react-best-practices）

该技能是 React Coder 的核心，专注于提升代码的可维护性和扩展性。

**主要原则**:
- **单一职责**: 组件应专注于单一功能。
- **组合优于继承**: 善用 `children` 和 Render Props。
- **状态提升**: 将状态保留在最近的共同祖先中。
- **关注点分离**: 区分展示组件与逻辑组件（Hooks 模式下）。

## 使用场景

### 1. 优化组件性能
识别并修复由于状态更新导致的大规模重渲染问题。
> "优化这个组件的渲染性能，检查是否有不必要的重渲染。"

### 2. 重构为自定义 Hooks
将组件内部复杂的业务逻辑提取出来，提高复用性。
> "将这个组件中的数据获取和表单逻辑提取为单独的自定义 Hooks。"

### 3. 代码审查
根据最佳实践审查现有代码。
> "检查这段代码是否违反了 React 最佳实践，特别是 useEffect 的依赖和状态管理方面。"

### 4. 生成新组件
根据需求描述生成符合规范的 React 组件。
> "创建一个支持搜索和分页的列表组件，使用 Tailwind CSS 样式。"

## 推荐技术栈

- **构建工具**: Vite / Next.js
- **状态管理**: Zustand (客户端) / TanStack Query (服务端)
- **样式**: Tailwind CSS
- **表单**: React Hook Form + Zod
- **测试**: Vitest + React Testing Library

## 最佳实践规范 (部分)

- ❌ 避免超过 200 行的巨型组件。
- ❌ 避免层层传递 props（Prop Drilling > 3层）。
- ❌ 避免在 `useEffect` 中处理衍生状态。
- ✅ 诚实填写 Hooks 的依赖数组。
- ✅ 使用 `React.lazy` 和 `Suspense` 进行代码分割。
