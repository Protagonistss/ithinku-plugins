---
name: vue3-best-practices
description: Vue 3 开发最佳实践指南，涵盖 Composition API, Setup Script, Pinia 及 TypeScript 集成。
---

# Vue 3 Best Practices

## 🌟 技能核心：拥抱组合式 API
本技能旨在指导开发者编写**模块化、类型安全、高性能**的 Vue 3 应用。
**核心原则**：Composition API First、逻辑复用、类型推导、单一数据流。

## 🧠 Core Principles (核心原则)

### 1. Script Setup 与 Composition API
- **Script Setup**: 默认使用 `<script setup lang="ts">`。它更简洁，运行时性能更好，IDE 支持更佳。
- **Top-Level Await**: 可以在 `<script setup>` 顶层直接使用 `await`。
- **Explicit Imports**: 显式导入 `ref`, `computed`, `watch` 等，虽然自动导入工具存在，但显式导入更利于代码阅读和依赖追踪。

### 2. 响应式数据 (Reactivity)
- **ref vs reactive**:
    - **优先使用 `ref`**: 适用于基本类型和对象，能够清晰地区分响应式变量（`.value`）。
    - **谨慎使用 `reactive`**: 解构会丢失响应性（除非使用 `toRefs`）。仅在处理深层嵌套且不解构的大对象时考虑使用。
- **Unwrapping**: 在 template 中 `ref` 会自动解包，但在 `<script>` 中必须访问 `.value`。

### 3. 组件通信 (Component Communication)
- **Props**: 使用 `defineProps` 声明 props，配合 TypeScript 接口定义类型。
    ```typescript
    const props = defineProps<{
      title: string;
      count?: number;
    }>();
    ```
- **Emits**: 使用 `defineEmits` 声明事件，确保类型安全。
    ```typescript
    const emit = defineEmits<{
      (e: 'change', id: number): void;
      (e: 'update', value: string): void;
    }>();
    ```
- **v-model**: 使用 `defineModel` (Vue 3.4+) 简化双向绑定。

### 4. 逻辑复用 (Composables)
- **Use Composables**: 替代 Mixins。将业务逻辑提取为 `useSomething` 函数。
- **Naming Convention**: 以 `use` 开头，返回一个包含响应式状态和方法的对象。
- **VueUse**: 优先检查 VueUse 库中是否已有现成的工具函数，避免重复造轮子。

## 🧩 状态管理 (State Management)
- **Pinia**: 这里的标准选择。
    - **Setup Store**: 偏好 Setup Stores (`defineStore('id', () => { ... })`) 而非 Option Stores，因为它与组件内的写法一致。
    - **Flat State**: 保持 State 扁平化，避免过度嵌套。
    - **Getters**: 等同于 computed 属性。
    - **Actions**: 处理同步和异步逻辑。

## 🚫 反模式 (Anti-Patterns)
- ❌ **Mixins**: 在 Vue 3 中完全禁止使用 Mixins。它们导致命名冲突和来源不明确。
- ❌ **Destructuring Props**: 直接解构 `props` 会导致响应性丢失。使用 `toRefs(props)` 或直接访问 `props.propName`（或 Vue 3.5+ 的响应式解构）。
- ❌ **Lifecycle Hooks in Setup**: 避免在 setup 中写 `created` 逻辑（setup 本身就是 created）。直接写在 setup 函数体内的代码即为初始化代码。
- ❌ **Ignoring .value**: 忘记在 script 中加 `.value` 是新手最常见的错误。

## ⚡ 性能优化 (Performance)
- **v-memo**: 对大型列表或表格行使用 `v-memo` 跳过不必要的更新。
- **Lazy Loading**: 路由组件懒加载 `() => import('./Component.vue')`。
- **KeepAlive**: 缓存非活跃组件实例。
- **ShallowRef**: 对于不需要深度响应的大型数据结构（如地图实例、图表实例），使用 `shallowRef`。

## 🛠️ 技术栈推荐
- **Build Tool**: Vite.
- **Router**: Vue Router 4.
- **State**: Pinia.
- **UI Lib**: Element Plus / Ant Design Vue / Naive UI / Tailwind CSS.
- **Testing**: Vitest + Vue Test Utils.

## 🎨 常用指令示例
```bash
# 生成 Composable
/vue-coder 提取这段逻辑为一个名为 usePagination 的 Composable 函数。

# 转换 Options API 为 Composition API
/vue-coder 将这个 Vue 2 的 Options API 组件重构为 Vue 3 的 <script setup lang="ts"> 写法。

# 优化响应式数据
/vue-coder 检查这段代码中 reactive 的使用是否合理，是否建议改为 ref。
```
