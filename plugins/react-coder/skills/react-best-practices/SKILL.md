---
name: react-best-practices
description: >-
  编写或修改 React 组件、Hooks、状态和数据请求时使用。
  用户提到 React、Hooks、useEffect、useState、组件重构时使用。
  已有技术栈和组件写法时沿用，不要另起一套。
---

# React

先看 `package.json` 和当前文件。类组件在用户没要求迁移时保持原样，不要改成函数组件。函数组件跟文件已有的写法。

依赖里没有的库不要新装。项目用 Redux、SWR、CSS Modules 或 Vite 时，不要改成 Zustand、TanStack Query、Tailwind 或 Next.js。

## 组件

一个组件做一件事。同一段逻辑在两处以上重复，或一个 effect 里做了几件不相干的事时，再抽自定义 Hook。不要因为文件超过某个行数就拆，也不要拆成容器组件和展示组件。

复用用 `children` 组合。props 要穿过很多层时，先把用到数据的组件挪到数据旁边。Context 只放主题、当前用户这类低频数据。会频繁变化的列表或表单状态不要放进 Context，否则子树会跟着重渲染。

## Hooks

只在组件或自定义 Hook 的顶层调用，不放在条件或循环里。

`useEffect`、`useMemo`、`useCallback` 的依赖数组按实际读取的值写全。依赖导致循环时，拆开副作用，或不要在渲染期间新建对象和函数。不要为了停掉循环而删掉依赖。

能在渲染时算出来的值，不要放进 effect 再 `setState`。

```tsx
// 由 props 推导的值在渲染期间计算
const fullName = `${user.firstName} ${user.lastName}`
```

## 数据请求

跟项目已有的请求方式。已经在用 TanStack Query 或 SWR 时，服务端数据放在那里，不要再复制进 Redux 或 Context。

必须在 effect 里请求时，丢掉过期响应，并在清理函数里中止。

```tsx
useEffect(() => {
  const controller = new AbortController()
  // userId 变化后，忽略上一次尚未返回的结果
  let ignore = false

  async function load() {
    const data = await getUser(userId, { signal: controller.signal })
    if (!ignore) setUser(data)
  }

  load()
  return () => {
    ignore = true
    controller.abort()
  }
}, [userId])
```

读 `window` 的逻辑放在客户端。Next.js 的 Server Component 不能调用 `useState` 和 `useEffect`。不要为了一处交互把整页标成 `"use client"`。

## 列表

列表项用稳定 id 做 `key`。只有列表静态且不会插入、删除或重排时，才用下标。

## 性能

先确认是渲染瓶颈，再加 `memo`、`useMemo`、`useCallback`。过滤、拼接这种便宜计算直接写。项目启用了 React Compiler 时，不要再手写这些缓存。

`memo` 包住的组件，不要每次接收新建的对象或回调。回调确实要稳定时，再用 `useCallback`。

路由和大块按需出现的界面用 `lazy` 与 `Suspense`。长列表在测量过卡顿之后，再用项目里已有的虚拟列表。

## 不要做的事

- 用 effect 把 props 同步进 state
- 一个 effect 里做几件不相干的事
- 依赖数组故意漏写
- 给每个函数套 `useCallback`，或给每个展示计算套 `useMemo`
