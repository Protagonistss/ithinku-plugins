<h1 align="center">✨ UI Design Plugin</h1>

<p align="center">
  <strong>做出对齐、克制、状态完整的产品界面。用户点名风格时才换皮肤</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Plugin-Claude_Code-blueviolet.svg" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
</p>

---

默认做产品界面：一套间距、一套字号、一种圆角、一个强调色，并补齐悬停、焦点、禁用、错误和空状态。

## 🎯 设计理念 (Philosophy)

- **产品完成度**：表面靠边框和背景色分开，阴影只留给浮层。控件高度、图标尺寸和数字对齐保持一致。
- **不套流行皮肤**：用户没点名时，不用渐变底、硬阴影、毛玻璃、霓虹、bento 和展示页式主视觉。
- **沿用现有系统**：仓库已有颜色、字号和组件时只扩展状态，不平行再造一套视觉。

## 🚀 核心能力

- **[Core Design](./skills/ui-design-core/SKILL.md)**：用户说不清问题时，自己看当前页面的尺度、状态、布局和交互，并直接改。已有设计系统沿用，用户没点名风格时不换皮肤。
- **[A11y Check](./skills/ui-design-a11y/SKILL.md)**：按 WCAG 2.2 AA 检查语义、键盘、焦点、对比度和减弱动效。

## 🎨 场景示例

### 改现有页面
> “改一下这个列表页。”或只丢出页面、说不出具体问题。技能自己看主任务、筛选位置、空状态和按钮层级，然后直接改。不要追问想改哪一点，也不要给几套方案让用户选。

### 点名风格
> “登录页改成 Neo-Brutalism：高饱和橙色、厚黑边和硬阴影。间距和表单状态仍然做完整。”

## ⚙️ 技术预设

样式、动效和图标跟仓库现有方案。项目里没有 Framer Motion、Lucide 或 Tailwind 时，不要为了这个插件新增它们。动效优先用 CSS，并尊重减弱动效设置。
