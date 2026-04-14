<h1 align="center">✨ Vue Coder Plugin</h1>

<p align="center">
  <strong>专为 Vue.js 开发者打造的智能编程助手，支持 Vue 2/3 全版本最佳实践</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Plugin-Claude_Code-blueviolet.svg" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
</p>

---

## 🚀 核心特性

本插件深度适配 Vue 生态系统，针对不同版本提供定制化的架构建议与代码生成：

*   **Vue 3 (默认推荐)**：全面拥抱 **Composition API**、`<script setup>`、TypeScript 强类型支持、Pinia 状态管理及 Vite 构建工具。
*   **Vue 2 (维护模式)**：针对遗留系统提供 **Options API** 规范化建议、Vuex 模块化重构以及 Mixins 的现代化替代方案。

## 🛠️ 包含技能 (Skills)

### 1. Vue 3 Best Practices
涵盖现代 Vue 开发的核心原则：
*   **逻辑复用**：智能提取 Composables，告别面条代码。
*   **响应式原理**：深度解析 `ref` vs `reactive` 的使用边界。
*   **生态集成**：完美适配 Vue Router 4 和 VueUse 工具库。

### 2. Vue 2 Best Practices
专注于传统模式的优化与迁移：
*   **组件规范**：Options API 的属性排序与逻辑归类。
*   **性能调优**：识别不必要的 Watcher 与计算属性瓶颈。
*   **向后兼容**：提供平滑迁移至 Vue 3 的过渡代码建议。

## 📖 使用指南

在对话中，Claude 会根据您的项目上下文（如 `package.json` 中的版本）自动切换策略。您也可以显式触发：

> “使用 Vue 3 的 Script Setup 语法写一个通用的表单校验组件。”
> “将这个复杂的 Vue 2 Mixin 重构为更易维护的 Vue 3 Composable。”
> “帮我检查这个组件是否符合 Vue 3 的响应式最佳实践。”

## 📦 推荐技术栈

| 领域 | 推荐方案 |
|------|----------|
| **构建/开发** | Vite |
| **状态管理** | Pinia (Vue 3) / Vuex 4 (Vue 2) |
| **路由** | Vue Router |
| **工具库** | VueUse |
| **测试** | Vitest + Vue Test Utils |
