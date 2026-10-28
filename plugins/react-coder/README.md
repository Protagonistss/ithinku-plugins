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

- **沿用现有写法**：类组件和现有状态库、样式方案保持不动。依赖里没有的库不新装。
- **Hooks**：逻辑重复或 effect 混了多件不相干的事时再抽取。依赖数组按实际读取的值写全。
- **数据请求**：跟项目已有方式。在 effect 里请求时丢掉过期响应。
- **性能**：先确认渲染瓶颈，再考虑 `memo`、`useMemo`、`useCallback`。启用 React Compiler 时不手写这些缓存。

## 🛠️ 核心技能

### `🎨 React Best Practices`
本技能是 React Coder 的灵魂，贯穿于每一个代码生成与评审环节。

- **组件**：用 `children` 组合。不要按行数拆分，也不要拆成容器组件和展示组件。
- **状态**：Context 只放低频数据。服务端数据留在项目已有的请求库里。

## 📖 使用场景

### 改现有组件
> “改一下这个用户资料组件。”技能保持现有的类组件或状态库，只修正 effect 依赖、过期请求和派生状态。

### 数据请求
> “这个详情会在 id 切换后显示上一个人的数据。”技能补上过期响应的丢弃，不为此换一套请求库。

## 📦 技术栈

框架、状态、样式、表单和测试都跟仓库现有依赖。项目里没有 Zustand、TanStack Query、Tailwind 或 Next.js 时，不要为了这个插件新增它们。
