---
name: ui-design-core
description: >-
  做页面、改现有界面、布局、交互、配色或动效时使用。
  用户给出页面或要求做界面时使用，不必等用户指出布局和交互上的问题。
  无障碍问题用 ui-design-a11y。已有设计系统时沿用它的尺度，不要另起一套皮肤。
---

# UI Design

先看仓库里已有的样式、组件库和框架。Vue 项目不要写出 React 组件，也不要引入项目里没有的动效库或图标库。类名落在仓库已有的方案上：Tailwind、CSS Modules、Vue scoped 或普通 CSS。

很多用户说不出哪里别扭，也给不出改法。不要追问风格、布局，或「你更想先改哪一点」，也不要先给几套方案让用户挑。自己看当前页面，缺的尺度、状态、布局和交互直接补上。

对比度、焦点和减弱动效交给 `ui-design-a11y`。成品不能低于 WCAG 2.2 AA。

## 默认做成产品界面

用户没点名某种风格时，做安静、对齐、可完成操作的产品界面。页面松散、主操作不明显、状态缺失时，直接收紧层级、间距、对齐和状态。不要等用户说「太平」「没有产品感」，也不要改成野兽派、玻璃拟态、杂志风、赛博朋克或 bento。

用户只给了一个页面、一张截图，或只说「做一下」「优化一下」时，按上面的判断做完这一页。字段、数据和业务步骤保留。

已有设计系统或组件库时，只使用它的颜色、字号、间距和圆角。缺的状态按同一套补上，不要平行再造一套视觉。

### 尺度

整页只用一套，不要混用拍脑袋的数值。

| 角色 | 约定 |
|---|---|
| 间距 | 以 4px 为基数：4、8、12、16、24、32、48。相关元素靠近，组与组之间加大一档 |
| 字号 | 产品界面控制在 4 档以内，例如 12、14、16、20。正文 14，标题只比正文大一到两档 |
| 行高 | 界面文字 1.4 到 1.5，长文 1.6。同一档字号只用一种行高 |
| 圆角 | 全站一个值。产品界面用 6px 或 8px。胶囊形只给明确的标签或开关 |
| 颜色 | 背景、表面、边框、正文、次要文字、一个强调色、一个危险色。强调色只用于主操作和当前项 |
| 字体 | 产品界面只用一种。优先项目已有字体；没有则用系统无衬线字体。不要默认 Inter、Roboto、Arial、Playfair Display |
| 图标 | 同一套、同一尺寸，通常 16px。不要用 emoji 当图标 |
| 数字 | 表格和金额用 `tabular-nums`，小数点和右对齐 |

展示页可以加大标题和留白，仍然用这一套基数，只是跳到更大的档，而不是另写一组随意的 `padding: 18px`、`font-size: 15px`。

### 完成度

表面上的区分靠背景色和 1px 边框。阴影只留给浮层：下拉、弹层、抽屉。不要给每张卡片加阴影，也不要在悬停时把卡片抬起来。

可点击的控件都要有默认、悬停、键盘焦点、禁用。输入框还要有错误态。列表和表格要有空状态：一句说明加一个主动作，不要放装饰插画。

同一页面上，按钮高度、输入框高度、图标尺寸和图标与文字的间距各自只有一种。内容边线对齐到同一列，不要靠视觉大概对齐。

产品页保持可扫描的密度。应用里的页头不要做成落地页主视觉，表格和表单不要被大段空白或巨号标题撑开。

动效只表示状态变化，例如菜单展开、按下反馈。时长 120ms 到 200ms。表单、表格和列表不要给每一行加动画，并尊重 `prefers-reduced-motion`。

## 布局和交互

改现有页面，或用户只给了页面、没说出问题时，自己对照下面的规则看，然后直接改。不要等用户描述问题，也不要先列建议再问做不做。

只改当前这个视图里让主任务变慢的布局和交互。字段、数据和业务步骤保留。视觉仍用上面的尺度，不靠换皮肤。不扩到用户没打开的其他页面。

### 布局

- 一页一件主任务。主按钮全页只有一个，放在标题行右侧；表单则放在字段组末尾
- 搜索和筛选紧挨着它们作用的列表。已选条件可见，并且能单独清除
- 表单单列，标签在输入框上方。相关字段分成组，组标题用次要文字
- 表格把用来识别的列放左边，行内主操作放右边，不要等悬停才出现
- 长页面的主操作在首屏可见。超过一屏的表单可以把操作条固定在底部
- 窄屏改成上下排列。正文不要小于 14px

### 交互

- 按钮分主操作、次操作、危险操作。确认框里的按钮写动作本身，例如「删除」，不要写「确定」
- 可以撤销的操作提供撤销。不能撤销的才弹出确认
- 提交后按钮进入进行中。失败原因回到刚才的字段；成功后留在用户还要继续处理的列表或详情，不要跳到一张空白完成页
- 会请求数据的区域分别给出加载、空和失败。失败提供重试
- 控件被禁用时，原因写在它旁边
- 字段在失焦时校验，错误贴着该字段
- 悬停不能是发现某个操作的唯一方式

不为了这些规则加操作引导、多步向导或额外页面。任务本身就很长时，才把一步拆开。

### 不要做成这样

这些是默认要避开的外观。用户没点名时，一个都不要用：

- 整页紫、蓝或粉的线性渐变，以及渐变字
- 黑粗边、实色硬阴影、高饱和色块
- 毛玻璃卡片、光斑、噪点底纹
- 霓虹、故障风、发光描边
- 用 bento 拼成的首页，或页头加主视觉加三列特性作为整个产品
- 每张卡片白底、软阴影、悬停上浮
- 多种圆角、多种阴影、多种强调色出现在同一页
- 为了「有设计感」把数据后台做成展示页

## 用户点名一种风格时

只有用户明确说出风格名字时才使用对应外观，并且只用一种。间距、字号、状态和对比度仍按上面的尺度做完。不要把硬阴影、毛玻璃和渐变字叠在一起。

点名之后仍然补齐悬停、焦点、禁用、错误和空状态。风格不是只做一张好看的卡片。

## 示例

下面是没有设计系统时的产品界面起点。仓库里已有 token 时，用仓库的值替换这些变量，不要两套并存。

```css
:root {
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --font-size-sm: 12px;
  --font-size-md: 14px;
  --font-size-lg: 20px;
  --radius: 8px;
  --color-bg: #f5f6f8;
  --color-surface: #fff;
  --color-border: #e4e7ec;
  --color-text: #172033;
  --color-muted: #4a5568;
  --color-accent: #1d4ed8;
  --color-danger: #b42318;
  font-family: ui-sans-serif, system-ui, sans-serif;
  color: var(--color-text);
  background: var(--color-bg);
}

.panel {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: var(--space-4);
}

.btn {
  height: 36px;
  padding: 0 var(--space-3);
  border: 1px solid transparent;
  border-radius: var(--radius);
  background: var(--color-accent);
  color: #fff;
  font-size: var(--font-size-md);
  transition: background-color 160ms cubic-bezier(0.2, 0, 0, 1);
}

.btn:hover {
  background: #1e40af;
}

.btn:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

.btn:disabled {
  background: #d0d5dd;
  color: #667085;
}

.field {
  height: 36px;
  width: 100%;
  padding: 0 var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  background: var(--color-surface);
  font-size: var(--font-size-md);
}

.field[aria-invalid="true"] {
  border-color: var(--color-danger);
}

.field-error {
  margin-top: var(--space-2);
  color: var(--color-danger);
  font-size: var(--font-size-sm);
}

@media (prefers-reduced-motion: reduce) {
  .btn {
    transition: none;
  }
}
```
