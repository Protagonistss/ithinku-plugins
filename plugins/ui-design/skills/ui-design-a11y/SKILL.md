---
name: ui-design-a11y
description: >-
  检查或修复无障碍问题时使用。
  用户提到无障碍、a11y、WCAG、键盘导航、屏幕阅读器、对比度、ARIA、焦点时使用。
  视觉风格用 ui-design-core。大胆配色和动效也要满足这里的对比度与减弱动效。
---

# Accessibility

按 WCAG 2.2 AA 检查和修复。先用语义元素和键盘能完成的交互，再考虑 ARIA。元素自带的语义不要再写一遍 role。

界面如果用了霓虹、玻璃或装饰动画，对比度和减弱动效仍然按这里处理。

## 图片

信息图片写清楚画面里是什么。装饰图片用空的 `alt=""`。不要写 `alt="image"` 或文件名。

```html
<img src="/photo.jpg" alt="仓库入口的装卸台" />
<img src="/divider.svg" alt="" />
```

## 表单

每个控件都有可见的标签，用 `for` 和 `id` 关联。Vue 里属性名仍是 `for`，React 里写成 `htmlFor`。

约束用 `required`，不要只写 `aria-required`。错误提示渲染出来之后，才给控件加上 `aria-describedby` 和 `aria-invalid="true"`。没有错误时，不要指向一个不存在的 id。

```html
<label for="email">邮箱地址</label>
<input id="email" type="email" required autocomplete="email" />

<label for="password">密码</label>
<input
  id="password"
  type="password"
  required
  autocomplete="current-password"
  aria-invalid="true"
  aria-describedby="password-error"
/>
<p id="password-error" role="alert">密码至少需要 8 个字符</p>
```

上面是出错时的写法。校验通过后去掉 `aria-invalid` 和 `aria-describedby`，并移除错误节点。

## 按钮和焦点

原生 `button` 已经响应 Enter 和 Space，不要再绑 `keydown` 去调用点击处理函数。Space 应在松开时触发，提前到按下会和系统行为不一致。

只有图标的按钮要有可访问名称。

```html
<button type="button">保存</button>
<button type="button" aria-label="关闭">
  <svg aria-hidden="true" viewBox="0 0 24 24"><!-- 图标 --></svg>
</button>
```

```css
:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

/* 鼠标点击不留焦点环，键盘焦点仍然保留 */
:focus:not(:focus-visible) {
  outline: none;
}
```

不要只写 `outline: none`。

## 对话框

Tab 必须留在对话框里。关闭或卸载时把焦点还给打开它的控件。父组件用条件渲染卸掉对话框时，在清理函数里归还焦点，不能只写在 `isOpen === false` 的分支里，那个分支不会执行。

对话框以外的页面内容加上 `inert`，避免屏幕阅读器仍能读到后面。

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  tabindex="-1"
>
  <h2 id="dialog-title">删除这条记录</h2>
  <button type="button">取消</button>
  <button type="button">删除</button>
</div>
```

```javascript
// requestClose 负责把对话框从页面拿掉。返回的函数在关闭或卸载时调用
function openDialog(dialog, requestClose) {
  const previouslyFocused = document.activeElement

  function focusable() {
    return [...dialog.querySelectorAll(
      'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
    )].filter((el) => el.getClientRects().length > 0)
  }

  function onKeyDown(event) {
    if (event.key === 'Escape') {
      event.preventDefault()
      requestClose()
      return
    }
    if (event.key !== 'Tab') return

    const items = focusable()
    if (items.length === 0) {
      event.preventDefault()
      dialog.focus()
      return
    }

    const first = items[0]
    const last = items[items.length - 1]
    const active = document.activeElement

    // 在首尾循环，避免 Tab 离开对话框
    if (event.shiftKey && (active === first || !dialog.contains(active))) {
      event.preventDefault()
      last.focus()
    } else if (!event.shiftKey && (active === last || !dialog.contains(active))) {
      event.preventDefault()
      first.focus()
    }
  }

  dialog.addEventListener('keydown', onKeyDown)
  const items = focusable()
  ;(items[0] ?? dialog).focus()

  return function closeDialog() {
    dialog.removeEventListener('keydown', onKeyDown)
    if (previouslyFocused instanceof HTMLElement) previouslyFocused.focus()
  }
}
```

`requestClose` 里先卸掉对话框，再调用 `closeDialog()`。条件渲染时，把 `closeDialog()` 放进卸载清理，不要放进 `isOpen === false` 的分支。

## 对比度

正文和背景至少 4.5:1。大号文字（常规 24px 或粗体约 19px 以上）和界面组件至少 3:1。数值要计算，不要写「看起来对比度够了」。

不要只靠颜色区分状态，同时给出文字或图标。

```css
.status-success::before {
  content: '✓ ';
}
```

## 页面结构

`header`、`main`、`nav`、`footer` 已经有语义，不要再加 `role="banner"`、`role="main"`、`role="contentinfo"`。页面上有多个导航时，给 `nav` 加不同的 `aria-label`。每个页面一个 `h1`，并提供跳到主内容的链接。

```html
<a href="#main-content">跳到主内容</a>
<header>
  <nav aria-label="主导航">
    <a href="/">首页</a>
  </nav>
</header>
<main id="main-content">
  <h1>页面标题</h1>
</main>
<footer>
  <p>页脚</p>
</footer>
```

## 动效

非必要的位移、闪烁和自动播放，在用户开启减弱动效时关掉。不要用一条作用在 `*` 上的 `!important` 去覆盖整个组件库，只停掉本次添加的装饰动画。

```css
@media (prefers-reduced-motion: reduce) {
  .promo-banner {
    animation: none;
    transition: none;
  }
}
```

## 提交前检查

- 信息图片有 alt，装饰图片的 alt 为空
- 控件有标签；错误出现时才关联描述
- 用 `button` 或链接完成操作，不把点击绑在没有键盘支持的 `div` 上
- 只用键盘能完成操作，焦点可见，对话框里 Tab 不逃逸
- 对比度按 4.5:1 和 3:1 量过，状态不只靠颜色
- 系统开启减弱动效时，装饰动画停掉
