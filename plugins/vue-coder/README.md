# Vue Coder Plugin

这是一个专为 Vue.js 开发者设计的 Claude 插件，旨在提供高质量的代码生成和最佳实践指导。

## 功能特性

本插件支持 Vue 2 和 Vue 3 双版本，针对不同的开发场景提供定制化建议：

*   **Vue 3 (默认推荐)**: 专注于 Composition API, `<script setup>`, TypeScript, Pinia 和 Vite。
*   **Vue 2 (维护模式)**: 专注于 Options API, Vuex 和遗留代码维护。

## 包含的技能

### 1. Vue 3 Best Practices
涵盖现代 Vue 开发的核心原则：
*   组件化思维与逻辑复用
*   响应式系统深度解析
*   Pinia 状态管理
*   VueUse 工具库集成

### 2. Vue 2 Best Practices
涵盖传统 Vue 开发模式：
*   Options API 规范
*   Mixins 的陷阱与替代方案
*   Vuex 模块化设计

## 使用方法

在对话中，Claude 会根据您的代码上下文自动匹配合适的 Vue 版本建议。您也可以显式指定：

*   "使用 Vue 3 写一个用户列表组件"
*   "重构这个 Vue 2 组件"
