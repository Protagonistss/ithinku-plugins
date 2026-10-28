---
name: vue2-best-practices
description: >-
  维护 Vue 2 项目、修改 Options API 组件或 Vuex 时使用。
  用户提到 Vue 2、Options API、Vuex、mixin、过滤器、迁移到 Vue 3 时使用。
  Vue 3 项目用 vue3-best-practices。
---

# Vue 2

维护已有 Vue 2 工程。先看 `package.json` 里的 `vue` 版本，再改代码。Vue 3 项目用 `vue3-best-practices`。

用户没有要求迁移时，保持当前文件的写法，不要把 Options API 改成 `<script setup>`，也不要引入 Pinia 或 `features/` 目录。

## 版本

| 版本 | 可以做 | 不要做 |
|---|---|---|
| 2.6 及以下 | 继续 Options API。只有依赖里已经有 `@vue/composition-api` 时才用 `setup()` | `<script setup>`、`defineModel`、`defineOptions` |
| 2.7 | 内置 Composition API，可以用 `<script setup>`、`defineProps`、`defineEmits` | `defineModel`、`defineOptions`、`defineSlots` 这些 Vue 3.3+ 宏 |

2.6 的 Composition API 是插件，不是 Vue 自带的。不要在 2.7 的说明里写成「引入插件」。

## 组件

`data` 必须是函数。对象和数组类型的 prop 默认值用工厂函数，避免多个实例共享同一个引用。

`methods` 和生命周期钩子不要写成箭头函数，否则 `this` 不是组件实例。

不要直接修改 prop。父子通信用 props 向下、事件向上。不要新增 `new Vue()` 事件总线；跨组件状态放进已有的 Vuex。

选项顺序跟该文件已有的顺序。新组件用：`name`、`components`、`props`、`data`、`computed`、`watch`、生命周期、`methods`。

派生数据用 `computed`。`watch` 只用于要触发副作用的时候。

```javascript
props: {
  // 对象默认值必须是工厂函数，避免多个实例共享同一引用
  config: {
    type: Object,
    default: () => ({ theme: 'light' })
  }
}
```

## 逻辑复用

不要新增 mixin。纯逻辑抽成普通函数再导入。

需要带状态的复用时，用作用域插槽或无渲染组件。不要用高阶组件，也不要把状态放进一个普通对象的 `this` 上，那样模板不会更新。

已经存在的 mixin，改的时候在组件里注明来源。

## Vuex

模块使用 `namespaced: true`，`state` 写成工厂函数。mutation 保持同步，异步放在 action 里。开发环境可以开 `strict`。

`mapState`、`mapGetters`、`mapActions` 可用可不用，命名空间字符串要和模块名一致。

```javascript
export default {
  namespaced: true,
  // state 用工厂函数，避免模块间共享状态
  state: () => ({ user: null }),
  getters: {
    isLoggedIn: (state) => state.user !== null
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
    }
  },
  actions: {
    async login({ commit }, credentials) {
      const user = await authService.login(credentials)
      commit('SET_USER', user)
    }
  }
}
```

## 面向 Vue 3 时停止新增

只在用户要做迁移准备时处理。不要借机重写整个组件。

- 过滤器。Vue 3 已移除，改成方法或 computed
- 实例上的 `$on`、`$off`、`$once`，以及 `$listeners`。Vue 3 里监听器并进 `$attrs`
- `inline-template`
- 继续往 `Vue.prototype` 上挂方法。Vue 3 用 `app.config.globalProperties`
