---
name: vue3-best-practices
description: >-
  使用 Vue 3 编写或修改组件、Composable、Pinia store 时使用。
  用户提到 Vue 3、Composition API、script setup、Pinia、defineProps、defineEmits、defineModel、Composable 时使用。
  Vue 2 项目用 vue2-best-practices。
---

# Vue 3

Vue 3 项目。Vue 2 用 `vue2-best-practices`。`defineModel`、`defineOptions`、`defineSlots` 不要写进 Vue 2.6，也不要写进 Vue 2.7。

## 目录

先沿用仓库里已有的目录。没有约定时，按项目类型选一种，不要套用唯一模板。

| 项目类型 | 默认倾向 |
|---|---|
| 多特性中后台 | `features/<能力>/` 收拢该能力的接口、状态、页面和类型。路由、布局、文案、应用级状态留在壳层 |
| 组件库、设计系统 | 按组件分目录，另配示例。不设业务路由，也不设 `features/` |
| 内容站、营销页 | 少量页面。Nuxt 项目跟 `pages/`、`server/` |
| 小型单页 | `App.vue` 和少量组件，不再加一层特性目录 |
| 已有工程 | 保持现有目录，包括 Vue 2 的 `views/` 与 Vuex 模块 |

下文示例里的导入路径只说明写法。落文件时按上表和仓库现状决定，不要照搬示例路径。

命名跟仓库现有风格。没有约定时：组件 PascalCase，Composable 用 `use` 前缀，store 用 `useXxxStore`。

## 组件

默认 `<script setup lang="ts">`。导入方式跟仓库现有代码：已有自动导入就不要再手写一遍 `import { ref } from 'vue'`。

顶层 `await` 会使组件变成异步组件，父级需要 `Suspense`。

### Props

Vue 3.5+ 可以解构 props，默认值写在解构上：

```typescript
const { title, count = 0 } = defineProps<{
  title: string
  count?: number
}>()
```

3.4 及以下用 `withDefaults`，或一直通过 `props.xxx` 访问。更早版本里解构 props 会失去响应性。响应式解构也可以用编译选项 `propsDestructure: true` 打开。

不要直接修改 prop。

### Emits、v-model、插槽与暴露

```typescript
const emit = defineEmits<{
  change: [id: number]
}>()

// Vue 3.4+。带名字的 v-model 用第一个参数区分
const modelValue = defineModel<string>()
const count = defineModel<number>('count', { default: 0 })

defineSlots<{
  default: (props: { item: Item }) => unknown
}>()

// 只暴露父组件需要调用的方法
defineExpose({
  focus: () => inputRef.value?.focus()
})
```

### 泛型组件

`generic` 需要 Vue 3.3+。

```vue
<script setup lang="ts" generic="T extends { id: number }">
defineProps<{
  items: T[]
  selected?: T
}>()
</script>
```

### 组件名与属性透传

`script setup` 默认用文件名作为组件名。下面两种情况再写 `defineOptions({ name })`（Vue 3.3+）：

- `KeepAlive` 的 `include` / `exclude` 要对上这个名字
- 模板里用的标签名和文件名不一致，包括递归引用

属性要落到内部某个节点、而不是组件根上时：

```vue
<script setup lang="ts">
// 仓库没有自动导入时才写这行
import { useAttrs } from 'vue'

defineOptions({ inheritAttrs: false })
const attrs = useAttrs()
</script>

<template>
  <input v-bind="attrs" />
</template>
```

`examples/component-example.vue` 的文件名不是 `TreeNode.vue`，模板里的递归标签才需要 `defineOptions({ name: 'TreeNode' })`。文件名已经对上时不要再写一遍。

## 响应式

| 场景 | 用 |
|---|---|
| 基本类型、可空值、需要整个替换的对象 | `ref` |
| 一组不会整个替换、也不会被解构的字段 | `reactive` |
| 图表、地图这类大型外部实例 | `shallowRef` |

`reactive` 对象解构后不再是响应式，要用 `toRefs`。这和 Vue 3.5 的 props 解构不是同一件事。

模板里 ref 会自动解包，`<script>` 里要写 `.value`。

## Composable

以 `use` 开头，返回 ref 和函数，里面不要用 `this`。已有 VueUse 能完成的不要再手写一份。

参数可能是值、ref 或 getter 时，用 `toValue`（Vue 3.3+）。更早版本用 `unref`，或只接收 `Ref`。

分页示例见 `examples/composable-example.ts`。

## Pinia

优先 Setup Store，和组件一样用 `ref` / `computed` / 函数。状态保持扁平，getter 用 `computed`，异步放在函数里。

```typescript
export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const isLoggedIn = computed(() => user.value !== null)

  async function login(credentials: LoginDTO) {
    user.value = await api.login(credentials)
  }

  return { user, isLoggedIn, login }
})
```

更完整的示例见 `examples/store-example.ts`。落文件时跟仓库已有的 store 目录，不要照搬示例文件名。

## 从 Options API 迁移

新组件不要再写 Options API。改旧组件时整份换掉，不要在同一个组件里两套状态各写一半。用户没有要求迁移时，不要改 Vue 2 文件。

| Options API | Composition API |
|---|---|
| `data()` | `ref()` / `reactive()` |
| `computed` | `computed()` |
| `methods` | 普通函数 |
| `watch` | `watch()` / `watchEffect()` |
| `created` | `<script setup>` 顶层 |
| `mounted` | `onMounted()` |
| `this.xxx` | 直接访问变量 |
| mixin | composable |

## 性能

先确认是渲染瓶颈，再加优化。

- 大列表用 `v-memo`，依赖项只放真正影响这行输出的值
- 重组件用路由懒加载或 `defineAsyncComponent`
- `KeepAlive` 只包需要保留状态的页面，`include` 依赖组件名
