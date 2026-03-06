---
name: vue2-best-practices
description: Vue 2 维护与开发最佳实践指南，涵盖 Options API, Vuex 及向 Vue 3 迁移的准备。
disable-model-invocation: false
---

# Vue 2 Best Practices (Legacy & Maintenance)

## 🌟 技能核心：稳定维护与平滑过渡
本技能旨在指导开发者维护现有的 Vue 2 项目，编写**清晰、可预测**的 Options API 代码，并为未来迁移到 Vue 3 做准备。
**核心原则**：规范化 Options API、谨慎使用 Mixins、组件解耦。

## 🧠 Core Principles (核心原则)

### 1. Options API 规范
- **Order of Options**: 遵循一致的选项顺序：
    1. `name`
    2. `components`
    3. `props`
    4. `data`
    5. `computed`
    6. `watch`
    7. `lifecycle hooks` (created, mounted, etc.)
    8. `methods`
- **Data Function**: `data` 必须始终是一个返回对象的函数，防止组件实例间状态污染。
- **Props Validation**: 始终为 props 定义详细的类型验证和默认值。

### 2. 逻辑复用 (Logic Reuse)
- **Mixins**:
    - **警告**: 尽量减少 Mixins 的使用。它们会导致命名冲突和隐式依赖，使代码难以理解。
    - **替代**: 如果必须复用逻辑，考虑使用 HOC (Higher Order Components) 或 Scoped Slots (作用域插槽)。
    - **规范**: 如果使用 Mixin，必须加上明确的前缀，并在组件注释中说明来源。
- **Utility Functions**: 将纯逻辑提取为独立的 JS 文件导入使用。

### 3. 组件通信
- **Event Bus**:
    - **警告**: 避免滥用全局 Event Bus (`new Vue()`) 进行通信，这会导致事件流难以追踪。
    - **替代**: 使用 Vuex 或 Props/Events 进行父子通信。
- **Props Down, Events Up**: 严格遵守单向数据流原则。不要直接修改 prop。

## 🧩 状态管理 (Vuex)
- **Vuex 3**:
    - **Modules**: 始终使用 Namespaced Modules (`namespaced: true`) 来组织 Store。
    - **MapHelpers**: 使用 `mapState`, `mapGetters`, `mapActions` 简化组件内的调用。
    - **Mutations**: 必须是同步的。异步逻辑放在 Actions 中。
    - **Strict Mode**: 在开发环境开启严格模式，确保状态只能通过 mutations 修改。

## 🚫 反模式 (Anti-Patterns)
- ❌ **Arrow Functions in Methods**: 不要在 `methods` 或生命周期钩子中使用箭头函数，这会导致 `this` 指向错误。
- ❌ **Direct DOM Manipulation**: 避免使用 jQuery 或直接操作 DOM，始终通过数据驱动视图。如果必须操作，使用 `ref`。
- ❌ **Over-reliance on Watchers**: 优先使用 `computed` 属性来处理派生数据，而不是滥用 `watch`。
- ❌ **Implicit Global Variables**: 避免直接在 `Vue.prototype` 上挂载过多全局变量。

## 🔄 迁移准备 (Migration Readiness)
- **Avoid Deprecated Features**: 停止使用即将在 Vue 3 移除的特性（如 Filters, Inline Templates, `$listeners`）。
- **Composition API Plugin**: 在 Vue 2.7+ 中，尝试引入 Composition API (`<script setup>`)，以便逐步过渡到 Vue 3 的写法。

## 📝 代码示例

### 1. 规范的 Options API 组件

```vue
<template>
  <div class="user-card">
    <h3>{{ formattedName }}</h3>
    <p>{{ user.email }}</p>
    <button @click="handleEdit">编辑</button>
  </div>
</template>

<script>
// ✅ 遵循选项顺序规范
export default {
  name: 'UserCard', // 1. name

  components: { // 2. components
    EditButton
  },

  props: { // 3. props - 带类型验证
    user: {
      type: Object,
      required: true,
      validator: (value) => ['id', 'name', 'email'].every(key => key in value)
    }
  },

  data() { // 4. data - 必须是函数
    return {
      isEditing: false
    }
  },

  computed: { // 5. computed
    formattedName() {
      return this.user.name.toUpperCase()
    }
  },

  watch: { // 6. watch
    'user.id': {
      handler(newId) {
        this.fetchUserData(newId)
      },
      immediate: true
    }
  },

  created() { // 7. 生命周期钩子
    this.initializeComponent()
  },

  mounted() {
    this.setupEventListeners()
  },

  methods: { // 8. methods - 避免箭头函数
    handleEdit() {
      this.$emit('edit', this.user.id)
    },

    fetchUserData(id) {
      // 数据获取逻辑
    },

    initializeComponent() {
      // 初始化逻辑
    },

    setupEventListeners() {
      // 事件监听
    }
  }
}
</script>
```

### 2. Vuex 模块化 Store

```javascript
// store/modules/user.js
// ✅ 使用命名空间模块
export default {
  namespaced: true,

  state: () => ({
    user: null,
    token: null,
    loading: false
  }),

  getters: {
    isLoggedIn: state => !!state.token,
    displayName: state => state.user?.name ?? '访客'
  },

  // Mutations 必须是同步的
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_TOKEN(state, token) {
      state.token = token
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    }
  },

  // Actions 处理异步逻辑
  actions: {
    async login({ commit }, credentials) {
      commit('SET_LOADING', true)
      try {
        const { user, token } = await authService.login(credentials)
        commit('SET_USER', user)
        commit('SET_TOKEN', token)
        return { success: true }
      } catch (error) {
        return { success: false, error: error.message }
      } finally {
        commit('SET_LOADING', false)
      }
    },

    logout({ commit }) {
      commit('SET_USER', null)
      commit('SET_TOKEN', null)
    }
  }
}
```

```vue
<!-- 组件中使用 Vuex -->
<template>
  <div v-if="isLoggedIn">
    <p>欢迎, {{ displayName }}</p>
    <button @click="logout">退出</button>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  name: 'UserStatus',

  computed: {
    // ✅ 使用 map 辅助函数
    ...mapState('user', ['loading']),
    ...mapGetters('user', ['isLoggedIn', 'displayName'])
  },

  methods: {
    ...mapActions('user', ['logout'])
  }
}
</script>
```

### 3. 避免 Mixin，使用工具函数

```javascript
// ❌ 避免 Mixin
const userMixin = {
  data() {
    return { user: null }
  },
  methods: {
    fetchUser() { /* ... */ }
  }
}

// ✅ 使用工具函数
// utils/user.js
export function createUserService() {
  return {
    user: null,
    async fetchUser(id) {
      this.user = await api.getUser(id)
      return this.user
    }
  }
}

// 组件中使用
import { createUserService } from '@/utils/user'

export default {
  data() {
    return {
      userService: createUserService()
    }
  },
  async created() {
    await this.userService.fetchUser(this.userId)
  }
}
```

### 4. Props 验证最佳实践

```vue
<script>
export default {
  props: {
    // ✅ 基础类型验证
    title: String,

    // ✅ 多种可能的类型
    value: [String, Number],

    // ✅ 必填字段
    userId: {
      type: [String, Number],
      required: true
    },

    // ✅ 带默认值
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    },

    // ✅ 对象/数组默认值使用工厂函数
    config: {
      type: Object,
      default: () => ({
        theme: 'light',
        locale: 'zh-CN'
      })
    },

    // ✅ 自定义验证
    email: {
      type: String,
      validator: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
    }
  }
}
</script>
```

### 5. Vue 2.7+ Composition API 迁移准备

```vue
<template>
  <div>
    <p>计数: {{ count }}</p>
    <button @click="increment">+1</button>
  </div>
</template>

<script>
// Vue 2.7+ 可以使用 Composition API
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'Counter',

  // ✅ 渐进式迁移：setup 函数
  setup() {
    const count = ref(0)
    const doubled = computed(() => count.value * 2)

    function increment() {
      count.value++
    }

    onMounted(() => {
      console.log('Counter mounted')
    })

    return {
      count,
      doubled,
      increment
    }
  }
}
</script>
```

## 🎨 常用指令示例
```bash
# 规范化 Options 顺序
/vue-coder 重新排列这个组件的选项顺序，使其符合最佳实践。

# 移除 Mixin
/vue-coder 分析这个组件使用的 Mixin，尝试将其重构为普通的函数导入或 HOC。

# Vuex 模块化
/vue-coder 将这个庞大的 Vuex store 拆分为独立的命名空间模块。
```
